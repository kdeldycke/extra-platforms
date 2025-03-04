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
"""Group models collection of platforms. Also referred as families or categories."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
from functools import cached_property
from typing import TYPE_CHECKING, Iterator

from boltons.iterutils import flatten_iter

from .platform import Platform

if TYPE_CHECKING:
    from . import _TNestedReferences


@dataclass(frozen=True)
class Group:
    """A ``Group`` identify a collection of ``Platform``.

    Used to group platforms of the same family.

    `set`-like methods are available and performed on the platform objects the group
    contains (in the ``self.platforms`` data field).

    .. todo::
        Replace the ``platforms``/``platform_ids`` combo fields with a single
        ``platforms`` field that is a simple `dict` of platform ID to platform object.
        But maybe that going to be too much of a hassle because a ``dict`` cannot be
        frozen.
    """

    id: str
    """Unique ID of the group."""

    name: str
    """User-friendly description of a group."""

    icon: str = field(repr=False, default="❓")
    """Icon of the group."""

    platforms: tuple[Platform, ...] = field(repr=False, default_factory=tuple)
    """Sorted list of platforms that belong to this group."""

    platform_ids: frozenset[str] = field(default_factory=frozenset, init=False)
    """Set of platform IDs that belong to this group."""

    def __post_init__(self):
        """Validate and normalize the group fields:

        - Ensure the group ID, name and icon are not empty.
        - Deduplicate platforms and sort them by IDs
        - Populate the set of platform IDs and check for duplicates
        """
        assert self.id, "Group ID cannot be empty."
        assert self.name, "Group name cannot be empty."
        assert self.icon, "Group icon cannot be empty."

        object.__setattr__(
            self,
            "platforms",
            tuple(sorted(set(self.platforms), key=lambda p: p.id)),
        )

        # Double check there are no Platform objects sharing the same IDs.
        id_counter = Counter(p.id for p in self.platforms)
        if len(set(id_counter)) != len(self.platforms):
            duplicates = (k for k, v in dict(id_counter).items() if v > 1)
            raise ValueError(
                "The group is not allowed to have platforms with duplicate IDs: "
                f"{', '.join(duplicates)}"
            )
        object.__setattr__(self, "platform_ids", frozenset(id_counter))

    @cached_property
    def short_desc(self) -> str:
        """Returns the group name with its first letter in lowercase to be used as a
        short description.

        Mainly used to produce docstrings for function dynamically generated for each
        group.
        """
        return self.name[0].lower() + self.name[1:]

    def __iter__(self) -> Iterator[Platform]:
        """Iterate over the platforms of the group."""
        yield from self.platforms

    def __len__(self) -> int:
        """Return the number of platforms in the group."""
        return len(self.platforms)

    def __contains__(self, platform: Platform | str) -> bool:
        """Test if ``Platform`` object or its ID is part of the group."""
        return (
            (platform in self.platform_ids)
            if isinstance(platform, str)
            else (platform in self.platforms)
        )

    def __getitem__(self, platform_id: str) -> Platform:
        """Return the platform whose ID is ``platform_id``."""
        for platform in self.platforms:
            if platform.id == platform_id:
                return platform
        raise KeyError(f"No platform found whose ID is {platform_id}")

    def items(self) -> Iterator[tuple[str, Platform]]:
        """Iterate over the platforms of the group as key-value pairs."""
        yield from ((platform.id, platform) for platform in self.platforms)

    @staticmethod
    def _extract_platforms(*other: _TNestedReferences) -> Iterator[Platform]:
        """Returns all platforms found in ``other``.

        ``other`` can be an arbitrarily nested ``Iterable`` of ``Group``, ``Platform``, or
        their IDs. ``None`` values and empty iterables are silently ignored.

        ..caution::
            Can returns duplicates.
        """
        for item in flatten_iter(other):
            match item:
                case None:
                    continue
                case Platform():
                    yield item
                case Group():
                    yield from item.platforms
                case str():
                    # Prevent circular import.
                    from .operations import platforms_from_ids

                    yield from platforms_from_ids(item)
                case _:
                    raise TypeError(f"Unsupported type: {type(item)}")

    def isdisjoint(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has no platforms in common with ``other``.

        Groups are disjoint if and only if their intersection is an empty set.

        ``other`` can be an arbitrarily nested ``Iterable`` of ``Group`` and ``Platform``.
        """
        return set(self.platforms).isdisjoint(self._extract_platforms(other))

    def fullyintersects(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has all platforms in common with ``other``."""
        return set(self.platforms) == set(self._extract_platforms(other))

    def issubset(self, other: _TNestedReferences) -> bool:
        """Test whether every platforms in the group is in other."""
        return set(self.platforms).issubset(self._extract_platforms(other))

    __le__ = issubset

    def __lt__(self, other: _TNestedReferences) -> bool:
        """Test whether every platform in the group is in other, but not all."""
        return self <= other and set(self.platforms) != set(
            self._extract_platforms(other)
        )

    def issuperset(self, other: _TNestedReferences) -> bool:
        """Test whether every platform in other is in the group."""
        return set(self.platforms).issuperset(self._extract_platforms(other))

    __ge__ = issuperset

    def __gt__(self, other: _TNestedReferences) -> bool:
        """Test whether every platform in other is in the group, but not all."""
        return self >= other and set(self.platforms) != set(
            self._extract_platforms(other)
        )

    def union(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with platforms from the group and all others.

        ..caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(
                set(self.platforms).union(
                    *(self._extract_platforms(other) for other in others)
                )
            ),
        )

    __or__ = union

    def intersection(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with platforms common to the group and all others.

        ..caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(
                set(self.platforms).intersection(
                    *(self._extract_platforms(other) for other in others)
                )
            ),
        )

    __and__ = intersection

    def difference(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with platforms in the group that are not in the others.

        ..caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(
                set(self.platforms).difference(
                    *(self._extract_platforms(other) for other in others)
                )
            ),
        )

    __sub__ = difference

    def symmetric_difference(self, other: _TNestedReferences) -> Group:
        """Return a new ``Group`` with platforms in either the group or other but not both.

        ..caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(
                set(self.platforms).symmetric_difference(self._extract_platforms(other))
            ),
        )

    __xor__ = symmetric_difference

    def copy(
        self,
        id: str | None = None,
        name: str | None = None,
        icon: str | None = None,
        platforms: tuple[Platform, ...] | None = None,
    ) -> Group:
        """Return a shallow copy of the group.

        Fields can be overridden by passing new values as arguments.
        """
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}
        return replace(self, **kwargs)
