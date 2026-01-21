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
"""Automation to keep extra-platforms documentation up-to-date.

.. tip::

    When the module is called directly, it will update all documentation files in-place:

    .. code-block:: shell-session

        $ run python -m extra_platforms.docs_update

    See how it is `used in .github/workflows/docs.yaml workflow
    <https://github.com/kdeldycke/extra-platforms/blob/main/.github/workflows/docs.yaml#L38-L39>`_.
"""

from __future__ import annotations

import re
import sys
from itertools import chain
from operator import attrgetter
from pathlib import Path
from textwrap import dedent, indent
from typing import Iterable

import wcwidth  # type: ignore[import-untyped]
from wcmatch import glob as wcglob

from extra_platforms import (
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUPS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_TRAITS,
    ARCH_32_BIT,
    ARCH_64_BIT,
    NON_OVERLAPPING_GROUPS,
    UNKNOWN_ARCHITECTURE,
    UNKNOWN_CI,
    UNKNOWN_PLATFORM,
    Group,
)
from extra_platforms.trait import Trait

DOCS_ROOT = Path(__file__).parent
"""The root path of Sphinx documentation."""

PROJECT_ROOT = DOCS_ROOT.parent
"""The root path of the project."""

README_PATH = PROJECT_ROOT / "readme.md"
"""The path to the ``readme.md`` file."""


def _visible_width(s: str) -> int:
    """Return the display width of a string, accounting for unicode characters.

    Uses wcwidth to calculate the proper display width of unicode and emoji characters.
    """
    width = wcwidth.wcswidth(s)
    # wcswidth returns -1 for control characters; fall back to len() in that case.
    return len(s) if width < 0 else width


def replace_content(
    filepath: Path | Iterable[Path],
    start_tag: str,
    end_tag: str,
    new_content: str,
) -> None:
    """Replace in the provided files the content surrounded by the provided tags.

    Tags are specified as simple names (e.g., "architecture-table-start") and will be
    matched with flexible whitespace handling. Supports both HTML comment format
    (``<!-- tag -->``) for Markdown and rST comment format (``.. tag``) for rST files.
    """
    if isinstance(filepath, Path):
        path_list = [filepath]
    else:
        path_list = list(filepath)

    for filepath in path_list:
        filepath = filepath.resolve()
        assert filepath.exists(), f"File {filepath} does not exist."
        assert filepath.is_file(), f"File {filepath} is not a file."

        orig_content = filepath.read_text(encoding="utf-8")
        is_rst = filepath.suffix == ".rst"

        if is_rst:
            # rST comment format: .. tag
            start_pattern = re.compile(
                rf"\.\.\s+{re.escape(start_tag)}\s*",
                re.MULTILINE | re.DOTALL,
            )
            end_pattern = re.compile(
                rf"\s*\.\.\s+{re.escape(end_tag)}",
                re.MULTILINE | re.DOTALL,
            )
            start_tag_formatted = f".. {start_tag}\n\n"
            end_tag_formatted = f"\n\n.. {end_tag}"
        else:
            # HTML comment format: <!-- tag -->
            start_pattern = re.compile(
                rf"<!--\s*{re.escape(start_tag)}\s*-->\s*",
                re.MULTILINE | re.DOTALL,
            )
            end_pattern = re.compile(
                rf"\s*<!--\s*{re.escape(end_tag)}\s*-->",
                re.MULTILINE | re.DOTALL,
            )
            start_tag_formatted = f"<!-- {start_tag} -->\n\n"
            end_tag_formatted = f"\n\n<!-- {end_tag} -->"

        # Find start tag.
        start_match = start_pattern.search(orig_content)
        if not start_match:
            continue

        # Split at start tag.
        pre_content = orig_content[: start_match.start()]
        after_start = orig_content[start_match.end() :]

        # Find end tag.
        end_match = end_pattern.search(after_start)
        if not end_match:
            continue

        # Split at end tag.
        post_content = after_start[end_match.end() :]

        filepath.write_text(
            f"{pre_content}{start_tag_formatted}{new_content}{end_tag_formatted}{post_content}",
            encoding="utf-8",
        )


