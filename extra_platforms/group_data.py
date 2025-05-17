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
"""Definitions of ready-to-use groups."""

from __future__ import annotations

from .group import Group
from .platform_data import (
    AIX,
    ALTLINUX,
    AMZN,
    ANDROID,
    ARCH,
    AZURE_PIPELINES,
    BAMBOO,
    BUILDKITE,
    BUILDROOT,
    CENTOS,
    CIRCLE_CI,
    CIRRUS_CI,
    CLOUDLINUX,
    CODEBUILD,
    CYGWIN,
    DEBIAN,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GITHUB_CI,
    GITLAB_CI,
    GUIX,
    HEROKU_CI,
    HURD,
    IBM_POWERKVM,
    KVMIBM,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    NOBARA,
    OPENBSD,
    OPENSUSE,
    ORACLE,
    PARALLELS,
    PIDORA,
    RASPBIAN,
    RHEL,
    ROCKY,
    SCIENTIFIC,
    SLACKWARE,
    SLES,
    SOLARIS,
    SUNOS,
    TEAMCITY,
    TRAVIS_CI,
    TUMBLEWEED,
    TUXEDO,
    UBUNTU,
    UNKNOWN_CI,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
)

ALL_PLATFORMS: Group = Group(
    "all_platforms",
    "All platforms",
    "⚙️",
    (
        AIX,
        ALTLINUX,
        AMZN,
        ANDROID,
        ARCH,
        AZURE_PIPELINES,
        BAMBOO,
        BUILDKITE,
        BUILDROOT,
        CENTOS,
        CIRCLE_CI,
        CIRRUS_CI,
        CLOUDLINUX,
        CODEBUILD,
        CYGWIN,
        DEBIAN,
        EXHERBO,
        FEDORA,
        FREEBSD,
        GENTOO,
        GITHUB_CI,
        GITLAB_CI,
        GUIX,
        HEROKU_CI,
        HURD,
        IBM_POWERKVM,
        KVMIBM,
        LINUXMINT,
        MACOS,
        MAGEIA,
        MANDRIVA,
        MIDNIGHTBSD,
        NETBSD,
        NOBARA,
        OPENBSD,
        OPENSUSE,
        ORACLE,
        PARALLELS,
        PIDORA,
        RASPBIAN,
        RHEL,
        ROCKY,
        SCIENTIFIC,
        SLACKWARE,
        SLES,
        SOLARIS,
        SUNOS,
        TEAMCITY,
        TRAVIS_CI,
        TUMBLEWEED,
        TUXEDO,
        UBUNTU,
        UNKNOWN_CI,
        UNKNOWN_LINUX,
        WINDOWS,
        WSL1,
        WSL2,
        XENSERVER,
    ),
)
"""All recognized platforms."""


CI = Group(
    "ci",
    "CI systems",
    "♺",
    (
        AZURE_PIPELINES,
        BAMBOO,
        BUILDKITE,
        GITHUB_CI,
        GITLAB_CI,
        CIRCLE_CI,
        CIRRUS_CI,
        CODEBUILD,
        HEROKU_CI,
        TEAMCITY,
        TRAVIS_CI,
        UNKNOWN_CI,
    ),
)
"""All Continuous Integration systems.

.. note::
    `List of known CI systems
    <https://adamj.eu/tech/2020/03/09/detect-if-your-tests-are-running-on-ci/>`_.
"""


ALL_PLATFORMS_WITHOUT_CI = Group(
    "all_platforms_without_ci",
    "Any platforms excluding CI systems",
    "🖥️",
    tuple(ALL_PLATFORMS - CI),
)
"""All platforms, without CI systems."""


ANY_WINDOWS = Group(
    "any_windows",
    "Any Windows",
    "🪟",
    (WINDOWS,),
)
"""All Windows operating systems."""


UNIX = Group(
    "unix",
    "Any Unix",
    "⨷",
    tuple(ALL_PLATFORMS - ANY_WINDOWS - CI),
)
"""All Unix-like operating systems and compatibility layers."""


UNIX_WITHOUT_MACOS = Group(
    "unix_without_macos",
    "Any Unix excluding macOS",
    "⨂",
    tuple(UNIX - MACOS),
)
"""All Unix platforms, without macOS.

This is useful to avoid macOS-specific workarounds on Unix platforms.
"""


