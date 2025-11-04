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
from .group_data import ALL_GROUPS, ALL_PLATFORMS
from .platform import Platform

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable


class DeferredCondition:
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


# Generate a pair of skip/unless decorators for each platform and group.
for obj in chain(ALL_PLATFORMS, ALL_GROUPS):
    # Sanity check to please the type checker.
    assert isinstance(obj, (Platform, Group))

    # Get the detection function for the current object.
    func = getattr(extra_platforms, f"is_{obj.id}")

    # Generate @skip decorator.
    skip_id = f"skip_{obj.id}"
    globals()[skip_id] = pytest.mark.skipif(
        DeferredCondition(func),  # type: ignore[arg-type]
        reason=f"Skip {obj.short_desc}",
    )

    # Generate @unless decorator.
    unless_id = f"unless_{obj.id}"
    globals()[unless_id] = pytest.mark.skipif(
        DeferredCondition(func, invert=True),  # type: ignore[arg-type]
        reason=f"Requires {obj.short_desc}",
    )


__all__ = (  # noqa: F405, F822
    "skip_aix",
    "skip_all_platforms",
    "skip_all_platforms_without_ci",
    "skip_altlinux",
    "skip_amzn",
    "skip_android",
    "skip_any_windows",
    "skip_arch",
    "skip_azure_pipelines",
    "skip_bamboo",
    "skip_bsd",
    "skip_bsd_without_macos",
    "skip_buildkite",
    "skip_buildroot",
    "skip_centos",
    "skip_ci",
    "skip_circle_ci",
    "skip_cirrus_ci",
    "skip_cloudlinux",
    "skip_codebuild",
    "skip_cygwin",
    "skip_debian",
    "skip_exherbo",
    "skip_fedora",
    "skip_freebsd",
    "skip_gentoo",
    "skip_github_ci",
    "skip_gitlab_ci",
    "skip_guix",
    "skip_heroku_ci",
    "skip_hurd",
    "skip_ibm_powerkvm",
    "skip_kvmibm",
    "skip_linux",
    "skip_linux_layers",
    "skip_linux_like",
    "skip_linuxmint",
    "skip_macos",
    "skip_mageia",
    "skip_mandriva",
    "skip_midnightbsd",
    "skip_netbsd",
    "skip_nobara",
    "skip_openbsd",
    "skip_opensuse",
    "skip_oracle",
    "skip_other_unix",
    "skip_parallels",
    "skip_pidora",
    "skip_raspbian",
    "skip_rhel",
    "skip_rocky",
    "skip_scientific",
    "skip_slackware",
    "skip_sles",
    "skip_solaris",
    "skip_sunos",
    "skip_system_v",
    "skip_teamcity",
    "skip_travis_ci",
    "skip_tumbleweed",
    "skip_tuxedo",
    "skip_ubuntu",
    "skip_ultramarine",
    "skip_unix",
    "skip_unix_layers",
    "skip_unix_without_macos",
    "skip_unknown_ci",
    "skip_unknown_linux",
    "skip_windows",
    "skip_wsl1",
    "skip_wsl2",
    "skip_xenserver",
    "unless_aix",
    "unless_all_platforms",
    "unless_all_platforms_without_ci",
    "unless_altlinux",
    "unless_amzn",
    "unless_android",
    "unless_any_windows",
    "unless_arch",
    "unless_azure_pipelines",
    "unless_bamboo",
    "unless_bsd",
    "unless_bsd_without_macos",
    "unless_buildkite",
    "unless_buildroot",
    "unless_centos",
    "unless_ci",
    "unless_circle_ci",
    "unless_cirrus_ci",
    "unless_cloudlinux",
    "unless_codebuild",
    "unless_cygwin",
    "unless_debian",
    "unless_exherbo",
    "unless_fedora",
    "unless_freebsd",
    "unless_gentoo",
    "unless_github_ci",
    "unless_gitlab_ci",
    "unless_guix",
    "unless_heroku_ci",
    "unless_hurd",
    "unless_ibm_powerkvm",
    "unless_kvmibm",
    "unless_linux",
    "unless_linux_layers",
    "unless_linux_like",
    "unless_linuxmint",
    "unless_macos",
    "unless_mageia",
    "unless_mandriva",
    "unless_midnightbsd",
    "unless_netbsd",
    "unless_nobara",
    "unless_openbsd",
    "unless_opensuse",
    "unless_oracle",
    "unless_other_unix",
    "unless_parallels",
    "unless_pidora",
    "unless_raspbian",
    "unless_rhel",
    "unless_rocky",
    "unless_scientific",
    "unless_slackware",
    "unless_sles",
    "unless_solaris",
    "unless_sunos",
    "unless_system_v",
    "unless_teamcity",
    "unless_travis_ci",
    "unless_tumbleweed",
    "unless_tuxedo",
    "unless_ubuntu",
    "unless_ultramarine",
    "unless_unix",
    "unless_unix_layers",
    "unless_unix_without_macos",
    "unless_unknown_ci",
    "unless_unknown_linux",
    "unless_windows",
    "unless_wsl1",
    "unless_wsl2",
    "unless_xenserver",
)
"""Expose all generated decorators.

.. note::
    The content of ``__all__`` is checked and enforced in unittests.
"""
