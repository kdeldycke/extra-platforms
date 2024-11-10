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

import pytest

from extra_platforms import (
    AIX,
    ALL_PLATFORMS,
    ALTLINUX,
    AMZN,
    ANDROID,
    ANY_WINDOWS,
    ARCH,
    BSD,
    BSD_WITHOUT_MACOS,
    BUILDROOT,
    CENTOS,
    CLOUDLINUX,
    CYGWIN,
    DEBIAN,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GUIX,
    HURD,
    IBM_POWERKVM,
    KVMIBM,
    LINUX,
    LINUX_LAYERS,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    OPENBSD,
    OPENSUSE,
    ORACLE,
    PARALLELS,
    PIDORA,
    RASPBIAN,
    RHEL,
    ROCKY,
    SCIENTIFIC,
    SLACKWARE,
    SLES,
    SOLARIS,
    SUNOS,
    TUXEDO,
    UBUNTU,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    Group,
    reduce,
)


def test_platform_deduplication():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    assert len(my_group) == 1
    assert len(my_group.platforms) == 1
    assert len(my_group.platform_ids) == 1

    assert my_group.platforms == (AIX,)
    assert my_group.platform_ids == frozenset({"aix"})


def test_platform_membership():
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA))
    assert AIX in my_group
    assert PIDORA in my_group
    assert RHEL not in my_group


def test_simple_union():
    new_group = ANY_WINDOWS.union(LINUX_LAYERS)

    assert ANY_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert new_group.issuperset(ANY_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)

    assert new_group.id == ANY_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.name == ANY_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.icon == ANY_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon

    assert set(new_group.platforms) != set(ANY_WINDOWS.platforms)
    assert set(new_group.platform_ids) != set(ANY_WINDOWS.platform_ids)
    assert set(new_group.platforms) != set(LINUX_LAYERS.platforms)
    assert set(new_group.platform_ids) != set(LINUX_LAYERS.platform_ids)

    assert set(new_group.platforms) == set(ANY_WINDOWS.platforms).union(
        LINUX_LAYERS.platforms
    )
    assert set(new_group.platform_ids) == set(ANY_WINDOWS.platform_ids).union(
        LINUX_LAYERS.platform_ids
    )


def test_multiple_union():
    new_group = ANY_WINDOWS.union(LINUX_LAYERS, UNIX_LAYERS)

    assert new_group.platform_ids == frozenset(("windows", "wsl1", "wsl2", "cygwin"))

    assert ANY_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert UNIX_LAYERS.issubset(new_group)

    assert new_group.issuperset(ANY_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)
    assert new_group.issuperset(UNIX_LAYERS)

    assert new_group.id == ANY_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.id != UNIX_LAYERS.id
    assert new_group.name == ANY_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.name != UNIX_LAYERS.name
    assert new_group.icon == ANY_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon
    assert new_group.icon != UNIX_LAYERS.icon

    assert set(new_group.platforms) != set(ANY_WINDOWS.platforms)
    assert set(new_group.platform_ids) != set(ANY_WINDOWS.platform_ids)
    assert set(new_group.platforms) != set(LINUX_LAYERS.platforms)
    assert set(new_group.platform_ids) != set(LINUX_LAYERS.platform_ids)
    assert set(new_group.platforms) != set(UNIX_LAYERS.platforms)
    assert set(new_group.platform_ids) != set(UNIX_LAYERS.platform_ids)

    assert set(new_group.platforms) == set(ANY_WINDOWS.platforms).union(
        LINUX_LAYERS.platforms
    ).union(UNIX_LAYERS.platforms)
    assert set(new_group.platform_ids) == set(ANY_WINDOWS.platform_ids).union(
        LINUX_LAYERS.platform_ids
    ).union(UNIX_LAYERS.platform_ids)


def test_single_intersection():
    new_group = ALL_PLATFORMS.intersection(ANY_WINDOWS)

    assert new_group.platform_ids == frozenset(("windows",))

    assert ANY_WINDOWS.issubset(new_group)
    assert not ALL_PLATFORMS.issubset(new_group)
    assert new_group.issuperset(ANY_WINDOWS)
    assert not new_group.issuperset(ALL_PLATFORMS)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != ANY_WINDOWS.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != ANY_WINDOWS.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != ANY_WINDOWS.icon

    assert set(new_group.platforms) != set(ALL_PLATFORMS.platforms)
    assert set(new_group.platform_ids) != set(ALL_PLATFORMS.platform_ids)

    assert set(new_group.platforms) == set(ANY_WINDOWS.platforms)
    assert set(new_group.platform_ids) == set(ANY_WINDOWS.platform_ids)


