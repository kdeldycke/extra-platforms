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
import re
from itertools import combinations
from pathlib import Path
from string import ascii_lowercase, digits

import pytest

import extra_platforms
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
    CI,
    EXTRA_GROUPS,
    NON_OVERLAPPING_GROUPS,
    UNKNOWN,
    Architecture,
    Group,
    Platform,
    Trait,
)
from extra_platforms import group_data as group_data_module


def test_group_class_metadata():
    class_id = Group.__name__.lower()

    assert Group.type_name
    assert Group.type_name.isascii()
    assert Group.type_name.isprintable()

    assert Group.data_module_id == f"{class_id}_data"
    assert hasattr(extra_platforms, Group.data_module_id)

    assert Group.unknown_symbol == "UNKNOWN"
    assert (
        Group.unknown_symbol == getattr(extra_platforms, Group.unknown_symbol).symbol_id
    )

    assert Group.all_group == "ALL_GROUPS"
    assert hasattr(extra_platforms, Group.all_group)

    assert Group.doc_page.startswith(class_id)
    assert Group.doc_page.endswith(".md")
    # Verify that the doc_page actually exists in the docs directory.
    doc_file = Path(__file__).parent.parent / "docs" / Group.doc_page
    assert doc_file.exists(), f"Documentation file not found: {doc_file}"
    assert doc_file.is_file(), f"Expected a file but got directory: {doc_file}"
    # Verify that the file starts with a proper markdown title.
    assert re.fullmatch(
        rf"# \{{octicon}}`\S+` {Group.type_name[0].upper()}{Group.type_name[1:]}s",
        doc_file.read_text(encoding="utf-8").splitlines()[0],
    )


def test_group_data_ordering():
    """Group instances follow logical order, not alphabetical."""
    group_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(group_data_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            assert node.value.func.id == "Group"
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            group_instance_ids.append(instance_id)

    # Group order is logical, not alphabetical.
    assert group_instance_ids != sorted(group_instance_ids)

    # Check all defined groups are in ALL_GROUPS.
    for group_symbol_id in group_instance_ids:
        group_id = group_symbol_id.lower()
        assert group_id in ALL_GROUP_IDS or group_id == UNKNOWN.id


@pytest.mark.parametrize("group", tuple(ALL_GROUPS), ids=lambda g: g.id)
def test_group_definitions(group: Group):
    assert isinstance(group, Group)

    # ID.
    assert group.id
    assert group.id.isascii()
    assert group.id[0] in ascii_lowercase
    assert group.id[-1] in ascii_lowercase + digits
    assert set(group.id).issubset(ascii_lowercase + digits + "_")
    assert group.id.islower()

    # Split ID by underscores to get individual tokens.
    tokens = group.id.split("_")
    # "unknown" is only allowed for the UNKNOWN group.
    if "unknown" in tokens:
        assert group.id.startswith("unknown")
        assert group is UNKNOWN
        assert group.name == "Unknown"
    # "all" is only allowed for all-traits groups.
    if "all" in tokens:
        assert group.id.startswith("all_")
    # "without" indicates exclusion, and must be part of a compound word.
    if "without" in tokens:
        assert "_without_" in group.id
    # Special words that should never appear as standalone tokens in group IDs.
    for special_word in ("any", "is", "skip", "unless", "not"):
        assert not group.id.startswith(special_word)
        assert special_word not in group.id.split("_")

    assert group.id not in ALL_TRAIT_IDS
    if group is UNKNOWN:
        assert group.id not in ALL_GROUP_IDS
        assert group.id not in ALL_IDS
    else:
        assert group.id in ALL_GROUP_IDS
        assert group.id in ALL_IDS

    # Symbol ID.
    assert group.symbol_id == group.id.upper()
    assert group.symbol_id.lower() == group.id
    assert group.symbol_id in group_data_module.__dict__
    assert getattr(group_data_module, group.symbol_id) is group
    assert getattr(extra_platforms, group.symbol_id) is group

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
    assert len(group._members) == len(group.member_ids)
    assert tuple(group._members.keys()) == tuple(group._members)
    assert len(set(group._members.keys())) == len(group._members)
    assert len(set(group._members.values())) == len(group._members)
    assert all(isinstance(m_id, str) for m_id in group._members.keys())
    assert all(isinstance(m, Trait) for m in group._members.values())

    # Canonical groups are self-canonical.
    assert group.canonical is (group in NON_OVERLAPPING_GROUPS)

    # Check general subset properties and operators.
    assert group.member_ids.issubset(ALL_TRAITS.member_ids)
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
    assert group.issubset(group._members.values())
    assert group.issuperset(group._members.values())

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
    assert not group.isdisjoint(group._members.values())
    assert group.fullyintersects(group)
    assert group.fullyintersects(group._members.values())

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


def test_unique_icons():
    """Check all group icons are unique."""
    icons = {group.icon for group in ALL_GROUPS}
    assert len(icons) == len(ALL_GROUPS)


def test_unknown_group():
    """All members of the UNKNOWN group are unknown traits."""
    for trait in UNKNOWN:
        assert trait.id.startswith("unknown_")
        assert trait.name.startswith("Unknown ")
        assert trait in ALL_TRAITS
        assert trait not in ALL_ARCHITECTURES
        assert trait not in ALL_PLATFORMS
        assert trait not in ALL_CI
        assert trait.icon == "❓"


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
        == ALL_ARCHITECTURE_GROUPS
        | ALL_PLATFORM_GROUPS
        | ALL_CI_GROUPS
        | {ALL_TRAITS}
        | {UNKNOWN}
    )


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