def _generate_markdown_table(
    table_data: list[list[str]],
    headers: list[str],
    alignments: list[str],
) -> str:
    """Generate a Markdown table using tabulate with custom alignment separators.

    This is a shared helper function that both generate_trait_table() and
    generate_group_table() use to render tables with proper Markdown alignment hints.

    Uses display width (not character count) for proper unicode/emoji padding,
    matching the behavior of mdformat linter.

    Args:
        table_data: List of rows, where each row is a list of cell values.
        headers: List of column header names.
        alignments: List of alignment hints ("left", "right", "center") for each column.

    Returns:
        A formatted Markdown table string with proper alignment separators.
    """
    # Calculate column widths based on display width (for proper unicode/emoji handling).
    # This matches the behavior of mdformat linter.
    col_widths = []
    for col_index, header in enumerate(headers):
        cells = [row[col_index] for row in table_data] + [header]
        col_widths.append(max(_visible_width(c) for c in cells))

    # Build separator row with proper alignment hints.
    # https://github.com/astanin/python-tabulate/pull/261
    # https://github.com/astanin/python-tabulate/issues/53
    separators = []
    for col_index, width in enumerate(col_widths):
        align = alignments[col_index]
        if align == "left":
            sep = f":{'-' * (width - 1)}"
        elif align == "center":
            sep = f":{'-' * (width - 2)}:"
        elif align == "right":
            sep = f"{'-' * (width - 1)}:"
        else:
            sep = "-" * width
        separators.append(sep)

    # Build all rows with proper display-width-based padding.
    def pad_cell(content: str, width: int, align: str) -> str:
        """Pad a cell to the target display width with proper alignment."""
        content_width: int = _visible_width(content)
        padding_needed: int = width - content_width
        if align == "center":
            left_pad: int = padding_needed // 2
            right_pad: int = padding_needed - left_pad
            result: str = " " * left_pad + content + " " * right_pad
            return result
        elif align == "right":
            result = " " * padding_needed + content
            return result
        else:  # left or default
            result = content + " " * padding_needed
            return result

    # Build header row.
    header_cells = [
        pad_cell(h, col_widths[i], alignments[i]) for i, h in enumerate(headers)
    ]

    # Build data rows.
    data_rows = []
    for row in table_data:
        row_cells = [
            pad_cell(cell, col_widths[i], alignments[i]) for i, cell in enumerate(row)
        ]
        data_rows.append(row_cells)

    # Assemble the table.
    lines = []
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(separators) + " |")
    for row_cells in data_rows:
        lines.append("| " + " | ".join(row_cells) + " |")

    return "\n".join(lines)


def generate_all_traits_table(traits: Iterable[Trait]) -> str:
    """Produce a simple Markdown table for a collection of traits.

    Similar to group tables, contains icon, symbol, type, name, and detection function.
    """
    table_data = []
    headers = ["Icon", "Symbol", "Name", "Detection function", "Type"]
    alignments = ["center", "left", "left", "left", "left"]

    traits_list = list(traits)
    for trait in sorted(traits_list, key=attrgetter("id")):
        table_data.append([
            trait.icon,
            f"{{data}}`~{trait.symbol_id}`",
            trait.name,
            f"{{func}}`~{trait.detection_func_id}`",
            type(trait).__name__,
        ])

    return _generate_markdown_table(table_data, headers, alignments)


