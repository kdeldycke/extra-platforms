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

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field, replace
from functools import cache, cached_property
from types import MappingProxyType
from typing import TypeVar, cast

from .trait import Trait, _Identifiable, _resolve_alias

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator

    from ._types import _TNestedReferences

_T = TypeVar("_T")


_MembersMapping = MappingProxyType[str, Trait]


def _all_group_suffix_to_type_id() -> dict[str, str]:
    """Map ``ALL_*`` group ID suffixes to their trait type IDs.

    Derived from {class}`~extra_platforms.Trait` and its subclasses, so an
    ``all_architectures`` group resolves to the singular ``architecture`` type
    ID (and likewise ``all_ci`` to ``ci``, ``all_traits`` to ``trait``, etc.).

    Rebuilt on each call rather than cached, so {class}`~extra_platforms.Trait`
    subclasses defined outside this package are picked up by the groups
    created after them.
    """
    return {
        cls.all_group.lower()[4:]: cls.type_id
        for cls in (Trait, *Trait.__subclasses__())
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
    for item in _flatten(other):
        match item:
            case None:
                continue
            case Trait():
                yield item
            case Group():
                yield from item._members.values()
            case str():
                yield from traits_from_ids(item)
            case _:
                raise TypeError(f"Unsupported type: {type(item)}")


@dataclass(frozen=True)
class Group(_Identifiable):
    """A {class}`~extra_platforms.Group` identifies a collection of
    {class}`~extra_platforms.Trait` members.

    Additionally of the common fields inherited from `_Identifiable`,
    each group provides:

    - `members`: An iterable of {class}`~extra_platforms.Trait`
      instances that belong to this group.
    - `member_ids`: A {class}`frozenset` of member IDs for quick lookup.
    - `canonical`: A {class}`bool` indicating if the group is canonical
      (non-overlapping).
    - various {class}`set`-like operations (union, intersection, difference, etc.).
    """

    unknown_symbol = "UNKNOWN"
    """Groups use `UNKNOWN` instead of `UNKNOWN_GROUP`."""

    members: Iterable[Trait] = field(repr=False, default_factory=tuple)
    """Traits in this group.

    Normalized to {class}`~types.MappingProxyType` at init, providing O(1) lookup by ID.
    """

    @property
    def _members(self) -> _MembersMapping:
        """Typed access to members as {class}`~types.MappingProxyType`.

        ```{warning}
        The `members` field is typed as {class}`~collections.abc.Iterable`
        to accept any iterable at construction time. After `__post_init__`,
        it is always a {class}`~types.MappingProxyType`. This property
        provides a {func}`~typing.cast` to that type, avoiding
        `# type: ignore` comments throughout the class.
        ```
        """
        return cast(_MembersMapping, self.members)

    def __post_init__(self):
        """Normalize members to a sorted, deduplicated mapping.

        ```{hint}
        Docstring generation is deferred to avoid circular imports during module
        initialization. See _docstrings._initialize_all_docstrings().
        ```
        """
        super().__post_init__()

        # Override detection_func_id and unless_decorator_id for groups
        # with "all_" prefix. Groups with "all_" prefix get "is_any_*"
        # detection functions and "unless_any_*" decorators (singular
        # form) to better convey the "any member matches" semantic.
        # Class-type groups (those matching Trait subclasses) use the subclass's
        # type_id.
        if self.id.startswith("all_"):
            suffix = self.id[4:]
            # Map the group suffix to a singular type_id, e.g. "architectures"
            # → "architecture", "platforms" → "platform", "traits" → "trait".
            suffix = _all_group_suffix_to_type_id().get(suffix, suffix)
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
        traits: Iterable[Trait]
        if isinstance(self.members, (MappingProxyType, dict)):
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

    def generate_docstring(self) -> str:
        """Generate comprehensive docstring for this group instance.

        Combines the attribute docstring from the source module with various metadata.
        """
        from extra_platforms._docstrings import get_attribute_docstring

        lines = []

        # Fetch attribute docstring from source module.
        source_docstring = get_attribute_docstring(
            f"extra_platforms.{self.data_module_id}", self.symbol_id
        )
        if source_docstring:
            lines.extend(source_docstring.strip().split("\n"))
            lines.append("")

        # Add metadata.
        lines.append(f"- **ID**: ``{self.id}``")
        lines.append(f"- **Name**: {self.name}")
        lines.append(f"- **Icon**: {self.icon}")
        lines.append(
            f"- **Canonical**: ``{self.canonical}`` {'⬥' if self.canonical else ''}"
        )
        lines.append(f"- **Detection function**: {{func}}`~{self.detection_func_id}`")
        lines.append(
            f"- **Pytest decorators**: {{deco}}`~pytest.{self.skip_decorator_id}` / "
            f"{{deco}}`~pytest.{self.unless_decorator_id}`"
        )

        # Add list of members with links to their definitions.
        member_links = [f"{{data}}`~{m.symbol_id}`" for m in self]
        type_counts = Counter(type(m).__name__ for m in self)

        if member_links:
            # Format type information with links.
            type_parts = [
                f"{count} {{class}}`~{class_name}`"
                for class_name, count in sorted(type_counts.items())
            ]
            type_info = ", ".join(type_parts)
            lines.append(f"- **Members** ({type_info}): {', '.join(member_links)}")

        return "\n".join(lines)

    @property
    def member_ids(self) -> frozenset[str]:
        """A {class}`frozenset` of member IDs that belong to this group."""
        return frozenset(self._members.keys())

    def __hash__(self) -> int:
        """Hash based on group ID and member IDs."""
        return hash((self.id, self.member_ids))

    @cached_property
    def canonical(self) -> bool:
        """Returns {data}`True` if the group is canonical (non-overlapping),
        {data}`False` otherwise.

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
        yield from self._members.values()

    def __len__(self) -> int:
        """Return the number of members in the group."""
        return len(self._members)

    def __bool__(self) -> bool:
        """Return {data}`True` if the group has members, {data}`False` otherwise."""
        return len(self._members) > 0

    def __contains__(self, item: Trait | str) -> bool:
        """Test if {class}`~extra_platforms.Trait` object or its ID is
        part of the group."""
        if isinstance(item, str):
            return item in self._members
        return item.id in self._members and self._members[item.id] == item

    def __getitem__(self, member_id: str) -> Trait:
        """Return the trait whose ID is `member_id`."""
        try:
            return self._members[member_id]
        except KeyError:
            raise KeyError(f"No trait found whose ID is {member_id}") from None

    def items(self) -> Iterator[tuple[str, Trait]]:
        """Iterate over the traits of the group as key-value pairs."""
        yield from self._members.items()

    def isdisjoint(self, other: _TNestedReferences) -> bool:
        """Return {data}`True` if the group has no members in common with `other`.

        Groups are disjoint if and only if their intersection is an empty {class}`set`.

        `other` can be an arbitrarily nested {class}`~collections.abc.Iterable` of
        {class}`~extra_platforms.Group` and {class}`~extra_platforms.Trait`.
        """
        return set(self._members.values()).isdisjoint(extract_members(other))

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
        return set(self._members.values()) == set(extract_members(other))

    def issubset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other."""
        return set(self._members.values()).issubset(extract_members(other))

    __le__ = issubset

    def __lt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in the group is in other, but not all."""
        other_members = set(extract_members(other))
        self_members = set(self._members.values())
        return self_members < other_members

    def issuperset(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group."""
        return set(self._members.values()).issuperset(extract_members(other))

    __ge__ = issuperset

    def __gt__(self, other: _TNestedReferences) -> bool:
        """Test whether every member in other is in the group, but not all."""
        other_members = set(extract_members(other))
        self_members = set(self._members.values())
        return self_members > other_members

    def union(self, *others: _TNestedReferences) -> Group:
        """Return a new {class}`~extra_platforms.Group` with members from
        the group and all others.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=set(self._members.values()).union(
                *(extract_members(other) for other in others)
            )
        )

    # No __ior__ and friends: augmented assignments on this immutable class
    # fall back to the binary operators, which return new Group instances.
    __or__ = union

    def intersection(self, *others: _TNestedReferences) -> Group:
        """Return a new {class}`~extra_platforms.Group` with members
        common to the group and all others.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=set(self._members.values()).intersection(
                *(extract_members(other) for other in others)
            )
        )

    __and__ = intersection

    def difference(self, *others: _TNestedReferences) -> Group:
        """Return a new {class}`~extra_platforms.Group` with members in the
        group that are not in the others.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=set(self._members.values()).difference(
                *(extract_members(other) for other in others)
            )
        )

    __sub__ = difference

    def symmetric_difference(self, other: _TNestedReferences) -> Group:
        """Return a new {class}`~extra_platforms.Group` with members in
        either the group or other but not both.

        ```{caution}
        The new {class}`~extra_platforms.Group` inherits the metadata of the
        first one. All other groups' metadata is ignored.
        ```
        """
        return self.copy(
            members=set(self._members.values()).symmetric_difference(
                extract_members(other)
            )
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

    def add(self, member: Trait | str) -> Group:
        """Return a new {class}`~extra_platforms.Group` with the specified trait added.

        If the trait is already in the group, returns a copy unchanged.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to add.
        :returns: A new {class}`~extra_platforms.Group` instance with the
            trait added.
        :raises ValueError: If the trait ID is not recognized.
        """
        if isinstance(member, str):
            member = traits_from_ids(member)[0]

        if member in self:
            return self.copy()

        return self.copy(members=set(self._members.values()) | {member})

    def remove(self, member: Trait | str) -> Group:
        """Return a new {class}`~extra_platforms.Group` with the specified
        trait removed.

        Raises {exc}`KeyError` if the trait is not in the group.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to remove.
        :returns: A new {class}`~extra_platforms.Group` instance with the
            trait removed.
        :raises KeyError: If the trait is not in the group.
        """
        member_id = member.id if isinstance(member, Trait) else member

        if member_id not in self._members:
            raise KeyError(f"Trait '{member_id}' is not in the group")

        return self.copy(
            members=tuple(t for tid, t in self._members.items() if tid != member_id)
        )

    def discard(self, member: Trait | str) -> Group:
        """Return a new {class}`~extra_platforms.Group` with the specified
        trait removed if present.

        Unlike {meth}`remove`, this does not raise an error if the trait
        is not found.

        :param member: A {class}`~extra_platforms.Trait` object or trait ID
            string to remove.
        :returns: A new {class}`~extra_platforms.Group` instance with the
            trait removed, or a copy if not present.
        """
        try:
            return self.remove(member)
        except KeyError:
            return self.copy()

    def pop(self, member_id: str | None = None) -> tuple[Trait, Group]:
        """Remove and return a trait from the group.

        :param member_id: Optional trait ID to remove. If not provided,
            removes an arbitrary trait (specifically, the first one in
            iteration order).
        :returns: A {class}`tuple` of (removed {class}`~extra_platforms.Trait`,
            new {class}`~extra_platforms.Group`).
        :raises KeyError: If ``member_id`` is provided but not found in the
            group.
        :raises KeyError: If the group is empty.
        """
        if not self._members:
            raise KeyError("pop from an empty group")

        if member_id is None:
            # Pop arbitrary (first) member.
            member_id = next(iter(self._members))

        # Raises KeyError if the trait is not in the group.
        new_group = self.remove(member_id)
        return self._members[member_id], new_group

    def clear(self) -> Group:
        """Return a new empty {class}`~extra_platforms.Group` with the same metadata.

        :returns: A new {class}`~extra_platforms.Group` instance with no
            members but same id, name, and icon.
        """
        return self.copy(members=())


# =============================================================================
# Lookup and reduction functions
# =============================================================================


def _unique(items: Iterable[_T]) -> tuple[_T, ...]:
    """Return a {class}`tuple` with duplicates removed, preserving order.

    This uses {meth}`dict.fromkeys` which:

    - Preserves insertion order (guaranteed since Python 3.7)
    - Removes duplicates ({class}`dict` keys are unique)
    """
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

    # Check for unrecognized IDs (aliases have already been resolved).
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
    unrecognized_ids = set(ids) - ALL_GROUP_IDS
    if unrecognized_ids:
        raise ValueError(
            "Unrecognized group IDs: " + ", ".join(sorted(unrecognized_ids))
        )
    return _unique(_group_lookup()[gid] for gid in ids)


def reduce(
    items: _TNestedReferences,
    target_pool: Iterable[Group | Trait] | None = None,
) -> frozenset[Group | Trait]:
    """Reduce a collection of traits to a minimal set.

    Returns a deduplicated set of {class}`~extra_platforms.Group` and
    {class}`~extra_platforms.Trait` that covers the same exact traits as the original
    input, but group as much traits as possible, to reduce the number of items.

    Only the groups defined in the `target_pool` are considered for the reduction.
    If no reference pool is provided, use all known groups.

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

    # Collect all traits.
    uncovered = set(extract_members(items))
    if not uncovered:
        return frozenset()

    # Build candidate groups: those that are subsets of the input traits.
    if target_pool is None:
        target_pool = ALL_GROUPS
    candidates = [
        g for g in target_pool if isinstance(g, Group) and g.issubset(uncovered)
    ]

    # Greedy selection: repeatedly pick the largest group that fits remaining traits.
    # Sort candidates by size (descending), then by ID for determinism.
    candidates.sort(key=lambda g: (-len(g), g.id))

    result: set[Group | Trait] = set()
    for group in candidates:
        # Only select if the group's members are all still uncovered.
        group_members = set(group)
        if group_members <= uncovered:
            result.add(group)
            uncovered -= group_members

    # Add any remaining uncovered traits individually.
    result.update(uncovered)

    return frozenset(result)
