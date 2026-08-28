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
for all platforms: Linux distributions (via `/etc/os-release`), macOS and Windows.

Linux reads `/etc/os-release`, then `/usr/lib/os-release`. When neither file is
readable, `_hostnamectl_os_release()` asks `systemd-hostnamed` for the same
identity over D-Bus and rebuilds the os-release fields from its answer.

```{seealso}
The [`os-release` specification](https://www.freedesktop.org/software/systemd/man/latest/os-release.html)
defines the format and fields of `/etc/os-release`.
```
"""

from __future__ import annotations

import os
import platform
import re
import shlex
import shutil
import subprocess
from functools import cache

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any


CODENAME_RE = re.compile(r"\((\D+)\)|,\s*(\D+)")
"""Matches a codename trailing a version string.

The [`os-release` specification](https://www.freedesktop.org/software/systemd/man/latest/os-release.html)
puts no codename in `VERSION`, but distributions append one anyway, either
parenthesized (``22.04.3 LTS (Jammy Jellyfish)``) or after a comma
(``10, Buster``). Both forms exclude digits, which keeps the version itself out
of the match.
"""


def _codename_from_version(version: str) -> str:
    """Extract the codename trailing a version string.

    Reads the same parenthesized or comma-separated forms from an os-release
    `VERSION` field and from a `PRETTY_NAME`, since a pretty name ends on the
    version its `VERSION` field carries.

    :param version: A version string, or any string ending on one.
    :return: The codename, or an empty string when the version carries none.
    """
    match = CODENAME_RE.search(version)
    if not match:
        return ""
    return (match.group(1) or match.group(2)).strip()


def _parse_os_release_content(lines: Iterable[str]) -> dict[str, str]:
    """Parse os-release file content into a dictionary.

    Uses {class}`shlex.shlex` in POSIX mode to handle quoting rules defined in the
    [`os-release` specification](https://www.freedesktop.org/software/systemd/man/latest/os-release.html).

    Keys are lowercased. A `codename` key is extracted from `VERSION` if present,
    with `VERSION_CODENAME` taking precedence over `UBUNTU_CODENAME`.

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
        codename = _codename_from_version(result["version"])
        if codename:
            result["version_codename"] = codename

    # UBUNTU_CODENAME is a fallback for VERSION_CODENAME.
    if "version_codename" not in result and "ubuntu_codename" in result:
        result["version_codename"] = result["ubuntu_codename"]

    return result


CPE_ID_OVERRIDES: dict[str, str] = {
    "alt:server": "altlinux",
    "amazon:amazon_linux": "amzn",
    "amazon:linux": "amzn",
    "opensuse:leap": "opensuse-leap",
    "oracle:linux": "ol",
    "redhat:enterprise_linux": "rhel",
    # Scientific Linux 7 declares ID="rhel" in its own os-release file.
    "scientificlinux:scientificlinux": "rhel",
    "slackware:slackware_linux": "slackware",
}
"""Maps a CPE ``vendor:product`` pair to the os-release `ID` of the same system.

A CPE product name and an os-release `ID` are set by different bodies, so they
agree for most distributions and diverge for some. Only the divergent pairs are
listed here: `_parse_cpe_name()` uses the product itself for all the others,
which covers `almalinux`, `centos`, `cloudlinux`, `fedora`, `kvmibm`,
`opensuse`, `rocky` and `sles`.

Each entry is read from a real os-release file declaring both fields, as
collected in
[python-distro's test resources](https://github.com/python-distro/distro/tree/master/tests/resources/distros).
Add an entry only from such a file: the rule is to reproduce the `ID` the system
itself declares, never to pick the ID that looks right.
"""


def _parse_cpe_name(cpe_name: str) -> dict[str, str]:
    """Extract os-release fields from a CPE name.

    A [CPE](https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe)
    name reaches an os-release file in either of two bindings, which list their
    components in the same order. One positional read covers the pair:

    - the 2.2 URI binding, ``cpe:/o:fedoraproject:fedora:19``
    - the 2.3 formatted string, ``cpe:2.3:o:amazon:amazon_linux:2023``

    Components past the version (update, edition, language, ...) are ignored:
    ``cpe:/o:cloudlinux:cloudlinux:7.3:GA:server`` yields the same fields as
    ``cpe:/o:cloudlinux:cloudlinux:7.3``.

    :param cpe_name: A CPE name, in either binding.
    :return: Dictionary of os-release fields, or empty dict when the name is not
        a CPE naming an operating system.
    """
    if cpe_name.startswith("cpe:2.3:"):
        components = cpe_name[len("cpe:2.3:") :].split(":")
    elif cpe_name.startswith("cpe:/"):
        components = cpe_name[len("cpe:/") :].split(":")
    else:
        return {}

    part, vendor, product, version = ([*components, "", "", "", ""])[:4]
    # An os-release CPE_NAME always names an operating system.
    if part != "o":
        return {}

    # "*" (any) and "-" (not applicable) are CPE placeholders, not values.
    vendor, product, version = (
        "" if value in ("*", "-") else value for value in (vendor, product, version)
    )

    result = {"cpe_name": cpe_name}
    distro_id = CPE_ID_OVERRIDES.get(f"{vendor}:{product}", product)
    if distro_id:
        result["id"] = distro_id
    if version:
        result["version_id"] = version
    return result


def _parse_hostnamectl_content(lines: Iterable[str]) -> dict[str, str]:
    """Parse `hostnamectl` status output into os-release fields.

    The output is a list of ``Label: value`` lines, of which two carry the
    operating system identity:

    ```text
      Operating System: CloudLinux 7.6 (Vladimir Lyakhov)
           CPE OS Name: cpe:/o:cloudlinux:cloudlinux:7.6:GA:server
    ```

    `Operating System` is the `PRETTY_NAME` of the system, and `CPE OS Name` its
    `CPE_NAME`. All other lines describe the host, not the distribution, and are
    dropped.

    :param lines: Iterable of lines from `hostnamectl` status output.
    :return: Dictionary of os-release fields, empty when the output names no
        operating system.
    """
    fields: dict[str, str] = {}
    for line in lines:
        # Split on the first colon only: a CPE name holds colons of its own,
        # but a label never does.
        label, separator, value = line.partition(":")
        if not separator:
            continue
        fields[label.strip().lower()] = value.strip()

    result: dict[str, str] = {}

    cpe_name = fields.get("cpe os name", "")
    if cpe_name:
        result.update(_parse_cpe_name(cpe_name))

    pretty_name = fields.get("operating system", "")
    if pretty_name:
        result["pretty_name"] = pretty_name
        codename = _codename_from_version(pretty_name)
        if codename:
            result["version_codename"] = codename

    return result


@cache
def _hostnamectl_os_release() -> dict[str, str]:
    """Rebuild os-release fields from `systemd-hostnamed`.

    `hostnamectl` reads the operating system identity from `systemd-hostnamed`
    over D-Bus, so it answers from the init system's view of the file system
    instead of the caller's. That is what makes it a distinct source and not a
    second read of the same file: a process jailed away from `/etc/os-release`
    still reaches the real one through the bus. CloudLinux VMs virtualizing
    `/etc` per user are the reported case, where every other strategy comes back
    empty, as reported in
    [`python-distro/distro#240`](https://github.com/python-distro/distro/issues/240).

    ```{caution}
    The same property makes the answer the *host* identity when a container
    reaches the host bus. Reaching that case needs an image shipping no
    os-release file at all, which in practice ships no `hostnamectl` either, so
    this returns an empty result without ever querying the bus.
    ```

    Any failure degrades to an empty result: no `hostnamectl` binary, no
    systemd, or an unreachable bus.

    :return: Dictionary of os-release fields, or empty dict when the identity
        cannot be read.
    """
    # Testing for the binary rather than for Linux covers a systemd-less
    # distribution too, and spares every other platform a subprocess it can only
    # fail to spawn.
    if shutil.which("hostnamectl") is None:
        return {}

    try:
        result = subprocess.run(
            ("hostnamectl", "status"),
            capture_output=True,
            text=True,
            encoding="utf-8",
            # An unreadable pretty name must not raise where a missing one does
            # not.
            errors="replace",
            check=True,
            # The bus call hangs when systemd is up but unresponsive.
            timeout=2,
            # Force the C locale to keep the labels parsed above stable.
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.SubprocessError):
        return {}

    # str() coerces an unexpected stdout (like a globally mocked subprocess.run
    # returning a Mock) to text, so parsing degrades to an empty result instead
    # of raising.
    return _parse_hostnamectl_content(str(result.stdout).splitlines())


@cache
def _parse_os_release() -> dict[str, str]:
    """Read and parse the os-release file.

    Tries `/etc/os-release` first, then `/usr/lib/os-release` as fallback per the
    specification. Falls back to `_hostnamectl_os_release()` when neither
    file is readable, which is the only source left on a system hiding both.

    :return: Dictionary of parsed key-value pairs, or empty dict if no file found.
    """
    for path in ("/etc/os-release", "/usr/lib/os-release"):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                return _parse_os_release_content(f)
    return _hostnamectl_os_release()


@cache
def os_release_id() -> str:
    """Return the sanitized distribution ID from os-release.

    Lowercases the `ID` field and replaces spaces with underscores. No other
    transformation is applied: sub-variant IDs (like ``ol`` for Oracle Linux,
    or ``opensuse-slowroll`` for the openSUSE Slowroll channel) are preserved
    verbatim, so {func}`linux_info` and ``Platform.info()`` expose the exact
    distribution flavor. Mapping these IDs to their canonical platform is the
    job of the detection functions (see ``is_oracle()`` and ``is_opensuse()``
    in ``detection.py``).

    :return: Sanitized distribution ID, or empty string if absent.
    """
    raw_id = _parse_os_release().get("id", "")
    return raw_id.lower().replace(" ", "_")


def _version_parts(release: str) -> dict[str, str | None]:
    """Split a dotted release string into `major`, `minor` and `build_number`.

    Missing components are set to `None`: a bare ``"14"`` release has no minor
    version nor build number, and an empty release string has no parts at all.
    """
    parts = dict(
        zip(
            ("major", "minor", "build_number"), release.split(".", 2) if release else ()
        )
    )
    return {
        "major": parts.get("major"),
        "minor": parts.get("minor"),
        "build_number": parts.get("build_number"),
    }


@cache
def linux_info() -> dict[str, Any]:
    """Fetch detailed Linux distribution information from os-release.

    Returns a dictionary with the same structure as `distro.info()` for
    consistency, including:

    - `id`: Distribution ID (e.g., "ubuntu", "fedora")
    - `version`: Full version string (e.g., "22.04")
    - `version_parts`: Dictionary with `major`, `minor`, `build_number`
    - `like`: Space-separated list of related distributions
    - `codename`: Distribution codename (e.g., "jammy")

    Missing fields are set to `None`, like in {func}`macos_info` and
    {func}`windows_info`.

    :return: Dictionary containing Linux distribution details.
    """
    data = _parse_os_release()
    version = data.get("version_id", "")
    return {
        "id": os_release_id() or None,
        "version": version or None,
        "version_parts": _version_parts(version),
        "like": data.get("id_like") or None,
        "codename": data.get("version_codename") or None,
    }


def invalidate_os_release_cache() -> None:
    """Clear caches for all os-release functions."""
    _hostnamectl_os_release.cache_clear()
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
    ("27", None): "Golden Gate",
}
"""Maps macOS `(major, minor)` version parts to release code name.

```{seealso}
- https://en.wikipedia.org/wiki/Template:MacOS_versions
- https://docs.python.org/3/library/platform.html#platform.mac_ver
```

```{todo}
Handle the oddity where some beta releases of macOS Tahoe report their major
version as `16` instead of `15` or `26`. Left unhandled for now, as we consider
this a glitch in macOS history, and do not have a proper way to detect beta
versions at this time.
```
"""


def get_macos_codename(major: str | None = None, minor: str | None = None) -> str:
    """Get the macOS codename for a given version.

    :param major: The major version number (like ``"10"``, ``"11"``, ``"14"``).
    :param minor: The minor version number (like ``"0"``, ``"15"``). For
        macOS 11+, this can be ``None`` as codenames are tied to major
        versions only.
    :returns: The codename for the macOS version (like ``"Sonoma"``,
        ``"Ventura"``).
    :raises ValueError: If no codename matches the given version, or if
        multiple codenames match (which shouldn't happen with valid data).
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

    Returns a dictionary with the same structure as `distro.info()` for
    consistency, including:

    - `version`: Full version string (e.g., "14.2.1")
    - `version_parts`: Dictionary with `major`, `minor`, `build_number`
    - `codename`: The macOS codename (e.g., "Sonoma")

    :returns: A dictionary containing macOS version details.
    :raises ValueError: If the current macOS version cannot be mapped to a
        codename.
    """
    release, _versioninfo, _machine = platform.mac_ver()
    version_parts = _version_parts(release)
    return {
        "version": release,
        "version_parts": version_parts,
        "codename": get_macos_codename(version_parts["major"], version_parts["minor"]),
    }


def windows_info() -> dict[str, Any]:
    """Fetch detailed Windows version information.

    Returns a dictionary with the same structure as `distro.info()` for
    consistency, including:

    - `version`: Full version string (e.g., "10.0.19041")
    - `version_parts`: Dictionary with `major`, `minor`, `build_number`
    - `codename`: A combination of version and edition (e.g., "10 Enterprise")

    :returns: A dictionary containing Windows version details.

    ```{todo}
    Get even more details for Windows version. See inspirations from:
    https://github.com/saltstack/salt/blob/246d066/salt/grains/core.py#L1432-L1488
    ```
    """
    release, _version, _csd, _ptype = platform.win32_ver()
    return {
        "version": release,
        "version_parts": _version_parts(release),
        "codename": f"{release} {platform.win32_edition()}",
    }
