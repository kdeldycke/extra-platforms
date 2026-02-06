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
    LINUX_LAYERS,
    LINUX_LIKE,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    NOBARA,
    NON_OVERLAPPING_GROUPS,
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
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    Group,
    Platform,
    Trait,
    extract_members,
    groups_from_ids,
    reduce,
    traits_from_ids,
)


def test_deduplication():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    assert len(my_group) == 1
    assert len(my_group.members) == 1
    assert len(my_group.member_ids) == 1

    assert tuple(my_group) == (AIX,)
    assert my_group.member_ids == frozenset({"aix"})


def test_membership():
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA))

    # Test iteration.
    assert list(my_group) == [AIX, PIDORA]
    assert tuple(my_group) == (AIX, PIDORA)
    assert set(my_group) == {AIX, PIDORA}

    # Test platform membership.
    assert AIX in my_group
    assert PIDORA in my_group
    assert RHEL not in my_group

    # Test platform ID membership.
    assert "aix" in my_group
    assert "pidora" in my_group
    assert "rhel" not in my_group

    # Test platform ID getter.
    assert my_group["aix"] == AIX
    assert my_group["pidora"] == PIDORA
    with pytest.raises(KeyError):
        my_group["rhel"]

    # Test platform items getter.
    assert list(my_group.items()) == [("aix", AIX), ("pidora", PIDORA)]


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], []),
        (tuple(), tuple()),
        (set(), set()),
        (frozenset(), frozenset()),
        (None, []),
        ([None], []),
        ([None, None, None], []),
        ([None, (None, None, [])], []),
        (AIX, [AIX]),
        ("aix", [AIX]),
        ([AIX], [AIX]),
        ([AIX, AIX], [AIX, AIX]),
        ([AIX, (AIX, AIX)], [AIX, AIX, AIX]),
        ([AIX, ("aix", AIX)], [AIX, AIX, AIX]),
        (LINUX_LAYERS, tuple(LINUX_LAYERS)),
        (LINUX_LAYERS, LINUX_LAYERS),
        ("linux_layers", LINUX_LAYERS),
        ([LINUX_LAYERS], LINUX_LAYERS),
        ([LINUX_LAYERS, LINUX_LAYERS], tuple(LINUX_LAYERS) * 2),
        ([LINUX_LAYERS, (LINUX_LAYERS, LINUX_LAYERS)], tuple(LINUX_LAYERS) * 3),
        ([LINUX_LAYERS, ("linux_layers", LINUX_LAYERS)], tuple(LINUX_LAYERS) * 3),
    ],
)
def test_extract_members(items, expected):
    assert tuple(extract_members(items)) == tuple(expected)


@pytest.mark.parametrize(
    "item", (42, 42.0, object(), lambda: None, [42], [42, 42], [42, [42, 42]])
)
def test_extract_members_bad_type(item):
    with pytest.raises(TypeError):
        tuple(extract_members(item))


def test_canonical_property():
    # A random group is not canonical by default.
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA))
    assert not my_group.canonical

    # An empty group is not canonical.
    empty_group = Group("empty", "Empty Group")
    assert not empty_group.canonical

    # A copied canonical group stays canonical.
    assert ALL_WINDOWS.canonical
    copied_windows = ALL_WINDOWS.copy()
    assert copied_windows.canonical

    # A modified canonical group is not canonical.
    assert LINUX.canonical
    modified_linux = LINUX.add(AIX)
    assert not modified_linux.canonical


def test_simple_union():
    new_group = ALL_WINDOWS.union(LINUX_LAYERS)

    assert ALL_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert new_group.issuperset(ALL_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)

    assert new_group.id == ALL_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.name == ALL_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.icon == ALL_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon

    assert set(new_group.members) != set(ALL_WINDOWS.members)
    assert set(new_group.member_ids) != set(ALL_WINDOWS.member_ids)
    assert set(new_group.members) != set(LINUX_LAYERS.members)
    assert set(new_group.member_ids) != set(LINUX_LAYERS.member_ids)

    assert set(new_group.members) == set(ALL_WINDOWS.members).union(
        LINUX_LAYERS.members
    )
    assert set(new_group.member_ids) == set(ALL_WINDOWS.member_ids).union(
        LINUX_LAYERS.member_ids
    )


