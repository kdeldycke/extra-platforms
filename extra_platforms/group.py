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
"""Group a collection of traits. Also referred as families."""

from __future__ import annotations

import os
import sys
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from functools import cache, cached_property, lru_cache
from operator import attrgetter
from types import MappingProxyType

from .trait import Trait, _Identifiable

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self, TypeVar

    from ._types import _TNestedReferences

    _T = TypeVar("_T")


_PACKAGE_DIR = os.path.dirname(__file__) + os.sep
"""Prefix of the source files of the package, which tells its frames from a caller's."""


def _all_group_suffix_to_type_id() -> dict[str, str]:
    """Map ``ALL_*`` group ID suffixes to their trait type IDs.

    Derived from {class}`~extra_platforms.Trait` and its subclasses, so an
    ``all_architectures`` group resolves to the singular ``architecture`` type
    ID (and likewise ``all_ci`` to ``ci``, ``all_traits`` to ``trait``, etc.).

    Rebuilt on each call rather than cached, so {class}`~extra_platforms.Trait`
    subclasses defined outside this package are picked up by the groups
    created after them.
    """
    # Star-unpacking fails type checking here: mypy joins the `Trait` class object
    # and the `type[Trait]` items of `__subclasses__()` into a bare `object`.
    return {
        cls.all_group.lower().removeprefix("all_"): cls.type_id
        for cls in [Trait] + Trait.__subclasses__()
    }


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


def extract_members(*other: _TNestedReferences) -> Iterator[Trait]:
    """Returns all traits found in `other`.

    `other` can be an arbitrarily nested {class}`~collections.abc.Iterable` of
    {class}`~extra_platforms.Group`, {class}`~extra_platforms.Trait`, or their IDs.
    `None` values and empty iterables are silently ignored.

    ```{caution}
    Can return duplicates.
    ```
    """
    # A group needs no case of its own: _flatten() already iterates it into its
    # traits.
    for item in _flatten(other):
        match item:
            case None:
                continue
            case Trait():
                yield item
            case str():
                yield from traits_from_ids(item)
            case _:
                raise TypeError(f"Unsupported type: {type(item)}")


