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


__all__ = (
    "skip_aix",  # noqa: F405, F822
    "skip_all_platforms",  # noqa: F405, F822
    "skip_all_platforms_without_ci",  # noqa: F405, F822
    "skip_altlinux",  # noqa: F405, F822
    "skip_amzn",  # noqa: F405, F822
    "skip_android",  # noqa: F405, F822
    "skip_any_windows",  # noqa: F405, F822
    "skip_arch",  # noqa: F405, F822
    "skip_azure_pipelines",  # noqa: F405, F822
    "skip_bamboo",  # noqa: F405, F822
    "skip_bsd",  # noqa: F405, F822
    "skip_bsd_without_macos",  # noqa: F405, F822
    "skip_buildkite",  # noqa: F405, F822
    "skip_buildroot",  # noqa: F405, F822
    "skip_centos",  # noqa: F405, F822
    "skip_ci",  # noqa: F405, F822
    "skip_circle_ci",  # noqa: F405, F822
    "skip_cirrus_ci",  # noqa: F405, F822
    "skip_cloudlinux",  # noqa: F405, F822
    "skip_codebuild",  # noqa: F405, F822
    "skip_cygwin",  # noqa: F405, F822
    "skip_debian",  # noqa: F405, F822
    "skip_exherbo",  # noqa: F405, F822
    "skip_fedora",  # noqa: F405, F822
    "skip_freebsd",  # noqa: F405, F822
    "skip_gentoo",  # noqa: F405, F822
    "skip_github_ci",  # noqa: F405, F822
    "skip_gitlab_ci",  # noqa: F405, F822
    "skip_guix",  # noqa: F405, F822
    "skip_heroku_ci",  # noqa: F405, F822
    "skip_hurd",  # noqa: F405, F822
    "skip_ibm_powerkvm",  # noqa: F405, F822
    "skip_kvmibm",  # noqa: F405, F822
    "skip_linux",  # noqa: F405, F822
    "skip_linux_layers",  # noqa: F405, F822
    "skip_linux_like",  # noqa: F405, F822
    "skip_linuxmint",  # noqa: F405, F822
    "skip_macos",  # noqa: F405, F822
    "skip_mageia",  # noqa: F405, F822
    "skip_mandriva",  # noqa: F405, F822
    "skip_midnightbsd",  # noqa: F405, F822
    "skip_netbsd",  # noqa: F405, F822
    "skip_nobara",  # noqa: F405, F822
    "skip_openbsd",  # noqa: F405, F822
    "skip_opensuse",  # noqa: F405, F822
    "skip_oracle",  # noqa: F405, F822
    "skip_other_unix",  # noqa: F405, F822
    "skip_parallels",  # noqa: F405, F822
    "skip_pidora",  # noqa: F405, F822
    "skip_raspbian",  # noqa: F405, F822
    "skip_rhel",  # noqa: F405, F822
    "skip_rocky",  # noqa: F405, F822
    "skip_scientific",  # noqa: F405, F822
    "skip_slackware",  # noqa: F405, F822
    "skip_sles",  # noqa: F405, F822
    "skip_solaris",  # noqa: F405, F822
    "skip_sunos",  # noqa: F405, F822
    "skip_system_v",  # noqa: F405, F822
    "skip_teamcity",  # noqa: F405, F822
    "skip_travis_ci",  # noqa: F405, F822
    "skip_tumbleweed",  # noqa: F405, F822
    "skip_tuxedo",  # noqa: F405, F822
    "skip_ubuntu",  # noqa: F405, F822
    "skip_unix",  # noqa: F405, F822
    "skip_unix_layers",  # noqa: F405, F822
    "skip_unix_without_macos",  # noqa: F405, F822
    "skip_unknown_ci",  # noqa: F405, F822
    "skip_unknown_linux",  # noqa: F405, F822
    "skip_windows",  # noqa: F405, F822
    "skip_wsl1",  # noqa: F405, F822
    "skip_wsl2",  # noqa: F405, F822
    "skip_xenserver",  # noqa: F405, F822
    "unless_aix",  # noqa: F405, F822
    "unless_all_platforms",  # noqa: F405, F822
    "unless_all_platforms_without_ci",  # noqa: F405, F822
    "unless_altlinux",  # noqa: F405, F822
    "unless_amzn",  # noqa: F405, F822
    "unless_android",  # noqa: F405, F822
    "unless_any_windows",  # noqa: F405, F822
    "unless_arch",  # noqa: F405, F822
    "unless_azure_pipelines",  # noqa: F405, F822
    "unless_bamboo",  # noqa: F405, F822
    "unless_bsd",  # noqa: F405, F822
    "unless_bsd_without_macos",  # noqa: F405, F822
    "unless_buildkite",  # noqa: F405, F822
    "unless_buildroot",  # noqa: F405, F822
    "unless_centos",  # noqa: F405, F822
    "unless_ci",  # noqa: F405, F822
    "unless_circle_ci",  # noqa: F405, F822
    "unless_cirrus_ci",  # noqa: F405, F822
    "unless_cloudlinux",  # noqa: F405, F822
    "unless_codebuild",  # noqa: F405, F822
    "unless_cygwin",  # noqa: F405, F822
    "unless_debian",  # noqa: F405, F822
    "unless_exherbo",  # noqa: F405, F822
    "unless_fedora",  # noqa: F405, F822
    "unless_freebsd",  # noqa: F405, F822
    "unless_gentoo",  # noqa: F405, F822
    "unless_github_ci",  # noqa: F405, F822
    "unless_gitlab_ci",  # noqa: F405, F822
    "unless_guix",  # noqa: F405, F822
    "unless_heroku_ci",  # noqa: F405, F822
    "unless_hurd",  # noqa: F405, F822
    "unless_ibm_powerkvm",  # noqa: F405, F822
    "unless_kvmibm",  # noqa: F405, F822
    "unless_linux",  # noqa: F405, F822
    "unless_linux_layers",  # noqa: F405, F822
    "unless_linux_like",  # noqa: F405, F822
    "unless_linuxmint",  # noqa: F405, F822
    "unless_macos",  # noqa: F405, F822
    "unless_mageia",  # noqa: F405, F822
    "unless_mandriva",  # noqa: F405, F822
    "unless_midnightbsd",  # noqa: F405, F822
    "unless_netbsd",  # noqa: F405, F822
    "unless_nobara",  # noqa: F405, F822
    "unless_openbsd",  # noqa: F405, F822
    "unless_opensuse",  # noqa: F405, F822
    "unless_oracle",  # noqa: F405, F822
    "unless_other_unix",  # noqa: F405, F822
    "unless_parallels",  # noqa: F405, F822
    "unless_pidora",  # noqa: F405, F822
    "unless_raspbian",  # noqa: F405, F822
    "unless_rhel",  # noqa: F405, F822
    "unless_rocky",  # noqa: F405, F822
    "unless_scientific",  # noqa: F405, F822
    "unless_slackware",  # noqa: F405, F822
    "unless_sles",  # noqa: F405, F822
    "unless_solaris",  # noqa: F405, F822
    "unless_sunos",  # noqa: F405, F822
    "unless_system_v",  # noqa: F405, F822
    "unless_teamcity",  # noqa: F405, F822
    "unless_travis_ci",  # noqa: F405, F822
    "unless_tumbleweed",  # noqa: F405, F822
    "unless_tuxedo",  # noqa: F405, F822
    "unless_ubuntu",  # noqa: F405, F822
    "unless_unix",  # noqa: F405, F822
    "unless_unix_layers",  # noqa: F405, F822
    "unless_unix_without_macos",  # noqa: F405, F822
    "unless_unknown_ci",  # noqa: F405, F822
    "unless_unknown_linux",  # noqa: F405, F822
    "unless_windows",  # noqa: F405, F822
    "unless_wsl1",  # noqa: F405, F822
    "unless_wsl2",  # noqa: F405, F822
    "unless_xenserver",  # noqa: F405, F822
)
"""Expose all generated decorators.

.. note::
    The content of ``__all__`` is checked and enforced in unittests.
"""