def test_multiple_union():
    new_group = ALL_WINDOWS.union(LINUX_LAYERS, UNIX_LAYERS)

    assert new_group.member_ids == frozenset(("windows", "wsl1", "wsl2", "cygwin"))

    assert ALL_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert UNIX_LAYERS.issubset(new_group)

    assert new_group.issuperset(ALL_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)
    assert new_group.issuperset(UNIX_LAYERS)

    assert new_group.id == ALL_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.id != UNIX_LAYERS.id
    assert new_group.name == ALL_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.name != UNIX_LAYERS.name
    assert new_group.icon == ALL_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon
    assert new_group.icon != UNIX_LAYERS.icon

    assert set(new_group.members) != set(ALL_WINDOWS.members)
    assert set(new_group.member_ids) != set(ALL_WINDOWS.member_ids)
    assert set(new_group.members) != set(LINUX_LAYERS.members)
    assert set(new_group.member_ids) != set(LINUX_LAYERS.member_ids)
    assert set(new_group.members) != set(UNIX_LAYERS.members)
    assert set(new_group.member_ids) != set(UNIX_LAYERS.member_ids)

    assert set(new_group.members) == set(ALL_WINDOWS.members).union(
        LINUX_LAYERS.members
    ).union(UNIX_LAYERS.members)
    assert set(new_group.member_ids) == set(ALL_WINDOWS.member_ids).union(
        LINUX_LAYERS.member_ids
    ).union(UNIX_LAYERS.member_ids)


def test_single_intersection():
    new_group = ALL_PLATFORMS.intersection(ALL_WINDOWS)

    assert new_group.member_ids == frozenset(("windows",))

    assert ALL_WINDOWS.issubset(new_group)
    assert not ALL_PLATFORMS.issubset(new_group)
    assert new_group.issuperset(ALL_WINDOWS)
    assert not new_group.issuperset(ALL_PLATFORMS)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != ALL_WINDOWS.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != ALL_WINDOWS.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != ALL_WINDOWS.icon

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)

    assert set(new_group.members) == set(ALL_WINDOWS.members)
    assert set(new_group.member_ids) == set(ALL_WINDOWS.member_ids)


def test_multiple_intersection():
    new_group = ALL_PLATFORMS.intersection(UNIX_WITHOUT_MACOS, BSD_WITHOUT_MACOS)

    assert new_group.member_ids == frozenset((
        "dragonfly_bsd",
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

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)
    assert set(new_group.members) != set(UNIX_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) != set(UNIX_WITHOUT_MACOS.member_ids)

    assert set(new_group.members) == set(BSD_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) == set(BSD_WITHOUT_MACOS.member_ids)


def test_single_difference():
    new_group = BSD.difference(BSD_WITHOUT_MACOS)

    assert new_group.member_ids == frozenset(("macos",))

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

    assert set(new_group.members) != set(BSD.members)
    assert set(new_group.member_ids) != set(BSD.member_ids)
    assert set(new_group.members) != set(BSD_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) != set(BSD_WITHOUT_MACOS.member_ids)

    assert set(new_group.members) == set(BSD.members).difference(
        BSD_WITHOUT_MACOS.members
    )
    assert set(new_group.member_ids) == set(BSD.member_ids).difference(
        BSD_WITHOUT_MACOS.member_ids
    )


def test_multiple_difference():
    new_group = ALL_PLATFORMS.difference(LINUX, UNIX, ALL_CI)

    assert new_group.member_ids == frozenset(("windows",))

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

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)
    assert set(new_group.members) != set(LINUX.members)
    assert set(new_group.member_ids) != set(LINUX.member_ids)
    assert set(new_group.members) != set(UNIX.members)
    assert set(new_group.member_ids) != set(UNIX.member_ids)

    assert set(new_group.members) == set(ALL_PLATFORMS.members).difference(
        LINUX.members
    ).difference(UNIX.members).difference(ALL_CI.members)
    assert set(new_group.member_ids) == set(ALL_PLATFORMS.member_ids).difference(
        LINUX.member_ids
    ).difference(UNIX.member_ids).difference(ALL_CI.member_ids)


def test_symmetric_difference():
    win_and_bsd = ALL_WINDOWS.union(BSD_WITHOUT_MACOS)
    new_group = win_and_bsd.symmetric_difference(BSD)

    assert new_group.member_ids == frozenset((("macos", "windows")))

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

    assert set(new_group.members) != set(BSD.members)
    assert set(new_group.member_ids) != set(BSD.member_ids)
    assert set(new_group.members) != set(win_and_bsd.members)
    assert set(new_group.member_ids) != set(win_and_bsd.member_ids)

    assert set(new_group.members) == set(win_and_bsd.members).symmetric_difference(
        BSD.members
    )
    assert set(new_group.member_ids) == set(
        win_and_bsd.member_ids
    ).symmetric_difference(BSD.member_ids)


