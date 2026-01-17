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

from .architecture_data import (
    AARCH64,
    ARM,
    ARMV5TEL,
    ARMV6L,
    ARMV7L,
    ARMV8L,
    I386,
    I586,
    I686,
    LOONGARCH64,
    MIPS,
    MIPS64,
    MIPS64EL,
    MIPSEL,
    PPC,
    PPC64,
    PPC64LE,
    RISCV32,
    RISCV64,
    S390X,
    SPARC,
    SPARC64,
    UNKNOWN_ARCHITECTURE,
    WASM32,
    WASM64,
    X86_64,
)
from .ci_data import (
    AZURE_PIPELINES,
    BAMBOO,
    BUILDKITE,
    CIRCLE_CI,
    CIRRUS_CI,
    CODEBUILD,
    GITHUB_CI,
    GITLAB_CI,
    HEROKU_CI,
    TEAMCITY,
    TRAVIS_CI,
    UNKNOWN_CI,
)
from .group import Group
from .platform_data import (
    AIX,
    ALTLINUX,
    AMZN,
    ANDROID,
    ARCH,
    BUILDROOT,
    CACHYOS,
    CENTOS,
    CLOUDLINUX,
    CYGWIN,
    DEBIAN,
    DRAGONFLY_BSD,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GUIX,
    HAIKU,
    HURD,
    IBM_POWERKVM,
    ILLUMOS,
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
    TUMBLEWEED,
    TUXEDO,
    UBUNTU,
    ULTRAMARINE,
    UNKNOWN_PLATFORM,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
)

# =============================================================================
# Architecture groups
# =============================================================================

ALL_ARCHITECTURES: Group = Group(
    "all_architectures",
    "All architectures",
    "🏛️",
    (
        AARCH64,
        ARM,
        ARMV5TEL,
        ARMV6L,
        ARMV7L,
        ARMV8L,
        I386,
        I586,
        I686,
        LOONGARCH64,
        MIPS,
        MIPS64,
        MIPS64EL,
        MIPSEL,
        PPC,
        PPC64,
        PPC64LE,
        RISCV32,
        RISCV64,
        S390X,
        SPARC,
        SPARC64,
        WASM32,
        WASM64,
        X86_64,
    ),
)
"""All recognized architectures.

.. caution::
    This group does not contain the :data:`UNKNOWN_ARCHITECTURE` trait.
"""


ALL_ARM = Group(
    "all_arm",
    "ARM architectures",
    "📱",
    (AARCH64, ARM, ARMV5TEL, ARMV6L, ARMV7L, ARMV8L),
)
"""All ARM-based architectures."""


X86 = Group(
    "x86",
    "x86 family",
    "𝘅",
    (I386, I586, I686, X86_64),
)
"""All x86-based architectures (Intel-compatible)."""


LOONGARCH = Group(
    "loongarch",
    "LoongArch",
    "🐉",
    (LOONGARCH64,),
)
"""LoongArch architecture."""


ALL_MIPS = Group(
    "all_mips",
    "MIPS architectures",
    "🔲",
    (MIPS, MIPS64, MIPS64EL, MIPSEL),
)
"""All MIPS-based architectures."""


POWERPC = Group(
    "powerpc",
    "PowerPC family",
    "⚡",
    (PPC, PPC64, PPC64LE),
)
"""All PowerPC-based architectures."""


RISCV = Group(
    "riscv",
    "RISC-V family",
    "Ⅴ",
    (RISCV32, RISCV64),
)
"""All RISC-V-based architectures."""


ALL_SPARC = Group(
    "all_sparc",
    "SPARC architectures",
    "☀️",
    (SPARC, SPARC64),
)
"""All SPARC-based architectures."""


IBM_MAINFRAME = Group(
    "ibm_mainframe",
    "IBM mainframe",
    "🏢",
    (S390X,),
)
"""IBM mainframe architectures."""


WEBASSEMBLY = Group(
    "webassembly",
    "WebAssembly",
    "🌐",
    (WASM32, WASM64),
)
"""WebAssembly architectures."""


