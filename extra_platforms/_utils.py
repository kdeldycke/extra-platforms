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
