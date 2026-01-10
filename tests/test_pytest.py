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
from itertools import chain
from pathlib import Path

import extra_platforms
from extra_platforms import (  # type: ignore[attr-defined]
    ALL_GROUPS,
    ALL_TRAITS,
    UNKNOWN,
    Group,
    Trait,
    is_any_windows,
    is_linux,
    is_macos,
    is_ubuntu,
    is_windows,
)
from extra_platforms.pytest import (
    skip_all_architectures,
    skip_all_platforms,
    skip_linux,
    skip_macos,
    skip_ubuntu,
    skip_windows,
    unless_all_architectures,
    unless_all_platforms,
    unless_linux,
    unless_macos,
    unless_ubuntu,
    unless_windows,
)


def _all_decorator_ids() -> list[str]:
    "Generate the list of decorators IDs we expect to find."
    all_decorator_ids = []
    for _obj in chain(ALL_TRAITS, UNKNOWN, ALL_GROUPS):
        assert isinstance(_obj, (Trait, Group))
        skip_id = f"skip_{_obj.id}"
        unless_id = f"unless_{_obj.id}"
        all_decorator_ids.extend([skip_id, unless_id])
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
    tree = ast.parse(pytest_file.read_text())

    # Collect all annotated assignments in the TYPE_CHECKING block.
    decorator_annotations = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "TYPE_CHECKING"
        ):
            for line in node.body:
                if (
                    isinstance(line, ast.AnnAssign)
                    and isinstance(line.target, ast.Name)
                    and line.target.id.startswith(("skip_", "unless_"))
                ):
                    decorator_annotations.append(line.target.id)

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


@skip_all_architectures
def test_skip_all_architectures():
    assert False, "This test should be skipped on all architectures."


@skip_all_platforms
def test_skip_all_platforms():
    assert False, "This test should be skipped on all platforms."


@unless_all_architectures
def test_unless_all_architectures():
    assert True, "This test should be run on all architectures."


@unless_all_platforms
def test_unless_all_platforms():
    assert True, "This test should be run on all platforms."


@skip_linux
def test_skip_linux():
    assert not is_linux()
    assert not is_ubuntu()
    assert is_any_windows() or is_macos() or is_windows()


@skip_macos
def test_skip_macos():
    assert not is_macos()
    assert is_any_windows() or is_linux() or is_ubuntu() or is_windows()


@skip_ubuntu
def test_skip_ubuntu():
    assert not is_ubuntu()
    assert is_any_windows() or is_linux() or is_macos() or is_windows()


@skip_windows
def test_skip_windows():
    assert not is_windows()
    assert not is_any_windows()
    assert is_linux() or is_macos() or is_ubuntu()


@unless_linux
def test_unless_linux():
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    # assert is_ubuntu()
    assert not is_windows()


@unless_macos
def test_unless_macos():
    assert not is_any_windows()
    assert not is_linux()
    assert is_macos()
    assert not is_ubuntu()
    assert not is_windows()


@unless_ubuntu
def test_unless_ubuntu():
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    assert is_ubuntu()
    assert not is_windows()


@unless_windows
def test_unless_windows():
    # assert is_any_windows()
    assert not is_linux()
    assert not is_macos()
    assert not is_ubuntu()
    assert is_windows()
