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

import platform as stdlib_platform
import sys
from functools import cache

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable


# This message is put up there because it is used in multiple places in other files.
_report_msg = (
    "Please report this at https://github.com/kdeldycke/extra-platforms/issues to "
    "improve detection heuristics."
)

from . import detection  # noqa: E402
from .architecture import Architecture  # noqa: E402
from .architecture_data import (  # noqa: E402
    AARCH64,
    ARM,
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
from .ci import CI  # noqa: E402
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
    is_unknown_architecture,
    is_unknown_ci,
    is_unknown_linux,
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
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_GROUPS,
    ALL_PLATFORMS,
    ALL_PLATFORMS_WITHOUT_CI,
    ALL_TRAITS,
    ANY_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    EXTRA_GROUPS,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    NON_OVERLAPPING_GROUPS,
    OTHER_UNIX,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
)
from .platform import Platform  # noqa: E402
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
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
)
from .trait import Trait  # noqa: E402

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
    platforms_from_ids,
    reduce,
)

__version__ = "5.1.1"


@cache
def current_architecture() -> Architecture:
    """Returns the ``Architecture`` matching the current environment.

    Always raises an error if the current environment is not recognized.
    """
    matching = []
    for arch in ALL_ARCHITECTURES.platforms:
        if arch.current:
            matching.append(arch)

    # Return the only matching architecture.
    if len(matching) == 1:
        return matching.pop()

    if not matching:
        # Dump the raw data provided by all primitives used for detection.
        raise SystemError(
            f"Unrecognized {stdlib_platform.machine()!r} / {sys.platform!r} / "
            f"{stdlib_platform.architecture()!r} architecture. {_report_msg}"
        )

    raise RuntimeError(
        f"Multiple architectures match current environment: {matching!r}. {_report_msg}"
    )


@cache
def current_platforms() -> tuple[Platform, ...]:
    """Evaluates all heuristics and returns a list of ``Platform`` matching the current
    environment.

    Always raises an error if the current environment is not recognized.

    .. attention::
        At this point it is too late to worry about caching. This function has no
        choice but to evaluate all platforms detection heuristics.
    """
    matching = []
    for p in ALL_PLATFORMS.platforms:
        if p.current:
            matching.append(p)

    if not matching:
        # Dump the raw data provided by all primitives used for detection.
        raise SystemError(
            f"Unrecognized {sys.platform!r} / "
            f"{stdlib_platform.platform(aliased=True, terse=True)!r} platform. "
            f"{_report_msg}"
        )

    return tuple(matching)


@cache
def current_os() -> Platform:
    """Always returns the best matching platform for the current environment, excluding
    CI systems.

    If multiple platforms match the current environment, this function will try to
    select the best, informative one.

    Raises an error if we can't decide on a single, appropriate platform.
    """
    matching = set(current_platforms()).difference(ALL_CI.platforms)

    # Return the only matching platform.
    if len(matching) == 1:
        return matching.pop()

    # Remove unknown Linux, which is too generic to be useful.
    if UNKNOWN_LINUX in matching:
        matching.remove(UNKNOWN_LINUX)
        if len(matching) == 1:
            return matching.pop()

    # Remove WSL1, then WSL2, until we have a single match. WSL is a generic platform,
    # so we should prefer the other, more specific platform matches like Ubuntu. See:
    # - https://github.com/kdeldycke/extra-platforms/issues/158
    # - https://github.com/kdeldycke/meta-package-manager/issues/944
    for wsl in (WSL1, WSL2):
        if wsl in matching:
            matching.remove(wsl)
            if len(matching) == 1:
                return matching.pop()

    # Our meta-heuristics above failed to decide on a single, appropriate platform.
    raise RuntimeError(
        f"Multiple platforms match current environment: {matching!r}. {_report_msg}"
    )


def current_traits() -> set[Trait]:
    """Returns all traits matching the current environment.

    This includes platforms, architectures, and CI systems.
    """
    traits = set()
    for trait in ALL_TRAITS.platforms:
        if trait.current:
            traits.add(trait)

    if len(traits) == 0:
        raise SystemError(f"Unrecognized system. {_report_msg}")

    return traits


