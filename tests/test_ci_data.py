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
"""Test all CI definitions, detection and CI-specific groups."""

from __future__ import annotations

import ast
import functools
import inspect
import json
import os
import sys
from pathlib import Path

from extra_platforms import (  # type: ignore[attr-defined]
    AARCH64,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_TRAITS,
    BASH,
    GITHUB_CI,
    MACOS,
    NON_OVERLAPPING_GROUPS,
    POWERSHELL,
    UBUNTU,
    UNKNOWN_CI,
    WINDOWS,
    WSL2,
    X86_64,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
    current_traits,
    is_aarch64,
    is_any_architecture,
    is_any_arm,
    is_any_ci,
    is_any_platform,
    is_any_shell,
    is_any_trait,
    is_any_windows,
    is_arch_32_bit,
    is_arch_64_bit,
    is_arm,
    is_azure_pipelines,
    is_bamboo,
    is_bash,
    is_big_endian,
    is_bourne_shells,
    is_bsd,
    is_buildkite,
    is_circle_ci,
    is_cirrus_ci,
    is_codebuild,
    is_github_ci,
    is_gitlab_ci,
    is_heroku_ci,
    is_linux,
    is_linux_layers,
    is_linux_like,
    is_little_endian,
    is_macos,
    is_powershell,
    is_teamcity,
    is_travis_ci,
    is_ubuntu,
    is_unix,
    is_unix_not_macos,
    is_unknown_architecture,
    is_unknown_ci,
    is_unknown_platform,
    is_unknown_shell,
    is_windows,
    is_windows_shells,
    is_wsl2,
    is_x86,
    is_x86_64,
)
from extra_platforms import ci_data as ci_data_module
from extra_platforms.pytest import unless_github_ci


@functools.cache
def github_runner_os() -> str | None:
    """Returns the OS name as defined in the GitHub Actions matrix context.

    .. caution::
        This only works when running inside a GitHub Actions job that uses a ``matrix``
        strategy with an ``os`` variant. Which is the case for the ``extra-platforms``
        workflows.
    """
    matrix_context_str = os.environ.get("EXTRA_PLATFORMS_TEST_MATRIX", "{}")
    matrix_context = json.loads(matrix_context_str)
    os_value = matrix_context.get("os")
    if isinstance(os_value, str):
        return os_value
    return None