def test_multiple_intersection():
    new_group = ALL_PLATFORMS.intersection(UNIX_WITHOUT_MACOS, BSD_WITHOUT_MACOS)

    assert new_group.platform_ids == frozenset((
        "freebsd",
        "midnightbsd",
        "netbsd",
        "openbsd",
        "sunos",
    ))

    assert new_group.issubset(ALL_PLATFORMS)
    assert new_group.issubset(UNIX_WITHOUT_MACOS)
    assert new_group.issubset(BSD_WITHOUT_MACOS)
    assert ALL_PLATFORMS.issuperset(new_group)
    assert UNIX_WITHOUT_MACOS.issuperset(new_group)
    assert BSD_WITHOUT_MACOS.issuperset(new_group)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != UNIX_WITHOUT_MACOS.id
    assert new_group.id != BSD_WITHOUT_MACOS.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != UNIX_WITHOUT_MACOS.name
    assert new_group.name != BSD_WITHOUT_MACOS.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != UNIX_WITHOUT_MACOS.icon
    assert new_group.icon != BSD_WITHOUT_MACOS.icon

    assert set(new_group.platforms) != set(ALL_PLATFORMS.platforms)
    assert set(new_group.platform_ids) != set(ALL_PLATFORMS.platform_ids)
    assert set(new_group.platforms) != set(UNIX_WITHOUT_MACOS.platforms)
    assert set(new_group.platform_ids) != set(UNIX_WITHOUT_MACOS.platform_ids)

    assert set(new_group.platforms) == set(BSD_WITHOUT_MACOS.platforms)
    assert set(new_group.platform_ids) == set(BSD_WITHOUT_MACOS.platform_ids)


def test_single_difference():
    new_group = BSD.difference(BSD_WITHOUT_MACOS)

    assert new_group.platform_ids == frozenset(("macos",))

    assert not BSD.issubset(new_group)
    assert BSD.issuperset(new_group)
    assert not BSD_WITHOUT_MACOS.issubset(new_group)
    assert not BSD_WITHOUT_MACOS.issuperset(new_group)

    assert not new_group.issuperset(BSD)
    assert not new_group.issuperset(BSD_WITHOUT_MACOS)
    assert new_group.issubset(BSD)
    assert not new_group.issubset(BSD_WITHOUT_MACOS)

    assert new_group.id == BSD.id
    assert new_group.id != BSD_WITHOUT_MACOS.id
    assert new_group.name == BSD.name
    assert new_group.name != BSD_WITHOUT_MACOS.name
    assert new_group.icon == BSD.icon
    assert new_group.icon != BSD_WITHOUT_MACOS.icon

    assert set(new_group.platforms) != set(BSD.platforms)
    assert set(new_group.platform_ids) != set(BSD.platform_ids)
    assert set(new_group.platforms) != set(BSD_WITHOUT_MACOS.platforms)
    assert set(new_group.platform_ids) != set(BSD_WITHOUT_MACOS.platform_ids)

    assert set(new_group.platforms) == set(BSD.platforms).difference(
        BSD_WITHOUT_MACOS.platforms
    )
    assert set(new_group.platform_ids) == set(BSD.platform_ids).difference(
        BSD_WITHOUT_MACOS.platform_ids
    )


