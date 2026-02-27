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
"""Test all platform definitions and platform-specific groups."""

from __future__ import annotations

from extra_platforms import (  # type: ignore[attr-defined]
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    OTHER_POSIX,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_PLATFORM,
    current_platform,
    is_aix,
    is_altlinux,
    is_amzn,
    is_android,
    is_any_platform,
    is_any_trait,
    is_arch,
    is_buildroot,
    is_cachyos,
    is_centos,
    is_cloudlinux,
    is_cygwin,
    is_debian,
    is_exherbo,
    is_fedora,
    is_freebsd,
    is_gentoo,
    is_guix,
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
    is_tumbleweed,
    is_tuxedo,
    is_ubuntu,
    is_ultramarine,
    is_unknown_platform,
    is_windows,
    is_wsl1,
    is_wsl2,
    is_xenserver,
)

from .test_ci_data import github_runner_os


def test_platform_detection():
    # We always expect to detect a platform.
    assert is_any_trait()
    assert is_any_platform()
    assert not is_unknown_platform()
    assert current_platform() is not UNKNOWN_PLATFORM

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
        assert is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()


def test_platform_logical_grouping():
    assert not ALL_PLATFORMS.canonical

    # All platforms are divided into Windows and Unix at the highest level.
    assert ALL_PLATFORMS.fullyintersects(ALL_WINDOWS | UNIX)
    assert ALL_WINDOWS.canonical
    assert not UNIX.canonical

    # Every group is a subset of UNIX except Windows and ALL_PLATFORMS.
    for group in ALL_PLATFORM_GROUPS:
        if group is ALL_WINDOWS or group is ALL_PLATFORMS:
            assert not group.issubset(UNIX)
            assert not UNIX.issuperset(group)
        else:
            assert group.issubset(UNIX)
            assert UNIX.issuperset(group)

    # All UNIX platforms are divided into BSD, Linux, and Unix families.
    assert UNIX.fullyintersects(
        BSD | LINUX | LINUX_LAYERS | SYSTEM_V | UNIX_LAYERS | OTHER_POSIX
    )
    assert BSD.canonical
    assert LINUX.canonical
    assert LINUX_LAYERS.canonical
    assert SYSTEM_V.canonical
    assert UNIX_LAYERS.canonical
    assert OTHER_POSIX.canonical

    # LINUX_LIKE is the union of LINUX and LINUX_LAYERS.
    assert LINUX.issubset(LINUX_LIKE)
    assert LINUX_LAYERS.issubset(LINUX_LIKE)
    assert LINUX_LIKE.issuperset(LINUX)
    assert LINUX_LIKE.issuperset(LINUX_LAYERS)
    assert not LINUX_LIKE.canonical

    # Relationships specific to UNIX_WITHOUT_MACOS.
    assert UNIX_WITHOUT_MACOS.issubset(UNIX)
    assert UNIX.issuperset(UNIX_WITHOUT_MACOS)
    assert not UNIX_WITHOUT_MACOS.canonical

    # Relationships specific to BSD_WITHOUT_MACOS.
    assert BSD_WITHOUT_MACOS.issubset(UNIX)
    assert BSD_WITHOUT_MACOS.issubset(BSD)
    assert UNIX.issuperset(BSD_WITHOUT_MACOS)
    assert BSD.issuperset(BSD_WITHOUT_MACOS)
    assert not BSD_WITHOUT_MACOS.canonical