ARCH_64_BIT = Group(
    "arch_64_bit",
    "64-bit architectures",
    "⁶⁴",
    (
        AARCH64,
        LOONGARCH64,
        MIPS64,
        MIPS64EL,
        PPC64,
        PPC64LE,
        RISCV64,
        S390X,
        SPARC64,
        WASM64,
        X86_64,
    ),
)
"""All 64-bit architectures."""


ARCH_32_BIT = Group(
    "arch_32_bit",
    "32-bit architectures",
    "³²",
    (
        ARM,
        ARMV5TEL,
        ARMV6L,
        ARMV7L,
        ARMV8L,
        I386,
        I586,
        I686,
        MIPS,
        MIPSEL,
        PPC,
        RISCV32,
        SPARC,
        WASM32,
    ),
)
"""All 32-bit architectures."""


# =============================================================================
# Platform groups
# =============================================================================

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
        BUILDROOT,
        CACHYOS,
        CENTOS,
        CLOUDLINUX,
        CYGWIN,
        DEBIAN,
        DRAGONFLY_BSD,
        EXHERBO,
        FEDORA,
        FREEBSD,
        GENTOO,
        GUIX,
        HAIKU,
        HURD,
        IBM_POWERKVM,
        ILLUMOS,
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
        TUMBLEWEED,
        TUXEDO,
        UBUNTU,
        ULTRAMARINE,
        WINDOWS,
        WSL1,
        WSL2,
        XENSERVER,
    ),
)
"""All recognized platforms.

.. caution::
    This group does not contain the :data:`UNKNOWN_PLATFORM` trait.
"""


ALL_WINDOWS = Group(
    "all_windows",
    "All Windows",
    "🪟",
    (WINDOWS,),
)
"""All Windows operating systems."""


UNIX = Group(
    "unix",
    "All Unix",
    "⨷",
    tuple(ALL_PLATFORMS - ALL_WINDOWS),
)
"""All Unix-like operating systems and compatibility layers."""


UNIX_WITHOUT_MACOS = Group(
    "unix_without_macos",
    "All Unix excluding macOS",
    "⨂",
    tuple(UNIX - MACOS),
)
"""All Unix platforms, without macOS.

This is useful to avoid macOS-specific workarounds on Unix platforms.
"""


BSD = Group(
    "bsd",
    "All BSD",
    "🅱️+",
    (DRAGONFLY_BSD, FREEBSD, MACOS, MIDNIGHTBSD, NETBSD, OPENBSD, SUNOS),
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
    "All BSD excluding macOS",
    "🅱️",
    tuple(BSD - MACOS),
)
"""All BSD platforms, without macOS.

This is useful to avoid macOS-specific workarounds on BSD platforms.
"""


