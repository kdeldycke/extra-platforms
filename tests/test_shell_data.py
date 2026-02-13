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
"""Test all shell definitions, detection and shell-specific groups."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from extra_platforms import (
    ALL_SHELL_GROUPS,
    ALL_SHELLS,
    ALL_TRAITS,
    BOURNE_SHELLS,
    C_SHELLS,
    NON_OVERLAPPING_GROUPS,
    OTHER_SHELLS,
    UNKNOWN_SHELL,
    current_shell,
    is_unknown_shell,
)
from extra_platforms import shell_data as shell_data_module


def test_shell_data_sorting():
    """Shell instances must be sorted alphabetically."""
    shell_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(shell_data_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            assert node.value.func.id == "Shell"
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            shell_instance_ids.append(instance_id)

    assert shell_instance_ids == sorted(shell_instance_ids)

    # Check all defined shells are referenced in top-level collections.
    all_shell_ids = set(map(str.lower, shell_instance_ids))
    assert all_shell_ids.issubset(ALL_SHELLS.member_ids | {UNKNOWN_SHELL.id})
    assert all_shell_ids.issubset(ALL_TRAITS.member_ids)


def test_shell_detection():
    """Basic shell detection sanity checks."""
    current_shell_result = current_shell()
    assert current_shell_result
    if is_unknown_shell():
        assert current_shell_result is UNKNOWN_SHELL
        assert current_shell_result not in ALL_SHELLS
    else:
        assert current_shell_result is not UNKNOWN_SHELL
        assert current_shell_result in ALL_SHELLS


def test_shell_logical_grouping():
    """All shell groups are subsets of ALL_SHELLS."""
    for group in ALL_SHELL_GROUPS:
        assert group.issubset(ALL_SHELLS)

    # All shells are divided into families.
    assert ALL_SHELLS.fullyintersects(
        BOURNE_SHELLS | C_SHELLS | OTHER_SHELLS | WINDOWS_SHELLS
    )
    assert not ALL_SHELLS.canonical
    assert BOURNE_SHELLS.canonical
    assert C_SHELLS.canonical
    assert OTHER_SHELLS.canonical
    assert WINDOWS_SHELLS.canonical


def test_no_missing_shell_in_groups():
    """Check all shells are attached to at least one non-overlapping group."""
    ALL_SHELLS.fullyintersects(ALL_SHELL_GROUPS & NON_OVERLAPPING_GROUPS)
