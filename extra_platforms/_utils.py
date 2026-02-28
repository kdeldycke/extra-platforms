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
"""Internal utility functions."""

from __future__ import annotations

from typing import Any


def _recursive_update(
    a: dict[str, Any], b: dict[str, Any], strict: bool = False
) -> dict[str, Any]:
    """Like standard ``dict.update()``, but recursive so sub-dict gets updated.

    Ignore elements present in ``b`` but not in ``a``. Unless ``strict`` is set to
    ``True``, in which case a ``ValueError`` exception will be raised.
    """
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = _recursive_update(a[k], v, strict=strict)
        # Ignore elements unregistered in the template structure.
        elif k in a:
            a[k] = b[k]
        elif strict:
            raise ValueError(f"Parameter {k!r} found in second dict but not in first.")
    return a


def _remove_blanks(
    tree: dict,
    remove_none: bool = True,
    remove_dicts: bool = True,
    remove_str: bool = True,
) -> dict:
    """Returns a copy of a dict without items whose values blanks.

    Are considered blanks:

    - ``None`` values
    - empty strings
    - empty ``dict``

    The removal of each of these class can be skipped by setting ``remove_*``
    parameters.

    Dictionarries are inspected recursively and their own blank values are removed.
    """
    result = {}
    for key, value in tree.items():
        # Skip None values if configured.
        if remove_none and value is None:
            continue

        # Recursively process nested dicts.
        if isinstance(value, dict):
            cleaned = _remove_blanks(value, remove_none, remove_dicts, remove_str)
            # Skip empty dicts if configured.
            if remove_dicts and not cleaned:
                continue
            result[key] = cleaned
        # Skip empty strings if configured.
        elif remove_str and isinstance(value, str) and not value:
            continue
        else:
            result[key] = value

    return result
