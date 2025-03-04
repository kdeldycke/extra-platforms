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

from random import choice
from typing import Iterable

import pytest

from extra_platforms import (
    AIX,
    ALL_GROUP_IDS,
    ALL_GROUPS,
    ALL_IDS,
    ALL_PLATFORM_IDS,
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
    LINUX_LIKE,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    NOBARA,
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
    TUMBLEWEED,
    TUXEDO,
    UBUNTU,
    UNIX,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    groups_from_ids,
    platforms_from_ids,
    reduce,
)


def test_unique_ids():
    """Platform and group IDs must be unique."""
    all_platform_ids = [p.id for p in ALL_PLATFORMS]

    # Platforms are expected to be sorted by ID.
    assert sorted(all_platform_ids) == all_platform_ids
    assert len(set(all_platform_ids)) == len(all_platform_ids)

    assert len(all_platform_ids) == len(ALL_PLATFORMS)
    assert len(all_platform_ids) == len(ALL_PLATFORMS.platform_ids)

    all_group_ids = {g.id for g in ALL_GROUPS}
    assert len(all_group_ids) == len(ALL_GROUPS)

    # Check there is no overlap between platform and group IDs.
    assert all_group_ids.isdisjoint(all_platform_ids)

    assert len(ALL_PLATFORM_IDS) == len(ALL_PLATFORMS)
    assert ALL_PLATFORM_IDS.issubset(ALL_IDS)
    assert ALL_PLATFORM_IDS.isdisjoint(ALL_GROUP_IDS)

    assert len(ALL_GROUP_IDS) == len(ALL_GROUPS)
    assert ALL_GROUP_IDS.issubset(ALL_IDS)
    assert ALL_GROUP_IDS.isdisjoint(ALL_PLATFORM_IDS)


def randomize_case(strings: Iterable[str]) -> set[str]:
    test_strings = set()
    for string in strings:
        test_strings.add(string)
        for str_func in (
            str.upper,
            str.lower,
            str.title,
            str.capitalize,
            str.casefold,
            str.swapcase,
        ):
            test_strings.add(str_func(string))
        test_strings.add(
            "".join(choice((str.upper, str.lower))(char) for char in string)
        )
    return test_strings


@pytest.mark.parametrize("platform_id", randomize_case(ALL_PLATFORM_IDS))
def test_platforms_from_ids(platform_id):
    platforms = platforms_from_ids(platform_id)
    assert platforms
    assert len(platforms) == 1
    platform = platforms[0]
    assert platform.id == platform_id.lower()
    assert platform in ALL_PLATFORMS.platforms


@pytest.mark.parametrize("group_id", randomize_case(ALL_GROUP_IDS))
def test_platforms_from_ids_group_resolve(group_id):
    """platforms_from_ids() can also resolve group IDs."""
    platforms = platforms_from_ids(group_id)
    assert platforms
    assert len(platforms) >= 1
    groups = groups_from_ids(group_id)
    assert len(groups) == 1
    group = groups[0]
    assert platforms == tuple(group.platforms)


@pytest.mark.parametrize("group_id", randomize_case(ALL_GROUP_IDS))
def test_groups_from_ids(group_id):
    groups = groups_from_ids(group_id)
    assert len(groups) == 1
    group = groups[0]
    assert group.id == group_id.lower()
    assert group in ALL_GROUPS


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], frozenset()),
        ((), frozenset()),
        (set(), frozenset()),
        (frozenset(), frozenset()),
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
                NOBARA,
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
                TUMBLEWEED,
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
    results = reduce(items)
    assert results == expected
    assert isinstance(results, frozenset)


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], frozenset()),
        ((), frozenset()),
        (set(), frozenset()),
        (frozenset(), frozenset()),
        ([AIX], {AIX}),
        ([AIX, AIX], {AIX}),
        ([WINDOWS], {ANY_WINDOWS}),
        (
            [BSD_WITHOUT_MACOS, MACOS],
            {FREEBSD, MACOS, MIDNIGHTBSD, NETBSD, OPENBSD, SUNOS},
        ),
        ([MACOS, WINDOWS, WSL1], {MACOS, ANY_WINDOWS, WSL1}),
    ],
)
def test_reduce_custom_targets(items, expected):
    target_pool = (
        MACOS,
        UNIX_WITHOUT_MACOS.copy(
            id="unix",
            name="Unix",
            platforms=tuple(UNIX_WITHOUT_MACOS - BSD_WITHOUT_MACOS - LINUX_LIKE),
        ),
        ANY_WINDOWS,
    )

    results = reduce(items, target_pool=target_pool)
    print(results)
    assert results == expected
    assert isinstance(results, frozenset)
