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
import tomllib
from pathlib import Path

import requests

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_PLATFORMS,
    GITHUB_CI,
    UNKNOWN_CI,
    UNKNOWN_LINUX,
    WSL1,
    WSL2,
    current_os,
    current_platforms,
    invalidate_caches,
    is_github_ci,
    is_macos,
    is_ubuntu,
    is_windows,
)
from extra_platforms import detection as detection_module
from extra_platforms import group as group_module
from extra_platforms import group_data as group_data_module
from extra_platforms import operations as operations_module
from extra_platforms import platform as platform_module
from extra_platforms import platform_data as platform_data_module

PROJECT_ROOT = Path(__file__).parent.parent
"""The root path of the project."""

PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
"""The path to the ``pyproject.toml`` file."""

PYPROJECT = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
"""The parsed content of the ``pyproject.toml`` file."""


def test_pyproject_keywords():
    """Check that keywords in ``pyproject.toml`` are correct."""
    # Build our ideal keywords list.
    ideal_keywords = [
        p.name
        for p in (
            ALL_PLATFORMS
            # Remove generic unknown platforms.
            - UNKNOWN_LINUX
            - UNKNOWN_CI
            # Remove versioned WSL platforms.
            - WSL1
            - WSL2
        )
    ]
    # Re-add un-versioned platform names.
    ideal_keywords.append("Windows Subsystem for Linux")
    # Manually add group names that are not platforms per se.
    ideal_keywords.extend((
        "Unix",
        "AT&T System Five",
    ))
    # Manually add extra keywords.
    ideal_keywords.extend((
        "multiplatform",
        "Pytest",
        "OS detection",
        "Platform detection",
    ))
    # Sort and deduplicate keywords (case-insensitive).
    ideal_keywords = sorted(set(ideal_keywords), key=lambda k: k.lower())

    # Load our keywords from pyproject.toml.
    keywords = PYPROJECT["project"]["keywords"]

    assert keywords == ideal_keywords


def test_pypoject_classifiers():
    """Check that Trove classifiers in ``pyproject.toml`` are correct."""
    # Fetch official trove classifiers from PyPI.
    response = requests.get("https://pypi.org/pypi?%3Aaction=list_classifiers")
    assert response.ok, f"{response.url} is not reachable: {response}"
    official_classifiers = response.text.splitlines()

    # Load our trove classifiers from pyproject.toml.
    classifiers = PYPROJECT["project"]["classifiers"]

    for classifier in classifiers:
        assert classifier in official_classifiers, (
            f"Classifier '{classifier}' is not an official trove classifier."
        )

    assert len(classifiers) == len(set(classifiers)), (
        "Classifiers must not contain duplicates."
    )

    sorted_classifiers = [c for c in official_classifiers if c in classifiers]
    assert sorted_classifiers == classifiers, (
        "Classifiers must be sorted in the same order as official trove classifiers."
    )

    os_classifiers = [
        c for c in official_classifiers if c.startswith("Operating System :: ")
    ]
    assert set(c for c in classifiers if c.startswith("Operating System :: ")) == set(
        os_classifiers
    ), "All Operating System classifiers must be present in our metadata."


def test_module_root_declarations():
    def fetch_module_implements(module) -> set[str]:
        """Fetch all methods, classes and constants implemented locally in a module's file."""
        members = set()
        tree = ast.parse(Path(inspect.getfile(module)).read_bytes())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    # Skip TYPE_CHECKING variable. See _types.py for more details.
                    if target.id == "TYPE_CHECKING":  # type: ignore[attr-defined]
                        continue
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
    operations_members = fetch_module_implements(operations_module)
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
    assert operations_members <= set(extra_platforms_members)

    expected_members = sorted(
        detection_members.union(group_members)
        .union(group_data_members)
        .union(platform_members)
        .union(platform_data_members)
        .union(operations_members)
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


def test_current_funcs():
    current_platforms_results = current_platforms()
    assert ALL_PLATFORMS.issuperset(current_platforms_results)
    if is_github_ci():
        assert len(current_platforms_results) == 2
        assert GITHUB_CI in current_platforms_results
    else:
        assert len(current_platforms_results) == 1

    current_os_result = current_os()
    assert current_os_result in ALL_PLATFORMS
    assert current_os_result in current_platforms_results


def test_group_membership_funcs():
    for group in ALL_GROUPS:
        func_id = f"is_{group.id}"
        assert func_id in extra_platforms.__dict__

        func = extra_platforms.__dict__[func_id]
        assert getattr(extra_platforms, func_id) is func

        assert isinstance(func(), bool)
        assert func() == (current_os() in group)

        assert group.name.lower() in func.__doc__.lower()


def test_invalidate_caches():
    """Test that invalidate_caches() properly clears all caches."""

    # Call detection functions to populate caches.
    _ = is_ubuntu()
    _ = is_macos()
    # Call global functions.
    _ = current_platforms()
    _ = current_os()
    # Call group membership functions.
    _ = is_windows()

    # Verify caches are populated.
    assert hasattr(is_ubuntu, "__wrapped__")
    assert hasattr(is_macos, "__wrapped__")
    assert hasattr(current_platforms, "__wrapped__")
    assert hasattr(current_os, "__wrapped__")
    assert hasattr(is_windows, "__wrapped__")

    # Access Platform.current to populate their caches.
    for platform_obj in ALL_PLATFORMS.platforms:
        _ = platform_obj.current
        # For cached_property, the value is stored in the instance's __dict__.
        assert "current" in vars(platform_obj), (
            f"'current' not cached for {platform_obj.id}"
        )

    # Check that caches have hits (values are cached).
    assert is_ubuntu.cache_info().hits > 0 or is_ubuntu.cache_info().currsize > 0
    assert is_macos.cache_info().hits > 0 or is_macos.cache_info().currsize > 0
    assert (
        current_platforms.cache_info().hits > 0
        or current_platforms.cache_info().currsize > 0
    )
    assert current_os.cache_info().hits > 0 or current_os.cache_info().currsize > 0
    assert is_windows.cache_info().hits > 0 or is_windows.cache_info().currsize > 0

    # Invalidate all caches.
    invalidate_caches()

    # Verify caches were cleared (currsize should be 0).
    assert is_ubuntu.cache_info().currsize == 0
    assert is_macos.cache_info().currsize == 0
    assert current_platforms.cache_info().currsize == 0
    assert current_os.cache_info().currsize == 0
    assert is_windows.cache_info().currsize == 0

    for platform_obj in ALL_PLATFORMS.platforms:
        assert "current" not in vars(platform_obj), (
            f"'current' cache not cleared for {platform_obj.id}"
        )
