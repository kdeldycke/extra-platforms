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

import functools
import json
import os

from extra_platforms import (
    ALL_PLATFORMS,
    GITHUB_CI,
    MACOS,
    UBUNTU,
    WINDOWS,
    current_os,
    current_platforms,
    is_aix,
    is_altlinux,
    is_amzn,
    is_android,
    is_arch,
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
    is_ibm_powerkvm,
    is_kvmibm,
    is_linuxmint,
    is_macos,
    is_mageia,
    is_mandriva,
    is_midnightbsd,
    is_netbsd,
    is_nobara,
    is_openbsd,
    is_opensuse,
    is_oracle,
    is_parallels,
    is_pidora,
    is_raspbian,
    is_rhel,
    is_rocky,
    is_scientific,
    is_slackware,
    is_sles,
    is_solaris,
    is_sunos,
    is_teamcity,
    is_travis_ci,
    is_tumbleweed,
    is_tuxedo,
    is_ubuntu,
    is_ultramarine,
    is_unknown_ci,
    is_unknown_linux,
    is_windows,
    is_wsl1,
    is_wsl2,
    is_xenserver,
)
from extra_platforms.platform_data import WSL2
from extra_platforms.pytest import unless_github_ci


def test_detection_functions():
    for platform in ALL_PLATFORMS.platforms:
        check_func_id = f"is_{platform.id}"
        assert check_func_id in globals()
        check_func = globals()[check_func_id]
        assert isinstance(check_func, functools._lru_cache_wrapper)
        assert isinstance(check_func(), bool)
        assert check_func() == platform.current


@functools.cached_property
def github_runner_os() -> str | None:
    """Returns the OS name as defined in the GitHub Actions matrix context.

    .. caution::
        This only works when running inside a GitHub Actions job that uses a ``matrix``
        strategy with an ``os`` variant. Which is the case for the ``extra-platforms``
        workflows.
    """
    matrix_context_str = os.environ.get("EXTRA_PLATFORMS_TEST_MATRIX", "{}")
    matrix_context = json.loads(matrix_context_str)
    return matrix_context.get("os")


@unless_github_ci
def test_github_runner_detection():
    """Test GitHub runner OS.

    List of available GitHub runner images:
    https://github.com/actions/runner-images#available-images
    """
    assert github_runner_os is not None, (
        "The EXTRA_PLATFORMS_TEST_MATRIX environment variable is not set. "
        "This test must be run inside a GitHub Actions job using a matrix strategy."
    )

    if github_runner_os in {
        "ubuntu-latest",
        "ubuntu-slim",
        "ubuntu-24.04",
        "ubuntu-24.04-arm",
        "ubuntu-22.04",
        "ubuntu-22.04-arm",
    }:
        assert is_ubuntu()
        assert current_os() is UBUNTU
        if github_runner_os == "ubuntu-slim":
            assert is_wsl2()
            assert current_platforms() == (GITHUB_CI, UBUNTU, WSL2)
        else:
            assert not is_wsl2()
            assert current_platforms() == (GITHUB_CI, UBUNTU)

    if github_runner_os in {
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
        assert current_os() is MACOS
        assert current_platforms() == (GITHUB_CI, MACOS)

    if github_runner_os in {
        "windows-latest",
        "windows-11-arm",
        "windows-2025",
        "windows-2022",
    }:
        assert is_windows()
        assert current_os() is WINDOWS
        assert current_platforms() == (GITHUB_CI, WINDOWS)


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
        # assert not is_ubuntu()
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
        # assert not is_macos()
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
        # assert not is_windows()
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
