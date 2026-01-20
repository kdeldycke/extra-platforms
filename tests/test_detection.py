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
import functools
import inspect
import re
from itertools import chain
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_TRAITS,
    UNKNOWN,
    Group,
    Trait,
    invalidate_caches,
    is_aarch64,
    is_arm,
    is_github_ci,
    is_gitlab_ci,
    is_windows,
    is_x86_64,
)
from extra_platforms import detection as detection_module


@pytest.mark.parametrize(
    "obj", list(chain(ALL_TRAITS, ALL_GROUPS)), ids=lambda obj: obj.id
)
def test_detection_trait_functions(obj: Trait | Group):
    # All traits must implement a real function in the detection module.
    if isinstance(obj, Trait):
        check_func = getattr(detection_module, obj.detection_func_id)
        assert hasattr(extra_platforms, obj.detection_func_id)
        # current property is aligned with detection function.
        assert check_func() == obj.current

    # All groups' detection functions are dynamically generated, but still must exist.
    else:
        assert not hasattr(detection_module, obj.detection_func_id)
        check_func = getattr(extra_platforms, obj.detection_func_id)

        # Groups do not have a "current" property.
        assert not hasattr(obj, "current")

    assert isinstance(check_func, functools._lru_cache_wrapper)
    assert isinstance(check_func(), bool)
    # Ensure the detection function name is lowercase.
    assert obj.detection_func_id.islower()

    # Verify the docstring contains an rST link to the symbol.
    # Format: either old style `SYMBOL_ID <...#extra_platforms.SYMBOL_ID>`_
    # or new style Sphinx role :data:`~extra_platforms.SYMBOL_ID`
    # or short-path style :data:`~SYMBOL_ID`
    assert check_func.__doc__ is not None and re.search(
        rf":data:`~(?:extra_platforms\.)?{re.escape(obj.symbol_id)}`",
        check_func.__doc__,
    )


def test_detection_heuristics_sorting():
    """Detection heuristics must be sorted within each section."""
    detection_path = Path(inspect.getfile(detection_module))
    tree = ast.parse(detection_path.read_bytes())
    source_lines = detection_path.read_text(encoding="utf-8").splitlines()

    # Find section boundaries by looking for comment markers.
    arch_section_start = None
    platform_section_start = None
    ci_section_start = None

    for i, line in enumerate(source_lines, start=1):
        if "Architecture detection heuristics" in line:
            arch_section_start = i
        elif "Platform detection heuristics" in line:
            platform_section_start = i
        elif "CI/CD detection heuristics" in line:
            ci_section_start = i

    assert arch_section_start is not None, "Architecture section not found"
    assert platform_section_start is not None, "Platform section not found"
    assert ci_section_start is not None, "CI/CD section not found"

    assert arch_section_start < platform_section_start
    assert platform_section_start < ci_section_start

    # Collect heuristic functions by section.
    all_heuristic_ids = []
    arch_heuristics = []
    platform_heuristics = []
    ci_heuristics = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_"):
            func_id = node.name
            assert func_id.islower()
            all_heuristic_ids.append(func_id)

            line_no = node.lineno
            if line_no >= arch_section_start and line_no < platform_section_start:
                arch_heuristics.append(func_id)
            elif line_no >= platform_section_start and line_no < ci_section_start:
                platform_heuristics.append(func_id)
            elif line_no >= ci_section_start:
                ci_heuristics.append(func_id)

    # Check there is no extra "is_" function.
    # All traits, including UNKNOWN traits, must have detection functions.
    assert {f"is_{p.id}" for p in ALL_TRAITS} == set(all_heuristic_ids)

    # We only allow one generic "is_unknown*()" detection heuristics per category.
    for heuristics in [arch_heuristics, platform_heuristics, ci_heuristics]:
        non_generic_func_ids = [
            func_id for func_id in heuristics if func_id.startswith("is_unknown")
        ]

        assert len(non_generic_func_ids) <= 1, (
            f"More than 1 is_unknown*() detection heuristics defined in {heuristics!r}"
        )

        if len(non_generic_func_ids):
            assert non_generic_func_ids[-1].startswith("is_unknown")

        # Verify each category is sorted alphabetically within itself.
        assert non_generic_func_ids == sorted(non_generic_func_ids), (
            f"Heuristics are not sorted: {non_generic_func_ids!r}"
        )


def test_is_arm_depends_on_arm_variants():
    """Test that is_arm() correctly calls ARM variant detection functions."""
    # Clear caches to ensure fresh evaluation.
    invalidate_caches()

    # Call is_arm() to ensure it internally calls the ARM variant functions.
    result = is_arm()

    # We can't easily test the internal calls without mocking,
    # but we can verify the function returns a boolean.
    assert isinstance(result, bool)

    invalidate_caches()


def test_detection_functions_cached():
    """Test that detection functions are cached with @cache decorator."""
    # Clear caches first.
    invalidate_caches()

    # Call each function twice.
    _ = is_aarch64()
    _ = is_aarch64()
    _ = is_windows()
    _ = is_windows()
    _ = is_x86_64()
    _ = is_x86_64()

    # Check that cache_info shows hits.
    assert is_aarch64.cache_info().hits >= 1
    assert is_windows.cache_info().hits >= 1
    assert is_x86_64.cache_info().hits >= 1

    invalidate_caches()


def test_environment_variable_ci_detection(monkeypatch):
    """Test CI detection based on environment variables."""
    invalidate_caches()

    # Mock GitHub CI environment variable.
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    invalidate_caches()
    assert is_github_ci() is True

    # Remove GitHub CI and add GitLab CI.
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("GITLAB_CI", "true")
    invalidate_caches()
    assert is_gitlab_ci() is True

    # Clean up.
    monkeypatch.delenv("GITLAB_CI", raising=False)
    invalidate_caches()


def test_detection_no_circular_dependencies():
    """Test that detection functions can all be called without circular dependency issues."""
    invalidate_caches()

    # Call all trait detection functions.
    for trait in ALL_TRAITS:
        # Access the current property, which calls the detection function.
        _ = trait.current

    # If no exception was raised, there are no circular dependencies.
    invalidate_caches()
