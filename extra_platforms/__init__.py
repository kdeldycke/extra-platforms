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
"""Expose package-wide elements."""

from __future__ import annotations

import logging
import platform as stdlib_platform
import sys
from functools import cache

from . import detection  # noqa: E402
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
from .detection import (  # noqa: E402
    is_aarch64,
    is_aix,
    is_altlinux,
    is_amzn,
    is_android,
    is_arch,
    is_arm,
    is_armv5tel,
    is_armv6l,
    is_armv7l,
    is_armv8l,
    is_azure_pipelines,
    is_bamboo,
    is_buildkite,
    is_buildroot,
    is_cachyos,
    is_centos,
    is_circle_ci,
    is_cirrus_ci,
    is_cloudlinux,
    is_codebuild,
    is_cygwin,
    is_debian,
    is_exherbo,
    is_fedora,
    is_freebsd,
    is_gentoo,
    is_github_ci,
    is_gitlab_ci,
    is_guix,
    is_heroku_ci,
    is_hurd,
    is_i386,
    is_i586,
    is_i686,
    is_ibm_powerkvm,
    is_kvmibm,
    is_linuxmint,
    is_loongarch64,
    is_macos,
    is_mageia,
    is_mandriva,
    is_midnightbsd,
    is_mips,
    is_mips64,
    is_mips64el,
    is_mipsel,
    is_netbsd,
    is_nobara,
    is_openbsd,
    is_opensuse,
    is_oracle,
    is_parallels,
    is_pidora,
    is_ppc,
    is_ppc64,
    is_ppc64le,
    is_raspbian,
    is_rhel,
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
    is_teamcity,
    is_travis_ci,
    is_tumbleweed,
    is_tuxedo,
    is_ubuntu,
    is_ultramarine,
    is_wasm32,
    is_wasm64,
    is_windows,
    is_wsl1,
    is_wsl2,
    is_x86_64,
    is_xenserver,
)
from .group import Group  # noqa: E402
from .group_data import (  # noqa: E402
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_ARM,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUPS,
    ALL_MIPS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_SPARC,
    ALL_TRAITS,
    ALL_WINDOWS,
    ARCH_32_BIT,
    ARCH_64_BIT,
    BSD,
    BSD_WITHOUT_MACOS,
    EXTRA_GROUPS,
    IBM_MAINFRAME,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    LOONGARCH,
    NON_OVERLAPPING_GROUPS,
    OTHER_UNIX,
    POWERPC,
    RISCV,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN,
    WEBASSEMBLY,
    X86,
)
from .platform_data import (  # noqa: E402
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
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GUIX,
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
    Architecture,
    Platform,
    Trait,
)

"""
.. important::
    Exposing everything at package level here motivates platforms and groups to have a
    unique and unambiguous ID. This constraint is enforced at the data-level and
    checked in unittests.

.. caution::
    The content of ``pytest.py`` file is not imported here at package level like this:

    .. code-block:: python
        from .pytest import *

    That is to make dependency on Pytest optional.
"""


from .operations import (  # noqa: E402
    ALL_GROUP_IDS,
    ALL_IDS,
    ALL_TRAIT_IDS,
    groups_from_ids,
    reduce,
    traits_from_ids,
)

__version__ = "7.0.0"


@cache
def _unrecognized_message() -> str:
    """Generate a consistent message for unrecognized environments."""
    return (
        f"Environment: {sys.platform!r} / "
        f"{stdlib_platform.platform(aliased=True, terse=True)!r} / "
        f"{stdlib_platform.machine()!r} / {stdlib_platform.architecture()!r}. "
        "Please report this at https://github.com/kdeldycke/extra-platforms/issues to "
        "improve detection heuristics."
    )