@dataclass(frozen=True)
class Group(_Identifiable, unknown_symbol="UNKNOWN"):
    """A {class}`~extra_platforms.Group` names a collection of traits.

    Its members are {class}`~extra_platforms.Trait` instances.

    Additionally of the common fields inherited from `_Identifiable`,
    each group provides:

    - `members`: An iterable of {class}`~extra_platforms.Trait`
      instances that belong to this group.
    - `member_ids`: A {class}`frozenset` of member IDs for quick lookup.
    - `canonical`: A {class}`bool` indicating if the group is canonical
      (non-overlapping).
    - various {class}`set`-like operations (union, intersection, difference, etc.).

    Its unknown symbol is `UNKNOWN`, instead of the derived `UNKNOWN_GROUP`.
    """

    members: Iterable[Trait] = field(repr=False, default_factory=tuple)
    """Traits in this group.

    Normalized to {class}`~types.MappingProxyType` at init, providing O(1) lookup by ID.
    """

    def __post_init__(self) -> None:
        """Normalize members to a mapping of deduplicated traits, sorted by ID.

        ```{hint}
        The docstring is not built here. For a predefined group,
        `_LazyDocstring` generates it on the first read of `__doc__`, once
        every module is imported.
        ```
        """
        super().__post_init__()

        # Accept a mapping of IDs to traits, or any iterable of traits.
        traits = (
            self.members.values() if isinstance(self.members, Mapping) else self.members
        )
        object.__setattr__(
            self,
            "members",
            MappingProxyType({
                trait.id: trait for trait in sorted(set(traits), key=attrgetter("id"))
            }),
        )

    @property
    def _members(self) -> MappingProxyType[str, Trait]:
        """Typed access to members as {class}`~types.MappingProxyType`.

        ```{warning}
        The `members` field is typed as {class}`~collections.abc.Iterable`
        to accept any iterable at construction time. After `__post_init__`,
        it is always a {class}`~types.MappingProxyType`, which this property
        tells the type checker.
        ```
        """
        return self.members  # type: ignore[return-value]

    @cached_property
    def _traits(self) -> frozenset[Trait]:
        """The members, as a {class}`frozenset` the set operations work on."""
        return frozenset(self._members.values())

    @cached_property
    def _any_stem(self) -> str:
        """The ID, or ``any_<type>`` for a group named ``all_*``.

        The detection function and the unless decorator of a group named
        ``all_*`` read "any member matches": {func}`~extra_platforms.is_any_arm`
        and {deco}`~pytest.unless_any_arm`. A group named after every trait of a
        type takes that type's singular ID: ``all_architectures`` gives
        ``any_architecture``.
        """
        if not self.id.startswith("all_"):
            return self.id
        suffix = self.id.removeprefix("all_")
        return "any_" + _all_group_suffix_to_type_id().get(suffix, suffix)

    @cached_property
    def detection_func_id(self) -> str:
        """ID of the detection function for this group.

        Named `is_<id>()`, `is_any_<type>()` for a group named `all_*`, and with
        `_not_` in place of `_without_` for more natural names, like
        {func}`~extra_platforms.is_unix_not_macos`.
        """
        return f"is_{self._any_stem}".replace("_without_", "_not_")

    @cached_property
    def skip_decorator_id(self) -> str:
        """ID of the Pytest skip decorator for this group.

        Named `@skip_<id>`, with `_not_` in place of `_without_`.
        """
        return f"skip_{self.id}".replace("_without_", "_not_")

    @cached_property
    def unless_decorator_id(self) -> str:
        """ID of the Pytest unless decorator for this group.

        Named `@unless_<id>`, `@unless_any_<type>` for a group named `all_*`, and
        with `_not_` in place of `_without_`.
        """
        return f"unless_{self._any_stem}".replace("_without_", "_not_")

    def _metadata_lines(self) -> list[str]:
        """The metadata list closing the generated docstring of the group."""
        lines = [
            *super()._metadata_lines(),
            f"- **Canonical**: ``{self.canonical}`` {'⬥' if self.canonical else ''}",
            *self._reference_lines(),
        ]
        if self:
            type_counts = Counter(type(member).__name__ for member in self)
            types = ", ".join(
                f"{count} {{class}}`~{class_name}`"
                for class_name, count in sorted(type_counts.items())
            )
            links = ", ".join(f"{{data}}`~{member.symbol_id}`" for member in self)
            lines.append(f"- **Members** ({types}): {links}")
        return lines

    @cached_property
    def member_ids(self) -> frozenset[str]:
        """A {class}`frozenset` of member IDs that belong to this group.

        Computed once: the members never change after `__post_init__`, and every
        trait asks each group for it when its docstring is generated.
        """
        return frozenset(self._members)

    def __hash__(self) -> int:
        """Hash based on group ID and member IDs."""
        return hash((self.id, self.member_ids))

    @cached_property
    def canonical(self) -> bool:
        """Return {data}`True` if the group is canonical (non-overlapping).

        A canonical group is one that does not share any members with other canonical
        groups. All canonical groups are non-overlapping.

        Non-canonical groups are provided for convenience, but overlap with each other
        or with canonical groups.

        ```{hint}
        Canonical groups are denoted with a ⬥ symbol in the documentation and tables.
        ```
        """
        # Avoid circular import.
        from .group_data import CANONICAL_GROUPS

        return self in CANONICAL_GROUPS

    def __iter__(self) -> Iterator[Trait]:
        """Iterate over the members of the group."""
        return iter(self._members.values())

    def __len__(self) -> int:
        """Return the number of members in the group.

        An empty group is falsy, like an empty {class}`set`.
        """
        return len(self._members)

    def __contains__(self, item: Trait | str) -> bool:
        """Test if a {class}`~extra_platforms.Trait` or its ID is in the group.

        A trait must equal the member of the same ID: one sharing the ID alone
        is not in the group.
        """
        if isinstance(item, str):
            return item in self._members
        return self._members.get(item.id) == item

    def __getitem__(self, member_id: str) -> Trait:
        """Return the trait whose ID is `member_id`."""
        try:
            return self._members[member_id]
        except KeyError:
            raise KeyError(f"No trait found whose ID is {member_id}") from None

    def items(self) -> Iterator[tuple[str, Trait]]:
        """Iterate over the traits of the group as key-value pairs."""
        return iter(self._members.items())

    def isdisjoint(self, other: _TNestedReferences) -> bool:
        """Return {data}`True` if the group has no members in common with `other`.

        Groups are disjoint if and only if their intersection is an empty {class}`set`.

        `other` can be an arbitrarily nested {class}`~collections.abc.Iterable` of
        {class}`~extra_platforms.Group` and {class}`~extra_platforms.Trait`.
        """
        return self._traits.isdisjoint(extract_members(other))

    def fullyintersects(self, other: _TNestedReferences) -> bool:
        """Return {data}`True` if the group has all members in common with `other`.

        This is the member-level equality test: the equivalent of ``==``
        between plain {class}`set` objects.

        ```{note}
        The name follows the {meth}`~Group.issubset` / {meth}`~Group.issuperset` /
        {meth}`~Group.isdisjoint` naming style of native {class}`set` methods.
        Python sets express this operation with the ``==`` operator, which
        {class}`~extra_platforms.Group` reserves for full identity comparison
        (ID, name, icon, and members).
        ```
        """
        return self._traits == set(extract_members(other))

    def issubset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other."""
        return self._traits.issubset(extract_members(other))

    __le__ = issubset

    def __lt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other, but not all."""
        return self._traits < set(extract_members(other))

    def issuperset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group."""
        return self._traits.issuperset(extract_members(other))

    __ge__ = issuperset

    def __gt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group, but not all."""
        return self._traits > set(extract_members(other))

    def union(self, *others: _TNestedReferences) -> Self:
        """Return a new {class}`~extra_platforms.Group` with members of all groups.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(members=self._traits.union(*map(extract_members, others)))

    # No __ior__ and friends: augmented assignments on this immutable class
    # fall back to the binary operators, which return new Group instances.
    __or__ = union

    def intersection(self, *others: _TNestedReferences) -> Self:
        """Return a new {class}`~extra_platforms.Group` with the shared members.

        A member is kept when the group and all others contain it.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=self._traits.intersection(*map(extract_members, others))
        )

    __and__ = intersection

    def difference(self, *others: _TNestedReferences) -> Self:
        """Return a new {class}`~extra_platforms.Group` without the others' members.

        A member is kept when the group contains it and no other does.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(members=self._traits.difference(*map(extract_members, others)))

    __sub__ = difference

    def symmetric_difference(self, other: _TNestedReferences) -> Self:
        """Return a new {class}`~extra_platforms.Group` with unshared members.

        A member is kept when either the group or other contains it, but not both.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=self._traits.symmetric_difference(extract_members(other))
        )

    __xor__ = symmetric_difference

    def copy(
        self,
        id: str | None = None,
        name: str | None = None,
        icon: str | None = None,
        members: Iterable[Trait] | None = None,
    ) -> Self:
        """Return a shallow copy of the group.

        Fields can be overridden by passing new values as arguments.
        """
        changes: dict[str, Any] = {
            "id": id,
            "name": name,
            "icon": icon,
            "members": members,
        }
        return replace(self, **{k: v for k, v in changes.items() if v is not None})

    def add(self, member: Trait | str) -> Self:
        """Return a new {class}`~extra_platforms.Group` with the specified trait added.

        If the trait is already in the group, returns a copy unchanged.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to add. A trait ID is case-insensitive, and can be an alias.
        :return: A new {class}`~extra_platforms.Group` instance with the
            trait added.
        :raises ValueError: If the string is not the ID of a trait, like the ID
            of a group.
        """
        if isinstance(member, str):
            member = _trait_from_id(member)
        return self.copy(members=self._traits | {member})

    def _member(self, member: Trait | str) -> Trait:
        """Return the member that `member` designates.

        :param member: A {class}`~extra_platforms.Trait` object, or a trait ID in
            any case, or an alias.
        :raises KeyError: If the trait is not in the group.
        """
        if isinstance(member, Trait):
            member_id = member.id
            found = member if member in self else None
        else:
            member_id = _resolve_alias(member.lower())
            found = self._members.get(member_id)
        if found is None:
            raise KeyError(f"Trait '{member_id}' is not in the group")
        return found

    def remove(self, member: Trait | str) -> Self:
        """Return a new {class}`~extra_platforms.Group` without the given trait.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to remove. A trait ID is case-insensitive, and can be an alias.
        :return: A new {class}`~extra_platforms.Group` instance with the
            trait removed.
        :raises KeyError: If the trait is not in the group.
        """
        return self.copy(members=self._traits - {self._member(member)})

    def discard(self, member: Trait | str) -> Self:
        """Return a new {class}`~extra_platforms.Group` without the trait, if present.

        Unlike {meth}`remove`, this does not raise an error if the trait
        is not found.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to remove.
        :return: A new {class}`~extra_platforms.Group` instance with the
            trait removed, or a copy if not present.
        """
        try:
            return self.remove(member)
        except KeyError:
            return self.copy()

    def pop(self, member_id: str | None = None) -> tuple[Trait, Self]:
        """Remove and return a trait from the group.

        :param member_id: Optional trait ID to remove. If not provided,
            removes an arbitrary trait (specifically, the first one in
            iteration order).
        :return: A {class}`tuple` of (removed {class}`~extra_platforms.Trait`,
            new {class}`~extra_platforms.Group`).
        :raises KeyError: If ``member_id`` is provided but not found in the
            group.
        :raises KeyError: If the group is empty.
        """
        if not self._members:
            raise KeyError("pop from an empty group")
        member = next(iter(self)) if member_id is None else self._member(member_id)
        return member, self.copy(members=self._traits - {member})

    def clear(self) -> Self:
        """Return a new empty {class}`~extra_platforms.Group` with the same metadata.

        :return: A new {class}`~extra_platforms.Group` instance with no
            members but same id, name, and icon.
        """
        return self.copy(members=())


