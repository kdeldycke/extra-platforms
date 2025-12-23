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
import sys
from operator import attrgetter
from pathlib import Path
from textwrap import dedent, indent
from typing import Iterable

from extra_platforms import (
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUPS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ARM,
    EXTRA_GROUPS,
    IBM_MAINFRAME,
    LOONGARCH,
    MIPS,
    NON_OVERLAPPING_GROUPS,
    POWERPC,
    RISCV,
    SPARC,
    WEBASSEMBLY,
    X86,
    Group,
)

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
    """Replace in the provided files the content surrounded by the provided tags."""
    if isinstance(filepath, Path):
        path_list = [filepath]
    else:
        path_list = filepath

    for filepath in path_list:
        filepath = filepath.resolve()
        assert filepath.exists(), f"File {filepath} does not exist."
        assert filepath.is_file(), f"File {filepath} is not a file."

        orig_content = filepath.read_text()

        # Extract pre- and post-content surrounding the tags.
        pre_content, table_start = orig_content.split(start_tag, 1)
        _, post_content = table_start.split(end_tag, 1)

        # Reconstruct the content with our updated table.
        filepath.write_text(
            f"{pre_content}{start_tag}{new_content}{end_tag}{post_content}",
        )


def generate_trait_table(traits, column_name: str) -> str:
    """Produce a Markdown table for a collection of traits.

    The table contains the icon, a linked name, the quoted ID, and a linked detection function for each trait.
    """
    lines: list[str] = []
    lines.append(f"| Icon | Name | {column_name} | Detection function |")
    lines.append("|:----:|:------|:-------------|:-------------------|")

    for trait in sorted(traits, key=attrgetter("id")):
        icon = html.escape(trait.icon)
        name = html.escape(trait.name)
        url = trait.url
        detection_func = f"[`is_{trait.id}()`](detection.md#extra_platforms.detection.is_{trait.id})"
        lines.append(f"| {icon} | [{name}]({url}) | `{trait.id}` | {detection_func} |")

    return "\n".join(lines)


def generate_groups_sankey(groups: frozenset[Group]) -> str:
    """Produce a Sankey diagram to map all platforms to their groups.

    Excludes the ``ALL_PLATFORMS`` group which unnecessarily adds noise to the already
    dense diagram.
    """
    table = []

    # Display biggest groups first. Add ID in the sorting key to get stable sorting on
    # tie.
    for group in sorted(groups, key=lambda g: (len(g), g.id), reverse=True):
        for member_id in group.members:
            # XXX Sankey diagrams do not support emoji icons yet.
            # table.append(
            #     f'"{html.escape(group.icon)} {group.id}",'
            #     f'"{html.escape(member.icon)} {member_id}",1'
            # )
            table.append(f"{group.id.upper()},{member_id},1")

    output = dedent("""\
        ```mermaid
        ---
        config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
        ---
        sankey-beta\n
        """)
    output += "\n".join(table)
    output += "\n```"
    return output


