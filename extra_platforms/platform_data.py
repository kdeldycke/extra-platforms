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
TUMBLEWEED = Platform("tumbleweed", "openSUSE Tumbleweed", "↻")
TUXEDO = Platform("tuxedo", "Tuxedo OS", "🤵")
UBUNTU = Platform("ubuntu", "Ubuntu", "🎯")
UNKNOWN_LINUX = Platform("unknown_linux", "Unknown Linux", "🐧")
WINDOWS = Platform("windows", "Windows", "🪟")
WSL1 = Platform("wsl1", "Windows Subsystem for Linux v1", "⊞")
WSL2 = Platform("wsl2", "Windows Subsystem for Linux v2", "⊞")
XENSERVER = Platform("xenserver", "XenServer")
"""All individual platforms."""
