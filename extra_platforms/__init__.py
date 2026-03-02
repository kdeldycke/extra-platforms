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
"""Expose package-wide elements."""

from __future__ import annotations

import platform as stdlib_platform
import sys
from functools import cache

from . import detection  # noqa: E402
from ._docstrings import _initialize_all_docstrings
from .agent_data import (  # noqa: E402
    CLAUDE_CODE,
    CLINE,
    CURSOR,
    UNKNOWN_AGENT,
)
from .architecture_data import (  # noqa: E402
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
from .ci_data import (  # noqa: E402
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
from .shell_data import (  # noqa: E402
    ASH,
    BASH,
    CMD,
    CSH,
    DASH,
    FISH,
    KSH,
    NUSHELL,
    POWERSHELL,
    TCSH,
    UNKNOWN_SHELL,
    XONSH,
    ZSH,
)
from .terminal_data import (  # noqa: E402
    ALACRITTY,
    APPLE_TERMINAL,
    CONTOUR,
    FOOT,
    GHOSTTY,
    GNOME_TERMINAL,
    GNU_SCREEN,
    HYPER,
    ITERM2,
    KITTY,
    KONSOLE,
    RIO,
    TABBY,
    TILIX,
    TMUX,
    UNKNOWN_TERMINAL,
    VSCODE_TERMINAL,
    WEZTERM,
    WINDOWS_TERMINAL,
    XTERM,
    ZELLIJ,
)
from .detection import (  # noqa: E402
    current_agent,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
    current_terminal,
    current_traits,
    is_aarch64,
    is_aix,
    is_alacritty,
    is_alpine,
    is_altlinux,
    is_amzn,
    is_android,
    is_apple_terminal,
    is_arch,
    is_ash,
    is_arm,
    is_armv5tel,
    is_armv6l,
    is_armv7l,
    is_armv8l,
    is_azure_pipelines,
    is_bamboo,
    is_bash,
    is_buildkite,
    is_buildroot,
    is_cachyos,
    is_claude_code,
    is_cline,
    is_centos,
    is_circle_ci,
    is_cirrus_ci,
    is_cloudlinux,
    is_cmd,
    is_codebuild,
    is_contour,
    is_csh,
    is_cursor,
    is_cygwin,
    is_dash,
    is_debian,
    is_dragonfly_bsd,
    is_exherbo,
    is_fedora,
    is_fish,
    is_foot,
    is_freebsd,
    is_generic_linux,
    is_gentoo,
    is_ghostty,
    is_github_ci,
    is_gitlab_ci,
    is_gnome_terminal,
    is_gnu_screen,
    is_guix,
    is_haiku,
    is_heroku_ci,
    is_hurd,
    is_hyper,
    is_i386,
    is_i586,
    is_i686,
    is_ibm_powerkvm,
    is_illumos,
    is_iterm2,
    is_kali,
    is_kitty,
    is_konsole,
    is_ksh,
    is_kvmibm,
    is_linuxmint,
    is_loongarch64,
    is_macos,
    is_mageia,
    is_mandriva,
    is_manjaro,
    is_midnightbsd,
    is_mips,
    is_mips64,
    is_mips64el,
    is_mipsel,
    is_netbsd,
    is_nobara,
    is_nushell,
    is_openbsd,
    is_opensuse,
    is_openwrt,
    is_oracle,
    is_parallels,
    is_pidora,
    is_powershell,
    is_ppc,
    is_ppc64,
    is_ppc64le,
    is_raspbian,
    is_rhel,
    is_rio,
    is_riscv32,
    is_riscv64,
    is_rocky,
    is_s390x,
    is_scientific,
    is_slackware,
    is_sles,
    is_solaris,
    is_sparc,
    is_sparc64,
    is_sunos,
    is_tabby,
    is_tcsh,
    is_teamcity,
    is_tilix,
    is_tmux,
    is_travis_ci,
    is_tumbleweed,
    is_tuxedo,
    is_ubuntu,
    is_ultramarine,
    is_unknown_agent,
    is_unknown_architecture,
    is_unknown_ci,
    is_unknown_platform,
    is_unknown_shell,
    is_unknown_terminal,
    is_vscode_terminal,
    is_wasm32,
    is_wasm64,
    is_wezterm,
    is_windows,
    is_windows_terminal,
    is_wsl1,
    is_wsl2,
    is_x86_64,
    is_xenserver,
    is_xonsh,
    is_xterm,
    is_zellij,
    is_zsh,
)
from .group import (  # noqa: E402
    Group,
    extract_members,
    groups_from_ids,
    reduce,
    traits_from_ids,
)
from .group_data import (  # noqa: E402
    ALL_AGENT_GROUPS,
    ALL_AGENTS,
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_ARM,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUP_IDS,
    ALL_GROUPS,
    ALL_IDS,
    ALL_MIPS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_SHELL_GROUPS,
    ALL_SHELLS,
    ALL_SPARC,
    ALL_TERMINAL_GROUPS,
    ALL_TERMINALS,
    ALL_TRAIT_IDS,
    ALL_TRAITS,
    ALL_WINDOWS,
    ARCH_32_BIT,
    ARCH_64_BIT,
    BIG_ENDIAN,
    BOURNE_SHELLS,
    BSD,
    BSD_WITHOUT_MACOS,
    C_SHELLS,
    EXTRA_GROUPS,
    GPU_TERMINALS,
    IBM_MAINFRAME,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    LITTLE_ENDIAN,
    LOONGARCH,
    MULTIPLEXERS,
    NATIVE_TERMINALS,
    NON_OVERLAPPING_GROUPS,
    OTHER_POSIX,
    OTHER_SHELLS,
    POWERPC,
    RISCV,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN,
    WEBASSEMBLY,
    WEB_TERMINALS,
    WINDOWS_SHELLS,
    X86,
)
from .platform_data import (  # noqa: E402
    AIX,
    ALPINE,
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
    GENERIC_LINUX,
    GENTOO,
    GUIX,
    HAIKU,
    HURD,
    IBM_POWERKVM,
    ILLUMOS,
    KALI,
    KVMIBM,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MANJARO,
    MIDNIGHTBSD,
    NETBSD,
    NOBARA,
    OPENBSD,
    OPENSUSE,
    OPENWRT,
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
from .trait import (  # noqa: E402
    CI,
    Agent,
    Architecture,
    Platform,
    Shell,
    Terminal,
    Trait,
)

"""
.. important::
    Exposing everything at package level here motivates platforms and groups to have a
    unique and unambiguous ID. This constraint is enforced at the data-level and
    checked in unittests.

.. hint::
    The content of ``pytest.py`` file is not imported here to make dependency on
    Pytest optional.
"""


__version__ = "11.0.2.dev0"


def _initialize_group_detection_functions() -> list[str]:
    """Initialize and register all group detection functions.

    Generates the appropriate test function for each group and registers it globally.
    Since traits and groups have unique, non-overlapping IDs, we can create a
    ``is_<group>()`` function for each group.

    Returns a list of all registered function IDs for cache invalidation purposes.
    """
    func_ids = []

    for group in ALL_GROUPS:
        func_id = group.detection_func_id

        # Create the group membership test function.
        # Use default argument to capture the current group value (not the
        # variable reference).
        def group_membership_check(_group: Group = group) -> bool:
            """Compares all the current traits to the ``group``."""
            return any(t in _group for t in current_traits())

        group_membership_check.__doc__ = (
            "Return ``True`` if at least one :func:`~current_traits` is "
            f"found in the :data:`~{group.symbol_id}` group."
        )

        assert func_id not in locals(), (
            f"Function ID {func_id} already defined locally."
        )
        func_ids.append(func_id)
        globals()[func_id] = cache(group_membership_check)

    return func_ids


_group_detection_func_ids = _initialize_group_detection_functions()
"""Generates ``is_<group>()`` function for each group.

These are the equivalent for groups of ``is_<trait>()`` functions defined in
``detection.py``.

These functions return a boolean value indicating the membership of the current
system into that group.
"""


def invalidate_caches():
    """Invalidate all cached properties.

    Inspired by the new `platform.invalidate_caches() from Python 3.14
    <https://docs.python.org/3.14/library/platform.html#platform.invalidate_caches>`_,
    which is also called here when available.
    """
    # Invalidate platform module caches if available.
    if sys.version_info >= (3, 14):
        stdlib_platform.invalidate_caches()

    # Invalidate os-release caches.
    from .platform_info import invalidate_os_release_cache

    invalidate_os_release_cache()

    # Invalidate cached properties of trait classes.
    for member in ALL_TRAITS:
        if "current" in vars(member):
            # Use object.__delattr__ to bypass frozen dataclass restriction.
            object.__delattr__(member, "current")

    # Invalidate cached trait detection functions.
    for func_id in dir(detection):
        func = getattr(detection, func_id)
        if callable(func) and hasattr(func, "cache_clear"):
            func.cache_clear()

    # Invalidate package-level cached functions.
    current_architecture.cache_clear()
    current_platform.cache_clear()
    current_shell.cache_clear()
    current_terminal.cache_clear()
    current_ci.cache_clear()
    current_agent.cache_clear()
    current_traits.cache_clear()

    # Invalidate dynamically generated group detection functions.
    for func_id in _group_detection_func_ids:
        globals()[func_id].cache_clear()


__all__ = (  # noqa: F405
    "AARCH64",
    "Agent",
    "AIX",
    "ALACRITTY",
    "ALL_AGENT_GROUPS",
    "ALL_AGENTS",
    "ALL_ARCHITECTURE_GROUPS",
    "ALL_ARCHITECTURES",
    "ALL_ARM",
    "ALL_CI",
    "ALL_CI_GROUPS",
    "ALL_GROUP_IDS",
    "ALL_GROUPS",
    "ALL_IDS",
    "ALL_MIPS",
    "ALL_PLATFORM_GROUPS",
    "ALL_PLATFORMS",
    "ALL_SHELL_GROUPS",
    "ALL_SHELLS",
    "ALL_SPARC",
    "ALL_TERMINAL_GROUPS",
    "ALL_TERMINALS",
    "ALL_TRAIT_IDS",
    "ALL_TRAITS",
    "ALL_WINDOWS",
    "ALPINE",
    "ALTLINUX",
    "AMZN",
    "ANDROID",
    "APPLE_TERMINAL",
    "ARCH",
    "ARCH_32_BIT",
    "ARCH_64_BIT",
    "Architecture",
    "ARM",
    "ARMV5TEL",
    "ARMV6L",
    "ARMV7L",
    "ARMV8L",
    "ASH",
    "AZURE_PIPELINES",
    "BAMBOO",
    "BASH",
    "BIG_ENDIAN",
    "BOURNE_SHELLS",
    "BSD",
    "BSD_WITHOUT_MACOS",
    "BUILDKITE",
    "BUILDROOT",
    "C_SHELLS",
    "CACHYOS",
    "CENTOS",
    "CI",
    "CIRCLE_CI",
    "CIRRUS_CI",
    "CLAUDE_CODE",
    "CLINE",
    "CLOUDLINUX",
    "CMD",
    "CODEBUILD",
    "CONTOUR",
    "CSH",
    "current_agent",
    "current_architecture",
    "current_ci",
    "current_platform",
    "current_shell",
    "current_terminal",
    "current_traits",
    "CURSOR",
    "CYGWIN",
    "DASH",
    "DEBIAN",
    "DRAGONFLY_BSD",
    "EXHERBO",
    "EXTRA_GROUPS",
    "extract_members",
    "FEDORA",
    "FISH",
    "FOOT",
    "FREEBSD",
    "GENERIC_LINUX",
    "GENTOO",
    "GHOSTTY",
    "GITHUB_CI",
    "GITLAB_CI",
    "GNOME_TERMINAL",
    "GNU_SCREEN",
    "GPU_TERMINALS",
    "Group",
    "groups_from_ids",
    "GUIX",
    "HAIKU",
    "HEROKU_CI",
    "HURD",
    "HYPER",
    "I386",
    "I586",
    "I686",
    "IBM_MAINFRAME",
    "IBM_POWERKVM",
    "ILLUMOS",
    "invalidate_caches",
    "is_aarch64",
    "is_aix",
    "is_alacritty",
    "is_alpine",
    "is_altlinux",
    "is_amzn",
    "is_android",
    "is_any_agent",  # noqa: F822
    "is_any_architecture",  # noqa: F822
    "is_any_arm",  # noqa: F822
    "is_any_ci",  # noqa: F822
    "is_any_mips",  # noqa: F822
    "is_any_platform",  # noqa: F822
    "is_any_shell",  # noqa: F822
    "is_any_sparc",  # noqa: F822
    "is_any_terminal",  # noqa: F822
    "is_any_trait",  # noqa: F822
    "is_any_windows",  # noqa: F822
    "is_apple_terminal",
    "is_arch",
    "is_arch_32_bit",  # noqa: F822
    "is_arch_64_bit",  # noqa: F822
    "is_arm",
    "is_armv5tel",
    "is_armv6l",
    "is_armv7l",
    "is_armv8l",
    "is_ash",
    "is_azure_pipelines",
    "is_bamboo",
    "is_bash",
    "is_big_endian",  # noqa: F822
    "is_bourne_shells",  # noqa: F822
    "is_bsd",  # noqa: F822
    "is_bsd_not_macos",  # noqa: F822
    "is_buildkite",
    "is_buildroot",
    "is_c_shells",  # noqa: F822
    "is_cachyos",
    "is_centos",
    "is_circle_ci",
    "is_cirrus_ci",
    "is_claude_code",
    "is_cline",
    "is_cloudlinux",
    "is_cmd",
    "is_codebuild",
    "is_contour",
    "is_csh",
    "is_cursor",
    "is_cygwin",
    "is_dash",
    "is_debian",
    "is_dragonfly_bsd",
    "is_exherbo",
    "is_fedora",
    "is_fish",
    "is_foot",
    "is_freebsd",
    "is_generic_linux",
    "is_gentoo",
    "is_ghostty",
    "is_github_ci",
    "is_gitlab_ci",
    "is_gnome_terminal",
    "is_gnu_screen",
    "is_gpu_terminals",  # noqa: F822
    "is_guix",
    "is_haiku",
    "is_heroku_ci",
    "is_hurd",
    "is_hyper",
    "is_i386",
    "is_i586",
    "is_i686",
    "is_ibm_mainframe",  # noqa: F822
    "is_ibm_powerkvm",
    "is_illumos",
    "is_iterm2",
    "is_kali",
    "is_kitty",
    "is_konsole",
    "is_ksh",
    "is_kvmibm",
    "is_linux",  # noqa: F822
    "is_linux_layers",  # noqa: F822
    "is_linux_like",  # noqa: F822
    "is_linuxmint",
    "is_little_endian",  # noqa: F822
    "is_loongarch",  # noqa: F822
    "is_loongarch64",
    "is_macos",
    "is_mageia",
    "is_mandriva",
    "is_manjaro",
    "is_midnightbsd",
    "is_mips",
    "is_mips64",
    "is_mips64el",
    "is_mipsel",
    "is_multiplexers",  # noqa: F822
    "is_native_terminals",  # noqa: F822
    "is_netbsd",
    "is_nobara",
    "is_nushell",
    "is_openbsd",
    "is_opensuse",
    "is_openwrt",
    "is_oracle",
    "is_other_posix",  # noqa: F822
    "is_other_shells",  # noqa: F822
    "is_parallels",
    "is_pidora",
    "is_powerpc",  # noqa: F822
    "is_powershell",
    "is_ppc",
    "is_ppc64",
    "is_ppc64le",
    "is_raspbian",
    "is_rhel",
    "is_rio",
    "is_riscv",  # noqa: F822
    "is_riscv32",
    "is_riscv64",
    "is_rocky",
    "is_s390x",
    "is_scientific",
    "is_slackware",
    "is_sles",
    "is_solaris",
    "is_sparc",
    "is_sparc64",
    "is_sunos",
    "is_system_v",  # noqa: F822
    "is_tabby",
    "is_tcsh",
    "is_teamcity",
    "is_tilix",
    "is_tmux",
    "is_travis_ci",
    "is_tumbleweed",  # noqa: F822
    "is_tuxedo",  # noqa: F822
    "is_ubuntu",
    "is_ultramarine",
    "is_unix",  # noqa: F822
    "is_unix_layers",  # noqa: F822
    "is_unix_not_macos",  # noqa: F822
    "is_unknown",  # noqa: F822
    "is_unknown_agent",
    "is_unknown_architecture",
    "is_unknown_ci",
    "is_unknown_platform",
    "is_unknown_shell",
    "is_unknown_terminal",
    "is_vscode_terminal",
    "is_wasm32",
    "is_wasm64",
    "is_web_terminals",  # noqa: F822
    "is_webassembly",  # noqa: F822
    "is_wezterm",
    "is_windows",
    "is_windows_shells",  # noqa: F822
    "is_windows_terminal",
    "is_wsl1",
    "is_wsl2",
    "is_x86",  # noqa: F822
    "is_x86_64",
    "is_xenserver",
    "is_xonsh",
    "is_xterm",
    "is_zellij",
    "is_zsh",
    "ITERM2",
    "KALI",
    "KITTY",
    "KONSOLE",
    "KSH",
    "KVMIBM",
    "LINUX",
    "LINUX_LAYERS",
    "LINUX_LIKE",
    "LINUXMINT",
    "LITTLE_ENDIAN",
    "LOONGARCH",
    "LOONGARCH64",
    "MACOS",
    "MAGEIA",
    "MANDRIVA",
    "MANJARO",
    "MIDNIGHTBSD",
    "MIPS",
    "MIPS64",
    "MIPS64EL",
    "MIPSEL",
    "MULTIPLEXERS",
    "NATIVE_TERMINALS",
    "NETBSD",
    "NOBARA",
    "NON_OVERLAPPING_GROUPS",
    "NUSHELL",
    "OPENBSD",
    "OPENSUSE",
    "OPENWRT",
    "ORACLE",
    "OTHER_POSIX",
    "OTHER_SHELLS",
    "PARALLELS",
    "PIDORA",
    "Platform",
    "POWERPC",
    "POWERSHELL",
    "PPC",
    "PPC64",
    "PPC64LE",
    "RASPBIAN",
    "reduce",
    "RHEL",
    "RIO",
    "RISCV",
    "RISCV32",
    "RISCV64",
    "ROCKY",
    "S390X",
    "SCIENTIFIC",
    "Shell",
    "SLACKWARE",
    "SLES",
    "SOLARIS",
    "SPARC",
    "SPARC64",
    "SUNOS",
    "SYSTEM_V",
    "TABBY",
    "TCSH",
    "TEAMCITY",
    "Terminal",
    "TILIX",
    "TMUX",
    "Trait",
    "traits_from_ids",
    "TRAVIS_CI",
    "TUMBLEWEED",
    "TUXEDO",
    "UBUNTU",
    "ULTRAMARINE",
    "UNIX",
    "UNIX_LAYERS",
    "UNIX_WITHOUT_MACOS",
    "UNKNOWN",
    "UNKNOWN_AGENT",
    "UNKNOWN_ARCHITECTURE",
    "UNKNOWN_CI",
    "UNKNOWN_PLATFORM",
    "UNKNOWN_SHELL",
    "UNKNOWN_TERMINAL",
    "VSCODE_TERMINAL",
    "WASM32",
    "WASM64",
    "WEB_TERMINALS",
    "WEBASSEMBLY",
    "WEZTERM",
    "WINDOWS",
    "WINDOWS_SHELLS",
    "WINDOWS_TERMINAL",
    "WSL1",
    "WSL2",
    "X86",
    "X86_64",
    "XENSERVER",
    "XONSH",
    "XTERM",
    "ZELLIJ",
    "ZSH",
)
"""Expose all package-wide elements.

.. note::
    The content of ``__all__`` is checked and enforced in unittests.

.. todo::
    Test Ruff's ``__all__`` formatting capabilities. And if good enough, remove
    ``__all__`` checks in unittests.
"""

# Initialize docstrings for all trait and group instances after all imports
# are complete. This avoids circular import issues during module initialization.

_initialize_all_docstrings(ALL_TRAITS, ALL_GROUPS)
