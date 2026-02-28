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
"""Test all CI definitions, detection and CI-specific groups."""

from __future__ import annotations

import functools
import json
import os
import sys

from extra_platforms import (  # type: ignore[attr-defined]
    AARCH64,
    ALL_CI,
    BASH,
    GITHUB_CI,
    MACOS,
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
            # XXX ubuntu-slim is a stripped-down WSL2 container.
            assert is_wsl2()
            assert is_linux_layers()
            assert is_bash()
            assert is_bourne_shells()
            assert not is_powershell()
            assert not is_windows_shells()
            assert current_shell() is BASH
            assert current_traits() == {
                current_architecture(),
                UBUNTU,
                WSL2,
                BASH,
                GITHUB_CI,
            }
        else:
            assert not is_wsl2()
            assert not is_linux_layers()
            assert is_bash()
            assert is_bourne_shells()
            # XXX PSModulePath leaks from Azure infrastructure into Ubuntu runners.
            assert is_powershell()
            assert is_windows_shells()
            assert current_shell() is BASH
            assert current_traits() == {
                current_architecture(),
                UBUNTU,
                BASH,
                POWERSHELL,
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
    assert ALL_CI.canonical
