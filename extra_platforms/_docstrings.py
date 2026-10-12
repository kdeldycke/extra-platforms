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
files, which the `generate_docstring()` method of a trait or group folds into
its own documentation. `trait._LazyDocstring` calls that method on the first
read of the `__doc__` of a predefined trait or group, so nothing here runs when
the package is imported.

```{note}
The attribute docstrings of a module are cached. A data module is therefore
read and parsed once, on the first docstring read of one of its traits or
groups. Without the cache, each read runs {func}`ast.parse` on a whole data
module again. Reading the docstring of every trait and group then takes
~110 ms instead of ~4 ms. Both figures are medians over 30 fresh CPython 3.12
interpreters on Apple Silicon.
```
"""

from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

# Per-module cache of attribute name to docstring. Populated lazily by
# `_parse_module_docstrings` on first access to a given module.
_module_docstrings_cache: dict[str, dict[str, str]] = {}


def _parse_module_docstrings(module_name: str) -> dict[str, str]:
    """Parse a module's source and return all attribute docstrings at once.

    Attribute docstrings are string literals that immediately follow an
    assignment statement at module level.

    :param module_name: The full module name (e.g.,
        'extra_platforms.platform_data').
    :returns: A mapping of attribute names to their docstrings. Empty dict if
        the module is not loaded or its source is unavailable.
    """
    # A trait or group exists only once its data module is loaded, so there is
    # nothing to import here. A name absent from sys.modules matches no data
    # module: a class defined outside the package derives such a name.
    module = sys.modules.get(module_name)
    if module is None:
        return {}

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

    ```{note}
    Returns `None` if source files are unavailable, which happens in
    compiled environments (e.g., Nuitka, PyInstaller, cx_Freeze). This
    graceful degradation allows the library to function without docstrings
    in compiled binaries.
    ```

    :param module_name: The full module name (e.g.,
        'extra_platforms.platform_data').
    :param attr_name: The attribute name to look for (e.g., 'NOBARA').
    :returns: The attribute docstring if found, or `None` if not found, or if
        the module is not loaded or its source is unavailable.
    """
    if module_name not in _module_docstrings_cache:
        _module_docstrings_cache[module_name] = _parse_module_docstrings(module_name)
    return _module_docstrings_cache[module_name].get(attr_name)
