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

import os

import pytest

from extra_platforms import (
    AARCH64,
    BASH,
    DASH,
    GITHUB_CI,
    MACOS,
    POWERSHELL,
    UBUNTU,
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
    is_bash,
    is_big_endian,
    is_bourne_shells,
    is_bsd,
    is_dash,
    is_github_ci,
    is_linux,
    is_linux_layers,
    is_linux_like,
    is_little_endian,
    is_macos,
    is_powershell,
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

from .conftest import github_runner_os


@pytest.mark.skipif(
    "EXTRA_PLATFORMS_TEST_MATRIX" not in os.environ,
    reason="needs EXTRA_PLATFORMS_TEST_MATRIX, set only by the matrix CI job",
)
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

    # GitHub sets RUNNER_ARCH to the runner's own architecture: X86, X64, ARM or
    # ARM64. The package never reads it, so it is an independent reference.
    runner_arch = os.environ.get("RUNNER_ARCH")
    # X86-64 runners.
    if runner_arch == "X64":
        assert is_x86_64()
        assert is_x86()
        assert current_architecture() is X86_64
        assert X86_64 in current_traits()
    # AArch64 runners.
    else:
        assert runner_arch == "ARM64"
        assert is_aarch64()
        assert not is_arm()
        assert is_any_arm()
        assert current_architecture() is AARCH64
        assert AARCH64 in current_traits()

    assert is_arch_64_bit()
    assert not is_arch_32_bit()
    assert is_little_endian()
    assert not is_big_endian()

    runner = github_runner_os()
    assert runner, "the matrix context names no runner image"

    # Linux runners.
    if runner.startswith("ubuntu-"):
        assert is_ubuntu()
        assert is_linux()
        assert is_linux_like()
        assert is_unix()
        assert is_unix_not_macos()
        assert current_platform() is UBUNTU
        if runner == "ubuntu-slim":
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
            expected_traits = {
                current_architecture(),
                UBUNTU,
                BASH,
                POWERSHELL,
                GITHUB_CI,
            }
            # XXX On some Ubuntu runners SHELL=/bin/sh resolves to /bin/dash,
            # so is_dash() is True independently of current_shell().
            if is_dash():
                expected_traits.add(DASH)
            assert current_traits() == expected_traits

    # macOS runners.
    elif runner.startswith("macos-"):
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
    elif runner.startswith("windows-"):
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

    # A runner of another family would leave the platform half unchecked.
    else:
        pytest.fail(f"Unrecognized GitHub runner image: {runner}")
