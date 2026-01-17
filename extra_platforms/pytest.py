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
"""Pytest decorators to skip tests depending on the platform they're run on.

Generates a pair of ready-to-use ``@skip_<id>`` and ``@unless_<id>`` decorators for
each platform and group.
"""

from __future__ import annotations

try:
    import pytest  # noqa: F401
except ImportError:
    raise ImportError(
        "You need to install extra_platforms[pytest] extra dependencies to use this "
        "module."
    )

from itertools import chain

import extra_platforms

from .group import Group
from .group_data import ALL_GROUPS, ALL_TRAITS
from .trait import Trait

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable

    from _pytest.mark.structures import MarkDecorator


class _DeferredCondition:
    """Defer the evaluation of a condition.

    This allow a callable returning a boolean to be evaluated only when the boolean
    value is requested.

    Pytest's marks can have a condition attached to them. Which is practical for
    implementing our own ready-to-use ``@skip`` and ``@unless`` decorators.

    The problem is: this condition is evaluated at import time. Which leads to all our
    platform detection heuristics to be called when we generates our custom decorators
    below.

    This issue is being discussed upstream at:
        - https://github.com/pytest-dev/pytest/issues/7395
        - https://github.com/pytest-dev/pytest/issues/9650
    """

    def __init__(self, condition: Callable[[], bool], invert: bool = False) -> None:
        self.condition = condition
        self.invert = invert

    def __bool__(self) -> bool:
        """Call the deferred condition and return its result."""
        result = self.condition()
        return not result if self.invert else result

    def __call__(self) -> bool:
        """Allow the condition to be called as a function."""
        return bool(self)


def _make_decorator_docstring(obj: Trait | Group, is_skip: bool) -> str:
    """Generate a reStructuredText docstring for a pytest decorator.

    Creates a concise docstring with links to the associated trait/group and
    its detection function, using unambiguous language about the behavior.

    Args:
        obj: The trait or group to document.
        is_skip: Whether this is a skip decorator (True) or unless decorator (False).

    Returns:
        A reStructuredText docstring.
    """
    # Create reference links using Sphinx roles for concise cross-referencing.
    symbol_link = f":data:`~extra_platforms.{obj.symbol_id}`"
    detection_link = f":func:`~extra_platforms.{obj.detection_func_id}`"

    is_group = isinstance(obj, Group)

    if is_skip:
        if is_group:
            summary = (
                f"Skip test if current environment matches any member of the "
                f"{symbol_link} group (i.e., when {detection_link} returns ``True``)."
            )
        else:
            summary = (
                f"Skip test if current environment is {symbol_link} "
                f"(i.e., when {detection_link} returns ``True``)."
            )
    else:
        if is_group:
            summary = (
                f"Run test only if current environment matches any member of the "
                f"{symbol_link} group (i.e., when {detection_link} returns ``True``). "
                f"Skip otherwise."
            )
        else:
            summary = (
                f"Run test only if current environment is {symbol_link} "
                f"(i.e., when {detection_link} returns ``True``). Skip otherwise."
            )

    return summary


# Generate a pair of skip/unless decorators for each platform and group.
for _obj in chain(ALL_TRAITS, ALL_GROUPS):
    # Sanity check to please the type checker.
    assert isinstance(_obj, (Trait, Group))

    # Get the detection function for the current object.
    _func = getattr(extra_platforms, _obj.detection_func_id)

    # Generate both skip and unless decorators for this object.
    for _is_skip in [True, False]:
        _decorator_id = _obj.skip_decorator_id if _is_skip else _obj.unless_decorator_id
        _reason_prefix = "Skip" if _is_skip else "Requires"
        _condition = _DeferredCondition(_func, invert=not _is_skip)

        _decorator = pytest.mark.skipif(
            _condition,  # type: ignore[arg-type]
            reason=f"{_reason_prefix} {_obj.name[0].lower() + _obj.name[1:]}",
        )

        # Set a custom docstring for Sphinx autodoc.
        _decorator.__doc__ = _make_decorator_docstring(_obj, is_skip=_is_skip)

        globals()[_decorator_id] = _decorator


