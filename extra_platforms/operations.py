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
from typing import TYPE_CHECKING, FrozenSet, Iterable

from boltons.iterutils import unique, unique_iter

from .group import Group
from .group_data import ALL_GROUPS, ALL_PLATFORMS
from .platform import Platform

if TYPE_CHECKING:
    from . import _TNestedReferences


ALL_PLATFORM_IDS: FrozenSet[str] = frozenset((p.id for p in ALL_PLATFORMS.platforms))
"""Set of all recognized platform IDs."""

ALL_GROUP_IDS: FrozenSet[str] = frozenset((p.id for p in ALL_GROUPS))
"""Set of all recognized group IDs."""

ALL_IDS: FrozenSet[str] = ALL_PLATFORM_IDS | ALL_GROUP_IDS
"""Set of all recognized platform and group IDs."""


def platforms_from_ids(*platform_ids: str) -> tuple[Platform]:
    """Returns a deduplicated tuple of platforms matching the provided IDs.

    IDs are case-insensitive, and can refer to any platforms or groups. Matching groups
    will be expanded to the platforms they contain.

    ..tip::
        If you want to reduce the returned set and removes as much overlaps as
        possible, you can use the ``extra_platforms.reduce()`` function on the results.
    """
    ids = unique((s.lower() for s in platform_ids))
    unrecognized_ids = set(ids) - ALL_IDS
    if unrecognized_ids:
        raise ValueError(
            "Unrecognized group or platform IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    platforms = []
    for platform_id in ids:
        if platform_id in ALL_PLATFORM_IDS:
            platforms.append(ALL_PLATFORMS[platform_id])
        else:
            groups = groups_from_ids(platform_id)
            assert len(groups) == 1
            platforms.extend(groups[0].platforms)
    return tuple(unique_iter(platforms))


def groups_from_ids(*group_ids: str) -> tuple[Group]:
    """Returns a deduplicated tuple of groups matching the provided IDs.

    IDs are case-insensitive.

    ..tip::
        If you want to reduce the returned set and removes as much overlaps as
        possible, you can use the ``extra_platforms.reduce()`` function on the results.
    """
    ids = unique((s.lower() for s in group_ids))
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
    return tuple(unique_iter(groups))


def reduce(
    items: _TNestedReferences, target_pool: Iterable[Group | Platform] | None = None
) -> frozenset[Group | Platform]:
    """Reduce a collection of platforms to a minimal set.

    Returns a deduplicated set of ``Group`` and ``Platform`` that covers the same exact
    platforms as the original input, but group as much platforms as possible, to reduce
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
    # Collect all platforms.
    platforms = frozenset(Group._extract_platforms(items))

    # List all groups overlapping the set of input platforms.
    if target_pool is None:
        target_pool = ALL_GROUPS
    overlapping_groups = frozenset(
        g for g in target_pool if isinstance(g, Group) and g.issubset(platforms)
    )

    # Test all combination of groups to find the smallest set of groups + platforms.
    min_items = 0
    results: list[frozenset[Group | Platform]] = []
    # Serialize group sets for deterministic lookups. Sort them by platform count.
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

            # Remove all platforms covered by the groups.
            ungrouped_platforms = set(platforms.copy())
            ungrouped_platforms.difference_update(*group_subset)

            # Merge the groups and the remaining platforms.
            reduction = frozenset(ungrouped_platforms.union(group_subset))
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
        msg = f"Multiple solutions found: {results}"
        raise RuntimeError(msg)

    # If no reduced solution was found, return the original platforms.
    if not results:
        return platforms

    return results.pop()
