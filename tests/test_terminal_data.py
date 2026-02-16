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
"""Test all terminal definitions, detection and terminal-specific groups."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from extra_platforms import (
    ALL_TERMINAL_GROUPS,
    ALL_TERMINALS,
    ALL_TRAITS,
    GPU_TERMINALS,
    MULTIPLEXERS,
    NATIVE_TERMINALS,
    NON_OVERLAPPING_GROUPS,
    UNKNOWN_TERMINAL,
    WEB_TERMINALS,
    current_terminal,
    is_unknown_terminal,
)
from extra_platforms import terminal_data as terminal_data_module


def test_terminal_data_sorting():
    """Terminal instances must be sorted alphabetically."""
    terminal_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(terminal_data_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            assert node.value.func.id == "Terminal"
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            terminal_instance_ids.append(instance_id)

    assert terminal_instance_ids == sorted(terminal_instance_ids)

    # Check all defined terminals are referenced in top-level collections.
    all_terminal_ids = set(map(str.lower, terminal_instance_ids))
    assert all_terminal_ids.issubset(ALL_TERMINALS.member_ids | {UNKNOWN_TERMINAL.id})
    assert all_terminal_ids.issubset(ALL_TRAITS.member_ids)


def test_terminal_detection():
    """Basic terminal detection sanity checks."""
    current_terminal_result = current_terminal()
    assert current_terminal_result
    if is_unknown_terminal():
        assert current_terminal_result is UNKNOWN_TERMINAL
        assert current_terminal_result not in ALL_TERMINALS
    else:
        assert current_terminal_result is not UNKNOWN_TERMINAL
        assert current_terminal_result in ALL_TERMINALS


def test_terminal_logical_grouping():
    """All terminal groups are subsets of ALL_TERMINALS."""
    for group in ALL_TERMINAL_GROUPS:
        assert group.issubset(ALL_TERMINALS)

    assert not ALL_TERMINALS.canonical
    assert GPU_TERMINALS.canonical
    assert MULTIPLEXERS.canonical
    assert NATIVE_TERMINALS.canonical
    assert WEB_TERMINALS.canonical


def test_no_missing_terminal_in_groups():
    """Check all terminals are attached to at least one non-overlapping group."""
    ALL_TERMINALS.fullyintersects(ALL_TERMINAL_GROUPS & NON_OVERLAPPING_GROUPS)
