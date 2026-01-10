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
"""Trait base class for architectures, platforms, CI systems, and more.

A trait represents a distinguishing characteristic of a runtime environment.
Each trait has a unique ID, a human-readable name, an icon, and the ability
to detect if it matches the current environment.

Data associated with traits can be aggressively cached and frozen, as they're only
computed based on environment-dependent values.
"""

from __future__ import annotations

import platform
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property

import distro

import extra_platforms

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


def _recursive_update(
    a: dict[str, Any], b: dict[str, Any], strict: bool = False
) -> dict[str, Any]:
    """Like standard ``dict.update()``, but recursive so sub-dict gets updated.

    Ignore elements present in ``b`` but not in ``a``. Unless ``strict`` is set to
    ``True``, in which case a ``ValueError`` exception will be raised.
    """
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = _recursive_update(a[k], v, strict=strict)
        # Ignore elements unregistered in the template structure.
        elif k in a:
            a[k] = b[k]
        elif strict:
            raise ValueError(f"Parameter {k!r} found in second dict but not in first.")
    return a


def _remove_blanks(
    tree: dict,
    remove_none: bool = True,
    remove_dicts: bool = True,
    remove_str: bool = True,
) -> dict:
    """Returns a copy of a dict without items whose values blanks.

    Are considered blanks:

    - ``None`` values
    - empty strings
    - empty ``dict``

    The removal of each of these class can be skipped by setting ``remove_*``
    parameters.

    Dictionarries are inspected recursively and their own blank values are removed.
    """
    result = {}
    for key, value in tree.items():
        # Skip None values if configured.
        if remove_none and value is None:
            continue

        # Recursively process nested dicts.
        if isinstance(value, dict):
            cleaned = _remove_blanks(value, remove_none, remove_dicts, remove_str)
            # Skip empty dicts if configured.
            if remove_dicts and not cleaned:
                continue
            result[key] = cleaned
        # Skip empty strings if configured.
        elif remove_str and isinstance(value, str) and not value:
            continue
        else:
            result[key] = value

    return result


@dataclass(frozen=True)
class Trait(ABC):
    """Base class for system traits like platforms and architectures.

    A trait is a distinguishing characteristic of the runtime environment that can
    be detected and identified. Examples include:

    - Operating systems (macOS, Linux, Windows)
    - CPU architectures (x86_64, ARM64)
    - CI/CD environments (GitHub Actions, GitLab CI)

    Each trait has:

    - A unique ID for programmatic use
    - A human-readable name
    - An icon for visual representation
    - A URL to official documentation
    - A ``current`` property that detects if this trait matches the runtime
    """

    id: str
    """Unique ID of the trait."""

    name: str
    """User-friendly name of the trait."""

    icon: str = field(repr=False, default="❓")
    """Icon of the trait."""

    url: str = field(repr=False, default="")
    """URL to the trait's official website or documentation."""

    detection_func_id: str = field(repr=False, init=False)
    """ID of the detection function for this trait.

    The detection function is expected to be named ``is_<id>()`` and located at the root
    of the ``extra_platforms`` module.
    """

    def __post_init__(self) -> None:
        """Validate and normalize trait fields.

        - Ensure the trait ID, name, icon and URL are not empty.
        - Ensure the URL starts with ``https://``.
        - Set the detection function ID based on the trait ID.
        - Populate the docstring.
        """
        assert self.id, f"{self.__class__.__name__} ID cannot be empty."
        assert self.name, f"{self.__class__.__name__} name cannot be empty."
        assert self.icon, f"{self.__class__.__name__} icon cannot be empty."
        assert self.url, f"{self.__class__.__name__} URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        object.__setattr__(self, "detection_func_id", f"is_{self.id}")

        object.__setattr__(self, "__doc__", f"Identify {self.name}.")

    @cached_property
    def short_desc(self) -> str:
        """Returns a short description of the trait.

        Mainly used to produce docstrings for functions dynamically generated for each
        group.
        """
        return self.name

    @cached_property
    def current(self) -> bool:
        """Returns whether the current environment matches this trait.

        The detection function is dynamically looked up based on the trait ID, and is
        expected to be found at the root of the ``extra_platforms`` module.

        Raises ``NotImplementedError`` if a detection function cannot be found.

        .. hint::
            This is a property to avoid calling all detection heuristics on
            ``Trait`` objects creation, which happens at module import time.
        """
        func = getattr(extra_platforms, self.detection_func_id, None)
        if not func:
            raise NotImplementedError(
                f"Detection function {self.detection_func_id}() is not implemented."
            )
        return func()  # type: ignore[no-any-return]

    @abstractmethod
    def info(self) -> dict:
        """Returns all trait attributes that can be gathered.

        Subclasses should override this to include trait-specific information.
        """
        ...

    def _base_info(self) -> dict[str, str | bool | None]:
        """Returns the base info dictionary common to all traits."""
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
            "current": self.current,
        }


