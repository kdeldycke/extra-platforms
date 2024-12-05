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
"""Pytest decorators to skip tests depending on the platform they're run on.

Generates a pair of ready-to-use ``@skip_<id>`` and ``@unless_<id>`` decorators for
each platform and group.
"""

from __future__ import annotations

try:
    import pytest  # noqa: F401
except ImportError:
    raise ImportError(
        "You need to install extra_platforms[pytest] extra dependencies to use this "
        "module."
    )

from itertools import chain
from typing import Callable

import extra_platforms

from .group import Group
from .group_data import ALL_GROUPS, ALL_PLATFORMS

__all__ = []


class DeferredCondition:
    """Defer the evaluation of a condition.

    This allow a callable returning a boolean to be evaluated only when the boolean
    value is requested.

    Pytest's marks can have a condition attached to them. Which is practical for
    implementing our own ready-to-use ``@skip`` and ``@unless`` decorators.

    The problem is: this condition is evaluated at import time. Which leads to all our
    platform detection heuristics to be called when we generates our custom decorators
    below.

    This issue is being discussed upstream at:
        - https://github.com/pytest-dev/pytest/issues/7395
        - https://github.com/pytest-dev/pytest/issues/9650
    """

    def __init__(self, condition: Callable[[], bool], invert: bool = False) -> None:
        self.condition = condition
        self.invert = invert

    def __bool__(self) -> bool:
        """Call the deferred condition and return its result."""
        result = self.condition()
        return not result if self.invert else result


# Generate a pair of skip/unless decorators for each platform and group.
for _obj in chain(ALL_PLATFORMS, ALL_GROUPS):
    # Get the detection function for the current object.
    func = getattr(extra_platforms, f"is_{_obj.id}")

    # Short description of the object to be used in the reason.
    short_desc = _obj.short_desc if isinstance(_obj, Group) else _obj.name

    # Generate @skip decorator.
    skip_id = f"skip_{_obj.id}"
    locals()[skip_id] = pytest.mark.skipif(
        DeferredCondition(func),
        reason=f"Skip {short_desc}",
    )

    # Generate @unless decorator.
    unless_id = f"unless_{_obj.id}"
    locals()[unless_id] = pytest.mark.skipif(
        DeferredCondition(func, invert=True),
        reason=f"Requires {short_desc}",
    )

    # Add the generated decorators to the list of exported symbols.
    __all__.extend([skip_id, unless_id])
