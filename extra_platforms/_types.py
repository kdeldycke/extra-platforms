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
"""Custom types used across the package.

Inspired by `how tomllib does it in the stdlib
<https://github.com/python/cpython/tree/main/Lib/tomllib>`_.

.. hint::
    These type are designed to be imported as follows:

    .. code-block:: python

        TYPE_CHECKING = False
        if TYPE_CHECKING:
            from typing import Sequence, ...

            from ._types import _TRef, _TNestedReferences, ...

    `Mypy is able to pick them up correctly
    <https://mypy.readthedocs.io/en/stable/common_issues.html#python-version-and-system-platform-checks>`_
    because ``TYPE_CHECKING`` is always evaluated to ``False`` at runtime, and to
    ``True`` `during static analysis
    <https://github.com/python/mypy/blob/6aa44da/mypy/reachability.py#L152>`_.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from .group import Group
from .trait import Trait

_T = TypeVar("_T")
"""Generic type variable."""


_TRef = Trait | Group | str | None
"""All types that can be used to reference a trait or a group:

- a :class:`~extra_platforms.Trait` object itself
- a :class:`~extra_platforms.Group` object representing a collection of traits
- a string representing a trait ID or a group ID
- ``None`` to represent an empty set of traits
"""

_TNestedReferences = _TRef | Iterable[_TRef | Iterable["_TNestedReferences"]]
"""Type for arbitrary nested references to traits and groups."""