# XXX Mypy doesn't understand dynamic type annotation, so we need to explicitly declare
# all generated decorators after their generation.
# These annotations are checked and enforced in unittests.
if TYPE_CHECKING:
    skip_aarch64: MarkDecorator
    skip_aix: MarkDecorator
    skip_all_architectures: MarkDecorator
    skip_all_arm: MarkDecorator
    skip_all_ci: MarkDecorator
    skip_all_mips: MarkDecorator
    skip_all_platforms: MarkDecorator
    skip_all_sparc: MarkDecorator
    skip_all_traits: MarkDecorator
    skip_all_windows: MarkDecorator
    skip_altlinux: MarkDecorator
    skip_amzn: MarkDecorator
    skip_android: MarkDecorator
    skip_arch: MarkDecorator
    skip_arch_32_bit: MarkDecorator
    skip_arch_64_bit: MarkDecorator
    skip_arm: MarkDecorator
    skip_armv5tel: MarkDecorator
    skip_armv6l: MarkDecorator
    skip_armv7l: MarkDecorator
    skip_armv8l: MarkDecorator
    skip_azure_pipelines: MarkDecorator
    skip_bamboo: MarkDecorator
    skip_bsd: MarkDecorator
    skip_bsd_not_macos: MarkDecorator
    skip_buildkite: MarkDecorator
    skip_buildroot: MarkDecorator
    skip_cachyos: MarkDecorator
    skip_centos: MarkDecorator
    skip_circle_ci: MarkDecorator
    skip_cirrus_ci: MarkDecorator
    skip_cloudlinux: MarkDecorator
    skip_codebuild: MarkDecorator
    skip_cygwin: MarkDecorator
    skip_debian: MarkDecorator
    skip_dragonfly_bsd: MarkDecorator
    skip_exherbo: MarkDecorator
    skip_fedora: MarkDecorator
    skip_freebsd: MarkDecorator
    skip_gentoo: MarkDecorator
    skip_github_ci: MarkDecorator
    skip_gitlab_ci: MarkDecorator
    skip_guix: MarkDecorator
    skip_haiku: MarkDecorator
    skip_heroku_ci: MarkDecorator
    skip_hurd: MarkDecorator
    skip_i386: MarkDecorator
    skip_i586: MarkDecorator
    skip_i686: MarkDecorator
    skip_ibm_mainframe: MarkDecorator
    skip_ibm_powerkvm: MarkDecorator
    skip_illumos: MarkDecorator
    skip_kvmibm: MarkDecorator
    skip_linux: MarkDecorator
    skip_linux_layers: MarkDecorator
    skip_linux_like: MarkDecorator
    skip_linuxmint: MarkDecorator
    skip_loongarch: MarkDecorator
    skip_loongarch64: MarkDecorator
    skip_macos: MarkDecorator
    skip_mageia: MarkDecorator
    skip_mandriva: MarkDecorator
    skip_midnightbsd: MarkDecorator
    skip_mips: MarkDecorator
    skip_mips64: MarkDecorator
    skip_mips64el: MarkDecorator
    skip_mipsel: MarkDecorator
    skip_netbsd: MarkDecorator
    skip_nobara: MarkDecorator
    skip_openbsd: MarkDecorator
    skip_opensuse: MarkDecorator
    skip_oracle: MarkDecorator
    skip_other_posix: MarkDecorator
    skip_parallels: MarkDecorator
    skip_pidora: MarkDecorator
    skip_powerpc: MarkDecorator
    skip_ppc: MarkDecorator
    skip_ppc64: MarkDecorator
    skip_ppc64le: MarkDecorator
    skip_raspbian: MarkDecorator
    skip_rhel: MarkDecorator
    skip_riscv: MarkDecorator
    skip_riscv32: MarkDecorator
    skip_riscv64: MarkDecorator
    skip_rocky: MarkDecorator
    skip_s390x: MarkDecorator
    skip_scientific: MarkDecorator
    skip_slackware: MarkDecorator
    skip_sles: MarkDecorator
    skip_solaris: MarkDecorator
    skip_sparc: MarkDecorator
    skip_sparc64: MarkDecorator
    skip_sunos: MarkDecorator
    skip_system_v: MarkDecorator
    skip_teamcity: MarkDecorator
    skip_travis_ci: MarkDecorator
    skip_tumbleweed: MarkDecorator
    skip_tuxedo: MarkDecorator
    skip_ubuntu: MarkDecorator
    skip_ultramarine: MarkDecorator
    skip_unix: MarkDecorator
    skip_unix_layers: MarkDecorator
    skip_unix_not_macos: MarkDecorator
    skip_unknown: MarkDecorator
    skip_unknown_architecture: MarkDecorator
    skip_unknown_ci: MarkDecorator
    skip_unknown_platform: MarkDecorator
    skip_wasm32: MarkDecorator
    skip_wasm64: MarkDecorator
    skip_webassembly: MarkDecorator
    skip_windows: MarkDecorator
    skip_wsl1: MarkDecorator
    skip_wsl2: MarkDecorator
    skip_x86: MarkDecorator
    skip_x86_64: MarkDecorator
    skip_xenserver: MarkDecorator
    unless_aarch64: MarkDecorator
    unless_aix: MarkDecorator
    unless_altlinux: MarkDecorator
    unless_amzn: MarkDecorator
    unless_android: MarkDecorator
    unless_any_architecture: MarkDecorator
    unless_any_arm: MarkDecorator
    unless_any_ci: MarkDecorator
    unless_any_mips: MarkDecorator
    unless_any_platform: MarkDecorator
    unless_any_sparc: MarkDecorator
    unless_any_trait: MarkDecorator
    unless_any_windows: MarkDecorator
    unless_arch: MarkDecorator
    unless_arch_32_bit: MarkDecorator
    unless_arch_64_bit: MarkDecorator
    unless_arm: MarkDecorator
    unless_armv5tel: MarkDecorator
    unless_armv6l: MarkDecorator
    unless_armv7l: MarkDecorator
    unless_armv8l: MarkDecorator
    unless_azure_pipelines: MarkDecorator
    unless_bamboo: MarkDecorator
    unless_bsd: MarkDecorator
    unless_bsd_not_macos: MarkDecorator
    unless_buildkite: MarkDecorator
    unless_buildroot: MarkDecorator
    unless_cachyos: MarkDecorator
    unless_centos: MarkDecorator
    unless_circle_ci: MarkDecorator
    unless_cirrus_ci: MarkDecorator
    unless_cloudlinux: MarkDecorator
    unless_codebuild: MarkDecorator
    unless_cygwin: MarkDecorator
    unless_debian: MarkDecorator
    unless_dragonfly_bsd: MarkDecorator
    unless_exherbo: MarkDecorator
    unless_fedora: MarkDecorator
    unless_freebsd: MarkDecorator
    unless_gentoo: MarkDecorator
    unless_github_ci: MarkDecorator
    unless_gitlab_ci: MarkDecorator
    unless_guix: MarkDecorator
    unless_haiku: MarkDecorator
    unless_heroku_ci: MarkDecorator
    unless_hurd: MarkDecorator
    unless_i386: MarkDecorator
    unless_i586: MarkDecorator
    unless_i686: MarkDecorator
    unless_ibm_mainframe: MarkDecorator
    unless_ibm_powerkvm: MarkDecorator
    unless_illumos: MarkDecorator
    unless_kvmibm: MarkDecorator
    unless_linux: MarkDecorator
    unless_linux_layers: MarkDecorator
    unless_linux_like: MarkDecorator
    unless_linuxmint: MarkDecorator
    unless_loongarch: MarkDecorator
    unless_loongarch64: MarkDecorator
    unless_macos: MarkDecorator
    unless_mageia: MarkDecorator
    unless_mandriva: MarkDecorator
    unless_midnightbsd: MarkDecorator
    unless_mips: MarkDecorator
    unless_mips64: MarkDecorator
    unless_mips64el: MarkDecorator
    unless_mipsel: MarkDecorator
    unless_netbsd: MarkDecorator
    unless_nobara: MarkDecorator
    unless_openbsd: MarkDecorator
    unless_opensuse: MarkDecorator
    unless_oracle: MarkDecorator
    unless_other_posix: MarkDecorator
    unless_parallels: MarkDecorator
    unless_pidora: MarkDecorator
    unless_powerpc: MarkDecorator
    unless_ppc: MarkDecorator
    unless_ppc64: MarkDecorator
    unless_ppc64le: MarkDecorator
    unless_raspbian: MarkDecorator
    unless_rhel: MarkDecorator
    unless_riscv: MarkDecorator
    unless_riscv32: MarkDecorator
    unless_riscv64: MarkDecorator
    unless_rocky: MarkDecorator
    unless_s390x: MarkDecorator
    unless_scientific: MarkDecorator
    unless_slackware: MarkDecorator
    unless_sles: MarkDecorator
    unless_solaris: MarkDecorator
    unless_sparc: MarkDecorator
    unless_sparc64: MarkDecorator
    unless_sunos: MarkDecorator
    unless_system_v: MarkDecorator
    unless_teamcity: MarkDecorator
    unless_travis_ci: MarkDecorator
    unless_tumbleweed: MarkDecorator
    unless_tuxedo: MarkDecorator
    unless_ubuntu: MarkDecorator
    unless_ultramarine: MarkDecorator
    unless_unix: MarkDecorator
    unless_unix_layers: MarkDecorator
    unless_unix_not_macos: MarkDecorator
    unless_unknown: MarkDecorator
    unless_unknown_architecture: MarkDecorator
    unless_unknown_ci: MarkDecorator
    unless_unknown_platform: MarkDecorator
    unless_wasm32: MarkDecorator
    unless_wasm64: MarkDecorator
    unless_webassembly: MarkDecorator
    unless_windows: MarkDecorator
    unless_wsl1: MarkDecorator
    unless_wsl2: MarkDecorator
    unless_x86: MarkDecorator
    unless_x86_64: MarkDecorator
    unless_xenserver: MarkDecorator
