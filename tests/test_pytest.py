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

import ast
from itertools import chain
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (  # type: ignore[attr-defined]
    ALL_GROUPS,
    ALL_TRAITS,
    UNKNOWN,
    Group,
    Trait,
    current_traits,
    is_aarch64,
    is_any_agent,
    is_any_architecture,
    is_any_ci,
    is_any_platform,
    is_any_shell,
    is_any_terminal,
    is_any_windows,
    is_bash,
    is_claude_code,
    is_github_ci,
    is_linux,
    is_macos,
    is_powershell,
    is_ubuntu,
    is_unknown_agent,
    is_unknown_architecture,
    is_unknown_ci,
    is_unknown_platform,
    is_unknown_shell,
    is_unknown_terminal,
    is_windows,
    is_x86_64,
)
from extra_platforms.pytest import (
    _DeferredCondition,
    skip_aarch64,
    skip_all_agents,
    skip_all_architectures,
    skip_all_ci,
    skip_all_platforms,
    skip_all_shells,
    skip_all_terminals,
    skip_bash,
    skip_claude_code,
    skip_github_ci,
    skip_linux,
    skip_macos,
    skip_powershell,
    skip_ubuntu,
    skip_unknown,
    skip_unknown_agent,
    skip_unknown_architecture,
    skip_unknown_ci,
    skip_unknown_platform,
    skip_unknown_shell,
    skip_unknown_terminal,
    skip_windows,
    skip_x86_64,
    unless_aarch64,
    unless_any_agent,
    unless_any_architecture,
    unless_any_ci,
    unless_any_platform,
    unless_any_shell,
    unless_any_terminal,
    unless_bash,
    unless_claude_code,
    unless_github_ci,
    unless_linux,
    unless_macos,
    unless_powershell,
    unless_ubuntu,
    unless_unknown,
    unless_unknown_agent,
    unless_unknown_architecture,
    unless_unknown_ci,
    unless_unknown_platform,
    unless_unknown_shell,
    unless_unknown_terminal,
    unless_windows,
    unless_x86_64,
)


def _all_decorator_ids() -> list[str]:
    """Generate the list of decorators IDs we expect to find."""
    all_decorator_ids = []
    for _obj in chain(ALL_TRAITS, ALL_GROUPS):
        assert isinstance(_obj, (Trait, Group))
        all_decorator_ids.extend([_obj.skip_decorator_id, _obj.unless_decorator_id])
    return sorted(all_decorator_ids)


def test_all_definition():
    # Pick the actual list of decorators from the module.
    collected_decorator_ids = [
        name
        for name in dir(extra_platforms.pytest)
        if name.startswith(("skip_", "unless_"))
    ]

    # Ensure we collected them all and they're naturally sorted.
    assert collected_decorator_ids == _all_decorator_ids()


def test_type_annotations():
    """Check all @skip_*/@unless_* annotations are defined and sorted."""
    pytest_file = Path(__file__).parent.parent / "extra_platforms" / "pytest.py"
    tree = ast.parse(pytest_file.read_text(encoding="utf-8"))

    # Collect all annotated assignments in the TYPE_CHECKING block.
    decorator_annotations = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "TYPE_CHECKING"
        ):
            decorator_annotations.extend(
                line.target.id
                for line in node.body
                if isinstance(line, ast.AnnAssign)
                and isinstance(line.target, ast.Name)
                and line.target.id.startswith(("skip_", "unless_"))
            )

    assert len(decorator_annotations), "No @skip_*/@unless_* annotations found."
    assert decorator_annotations == sorted(decorator_annotations), (
        "@skip_*/@unless_* annotations not sorted alphabetically."
    )

    expected_annotations = _all_decorator_ids()
    assert decorator_annotations == expected_annotations, (
        f"@skip_*/@unless_* annotations don't match expectations:\n"
        f"- Missing: {set(expected_annotations) - set(decorator_annotations)}\n"
        f"- Extra: {set(decorator_annotations) - set(expected_annotations)}"
    )


@skip_unknown
def test_skip_unknown():
    assert not current_traits().intersection(UNKNOWN)


