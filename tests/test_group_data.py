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
import inspect
from itertools import combinations
from pathlib import Path
from string import ascii_lowercase, digits

from extra_platforms import (
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUP_IDS,
    ALL_GROUPS,
    ALL_IDS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_TRAIT_IDS,
    ALL_TRAITS,
    ANY_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    EXTRA_GROUPS,
    LINUX,
    LINUX_LAYERS,
    NON_OVERLAPPING_GROUPS,
    OTHER_UNIX,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    Group,
    Trait,
)
from extra_platforms import group_data as group_data_module
from extra_platforms.architecture import Architecture
from extra_platforms.ci import CI
from extra_platforms.platform import Platform


def test_group_data_ordering():
    """Group instances follow logical order, not alphabetical."""
    group_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(group_data_module)).read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and node.value.func.id == "Group"
        ):
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            group_instance_ids.append(instance_id)

    # Group order is logical, not alphabetical.
    assert group_instance_ids != sorted(group_instance_ids)


def test_group_definitions():
    for group in ALL_GROUPS:
        assert isinstance(group, Group)

        # ID.
        assert group.id
        assert group.id.isascii()
        assert group.id[0] in ascii_lowercase
        assert group.id[-1] in ascii_lowercase + digits
        assert set(group.id).issubset(ascii_lowercase + digits + "_")
        assert group.id.islower()
        # Only the group referencing all platforms and its derivate are allowed to
        # start with "all_" prefix.
        if group in (ALL_ARCHITECTURES, ALL_PLATFORMS, ALL_CI, ALL_TRAITS):
            assert group.id.startswith("all_")
        else:
            assert not group.id.startswith("all_")
        assert group.id not in ALL_TRAIT_IDS
        assert group.id in ALL_GROUP_IDS
        assert group.id in ALL_IDS

        # Name.
        assert group.name
        assert group.name.isascii()
        assert group.name.isprintable()

        # Icon.
        assert group.icon
        assert 3 >= len(group.icon) >= 1

        # Members.
        assert len(group) > 0

        # Members are unique, in keys and values.
        assert len(group.members) == len(group.member_ids)
        assert group.member_ids.issubset(ALL_TRAITS.member_ids)
        assert tuple(group.members.keys()) == tuple(group.members)
        assert len(set(group.members.keys())) == len(group.members)
        assert len(set(group.members.values())) == len(group.members)
        assert all(isinstance(m_id, str) for m_id in group.members.keys())
        assert all(isinstance(m, Trait) for m in group.members.values())

        # Canonical groups are self-canonical.
        assert group.canonical is (group in NON_OVERLAPPING_GROUPS)

        # Check general subset properties and operators.
        assert group.issubset(ALL_TRAITS)
        assert group <= ALL_TRAITS
        if group != ALL_TRAITS:
            assert group < ALL_TRAITS
        assert ALL_TRAITS.issuperset(group)
        assert ALL_TRAITS >= group
        if group != ALL_TRAITS:
            assert ALL_TRAITS > group

        # Each group is both a subset and a superset of itself.
        assert group.issubset(group)
        assert group.issuperset(group)
        assert group.issubset(group.members.values())
        assert group.issuperset(group.members.values())

        # Test against empty iterables.
        assert group.issuperset(())
        assert group.issuperset([])
        assert group.issuperset({})
        assert group.issuperset(set())
        assert group.issuperset(frozenset())
        assert not group.issubset(())
        assert not group.issubset([])
        assert not group.issubset({})
        assert not group.issubset(set())
        assert not group.issubset(frozenset())

        for member in group:
            assert member in group
            assert member in ALL_TRAITS
            assert isinstance(member, Trait)
            assert member.id in group.member_ids
            assert group.issuperset([member])
            if len(group) == 1:
                assert group.issubset([member])
            else:
                assert not group.issubset([member])

        # A group cannot be disjoint from itself.
        assert not group.isdisjoint(group)
        assert not group.isdisjoint(group.members.values())
        assert group.fullyintersects(group)
        assert group.fullyintersects(group.members.values())

        # Test union.
        assert group.union() == group
        assert group.union(()) == group
        assert group.union([]) == group
        assert group.union({}) == group
        assert group.union(set()) == group
        assert group.union(frozenset()) == group
        assert group.union(group) == group
        assert group.union(group, group) == group
        assert group | group == group
        assert group | group | group == group

        empty_group = Group(group.id, group.name, group.icon)

        # Test intersection.
        assert group.intersection() == group
        assert group.intersection(()) == empty_group
        assert group.intersection([]) == empty_group
        assert group.intersection({}) == empty_group
        assert group.intersection(set()) == empty_group
        assert group.intersection(frozenset()) == empty_group
        assert group.intersection(group) == group
        assert group.intersection(group, group) == group
        assert group & group == group
        assert group & group & group == group

        # Test difference.
        assert group.difference() == group
        assert group.difference(()) == group
        assert group.difference([]) == group
        assert group.difference({}) == group
        assert group.difference(set()) == group
        assert group.difference(frozenset()) == group
        assert group.difference(group) == empty_group
        assert group.difference(group, group) == empty_group
        assert group - group == empty_group
        assert group - group - group == empty_group

        # Test symmetric_difference.
        assert group.symmetric_difference(()) == group
        assert group.symmetric_difference([]) == group
        assert group.symmetric_difference({}) == group
        assert group.symmetric_difference(set()) == group
        assert group.symmetric_difference(frozenset()) == group
        assert group.symmetric_difference(group) == empty_group
        assert group ^ group == empty_group