def test_multiple_difference():
    new_group = ALL_PLATFORMS.difference(LINUX, UNIX)

    assert new_group.platform_ids == frozenset(("windows",))

    assert not ALL_PLATFORMS.issubset(new_group)
    assert ALL_PLATFORMS.issuperset(new_group)
    assert not LINUX.issubset(new_group)
    assert not LINUX.issuperset(new_group)
    assert not UNIX.issubset(new_group)
    assert not UNIX.issuperset(new_group)

    assert not new_group.issuperset(ALL_PLATFORMS)
    assert not new_group.issuperset(LINUX)
    assert not new_group.issuperset(UNIX)
    assert new_group.issubset(ALL_PLATFORMS)
    assert not new_group.issubset(LINUX)
    assert not new_group.issubset(UNIX)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != LINUX.id
    assert new_group.id != UNIX.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != LINUX.name
    assert new_group.name != UNIX.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != LINUX.icon
    assert new_group.icon != UNIX.icon

    assert set(new_group.platforms) != set(ALL_PLATFORMS.platforms)
    assert set(new_group.platform_ids) != set(ALL_PLATFORMS.platform_ids)
    assert set(new_group.platforms) != set(LINUX.platforms)
    assert set(new_group.platform_ids) != set(LINUX.platform_ids)
    assert set(new_group.platforms) != set(UNIX.platforms)
    assert set(new_group.platform_ids) != set(UNIX.platform_ids)

    assert set(new_group.platforms) == set(ALL_PLATFORMS.platforms).difference(
        LINUX.platforms
    ).difference(UNIX.platforms)
    assert set(new_group.platform_ids) == set(ALL_PLATFORMS.platform_ids).difference(
        LINUX.platform_ids
    ).difference(UNIX.platform_ids)


def test_symmetric_difference():
    win_and_bsd = ANY_WINDOWS.union(BSD_WITHOUT_MACOS)
    new_group = win_and_bsd.symmetric_difference(BSD)

    assert new_group.platform_ids == frozenset((("macos", "windows")))

    assert not win_and_bsd.issubset(new_group)
    assert not win_and_bsd.issuperset(new_group)
    assert not BSD.issubset(new_group)
    assert not BSD.issuperset(new_group)

    assert not new_group.issuperset(win_and_bsd)
    assert not new_group.issuperset(BSD)
    assert not new_group.issubset(win_and_bsd)
    assert not new_group.issubset(BSD)

    assert new_group.id == win_and_bsd.id
    assert new_group.id != BSD.id
    assert new_group.name == win_and_bsd.name
    assert new_group.name != BSD.name
    assert new_group.icon == win_and_bsd.icon
    assert new_group.icon != BSD.icon

    assert set(new_group.platforms) != set(BSD.platforms)
    assert set(new_group.platform_ids) != set(BSD.platform_ids)
    assert set(new_group.platforms) != set(win_and_bsd.platforms)
    assert set(new_group.platform_ids) != set(win_and_bsd.platform_ids)

    assert set(new_group.platforms) == set(win_and_bsd.platforms).symmetric_difference(
        BSD.platforms
    )
    assert set(new_group.platform_ids) == set(
        win_and_bsd.platform_ids
    ).symmetric_difference(BSD.platform_ids)


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], set()),
        ((), set()),
        (set(), set()),
        ([AIX], {AIX}),
        ([AIX, AIX], {AIX}),
        ([UNIX], {UNIX}),
        ([UNIX, UNIX], {UNIX}),
        ([UNIX, AIX], {UNIX}),
        ([WINDOWS], {ANY_WINDOWS}),
        ([ALL_PLATFORMS, WINDOWS], {ALL_PLATFORMS}),
        ([UNIX, WINDOWS], {ALL_PLATFORMS}),
        ([UNIX, ANY_WINDOWS], {ALL_PLATFORMS}),
        ([BSD_WITHOUT_MACOS, UNIX], {UNIX}),
        ([BSD_WITHOUT_MACOS, MACOS], {BSD}),
        (
            [
                AIX,
                ALTLINUX,
                AMZN,
                ANDROID,
                ARCH,
                BUILDROOT,
                CENTOS,
                CLOUDLINUX,
                CYGWIN,
                DEBIAN,
                EXHERBO,
                FEDORA,
                FREEBSD,
                GENTOO,
                GUIX,
                HURD,
                IBM_POWERKVM,
                KVMIBM,
                LINUXMINT,
                MACOS,
                MAGEIA,
                MANDRIVA,
                MIDNIGHTBSD,
                NETBSD,
                OPENBSD,
                OPENSUSE,
                ORACLE,
                PARALLELS,
                PIDORA,
                RASPBIAN,
                RHEL,
                ROCKY,
                SCIENTIFIC,
                SLACKWARE,
                SLES,
                SOLARIS,
                SUNOS,
                TUXEDO,
                UBUNTU,
                UNKNOWN_LINUX,
                WINDOWS,
                WSL1,
                WSL2,
                XENSERVER,
            ],
            {ALL_PLATFORMS},
        ),
    ],
)
def test_reduction(items, expected):
    assert reduce(items) == expected
