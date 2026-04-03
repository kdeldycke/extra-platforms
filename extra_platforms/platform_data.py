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
"""Platform definitions and metadata.

.. note::
    Default icons are inspired from Starship project:
    - https://starship.rs/config/#os
    - https://github.com/starship/starship/blob/master/.github/config-schema.json

    Some icons, especially Linux distributions, have their own dedicated `codepoints in
    NerdFonts <https://www.nerdfonts.com/cheat-sheet>`_.
"""

from __future__ import annotations

from .trait import Platform

AIX = Platform("aix", "IBM AIX", "➿", "https://ibm.com/products/aix/")

ALPINE = Platform("alpine", "Alpine Linux", "🏔️", "https://alpinelinux.org")

ALTLINUX = Platform("altlinux", "ALT Linux", "Δ", "https://altlinux.org")

AMZN = Platform("amzn", "Amazon Linux", "⤻", "https://aws.amazon.com/amazon-linux-ami/")

ANDROID = Platform("android", "Android", "🤖", "https://android.com")

ARCH = Platform("arch", "Arch Linux", "🎗️", "https://archlinux.org")

BUILDROOT = Platform("buildroot", "Buildroot", "⛑️", "https://buildroot.org")

CACHYOS = Platform("cachyos", "CachyOS", "⌬", "https://cachyos.org")

CENTOS = Platform("centos", "CentOS", "💠", "https://centos.org")

CLOUDLINUX = Platform("cloudlinux", "CloudLinux OS", "꩜", "https://cloudlinux.com")

CYGWIN = Platform("cygwin", "Cygwin", "Ͼ", "https://cygwin.com")

DEBIAN = Platform("debian", "Debian", "🌀", "https://debian.org")

DRAGONFLY_BSD = Platform(
    "dragonfly_bsd", "DragonFly BSD", "🪰", "https://www.dragonflybsd.org"
)

EXHERBO = Platform("exherbo", "Exherbo Linux", "🐽", "https://exherbolinux.org")

FEDORA = Platform("fedora", "Fedora", "🎩", "https://fedoraproject.org")

FREEBSD = Platform("freebsd", "FreeBSD", "😈", "https://freebsd.org")

GENERIC_LINUX = Platform("generic_linux", "Generic Linux", "🥚", "https://kernel.org")

GENTOO = Platform("gentoo", "Gentoo Linux", "🗜️", "https://gentoo.org")

GUIX = Platform("guix", "Guix System", "🐃", "https://guix.gnu.org")

HAIKU = Platform("haiku", "Haiku", "🍂", "https://www.haiku-os.org")

HURD = Platform("hurd", "GNU/Hurd", "🦬", "https://www.gnu.org/software/hurd/")

IBM_POWERKVM = Platform(
    "ibm_powerkvm",
    "IBM PowerKVM",
    "🤹",
    "https://ibm.com/mysupport/s/topic/0TO50000000QkyPGAS/",
)

ILLUMOS = Platform("illumos", "illumos", "🔥", "https://illumos.org")

KALI = Platform("kali", "Kali Linux", "🔱", "https://kali.org")

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

MANJARO = Platform("manjaro", "Manjaro Linux", "▲", "https://manjaro.org")

MIDNIGHTBSD = Platform("midnightbsd", "MidnightBSD", "🌘", "https://midnightbsd.org")

NETBSD = Platform("netbsd", "NetBSD", "🚩", "https://netbsd.org")

NOBARA = Platform("nobara", "Nobara", "", "https://nobaraproject.org")
"""
.. note::
    Instead of using a loose Unicode icon for the Nobara OS, or just not adding any, we
    are using a `NerdFont <https://www.nerdfonts.com>`_ icon instead: ` (i.e.
    nf-linux-nobara / f380)
    <https://www.nerdfonts.com/cheat-sheet?glyphSearch=nf-linux-nobara>`_.

    The side-effect of using a NerdFont character is it will only display correctly
    when using a supported font. Otherwise, it will appear as an unknown or invisible
    character depending on the fonts.

.. todo::
    In the future, we may want to have two icons for each platform, one that is
    Unicode-based, the other that is NerdFont-based.
"""

OPENBSD = Platform("openbsd", "OpenBSD", "🐡", "https://openbsd.org")

OPENSUSE = Platform("opensuse", "openSUSE", "🦎", "https://opensuse.org")

OPENWRT = Platform("openwrt", "OpenWrt", "📶", "https://openwrt.org")

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

SUNOS = Platform("sunos", "SunOS", "🌅", "https://wikipedia.org/wiki/SunOS")

TUMBLEWEED = Platform(
    "tumbleweed", "openSUSE Tumbleweed", "↻", "https://get.opensuse.org/tumbleweed/"
)

TUXEDO = Platform("tuxedo", "Tuxedo OS", "🤵", "https://tuxedocomputers.com/os")

UBUNTU = Platform("ubuntu", "Ubuntu", "🎯", "https://ubuntu.com")

ULTRAMARINE = Platform(
    "ultramarine", "Ultramarine", "🌊", "https://ultramarine-linux.org"
)

UNKNOWN_PLATFORM = Platform(
    "unknown_platform",
    "Unknown platform",
    "❓",
    "https://en.wikipedia.org/wiki/Computer_platform",
)

VOID = Platform("void", "Void Linux", "∅", "https://voidlinux.org/")

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