@unless_unknown
def test_unless_unknown():
    assert current_traits().intersection(UNKNOWN)


@skip_all_architectures
def test_skip_all_architectures():
    assert is_unknown_architecture()
    assert False, (
        "This test should always be skipped as we expect to always detect "
        "an architecture."
    )


@unless_any_architecture
def test_unless_any_architecture():
    assert not is_unknown_architecture()
    assert True, (
        "This test should always be run as we expect to always detect an architecture."
    )


@skip_all_platforms
def test_skip_all_platforms():
    assert is_unknown_platform()
    assert False, (
        "This test should always be skipped as we expect to always detect a platform."
    )


@unless_any_platform
def test_unless_any_platform():
    assert not is_unknown_platform()
    assert True, (
        "This test should always be run as we expect to always detect a platform."
    )


@skip_all_shells
def test_skip_all_shells():
    assert is_unknown_shell()
    assert False, (
        "This test should always be skipped as we expect to always detect a shell."
    )


@unless_any_shell
def test_unless_any_shell():
    assert not is_unknown_shell()
    assert True, "This test should always be run as we expect to always detect a shell."


@skip_all_terminals
def test_skip_all_terminals():
    assert is_unknown_terminal()


@unless_any_terminal
def test_unless_any_terminal():
    assert not is_unknown_terminal()


@skip_all_ci
def test_skip_all_ci():
    assert is_unknown_ci()


@unless_any_ci
def test_unless_any_ci():
    assert not is_unknown_ci()


@skip_all_agents
def test_skip_all_agents():
    assert is_unknown_agent()


@unless_any_agent
def test_unless_any_agent():
    assert not is_unknown_agent()


@skip_unknown_architecture
def test_skip_unknown_architecture():
    assert is_any_architecture()
    assert not is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@unless_unknown_architecture
def test_unless_unknown_architecture():
    assert not is_any_architecture()
    assert is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@skip_unknown_platform
def test_skip_unknown_platform():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform()
    assert not is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@unless_unknown_platform
def test_unless_unknown_platform():
    assert is_any_architecture() or is_unknown_architecture()

    assert not is_any_platform()
    assert is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@skip_unknown_shell
def test_skip_unknown_shell():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell()
    assert not is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@unless_unknown_shell
def test_unless_unknown_shell():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert not is_any_shell()
    assert is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@skip_unknown_terminal
def test_skip_unknown_terminal():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal()
    assert not is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@unless_unknown_terminal
def test_unless_unknown_terminal():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert not is_any_terminal()
    assert is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@skip_unknown_ci
def test_skip_unknown_ci():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci()
    assert not is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@unless_unknown_ci
def test_unless_unknown_ci():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert not is_any_ci()
    assert is_unknown_ci()

    assert is_any_agent() or is_unknown_agent()


@skip_unknown_agent
def test_skip_unknown_agent():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert is_any_agent()
    assert not is_unknown_agent()


@unless_unknown_agent
def test_unless_unknown_agent():
    assert is_any_architecture() or is_unknown_architecture()

    assert is_any_platform() or is_unknown_platform()

    assert is_any_shell() or is_unknown_shell()

    assert is_any_terminal() or is_unknown_terminal()

    assert is_any_ci() or is_unknown_ci()

    assert not is_any_agent()
    assert is_unknown_agent()


@skip_aarch64
def test_skip_aarch64():
    assert is_any_architecture()
    assert not is_aarch64()


@unless_aarch64
def test_unless_aarch64():
    assert is_any_architecture()
    assert is_aarch64()


@skip_x86_64
def test_skip_x86_64():
    assert is_any_architecture()
    assert not is_x86_64()


@unless_x86_64
def test_unless_x86_64():
    assert is_any_architecture()
    assert is_x86_64()


@skip_linux
def test_skip_linux():
    assert is_any_platform()
    assert not is_linux()
    assert not is_ubuntu()
    assert is_any_windows() or is_macos() or is_windows()


@unless_linux
def test_unless_linux():
    assert is_any_platform()
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    # assert is_ubuntu()
    assert not is_windows()


@skip_macos
def test_skip_macos():
    assert is_any_platform()
    assert not is_macos()
    assert is_any_windows() or is_linux() or is_ubuntu() or is_windows()


