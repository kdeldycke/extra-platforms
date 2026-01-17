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
    ALL_WINDOWS,
    ALTLINUX,
    AMZN,
    ANDROID,
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
    DRAGONFLY_BSD,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GITHUB_CI,
    GITLAB_CI,
    GUIX,
    HAIKU,
    HEROKU_CI,
    HURD,
    IBM_POWERKVM,
    ILLUMOS,
    KVMIBM,
    LINUX,
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
    UNKNOWN,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    groups_from_ids,
    reduce,
    traits_from_ids,
)


def test_unique_ids():
    """Traits and group IDs must be unique."""
    all_trait_ids = [p.id for p in ALL_TRAITS]

    # Traits are expected to be sorted by ID.
    assert sorted(all_trait_ids) == all_trait_ids
    assert len(set(all_trait_ids)) == len(all_trait_ids)
    assert len(all_trait_ids) == len(ALL_TRAITS)
    assert len(all_trait_ids) == len(ALL_TRAITS.member_ids)

    all_group_ids = {g.id for g in ALL_GROUPS}
    assert len(all_group_ids) == len(ALL_GROUPS)

    # Check there is no overlap between trait and group IDs.
    assert all_group_ids.isdisjoint(all_trait_ids)

    assert len(ALL_TRAIT_IDS) == len(ALL_TRAITS) - len(UNKNOWN)
    assert ALL_TRAIT_IDS.issubset(ALL_IDS)
    assert ALL_TRAIT_IDS.isdisjoint(ALL_GROUP_IDS)

    assert len(ALL_GROUP_IDS) == len(ALL_GROUPS) - 1  # Exclude UNKNOWN group.
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
    assert trait in ALL_TRAITS


@pytest.mark.parametrize("group_id", randomize_case(ALL_GROUP_IDS))
def test_traits_from_ids_group_resolve(group_id):
    """traits_from_ids() can also resolve group IDs."""
    traits = traits_from_ids(group_id)
    assert traits
    assert len(traits) >= 1
    groups = groups_from_ids(group_id)
    assert len(groups) == 1
    group = groups[0]
    assert traits == tuple(group)


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
        ([WINDOWS], {ALL_WINDOWS}),
        ([ALL_PLATFORMS, WINDOWS], {ALL_PLATFORMS}),
        ([UNIX, WINDOWS, ALL_CI], {ALL_PLATFORMS, ALL_CI}),
        ([UNIX, ALL_WINDOWS, ALL_CI], {ALL_PLATFORMS, ALL_CI}),
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
                DRAGONFLY_BSD,
                EXHERBO,
                FEDORA,
                FREEBSD,
                GENTOO,
                GITHUB_CI,
                GITLAB_CI,
                GUIX,
                HAIKU,
                HEROKU_CI,
                HURD,
                IBM_POWERKVM,
                ILLUMOS,
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
        ([WINDOWS], {ALL_WINDOWS}),
        (
            [BSD_WITHOUT_MACOS, MACOS],
            {DRAGONFLY_BSD, FREEBSD, MACOS, MIDNIGHTBSD, NETBSD, OPENBSD, SUNOS},
        ),
        ([MACOS, WINDOWS, WSL1], {MACOS, ALL_WINDOWS, WSL1}),
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
        ALL_WINDOWS,
    )

    results = reduce(items, target_pool=target_pool)
    print(results)
    assert results == expected
    assert isinstance(results, frozenset)


def test_traits_from_ids_with_invalid_id():
    """Test that traits_from_ids raises ValueError for invalid IDs."""
    with pytest.raises(ValueError, match="Unrecognized group or trait IDs"):
        traits_from_ids("invalid_id_that_does_not_exist")


def test_groups_from_ids_with_invalid_id():
    """Test that groups_from_ids raises ValueError for invalid IDs."""
    with pytest.raises(ValueError, match="Unrecognized group IDs"):
        groups_from_ids("invalid_group_id_that_does_not_exist")


def test_traits_from_ids_with_empty_list():
    """Test that traits_from_ids works with empty input."""
    result = traits_from_ids()
    assert result == tuple()


def test_groups_from_ids_with_empty_list():
    """Test that groups_from_ids works with empty input."""
    result = groups_from_ids()
    assert result == tuple()


def test_traits_from_ids_with_multiple_valid_ids():
    """Test that traits_from_ids works with multiple valid IDs."""
    result = traits_from_ids("linux", "ubuntu", "macos")
    # Should include LINUX group members plus UBUNTU and MACOS.
    assert UBUNTU in result
    assert MACOS in result
    # LINUX is a group, so its members should be in the result.
    assert DEBIAN in result


def test_groups_from_ids_with_multiple_valid_ids():
    """Test that groups_from_ids works with multiple valid IDs."""
    result = groups_from_ids("linux", "bsd", "unix")
    assert LINUX in result
    assert BSD in result
    assert UNIX in result


def test_reduce_with_already_minimal_group():
    """Test reduce with groups that cannot be further reduced."""
    # AIX is a single platform, can't be reduced further.
    result = reduce([AIX])
    assert result == {AIX}


def test_reduce_with_complex_overlap():
    """Test reduce with complex overlapping groups."""
    # Test with multiple groups that have complex overlaps.
    result = reduce([LINUX, BSD, UNIX])
    # Should return the minimal covering set.
    assert isinstance(result, frozenset)
    # UNIX covers both LINUX and BSD, so it's the minimal representation.
    assert UNIX in result
    assert len(result) == 1


def test_reduce_returns_frozenset():
    """Test that reduce always returns a frozenset."""
    result1 = reduce([])
    result2 = reduce([MACOS])
    result3 = reduce([LINUX, BSD])

    assert isinstance(result1, frozenset)
    assert isinstance(result2, frozenset)
    assert isinstance(result3, frozenset)


def test_all_ids_constant():
    """Test that ALL_IDS constant contains all trait and group IDs."""
    # ALL_IDS should be the union of ALL_TRAIT_IDS and ALL_GROUP_IDS.
    assert ALL_IDS == ALL_TRAIT_IDS | ALL_GROUP_IDS


def test_all_trait_ids_completeness():
    """Test that ALL_TRAIT_IDS contains IDs from all non-unknown traits."""
    # ALL_TRAIT_IDS excludes unknown traits.
    expected_ids = {trait.id for trait in ALL_TRAITS if not trait.id.startswith("unknown")}
    assert ALL_TRAIT_IDS == expected_ids


def test_all_group_ids_completeness():
    """Test that ALL_GROUP_IDS contains IDs from all non-unknown groups."""
    # ALL_GROUP_IDS excludes the UNKNOWN group.
    expected_ids = {group.id for group in ALL_GROUPS if group.id != "unknown"}
    assert ALL_GROUP_IDS == expected_ids
