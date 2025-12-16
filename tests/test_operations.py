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
    ALL_CI,
    ALL_GROUP_IDS,
    ALL_GROUPS,
    ALL_IDS,
    ALL_PLATFORMS,
    ALL_TRAIT_IDS,
    ALL_TRAITS,
    ALTLINUX,
    AMZN,
    ANDROID,
    ANY_WINDOWS,
    ARCH,
    AZURE_PIPELINES,
    BAMBOO,
    BSD,
    BSD_WITHOUT_MACOS,
    BUILDKITE,
    BUILDROOT,
    CACHYOS,
    CENTOS,
    CIRCLE_CI,
    CIRRUS_CI,
    CLOUDLINUX,
    CODEBUILD,
    CYGWIN,
    DEBIAN,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GITHUB_CI,
    GITLAB_CI,
    GUIX,
    HEROKU_CI,
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
    TEAMCITY,
    TRAVIS_CI,
    TUMBLEWEED,
    TUXEDO,
    UBUNTU,
    ULTRAMARINE,
    UNIX,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_CI,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    groups_from_ids,
    reduce,
    traits_from_ids,
)


def test_unique_ids():
    """Platform and group IDs must be unique."""
    all_platform_ids = [p.id for p in ALL_PLATFORMS]

    # Platforms are expected to be sorted by ID.
    assert sorted(all_platform_ids) == all_platform_ids
    assert len(set(all_platform_ids)) == len(all_platform_ids)

    assert len(all_platform_ids) == len(ALL_PLATFORMS)
    assert len(all_platform_ids) == len(ALL_PLATFORMS.member_ids)

    all_group_ids = {g.id for g in ALL_GROUPS}
    assert len(all_group_ids) == len(ALL_GROUPS)

    # Check there is no overlap between platform and group IDs.
    assert all_group_ids.isdisjoint(all_platform_ids)

    assert len(ALL_TRAIT_IDS) == len(ALL_TRAITS)
    assert ALL_TRAIT_IDS.issubset(ALL_IDS)
    assert ALL_TRAIT_IDS.isdisjoint(ALL_GROUP_IDS)

    assert len(ALL_GROUP_IDS) == len(ALL_GROUPS)
    assert ALL_GROUP_IDS.issubset(ALL_IDS)
    assert ALL_GROUP_IDS.isdisjoint(ALL_TRAIT_IDS)


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


@pytest.mark.parametrize("trait_id", randomize_case(ALL_TRAIT_IDS))
def test_traits_from_ids(trait_id):
    traits = traits_from_ids(trait_id)
    assert traits
    assert len(traits) == 1
    trait = traits[0]
    assert trait.id == trait_id.lower()
    assert trait in ALL_TRAITS.members


@pytest.mark.parametrize("group_id", randomize_case(ALL_GROUP_IDS))
def test_traits_from_ids_group_resolve(group_id):
    """traits_from_ids() can also resolve group IDs."""
    traits = traits_from_ids(group_id)
    assert traits
    assert len(traits) >= 1
    groups = groups_from_ids(group_id)
    assert len(groups) == 1
    group = groups[0]
    assert traits == tuple(group.members)


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
        ([UNIX, WINDOWS, ALL_CI], {ALL_PLATFORMS, ALL_CI}),
        ([UNIX, ANY_WINDOWS, ALL_CI], {ALL_PLATFORMS, ALL_CI}),
        ([BSD_WITHOUT_MACOS, UNIX], {UNIX}),
        ([BSD_WITHOUT_MACOS, MACOS], {BSD}),
        (
            [
                AIX,
                ALTLINUX,
                AMZN,
                ANDROID,
                ARCH,
                AZURE_PIPELINES,
                BAMBOO,
                BUILDKITE,
                BUILDROOT,
                CACHYOS,
                CENTOS,
                ALL_CI,
                CIRCLE_CI,
                CIRRUS_CI,
                CLOUDLINUX,
                CODEBUILD,
                CYGWIN,
                DEBIAN,
                EXHERBO,
                FEDORA,
                FREEBSD,
                GENTOO,
                GITHUB_CI,
                GITLAB_CI,
                GUIX,
                HEROKU_CI,
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
                TEAMCITY,
                TRAVIS_CI,
                TUMBLEWEED,
                TUXEDO,
                UBUNTU,
                ULTRAMARINE,
                UNKNOWN_CI,
                UNKNOWN_LINUX,
                WINDOWS,
                WSL1,
                WSL2,
                XENSERVER,
            ],
            {ALL_PLATFORMS, ALL_CI},
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
            members=tuple(UNIX_WITHOUT_MACOS - BSD_WITHOUT_MACOS - LINUX_LIKE),
        ),
        ANY_WINDOWS,
    )

    results = reduce(items, target_pool=target_pool)
    print(results)
    assert results == expected
    assert isinstance(results, frozenset)