BSD = Group(
    "bsd",
    "Any BSD",
    "🅱️+",
    (FREEBSD, MACOS, MIDNIGHTBSD, NETBSD, OPENBSD, SUNOS),
)
"""All BSD platforms.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `386BSD` (`FreeBSD`, `NetBSD`, `OpenBSD`, `DragonFly BSD`)
    - `NeXTSTEP`
    - `Darwin` (`macOS`, `iOS`, `audioOS`, `iPadOS`, `tvOS`, `watchOS`, `bridgeOS`)
    - `SunOS`
    - `Ultrix`
"""


BSD_WITHOUT_MACOS = Group(
    "bsd_without_macos",
    "Any BSD excluding macOS",
    "🅱️",
    tuple(BSD - MACOS),
)
"""All BSD platforms, without macOS.

This is useful to avoid macOS-specific workarounds on BSD platforms.
"""


LINUX = Group(
    "linux",
    "Any Linux distribution",
    "🐧",
    (
        ALTLINUX,
        AMZN,
        ANDROID,
        ARCH,
        BUILDROOT,
        CENTOS,
        CLOUDLINUX,
        DEBIAN,
        EXHERBO,
        FEDORA,
        GENTOO,
        GUIX,
        IBM_POWERKVM,
        KVMIBM,
        LINUXMINT,
        MAGEIA,
        MANDRIVA,
        NOBARA,
        OPENSUSE,
        ORACLE,
        PARALLELS,
        PIDORA,
        RASPBIAN,
        RHEL,
        ROCKY,
        SCIENTIFIC,
        SLACKWARE,
        SLES,
        TUMBLEWEED,
        TUXEDO,
        UBUNTU,
        UNKNOWN_LINUX,
        XENSERVER,
    ),
)
"""All distributions based on a Linux kernel.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Android`
    - `ChromeOS`
    - any other distribution
"""


LINUX_LAYERS = Group(
    "linux_layers",
    "Any Linux compatibility layers",
    "≚",
    (WSL1, WSL2),
)
"""Interfaces that allows Linux binaries to run on a different host system.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Windows Subsystem for Linux`
"""


LINUX_LIKE = Group(
    "linux_like",
    "Any Linux and compatibility layers",
    "🐧+",
    tuple(LINUX | LINUX_LAYERS),
)
"""Sum of all Linux distributions and Linux compatibility layers."""


SYSTEM_V = Group(
    "system_v",
    "Any Unix derived from AT&T System Five",
    "Ⅴ",
    (AIX, SOLARIS),
)
"""All Unix platforms derived from AT&T System Five.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `A/UX`
    - `AIX`
    - `HP-UX`
    - `IRIX`
    - `OpenServer`
    - `Solaris`
    - `OpenSolaris`
    - `Illumos`
    - `Tru64`
    - `UNIX`
    - `UnixWare`
"""


UNIX_LAYERS = Group(
    "unix_layers",
    "Any Unix compatibility layers",
    "≛",
    (CYGWIN,),
)
"""Interfaces that allows Unix binaries to run on a different host system.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Cygwin`
    - `Darling`
    - `Eunice`
    - `GNV`
    - `Interix`
    - `MachTen`
    - `Microsoft POSIX subsystem`
    - `MKS Toolkit`
    - `PASE`
    - `P.I.P.S.`
    - `PWS/VSE-AF`
    - `UNIX System Services`
    - `UserLAnd Technologies`
    - `Windows Services for UNIX`
"""


OTHER_UNIX = Group(
    "other_unix",
    "Any other Unix",
    "⊎",
    tuple(UNIX - BSD - LINUX - LINUX_LAYERS - SYSTEM_V - UNIX_LAYERS),
)
"""All other Unix platforms.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Coherent`
    - `GNU/Hurd`
    - `HarmonyOS`
    - `LiteOS`
    - `LynxOS`
    - `Minix`
    - `MOS`
    - `OSF/1`
    - `QNX`
    - `BlackBerry 10`
    - `Research Unix`
    - `SerenityOS`
"""


NON_OVERLAPPING_GROUPS: frozenset[Group] = frozenset(
    (
        ANY_WINDOWS,
        BSD,
        LINUX,
        LINUX_LAYERS,
        SYSTEM_V,
        UNIX_LAYERS,
        OTHER_UNIX,
        CI,
    ),
)
"""Non-overlapping groups."""


EXTRA_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_PLATFORMS,
        ALL_PLATFORMS_WITHOUT_CI,
        LINUX_LIKE,
        UNIX,
        UNIX_WITHOUT_MACOS,
        BSD_WITHOUT_MACOS,
    ),
)
"""Overlapping groups, defined for convenience."""


ALL_GROUPS: frozenset[Group] = frozenset(NON_OVERLAPPING_GROUPS | EXTRA_GROUPS)
"""All groups."""
