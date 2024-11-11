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
from pathlib import Path

import extra_platforms
from extra_platforms import ALL_GROUPS, ALL_PLATFORMS, current_os
from extra_platforms import detection as detection_module
from extra_platforms import group as group_module
from extra_platforms import group_data as group_data_module
from extra_platforms import platform as platform_module
from extra_platforms import platform_data as platform_data_module


def test_module_root_declarations():
    def fetch_module_implements(module) -> set[str]:
        """Fetch all methods, classes and constants implemented locally in a module's file."""
        members = set()
        tree = ast.parse(Path(inspect.getfile(module)).read_bytes())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    members.add(target.id)  # type: ignore[attr-defined]
            elif isinstance(node, ast.AnnAssign):
                members.add(node.target.id)  # type: ignore[union-attr]
            elif isinstance(node, ast.FunctionDef):
                members.add(node.name)
            elif isinstance(node, ast.ClassDef):
                members.add(node.name)
        return {m for m in members if not m.startswith("_")}

    detection_members = fetch_module_implements(detection_module)
    group_members = fetch_module_implements(group_module)
    group_data_members = fetch_module_implements(group_data_module)
    platform_members = fetch_module_implements(platform_module)
    platform_data_members = fetch_module_implements(platform_data_module)
    root_members = fetch_module_implements(extra_platforms)
    # Update root members with auto-generated ``is_<group.id>`` variables.
    root_members.update((f"is_{g.id}" for g in ALL_GROUPS))

    # Check all members are exposed at the module root.
    tree = ast.parse(Path(inspect.getfile(extra_platforms)).read_bytes())
    extra_platforms_members = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if target.id == "__all__":
                    for element in node.value.elts:
                        extra_platforms_members.append(element.value)

    assert detection_members <= set(extra_platforms_members)
    assert group_members <= set(extra_platforms_members)
    assert group_data_members <= set(extra_platforms_members)
    assert platform_members <= set(extra_platforms_members)
    assert platform_data_members <= set(extra_platforms_members)

    expected_members = sorted(
        detection_members.union(group_members)
        .union(group_data_members)
        .union(platform_members)
        .union(platform_data_members)
        .union(root_members),
        key=lambda m: (m.lower(), m),
    )
    assert expected_members == extra_platforms_members


def test_code_sorting():
    """Implementation must have all its methods and objects sorted."""
    heuristic_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(detection_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_"):
            func_id = node.name
            assert func_id.islower()
            heuristic_instance_ids.append(func_id)

    platform_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(platform_data_module)).read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and node.value.func.id == "Platform"
        ):
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            platform_instance_ids.append(instance_id)

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

    # Check there is no extra "is_" function.
    assert {f"is_{p.id}" for p in ALL_PLATFORMS.platforms} == set(
        heuristic_instance_ids
    )

    assert heuristic_instance_ids == sorted(heuristic_instance_ids)
    assert platform_instance_ids == sorted(platform_instance_ids)
    # XXX Group order is logical, not alphabetical.
    # assert group_instance_ids == sorted(group_instance_ids)


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

    assert all_group_ids.isdisjoint(all_platform_ids)


def test_current_os_func():
    # Function.
    current_platform = current_os()
    assert current_platform in ALL_PLATFORMS.platforms