# =============================================================================
# Lookup and reduction functions
# =============================================================================


def _unique(items: Iterable[_T]) -> tuple[_T, ...]:
    """Return a {class}`tuple` with duplicates removed, preserving order."""
    return tuple(dict.fromkeys(items))


@cache
def _group_lookup() -> dict[str, Group]:
    """Map group IDs to their {class}`~extra_platforms.Group` instances.

    Cached for O(1) lookups: the set of predefined groups is fixed once
    ``group_data`` is imported.
    """
    # Avoid circular import.
    from .group_data import ALL_GROUPS

    return {group.id: group for group in ALL_GROUPS}


@cache
def _alias_lookup() -> dict[str, str]:
    """Map each trait alias to the canonical ID of its trait."""
    # Avoid circular import.
    from .group_data import ALL_TRAITS

    return {alias: trait.id for trait in ALL_TRAITS for alias in trait.aliases}


@lru_cache(maxsize=128)
def _resolve_alias(id_: str) -> str:
    """Resolve an alias to its canonical ID, emitting a warning if an alias is used.

    Results are cached, so the warning is only emitted once per alias.

    :param id_: The ID to resolve (already lowercased).
    :return: The canonical ID if ``id_`` is an alias, otherwise ``id_`` unchanged.
    """
    canonical_id = _alias_lookup().get(id_)
    if canonical_id is None:
        return id_

    import warnings

    # Point the warning at the first caller outside the package: each public
    # entry point reaches here through a call chain of its own depth.
    frame = sys._getframe()
    stacklevel = 1
    while frame.f_back and frame.f_code.co_filename.startswith(_PACKAGE_DIR):
        frame = frame.f_back
        stacklevel += 1

    warnings.warn(
        f"'{id_}' is an alias for '{canonical_id}'. "
        f"Use the canonical ID '{canonical_id}' instead.",
        UserWarning,
        stacklevel=stacklevel,
    )
    return canonical_id


