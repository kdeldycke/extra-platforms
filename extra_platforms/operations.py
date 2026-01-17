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
"""Operations on a mix of Groups and Platforms."""

from __future__ import annotations

from itertools import combinations

from .group import Group
from .group_data import ALL_GROUPS, ALL_TRAITS, UNKNOWN

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from ._types import _T, _TNestedReferences
    from .trait import Trait


ALL_TRAIT_IDS: frozenset[str] = frozenset((p.id for p in ALL_TRAITS - UNKNOWN))
"""Set of all recognized traits IDs.

.. attention::
    This collection does not contain all the ``UNKNOWN_*`` traits.
"""

ALL_GROUP_IDS: frozenset[str] = frozenset((p.id for p in ALL_GROUPS - {UNKNOWN}))
"""Set of all recognized group IDs.

.. attention::
    This collection does not contain the :data:`~extra_platforms.UNKNOWN` group.
"""

ALL_IDS: frozenset[str] = ALL_TRAIT_IDS | ALL_GROUP_IDS
"""Set of all recognized traits and group IDs.

.. attention::
    This collection does not contain all the ``UNKNOWN_*`` traits and the
    :data:`~extra_platforms.UNKNOWN` group.
"""


def _unique(items: Iterable[_T]) -> tuple[_T, ...]:
    """Return a tuple with duplicates removed, preserving order.

    This uses ``dict.fromkeys()`` which:

    - Preserves insertion order (guaranteed since Python 3.7)
    - Removes duplicates (dict keys are unique)
    """
    return tuple(dict.fromkeys(items))


def traits_from_ids(*trait_and_group_ids: str) -> tuple[Trait, ...]:
    """Returns a deduplicated tuple of traits matching the provided IDs.

    IDs are case-insensitive, and can refer to any traits or groups. Matching groups
    will be expanded to the traits they contain.

    Order of the returned traits matches the order of the provided IDs.

    .. tip::
        If you want to reduce the returned set and removes as much overlaps as
        possible, you can use the ``extra_platforms.reduce()`` function on the results.
    """
    ids = _unique((s.lower() for s in trait_and_group_ids))
    unrecognized_ids = set(ids) - ALL_IDS
    if unrecognized_ids:
        raise ValueError(
            "Unrecognized group or trait IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    traits = []
    for trait_id in ids:
        if trait_id in ALL_TRAIT_IDS:
            traits.append(ALL_TRAITS[trait_id])
        else:
            groups = groups_from_ids(trait_id)
            assert len(groups) == 1
            traits.extend(groups[0])
    return _unique(traits)


def groups_from_ids(*group_ids: str) -> tuple[Group, ...]:
    """Returns a deduplicated tuple of groups matching the provided IDs.

    IDs are case-insensitive.

    Order of the returned groups matches the order of the provided IDs.

    .. tip::
        If you want to reduce the returned set and removes as much overlaps as
        possible, you can use the ``extra_platforms.reduce()`` function on the results.
    """
    ids = _unique((s.lower() for s in group_ids))
    unrecognized_ids = set(ids) - ALL_GROUP_IDS
    if unrecognized_ids:
        raise ValueError(
            "Unrecognized group IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    groups = []
    for group_id in ids:
        for group in ALL_GROUPS:
            if group.id == group_id:
                groups.append(group)
    return _unique(groups)


def reduce(
    items: _TNestedReferences,
    target_pool: Iterable[Group | Trait] | None = None,
) -> frozenset[Group | Trait]:
    """Reduce a collection of traits to a minimal set.

    Returns a deduplicated set of ``Group`` and ``Trait`` that covers the same exact
    traits as the original input, but group as much traits as possible, to reduce
    the number of items.

    Only the groups defined in the ``target_pool`` are considered for the reduction.
    If no reference pool is provided, use all known groups.

    .. hint::
        Maybe this could be solved with some `Euler diagram
        <https://en.wikipedia.org/wiki/Euler_diagram>`_ algorithms, like those
        implemented in `eule <https://github.com/trouchet/eule>`_.

        This is being discussed upstream at `trouchet/eule#120
        <https://github.com/trouchet/eule/issues/120>`_.

    .. todo::
        Should we rename or alias this method to `collapse()`? Cannot decide if it is
        more descriptive or not...
    """
    # Collect all traits.
    traits = frozenset(Group._extract_members(items))

    # List all groups overlapping the set of input traits.
    if target_pool is None:
        target_pool = ALL_GROUPS
    overlapping_groups = frozenset(
        g for g in target_pool if isinstance(g, Group) and g.issubset(traits)
    )

    # Test all combination of groups to find the smallest set of groups + traits.
    min_items = 0
    results: list[frozenset[Group | Trait]] = []
    # Serialize group sets for deterministic lookups. Sort them by trait count.
    groups = tuple(sorted(overlapping_groups, key=len, reverse=True))
    for subset_size in range(1, len(groups) + 1):
        # If we already have a solution that involves less items than the current
        # subset of groups we're going to evaluates, there is no point in continuing.
        if min_items and subset_size > min_items:
            break

        for group_subset in combinations(groups, subset_size):
            # If any group overlaps another, there is no point in exploring this subset.
            if not all(g[0].isdisjoint(g[1]) for g in combinations(group_subset, 2)):
                continue

            # Remove all traits covered by the groups.
            ungrouped_traits = set(traits.copy())
            ungrouped_traits.difference_update(*group_subset)

            # Merge the groups and the remaining traits.
            reduction = frozenset(ungrouped_traits.union(group_subset))
            reduction_size = len(reduction)

            # Reset the results if we have a new solution that is better than the
            # previous ones.
            if not results or reduction_size < min_items:
                results = [reduction]
                min_items = reduction_size
            # If the solution is as good as the previous one, add it to the results.
            elif reduction_size == min_items:
                results.append(reduction)

    if len(results) > 1:
        raise RuntimeError(f"Multiple solutions found: {results}")

    # If no reduced solution was found, return the original traits.
    if not results:
        return traits

    return results.pop()
