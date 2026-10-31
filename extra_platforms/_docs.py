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
"""Markdown generators for the Sphinx trait and group pages.

Private, documentation-build-only helpers: they produce the Markdown tables and
Mermaid diagrams that the trait and group pages render live through
``click_extra.sphinx``'s ``{python:render}`` ``:mirror:`` blocks. Living inside
the installed package (rather than under ``docs/``) is what lets those blocks
import the generators when ``click-extra refresh-directives`` refreshes the
committed mirror regions offline, and when Sphinx regenerates them at build
time.

```{important}
This module is never imported by the package at runtime (``__init__`` does
not touch it), so ``extra_platforms`` keeps its dependency-free runtime. It
requires the ``docs`` dependency group (``click-extra``) and is only ever
imported while building or refreshing the documentation.
```
"""

from __future__ import annotations

from operator import attrgetter
from textwrap import dedent, indent

from click_extra import TableFormat, render_table

import extra_platforms

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from extra_platforms import Group, Trait


_GROUP_API_FUNCTIONS = (
    "extract_members",
    "groups_from_ids",
    "reduce",
    "traits_from_ids",
)
"""Trait and group operation functions documented in their own groups.md section.

Excluded from automodule directives so groups.md stays their canonical location.
"""


def generate_trait_table(
    traits: Iterable[Trait],
    *,
    include_type: bool = False,
    include_hint: bool = True,
) -> str:
    """Produce a Markdown table for a collection of traits.

    :param traits: The traits to include in the table.
    :param include_type: If ``True``, add a "Type" column showing each trait's
        class name.
    :param include_hint: If ``True``, append a hint block explaining the unknown
        trait for this trait type.  Requires all traits to be of the same class.
    """
    table_data = []
    headers = ["Icon", "Symbol", "Name", "Detection function"]
    alignments = ["center", "left", "left", "left"]
    if include_type:
        headers.append("Type")
        alignments.append("left")

    traits_list = list(traits)

    if include_hint:
        # All traits must be of the same class to produce the hint block.
        all_classes = {type(trait) for trait in traits_list}
        assert len(all_classes) == 1, (
            "All traits must be of the same class to generate a trait table."
        )
        trait_class = all_classes.pop()

    for trait in sorted(traits_list, key=attrgetter("id")):
        row = [
            trait.icon,
            f"{{data}}`~{trait.symbol_id}`",
            trait.name,
            f"{{func}}`~{trait.detection_func_id}`",
        ]
        if include_type:
            row.append(type(trait).__name__)
        table_data.append(row)

    table = render_table(
        table_data,
        headers,
        table_format=TableFormat.GITHUB,
        colalign=alignments,
    )

    if include_hint:
        unknown = f"{{data}}`~{trait_class.unknown_symbol}`"
        all_group = f"{{data}}`~{trait_class.all_group}`"
        resolver = f"{{func}}`~current_{trait_class.type_id}`"
        name = trait_class.type_name
        hint = dedent(f"""
            ```{{hint}}
            The {unknown} trait represents an unrecognized
            {name}. It is not included in the {all_group} group,
            and will be returned by {resolver} if the current
            {name} is not recognized.
            ```""")
        table = f"{table}\n{hint}"

    return table


def generate_group_table(groups: Iterable[Group]) -> str:
    """Produce a Markdown table for a collection of groups.

    The table contains the icon, symbol with link to documentation, description,
    a linked detection function, and canonical status for each group.
    A hint block is appended after the table to explain canonical groups.

    :param groups: The groups to include in the table.
    """
    headers = [
        "Icon",
        "Symbol",
        "Description",
        "[Detection](detection.md)",
        "{attr}`Canonical <Group.canonical>`",
    ]
    alignments = ["center", "left", "left", "left", "center"]

    sorted_groups = sorted(groups, key=attrgetter("id"))
    table_data = [
        [
            group.icon,
            f"{{data}}`~{group.symbol_id}`",
            group.name,
            f"{{func}}`~{group.detection_func_id}`",
            "⬥" if group.canonical else "",
        ]
        for group in sorted_groups
    ]

    table = render_table(
        table_data, headers, table_format=TableFormat.GITHUB, colalign=alignments
    )

    # Append hint block explaining canonical groups
    if len(sorted_groups) > 1:
        hint = dedent("""
            ```{hint}
            Canonical groups are non-overlapping groups that together cover all
            recognized traits. They are marked with a ⬥ icon in the table above.

            Other groups are provided for convenience, but overlap with each other or
            with canonical groups.
            ```""")
        table = f"{table}\n{hint}"

    return table


