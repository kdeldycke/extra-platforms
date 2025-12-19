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

from __future__ import annotations

import ast
import functools
import inspect
import json
import os
from pathlib import Path

from extra_platforms import (  # type: ignore[attr-defined]
    AARCH64,
    ALL_TRAITS,
    GITHUB_CI,
    MACOS,
    UBUNTU,
    UNKNOWN_ARCHITECTURE,
    WINDOWS,
    WSL2,
    X86_64,
    current_architecture,
    current_ci,
    current_platform,
    current_traits,
    is_aarch64,
    is_aix,
    is_all_ci,
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
from extra_platforms import detection as detection_module
from extra_platforms.pytest import unless_github_ci


def test_detection_functions():
    for platform in ALL_TRAITS:
        check_func_id = f"is_{platform.id}"
        assert check_func_id in globals()
        check_func = globals()[check_func_id]
        assert isinstance(check_func, functools._lru_cache_wrapper)
        assert isinstance(check_func(), bool)
        assert check_func() == platform.current


def test_detection_heuristics_sorting():
    """Detection heuristics must be sorted within each section."""
    detection_path = Path(inspect.getfile(detection_module))
    tree = ast.parse(detection_path.read_bytes())
    source_lines = detection_path.read_text().splitlines()

    # Find section boundaries by looking for comment markers.
    arch_section_start = None
    platform_section_start = None
    ci_section_start = None

    for i, line in enumerate(source_lines, start=1):
        if "Architecture detection heuristics" in line:
            arch_section_start = i
        elif "Platform detection heuristics" in line:
            platform_section_start = i
        elif "CI/CD detection heuristics" in line:
            ci_section_start = i

    assert arch_section_start is not None, "Architecture section not found"
    assert platform_section_start is not None, "Platform section not found"
    assert ci_section_start is not None, "CI/CD section not found"

    assert arch_section_start < platform_section_start
    assert platform_section_start < ci_section_start

    # Collect heuristic functions by section.
    all_heuristic_ids = []
    arch_heuristics = []
    platform_heuristics = []
    ci_heuristics = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_"):
            func_id = node.name
            assert func_id.islower()
            all_heuristic_ids.append(func_id)

            line_no = node.lineno
            if line_no >= arch_section_start and line_no < platform_section_start:
                arch_heuristics.append(func_id)
            elif line_no >= platform_section_start and line_no < ci_section_start:
                platform_heuristics.append(func_id)
            elif line_no >= ci_section_start:
                ci_heuristics.append(func_id)

    # Check there is no extra "is_" function.
    assert {f"is_{p.id}" for p in ALL_TRAITS} == set(all_heuristic_ids)

    # We only allow one generic "is_unknown*()" detection heuristics per category.
    for heuristics in [arch_heuristics, platform_heuristics, ci_heuristics]:
        non_generic_func_ids = [
            func_id for func_id in heuristics if func_id.startswith("is_unknown")
        ]

        assert len(non_generic_func_ids) <= 1, (
            f"More than 1 is_unknown*() detection heuristics defined in {heuristics!r}"
        )

        if len(non_generic_func_ids):
            assert non_generic_func_ids[-1].startswith("is_unknown")

        # Verify each category is sorted alphabetically within itself.
        assert non_generic_func_ids == sorted(non_generic_func_ids), (
            f"Heuristics are not sorted: {non_generic_func_ids!r}"
        )


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
    assert current_ci() is GITHUB_CI
    assert is_all_ci()
    assert is_github_ci()

    assert GITHUB_CI in current_traits()
    assert current_architecture() in current_traits()
    assert current_platform() in current_traits()
    assert current_platform() in current_traits()
    assert current_ci() in current_traits()

    assert github_runner_os() is not None, (
        "The EXTRA_PLATFORMS_TEST_MATRIX environment variable is not set. "
        "This test must be run inside a GitHub Actions job using a matrix strategy."
    )

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
    elif github_runner_os() == "windows-11-arm":
        assert current_architecture() is UNKNOWN_ARCHITECTURE
        assert UNKNOWN_ARCHITECTURE in current_traits()
        assert is_unknown_architecture()
    else:
        assert current_architecture() is AARCH64
        assert AARCH64 in current_traits()
        assert is_aarch64()

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

    if github_runner_os() in {
        "windows-latest",
        "windows-11-arm",
        "windows-2025",
        "windows-2022",
    }:
        assert current_platform() is WINDOWS
        assert current_traits() == {GITHUB_CI, WINDOWS, current_architecture()}
        assert is_windows()


def test_mutual_exclusion():
    """Only directly tests OSes on which the test suite is running via GitHub
    actions."""

    if is_ubuntu():
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_cachyos()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        assert not is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_nobara()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tumbleweed()
        assert not is_tuxedo()
        assert is_ubuntu()
        assert not is_ultramarine()
        assert not is_unknown_linux()
        assert not is_windows()
        assert not is_wsl1()
        # ubuntu-slim is a GitHub actions image running on WSL2.
        if github_runner_os() == "ubuntu-slim":
            assert is_wsl2()
        else:
            assert not is_wsl2()
        assert not is_xenserver()

    if is_macos():
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_cachyos()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        assert is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_nobara()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tumbleweed()
        assert not is_tuxedo()
        assert not is_ubuntu()
        assert not is_ultramarine()
        assert not is_unknown_linux()
        assert not is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()

    if is_windows():
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_cachyos()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        assert not is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_nobara()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tumbleweed()
        assert not is_tuxedo()
        assert not is_ubuntu()
        assert not is_ultramarine()
        assert not is_unknown_linux()
        assert is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()

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
        assert not is_unknown_ci()

    if is_x86_64():
        assert not is_i386()
        assert not is_i586()
        assert not is_i686()
        assert is_x86_64()
        assert not is_arm()
        assert not is_armv6l()
        assert not is_armv7l()
        assert not is_armv8l()
        assert not is_aarch64()
        assert not is_mips()
        assert not is_mipsel()
        assert not is_mips64()
        assert not is_mips64el()
        assert not is_ppc()
        assert not is_ppc64()
        assert not is_ppc64le()
        assert not is_riscv32()
        assert not is_riscv64()
        assert not is_sparc()
        assert not is_sparc64()
        assert not is_s390x()
        assert not is_loongarch64()
        assert not is_unknown_architecture()
        assert not is_wasm32()
        assert not is_wasm64()

    if is_aarch64():
        assert not is_i386()
        assert not is_i586()
        assert not is_i686()
        assert not is_x86_64()
        assert not is_arm()
        assert not is_armv6l()
        assert not is_armv7l()
        assert not is_armv8l()
        assert is_aarch64()
        assert not is_mips()
        assert not is_mipsel()
        assert not is_mips64()
        assert not is_mips64el()
        assert not is_ppc()
        assert not is_ppc64()
        assert not is_ppc64le()
        assert not is_riscv32()
        assert not is_riscv64()
        assert not is_sparc()
        assert not is_sparc64()
        assert not is_s390x()
        assert not is_loongarch64()
        assert not is_unknown_architecture()
        assert not is_wasm32()
        assert not is_wasm64()