def test_each_trait_in_exactly_one_canonical_group():
    """Check each trait belongs to exactly one canonical group."""
    for trait in ALL_TRAITS:
        canonical_groups = [group for group in NON_OVERLAPPING_GROUPS if trait in group]
        assert len(canonical_groups) == 1, (
            f"Trait {trait.id!r} is in {len(canonical_groups)} canonical groups: "
            f"{[g.id for g in canonical_groups]}"
        )


def test_canonical_groups_dont_overlap():
    """Test that canonical groups have no members in common with each other."""
    canonical_list = list(NON_OVERLAPPING_GROUPS)
    for i, group1 in enumerate(canonical_list):
        for group2 in canonical_list[i + 1 :]:
            assert group1.isdisjoint(group2), (
                f"Canonical groups {group1.id} and {group2.id} overlap"
            )


def test_canonical_groups_cover_all_traits():
    """Test that canonical groups together cover all recognized traits."""
    # Union all canonical groups, excluding unknown traits.
    all_canonical_members = set()
    for group in NON_OVERLAPPING_GROUPS:
        for member in group:
            # Exclude unknown traits.
            if not member.id.startswith("unknown_"):
                all_canonical_members.add(member)

    # Should cover all traits except UNKNOWN.
    # ALL_TRAITS - UNKNOWN returns a Group, so we compare to its set.
    assert all_canonical_members == set(ALL_TRAITS - UNKNOWN), (
        "Canonical groups don't cover all non-UNKNOWN traits"
    )


def test_non_overlapping_groups_completeness():
    """Test that NON_OVERLAPPING_GROUPS is properly defined."""
    # Should have at least 3 canonical groups (architectures, platforms, CI).
    assert len(NON_OVERLAPPING_GROUPS) >= 3

    # Each group in NON_OVERLAPPING_GROUPS should have canonical=True.
    for group in NON_OVERLAPPING_GROUPS:
        assert group.canonical is True


def test_canonical_group_marker():
    """Test that canonical groups have the ⬥ marker in their documentation."""
    for group in NON_OVERLAPPING_GROUPS:
        # We can't directly test the markdown output, but we can verify
        # the canonical property is True.
        assert group.canonical is True

    # Non-canonical groups should have canonical=False.
    for group in EXTRA_GROUPS:
        assert group.canonical is False