def test_copy():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    my_group_copy1 = my_group.copy()
    assert my_group == my_group_copy1
    assert my_group is not my_group_copy1

    my_group_copy2 = my_group.copy(
        id="my_group_copy2", name="My Group Copy 2", icon="🚀"
    )
    assert my_group_copy2 != my_group
    assert my_group_copy2 is not my_group
    assert my_group_copy2 != my_group_copy1
    assert my_group_copy2 is not my_group_copy1
    assert my_group_copy2.id == "my_group_copy2"
    assert my_group_copy2.name == "My Group Copy 2"
    assert my_group_copy2.icon == "🚀"
    assert my_group_copy2.members == my_group.members
    assert my_group_copy2.member_ids == my_group.member_ids
    assert my_group_copy2.members == my_group_copy1.members
    assert my_group_copy2.member_ids == my_group_copy1.member_ids


def test_bool():
    """Test __bool__() method for truth value testing."""
    # Empty group should be falsy.
    empty_group = Group("empty", "Empty Group", "❌", tuple())
    assert not empty_group
    assert bool(empty_group) is False

    # Non-empty group should be truthy.
    non_empty_group = Group("non_empty", "Non-Empty Group", "✅", (AIX, PIDORA))
    assert non_empty_group
    assert bool(non_empty_group) is True

    # Group with one member should be truthy.
    single_member = Group("single", "Single Member", "✅", (AIX,))
    assert single_member
    assert bool(single_member) is True


def test_add():
    """Test add() method for adding a single trait."""
    my_group = Group("my_group", "My Group", "✅", (AIX,))

    # Add a new trait.
    new_group = my_group.add(PIDORA)
    assert PIDORA in new_group
    assert AIX in new_group
    assert len(new_group) == 2
    assert new_group.member_ids == frozenset({"aix", "pidora"})

    # Original group should be unchanged.
    assert len(my_group) == 1
    assert PIDORA not in my_group

    # Add a trait that already exists (should return unchanged copy).
    same_group = new_group.add(AIX)
    assert len(same_group) == 2
    assert same_group.member_ids == new_group.member_ids

    # Add by trait ID string.
    with_rhel = my_group.add("rhel")
    assert RHEL in with_rhel
    assert "rhel" in with_rhel
    assert len(with_rhel) == 2

    # Add invalid trait ID should raise ValueError.
    with pytest.raises(ValueError, match="Unrecognized group or trait IDs"):
        my_group.add("invalid_trait_id")


def test_remove():
    """Test remove() method for removing a trait with error checking."""
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA, RHEL))

    # Remove a trait by object.
    new_group = my_group.remove(PIDORA)
    assert PIDORA not in new_group
    assert AIX in new_group
    assert RHEL in new_group
    assert len(new_group) == 2
    assert new_group.member_ids == frozenset({"aix", "rhel"})

    # Original group should be unchanged.
    assert len(my_group) == 3
    assert PIDORA in my_group

    # Remove by trait ID string.
    without_aix = my_group.remove("aix")
    assert AIX not in without_aix
    assert "aix" not in without_aix
    assert len(without_aix) == 2

    # Remove non-existent trait should raise KeyError.
    with pytest.raises(KeyError, match="Trait 'invalid' is not in the group"):
        my_group.remove("invalid")

    with pytest.raises(KeyError, match="is not in the group"):
        new_group.remove(PIDORA)


def test_discard():
    """Test discard() method for removing a trait without error."""
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA, RHEL))

    # Discard a trait by object.
    new_group = my_group.discard(PIDORA)
    assert PIDORA not in new_group
    assert AIX in new_group
    assert RHEL in new_group
    assert len(new_group) == 2

    # Original group should be unchanged.
    assert len(my_group) == 3
    assert PIDORA in my_group

    # Discard by trait ID string.
    without_aix = my_group.discard("aix")
    assert AIX not in without_aix
    assert len(without_aix) == 2

    # Discard non-existent trait should NOT raise error.
    same_group = my_group.discard("invalid")
    assert len(same_group) == 3
    assert same_group.member_ids == my_group.member_ids

    # Discard already removed trait should NOT raise error.
    still_same = new_group.discard(PIDORA)
    assert len(still_same) == 2


