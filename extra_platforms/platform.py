# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Platforms, also known as Operating Systems.

Everything here can be aggressively cached and frozen, as it's only compute
platform-dependent values.
"""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

import distro

# TODO: eliminate boltons dependency
from boltons.iterutils import remap

from . import detection

_MACOS_CODENAMES = {
    ("10", "0"): "Cheetah",
    ("10", "1"): "Puma",
    ("10", "2"): "Jaguar",
    ("10", "3"): "Panther",
    ("10", "4"): "Tiger",
    ("10", "5"): "Leopard",
    ("10", "6"): "Snow Leopard",
    ("10", "7"): "Lion",
    ("10", "8"): "Mountain Lion",
    ("10", "9"): "Mavericks",
    ("10", "10"): "Yosemite",
    ("10", "11"): "El Capitan",
    ("10", "12"): "Sierra",
    ("10", "13"): "High Sierra",
    ("10", "14"): "Mojave",
    ("10", "15"): "Catalina",
    ("11", None): "Big Sur",
    ("12", None): "Monterey",
    ("13", None): "Ventura",
    ("14", None): "Sonoma",
    ("15", None): "Sequoia",
}
"""Maps macOS ``(major, minor)`` version parts to release code name.

See:
- https://en.wikipedia.org/wiki/Template:MacOS_versions
- https://docs.python.org/3/library/platform.html#platform.mac_ver
"""


def _get_macos_codename(major: str | None = None, minor: str | None = None) -> str:
    matches = set()
    for (major_key, minor_key), codename in _MACOS_CODENAMES.items():
        if minor_key is not None and minor_key != minor:
            continue
        if major_key == major:
            matches.add(codename)
    if not matches:
        raise ValueError(f"No macOS codename match version ({major!r}, {minor!r})")
    if len(matches) != 1:
        raise ValueError(
            f"Version {major}.{minor} match multiple codenames: {matches!r}"
        )
    return matches.pop()


def _recursive_update(
    a: dict[str, Any], b: dict[str, Any], strict: bool = False
) -> dict[str, Any]:
    """Like standard ``dict.update()``, but recursive so sub-dict gets updated.

    Ignore elements present in ``b`` but not in ``a``. Unless ``strict`` is set to
    `True`, in which case a `ValueError` exception will be raised.
    """
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = _recursive_update(a[k], v, strict=strict)
        # Ignore elements unregistered in the template structure.
        elif k in a:
            a[k] = b[k]
        elif strict:
            msg = f"Parameter {k!r} found in second dict but not in first."
            raise ValueError(msg)
    return a


def _remove_blanks(
    tree: dict,
    remove_none: bool = True,
    remove_dicts: bool = True,
    remove_str: bool = True,
) -> dict:
    """Returns a copy of a dict without items whose values blanks.

    Are considered blanks:
    - `None` values
    - empty strings
    - empty `dict`

    The removal of each of these class can be skipped by setting ``remove_*``
    parameters.

    Dictionarries are inspected recursively and their own blank values are removed.
    """

    def visit(path, key, value) -> bool:
        """Ignore some class of blank values depending on configuration."""
        if remove_none and value is None:
            return False
        if remove_dicts and isinstance(value, dict) and not len(value):
            return False
        if remove_str and isinstance(value, str) and not len(value):
            return False
        return True

    return remap(tree, visit=visit)  # type: ignore[no-any-return]


@dataclass(frozen=True)
class Platform:
    """A platform can identify multiple distributions or OSes with the same
    characteristics.

    It has a unique ID, a human-readable name, and boolean to flag current platform.
    """

    id: str
    """Unique ID of the platform."""

    name: str
    """User-friendly name of the platform."""

    icon: str = field(repr=False, default="❓")
    """Icon of the platform."""

    url: str = field(repr=False, default="")
    """URL to the platform's official website."""

    def __post_init__(self):
        """Validate and normalize platform fields:

        - Ensure the platform ID, name, icon and URL are not empty.
        - Ensure the URL starts with ``https://``.
        - Set the ``current`` field.
        - Populate the docstring.
        """
        assert self.id, "Platform ID cannot be empty."
        assert self.name, "Platform name cannot be empty."
        assert self.icon, "Platform icon cannot be empty."
        assert self.url, "Platform URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        object.__setattr__(self, "__doc__", f"Identify {self.name}.")

    @cached_property
    def short_desc(self) -> str:
        """Returns a short description of the platform.

        Mainly used to produce docstrings for function dynamically generated for each
        group.
        """
        return self.name

    @cached_property
    def current(self) -> bool:
        """Returns whether the current platform is this one.

        This is a property to avoid calling all platform detection heuristics on
        ``Platform`` objects creation, which happens at module import time.
        """
        return getattr(detection, f"is_{self.id}")()  # type: ignore[no-any-return]

    def info(self) -> dict[str, str | bool | None | dict[str, str | None]]:
        """Returns all platform attributes we can gather."""
        info = {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
            "current": self.current,
            # Extra fields from distro.info().
            "distro_id": None,
            "version": None,
            "version_parts": {"major": None, "minor": None, "build_number": None},
            "like": None,
            "codename": None,
        }
        if self.current:
            # Get extra Linux distribution info from distro.
            distro_info = dict(distro.info())
            # Rename distro ID to avoid conflict with our own ID.
            distro_info["distro_id"] = distro_info.pop("id")
            info = _recursive_update(info, _remove_blanks(distro_info), strict=True)

            # Add extra macOS infos.
            if self.id == "macos":
                info = _recursive_update(info, self._macos_infos(), strict=True)

            # Add extra Windows infos.
            elif self.id == "windows":
                info = _recursive_update(info, self._windows_infos(), strict=True)

        return info  # type: ignore[return-value]

    @staticmethod
    def _macos_infos() -> dict[str, Any]:
        """Fetch extra macOS infos.

        Returns the same dict structure as ``distro.info()``.
        """
        release, _versioninfo, _machine = platform.mac_ver()
        parts = dict(zip(("major", "minor", "build_number"), release.split(".", 2)))
        major = parts.get("major")
        minor = parts.get("minor")
        build_number = parts.get("build_number")
        return {
            "version": release,
            "version_parts": {
                "major": major,
                "minor": minor,
                "build_number": build_number,
            },
            "codename": _get_macos_codename(major, minor),
        }

    @staticmethod
    def _windows_infos() -> dict[str, Any]:
        """Fetch extra Windows infos.

        Returns the same dict structure as ``distro.info()``.

        .. todo:
            Get even more details for windows version? See inspirations from:
            https://github.com/saltstack/salt/blob/246d066/salt/grains/core.py#L1432-L1488
        """
        release, _version, _csd, _ptype = platform.win32_ver()
        parts = dict(zip(("major", "minor", "build_number"), release.split(".", 2)))
        major = parts.get("major")
        minor = parts.get("minor")
        build_number = parts.get("build_number")
        return {
            "version": release,
            "version_parts": {
                "major": major,
                "minor": minor,
                "build_number": build_number,
            },
            "codename": " ".join((release, platform.win32_edition())),
        }