def test_group_constants():
    """Group constants and IDs must be aligned."""
    for group in ALL_GROUPS:
        group_constant = group.id.upper()
        assert group_constant in group_data_module.__dict__
        assert getattr(group_data_module, group_constant) is group


def test_unique_icons():
    """Check all group icons are unique."""
    icons = {group.icon for group in ALL_GROUPS}
    assert len(icons) == len(ALL_GROUPS)


def test_platform_logical_grouping():
    """Test logical grouping of platforms."""
    for group in BSD, LINUX, LINUX_LAYERS, SYSTEM_V, UNIX_LAYERS, OTHER_UNIX:
        assert group.issubset(UNIX)
        assert UNIX.issuperset(group)

    assert UNIX_WITHOUT_MACOS.issubset(UNIX)
    assert UNIX.issuperset(UNIX_WITHOUT_MACOS)

    assert BSD_WITHOUT_MACOS.issubset(UNIX)
    assert BSD_WITHOUT_MACOS.issubset(BSD)
    assert UNIX.issuperset(BSD_WITHOUT_MACOS)
    assert BSD.issuperset(BSD_WITHOUT_MACOS)

    # All platforms are divided into Windows and Unix at the highest level.
    assert ALL_PLATFORMS.fullyintersects(ANY_WINDOWS | UNIX)
    assert ANY_WINDOWS.canonical
    assert not UNIX.canonical

    # All UNIX platforms are divided into BSD, Linux, and Unix families.
    assert UNIX.fullyintersects(
        BSD | LINUX | LINUX_LAYERS | SYSTEM_V | UNIX_LAYERS | OTHER_UNIX
    )
    assert BSD.canonical
    assert LINUX.canonical
    assert LINUX_LAYERS.canonical
    assert SYSTEM_V.canonical
    assert UNIX_LAYERS.canonical
    assert OTHER_UNIX.canonical


def test_sets_of_groups():
    """Test properties of sets of groups, as well as individual groups."""
    for group_set in (
        ALL_ARCHITECTURE_GROUPS,
        ALL_PLATFORM_GROUPS,
        ALL_CI_GROUPS,
        NON_OVERLAPPING_GROUPS,
        EXTRA_GROUPS,
    ):
        assert len(group_set) > 0
        assert isinstance(group_set, frozenset)
        assert all(isinstance(g, Group) for g in group_set)
        assert group_set.issubset(ALL_GROUPS)
        assert ALL_GROUPS.issuperset(group_set)

    # Check groups containing the same kind of traits.
    for architecture_group in ALL_ARCHITECTURE_GROUPS:
        assert all(isinstance(m, Architecture) for m in architecture_group)
    for platform_group in ALL_PLATFORM_GROUPS:
        assert all(isinstance(m, Platform) for m in platform_group)
    for ci_group in ALL_CI_GROUPS:
        assert all(isinstance(m, CI) for m in ci_group)

    assert ALL_ARCHITECTURES.fullyintersects(ALL_ARCHITECTURE_GROUPS)
    assert ALL_PLATFORMS.fullyintersects(ALL_PLATFORM_GROUPS)
    assert ALL_CI.fullyintersects(ALL_CI_GROUPS)

    # Non-overlapping groups and overlapping groups don't overlap.
    assert NON_OVERLAPPING_GROUPS.isdisjoint(EXTRA_GROUPS)

    assert ALL_GROUPS == NON_OVERLAPPING_GROUPS | EXTRA_GROUPS
    assert (
        ALL_GROUPS
        == ALL_ARCHITECTURE_GROUPS | ALL_PLATFORM_GROUPS | ALL_CI_GROUPS | {ALL_TRAITS}
    )


def test_no_missing_platform_in_groups():
    """Check all platform are attached to at least one non-overlapping group."""
    ALL_PLATFORMS.fullyintersects(ALL_PLATFORM_GROUPS & NON_OVERLAPPING_GROUPS)


def test_non_overlapping_groups():
    """Check non-overlapping groups are mutually exclusive."""
    for combination in combinations(NON_OVERLAPPING_GROUPS, 2):
        group1, group2 = combination
        assert group1.isdisjoint(group2)
        assert group2.isdisjoint(group1)
        assert group1.canonical
        assert group2.canonical


def test_overlapping_groups():
    """Check all extra groups overlaps with at least one non-overlapping."""
    for extra_group in EXTRA_GROUPS:
        overlap = False
        for group in NON_OVERLAPPING_GROUPS:
            if not extra_group.isdisjoint(group):
                overlap = True
                break
        assert overlap is True
        assert not extra_group.canonical
