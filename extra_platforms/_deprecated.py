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

Renamed and removed symbols stay importable from their original module for a
deprecation cycle. Accessing one emits a {exc}`DeprecationWarning` pointing to
its replacement, through the [PEP 562](https://peps.python.org/pep-0562/)
module ``__getattr__`` hooks in ``__init__.py`` and ``pytest.py``.

```{important}
Aliases registered here are scheduled for removal in the major release recorded
in {data}`REMOVAL_VERSION`.
```

```{todo}
Remove all registered aliases (and their tests) in ``14.0.0``.
```
"""

from __future__ import annotations

import warnings
from importlib import import_module

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

REMOVAL_VERSION = "14.0.0"
"""The release in which the registered aliases stop resolving."""

DEPRECATED_ALIASES: dict[str, dict[str, str]] = {
    "extra_platforms": {
        "EXTRA_GROUPS": "NON_CANONICAL_GROUPS",
        "NON_OVERLAPPING_GROUPS": "CANONICAL_GROUPS",
        "TUMBLEWEED": "OPENSUSE",
        "is_tumbleweed": "is_opensuse",
    },
    "extra_platforms.pytest": {
        "skip_tumbleweed": "skip_opensuse",
        "unless_tumbleweed": "unless_opensuse",
    },
}
"""Maps each deprecated symbol to its replacement, keyed by hosting module."""


def resolve_deprecated(module_id: str, name: str) -> Any:
    """Return the replacement object for the deprecated ``name`` in ``module_id``.

    Emits a {exc}`DeprecationWarning` naming the replacement, attributed to the
    caller's access site (``stacklevel=3``: this function, the hosting module's
    ``__getattr__``, then the caller).
    """
    replacement = DEPRECATED_ALIASES[module_id][name]
    warnings.warn(
        f"{name} is deprecated and will be removed in extra-platforms "
        f"{REMOVAL_VERSION}, use {replacement} instead.",
        DeprecationWarning,
        stacklevel=3,
    )
    return getattr(import_module(module_id), replacement)
