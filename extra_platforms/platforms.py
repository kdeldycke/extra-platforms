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
"""Platform definitions and metadata.

Everything here can be aggressively cached and frozen, as it's only compute
platform-dependent values.

.. note::

    Default icons are inspired from Starship project:
    - https://starship.rs/config/#os
    - https://github.com/davidkna/starship/blob/e9faf17/.github/config-schema.json#L1221-L1269
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import distro
from boltons.iterutils import remap

from . import detection


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

    current: bool = field(init=False)
    """`True` if current environment runs on this platform."""

    def __post_init__(self):
        """Set the ``current`` attribute to identifying the current platform."""
        object.__setattr__(self, "current", detection.__dict__[f"is_{self.id}"]())
        object.__setattr__(self, "__doc__", f"Identify {self.name}.")

    def info(self) -> dict[str, str | bool | None | dict[str, str | None]]:
        """Returns all platform attributes we can gather."""
        info = {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "current": self.current,
            # Extra fields from distro.info().
            "distro_id": None,
            "version": None,
            "version_parts": {"major": None, "minor": None, "build_number": None},
            "like": None,
            "codename": None,
        }
        # Get extra info from distro.
        if self.current:
            d_info = dict(distro.info())
            # Rename distro ID to avoid conflict with our own ID.
            d_info["distro_id"] = d_info.pop("id")
            info = _recursive_update(info, _remove_blanks(d_info))
        return info  # type: ignore[return-value]


AIX = Platform("aix", "IBM AIX", "➿")
ALTLINUX = Platform("altlinux", "ALT Linux")
AMZN = Platform("amzn", "Amazon Linux", "🙂")
ANDROID = Platform("android", "Android", "🤖")
ARCH = Platform("arch", "Arch Linux", "🎗️")
BUILDROOT = Platform("buildroot", "Buildroot")
CENTOS = Platform("centos", "CentOS", "💠")
CLOUDLINUX = Platform("cloudlinux", "CloudLinux OS")
CYGWIN = Platform("cygwin", "Cygwin", "Ͼ")
DEBIAN = Platform("debian", "Debian", "🌀")
EXHERBO = Platform("exherbo", "Exherbo Linux")
FEDORA = Platform("fedora", "Fedora", "🎩")
FREEBSD = Platform("freebsd", "FreeBSD", "😈")
GENTOO = Platform("gentoo", "Gentoo Linux", "🗜️")
GUIX = Platform("guix", "Guix System")
HURD = Platform("hurd", "GNU/Hurd", "🐃")
IBM_POWERKVM = Platform("ibm_powerkvm", "IBM PowerKVM")
KVMIBM = Platform("kvmibm", "KVM for IBM z Systems")
LINUXMINT = Platform("linuxmint", "Linux Mint", "🌿")
MACOS = Platform("macos", "macOS", "🍎")
MAGEIA = Platform("mageia", "Mageia")
MANDRIVA = Platform("mandriva", "Mandriva Linux")
MIDNIGHTBSD = Platform("midnightbsd", "MidnightBSD", "🌘")
NETBSD = Platform("netbsd", "NetBSD", "🚩")
OPENBSD = Platform("openbsd", "OpenBSD", "🐡")
OPENSUSE = Platform("opensuse", "openSUSE", "🦎")
ORACLE = Platform("oracle", "Oracle Linux", "🦴")
PARALLELS = Platform("parallels", "Parallels")
PIDORA = Platform("pidora", "Pidora")
RASPBIAN = Platform("raspbian", "Raspbian", "🍓")
RHEL = Platform("rhel", "RedHat Enterprise Linux", "🎩")
ROCKY = Platform("rocky", "Rocky Linux", "💠")
SCIENTIFIC = Platform("scientific", "Scientific Linux")
SLACKWARE = Platform("slackware", "Slackware")
SLES = Platform("sles", "SUSE Linux Enterprise Server", "🦎")
SOLARIS = Platform("solaris", "Solaris", "🌞")
SUNOS = Platform("sunos", "SunOS", "☀️")
UBUNTU = Platform("ubuntu", "Ubuntu", "🎯")
UNKNOWN_LINUX = Platform("unknown_linux", "Unknown Linux", "🐧")
WINDOWS = Platform("windows", "Windows", "🪟")
WSL1 = Platform("wsl1", "Windows Subsystem for Linux v1", "⊞")
WSL2 = Platform("wsl2", "Windows Subsystem for Linux v2", "⊞")
XENSERVER = Platform("xenserver", "XenServer")