def _analyze_group_hierarchy(
    groups: Iterable[Group],
) -> tuple[Group, list[Group], list]:
    """Analyze a collection of groups to identify the superset and missing traits.

    :param groups: An iterable of groups including both the superset group (like
        `ALL_ARCHITECTURES` or `ALL_PLATFORMS`) and intermediate groups.
    :returns: A tuple of ``(superset, intermediate_groups, missing_traits)`` where:

        - ``superset``: The group that contains all others as subsets
        - ``intermediate_groups``: All groups except the superset
        - ``missing_traits``: Traits in the superset not covered by any
          intermediate group
    :raises ValueError: If no superset group is found among the inputs.
    """
    groups_list = list(groups)

    # Find the superset group (the one that contains all others as subsets).
    supersets = [
        g
        for g in groups_list
        if all(g >= other for other in groups_list if other.id != g.id)
    ]

    if not supersets:
        raise ValueError(
            "No superset group found. The input must include a group that "
            "contains all members of other groups, like ALL_ARCHITECTURES or "
            "ALL_PLATFORMS."
        )

    superset = supersets[0]

    # Separate intermediate groups from the superset.
    intermediate_groups = [g for g in groups_list if g.id != superset.id]

    # Compute the union of all intermediate groups to find missing traits.
    union_of_intermediate: set[str] = set()
    for group in intermediate_groups:
        union_of_intermediate.update(group.member_ids)

    # Find traits in the superset that aren't covered by any intermediate group.
    missing_trait_ids = superset.member_ids - union_of_intermediate
    missing_traits = sorted(
        [superset[tid] for tid in missing_trait_ids],
        key=lambda t: t.id,
    )

    return superset, intermediate_groups, missing_traits


def generate_sankey(groups: Iterable[Group]) -> str:
    """Produce a Sankey diagram showing trait hierarchy.

    ```{warning}
    Output must stay compatible with the Mermaid version bundled in
    ``sphinxcontrib-mermaid``. See module docstring for details.
    ```

    The diagram shows connections from a top-level (superset) group to intermediate
    groups to their individual members. The weights of the first layer reflect the
    number of members in each intermediate group. Missing traits (present in the
    superset but not in any intermediate group) are shown as direct children of
    the superset, placed at the end of the diagram specification.

    :param groups: An iterable of groups including both the superset group (like
        `ALL_ARCHITECTURES` or `ALL_PLATFORMS`) and intermediate groups to
        display (like `CANONICAL_GROUPS & ALL_ARCHITECTURE_GROUPS`).
    :raises ValueError: If no superset group is found among the inputs.

    Nodes carry their bare ``symbol_id`` as label, because the Mermaid Sankey
    parser accepts ASCII characters only. The `{todo}` to label them with their
    icons is in `docs/architectures.md`, where the todo list collects it.
    """
    superset, intermediate_groups, missing_traits = _analyze_group_hierarchy(groups)

    sorted_intermediates = sorted(
        intermediate_groups, key=lambda g: (len(g), g.id), reverse=True
    )

    table = []

    # First layer: superset -> intermediate groups (weight = number of members
    # in group).
    for group in sorted_intermediates:
        member_count = len(group)
        table.append(f"{superset.symbol_id},{group.symbol_id},{member_count}")

    # Second layer: intermediate groups -> their members (weight = 1 each).
    for group in sorted_intermediates:
        # Bare symbol IDs: Mermaid Sankey diagrams do not support emoji
        # labels. See the docstring above.
        table.extend(f"{group.symbol_id},{member.symbol_id},1" for member in group)

    # Third layer: superset -> missing traits (weight = 1 each), placed at the end.
    table.extend(
        f"{superset.symbol_id},{trait.symbol_id},1" for trait in missing_traits
    )
    output = dedent("""\
        ```mermaid
        ---
        config: {"sankey": {"showValues": false, "width": 800, "height": 800}}
        ---
        sankey-beta\n
        """)
    output += "\n".join(table)
    output += "\n```"
    return output


