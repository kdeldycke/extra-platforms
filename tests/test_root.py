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
import sys
from pathlib import Path

import pytest
import requests

import extra_platforms
from extra_platforms import (
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_GROUPS,
    ALL_PLATFORMS,
    ALL_TRAITS,
    SYSTEM_V,
    UNIX,
    UNKNOWN,
    UNKNOWN_ARCHITECTURE,
    UNKNOWN_CI,
    UNKNOWN_PLATFORM,
    WSL1,
    WSL2,
    current_architecture,
    current_ci,
    current_platform,
    current_traits,
    invalidate_caches,
    is_github_ci,
    is_macos,
    is_ubuntu,
    is_windows,
)
from extra_platforms import _deprecated as deprecated_module
from extra_platforms import architecture_data as architecture_data_module
from extra_platforms import ci_data as ci_data_module
from extra_platforms import detection as detection_module
from extra_platforms import group as group_module
from extra_platforms import group_data as group_data_module
from extra_platforms import operations as operations_module
from extra_platforms import platform_data as platform_data_module
from extra_platforms import trait as trait_module

from .test_ci_data import github_runner_os

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]


PROJECT_ROOT = Path(__file__).parent.parent
"""The root path of the project."""

PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
"""The path to the ``pyproject.toml`` file."""

PYPROJECT = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
"""The parsed content of the ``pyproject.toml`` file."""


