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
"""Backward-compatible deprecated aliases.

Renamed symbols stay importable from their original module for a deprecation
cycle. Accessing one emits a {exc}`DeprecationWarning` pointing to its
replacement, through the [PEP 562](https://peps.python.org/pep-0562/) module
``__getattr__`` hook in ``_utils.py``.

```{important}
Aliases registered here are scheduled for removal in the major release recorded
in {data}`REMOVAL_VERSION`.
```

The `{todo}` that schedules their removal is in the docstring of `__init__.py`,
where the todo list collects it.
"""

from __future__ import annotations

import warnings
from importlib import import_module

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

REMOVAL_VERSION = "16.0.0"
"""The release in which the registered aliases stop resolving."""

DEPRECATED_ALIASES: dict[str, dict[str, str]] = {
    # Click Extra 9.5.1 and older import these private helpers.
    "extra_platforms._utils": {
        "_recursive_update": "recursive_update",
        "_remove_blanks": "remove_blanks",
    },
}
"""Maps each deprecated symbol to its replacement, keyed by hosting module."""


def resolve_deprecated(module_id: str, name: str) -> Any:
    """Resolve an attribute access from a module's ``__getattr__`` hook.

    Looks ``name`` up among the {data}`DEPRECATED_ALIASES` registered for
    ``module_id``. For a deprecated alias, emits a {exc}`DeprecationWarning`
    naming the replacement and returns the replacement object. For any other
    name, raises {exc}`AttributeError` so unknown attributes behave as usual.

    The warning is attributed to the caller's access site (``stacklevel=3``:
    this function, the hosting module's ``__getattr__``, then the caller).
    """
    replacement = DEPRECATED_ALIASES.get(module_id, {}).get(name)
    if replacement is None:
        raise AttributeError(f"module {module_id!r} has no attribute {name!r}")
    warnings.warn(
        f"{name} is deprecated and will be removed in extra-platforms "
        f"{REMOVAL_VERSION}, use {replacement} instead.",
        DeprecationWarning,
        stacklevel=3,
    )
    return getattr(import_module(module_id), replacement)
