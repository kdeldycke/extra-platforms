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
"""Group a collection of traits. Also referred as families."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field, replace
from functools import cached_property
from types import MappingProxyType

from .trait import Trait

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator

    from ._types import _TNestedReferences


def _flatten(items: Iterable) -> Iterator:
    """Recursively flatten nested iterables (except strings).

    Yields items from nested iterables one at a time, preserving order.
    Strings are treated as atomic values, not iterable containers.
    """
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from _flatten(item)
        else:
            yield item


@dataclass(frozen=True)
class Group:
    """A ``Group`` identify a collection of members.

    Members can be ``Trait`` instances: ``Platform``, ``Architecture``, or ``CI``.

    `set`-like methods are available and performed on the members of the group.

    The ``members`` field is an immutable mapping (``MappingProxyType``) from member
    ID to ``Trait`` object, providing O(1) lookup by ID.
    """

    id: str
    """Unique ID of the group."""

    name: str
    """User-friendly description of a group."""

    icon: str = field(repr=False, default="❓")
    """Icon of the group."""

    members: MappingProxyType[str, Trait] = field(
        repr=False, default_factory=lambda: MappingProxyType({})
    )
    """Immutable mapping of member ID to ``Trait`` object.

    Accepts an iterable of ``Trait`` objects during construction, which gets
    normalized to an immutable ``MappingProxyType[str, Trait]`` in ``__post_init__``.

    After initialization, this is always a ``MappingProxyType[str, Trait]``.
    """

    def __post_init__(self):
        """Validate and normalize the group fields:

        - Ensure the group ID, name and icon are not empty.
        - Deduplicate members and sort them by IDs
        - Convert input to immutable MappingProxyType
        """
        assert self.id, "Group ID cannot be empty."
        assert self.name, "Group name cannot be empty."
        assert self.icon, "Group icon cannot be empty."

        # Accept either a MappingProxyType, dict, or iterable of Traits.
        if isinstance(self.members, MappingProxyType):
            traits = self.members.values()
        elif isinstance(self.members, dict):
            traits = self.members.values()
        else:
            traits = self.members

        # Deduplicate and sort by ID, then build the immutable mapping.
        sorted_traits = sorted(set(traits), key=lambda t: t.id)
        object.__setattr__(
            self,
            "members",
            MappingProxyType({t.id: t for t in sorted_traits}),
        )

    @property
    def member_ids(self) -> frozenset[str]:
        """Set of member IDs that belong to this group."""
        return frozenset(self.members.keys())

    def __hash__(self) -> int:
        """Return a hash based on the group's immutable identity.

        The hash is computed from the group ID and the frozenset of member IDs,
        both of which are immutable.
        """
        return hash((self.id, self.member_ids))

    @cached_property
    def short_desc(self) -> str:
        """Returns the group name with its first letter in lowercase to be used as a
        short description.

        Mainly used to produce docstrings for function dynamically generated for each
        group.
        """
        return self.name[0].lower() + self.name[1:]

    def __iter__(self) -> Iterator[Trait]:
        """Iterate over the members of the group."""
        yield from self.members.values()

    def __len__(self) -> int:
        """Return the number of members in the group."""
        return len(self.members)

    def __contains__(self, item: Trait | str) -> bool:
        """Test if ``Trait`` object or its ID is part of the group."""
        if isinstance(item, str):
            return item in self.members
        return item.id in self.members and self.members[item.id] == item

    def __getitem__(self, member_id: str) -> Trait:
        """Return the trait whose ID is ``member_id``."""
        try:
            return self.members[member_id]
        except KeyError:
            raise KeyError(f"No trait found whose ID is {member_id}") from None

    def items(self) -> Iterator[tuple[str, Trait]]:
        """Iterate over the traits of the group as key-value pairs."""
        yield from self.members.items()

    @staticmethod
    def _extract_members(*other: _TNestedReferences) -> Iterator[Trait]:
        """Returns all traits found in ``other``.

        ``other`` can be an arbitrarily nested ``Iterable`` of ``Group``, ``Trait``, or
        their IDs. ``None`` values and empty iterables are silently ignored.

        .. caution::
            Can returns duplicates.
        """
        for item in _flatten(other):
            match item:
                case None:
                    continue
                case Trait():
                    yield item
                case Group():
                    yield from item.members.values()
                case str():
                    # Prevent circular import.
                    from .operations import traits_from_ids

                    yield from traits_from_ids(item)
                case _:
                    raise TypeError(f"Unsupported type: {type(item)}")

    def isdisjoint(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has no members in common with ``other``.

        Groups are disjoint if and only if their intersection is an empty set.

        ``other`` can be an arbitrarily nested ``Iterable`` of ``Group`` and ``Trait``.
        """
        return set(self.members.values()).isdisjoint(self._extract_members(other))

    def fullyintersects(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has all members in common with ``other``."""
        return set(self.members.values()) == set(self._extract_members(other))

    def issubset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other."""
        return set(self.members.values()).issubset(self._extract_members(other))

    __le__ = issubset

    def __lt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other, but not all."""
        return self <= other and set(self.members.values()) != set(
            self._extract_members(other)
        )

    def issuperset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group."""
        return set(self.members.values()).issuperset(self._extract_members(other))

    __ge__ = issuperset

    def __gt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group, but not all."""
        return self >= other and set(self.members.values()) != set(
            self._extract_members(other)
        )

    def union(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with members from the group and all others.

        .. caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(
                set(self.members.values()).union(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __or__ = union

    def intersection(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with members common to the group and all others.

        .. caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(  # type: ignore[arg-type]
                set(self.members.values()).intersection(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __and__ = intersection

    def difference(self, *others: _TNestedReferences) -> Group:
        """Return a new ``Group`` with members in the group that are not in the others.

        .. caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(  # type: ignore[arg-type]
                set(self.members.values()).difference(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __sub__ = difference

    def symmetric_difference(self, other: _TNestedReferences) -> Group:
        """Return a new ``Group`` with members in either the group or other but not both.

        .. caution::
            The new ``Group`` will inherits the metadata of the first one. All other
            groups' metadata will be ignored.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(  # type: ignore[arg-type]
                set(self.members.values()).symmetric_difference(
                    self._extract_members(other)
                )
            ),
        )

    __xor__ = symmetric_difference

    def copy(
        self,
        id: str | None = None,
        name: str | None = None,
        icon: str | None = None,
        members: Iterable[Trait] | None = None,
    ) -> Group:
        """Return a shallow copy of the group.

        Fields can be overridden by passing new values as arguments.
        """
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}
        return replace(self, **kwargs)
