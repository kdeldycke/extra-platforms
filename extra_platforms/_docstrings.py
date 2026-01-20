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
"""Utilities for generating runtime docstrings for traits and groups.

This module provides functions to extract attribute docstrings from source
files and generate comprehensive documentation for trait and group instances.

The :func:`_initialize_all_docstrings` function should be called from
``__init__.py`` after all trait and group instances are imported to populate
their ``__doc__`` attributes.
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


def get_attribute_docstring(module_name: str, attr_name: str) -> str | None:
    """Extract attribute docstring from a module's source file.

    Attribute docstrings are string literals that immediately follow an
    assignment. This function parses the source file using AST to find such
    docstrings.

    :param module_name: The full module name (e.g.,
        'extra_platforms.platform_data').
    :param attr_name: The attribute name to look for (e.g., 'NOBARA').
    :returns: The attribute docstring if found, or None.
    """
    module = importlib.import_module(module_name)
    source_file = inspect.getsourcefile(module)
    if not source_file:
        raise FileNotFoundError(f"Cannot find source file for module {module_name}")

    source = Path(source_file).read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Look for assignment (or annotated assignment) followed by a string
    # literal.
    for i, node in enumerate(tree.body):
        # Handle both regular assignments and annotated assignments.
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == attr_name:
                    # Check if the next statement is a string expression.
                    if i + 1 < len(tree.body):
                        next_node = tree.body[i + 1]
                        if isinstance(next_node, ast.Expr) and isinstance(
                            next_node.value, ast.Constant
                        ):
                            if isinstance(next_node.value.value, str):
                                return next_node.value.value
        elif isinstance(node, ast.AnnAssign):
            # Handle annotated assignments like: x: type = value.
            if isinstance(node.target, ast.Name) and node.target.id == attr_name:
                # Check if the next statement is a string expression.
                if i + 1 < len(tree.body):
                    next_node = tree.body[i + 1]
                    if isinstance(next_node, ast.Expr) and isinstance(
                        next_node.value, ast.Constant
                    ):
                        if isinstance(next_node.value.value, str):
                            return next_node.value.value

    return None


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