def generate_trait_table(traits: Iterable[Trait]) -> str:
    """Produce a Markdown table for a collection of traits.

    The table contains the icon, the symbol constant name (linked to its full definition),
    a linked name, and a linked detection function for each trait. A hint block is appended
    after the table explaining the unknown trait for this trait type.
    """
    table_data = []
    headers = ["Icon", "Symbol", "Name", "Detection function"]
    alignments = ["center", "left", "left", "left"]

    # Get metadata from the first trait (all traits in the table should be the
    # same type).
    traits_list = list(traits)
    all_classes = {type(trait) for trait in traits_list}
    assert len(all_classes) == 1, (
        "All traits must be of the same class to generate a trait table."
    )
    trait_class = all_classes.pop()

    for trait in sorted(traits_list, key=attrgetter("id")):
        table_data.append([
            trait.icon,
            f"{{data}}`~{trait.symbol_id}`",
            trait.name,
            f"{{func}}`~{trait.detection_func_id}`",
        ])

    table = _generate_markdown_table(table_data, headers, alignments)

    # Append hint block explaining unknown trait if trait type was detected.
    hint = dedent(f"""
        ```{{hint}}
        The {{data}}`~{trait_class.unknown_symbol}` trait represents an unrecognized
        {trait_class.type_name}. It is not included in the {{data}}`~{trait_class.all_group}` group,
        and will be returned by {{func}}`~current_{trait_class.type_id}` if the current
        {trait_class.type_name} is not recognized.
        ```""")
    return f"{table}\n{hint}"


def generate_group_table(groups: Iterable[Group]) -> str:
    """Produce a Markdown table for a collection of groups.

    The table contains the icon, symbol with link to documentation, description,
    a linked detection function, and canonical status for each group.
    A hint block is appended after the table to explain canonical groups.

    Args:
        groups: The groups to include in the table.
    """
    table_data = []
    headers = [
        "Icon",
        "Symbol",
        "Description",
        "[Detection](detection.md)",
        "[Canonical](groups.md#extra_platforms.group.Group.canonical)",
    ]
    alignments = ["center", "left", "left", "left", "center"]

    sorted_groups = sorted(groups, key=attrgetter("id"))
    for group in sorted_groups:
        table_data.append([
            group.icon,
            f"{{data}}`~{group.symbol_id}`",
            group.name,
            f"{{func}}`~{group.detection_func_id}`",
            "⬥" if group.canonical else "",
        ])

    table = _generate_markdown_table(table_data, headers, alignments)

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

    Args:
        groups: An iterable of groups including both the superset group (e.g.,
                ALL_ARCHITECTURES, ALL_PLATFORMS) and intermediate groups.

    Returns:
        A tuple of (superset, intermediate_groups, missing_traits) where:
        - superset: The group that contains all others as subsets
        - intermediate_groups: All groups except the superset, sorted by size (descending)
        - missing_traits: Traits in the superset not covered by any intermediate group

    Raises:
        ValueError: If no superset group is found among the inputs.
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
            "contains all members of other groups (e.g., ALL_ARCHITECTURES, "
            "ALL_PLATFORMS)."
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

    The diagram shows connections from a top-level (superset) group to intermediate
    groups to their individual members. The weights of the first layer reflect the
    number of members in each intermediate group. Missing traits (present in the
    superset but not in any intermediate group) are shown as direct children of
    the superset, placed at the end of the diagram specification.

    Args:
        groups: An iterable of groups including both the superset group (e.g.,
                ALL_ARCHITECTURES, ALL_PLATFORMS) and intermediate groups to
                display (e.g., NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS).

    Raises:
        ValueError: If no superset group is found among the inputs.
    """
    superset, intermediate_groups, missing_traits = _analyze_group_hierarchy(groups)

    table = []

    # First layer: superset -> intermediate groups (weight = number of members
    # in group).
    for group in sorted(
        intermediate_groups, key=lambda g: (len(g), g.id), reverse=True
    ):
        member_count = len(group)
        table.append(f"{superset.symbol_id},{group.symbol_id},{member_count}")

    # Second layer: intermediate groups -> their members (weight = 1 each).
    for group in sorted(
        intermediate_groups, key=lambda g: (len(g), g.id), reverse=True
    ):
        for member in group._members.values():
            # XXX Sankey diagrams do not support emoji icons yet.
            # table.append(
            #     f'"{html.escape(group.icon)} {group.id}",'
            #     f'"{html.escape(member.icon)} {member_id}",1'
            # )
            table.append(f"{group.symbol_id},{member.symbol_id},1")

    # Third layer: superset -> missing traits (weight = 1 each), placed at the end.
    for trait in missing_traits:
        table.append(f"{superset.symbol_id},{trait.symbol_id},1")
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

    Includes missing traits (present in the superset but not in any intermediate group)
    as direct children of the superset.

    Args:
        groups: An iterable of groups including both the superset group (e.g.,
                ALL_ARCHITECTURES, ALL_PLATFORMS) and intermediate groups to
                display (e.g., NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS).

    Raises:
        ValueError: If no superset group is found among the inputs.
    """
    superset, intermediate_groups, missing_traits = _analyze_group_hierarchy(groups)

    group_map = ""
    for group in sorted(intermediate_groups, key=attrgetter("id"), reverse=True):
        group_map += f"){group.icon} {group.symbol_id}(\n"
        for platform in group:
            group_map += f"    ({platform.icon} {platform.symbol_id})\n"

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
    table_data = []
    headers = ["Skip decorator", "Unless decorator", "Icon", "Associated symbol"]
    alignments = ["left", "left", "center", "left"]

    for obj in sorted(objects, key=attrgetter("id")):
        table_data.append([
            f"{{func}}`~pytest.{obj.skip_decorator_id}`",
            f"{{func}}`~pytest.{obj.unless_decorator_id}`",
            obj.icon,
            f"{{data}}`~{obj.symbol_id}`",
        ])

    return _generate_markdown_table(table_data, headers, alignments)


