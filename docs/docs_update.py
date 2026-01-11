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

import html
import re
import sys
from itertools import chain
from operator import attrgetter
from pathlib import Path
from textwrap import dedent, indent
from typing import Iterable

from tabulate import tabulate
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


def replace_content(
    filepath: Path | Iterable[Path],
    start_tag: str,
    end_tag: str,
    new_content: str,
) -> None:
    """Replace in the provided files the content surrounded by the provided tags.

    Tags are specified as simple names (e.g., "architecture-table-start") and will be
    matched with flexible whitespace handling in HTML comment format.
    """
    if isinstance(filepath, Path):
        path_list = [filepath]
    else:
        path_list = list(filepath)

    for filepath in path_list:
        filepath = filepath.resolve()
        assert filepath.exists(), f"File {filepath} does not exist."
        assert filepath.is_file(), f"File {filepath} is not a file."

        orig_content = filepath.read_text()

        # Construct regex patterns that match tags with flexible whitespace.
        # Matches: <!-- tag -->\s* (any whitespace including newlines)
        start_pattern = re.compile(
            rf"<!--\s*{re.escape(start_tag)}\s*-->\s*",
            re.MULTILINE | re.DOTALL,
        )
        end_pattern = re.compile(
            rf"\s*<!--\s*{re.escape(end_tag)}\s*-->",
            re.MULTILINE | re.DOTALL,
        )

        # Find start tag
        start_match = start_pattern.search(orig_content)
        if not start_match:
            continue

        # Split at start tag
        pre_content = orig_content[: start_match.start()]
        after_start = orig_content[start_match.end() :]

        # Find end tag
        end_match = end_pattern.search(after_start)
        if not end_match:
            continue

        # Split at end tag
        post_content = after_start[end_match.end() :]

        # Reconstruct with standardized formatting
        start_tag_formatted = f"<!-- {start_tag} -->\n\n"
        end_tag_formatted = f"\n\n<!-- {end_tag} -->"

        filepath.write_text(
            f"{pre_content}{start_tag_formatted}{new_content}{end_tag_formatted}{post_content}",
        )


def _generate_markdown_table(
    table_data: list[list[str]],
    headers: list[str],
    alignments: list[str],
) -> str:
    """Generate a Markdown table using tabulate with custom alignment separators.

    This is a shared helper function that both generate_trait_table() and
    generate_group_table() use to render tables with proper Markdown alignment hints.

    Args:
        table_data: List of rows, where each row is a list of cell values.
        headers: List of column header names.
        alignments: List of alignment hints ("left", "right", "center") for each column.

    Returns:
        A formatted Markdown table string with proper alignment separators.
    """
    rendered_table = tabulate(
        table_data,
        headers=headers,
        tablefmt="github",
        colalign=alignments,
        disable_numparse=True,
    )

    # Manually produce Markdown alignment hints. This has been proposed upstream at:
    # https://github.com/astanin/python-tabulate/pull/261
    # https://github.com/astanin/python-tabulate/issues/53
    # Copy of:
    # https://github.com/kdeldycke/meta-package-manager/blob/6d250993edf22ba7456ad0f105d8937f7e650ccd/meta_package_manager/inventory.py#L139C1-L160C1
    separators = []
    for col_index, header in enumerate(headers):
        cells = [line[col_index] for line in table_data] + [header]
        max_len = max(len(c) for c in cells)
        align = alignments[col_index]
        if align == "left":
            sep = f":{'-' * (max_len - 1)}"
        elif align == "center":
            sep = f":{'-' * (max_len - 2)}:"
        elif align == "right":
            sep = f"{'-' * (max_len - 1)}:"
        else:
            sep = "-" * max_len
        separators.append(sep)
    header_separator = f"| {' | '.join(separators)} |"

    lines = rendered_table.splitlines()
    lines[1] = header_separator

    return "\n".join(lines)


def generate_trait_table(traits: Iterable[Trait]) -> str:
    """Produce a Markdown table for a collection of traits.

    The table contains the icon, the symbol constant name (linked to its full definition),
    a linked name, and a linked detection function for each trait. A hint block is appended
    after the table explaining the unknown trait for this trait type.
    """
    table_data = []
    headers = ["Icon", "Symbol", "Name", "Detection function"]
    alignments = ["center", "left", "left", "left"]

    # Get metadata from the first trait (all traits in the table should be the same type).
    traits_list = list(traits)
    all_classes = {type(trait) for trait in traits_list}
    assert len(all_classes) == 1, (
        "All traits must be of the same class to generate a trait table."
    )
    meta = all_classes.pop().metadata

    for trait in sorted(traits_list, key=attrgetter("id")):
        table_data.append([
            html.escape(trait.icon),
            f"[`{trait.symbol_id}`](#extra_platforms.{meta.data_module_id}.{trait.symbol_id})",
            trait.name,
            f"[`is_{trait.id}()`](detection.md#extra_platforms.detection.is_{trait.id})",
        ])

    table = _generate_markdown_table(table_data, headers, alignments)

    # Append hint block explaining unknown trait if trait type was detected.
    hint = f"""
```{{hint}}
The [`{meta.unknown_symbol}`](#extra_platforms.{meta.data_module_id}.{meta.unknown_symbol}) trait represents an unrecognized {meta.type_name}. It is not included in the [`{meta.all_group}`](groups.md#extra_platforms.group_data.{meta.all_group}) group, and will be returned by `{meta.current_func_id}()` if the current {meta.type_name} is not recognized.
```"""
    return f"{table}\n{hint}"


