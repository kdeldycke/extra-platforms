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
"""Test trait data sorting and group coverage across all trait types."""

from __future__ import annotations

import ast
import inspect
from operator import attrgetter
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_TRAITS,
    NON_OVERLAPPING_GROUPS,
    Agent,
    Architecture,
    CI,
    Platform,
    Shell,
    Terminal,
)

TRAIT_CLASSES = (Architecture, Platform, Shell, Terminal, CI, Agent)


@pytest.mark.parametrize("klass", TRAIT_CLASSES, ids=attrgetter("__name__"))
def test_trait_data_sorting(klass):
    """Trait instances must be sorted alphabetically in their data module."""
    data_module = getattr(extra_platforms, klass.data_module_id)
    instance_ids = []
    tree = ast.parse(Path(inspect.getfile(data_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            assert node.value.func.id == klass.__name__
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            instance_ids.append(instance_id)

    assert instance_ids == sorted(instance_ids)

    # Check all defined traits are referenced in top-level collections.
    all_group = getattr(extra_platforms, klass.all_group)
    unknown_trait = getattr(extra_platforms, klass.unknown_symbol)
    all_ids = set(map(str.lower, instance_ids))
    assert all_ids.issubset(all_group.member_ids | {unknown_trait.id})
    assert all_ids.issubset(ALL_TRAITS.member_ids)


@pytest.mark.parametrize("klass", TRAIT_CLASSES, ids=attrgetter("__name__"))
def test_groups_are_subsets(klass):
    """All groups of a trait type are subsets of the corresponding ALL_* group."""
    all_group = getattr(extra_platforms, klass.all_group)
    all_type_groups_symbol = f"ALL_{klass.type_id.upper()}_GROUPS"
    all_type_groups = getattr(extra_platforms, all_type_groups_symbol)
    for group in all_type_groups:
        assert group.issubset(all_group)


@pytest.mark.parametrize("klass", TRAIT_CLASSES, ids=attrgetter("__name__"))
def test_no_missing_trait_in_groups(klass):
    """Check all traits are attached to at least one non-overlapping group."""
    all_group = getattr(extra_platforms, klass.all_group)
    all_type_groups_symbol = f"ALL_{klass.type_id.upper()}_GROUPS"
    all_type_groups = getattr(extra_platforms, all_type_groups_symbol)
    all_group.fullyintersects(all_type_groups & NON_OVERLAPPING_GROUPS)