def generate_autodata_directives(traits: Iterable[Trait | Group]) -> str:
    """Generate Sphinx autodata directives for a collection of traits or groups.

    This produces a code block with ``.. autodata::`` directives for each trait,
    allowing Sphinx to document module-level constants with their dynamic docstrings.

    The module name is automatically determined from the trait type.

    Args:
        traits: The traits or groups to generate directives for.

    Returns:
        A MyST-compatible code block containing the autodata directives.
    """
    traits_list = list(traits)
    if not traits_list:
        return "```{eval-rst}\n```"

    directives = []
    for trait in sorted(traits_list, key=attrgetter("id")):
        directives.append(f".. autodata:: extra_platforms.{trait.symbol_id}")

    joined = "\n".join(directives)
    return f"```{{eval-rst}}\n{joined}\n```"


def generate_all_detection_function_table(objects: Iterable[Trait | Group]) -> str:
    """Generate a combined Markdown table for all detection functions.

    This produces a single table listing all detection functions for both
    individual traits (is_macos, is_ubuntu, etc.) and groups (is_linux, is_unix, etc.),
    sorted by function name.

    Args:
        objects: The traits and groups whose detection functions should be included.

    Returns:
        A Markdown table with all detection functions.
    """
    table_data = []
    headers = ["Detection function", "Icon", "Associated symbol"]
    alignments = ["left", "center", "left"]

    for obj in sorted(objects, key=attrgetter("detection_func_id")):
        table_data.append([
            f"{{func}}`~{obj.detection_func_id}`",
            obj.icon,
            f"{{data}}`~{obj.symbol_id}`",
        ])

    return _generate_markdown_table(table_data, headers, alignments)


def generate_detection_autofunction(objects: Iterable[Trait | Group]) -> str:
    """Generate Sphinx autofunction directives for detection functions.

    Generates directives for both trait detection functions (``is_<trait>()``)
    defined in the ``detection`` module and group detection functions
    (``is_<group>()``) dynamically generated in the ``extra_platforms`` package.

    Args:
        objects: The traits or groups whose detection functions should be documented.

    Returns:
        A MyST-compatible code block containing the autofunction directives with
        links to their associated symbols.
    """
    objects_list = list(objects)
    if not objects_list:
        return "```{eval-rst}\n```"

    # Generate autofunction directives with associated symbol links
    directives = []
    for obj in sorted(objects_list, key=attrgetter("id")):
        directives.append(f".. autofunction:: extra_platforms.{obj.detection_func_id}")

    output = "```{eval-rst}\n"
    output += "\n".join(directives)
    output += "\n```"
    return output


