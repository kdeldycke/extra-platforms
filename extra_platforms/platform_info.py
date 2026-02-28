# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Platform-specific information gathering.

This module provides utilities to fetch detailed version and codename information
for all platforms: Linux distributions (via ``/etc/os-release``), macOS and Windows.

.. seealso::
    The `os-release specification
    <https://www.freedesktop.org/software/systemd/man/latest/os-release.html>`_
    defines the format and fields of ``/etc/os-release``.
"""

from __future__ import annotations

import os
import platform
import re
import shlex
from functools import cache

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Iterable


def _parse_os_release_content(lines: Iterable[str]) -> dict[str, str]:
    """Parse os-release file content into a dictionary.

    Uses :class:`shlex.shlex` in POSIX mode to handle quoting rules defined in the
    `os-release specification
    <https://www.freedesktop.org/software/systemd/man/latest/os-release.html>`_.

    Keys are lowercased. A ``codename`` key is extracted from ``VERSION`` if present,
    with ``VERSION_CODENAME`` taking precedence over ``UBUNTU_CODENAME``.

    :param lines: Iterable of lines from an os-release file.
    :return: Dictionary of parsed key-value pairs.
    """
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().lower()
        # Use shlex to unquote the value.
        lexer = shlex.shlex(value, posix=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
        result[key] = " ".join(tokens) if tokens else ""

    # Extract codename from VERSION field if not already present.
    if "version_codename" not in result and "version" in result:
        # Match patterns like "(Focal Fossa)" or ", Focal Fossa".
        match = re.search(r"\((\D+)\)|,\s*(\D+)", result["version"])
        if match:
            result["version_codename"] = (match.group(1) or match.group(2)).strip()

    # UBUNTU_CODENAME is a fallback for VERSION_CODENAME.
    if "version_codename" not in result and "ubuntu_codename" in result:
        result["version_codename"] = result["ubuntu_codename"]

    return result


@cache
def _parse_os_release() -> dict[str, str]:
    """Read and parse the os-release file.

    Tries ``/etc/os-release`` first, then ``/usr/lib/os-release`` as fallback per the
    specification.

    :return: Dictionary of parsed key-value pairs, or empty dict if no file found.
    """
    for path in ("/etc/os-release", "/usr/lib/os-release"):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                return _parse_os_release_content(f)
    return {}


# Normalization table for distro IDs that differ between os-release and distro library.
_OS_RELEASE_ID_NORMALIZATION: dict[str, str] = {
    "ol": "oracle",
    "opensuse-leap": "opensuse",
}


@cache
def os_release_id() -> str:
    """Return the normalized distribution ID from os-release.

    Lowercases the ``ID`` field, replaces spaces with underscores, and applies
    a normalization table for known ID differences.

    :return: Normalized distribution ID, or empty string if absent.
    """
    raw_id = _parse_os_release().get("id", "")
    normalized = raw_id.lower().replace(" ", "_")
    return _OS_RELEASE_ID_NORMALIZATION.get(normalized, normalized)


@cache
def linux_info() -> dict[str, Any]:
    """Fetch detailed Linux distribution information from os-release.

    Returns a dictionary with the same structure as ``distro.info()`` for
    consistency, including:

    - ``id``: Distribution ID (e.g., "ubuntu", "fedora")
    - ``version``: Full version string (e.g., "22.04")
    - ``version_parts``: Dictionary with ``major``, ``minor``, ``build_number``
    - ``like``: Space-separated list of related distributions
    - ``codename``: Distribution codename (e.g., "jammy")

    :return: Dictionary containing Linux distribution details.
    """
    data = _parse_os_release()
    dist_id = os_release_id()
    version = data.get("version_id", "")
    parts = version.split(".", 2) if version else []
    return {
        "id": dist_id,
        "version": version,
        "version_parts": {
            "major": parts[0] if len(parts) > 0 else "",
            "minor": parts[1] if len(parts) > 1 else "",
            "build_number": parts[2] if len(parts) > 2 else "",
        },
        "like": data.get("id_like", ""),
        "codename": data.get("version_codename", ""),
    }


def invalidate_os_release_cache() -> None:
    """Clear caches for all os-release functions."""
    _parse_os_release.cache_clear()
    os_release_id.cache_clear()
    linux_info.cache_clear()


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