LINUX = Group(
    "linux",
    "Linux distributions",
    "🐧",
    (
        ALTLINUX,
        AMZN,
        ANDROID,
        ARCH,
        BUILDROOT,
        CACHYOS,
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
        ULTRAMARINE,
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
    "Linux compatibility layers",
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
    "All Linux & compatibility layers",
    "🐧+",
    tuple(LINUX | LINUX_LAYERS),
)
"""Sum of all Linux distributions and Linux compatibility layers."""


SYSTEM_V = Group(
    "system_v",
    "AT&T System Five",
    "𝐕",
    (AIX, ILLUMOS, SOLARIS),
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
    "Unix compatibility layers",
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


OTHER_POSIX = Group(
    "other_posix",
    "Other POSIX-compliant platforms",
    "🅟",
    tuple(UNIX - BSD - LINUX - LINUX_LAYERS - SYSTEM_V - UNIX_LAYERS),
)
"""All other UNIX-like or POSIX-compliant platforms.

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


# =============================================================================
# CI groups
# =============================================================================

ALL_CI = Group(
    "all_ci",
    "CI systems",
    "♺",
    (
        AZURE_PIPELINES,
        BAMBOO,
        BUILDKITE,
        CIRCLE_CI,
        CIRRUS_CI,
        CODEBUILD,
        GITHUB_CI,
        GITLAB_CI,
        HEROKU_CI,
        TEAMCITY,
        TRAVIS_CI,
    ),
)
"""All recognized Continuous Integration systems.

.. caution::
    This group does not contain the :data:`UNKNOWN_CI` trait.

.. seealso::
    `List of known CI systems
    <https://adamj.eu/tech/2020/03/09/detect-if-your-tests-are-running-on-ci/>`_.
"""


# =============================================================================
# Mixed groups
# =============================================================================

UNKNOWN = Group(
    "unknown",
    "Unknown",
    "❓",
    (UNKNOWN_ARCHITECTURE, UNKNOWN_CI, UNKNOWN_PLATFORM),
)
"""Unknown or unrecognized traits."""


ALL_TRAITS = Group(
    "all_traits",
    "All architectures, platforms and CI systems",
    "⁕",
    tuple(ALL_ARCHITECTURES | ALL_PLATFORMS | ALL_CI | UNKNOWN),
)
"""All predefined architectures, platforms and CI systems.

.. hint::
    This group includes all ``UNKNOWN_*`` traits.
"""


# =============================================================================
# Collections of groups
# =============================================================================

ALL_ARCHITECTURE_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_ARCHITECTURES,
        ALL_ARM,
        X86,
        LOONGARCH,
        ALL_MIPS,
        POWERPC,
        RISCV,
        ALL_SPARC,
        IBM_MAINFRAME,
        WEBASSEMBLY,
        ARCH_64_BIT,
        ARCH_32_BIT,
    ),
)
"""All groups whose members are architectures."""


ALL_PLATFORM_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_PLATFORMS,
        ALL_WINDOWS,
        UNIX,
        UNIX_WITHOUT_MACOS,
        BSD,
        BSD_WITHOUT_MACOS,
        LINUX,
        LINUX_LAYERS,
        LINUX_LIKE,
        SYSTEM_V,
        UNIX_LAYERS,
        OTHER_POSIX,
    ),
)
"""All groups whose members are platforms."""


ALL_CI_GROUPS: frozenset[Group] = frozenset((ALL_CI,))
"""All groups whose members are CI systems.

.. note::
    Not that useful currently, but provided for symmetry with architecture and platform
    groups.
"""


NON_OVERLAPPING_GROUPS: frozenset[Group] = frozenset(
    (
        # Architecture groups.
        ALL_ARM,
        X86,
        LOONGARCH,
        ALL_MIPS,
        POWERPC,
        RISCV,
        ALL_SPARC,
        IBM_MAINFRAME,
        WEBASSEMBLY,
        # Platform groups.
        ALL_WINDOWS,
        BSD,
        LINUX,
        LINUX_LAYERS,
        SYSTEM_V,
        UNIX_LAYERS,
        OTHER_POSIX,
        # CI groups.
        ALL_CI,
        # Mixed groups.
        UNKNOWN,
    ),
)
"""Non-overlapping groups.

.. hint::
    These groups together cover all predefined architectures, platforms, and CI systems,
    including traits from the :data:`~extra_platforms.UNKNOWN` group.

    All groups in this collection are marked as canonical.
"""


EXTRA_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_TRAITS,
        # Architecture groups.
        ALL_ARCHITECTURES,
        ARCH_64_BIT,
        ARCH_32_BIT,
        # Platform groups.
        ALL_PLATFORMS,
        UNIX,
        UNIX_WITHOUT_MACOS,
        BSD_WITHOUT_MACOS,
        LINUX_LIKE,
    ),
)
"""Overlapping groups, defined for convenience.

.. hint::
    None of these groups are marked as canonical.
"""


ALL_GROUPS: frozenset[Group] = frozenset(NON_OVERLAPPING_GROUPS | EXTRA_GROUPS)
"""All predefined groups.

.. hint::
    This collection contains both canonical and non-canonical groups, including the
    :data:`~extra_platforms.UNKNOWN` group.
"""