def test_pop():
    """Test pop() method for removing and returning a trait."""
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA, RHEL))

    # Pop a specific trait by ID.
    popped_trait, new_group = my_group.pop("pidora")
    assert popped_trait == PIDORA
    assert PIDORA not in new_group
    assert AIX in new_group
    assert RHEL in new_group
    assert len(new_group) == 2

    # Original group should be unchanged.
    assert len(my_group) == 3
    assert PIDORA in my_group

    # Pop arbitrary trait (first in iteration order).
    trait, smaller_group = new_group.pop()
    assert trait in {AIX, RHEL}
    assert trait not in smaller_group
    assert len(smaller_group) == 1

    # Pop from empty group should raise KeyError.
    empty_group = Group("empty", "Empty", "❌", tuple())
    with pytest.raises(KeyError, match="pop from an empty group"):
        empty_group.pop()

    # Pop non-existent trait ID should raise KeyError.
    with pytest.raises(KeyError, match="Trait 'invalid' is not in the group"):
        my_group.pop("invalid")


def test_clear():
    """Test clear() method for emptying a group."""
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA, RHEL))

    # Clear the group.
    empty_group = my_group.clear()
    assert len(empty_group) == 0
    assert not empty_group
    assert empty_group.member_ids == frozenset()

    # Metadata should be preserved.
    assert empty_group.id == my_group.id
    assert empty_group.name == my_group.name
    assert empty_group.icon == my_group.icon

    # Original group should be unchanged.
    assert len(my_group) == 3

    # Clear an already empty group.
    still_empty = empty_group.clear()
    assert len(still_empty) == 0
    assert still_empty.id == empty_group.id


def test_in_place_operators():
    """Test in-place operators that return new instances."""
    group_a = Group("group_a", "Group A", "🅰️", (AIX, PIDORA))
    group_b = Group("group_b", "Group B", "🅱️", (RHEL, PIDORA))

    # Test |= (union).
    result = group_a | group_b
    result_inplace = group_a.copy()
    result_inplace |= group_b
    assert result.member_ids == result_inplace.member_ids
    assert result.member_ids == frozenset({"aix", "pidora", "rhel"})

    # Test &= (intersection).
    result = group_a & group_b
    result_inplace = group_a.copy()
    result_inplace &= group_b
    assert result.member_ids == result_inplace.member_ids
    assert result.member_ids == frozenset({"pidora"})

    # Test -= (difference).
    result = group_a - group_b
    result_inplace = group_a.copy()
    result_inplace -= group_b
    assert result.member_ids == result_inplace.member_ids
    assert result.member_ids == frozenset({"aix"})

    # Test ^= (symmetric difference).
    result = group_a ^ group_b
    result_inplace = group_a.copy()
    result_inplace ^= group_b
    assert result.member_ids == result_inplace.member_ids
    assert result.member_ids == frozenset({"aix", "rhel"})

    # Verify original groups are unchanged.
    assert group_a.member_ids == frozenset({"aix", "pidora"})
    assert group_b.member_ids == frozenset({"rhel", "pidora"})


def test_set_operations_with_new_methods():
    """Test combining new methods with existing set operations."""
    base_group = Group("base", "Base Group", "🔵", (AIX, PIDORA))

    # Add, then union.
    with_rhel = base_group.add(RHEL)
    union_result = with_rhel.union(BSD_WITHOUT_MACOS)
    assert RHEL in union_result
    assert AIX in union_result
    assert PIDORA in union_result
    assert len(union_result) > 3

    # Remove, then intersection.
    without_aix = base_group.remove(AIX)
    intersection_result = without_aix.intersection(ALL_PLATFORMS)
    assert AIX not in intersection_result
    assert PIDORA in intersection_result

    # Clear, then add.
    empty = base_group.clear()
    with_one = empty.add(RHEL)
    assert len(with_one) == 1
    assert RHEL in with_one

    # Pop, then discard.
    popped_trait, remaining = base_group.pop("aix")
    assert popped_trait == AIX
    after_discard = remaining.discard("pidora")
    assert len(after_discard) == 0


def test_extract_members_with_unsupported_type():
    """Test that extract_members raises TypeError for unsupported types."""
    # Pass an unsupported type.
    with pytest.raises(TypeError, match="Unsupported type"):
        list(extract_members(123))


