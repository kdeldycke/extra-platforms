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
"""Platform-specific information gathering.

This module provides utilities to fetch detailed version and codename information
for macOS and Windows platforms, extending the capabilities of the ``distro`` library
which primarily focuses on Linux distributions.

.. hint::
    This module complement the ``distro`` library by extending [support to non-Linux
    platforms like macOS and Windows](https://github.com/python-distro/distro/issues/177).

    It has the potential to serve as a total replacement of ``distro`` in the future, if
    the later is abandoned.
"""

from __future__ import annotations

import platform

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


MACOS_CODENAMES: dict[tuple[str, str | None], str] = {
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

.. seealso::
    - https://en.wikipedia.org/wiki/Template:MacOS_versions
    - https://docs.python.org/3/library/platform.html#platform.mac_ver

.. hint::
    There is this oddity where some beta release of macOS Tahoe report major
    version as ``16`` instead of ``15`` or ``26``. We choose to not handle this case
    for now, as we consider this a glitch in macOS history, and do not have a proper
    way to detect beta versions at this time.
"""


def get_macos_codename(major: str | None = None, minor: str | None = None) -> str:
    """Get the macOS codename for a given version.

    Args:
        major: The major version number (e.g., "10", "11", "14").
        minor: The minor version number (e.g., "0", "15"). For macOS 11+,
            this can be None as codenames are tied to major versions only.

    Returns:
        The codename for the macOS version (e.g., "Sonoma", "Ventura").

    Raises:
        ValueError: If no codename matches the given version, or if multiple
            codenames match (which shouldn't happen with valid data).
    """
    matches = set()
    for (major_key, minor_key), codename in MACOS_CODENAMES.items():
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


def macos_info() -> dict[str, Any]:
    """Fetch detailed macOS version information.

    Returns a dictionary with the same structure as ``distro.info()`` for
    consistency, including:

    - ``version``: Full version string (e.g., "14.2.1")
    - ``version_parts``: Dictionary with ``major``, ``minor``, ``build_number``
    - ``codename``: The macOS codename (e.g., "Sonoma")

    Returns:
        A dictionary containing macOS version details.

    Raises:
        ValueError: If the current macOS version cannot be mapped to a codename.
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
        "codename": get_macos_codename(major, minor),
    }


def windows_info() -> dict[str, Any]:
    """Fetch detailed Windows version information.

    Returns a dictionary with the same structure as ``distro.info()`` for
    consistency, including:

    - ``version``: Full version string (e.g., "10.0.19041")
    - ``version_parts``: Dictionary with ``major``, ``minor``, ``build_number``
    - ``codename``: A combination of version and edition (e.g., "10 Enterprise")

    Returns:
        A dictionary containing Windows version details.

    .. todo::
        Get even more details for Windows version. See inspirations from:
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
