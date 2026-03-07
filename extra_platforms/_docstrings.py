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
"""Utilities for generating runtime docstrings for traits and groups.

This module provides functions to extract attribute docstrings from source
files and generate comprehensive documentation for trait and group instances.

The :func:`_initialize_all_docstrings` function should be called from
``__init__.py`` after all trait and group instances are imported to populate
their ``__doc__`` attributes.

.. note::
    AST parse results are cached per module to avoid redundant work. Without
    caching, each of the ~170 trait/group instances triggers a full
    ``ast.parse()`` of its source module, totaling ~300 parses at import time
    (~115 ms). With per-module caching this drops to ~7 parses (~2.5 ms),
    reducing ``import extra_platforms`` from ~120 ms to ~10 ms.
"""

from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from . import Group, Trait

# Per-module cache of attribute name to docstring. Populated lazily by
# ``_parse_module_docstrings`` on first access to a given module.
_module_docstrings_cache: dict[str, dict[str, str]] = {}


def _parse_module_docstrings(module_name: str) -> dict[str, str]:
    """Parse a module's source and return all attribute docstrings at once.

    Attribute docstrings are string literals that immediately follow an
    assignment statement at module level.

    :param module_name: The full module name (e.g.,
        'extra_platforms.platform_data').
    :returns: A mapping of attribute names to their docstrings. Empty dict if
        the source is unavailable.
    """
    module = importlib.import_module(module_name)
    source_file = inspect.getsourcefile(module)
    if not source_file:
        # Source file not available (e.g., compiled module).
        return {}

    try:
        source = Path(source_file).read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        # Source file doesn't exist on disk (e.g., Nuitka-compiled binary).
        return {}

    tree = ast.parse(source)

    docstrings: dict[str, str] = {}
    body = tree.body

    # Walk all top-level statements, looking for assignments followed by a
    # string literal (the attribute docstring convention).
    for i, node in enumerate(body):
        names: list[str] = []

        if isinstance(node, ast.Assign):
            names.extend(
                target.id for target in node.targets if isinstance(target, ast.Name)
            )
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            # Handle annotated assignments like: x: type = value.
            names.append(node.target.id)

        if not names:
            continue

        # Check if the next statement is a string expression.
        if i + 1 < len(body):
            next_node = body[i + 1]
            if (
                isinstance(next_node, ast.Expr)
                and isinstance(next_node.value, ast.Constant)
                and isinstance(next_node.value.value, str)
            ):
                for name in names:
                    docstrings[name] = next_node.value.value

    return docstrings


def get_attribute_docstring(module_name: str, attr_name: str) -> str | None:
    """Extract attribute docstring from a module's source file.

    Attribute docstrings are string literals that immediately follow an
    assignment. Results are cached per module so each source file is parsed
    only once regardless of how many attributes are looked up.

    .. note::
        Returns ``None`` if source files are unavailable, which happens in
        compiled environments (e.g., Nuitka, PyInstaller, cx_Freeze). This
        graceful degradation allows the library to function without docstrings
        in compiled binaries.

    :param module_name: The full module name (e.g.,
        'extra_platforms.platform_data').
    :param attr_name: The attribute name to look for (e.g., 'NOBARA').
    :returns: The attribute docstring if found, or ``None`` if not found or
        source is unavailable.
    """
    if module_name not in _module_docstrings_cache:
        _module_docstrings_cache[module_name] = _parse_module_docstrings(module_name)
    return _module_docstrings_cache[module_name].get(attr_name)


def _initialize_all_docstrings(
    traits: Iterable[Trait], groups: Iterable[Group]
) -> None:
    """Initialize docstrings for all trait and group instances.

    This function should be called from ``__init__.py`` after all trait and
    group instances are imported. It iterates through all instances and sets
    their ``__doc__`` attributes by calling their ``generate_docstring()``
    methods.

    This approach avoids circular import issues that would occur if docstrings
    were generated in ``__post_init__`` during module initialization.

    :param traits: All trait instances to initialize docstrings for.
    :param groups: All group instances to initialize docstrings for.
    """
    # Initialize trait docstrings.
    for trait in traits:
        object.__setattr__(trait, "__doc__", trait.generate_docstring())

    # Initialize group docstrings.
    for group in groups:
        object.__setattr__(group, "__doc__", group.generate_docstring())
