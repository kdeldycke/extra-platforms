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

.. note::

    Default icons are inspired from Starship project:
    - https://starship.rs/config/#os
    - https://github.com/davidkna/starship/blob/e9faf17/.github/config-schema.json#L1221-L1269
"""

from __future__ import annotations

from .platform import Platform

AIX = Platform("aix", "IBM AIX", "➿", "https://ibm.com/products/aix/")
ALTLINUX = Platform("altlinux", "ALT Linux", "🐧", "https://altlinux.org")
AMZN = Platform(
    "amzn", "Amazon Linux", "🙂", "https://aws.amazon.com/amazon-linux-ami/"
)
ANDROID = Platform("android", "Android", "🤖", "https://android.com")
ARCH = Platform("arch", "Arch Linux", "🎗️", "https://archlinux.org")
BUILDROOT = Platform("buildroot", "Buildroot", "⛑️", "https://buildroot.org")
CENTOS = Platform("centos", "CentOS", "💠", "https://centos.org")
CLOUDLINUX = Platform("cloudlinux", "CloudLinux OS", "꩜", "https://cloudlinux.com")
CYGWIN = Platform("cygwin", "Cygwin", "Ͼ", "https://cygwin.com")
DEBIAN = Platform("debian", "Debian", "🌀", "https://debian.org")
EXHERBO = Platform("exherbo", "Exherbo Linux", "🐽", "https://exherbolinux.org")
FEDORA = Platform("fedora", "Fedora", "🎩", "https://fedoraproject.org")
FREEBSD = Platform("freebsd", "FreeBSD", "😈", "https://freebsd.org")
GENTOO = Platform("gentoo", "Gentoo Linux", "🗜️", "https://gentoo.org")
GUIX = Platform("guix", "Guix System", "🐃", "https://guix.gnu.org")
HURD = Platform("hurd", "GNU/Hurd", "🐃", "https://gnu.org/software/hurd/")
IBM_POWERKVM = Platform(
    "ibm_powerkvm",
    "IBM PowerKVM",
    "🤹",
    "https://ibm.com/mysupport/s/topic/0TO50000000QkyPGAS/",
)
KVMIBM = Platform(
    "kvmibm", "KVM for IBM z Systems", "🤹", "https://ibm.com/products/kvm/"
)
LINUXMINT = Platform("linuxmint", "Linux Mint", "🌿", "https://linuxmint.com")
MACOS = Platform("macos", "macOS", "🍎", "https://apple.com/macos/")
MAGEIA = Platform("mageia", "Mageia", "⍥", "https://mageia.org")
MANDRIVA = Platform(
    "mandriva",
    "Mandriva Linux",
    "💫",
    "https://web.archive.org/web/20150522203942/https://mandriva.com/en/mbs/",
)
MIDNIGHTBSD = Platform("midnightbsd", "MidnightBSD", "🌘", "https://midnightbsd.org")
NETBSD = Platform("netbsd", "NetBSD", "🚩", "https://netbsd.org")
OPENBSD = Platform("openbsd", "OpenBSD", "🐡", "https://openbsd.org")
OPENSUSE = Platform("opensuse", "openSUSE", "🦎", "https://opensuse.org")
ORACLE = Platform("oracle", "Oracle Linux", "🦴", "https://oracle.com/linux/")
PARALLELS = Platform("parallels", "Parallels", "∥", "https://parallels.com")
PIDORA = Platform(
    "pidora",
    "Pidora",
    "🍓",
    "https://web.archive.org/web/20200227132047/http://pidora.ca:80/",
)
RASPBIAN = Platform("raspbian", "Raspbian", "🍓", "https://raspberrypi.com/software/")
RHEL = Platform("rhel", "RedHat Enterprise Linux", "🎩", "https://redhat.com/rhel/")
ROCKY = Platform("rocky", "Rocky Linux", "⛰️", "https://rockylinux.org")
SCIENTIFIC = Platform(
    "scientific", "Scientific Linux", "⚛️", "https://scientificlinux.org"
)
SLACKWARE = Platform("slackware", "Slackware", "🚬", "https://www.slackware.com")
SLES = Platform(
    "sles", "SUSE Linux Enterprise Server", "🦎", "https://suse.com/products/server/"
)
SOLARIS = Platform("solaris", "Solaris", "🌞", "https://oracle.com/solaris")
SUNOS = Platform("sunos", "SunOS", "☀️", "https://wikipedia.org/wiki/SunOS")
TUMBLEWEED = Platform(
    "tumbleweed", "openSUSE Tumbleweed", "↻", "https://get.opensuse.org/tumbleweed/"
)
TUXEDO = Platform("tuxedo", "Tuxedo OS", "🤵", "https://tuxedocomputers.com/os")
UBUNTU = Platform("ubuntu", "Ubuntu", "🎯", "https://ubuntu.com")
UNKNOWN_LINUX = Platform("unknown_linux", "Unknown Linux", "🐧", "https://kernel.org")
WINDOWS = Platform("windows", "Windows", "🪟", "https://windows.com")
WSL1 = Platform(
    "wsl1",
    "Windows Subsystem for Linux v1",
    "⊞",
    "https://learn.microsoft.com/windows/wsl",
)
WSL2 = Platform(
    "wsl2",
    "Windows Subsystem for Linux v2",
    "⊞",
    "https://learn.microsoft.com/windows/wsl",
)
XENSERVER = Platform("xenserver", "XenServer", "Ⓧ", "https://xenproject.org")
"""All individual platforms."""