def generate_traits_mindmap(groups: Iterable[Group]) -> str:
    """Produce a mindmap hierarchy to show the hierarchy of groups and their traits.

    ```{warning}
    Output must stay compatible with the Mermaid version bundled in
    ``sphinxcontrib-mermaid``. See module docstring for details.
    ```

    Includes missing traits (present in the superset but not in any intermediate group)
    as direct children of the superset.

    :param groups: An iterable of groups including both the superset group (like
        `ALL_ARCHITECTURES` or `ALL_PLATFORMS`) and intermediate groups to
        display (like `CANONICAL_GROUPS & ALL_ARCHITECTURE_GROUPS`).
    :raises ValueError: If no superset group is found among the inputs.
    """
    superset, intermediate_groups, missing_traits = _analyze_group_hierarchy(groups)

    group_map = ""
    for group in sorted(intermediate_groups, key=attrgetter("id"), reverse=True):
        group_map += f"){group.icon} {group.symbol_id}(\n"
        for member in group:
            group_map += f"    ({member.icon} {member.symbol_id})\n"

    # Add missing traits as direct children of the superset.
    for trait in missing_traits:
        group_map += f"({trait.icon} {trait.symbol_id})\n"
    name = f"{superset.icon} {superset.symbol_id}"
    output = dedent(f"""\
        ```mermaid
        ---
        config: {{"mindmap": {{"padding": 5}}}}
        ---
        mindmap
            (({name}))
        """)
    output += indent(group_map, " " * 8)
    output += "```"
    return output


def generate_decorators_table(objects: Iterable[Trait | Group]) -> str:
    """Produce a Markdown table for pytest decorators.

    The table contains the skip decorator (linked), unless decorator (linked),
    icon, and source symbol link for each trait or group.
    """
    headers = ["Skip decorator", "Unless decorator", "Icon", "Associated symbol"]
    alignments = ["left", "left", "center", "left"]

    table_data = [
        [
            f"{{deco}}`~pytest.{obj.skip_decorator_id}`",
            f"{{deco}}`~pytest.{obj.unless_decorator_id}`",
            obj.icon,
            f"{{data}}`~{obj.symbol_id}`",
        ]
        for obj in sorted(objects, key=attrgetter("id"))
    ]

    return render_table(
        table_data, headers, table_format=TableFormat.GITHUB, colalign=alignments
    )


def generate_all_detection_function_table(objects: Iterable[Trait | Group]) -> str:
    """Generate a combined Markdown table for all detection functions.

    This produces a single table listing all detection functions for both
    individual traits (is_macos, is_ubuntu, etc.) and groups (is_linux, is_unix, etc.),
    sorted by function name.

    :param objects: The traits and groups whose detection functions should be
        included.
    :returns: A Markdown table with all detection functions.
    """
    headers = ["Detection function", "Icon", "Associated symbol"]
    alignments = ["left", "center", "left"]

    table_data = [
        [
            f"{{func}}`~{obj.detection_func_id}`",
            obj.icon,
            f"{{data}}`~{obj.symbol_id}`",
        ]
        for obj in sorted(objects, key=attrgetter("detection_func_id"))
    ]

    return render_table(
        table_data, headers, table_format=TableFormat.GITHUB, colalign=alignments
    )


def generate_sphinx_directives(
    objects: Iterable[Trait | Group],
    directive: str,
    attr: str,
) -> str:
    """Generate Sphinx autodoc directives for a collection of traits or groups.

    Produces a MyST ``{eval-rst}`` block with one directive line per object.

    ```{note}
    Autodoc directives (``autodata``, ``autofunction``, ``autoclass``, etc.)
    cannot be used as native MyST directives. They perform internal rST nested
    parsing that requires an rST parser context only ``{eval-rst}`` provides.
    See [executablebooks/MyST-Parser#587](https://github.com/executablebooks/MyST-Parser/issues/587),
    [executablebooks/MyST-Parser#228](https://github.com/executablebooks/MyST-Parser/issues/228)
    and [executablebooks/MyST-Parser#1119](https://github.com/executablebooks/MyST-Parser/issues/1119).
    ```

    :param objects: The traits or groups to generate directives for.
    :param directive: The Sphinx directive name, like ``"autodata"`` or
        ``"autofunction"``.
    :param attr: The attribute name on each object that provides the qualified
        identifier, like ``"symbol_id"`` or ``"detection_func_id"``.
    """
    objects_list = list(objects)
    if not objects_list:
        return "```{eval-rst}\n```"

    directives = [
        f".. {directive}:: extra_platforms.{getattr(obj, attr)}"
        for obj in sorted(objects_list, key=attrgetter("id"))
    ]

    joined = "\n".join(directives)
    return f"```{{eval-rst}}\n{joined}\n```"


