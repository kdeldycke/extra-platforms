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

from __future__ import annotations

from operator import attrgetter

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
    BSD,
    BSD_WITHOUT_MACOS,
    DEBIAN,
    DRAGONFLY_BSD,
    FREEBSD,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    MACOS,
    MIDNIGHTBSD,
    NETBSD,
    OPENBSD,
    PIDORA,
    RHEL,
    SUNOS,
    UBUNTU,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    WINDOWS,
    WSL1,
    Group,
    Platform,
    extract_members,
    groups_from_ids,
    reduce,
    traits_from_ids,
)
from extra_platforms.trait import _resolve_alias

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable


def test_deduplication():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    assert len(my_group) == 1
    assert len(my_group._members) == 1
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
    with pytest.raises(KeyError, match="No trait found whose ID is rhel"):
        my_group["rhel"]

    # Test platform items getter.
    assert list(my_group.items()) == [("aix", AIX), ("pidora", PIDORA)]


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], []),
        ((), ()),
        (set(), set()),
        (frozenset(), frozenset()),
        (None, []),
        ([None], []),
        ([None, None, None], []),
        ([None, (None, None, [])], []),
        ((AIX, None, None), [AIX]),
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
        ([LINUX, [UBUNTU]], (*LINUX, UBUNTU)),
    ],
)
def test_extract_members(items, expected):
    assert tuple(extract_members(items)) == tuple(expected)


@pytest.mark.parametrize(
    "item", (42, 42.0, object(), lambda: None, [42], [42, 42], [42, [42, 42]])
)
def test_extract_members_bad_type(item):
    with pytest.raises(TypeError, match="Unsupported type"):
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


@pytest.mark.parametrize(
    ("method", "first", "others", "expected"),
    (
        pytest.param(
            "union",
            ALL_WINDOWS,
            (LINUX_LAYERS,),
            {"windows", "wsl1", "wsl2"},
            id="union",
        ),
        pytest.param(
            "union",
            ALL_WINDOWS,
            (LINUX_LAYERS, UNIX_LAYERS),
            {"windows", "wsl1", "wsl2", "cygwin", "os400"},
            id="union_of_many",
        ),
        pytest.param(
            "intersection",
            ALL_PLATFORMS,
            (ALL_WINDOWS,),
            {"windows"},
            id="intersection",
        ),
        pytest.param(
            "intersection",
            ALL_PLATFORMS,
            (UNIX_WITHOUT_MACOS, BSD_WITHOUT_MACOS),
            {"dragonfly_bsd", "freebsd", "midnightbsd", "netbsd", "openbsd", "sunos"},
            id="intersection_of_many",
        ),
        pytest.param(
            "difference", BSD, (BSD_WITHOUT_MACOS,), {"macos"}, id="difference"
        ),
        pytest.param(
            "difference",
            ALL_PLATFORMS,
            (LINUX, UNIX, ALL_CI),
            {"windows"},
            id="difference_of_many",
        ),
        pytest.param(
            "symmetric_difference",
            ALL_WINDOWS | BSD_WITHOUT_MACOS,
            (BSD,),
            {"macos", "windows"},
            id="symmetric_difference",
        ),
    ),
)
def test_set_operation(method, first, others, expected):
    """A set operation acts on the members, keeping the first group's metadata."""
    result = getattr(first, method)(*others)
    assert result.member_ids == frozenset(expected)
    # The members match what the same operation gives on native sets.
    assert set(result) == getattr(set(first), method)(*map(set, others))
    assert (result.id, result.name, result.icon) == (first.id, first.name, first.icon)


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
    empty_group = Group("empty", "Empty Group", "❌", ())
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
    empty_group = Group("empty", "Empty", "❌", ())
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


def test_group_operations_with_empty_groups():
    """Test group operations with empty groups."""
    empty_group = Group(id="empty", name="Empty Group", icon="❌", members=())

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


def test_group_fullyintersects():
    """Test fullyintersects method."""
    # LINUX and BSD should be disjoint (no full intersection).
    assert not LINUX.fullyintersects(BSD)

    # LINUX should fully intersect with itself.
    assert LINUX.fullyintersects(LINUX)

    # A strict superset or subset is no full intersection.
    assert not BSD.fullyintersects(BSD_WITHOUT_MACOS)
    assert not BSD_WITHOUT_MACOS.fullyintersects(BSD)


def test_unique_ids():
    """Group IDs are unique, and no trait shares one.

    No check of the trait IDs belongs here: a group keys its members by ID, so
    `ALL_TRAITS` hides a duplicate. `test_trait_data.py` checks them instead.
    """
    all_group_ids = {g.id for g in ALL_GROUPS}
    assert len(all_group_ids) == len(ALL_GROUPS)
    assert all_group_ids.isdisjoint(ALL_TRAITS.member_ids)


def randomize_case(strings: Iterable[str]) -> list[str]:
    """Generate variations of strings with different case.

    Sorted, so every xdist worker collects the same parameters in the same order.
    """
    test_strings = set()
    for string in strings:
        test_strings.add(string)
        test_strings.update(
            str_func(string)
            for str_func in (
                str.upper,
                str.lower,
                str.title,
                str.capitalize,
                str.casefold,
                str.swapcase,
            )
        )
        test_strings.add(
            "".join(
                char.upper() if i % 2 else char.lower() for i, char in enumerate(string)
            )
        )
    return sorted(test_strings)


@pytest.mark.parametrize("trait_id", randomize_case(ALL_TRAIT_IDS))
def test_traits_from_ids(trait_id):
    """Test traits_from_ids with various case variations."""
    traits = traits_from_ids(trait_id)
    assert traits
    assert len(traits) == 1
    trait = traits[0]
    assert trait.id == trait_id.lower()
    assert trait in ALL_TRAITS


@pytest.mark.parametrize(
    ("alias", "trait"),
    # ALL_TRAITS iterates in ID order, so sorting each set of aliases is enough
    # to collect the same order on every xdist worker.
    [(alias, trait) for trait in ALL_TRAITS for alias in sorted(trait.aliases)],
    ids=lambda value: value if isinstance(value, str) else value.id,
)
@pytest.mark.parametrize(
    "resolve", (traits_from_ids, extract_members), ids=attrgetter("__name__")
)
def test_alias_resolves_with_warning(resolve, alias, trait):
    """An alias resolves to its trait, with a warning naming the canonical ID.

    The warning points at the caller, whatever call chain inside the package
    reached the resolution.
    """
    # The resolution is cached, so it warns on its first call only.
    _resolve_alias.cache_clear()
    with pytest.warns(
        UserWarning, match=f"'{alias}' is an alias for '{trait.id}'"
    ) as record:
        assert tuple(resolve(alias.upper())) == (trait,)
    assert record[0].filename == __file__


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
        ([LINUX, BSD, UNIX], {UNIX}),
        (
            # Every individual platform, plus the ALL_CI group and every
            # individual CI system: reduces to the two "all" groups.
            [*ALL_PLATFORMS, ALL_CI, *ALL_CI],
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


@pytest.mark.parametrize(
    ("from_ids", "message"),
    (
        (traits_from_ids, "Unrecognized group or trait IDs"),
        (groups_from_ids, "Unrecognized group IDs"),
    ),
    ids=("traits_from_ids", "groups_from_ids"),
)
def test_from_ids_edge_cases(from_ids, message):
    """No ID resolves to nothing, and an unknown ID raises."""
    assert from_ids() == ()
    with pytest.raises(ValueError, match=message):
        from_ids("cucumber")


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
