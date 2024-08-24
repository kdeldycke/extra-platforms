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
from pathlib import Path
from textwrap import dedent, indent

from . import ALL_GROUPS, EXTRA_GROUPS, NON_OVERLAPPING_GROUPS, Group


def replace_content(
    filepath: Path,
    start_tag: str,
    end_tag: str,
    new_content: str,
) -> None:
    """Replace in the provided file the content surrounded by the provided tags."""
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


def generate_platform_sankey() -> str:
    """Produce a Sankey diagram to map all platforms to their platforms."""
    table = []

    # Display biggest groups first. Add ID in the sorting key to get stable sorting on
    # tie.
    for group in sorted(
        ALL_GROUPS, key=lambda g: (len(g.platform_ids), g.id), reverse=True
    ):
        for platform in group.platforms:
            # XXX Sankey diagrams do not support emoji icons yet.
            # table.append(
            #     f'"{html.escape(group.icon)} {group.id}",'
            #     f'"{html.escape(platform.icon)} {platform.id}",1'
            # )
            table.append(f"{group.id},{platform.id},1")

    output = dedent("""\
        ```mermaid
        ---
        config:
          sankey:
            showValues: false
        ---
        sankey-beta\n
        """)
    output += "\n".join(table)
    output += "\n```"
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
    for group in sorted(groups, key=lambda g: g.id):
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
            # Use attributes blocks extension to add a title.
            f"#### `extra_platforms.{graph_id}` - {description}\n",
            "```mermaid",
            "flowchart",
            indent("\n".join(sorted(subgraphs)), INDENT),
            "```",
        ),
    )


def update_docs() -> None:
    """Update documentation with dynamic content."""
    project_root = Path(__file__).parent.parent

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

    # Update the platform diagrams in readme.
    replace_content(
        project_root.joinpath("readme.md"),
        "<!-- platform-sankey-start -->\n\n",
        "\n\n<!-- platform-sankey-end -->",
        generate_platform_sankey(),
    )

    platform_doc = project_root.joinpath("readme.md")
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
    sys.exit(update_docs())  # type: ignore[func-returns-value]