def generate_pytest_decorator_autodata(objects: Iterable[Trait | Group]) -> str:
    """Generate Sphinx autodecorator directives for pytest decorators.

    Generates directives for both ``@skip_<id>`` and ``@unless_<id>`` decorators
    defined in the ``extra_platforms.pytest`` module, organized in separate sections.

    Uses ``{eval-rst}`` for the same reason as {func}`generate_sphinx_directives`.
    """
    sorted_objects = sorted(objects, key=attrgetter("id"))

    pairs = (
        ("Skip decorators", "skip_decorator_id"),
        ("Unless decorators", "unless_decorator_id"),
    )

    def _directive_section(title: str, directives: Iterable[str]) -> str:
        joined = "\n".join(directives)
        return f"## {title}\n\n```{{eval-rst}}\n{joined}\n```"

    sections = (
        _directive_section(
            name,
            (
                f".. autodecorator:: extra_platforms.pytest.{getattr(o, attr)}"
                for o in sorted_objects
            ),
        )
        for name, attr in pairs
    )

    return "\n\n".join(sections)


def generate_group_module_automodule() -> str:
    """Generate the extra_platforms.group automodule for groups.md.

    Excludes Group class and utility functions that are documented separately
    in the same file. Uses ``{eval-rst}`` for the same reason as
    {func}`generate_sphinx_directives`.
    """
    # Exclude Group class (documented via autoclass) and utility functions
    # (documented in "Trait and group operations" section).
    exclude_list = ["Group", *_GROUP_API_FUNCTIONS]

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: extra_platforms.group
           :members:
           :undoc-members:
           :show-inheritance:
           :exclude-members: {exclude_members}
        ```""")


def generate_group_data_module_automodule(groups: Iterable[Group]) -> str:
    """Generate the extra_platforms.group_data automodule for groups.md.

    Excludes all Group instances and frozenset collections that are documented
    separately in the same file. Uses ``{eval-rst}`` for the same reason as
    {func}`generate_sphinx_directives`.

    :param groups: All predefined groups to exclude.
    """
    from extra_platforms import group_data

    # Exclude all Group instances (documented in "Predefined groups" section).
    # Group IDs are lowercase but Python symbols are uppercase.
    exclude_list = [g.id.upper() for g in groups]

    # Exclude frozenset collections (documented in "Group collections" and
    # "ID collections" sections). Discovered from the module itself so new
    # collections are excluded automatically.
    exclude_list.extend(
        name
        for name, value in vars(group_data).items()
        if name.isupper() and isinstance(value, frozenset)
    )

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: extra_platforms.group_data
           :exclude-members: {exclude_members}
        ```""")


def generate_extra_platforms_automodule() -> str:
    """Generate the extra_platforms automodule directive, without its callables.

    Every function and class exported at the root of the package is documented on
    a dedicated page: detection functions in detection.md, group operations in
    groups.md, {func}`~extra_platforms.shell_from_path` in shells.md, and the
    classes in trait.md and groups.md. This automodule renders the data alone:
    the traits, the groups and their collections.

    Uses ``{eval-rst}`` for the same reason as {func}`generate_sphinx_directives`.
    """
    exclude_members = ", ".join(
        sorted(
            name
            for name in extra_platforms.__all__
            if callable(getattr(extra_platforms, name))
        )
    )

    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: extra_platforms
           :members:
           :show-inheritance:
           :undoc-members:
           :exclude-members: {exclude_members}
        ```""")