@cache
def current_architecture(strict: bool = False) -> Architecture:
    """Returns the ``Architecture`` matching the current environment.

    Returns ``UNKNOWN_ARCHITECTURE`` if not running inside a recognized architecture.
    To raise an error instead, set ``strict`` to ``True``.

    Always raises an error if multiple architectures match.
    """
    matching = set()
    # Iterate over all recognized architectures.
    for arch in ALL_ARCHITECTURES:
        if arch.current:
            # Assert to please type checkers.
            assert isinstance(arch, Architecture)
            matching.add(arch)

    # Return the only matching architecture.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple architectures matches: {matching!r}. {_unrecognized_message()}"
        )

    # No matching architecture found.
    msg = f"Unrecognized architecture: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
    return UNKNOWN_ARCHITECTURE


@cache
def current_platform(strict: bool = False) -> Platform:
    """Always returns the best matching ``Platform`` for the current environment.

    Returns ``UNKNOWN_PLATFORM`` if not running inside a recognized platform.
    To raise an error instead, set ``strict`` to ``True``.

    If multiple platforms match the current environment, this function will try to
    select the best, informative one. Raises an error if we can't decide on a single,
    appropriate platform.
    """
    matching = set()
    for platform in ALL_PLATFORMS:
        if platform.current:
            # Assert to please type checkers.
            assert isinstance(platform, Platform)
            matching.add(platform)

    # Return the only matching platform.
    if len(matching) == 1:
        return matching.pop()

    # Removes some generic platforms from the matching, until we have a single match.
    # Starts by removing the least specific WSL1, then WSL2: WSL is a generic platform,
    # so we should prefer the remaining, more specific platform matches like Ubuntu. See:
    # - https://github.com/kdeldycke/extra-platforms/issues/158
    # - https://github.com/kdeldycke/meta-package-manager/issues/944
    for wsl in (WSL1, WSL2):
        if wsl in matching:
            matching.remove(wsl)
            if len(matching) == 1:
                return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple platforms matches: {matching!r}. {_unrecognized_message()}"
        )

    # No matching platform found.
    msg = f"Unrecognized platform: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
    return UNKNOWN_PLATFORM


@cache
def current_ci(strict: bool = False) -> CI | None:
    """Returns the ``CI`` system matching the current environment.

    Returns ``UNKNOWN_CI`` if not running inside a recognized CI system.
    To raise an error instead, set ``strict`` to ``True``.

    Always raises an error if multiple CI systems match.
    """
    matching = set()
    # Iterate over all recognized CI systems.
    for ci in ALL_CI:
        if ci.current:
            # Assert to please type checkers.
            assert isinstance(ci, CI)
            matching.add(ci)

    # Return the only matching CI system.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple CI matches: {matching!r}. {_unrecognized_message()}"
        )

    # No matching CI system found.
    msg = f"Unrecognized CI: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
    return UNKNOWN_CI


@cache
def current_traits() -> set[Trait]:
    """Returns all traits matching the current environment.

    This includes platforms, architectures and CI systems.

    .. caution::
        Never returns ``UNKNOWN_*`` traits.

    Raises an error if the current environment is not recognized at all.

    .. attention::
        At this point it is too late to worry about caching. This function has no
        choice but to evaluate all detection heuristics.
    """
    matching = set()
    for trait in ALL_TRAITS - UNKNOWN:
        if trait.current:
            matching.add(trait)

    if not matching:
        raise SystemError(f"Unrecognized environment: {_unrecognized_message()}")

    return matching


@cache
def is_unknown_architecture() -> bool:
    """Return ``True`` if current architecture is `UNKNOWN_ARCHITECTURE <architectures.html#extra_platforms.UNKNOWN_ARCHITECTURE>`_."""
    return current_architecture() is UNKNOWN_ARCHITECTURE


@cache
def is_unknown_platform() -> bool:
    """Return ``True`` if current platform is `UNKNOWN_PLATFORM <platforms.html#extra_platforms.UNKNOWN_PLATFORM>`_."""
    return current_platform() is UNKNOWN_PLATFORM


@cache
def is_unknown_ci() -> bool:
    """Return ``True`` if current CI is `UNKNOWN_CI <ci.html#extra_platforms.UNKNOWN_CI>`_."""
    return current_ci() is UNKNOWN_CI


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
        def group_membership_check() -> bool:
            """Compares all the current traits to the ``group``."""
            return any(t in group for t in current_traits())

        group_membership_check.__doc__ = f"Return ``True`` if current traits match `{group.symbol_id} <groups.html#extra_platforms.{group.symbol_id}>`_ group."

        assert func_id not in locals(), (
            f"Function ID {func_id} already defined locally."
        )
        func_ids.append(func_id)
        globals()[func_id] = cache(group_membership_check)

    return func_ids