def test_ci_data_sorting():
    """CI instances must be sorted alphabetically."""
    ci_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(ci_data_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            assert node.value.func.id == "CI"
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            ci_instance_ids.append(instance_id)

    assert ci_instance_ids == sorted(ci_instance_ids)

    # Check all defined CI systems are references in top-level collections.
    all_ci_ids = set(map(str.lower, ci_instance_ids))
    assert all_ci_ids.issubset(ALL_CI.member_ids | {UNKNOWN_CI.id})
    assert all_ci_ids.issubset(ALL_TRAITS.member_ids)


@unless_github_ci
def test_github_runner_detection():
    """Test GitHub runner OS.

    List of available GitHub runner images:
    https://github.com/actions/runner-images#available-images
    """
    assert is_github_ci()
    assert current_ci() is GITHUB_CI
    assert GITHUB_CI in current_traits()

    assert current_architecture() in current_traits()
    assert current_platform() in current_traits()
    assert current_shell() in current_traits()
    assert current_ci() in current_traits()

    assert is_any_trait()
    assert is_any_architecture()
    assert is_any_platform()
    assert is_any_shell()
    assert is_any_ci()

    assert not is_unknown_architecture()
    assert not is_unknown_platform()
    assert not is_unknown_shell()
    assert not is_unknown_ci()

    assert github_runner_os() is not None, (
        "The EXTRA_PLATFORMS_TEST_MATRIX environment variable is not set. "
        "This test must be run inside a GitHub Actions job using a matrix strategy."
    )

    # X86-64 runners.
    if github_runner_os() in {
        "ubuntu-slim",
        "ubuntu-24.04",
        "ubuntu-22.04",
        "macos-15-intel",
        "windows-2025",
        "windows-2022",
    } or (
        # XXX Python <= 3.10.x on Windows ARM runners reports x86_64.
        github_runner_os() == "windows-11-arm" and sys.version_info < (3, 11)
    ):
        assert is_x86_64()
        assert is_x86()
        assert current_architecture() is X86_64
        assert X86_64 in current_traits()
    # AArch64 runners.
    else:
        assert is_aarch64()
        assert not is_arm()
        assert is_any_arm()
        assert current_architecture() is AARCH64
        assert AARCH64 in current_traits()

    assert is_arch_64_bit()
    assert not is_arch_32_bit()
    assert is_little_endian()
    assert not is_big_endian()

    # Linux runners.
    if github_runner_os() in {
        "ubuntu-latest",
        "ubuntu-slim",
        "ubuntu-24.04",
        "ubuntu-24.04-arm",
        "ubuntu-22.04",
        "ubuntu-22.04-arm",
    }:
        assert is_ubuntu()
        assert is_linux()
        assert is_linux_like()
        assert is_unix()
        assert is_unix_not_macos()
        assert current_platform() is UBUNTU
        if github_runner_os() == "ubuntu-slim":
            # XXX ubuntu-slim is a special case: it's running in a WSL2 container on
            # Windows.
            assert is_wsl2()
            assert is_linux_layers()
            assert not is_bash()
            assert is_powershell()
            assert is_windows_shells()
            assert current_shell() is POWERSHELL
            assert current_traits() == {
                current_architecture(),
                UBUNTU,
                WSL2,
                POWERSHELL,
                GITHUB_CI,
            }
        else:
            assert not is_wsl2()
            assert not is_linux_layers()
            assert is_bash()
            assert is_bourne_shells()
            assert not is_powershell()
            assert not is_windows_shells()
            assert current_shell() is BASH
            assert current_traits() == {
                current_architecture(),
                UBUNTU,
                BASH,
                GITHUB_CI,
            }

    # MacOS runners.
    if github_runner_os() in {
        "macos-latest",
        "macos-latest-large",
        "macos-26",
        "macos-26-xlarge",
        "macos-15",
        "macos-15-intel",
        "macos-15-large",
        "macos-15-xlarge",
        "macos-14",
        "macos-14-large",
        "macos-14-xlarge",
    }:
        assert is_macos()
        assert is_bsd()
        assert is_unix()
        assert current_platform() is MACOS
        assert is_bash()
        assert is_bourne_shells()
        assert current_shell() is BASH
        assert current_traits() == {
            current_architecture(),
            MACOS,
            BASH,
            GITHUB_CI,
        }

    # Windows runners.
    if github_runner_os() in {
        "windows-latest",
        "windows-11-arm",
        "windows-2025",
        "windows-2022",
    }:
        assert is_windows()
        assert is_any_windows()
        assert current_platform() is WINDOWS
        assert is_powershell()
        assert is_windows_shells()
        assert current_shell() is POWERSHELL
        assert current_traits() == {
            current_architecture(),
            WINDOWS,
            POWERSHELL,
            GITHUB_CI,
        }


def test_ci_detection():
    # We always expect to detect something.
    assert is_any_trait()

    # We don't always expect to detect a CI.
    assert current_ci()
    if is_unknown_ci():
        assert current_ci() is UNKNOWN_CI
        assert current_ci() not in ALL_CI
        assert not is_any_ci()
    else:
        assert current_ci() is not UNKNOWN_CI
        assert current_ci() in ALL_CI
        assert is_any_ci()

    if is_github_ci():
        assert not is_azure_pipelines()
        assert not is_bamboo()
        assert not is_buildkite()
        assert not is_circle_ci()
        assert not is_cirrus_ci()
        assert not is_codebuild()
        assert is_github_ci()
        assert not is_gitlab_ci()
        assert not is_heroku_ci()
        assert not is_teamcity()
        assert not is_travis_ci()


def test_ci_logical_grouping():
    for group in ALL_CI_GROUPS:
        assert group.issubset(ALL_CI)

    assert ALL_CI.canonical


def test_no_missing_ci_in_groups():
    """Check all CI are attached to at least one non-overlapping group."""
    ALL_CI.fullyintersects(ALL_CI_GROUPS & NON_OVERLAPPING_GROUPS)
