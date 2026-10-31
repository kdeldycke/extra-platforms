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
import subprocess
from itertools import chain
from operator import attrgetter
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_TRAITS,
    Group,
    Trait,
    is_unknown_architecture,
)
from extra_platforms.pytest import (
    _DeferredCondition,
    skip_all_architectures,
    unless_any_architecture,
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
    tree = ast.parse(pytest_file.read_text(encoding="UTF-8"))

    # Collect all annotated assignments in the TYPE_CHECKING block.
    decorator_annotations: list[str] = []
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


@pytest.mark.parametrize(
    "obj",
    sorted(chain(ALL_TRAITS, ALL_GROUPS), key=attrgetter("id")),
    ids=attrgetter("id"),
)
def test_generated_decorators(obj):
    """Each trait and group gets a skip and an unless decorator.

    Both read the detection function of their object, with opposite outcomes.
    """
    detected = getattr(extra_platforms, obj.detection_func_id)()
    symbol_link = f"{{data}}`~extra_platforms.{obj.symbol_id}`"
    for decorator_id, reason_prefix, doc_prefix, skips in (
        (obj.skip_decorator_id, "Skip", "Skip test if", detected),
        (obj.unless_decorator_id, "Requires", "Run test only if", not detected),
    ):
        decorator = getattr(extra_platforms.pytest, decorator_id)
        assert isinstance(decorator, pytest.MarkDecorator)
        assert decorator.mark.name == "skipif"
        assert bool(decorator.mark.args[0]) is skips
        assert decorator.mark.kwargs["reason"] == f"{reason_prefix} {obj.name}"
        assert decorator.__doc__ is not None
        assert decorator.__doc__.startswith(doc_prefix)
        assert symbol_link in decorator.__doc__


@skip_all_architectures
def test_skip_all_architectures():
    """A skip decorator keeps the test from running at all."""
    assert is_unknown_architecture()
    assert False, (
        "This test should always be skipped as we expect to always detect "
        "an architecture."
    )


@unless_any_architecture
def test_unless_any_architecture():
    """An unless decorator lets the test run."""
    assert not is_unknown_architecture()


@pytest.mark.parametrize(
    ("result", "invert", "expected"),
    (
        (True, False, True),
        (False, False, False),
        (True, True, False),
        (False, True, True),
    ),
)
def test_deferred_condition(result, invert, expected):
    """The condition runs only when its value is read, inverted on request."""
    calls: list[None] = []

    def condition():
        calls.append(None)
        return result

    deferred = _DeferredCondition(condition, invert=invert)
    assert not calls
    assert bool(deferred) is expected
    assert deferred() is expected
    assert len(calls) == 2


def test_write_fake_executable(tmp_path):
    """The fake executable runs under a Python shebang and honors its outputs."""
    fake = extra_platforms.pytest.write_fake_executable(
        tmp_path / "fake",
        stdout="out\n",
        stderr="err\n",
        returncode=3,
    )
    result = subprocess.run(
        [str(fake), "--ignored-argument"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "out\n"
    assert result.stderr == "err\n"
    assert result.returncode == 3