def test_getitem_with_missing_key():
    """Test that __getitem__ raises KeyError with proper message."""
    with pytest.raises(KeyError, match="No trait found whose ID is nonexistent"):
        _ = LINUX["nonexistent"]


def test_empty_group_bool():
    """Test that empty groups evaluate to False."""
    empty_group = Group(id="empty", name="Empty Group", icon="❌", members=tuple())
    assert bool(empty_group) is False
    assert len(empty_group) == 0


def test_group_operations_with_empty_groups():
    """Test group operations with empty groups."""
    empty_group = Group(id="empty", name="Empty Group", icon="❌", members=tuple())

    # Union with empty group.
    result = LINUX.union(empty_group)
    assert result == LINUX

    # Intersection with empty group.
    result = LINUX.intersection(empty_group)
    assert len(result) == 0

    # Difference with empty group.
    result = LINUX.difference(empty_group)
    assert result == LINUX

    # Empty group is disjoint with everything.
    assert LINUX.isdisjoint(empty_group)
    assert empty_group.isdisjoint(LINUX)


def test_group_with_duplicate_members():
    """Test that duplicate members in constructor are deduplicated."""
    # Create a group with duplicate members.
    group = Group(
        id="test_dupe",
        name="Test Duplicate",
        icon="🔁",
        members=[UBUNTU, UBUNTU, UBUNTU],
    )

    # Should only have one UBUNTU.
    assert len(group) == 1
    assert UBUNTU in group


def test_group_contains_with_string():
    """Test Group.__contains__ with string IDs."""
    assert "ubuntu" in LINUX
    assert "nonexistent" not in LINUX


def test_group_contains_with_wrong_trait_object():
    """Test that Group.__contains__ checks object identity, not just ID."""
    # Create a fake trait with the same ID as Ubuntu but different object.
    fake_ubuntu = Platform(
        id="ubuntu",
        name="Fake Ubuntu",
        icon="🐧",
        url="https://example.com",
    )

    # The real UBUNTU should be in LINUX.
    assert UBUNTU in LINUX

    # The fake ubuntu with the same ID but different object should NOT be in LINUX.
    assert fake_ubuntu not in LINUX


def test_group_items():
    """Test Group.items() returns key-value pairs."""
    items = list(BSD.items())
    assert len(items) > 0
    for trait_id, trait in items:
        assert isinstance(trait_id, str)
        assert isinstance(trait, Trait)
        assert trait.id == trait_id


def test_group_extract_members_with_none():
    """Test that extract_members ignores None values."""
    result = list(extract_members(UBUNTU, None, None))
    assert result == [UBUNTU]


def test_group_extract_members_nested():
    """Test that extract_members handles nested structures."""
    # Nested list of groups and traits.
    result = list(extract_members([LINUX, [UBUNTU]]))
    # Should include all members of LINUX plus UBUNTU.
    assert UBUNTU in result
    # LINUX members should also be in result.
    assert any(t.id == "debian" for t in result)


def test_group_fullyintersects():
    """Test fullyintersects method."""
    # LINUX and BSD should be disjoint (no full intersection).
    assert not LINUX.fullyintersects(BSD)

    # LINUX should fully intersect with itself.
    assert LINUX.fullyintersects(LINUX)


def test_group_canonical_property():
    """Test that Group.canonical property works correctly."""
    # LINUX is canonical.
    if LINUX in NON_OVERLAPPING_GROUPS:
        assert LINUX.canonical is True

    # UNIX is not canonical (overlaps with others).
    if UNIX not in NON_OVERLAPPING_GROUPS:
        assert UNIX.canonical is False


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
    """Generate variations of strings with different case."""
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
    """Test traits_from_ids with various case variations."""
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
    """Test groups_from_ids with various case variations."""
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
    """Test reduce function with various inputs."""
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
    """Test reduce with custom target pool."""
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
    expected_ids = {
        trait.id for trait in ALL_TRAITS if not trait.id.startswith("unknown")
    }
    assert ALL_TRAIT_IDS == expected_ids


def test_all_group_ids_completeness():
    """Test that ALL_GROUP_IDS contains IDs from all non-unknown groups."""
    # ALL_GROUP_IDS excludes the UNKNOWN group.
    expected_ids = {group.id for group in ALL_GROUPS if group.id != "unknown"}
    assert ALL_GROUP_IDS == expected_ids