def generate_pytest_decorator_autodata(objects: Iterable[Trait | Group]) -> str:
    """Generate Sphinx autodecorator directives for pytest decorators.

    Generates directives for both ``@skip_<id>`` and ``@unless_<id>`` decorators
    defined in the ``extra_platforms.pytest`` module, organized in separate sections.

    Uses the built-in ``autodecorator`` directive which renders decorator names with @ prefix.
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


def generate_pytest_automodule(objects: Iterable[Trait | Group]) -> str:
    """Generate the pytest automodule directive with dynamically excluded members.

    This excludes all dynamically generated decorators from the automodule output,
    since they are documented separately via autodata directives in a dedicated section.

    Args:
        objects: The traits or groups whose decorators should be excluded.

    Returns:
        A MyST-compatible code block containing the automodule directive.
    """
    objects_list = list(objects)

    exclude_list = [
        decorator_id
        for obj in sorted(objects_list, key=attrgetter("id"))
        for decorator_id in (obj.skip_decorator_id, obj.unless_decorator_id)
    ]

    exclude_members = ", ".join(exclude_list)

    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: extra_platforms.pytest
           :members:
           :undoc-members:
           :show-inheritance:
           :exclude-members: {exclude_members}
        ```""")


def generate_group_automodule() -> str:
    """Generate the extra_platforms.group automodule directive with excluded members.

    This excludes utility functions that are documented in groups.md.

    Returns:
        An rST automodule directive with exclude-members.
    """
    # Exclude utility functions documented in groups.md.
    exclude_list = [
        "groups_from_ids",
        "reduce",
        "traits_from_ids",
    ]

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        .. automodule:: extra_platforms.group
           :members:
           :show-inheritance:
           :undoc-members:
           :exclude-members: {exclude_members}""")


def generate_trait_automodule() -> str:
    """Generate the extra_platforms.trait automodule directive with excluded members.

    This excludes core classes that are documented in trait.md.

    Returns:
        An rST automodule directive with exclude-members.
    """
    # Exclude core classes documented in trait.md.
    exclude_list = [
        "Architecture",
        "CI",
        "Platform",
        "Trait",
    ]

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        .. automodule:: extra_platforms.trait
           :members:
           :show-inheritance:
           :undoc-members:
           :exclude-members: {exclude_members}""")