@dataclass(frozen=True)
class Architecture(Trait):
    """A CPU architecture identifies a `processor instruction set
    <https://en.wikipedia.org/wiki/Instruction_set_architecture>`_.

    It has a unique ID, a human-readable name, and boolean to flag current architecture.
    """

    icon: str = field(repr=False, default="▣")
    """Icon of the architecture."""

    def __post_init__(self) -> None:
        """Validate and normalize architecture fields."""
        super().__post_init__()
        # Customize the docstring for architectures.
        object.__setattr__(self, "__doc__", f"Identify {self.name} architecture.")

    def info(self) -> dict[str, str | bool | None]:
        """Returns all architecture attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **self._base_info(),
            "machine": None,
            "processor": None,
        }
        if self.current:
            info["machine"] = platform.machine() or None
            info["processor"] = platform.processor() or None

        return info


@dataclass(frozen=True)
class Platform(Trait):
    """A platform can identify multiple distributions or OSes with the same
    characteristics.

    It has a unique ID, a human-readable name, and boolean to flag current platform.
    """

    icon: str = field(repr=False, default="❓")
    """Icon of the platform."""

    def __post_init__(self) -> None:
        """Validate and normalize platform fields."""
        super().__post_init__()

    def info(self) -> dict[str, str | bool | None | dict[str, str | None]]:
        """Returns all platform attributes we can gather."""
        info: dict[str, str | bool | None | dict[str, str | None]] = {
            **self._base_info(),
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

        return info

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
        ("26", None): "Tahoe",
    }
    """Maps macOS ``(major, minor)`` version parts to release code name.

    See:

    - https://en.wikipedia.org/wiki/Template:MacOS_versions
    - https://docs.python.org/3/library/platform.html#platform.mac_ver
    """

    @classmethod
    def _get_macos_codename(
        cls, major: str | None = None, minor: str | None = None
    ) -> str:
        matches = set()
        for (major_key, minor_key), codename in cls._MACOS_CODENAMES.items():
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

    @classmethod
    def _macos_infos(cls) -> dict[str, Any]:
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
            "codename": cls._get_macos_codename(major, minor),
        }

    @classmethod
    def _windows_infos(cls) -> dict[str, Any]:
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


@dataclass(frozen=True)
class CI(Trait):
    """A CI/CD environment identifies a continuous integration platform.

    It has a unique ID, a human-readable name, and boolean to flag current CI.
    """

    icon: str = field(repr=False, default="♲")
    """Icon of the CI environment."""

    def __post_init__(self) -> None:
        """Validate and normalize CI fields."""
        super().__post_init__()
        # Customize the docstring for CI environments.
        object.__setattr__(self, "__doc__", f"Identify {self.name} CI environment.")

    def info(self) -> dict[str, str | bool | None]:
        """Returns all CI attributes we can gather."""
        return {
            **self._base_info(),
        }
