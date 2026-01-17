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
from typing import cast

from .trait import Trait, _Identifiable

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator

    from ._types import _TNestedReferences

_MembersMapping = MappingProxyType[str, Trait]


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
class Group(_Identifiable):
    """A ``Group`` identifies a collection of ``Trait`` members.

    Additionally of the common fields inherited from ``_Identifiable``, each trait provides:

    - ``members``: An iterable of ``Trait`` instances that belong to this group.
    - ``member_ids``: A frozenset of member IDs for quick lookup.
    - ``canonical``: A boolean indicating if the group is canonical (non-overlapping).
    - various `set`-like operations (union, intersection, difference, etc.).
    """

    unknown_symbol = "UNKNOWN"
    """Groups use ``UNKNOWN`` instead of ``UNKNOWN_GROUP``."""

    members: Iterable[Trait] = field(repr=False, default_factory=tuple)
    """Traits in this group.

    Normalized to ``MappingProxyType[str, Trait]`` at init, providing O(1) lookup by ID.
    """

    @property
    def _members(self) -> _MembersMapping:
        """Typed access to members as ``MappingProxyType[str, Trait]``.

        .. warning::
            The ``members`` field is typed as ``Iterable[Trait]`` to accept any
            iterable at construction time. After ``__post_init__``, it is always a
            ``MappingProxyType[str, Trait]``. This property provides a ``cast()`` to
            that type, avoiding ``# type: ignore`` comments throughout the class.
        """
        return cast(_MembersMapping, self.members)

    def __post_init__(self):
        """Normalize members to a sorted, deduplicated mapping."""
        super().__post_init__()

        # Override detection_func_id and unless_decorator_id for groups with "all_" prefix.
        # Groups with "all_" prefix get "is_any_*" detection functions and "unless_any_*"
        # decorators (singular form) to better convey the "any member matches" semantic.
        # Class-type groups (those matching Trait subclasses) use the subclass's
        # type_id.
        if self.id.startswith("all_"):
            suffix = self.id[4:]
            # Map group suffix to singular type_id using Trait and its subclasses.
            # e.g., "architectures" → "architecture", "platforms" → "platform",
            #       "ci" → "ci", "traits" → "trait"
            suffix_to_type_id = {
                cls.all_group.lower()[4:]: cls.type_id
                for cls in (Trait, *Trait.__subclasses__())
            }
            if suffix in suffix_to_type_id:
                suffix = suffix_to_type_id[suffix]
            object.__setattr__(self, "detection_func_id", f"is_any_{suffix}")
            object.__setattr__(self, "unless_decorator_id", f"unless_any_{suffix}")

        # Override IDs for groups with "_without_" to use "_not_" instead.
        # This produces more natural function names like is_unix_not_macos() instead of
        # is_unix_without_macos().
        if "_without_" in self.id:
            func_id = self.detection_func_id.replace("_without_", "_not_")
            skip_id = self.skip_decorator_id.replace("_without_", "_not_")
            unless_id = self.unless_decorator_id.replace("_without_", "_not_")
            object.__setattr__(self, "detection_func_id", func_id)
            object.__setattr__(self, "skip_decorator_id", skip_id)
            object.__setattr__(self, "unless_decorator_id", unless_id)

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
        return frozenset(self._members.keys())

    def __hash__(self) -> int:
        """Hash based on group ID and member IDs."""
        return hash((self.id, self.member_ids))

    @cached_property
    def canonical(self) -> bool:
        """Returns `True` if the group is canonical (non-overlapping), `False` otherwise.

        A canonical group is one that does not share any members with other canonical
        groups. All canonical groups are non-overlapping.

        Non-canonical groups are provided for convenience, but overlap with each other
        or with canonical groups.

        .. hint::
            Canonical groups are denoted with a ⬥ symbol in the documentation and tables.
        """
        # Avoid circular import.
        from .group_data import NON_OVERLAPPING_GROUPS

        return self in NON_OVERLAPPING_GROUPS

    def __iter__(self) -> Iterator[Trait]:
        """Iterate over the members of the group."""
        yield from self._members.values()

    def __len__(self) -> int:
        """Return the number of members in the group."""
        return len(self._members)

    def __bool__(self) -> bool:
        """Return `True` if the group has members, `False` otherwise."""
        return len(self._members) > 0

    def __contains__(self, item: Trait | str) -> bool:
        """Test if ``Trait`` object or its ID is part of the group."""
        if isinstance(item, str):
            return item in self._members
        return item.id in self._members and self._members[item.id] == item

    def __getitem__(self, member_id: str) -> Trait:
        """Return the trait whose ID is ``member_id``."""
        try:
            return self._members[member_id]
        except KeyError:
            raise KeyError(f"No trait found whose ID is {member_id}") from None

    def items(self) -> Iterator[tuple[str, Trait]]:
        """Iterate over the traits of the group as key-value pairs."""
        yield from self._members.items()

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
                    yield from item._members.values()
                case str():
                    # Prevent circular import.
                    from .operations import traits_from_ids

                    yield from traits_from_ids(item)
                case _:
                    raise TypeError(f"Unsupported type: {type(item)}")

    @staticmethod
    def _extract_platforms(*other: _TNestedReferences) -> Iterator[Trait]:
        """Deprecated alias for `_extract_members()`.

        .. deprecated:: 6.0.0
           Use `_extract_members()` instead.
        """
        # Prevent circular import.
        from ._deprecated import _warn_deprecated

        _warn_deprecated("Group._extract_platforms()", "Group._extract_members()")
        return Group._extract_members(*other)

    def isdisjoint(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has no members in common with ``other``.

        Groups are disjoint if and only if their intersection is an empty set.

        ``other`` can be an arbitrarily nested ``Iterable`` of ``Group`` and ``Trait``.
        """
        return set(self._members.values()).isdisjoint(self._extract_members(other))

    def fullyintersects(self, other: _TNestedReferences) -> bool:
        """Return `True` if the group has all members in common with ``other``."""
        return set(self._members.values()) == set(self._extract_members(other))

    def issubset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other."""
        return set(self._members.values()).issubset(self._extract_members(other))

    __le__ = issubset

    def __lt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other, but not all."""
        return self <= other and set(self._members.values()) != set(
            self._extract_members(other)
        )

    def issuperset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group."""
        return set(self._members.values()).issuperset(self._extract_members(other))

    __ge__ = issuperset

    def __gt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group, but not all."""
        return self >= other and set(self._members.values()) != set(
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
                set(self._members.values()).union(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __or__ = union
    __ior__ = union

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
            tuple(
                set(self._members.values()).intersection(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __and__ = intersection
    __iand__ = intersection

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
            tuple(
                set(self._members.values()).difference(
                    *(self._extract_members(other) for other in others)
                )
            ),
        )

    __sub__ = difference
    __isub__ = difference

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
            tuple(
                set(self._members.values()).symmetric_difference(
                    self._extract_members(other)
                )
            ),
        )

    __xor__ = symmetric_difference
    __ixor__ = symmetric_difference

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

    def add(self, member: Trait | str) -> Group:
        """Return a new ``Group`` with the specified trait added.

        If the trait is already in the group, returns a copy unchanged.

        Args:
            member: A ``Trait`` object or trait ID string to add.

        Returns:
            A new ``Group`` instance with the trait added.

        Raises:
            ValueError: If the trait ID is not recognized.
        """
        if isinstance(member, str):
            # Prevent circular import.
            from .operations import traits_from_ids

            traits = traits_from_ids(member)
            member = traits[0]

        if member in self:
            return self.copy()

        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(set(self._members.values()) | {member}),
        )

    def remove(self, member: Trait | str) -> Group:
        """Return a new ``Group`` with the specified trait removed.

        Raises ``KeyError`` if the trait is not in the group.

        Args:
            member: A ``Trait`` object or trait ID string to remove.

        Returns:
            A new ``Group`` instance with the trait removed.

        Raises:
            KeyError: If the trait is not in the group.
        """
        member_id = member.id if isinstance(member, Trait) else member

        if member_id not in self._members:
            raise KeyError(f"Trait '{member_id}' is not in the group")

        new_members = {
            tid: trait for tid, trait in self._members.items() if tid != member_id
        }

        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(new_members.values()),
        )

    def discard(self, member: Trait | str) -> Group:
        """Return a new ``Group`` with the specified trait removed if present.

        Unlike ``remove()``, this does not raise an error if the trait is not found.

        Args:
            member: A ``Trait`` object or trait ID string to remove.

        Returns:
            A new ``Group`` instance with the trait removed, or a copy if not present.
        """
        member_id = member.id if isinstance(member, Trait) else member

        if member_id not in self._members:
            return self.copy()

        new_members = {
            tid: trait for tid, trait in self._members.items() if tid != member_id
        }

        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(new_members.values()),
        )

    def pop(self, member_id: str | None = None) -> tuple[Trait, Group]:
        """Remove and return a trait from the group.

        Args:
            member_id: Optional trait ID to remove. If not provided, removes an arbitrary
                trait (specifically, the first one in iteration order).

        Returns:
            A tuple of (removed_trait, new_group).

        Raises:
            KeyError: If ``member_id`` is provided but not found in the group.
            KeyError: If the group is empty.
        """
        if not self._members:
            raise KeyError("pop from an empty group")

        if member_id is None:
            # Pop arbitrary (first) member.
            member_id = next(iter(self._members))

        if member_id not in self._members:
            raise KeyError(f"Trait '{member_id}' is not in the group")

        popped_trait = self._members[member_id]
        new_members = {
            tid: trait for tid, trait in self._members.items() if tid != member_id
        }

        new_group = Group(
            self.id,
            self.name,
            self.icon,
            tuple(new_members.values()),
        )

        return popped_trait, new_group

    def clear(self) -> Group:
        """Return a new empty ``Group`` with the same metadata.

        Returns:
            A new ``Group`` instance with no members but same id, name, and icon.
        """
        return Group(
            self.id,
            self.name,
            self.icon,
            tuple(),
        )