def generate_multi_level_sankey(groups: Iterable[Group]) -> str:
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
    groups_list = list(groups)

    # Find the superset group (the one that contains all others as subsets).
    supersets = [
        g for g in groups_list
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
    union_of_intermediate = set()
    for group in intermediate_groups:
        union_of_intermediate.update(group.member_ids)

    # Find traits in the superset that aren't covered by any intermediate group.
    missing_trait_ids = superset.member_ids - union_of_intermediate
    missing_traits = sorted(
        [superset[tid] for tid in missing_trait_ids],
        key=lambda t: t.id,
    )

    table = []

    # First layer: superset -> intermediate groups (weight = number of members in group).
    for group in sorted(intermediate_groups, key=lambda g: (len(g), g.id), reverse=True):
        member_count = len(group.members)
        table.append(f"{superset.id.upper()},{group.id.upper()},{member_count}")

    # Second layer: intermediate groups -> their members (weight = 1 each).
    for group in sorted(intermediate_groups, key=lambda g: (len(g), g.id), reverse=True):
        for member_id in group.members:
            table.append(f"{group.id.upper()},{member_id},1")

    # Third layer: superset -> missing traits (weight = 1 each), placed at the end.
    for trait in missing_traits:
        table.append(f"{superset.id.upper()},{trait.id},1")

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


def generate_traits_mindmap(top_group: Group, groups: frozenset[Group]) -> str:
    """Produce a mindmap hierarchy to show the non-overlapping groups of traits."""
    group_map = ""
    for group in sorted(groups, key=attrgetter("id"), reverse=True):
        group_map += f"){group.icon} {group.id.upper()}(\n"
        for platform_id, platform in group.members.items():
            group_map += f"    ({platform.icon} {platform_id})\n"

    name = f"{html.escape(top_group.icon)} {top_group.id}"
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


def generate_platforms_graph(
    graph_id: str,
    description: str,
    groups: frozenset[Group],
) -> str:
    """Generates an `Euler diagram <https://xkcd.com/2721/>`_ of platform and their
    grouping.

    Euler diagrams are `not supported by mermaid yet
    <https://github.com/mermaid-js/mermaid/issues/2583>`_ so we fallback on a flowchart
    without arrows.

    Returns a ready to use and properly indented MyST block.
    """
    INDENT = " " * 4
    subgraphs = set()

    # Create one subgraph per group.
    for group in sorted(groups, key=attrgetter("id")):
        nodes = set()
        for platform in group:
            # Make the node ID unique for overlapping groups.
            nodes.add(
                f"{group.id}_{platform.id}"
                f"(<code>{platform.id}</code><br/>"
                f"{html.escape(platform.icon)} <em>{html.escape(platform.name)}</em>)",
            )
        subgraphs.add(
            f'subgraph "<code>extra_platforms.{group.id.upper()}</code>'
            "<br/>"
            f'{html.escape(group.icon)} <em>{html.escape(group.name)}</em>"'
            "\n" + indent("\n".join(sorted(nodes)), INDENT) + "\nend",
        )

    # Wrap the Mermaid code into a MyST block.
    return "\n".join(
        (
            dedent(f"""\
                ```mermaid
                ---
                title: <code>extra_platforms.{graph_id}</code> - {description}
                ---
                flowchart
                """),
            indent("\n".join(sorted(subgraphs)), INDENT),
            "```",
        ),
    )


def update_docs() -> None:
    """Update documentation with dynamic content."""
    # Update trait tables.
    replace_content(
        DOCS_ROOT / "architectures.md",
        "<!-- architecture-table-start -->\n\n",
        "\n\n<!-- architecture-table-end -->",
        generate_trait_table(ALL_ARCHITECTURES, "Architecture ID"),
    )
    replace_content(
        DOCS_ROOT / "platforms.md",
        "<!-- platform-table-start -->\n\n",
        "\n\n<!-- platform-table-end -->",
        generate_trait_table(ALL_PLATFORMS, "Platform ID"),
    )
    replace_content(
        DOCS_ROOT / "ci.md",
        "<!-- ci-table-start -->\n\n",
        "\n\n<!-- ci-table-end -->",
        generate_trait_table(ALL_CI, "CI ID"),
    )

    # Update multi-level Sankey diagrams.
    replace_content(
        DOCS_ROOT / "architectures.md",
        "<!-- architecture-multi-level-sankey-start -->\n\n",
        "\n\n<!-- architecture-multi-level-sankey-end -->",
        generate_multi_level_sankey(
            list(NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS) + [ALL_ARCHITECTURES]
        ),
    )
    replace_content(
        DOCS_ROOT / "platforms.md",
        "<!-- platform-multi-level-sankey-start -->\n\n",
        "\n\n<!-- platform-multi-level-sankey-end -->",
        generate_multi_level_sankey(
            list(NON_OVERLAPPING_GROUPS & ALL_PLATFORM_GROUPS) + [ALL_PLATFORMS]
        ),
    )

    # Update Sankey diagrams.
    replace_content(
        DOCS_ROOT / "architectures.md",
        "<!-- architecture-sankey-start -->\n\n",
        "\n\n<!-- architecture-sankey-end -->",
        "\n\n".join(
            (
                generate_groups_sankey({group})
                for group in sorted(
                    NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS,
                    key=attrgetter("id"),
                )
            ),
        ),
    )
    replace_content(
        DOCS_ROOT / "platforms.md",
        "<!-- extra-platform-groups-sankey-start -->\n\n",
        "\n\n<!-- extra-platform-groups-sankey-end -->",
        "\n\n".join(
            (
                generate_groups_sankey({group})
                for group in sorted(
                    EXTRA_GROUPS & ALL_PLATFORM_GROUPS, key=attrgetter("id")
                )
            ),
        ),
    )
    replace_content(
        DOCS_ROOT / "ci.md",
        "<!-- ci-sankey-start -->\n\n",
        "\n\n<!-- ci-sankey-end -->",
        generate_groups_sankey(ALL_CI_GROUPS),
    )

    # Update mindmap diagrams showing the hierarchy of non-overlapping groups.
    replace_content(
        (README_PATH, DOCS_ROOT / "architectures.md"),
        "<!-- architecture-mindmap-start -->\n\n",
        "\n\n<!-- architecture-mindmap-end -->",
        generate_traits_mindmap(
            ALL_ARCHITECTURES, NON_OVERLAPPING_GROUPS & ALL_ARCHITECTURE_GROUPS
        ),
    )
    replace_content(
        (README_PATH, DOCS_ROOT / "platforms.md"),
        "<!-- platform-mindmap-start -->\n\n",
        "\n\n<!-- platform-mindmap-end -->",
        generate_traits_mindmap(
            ALL_PLATFORMS, NON_OVERLAPPING_GROUPS & ALL_PLATFORM_GROUPS
        ),
    )
    replace_content(
        README_PATH,
        "<!-- ci-mindmap-start -->\n\n",
        "\n\n<!-- ci-mindmap-end -->",
        generate_traits_mindmap(ALL_CI, NON_OVERLAPPING_GROUPS & ALL_CI_GROUPS),
    )

    # Update grouping charts of all groups, including non-overlapping and extra groups.
    platform_doc = PROJECT_ROOT / "docs" / "groups.md"
    # TODO: Replace this hard-coded dict by allowing Group dataclass to group
    # other groups.
    all_groups = (
        {
            "id": "NON_OVERLAPPING_GROUPS",
            "description": "Non-overlapping groups.",
            "groups": NON_OVERLAPPING_GROUPS,
        },
        {
            "id": "EXTRA_GROUPS",
            "description": "Overlapping groups, defined for convenience.",
            "groups": EXTRA_GROUPS,
        },
    )
    assert frozenset(g for groups in all_groups for g in groups["groups"]) == ALL_GROUPS
    for top_groups in all_groups:
        replace_content(
            platform_doc,
            f"<!-- {top_groups['id']}-graph-start -->\n\n",
            f"\n\n<!-- {top_groups['id']}-graph-end -->",
            generate_platforms_graph(
                top_groups["id"],  # type: ignore[arg-type]
                top_groups["description"],  # type: ignore[arg-type]
                top_groups["groups"],  # type: ignore[arg-type]
            ),
        )


if __name__ == "__main__":
    print("Updating documentation...")
    sys.exit(update_docs())  # type: ignore[func-returns-value]