def test_pyproject_keywords():
    """Check that keywords in ``pyproject.toml`` are correct."""
    # Add all platforms and architectures.
    ideal_keywords = [
        p.name
        for p in (
            ALL_TRAITS
            # Remove versioned WSL platforms.
            - WSL1
            - WSL2
            # Remove UNKNOWN_* traits.
            - UNKNOWN
        )
    ]
    # Re-add un-versioned platform names.
    ideal_keywords.append("Windows Subsystem for Linux")
    # Manually add group names that are not platforms per se.
    ideal_keywords.extend((
        UNIX.name.lstrip("Any "),
        SYSTEM_V.name,
    ))
    # Manually add extra keywords.
    ideal_keywords.extend((
        "multiplatform",
        "Pytest",
        "OS detection",
        "Platform detection",
        "Architecture detection",
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
                    # Skip subscript targets like sys.modules["..."] = ...
                    if not isinstance(target, ast.Name):
                        continue
                    # Skip TYPE_CHECKING variable. See _types.py for more details.
                    if target.id == "TYPE_CHECKING":
                        continue
                    members.add(target.id)
            elif isinstance(node, ast.AnnAssign):
                members.add(node.target.id)  # type: ignore[union-attr]
            elif isinstance(node, ast.FunctionDef):
                members.add(node.name)
            elif isinstance(node, ast.ClassDef):
                members.add(node.name)
        return {m for m in members if not m.startswith("_")}

    detection_members = fetch_module_implements(detection_module)
    architecture_data_members = fetch_module_implements(architecture_data_module)
    ci_data_members = fetch_module_implements(ci_data_module)
    group_members = fetch_module_implements(group_module)
    group_data_members = fetch_module_implements(group_data_module)
    platform_data_members = fetch_module_implements(platform_data_module)
    operations_members = fetch_module_implements(operations_module)
    trait_members = fetch_module_implements(trait_module)
    deprecated_members = fetch_module_implements(deprecated_module)
    root_members = fetch_module_implements(extra_platforms)
    # Update root members with auto-generated group detection function names.
    root_members.update((g.detection_func_id for g in ALL_GROUPS))

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
    assert architecture_data_members <= set(extra_platforms_members)
    assert ci_data_members <= set(extra_platforms_members)
    assert group_members <= set(extra_platforms_members)
    assert group_data_members <= set(extra_platforms_members)
    assert platform_data_members <= set(extra_platforms_members)
    assert operations_members <= set(extra_platforms_members)
    assert trait_members <= set(extra_platforms_members)
    assert deprecated_members <= set(extra_platforms_members)

    expected_members = sorted(
        detection_members
        .union(group_members)
        .union(architecture_data_members)
        .union(ci_data_members)
        .union(group_data_members)
        .union(platform_data_members)
        .union(operations_members)
        .union(trait_members)
        .union(deprecated_members)
        .union(root_members),
        key=lambda m: (m.lower(), m),
    )
    assert expected_members == extra_platforms_members


def test_current_funcs():
    current_traits_results = current_traits()
    assert ALL_TRAITS.issuperset(current_traits_results)

    # 1 platform + 1 architecture = 2 traits.
    detected_traits = 2
    if is_github_ci():
        if github_runner_os() == "ubuntu-slim":
            # 1 platform + 2 architectures (Ubuntu + WSL) + 1 CI = 4 traits.
            detected_traits = 4
        else:
            # 1 platform + 1 architecture + 1 CI = 3 traits.
            detected_traits = 3
    assert len(current_traits_results) == detected_traits

    current_architecture_result = current_architecture()
    assert current_architecture_result in ALL_ARCHITECTURES
    assert current_architecture_result in current_traits_results
    assert current_architecture_result is not UNKNOWN_ARCHITECTURE

    current_platform_result = current_platform()
    assert current_platform_result in ALL_PLATFORMS
    assert current_platform_result in current_traits_results
    assert current_platform_result is not UNKNOWN_PLATFORM

    current_ci_result = current_ci()
    assert current_ci_result in ALL_CI | {UNKNOWN_CI}
    if current_ci_result is not UNKNOWN_CI:
        assert current_ci_result in current_traits_results


def test_current_architecture_strict(monkeypatch):
    """Test that ``current_architecture(strict=True)`` raises an error when unrecognized."""
    # First verify that without mocking, current_architecture works normally.
    invalidate_caches()
    arch = current_architecture()
    assert arch in ALL_ARCHITECTURES
    assert arch is not UNKNOWN_ARCHITECTURE

    # Now mock all architectures to not match.
    invalidate_caches()
    for arch in ALL_ARCHITECTURES:
        monkeypatch.setattr(type(arch), "current", property(lambda self: False))

    # Without strict mode, we get UNKNOWN_ARCHITECTURE.
    result = current_architecture(strict=False)
    assert result is UNKNOWN_ARCHITECTURE

    # With strict mode, we get a SystemError.
    invalidate_caches()
    with pytest.raises(SystemError, match="Unrecognized architecture"):
        current_architecture(strict=True)

    # Cleanup: restore the original property.
    invalidate_caches()


def test_current_platform_strict(monkeypatch):
    """Test that ``current_platform(strict=True)`` raises an error when unrecognized."""
    # First verify that without mocking, current_platform works normally.
    invalidate_caches()
    platform = current_platform()
    assert platform in ALL_PLATFORMS
    assert platform is not UNKNOWN_PLATFORM

    # Now mock all platforms to not match.
    invalidate_caches()
    for platform in ALL_PLATFORMS:
        monkeypatch.setattr(type(platform), "current", property(lambda self: False))

    # Without strict mode, we get UNKNOWN_PLATFORM.
    result = current_platform(strict=False)
    assert result is UNKNOWN_PLATFORM

    # With strict mode, we get a SystemError.
    invalidate_caches()
    with pytest.raises(SystemError, match="Unrecognized platform"):
        current_platform(strict=True)

    # Cleanup: restore the original property.
    invalidate_caches()


def test_current_ci_strict(monkeypatch):
    """Test that ``current_ci(strict=True)`` raises an error when unrecognized."""
    # Now mock all CI systems to not match.
    invalidate_caches()
    for ci in ALL_CI:
        monkeypatch.setattr(type(ci), "current", property(lambda self: False))

    # Without strict mode, we get UNKNOWN_CI.
    result = current_ci(strict=False)
    assert result is UNKNOWN_CI

    # With strict mode, we get a SystemError.
    invalidate_caches()
    with pytest.raises(SystemError, match="Unrecognized CI"):
        current_ci(strict=True)

    # Cleanup: restore the original property.
    invalidate_caches()


def test_group_membership_funcs():
    for group in ALL_GROUPS:
        assert group.detection_func_id in extra_platforms.__dict__

        func = extra_platforms.__dict__[group.detection_func_id]
        assert getattr(extra_platforms, group.detection_func_id) is func

        assert isinstance(func(), bool)
        assert func() == any(t in group for t in current_traits())

        assert group.name.lower() in func.__doc__.lower()


def test_invalidate_caches():
    """Test that invalidate_caches() properly clears all caches."""

    # Call detection functions to populate caches.
    _ = is_ubuntu()
    _ = is_macos()
    # Call global functions.
    _ = current_traits()
    _ = current_platform()
    # Call group membership functions.
    _ = is_windows()

    # Verify caches are populated.
    assert hasattr(is_ubuntu, "__wrapped__")
    assert hasattr(is_macos, "__wrapped__")
    assert hasattr(current_traits, "__wrapped__")
    assert hasattr(current_platform, "__wrapped__")
    assert hasattr(is_windows, "__wrapped__")

    # Access Platform.current to populate their caches.
    for platform_obj in ALL_PLATFORMS:
        _ = platform_obj.current
        # For cached_property, the value is stored in the instance's __dict__.
        assert "current" in vars(platform_obj), (
            f"'current' not cached for {platform_obj.id}"
        )

    # Check that caches have hits (values are cached).
    assert is_ubuntu.cache_info().hits > 0 or is_ubuntu.cache_info().currsize > 0
    assert is_macos.cache_info().hits > 0 or is_macos.cache_info().currsize > 0
    assert (
        current_traits.cache_info().hits > 0 or current_traits.cache_info().currsize > 0
    )
    assert (
        current_platform.cache_info().hits > 0
        or current_platform.cache_info().currsize > 0
    )
    assert is_windows.cache_info().hits > 0 or is_windows.cache_info().currsize > 0

    # Invalidate all caches.
    invalidate_caches()

    # Verify caches were cleared (currsize should be 0).
    assert is_ubuntu.cache_info().currsize == 0
    assert is_macos.cache_info().currsize == 0
    assert current_traits.cache_info().currsize == 0
    assert current_platform.cache_info().currsize == 0
    assert is_windows.cache_info().currsize == 0

    for platform_obj in ALL_PLATFORMS:
        assert "current" not in vars(platform_obj), (
            f"'current' cache not cleared for {platform_obj.id}"
        )
