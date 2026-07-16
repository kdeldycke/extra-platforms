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

Renamed symbols stay importable from the package root for a deprecation cycle.
Accessing one emits a {exc}`DeprecationWarning` pointing to its replacement,
through the [PEP 562](https://peps.python.org/pep-0562/) module
``__getattr__`` hook in ``__init__.py``.

```{important}
Aliases registered here are scheduled for removal in the major release recorded
in {data}`REMOVAL_VERSION`.
```

```{todo}
Remove the ``NON_OVERLAPPING_GROUPS`` and ``EXTRA_GROUPS`` aliases (and their
tests) in ``14.0.0``.
```
"""

from __future__ import annotations

import warnings

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

REMOVAL_VERSION = "14.0.0"
"""The release in which the registered aliases stop resolving."""

DEPRECATED_ALIASES: dict[str, str] = {
    "EXTRA_GROUPS": "NON_CANONICAL_GROUPS",
    "NON_OVERLAPPING_GROUPS": "CANONICAL_GROUPS",
}
"""Maps each deprecated symbol to its replacement at the package root."""


def resolve_deprecated(name: str) -> Any:
    """Return the replacement object for the deprecated ``name``.

    Emits a {exc}`DeprecationWarning` naming the replacement, attributed to the
    caller's access site (``stacklevel=3``: this function, the package root's
    ``__getattr__``, then the caller).
    """
    replacement = DEPRECATED_ALIASES[name]
    warnings.warn(
        f"{name} is deprecated and will be removed in extra-platforms "
        f"{REMOVAL_VERSION}, use {replacement} instead.",
        DeprecationWarning,
        stacklevel=3,
    )
    import extra_platforms

    return getattr(extra_platforms, replacement)