def _generate_group_membership_func(_group: Group) -> Callable:
    """Factory to dynamiccaly produce a group membership test function."""

    def group_membership_check() -> bool:
        """Compares all the current traits to the ``_group``.

        Returns ``True`` if at least one trait is part of the group, ``False``
        otherwise.
        """
        return any(t in _group for t in current_traits())

    group_membership_check.__doc__ = (
        "Returns ``True`` if at least one trait is part of the group composed of "
        f"{_group.short_desc}, ``False`` otherwise."
    )
    return cache(group_membership_check)


_group_membership_func_ids = []
for _group in ALL_GROUPS:
    _func_id = f"is_{_group.id}"
    assert _func_id not in locals(), f"Function ID {_func_id} already defined locally."
    _group_membership_func_ids.append(_func_id)
    globals()[_func_id] = _generate_group_membership_func(_group)
"""Generates an ``is_<group.id>()`` local function for each group.

These functions return a boolean value indicating the membership of the current
system into that group.

Since traits and groups have unique, non-overlapping IDs, we can create a
``is_<group.id>`` method for each group. The value of this boolean variable mark the
membership of the current system to that group.
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

    # Invalidate cached properties of the Platform and Architecture classes.
    for member in ALL_TRAITS.platforms:
        if "current" in vars(member):
            # Use object.__delattr__ to bypass frozen dataclass restriction.
            object.__delattr__(member, "current")

    # Invalidate detection module cached functions.
    for func_id in dir(detection):
        func = getattr(detection, func_id)
        if callable(func) and hasattr(func, "cache_clear"):
            func.cache_clear()

    # Invalidate current_architecture, current_platforms and current_os caches.
    current_architecture.cache_clear()
    current_platforms.cache_clear()
    current_os.cache_clear()

    # Invalidate dynamically generated group membership functions.
    for func_id in _group_membership_func_ids:
        globals()[func_id].cache_clear()


__all__ = (  # noqa: F405
    "AARCH64",
    "AIX",
    "ALL_ARCHITECTURES",
    "ALL_CI",
    "ALL_GROUP_IDS",
    "ALL_GROUPS",
    "ALL_IDS",
    "ALL_PLATFORMS",
    "ALL_PLATFORMS_WITHOUT_CI",
    "ALL_TRAIT_IDS",
    "ALL_TRAITS",
    "ALTLINUX",
    "AMZN",
    "ANDROID",
    "ANY_WINDOWS",
    "ARCH",
    "Architecture",
    "ARM",
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
    "current_os",
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
    "IBM_POWERKVM",
    "invalidate_caches",
    "is_aarch64",
    "is_aix",
    "is_all_architectures",  # noqa: F822
    "is_all_ci",  # noqa: F822
    "is_all_platforms",  # noqa: F822
    "is_all_traits",  # noqa: F822
    "is_altlinux",
    "is_amzn",
    "is_android",
    "is_any_windows",  # noqa: F822
    "is_arch",
    "is_arm",
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
    "is_ibm_powerkvm",
    "is_kvmibm",
    "is_linux",  # noqa: F822
    "is_linux_layers",  # noqa: F822
    "is_linux_like",  # noqa: F822
    "is_linuxmint",
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
    "is_ppc",
    "is_ppc64",
    "is_ppc64le",
    "is_raspbian",
    "is_rhel",
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
    "is_unknown_architecture",
    "is_unknown_ci",
    "is_unknown_linux",
    "is_wasm32",
    "is_wasm64",
    "is_windows",
    "is_wsl1",
    "is_wsl2",
    "is_x86_64",
    "is_xenserver",
    "KVMIBM",
    "LINUX",
    "LINUX_LAYERS",
    "LINUX_LIKE",
    "LINUXMINT",
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
    "PPC",
    "PPC64",
    "PPC64LE",
    "RASPBIAN",
    "reduce",
    "RHEL",
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
    "TRAVIS_CI",
    "TUMBLEWEED",
    "TUXEDO",
    "UBUNTU",
    "ULTRAMARINE",
    "UNIX",
    "UNIX_LAYERS",
    "UNIX_WITHOUT_MACOS",
    "UNKNOWN_ARCHITECTURE",
    "UNKNOWN_CI",
    "UNKNOWN_LINUX",
    "WASM32",
    "WASM64",
    "WINDOWS",
    "WSL1",
    "WSL2",
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