@unless_macos
def test_unless_macos():
    assert is_any_platform()
    assert not is_any_windows()
    assert not is_linux()
    assert is_macos()
    assert not is_ubuntu()
    assert not is_windows()


@skip_ubuntu
def test_skip_ubuntu():
    assert is_any_platform()
    assert not is_ubuntu()
    assert is_any_windows() or is_linux() or is_macos() or is_windows()


@unless_ubuntu
def test_unless_ubuntu():
    assert is_any_platform()
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    assert is_ubuntu()
    assert not is_windows()


@skip_windows
def test_skip_windows():
    assert is_any_platform()
    assert not is_windows()
    assert not is_any_windows()
    assert is_linux() or is_macos() or is_ubuntu()


@unless_windows
def test_unless_windows():
    assert is_any_platform()
    # assert is_any_windows()
    assert not is_linux()
    assert not is_macos()
    assert not is_ubuntu()
    assert is_windows()


@skip_bash
def test_skip_bash():
    assert is_any_shell()
    assert not is_bash()


@unless_bash
def test_unless_bash():
    assert is_any_shell()
    assert is_bash()


@skip_powershell
def test_skip_powershell():
    assert is_any_shell()
    assert not is_powershell()


@unless_powershell
def test_unless_powershell():
    assert is_any_shell()
    assert is_powershell()


@skip_github_ci
def test_skip_github_ci():
    assert is_any_ci() or is_unknown_ci()
    assert not is_github_ci()


@unless_github_ci
def test_unless_github_ci():
    assert is_any_ci()
    assert not is_unknown_ci()
    assert is_github_ci()


@skip_claude_code
def test_skip_claude_code():
    assert is_any_agent() or is_unknown_agent()
    assert not is_claude_code()


@unless_claude_code
def test_unless_claude_code():
    assert is_any_agent()
    assert not is_unknown_agent()
    assert is_claude_code()


def test_deferred_condition_defers_evaluation():
    """Test that _DeferredCondition defers evaluation until needed."""
    # Track whether the condition was called.
    called = []

    def condition():
        called.append(True)
        return True

    # Creating the _DeferredCondition should NOT call the condition.
    deferred = _DeferredCondition(condition)
    assert len(called) == 0

    # Only when we evaluate it as a bool should it call the condition.
    result = bool(deferred)
    assert len(called) == 1
    assert result is True


def test_deferred_condition_bool():
    """Test that _DeferredCondition.__bool__() calls the condition."""

    def true_condition():
        return True

    def false_condition():
        return False

    assert bool(_DeferredCondition(true_condition)) is True
    assert bool(_DeferredCondition(false_condition)) is False


def test_deferred_condition_call():
    """Test that _DeferredCondition.__call__() works."""

    def true_condition():
        return True

    deferred = _DeferredCondition(true_condition)
    result = deferred()
    assert result is True


def test_deferred_condition_invert_false():
    """Test that _DeferredCondition with invert=False returns the condition result."""

    def true_condition():
        return True

    def false_condition():
        return False

    assert bool(_DeferredCondition(true_condition, invert=False)) is True
    assert bool(_DeferredCondition(false_condition, invert=False)) is False


def test_deferred_condition_invert_true():
    """Test that _DeferredCondition with invert=True inverts the condition result."""
    from extra_platforms.pytest import _DeferredCondition

    def true_condition():
        return True

    def false_condition():
        return False

    assert bool(_DeferredCondition(true_condition, invert=True)) is False
    assert bool(_DeferredCondition(false_condition, invert=True)) is True


def test_deferred_condition_with_pytest_skipif():
    """Test that _DeferredCondition works with pytest.mark.skipif."""

    # Create a condition that always returns True.
    def always_skip():
        return True

    condition = _DeferredCondition(always_skip)

    # Create a skipif mark.
    mark = pytest.mark.skipif(condition, reason="Testing deferred condition")

    # The mark should have the condition.
    assert mark is not None
    # We can't easily test if the skip actually happens without running pytest,
    # but we can verify the condition evaluates correctly.
    assert bool(condition) is True
