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
"""Heuristics to detect each platform.

All these heuristics can be hard-cached as the underlying system is not changing
between code execution.

We mostly rely on `distro <https://github.com/python-distro/distro>`_ to detect the
Linux distribution, has it is the recommended replacement for Python's original
``platform.linux_distribution`` function (which was removed in Python 3.8).

We then fill in the gaps with ``sys.platform`` and environment variables to detect
systems not covered by ``distro``.

This collection of heuristics is designed as a set of separate function with minimal
logic and dependencies. That way we can double-check during execution that no
heuristics are conflicting or matching multiple systems at the same time.

.. note::

    Heuristics for unrecognized platforms can be transplanted from `Rust's sysinfo
    crate <https://github.com/stanislav-tkach/os_info/tree/master/os_info/src>`_.
"""

from __future__ import annotations

import platform
import sys
from os import environ

import distro

from . import cache


@cache
def is_aix() -> bool:
    """Return `True` only if current platform is AIX."""
    return sys.platform.startswith("aix") or distro.id() == "aix"


@cache
def is_altlinux() -> bool:
    """Return `True` only if current platform is ALT Linux."""
    return distro.id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return `True` only if current platform is Amazon Linux."""
    return distro.id() == "amzn"


@cache
def is_android() -> bool:
    """Return `True` only if current platform is Android.

    Source: https://github.com/kivy/kivy/blob/master/kivy/utils.py#L429
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return `True` only if current platform is Arch Linux."""
    return distro.id() == "arch"


@cache
def is_buildroot() -> bool:
    """Return `True` only if current platform is Buildroot."""
    return distro.id() == "buildroot"


@cache
def is_centos() -> bool:
    """Return `True` only if current platform is CentOS."""
    return distro.id() == "centos"


@cache
def is_cloudlinux() -> bool:
    """Return `True` only if current platform is CloudLinux OS."""
    return distro.id() == "cloudlinux"


@cache
def is_cygwin() -> bool:
    """Return `True` only if current platform is Cygwin."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return `True` only if current platform is Debian."""
    return distro.id() == "debian"


@cache
def is_exherbo() -> bool:
    """Return `True` only if current platform is Exherbo Linux."""
    return distro.id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return `True` only if current platform is Fedora."""
    return distro.id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return `True` only if current platform is FreeBSD."""
    return sys.platform.startswith("freebsd") or distro.id() == "freebsd"


@cache
def is_gentoo() -> bool:
    """Return `True` only if current platform is GenToo Linux."""
    return distro.id() == "gentoo"


@cache
def is_guix() -> bool:
    """Return `True` only if current platform is Guix System."""
    return distro.id() == "guix"


@cache
def is_hurd() -> bool:
    """Return `True` only if current platform is GNU/Hurd."""
    return sys.platform.startswith("GNU")


@cache
def is_ibm_powerkvm() -> bool:
    """Return `True` only if current platform is IBM PowerKVM."""
    return distro.id() == "ibm_powerkvm"


@cache
def is_kvmibm() -> bool:
    """Return `True` only if current platform is KVM for IBM z Systems."""
    return distro.id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return `True` only if current platform is Linux Mint."""
    return distro.id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return `True` only if current platform is macOS."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return `True` only if current platform is Mageia."""
    return distro.id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return `True` only if current platform is Mandriva Linux."""
    return distro.id() == "mandriva"


@cache
def is_midnightbsd() -> bool:
    """Return `True` only if current platform is MidnightBSD."""
    return sys.platform.startswith("midnightbsd") or distro.id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return `True` only if current platform is NetBSD."""
    return sys.platform.startswith("netbsd") or distro.id() == "netbsd"


@cache
def is_openbsd() -> bool:
    """Return `True` only if current platform is OpenBSD."""
    return sys.platform.startswith("openbsd") or distro.id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return `True` only if current platform is openSUSE."""
    return distro.id() == "opensuse"


@cache
def is_oracle() -> bool:
    """Return `True` only if current platform is Oracle Linux (and Oracle Enterprise Linux)."""
    return distro.id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return `True` only if current platform is Parallels."""
    return distro.id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return `True` only if current platform is Pidora."""
    return distro.id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return `True` only if current platform is Raspbian."""
    return distro.id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return `True` only if current platform is RedHat Enterprise Linux."""
    return distro.id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return `True` only if current platform is Rocky Linux."""
    return distro.id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return `True` only if current platform is Scientific Linux."""
    return distro.id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return `True` only if current platform is Slackware."""
    return distro.id() == "slackware"


@cache
def is_sles() -> bool:
    """Return `True` only if current platform is SUSE Linux Enterprise Server."""
    return distro.id() == "sles"


@cache
def is_solaris() -> bool:
    """Return `True` only if current platform is Solaris."""
    return platform.platform(aliased=True, terse=True).startswith("Solaris")


@cache
def is_sunos() -> bool:
    """Return `True` only if current platform is SunOS."""
    return platform.platform(aliased=True, terse=True).startswith("SunOS")


@cache
def is_ubuntu() -> bool:
    """Return `True` only if current platform is Ubuntu."""
    return distro.id() == "ubuntu"


@cache
def is_unknown_linux() -> bool:
    """Return `True` only if current platform is an unknown Linux.

    Excludes WSL1 and WSL2 from this check to
    `avoid false positives <https://github.com/kdeldycke/meta-package-manager/issues/944>`_.
    """
    return sys.platform.startswith("linux") and not (
        is_ubuntu() or is_wsl1() or is_wsl2()
    )


@cache
def is_windows() -> bool:
    """Return `True` only if current platform is Windows."""
    return sys.platform.startswith("win32")


@cache
def is_wsl1() -> bool:
    """Return `True` only if current platform is Windows Subsystem for Linux v1.

    .. caution::
        The only difference between WSL1 and WSL2 is `the case of the kernel release
        version <https://github.com/andweeb/presence.nvim/pull/64#issue-1174430662>`_:

        - WSL 1:

          .. code-block:: shell-session

                $ uname -r
                4.4.0-22572-Microsoft

        - WSL 2:

          .. code-block:: shell-session

                $ uname -r
                5.10.102.1-microsoft-standard-WSL2
    """
    return "Microsoft" in platform.release()


@cache
def is_wsl2() -> bool:
    """Return `True` only if current platform is Windows Subsystem for Linux v2."""
    return "microsoft" in platform.release()


@cache
def is_xenserver() -> bool:
    """Return `True` only if current platform is XenServer."""
    return distro.id() == "xenserver"