def generate_extra_platforms_automodule(objects: Iterable[Trait | Group]) -> str:
    """Generate the extra_platforms automodule directive with excluded members.

    This excludes detection functions, utility functions, and core classes from the
    automodule output, since they are documented in other files:
    - Detection functions in detection.md ({{func}} → detection.html)
    - Utility functions in detection.md and groups.md ({{func}} → detection.html, groups.html)
    - Core classes in trait.md and groups.md ({{class}} → trait.html, groups.html)

    Args:
        objects: The traits and groups whose detection functions should be excluded.

    Returns:
        An rST automodule directive with exclude-members.
    """
    objects_list = list(objects)

    # Exclude all detection functions so detection.md is the canonical location.
    exclude_list = [
        obj.detection_func_id for obj in sorted(objects_list, key=attrgetter("id"))
    ]

    # Also exclude utility functions documented in detection.md.
    exclude_list.extend([
        "current_architecture",
        "current_ci",
        "current_os",
        "current_platform",
        "current_platforms",
        "current_traits",
        "invalidate_caches",
    ])

    # Also exclude group utility functions documented in groups.md.
    exclude_list.extend([
        "groups_from_ids",
        "reduce",
        "traits_from_ids",
    ])

    # Also exclude core classes documented in trait.md and groups.md.
    exclude_list.extend([
        "Architecture",
        "CI",
        "Group",
        "Platform",
        "Trait",
    ])

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        .. automodule:: extra_platforms
           :members:
           :show-inheritance:
           :undoc-members:
           :exclude-members: {exclude_members}""")


def update_docs() -> None:
    """Update documentation with dynamic content.

    Dynamically discovers all markdown files in the documentation root
    and applies content replacements based on HTML comment tags found
    in each file.

    .. todo::
        Maybe one day we'll be able to generate [Euler diagrams](https://xkcd.com/2721/)
        instead of Sankey diagrams for the group visualizations.

        There's still a chance to [have them supported by
        Mermaid](https://github.com/mermaid-js/mermaid/issues/2583).
    """
    # Define all replacement rules as (start_tag, end_tag, content) tuples.
    # Tags are simple names that will be wrapped in HTML comments automatically.
    replacement_rules = [
        # Trait tables.
        (
            "architecture-table-start",
            "architecture-table-end",
            generate_trait_table(ALL_ARCHITECTURES),
        ),
        (
            "platform-table-start",
            "platform-table-end",
            generate_trait_table(ALL_PLATFORMS),
        ),
        (
            "ci-table-start",
            "ci-table-end",
            generate_trait_table(ALL_CI),
        ),
        # All traits table (for trait.md) - merged table of all traits.
        (
            "all-traits-table-start",
            "all-traits-table-end",
            generate_all_traits_table(ALL_TRAITS),
        ),
        # Sankey diagrams.
        (
            "architecture-canonical-sankey-start",
            "architecture-canonical-sankey-end",
            generate_sankey(
                list(NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS)
                + [ALL_ARCHITECTURES]
            ),
        ),
        (
            "architecture-bitness-sankey-start",
            "architecture-bitness-sankey-end",
            generate_sankey([ARCH_32_BIT, ARCH_64_BIT, ALL_ARCHITECTURES]),
        ),
        (
            "platform-multi-level-sankey-start",
            "platform-multi-level-sankey-end",
            generate_sankey(
                list(NON_OVERLAPPING_GROUPS & ALL_PLATFORM_GROUPS) + [ALL_PLATFORMS]
            ),
        ),
        (
            "ci-sankey-start",
            "ci-sankey-end",
            generate_sankey(ALL_CI_GROUPS),
        ),
        # Mindmap diagrams.
        (
            "architecture-canonical-mindmap-start",
            "architecture-canonical-mindmap-end",
            generate_traits_mindmap(
                list(NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS)
                + [ALL_ARCHITECTURES]
            ),
        ),
        (
            "architecture-bitness-mindmap-start",
            "architecture-bitness-mindmap-end",
            generate_traits_mindmap([ARCH_32_BIT, ARCH_64_BIT, ALL_ARCHITECTURES]),
        ),
        (
            "platform-mindmap-start",
            "platform-mindmap-end",
            generate_traits_mindmap(
                list(NON_OVERLAPPING_GROUPS & ALL_PLATFORM_GROUPS) + [ALL_PLATFORMS]
            ),
        ),
        (
            "ci-mindmap-start",
            "ci-mindmap-end",
            generate_traits_mindmap(
                list(NON_OVERLAPPING_GROUPS & ALL_CI_GROUPS) + [ALL_CI]
            ),
        ),
        # Group tables.
        (
            "architecture-groups-table-start",
            "architecture-groups-table-end",
            generate_group_table(ALL_ARCHITECTURE_GROUPS),
        ),
        (
            "platform-groups-table-start",
            "platform-groups-table-end",
            generate_group_table(ALL_PLATFORM_GROUPS),
        ),
        (
            "ci-groups-table-start",
            "ci-groups-table-end",
            generate_group_table(ALL_CI_GROUPS),
        ),
        (
            "groups-table-start",
            "groups-table-end",
            generate_group_table(ALL_GROUPS),
        ),
        # Pytest decorators table.
        (
            "decorators-table-start",
            "decorators-table-end",
            generate_decorators_table(chain(ALL_TRAITS, ALL_GROUPS)),
        ),
        # Autodata directives for Sphinx documentation of module-level constants.
        (
            "architecture-data-autodata-start",
            "architecture-data-autodata-end",
            generate_autodata_directives(
                list(ALL_ARCHITECTURES) + [UNKNOWN_ARCHITECTURE]
            ),
        ),
        (
            "platform-data-autodata-start",
            "platform-data-autodata-end",
            generate_autodata_directives(list(ALL_PLATFORMS) + [UNKNOWN_PLATFORM]),
        ),
        (
            "ci-data-autodata-start",
            "ci-data-autodata-end",
            generate_autodata_directives(list(ALL_CI) + [UNKNOWN_CI]),
        ),
        (
            "group-data-autodata-start",
            "group-data-autodata-end",
            generate_autodata_directives([g for g in ALL_GROUPS]),
        ),
        # Autofunction directives for all detection functions (traits and groups).
        (
            "all-detection-function-table-start",
            "all-detection-function-table-end",
            generate_all_detection_function_table(chain(ALL_TRAITS, ALL_GROUPS)),
        ),
        (
            "trait-detection-autofunction-start",
            "trait-detection-autofunction-end",
            generate_detection_autofunction(ALL_TRAITS),
        ),
        (
            "group-detection-autofunction-start",
            "group-detection-autofunction-end",
            generate_detection_autofunction(ALL_GROUPS),
        ),
        # Pytest automodule directive (excludes dynamically generated decorators).
        (
            "pytest-automodule-start",
            "pytest-automodule-end",
            generate_pytest_automodule(chain(ALL_TRAITS, ALL_GROUPS)),
        ),
        # Pytest decorator autodata directives.
        (
            "pytest-decorators-autodata-start",
            "pytest-decorators-autodata-end",
            generate_pytest_decorator_autodata(chain(ALL_TRAITS, ALL_GROUPS)),
        ),
        # Extra-platforms automodule directive (excludes detection functions).
        (
            "extra-platforms-automodule-start",
            "extra-platforms-automodule-end",
            generate_extra_platforms_automodule(chain(ALL_TRAITS, ALL_GROUPS)),
        ),
        # Group automodule directive (excludes utility functions).
        (
            "group-automodule-start",
            "group-automodule-end",
            generate_group_automodule(),
        ),
        # Trait automodule directive (excludes core classes).
        (
            "trait-automodule-start",
            "trait-automodule-end",
            generate_trait_automodule(),
        ),
    ]

    # Collect all markdown and rST files from docs directory and project root.
    all_doc_files = set()

    # Add markdown files from docs directory using wcmatch glob.
    for md_file in wcglob.iglob(str(DOCS_ROOT / "**/*.md"), flags=wcglob.GLOBSTAR):
        all_doc_files.add(Path(md_file).resolve())

    # Add rST files from docs directory.
    for rst_file in wcglob.iglob(str(DOCS_ROOT / "**/*.rst"), flags=wcglob.GLOBSTAR):
        all_doc_files.add(Path(rst_file).resolve())

    # Add readme.md from project root.
    if README_PATH.exists():
        all_doc_files.add(README_PATH.resolve())

    # Apply each replacement rule to all matching files.
    for start_tag, end_tag, content in replacement_rules:
        matching_files: list[Path] = []
        # Use regex to check if tags exist (with flexible whitespace).
        # Support both HTML comments (Markdown) and rST comments.
        html_start_pattern = re.compile(
            rf"<!--\s*{re.escape(start_tag)}\s*-->",
            re.MULTILINE | re.DOTALL,
        )
        html_end_pattern = re.compile(
            rf"<!--\s*{re.escape(end_tag)}\s*-->",
            re.MULTILINE | re.DOTALL,
        )
        rst_start_pattern = re.compile(
            rf"\.\.\s+{re.escape(start_tag)}",
            re.MULTILINE | re.DOTALL,
        )
        rst_end_pattern = re.compile(
            rf"\.\.\s+{re.escape(end_tag)}",
            re.MULTILINE | re.DOTALL,
        )

        for filepath in all_doc_files:
            file_content = filepath.read_text(encoding="utf-8")
            has_html_tags = html_start_pattern.search(
                file_content
            ) and html_end_pattern.search(file_content)
            has_rst_tags = rst_start_pattern.search(
                file_content
            ) and rst_end_pattern.search(file_content)
            if has_html_tags or has_rst_tags:
                matching_files.append(filepath)
        if matching_files:
            replace_content(matching_files, start_tag, end_tag, content)


if __name__ == "__main__":
    print("Updating documentation...")
    sys.exit(update_docs())  # type: ignore[func-returns-value]
