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
from pathlib import Path

from extra_platforms import (  # type: ignore[attr-defined]
    AARCH64,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_TRAITS,
    GITHUB_CI,
    MACOS,
    NON_OVERLAPPING_GROUPS,
    UBUNTU,
    UNKNOWN_CI,
    WINDOWS,
    WSL2,
    X86_64,
    current_architecture,
    current_ci,
    current_platform,
    current_traits,
    is_aarch64,
    is_any_ci,
    is_any_trait,
    is_arch_64_bit,
    is_azure_pipelines,
    is_bamboo,
    is_buildkite,
    is_circle_ci,
    is_cirrus_ci,
    is_codebuild,
    is_github_ci,
    is_gitlab_ci,
    is_heroku_ci,
    is_macos,
    is_teamcity,
    is_travis_ci,
    is_ubuntu,
    is_unknown_architecture,
    is_unknown_ci,
    is_unknown_platform,
    is_windows,
    is_wsl2,
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
    assert current_ci() is GITHUB_CI
    assert is_any_ci()
    assert is_github_ci()

    assert GITHUB_CI in current_traits()
    assert current_architecture() in current_traits()
    assert current_platform() in current_traits()
    assert current_ci() in current_traits()

    assert github_runner_os() is not None, (
        "The EXTRA_PLATFORMS_TEST_MATRIX environment variable is not set. "
        "This test must be run inside a GitHub Actions job using a matrix strategy."
    )

    assert not is_unknown_architecture()
    assert not is_unknown_platform()
    assert not is_unknown_ci()

    # X86-64 runners.
    if github_runner_os() in {
        "ubuntu-slim",
        "ubuntu-24.04",
        "ubuntu-22.04",
        "macos-15-intel",
        "windows-2025",
        "windows-2022",
    }:
        assert current_architecture() is X86_64
        assert X86_64 in current_traits()
        assert is_x86_64()
    # AArch64 runners.
    else:
        assert current_architecture() is AARCH64
        assert AARCH64 in current_traits()
        assert is_aarch64()

    assert is_arch_64_bit()

    # Linux runners.
    if github_runner_os() in {
        "ubuntu-latest",
        "ubuntu-slim",
        "ubuntu-24.04",
        "ubuntu-24.04-arm",
        "ubuntu-22.04",
        "ubuntu-22.04-arm",
    }:
        assert current_platform() is UBUNTU
        assert is_ubuntu()
        if github_runner_os() == "ubuntu-slim":
            assert current_traits() == {GITHUB_CI, UBUNTU, WSL2, current_architecture()}
            assert is_wsl2()
        else:
            assert current_traits() == {GITHUB_CI, UBUNTU, current_architecture()}
            assert not is_wsl2()

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
        assert current_platform() is MACOS
        assert current_traits() == {GITHUB_CI, MACOS, current_architecture()}
        assert is_macos()

    # Windows runners.
    if github_runner_os() in {
        "windows-latest",
        "windows-11-arm",
        "windows-2025",
        "windows-2022",
    }:
        assert current_platform() is WINDOWS
        assert current_traits() == {GITHUB_CI, WINDOWS, current_architecture()}
        assert is_windows()


def test_ci_detection():
    # We always expect to detect something.
    assert is_any_trait()

    # We don't always expect to detect a CI.
    current_ci_result = current_ci()
    assert current_ci_result
    if is_unknown_ci():
        assert current_ci_result is UNKNOWN_CI
        assert current_ci_result not in ALL_CI
        assert not is_any_ci()
    else:
        assert current_ci_result is not UNKNOWN_CI
        assert current_ci_result in ALL_CI
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


def test_no_missing_ci_in_groups():
    """Check all CI are attached to at least one non-overlapping group."""
    ALL_CI.fullyintersects(ALL_CI_GROUPS & NON_OVERLAPPING_GROUPS)