_group_detection_func_ids = _initialize_group_detection_functions()
"""Generates ``is_<group>()`` function for each group.

These are the equivalent for groups of ``is_<trait>()`` functions defined in ``detection.py``.

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
    current_ci.cache_clear()
    current_traits.cache_clear()

    # Invalidate dynamically generated group detection functions.
    for func_id in _group_detection_func_ids:
        globals()[func_id].cache_clear()


from ._deprecated import (  # noqa: E402
    ALL_PLATFORM_IDS,
    ALL_PLATFORMS_WITHOUT_CI,
    ANY_ARM,
    ANY_MIPS,
    ANY_SPARC,
    ANY_WINDOWS,
    UNKNOWN_LINUX,
    current_os,
    current_platforms,
    is_all_architectures,
    is_all_ci,
    is_all_platforms,
    is_all_platforms_without_ci,
    is_all_traits,
    is_ci,
    is_unknown_linux,
    platforms_from_ids,
)

__all__ = (  # noqa: F405
    "AARCH64",
    "AIX",
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
    "ALL_PLATFORM_IDS",
    "ALL_PLATFORMS",
    "ALL_PLATFORMS_WITHOUT_CI",
    "ALL_SPARC",
    "ALL_TRAIT_IDS",
    "ALL_TRAITS",
    "ALL_WINDOWS",
    "ALTLINUX",
    "AMZN",
    "ANDROID",
    "ANY_ARM",
    "ANY_MIPS",
    "ANY_SPARC",
    "ANY_WINDOWS",
    "ARCH",
    "ARCH_32_BIT",
    "ARCH_64_BIT",
    "Architecture",
    "ARM",
    "ARMV5TEL",
    "ARMV6L",
    "ARMV7L",
    "ARMV8L",
    "AZURE_PIPELINES",
    "BAMBOO",
    "BSD",
    "BSD_WITHOUT_MACOS",
    "BUILDKITE",
    "BUILDROOT",
    "CACHYOS",
    "CENTOS",
    "CI",
    "CIRCLE_CI",
    "CIRRUS_CI",
    "CLOUDLINUX",
    "CODEBUILD",
    "current_architecture",
    "current_ci",
    "current_os",
    "current_platform",
    "current_platforms",
    "current_traits",
    "CYGWIN",
    "DEBIAN",
    "EXHERBO",
    "EXTRA_GROUPS",
    "FEDORA",
    "FREEBSD",
    "GENTOO",
    "GITHUB_CI",
    "GITLAB_CI",
    "Group",
    "groups_from_ids",
    "GUIX",
    "HEROKU_CI",
    "HURD",
    "I386",
    "I586",
    "I686",
    "IBM_MAINFRAME",
    "IBM_POWERKVM",
    "invalidate_caches",
    "is_aarch64",
    "is_aix",
    "is_all_architectures",
    "is_all_ci",
    "is_all_platforms",
    "is_all_platforms_without_ci",
    "is_all_traits",
    "is_altlinux",
    "is_amzn",
    "is_android",
    "is_any_architecture",  # noqa: F822
    "is_any_arm",  # noqa: F822
    "is_any_ci",  # noqa: F822
    "is_any_mips",  # noqa: F822
    "is_any_platform",  # noqa: F822
    "is_any_sparc",  # noqa: F822
    "is_any_trait",  # noqa: F822
    "is_any_windows",  # noqa: F822
    "is_arch",
    "is_arch_32_bit",  # noqa: F822
    "is_arch_64_bit",  # noqa: F822
    "is_arm",
    "is_armv5tel",
    "is_armv6l",
    "is_armv7l",
    "is_armv8l",
    "is_azure_pipelines",
    "is_bamboo",
    "is_bsd",  # noqa: F822
    "is_bsd_without_macos",  # noqa: F822
    "is_buildkite",
    "is_buildroot",
    "is_cachyos",
    "is_centos",
    "is_ci",
    "is_circle_ci",
    "is_cirrus_ci",
    "is_cloudlinux",
    "is_codebuild",
    "is_cygwin",
    "is_debian",
    "is_exherbo",
    "is_fedora",
    "is_freebsd",
    "is_gentoo",
    "is_github_ci",
    "is_gitlab_ci",
    "is_guix",
    "is_heroku_ci",
    "is_hurd",
    "is_i386",
    "is_i586",
    "is_i686",
    "is_ibm_mainframe",  # noqa: F822
    "is_ibm_powerkvm",
    "is_kvmibm",
    "is_linux",  # noqa: F822
    "is_linux_layers",  # noqa: F822
    "is_linux_like",  # noqa: F822
    "is_linuxmint",
    "is_loongarch",  # noqa: F822
    "is_loongarch64",
    "is_macos",
    "is_mageia",
    "is_mandriva",
    "is_midnightbsd",
    "is_mips",
    "is_mips64",
    "is_mips64el",
    "is_mipsel",
    "is_netbsd",
    "is_nobara",
    "is_openbsd",
    "is_opensuse",
    "is_oracle",
    "is_other_unix",  # noqa: F822
    "is_parallels",
    "is_pidora",
    "is_powerpc",  # noqa: F822
    "is_ppc",
    "is_ppc64",
    "is_ppc64le",
    "is_raspbian",
    "is_rhel",
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
    "is_teamcity",
    "is_travis_ci",
    "is_tumbleweed",  # noqa: F822
    "is_tuxedo",  # noqa: F822
    "is_ubuntu",
    "is_ultramarine",
    "is_unix",  # noqa: F822
    "is_unix_layers",  # noqa: F822
    "is_unix_without_macos",  # noqa: F822
    "is_unknown",  # noqa: F822
    "is_unknown_architecture",
    "is_unknown_ci",
    "is_unknown_linux",
    "is_unknown_platform",
    "is_wasm32",
    "is_wasm64",
    "is_webassembly",  # noqa: F822
    "is_windows",
    "is_wsl1",
    "is_wsl2",
    "is_x86",  # noqa: F822
    "is_x86_64",
    "is_xenserver",
    "KVMIBM",
    "LINUX",
    "LINUX_LAYERS",
    "LINUX_LIKE",
    "LINUXMINT",
    "LOONGARCH",
    "LOONGARCH64",
    "MACOS",
    "MAGEIA",
    "MANDRIVA",
    "MIDNIGHTBSD",
    "MIPS",
    "MIPS64",
    "MIPS64EL",
    "MIPSEL",
    "NETBSD",
    "NOBARA",
    "NON_OVERLAPPING_GROUPS",
    "OPENBSD",
    "OPENSUSE",
    "ORACLE",
    "OTHER_UNIX",
    "PARALLELS",
    "PIDORA",
    "Platform",
    "platforms_from_ids",
    "POWERPC",
    "PPC",
    "PPC64",
    "PPC64LE",
    "RASPBIAN",
    "reduce",
    "RHEL",
    "RISCV",
    "RISCV32",
    "RISCV64",
    "ROCKY",
    "S390X",
    "SCIENTIFIC",
    "SLACKWARE",
    "SLES",
    "SOLARIS",
    "SPARC",
    "SPARC64",
    "SUNOS",
    "SYSTEM_V",
    "TEAMCITY",
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
    "UNKNOWN_ARCHITECTURE",
    "UNKNOWN_CI",
    "UNKNOWN_LINUX",
    "UNKNOWN_PLATFORM",
    "WASM32",
    "WASM64",
    "WEBASSEMBLY",
    "WINDOWS",
    "WSL1",
    "WSL2",
    "X86",
    "X86_64",
    "XENSERVER",
)
"""Expose all package-wide elements.

.. note::
    The content of ``__all__`` is checked and enforced in unittests.

.. todo::
    Test Ruff's ``__all__`` formatting capabilities. And if good enough, remove
    ``__all__`` checks in unittests.
"""