def _trait_from_id(trait_id: str) -> Trait:
    """Return the trait whose ID or alias is `trait_id`, in any case.

    :raises ValueError: If `trait_id` is not the ID of a trait.
    """
    # Avoid circular import.
    from .group_data import ALL_TRAIT_IDS, ALL_TRAITS

    resolved_id = _resolve_alias(trait_id.lower())
    if resolved_id not in ALL_TRAIT_IDS:
        raise ValueError(f"Unrecognized trait ID: {trait_id}")
    return ALL_TRAITS[resolved_id]


def traits_from_ids(*trait_and_group_ids: str) -> tuple[Trait, ...]:
    """Returns a deduplicated {class}`tuple` of traits matching the provided IDs.

    IDs are case-insensitive, and can refer to any traits or groups. Matching groups
    will be expanded to the {class}`~extra_platforms.Trait` instances they contain.

    Aliases are automatically resolved to their canonical IDs, with a warning emitted
    to encourage using the canonical ID directly.

    Order of the returned traits matches the order of the provided IDs.

    ```{tip}
    If you want to reduce the returned set and remove as much overlap as
    possible, you can use the {func}`~extra_platforms.reduce` function on the results.
    ```
    """
    # Avoid circular import.
    from .group_data import ALL_IDS, ALL_TRAIT_IDS, ALL_TRAITS

    # Normalize to lowercase and resolve aliases.
    ids = _unique(_resolve_alias(s.lower()) for s in trait_and_group_ids)
    if unrecognized_ids := set(ids) - ALL_IDS:
        raise ValueError(
            "Unrecognized group or trait IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    traits: list[Trait] = []
    for id_ in ids:
        if id_ in ALL_TRAIT_IDS:
            traits.append(ALL_TRAITS[id_])
        else:
            traits.extend(_group_lookup()[id_])
    return _unique(traits)


def groups_from_ids(*group_ids: str) -> tuple[Group, ...]:
    """Returns a deduplicated {class}`tuple` of groups matching the provided IDs.

    IDs are case-insensitive.

    Order of the returned {class}`~extra_platforms.Group` instances matches the order of
    the provided IDs.

    ```{tip}
    If you want to reduce the returned set and remove as much overlap as
    possible, you can use the {func}`~extra_platforms.reduce` function on the results.
    ```
    """
    # Avoid circular import.
    from .group_data import ALL_GROUP_IDS

    ids = _unique(s.lower() for s in group_ids)
    if unrecognized_ids := set(ids) - ALL_GROUP_IDS:
        raise ValueError(
            "Unrecognized group IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    return tuple(_group_lookup()[gid] for gid in ids)


def reduce(
    items: _TNestedReferences,
    target_pool: Iterable[Group | Trait] | None = None,
) -> frozenset[Group | Trait]:
    """Reduce a collection of traits to a minimal set.

    Returns a deduplicated set of {class}`~extra_platforms.Group` and
    {class}`~extra_platforms.Trait` that covers the same exact traits as the original
    input, but group as much traits as possible, to reduce the number of items.

    Only the groups defined in the `target_pool` are considered for the reduction.
    If no reference pool is provided, use all known groups. Empty groups cover
    nothing, and are never picked.

    ```{note}
    The algorithm is a variant of the [Set Cover
    Problem](https://en.wikipedia.org/wiki/Set_cover_problem), which is
    NP-hard. This implementation uses a [greedy
    approximation](https://en.wikipedia.org/wiki/Set_cover_problem#Greedy_algorithm)
    that iteratively selects the largest group fitting the remaining
    uncovered traits.
    ```
    """
    # Avoid circular import.
    from .group_data import ALL_GROUPS

    uncovered = set(extract_members(items))
    if not uncovered:
        return frozenset()

    # Candidates are the non-empty groups whose members are all in the input,
    # largest first, then by ID for determinism.
    candidates = sorted(
        (
            group
            for group in (ALL_GROUPS if target_pool is None else target_pool)
            if isinstance(group, Group) and group and group._traits <= uncovered
        ),
        key=lambda group: (-len(group), group.id),
    )

    # Greedy selection: keep a group only while all its members are uncovered.
    result: set[Group | Trait] = set()
    for group in candidates:
        if group._traits <= uncovered:
            result.add(group)
            uncovered -= group._traits

    # Add any remaining uncovered traits individually.
    result.update(uncovered)
    return frozenset(result)