def generate_group_table(groups: Iterable[Group]) -> str:
    """Produce a Markdown table for a collection of groups.

    The table contains the icon, symbol with link to documentation, description, member count, and canonical
    status for each group. A hint block is appended after the table to explain canonical groups.

    Args:
        groups: The groups to include in the table.
    """
    table_data = []
    headers = ["Icon", "Symbol", "Description", "Canonical", "Member count"]
    alignments = ["center", "left", "left", "center", "right"]

    for group in sorted(groups, key=attrgetter("id")):
        table_data.append([
            html.escape(group.icon),
            f"[`{group.symbol_id}`](groups.md#extra_platforms.group_data.{group.symbol_id})",
            group.name,
            "⬥" if group.canonical else "",
            str(len(group)),
        ])

    table = _generate_markdown_table(table_data, headers, alignments)

    # Append hint block explaining canonical groups
    hint = """
```{hint}
Canonical groups are non-overlapping groups that together cover all recognized traits. They are marked with a ⬥ icon in the table above.

Other groups are provided for convenience, but overlap with each other or with canonical groups.
```"""

    return f"{table}\n{hint}"


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
        group_map += f"({html.escape(trait.icon)} {trait.symbol_id})\n"
    name = f"{html.escape(superset.icon)} {superset.symbol_id}"
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

    The table contains the skip decorator, unless decorator, symbol link, and description for each trait or group.
    """
    table_data = []
    headers = ["Skip decorator", "Unless decorator", "Source symbol", "Description"]
    alignments = ["left", "left", "left", "left"]

    for trait in sorted(objects, key=attrgetter("id")):
        meta = type(trait).metadata
        table_data.append([
            f"`@skip_{trait.id}`",
            f"`@unless_{trait.id}`",
            f"[`{trait.symbol_id}`]({meta.doc_page}#extra_platforms.{meta.data_module_id}.{trait.symbol_id})",
            html.escape(trait.name),
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
        meta = type(trait).metadata
        directives.append(
            f".. autodata:: extra_platforms.{meta.data_module_id}.{trait.symbol_id}"
        )

    output = "```{eval-rst}\n"
    output += "\n".join(directives)
    output += "\n```"
    return output


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
        # Sankey diagrams.
        (
            "architecture-multi-level-sankey-start",
            "architecture-multi-level-sankey-end",
            generate_sankey(
                list(NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS)
                + [ALL_ARCHITECTURES]
            ),
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
            "architecture-mindmap-start",
            "architecture-mindmap-end",
            generate_traits_mindmap(
                list(NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS)
                + [ALL_ARCHITECTURES]
            ),
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
    ]

    # Collect all markdown files from docs directory and project root.
    all_md_files = set()

    # Add markdown files from docs directory using wcmatch glob.
    for md_file in wcglob.iglob(str(DOCS_ROOT / "**/*.md"), flags=wcglob.GLOBSTAR):
        all_md_files.add(Path(md_file).resolve())

    # Add readme.md from project root.
    if README_PATH.exists():
        all_md_files.add(README_PATH.resolve())

    # Apply each replacement rule to all matching files.
    for start_tag, end_tag, content in replacement_rules:
        matching_files: list[Path] = []
        # Use regex to check if tags exist (with flexible whitespace)
        start_pattern = re.compile(
            rf"<!--\s*{re.escape(start_tag)}\s*-->",
            re.MULTILINE | re.DOTALL,
        )
        end_pattern = re.compile(
            rf"<!--\s*{re.escape(end_tag)}\s*-->",
            re.MULTILINE | re.DOTALL,
        )

        for filepath in all_md_files:
            file_content = filepath.read_text()
            if start_pattern.search(file_content) and end_pattern.search(file_content):
                matching_files.append(filepath)
        if matching_files:
            replace_content(matching_files, start_tag, end_tag, content)


if __name__ == "__main__":
    print("Updating documentation...")
    sys.exit(update_docs())  # type: ignore[func-returns-value]
