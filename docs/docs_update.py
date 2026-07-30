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
"""Automation to keep extra-platforms documentation up-to-date.

:func:`update_docs` materializes the content that cannot render live: the
``readme.md`` mindmaps (GitHub cannot execute Sphinx directives) and the reST
autodoc regions (``{eval-rst}`` ``autodata``/``autofunction``/``automodule``).

The trait and group pages render their own tables and diagrams live via
``{python:render}`` ``:mirror:`` blocks calling :mod:`extra_platforms._docs`;
their committed ``<!-- mirror -->`` regions are refreshed by
``click-extra refresh-directives`` (the fourth ``repomatic update-docs`` phase),
not by this script.

.. tip::

    When run directly, it updates all documentation files in-place:

    .. code-block:: shell-session

        $ uv run python docs/docs_update.py

    In CI, the same update runs through the ``repomatic update-docs`` step of the
    `autofix workflow
    <https://github.com/kdeldycke/extra-platforms/blob/main/.github/workflows/autofix.yaml>`_.

.. warning::
    The generated Mermaid syntax targets the version bundled with
    ``sphinxcontrib-mermaid``, currently ``11.12.1``. See the hard-coded
    ``MERMAID_VERSION`` constant in `sphinxcontrib-mermaid's source
    <https://github.com/mgaitan/sphinxcontrib-mermaid/blob/master/sphinxcontrib/mermaid/__init__.py>`_.
    Avoid using Mermaid features introduced after that version.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable
from itertools import chain
from operator import attrgetter
from pathlib import Path
from textwrap import dedent

from click_extra.sphinx._base import update_blocks

from extra_platforms import (
    ALL_AGENT_GROUPS,
    ALL_AGENTS,
    ALL_ARCHITECTURE_GROUPS,
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_CI_GROUPS,
    ALL_GROUPS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_SHELL_GROUPS,
    ALL_SHELLS,
    ALL_TERMINAL_GROUPS,
    ALL_TERMINALS,
    ALL_TRAITS,
    CANONICAL_GROUPS,
    UNKNOWN_AGENT,
    UNKNOWN_ARCHITECTURE,
    UNKNOWN_CI,
    UNKNOWN_PLATFORM,
    UNKNOWN_SHELL,
    UNKNOWN_TERMINAL,
    Group,
    Trait,
)
from extra_platforms._docs import generate_traits_mindmap

_GROUP_API_FUNCTIONS = (
    "extract_members",
    "groups_from_ids",
    "reduce",
    "traits_from_ids",
)
"""Trait and group operation functions documented in their own groups.md section.

Excluded from automodule directives so groups.md stays their canonical location.
"""

DOCS_ROOT = Path(__file__).parent
"""The root path of Sphinx documentation."""

PROJECT_ROOT = DOCS_ROOT.parent
"""The root path of the project."""

README_PATH = PROJECT_ROOT / "readme.md"
"""The path to the ``readme.md`` file."""


def replace_region(text: str, start_tag: str, end_tag: str, new_content: str) -> str:
    """Return `text` with the content between the two tag comments replaced.

    Tags are matched as ``<!-- tag -->`` HTML comments with flexible whitespace
    (e.g. ``start_tag="architecture-mindmap-start"``). When either tag is absent
    the text is returned unchanged, so this is safe to apply to every file.

    Pure transform: writing back to disk (and the ``--check`` dry-run) is handled
    by :func:`click_extra.sphinx._base.update_blocks`.
    """
    start_pattern = re.compile(
        rf"<!--\s*{re.escape(start_tag)}\s*-->\s*",
        re.MULTILINE | re.DOTALL,
    )
    end_pattern = re.compile(
        rf"\s*<!--\s*{re.escape(end_tag)}\s*-->",
        re.MULTILINE | re.DOTALL,
    )

    start_match = start_pattern.search(text)
    if not start_match:
        return text
    after_start = text[start_match.end() :]
    end_match = end_pattern.search(after_start)
    if not end_match:
        return text

    pre_content = text[: start_match.start()]
    post_content = after_start[end_match.end() :]
    return (
        f"{pre_content}<!-- {start_tag} -->\n\n{new_content}"
        f"\n\n<!-- {end_tag} -->{post_content}"
    )


def generate_sphinx_directives(
    objects: Iterable[Trait | Group],
    directive: str,
    attr: str,
) -> str:
    """Generate Sphinx autodoc directives for a collection of traits or groups.

    Produces a MyST ``{eval-rst}`` block with one directive line per object.

    .. note::
        Autodoc directives (``autodata``, ``autofunction``, ``autoclass``, etc.)
        cannot be used as native MyST directives. They perform internal rST nested
        parsing that requires an rST parser context only ``{eval-rst}`` provides.
        See `MyST-Parser #587 <https://github.com/executablebooks/MyST-Parser/issues/587>`_,
        `#228 <https://github.com/executablebooks/MyST-Parser/issues/228>`_,
        and `#1119 <https://github.com/executablebooks/MyST-Parser/issues/1119>`_.

    :param objects: The traits or groups to generate directives for.
    :param directive: The Sphinx directive name (e.g. ``"autodata"``,
        ``"autofunction"``).
    :param attr: The attribute name on each object that provides the qualified
        identifier (e.g. ``"symbol_id"``, ``"detection_func_id"``).
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

    Uses ``{eval-rst}`` for the same reason as :func:`generate_sphinx_directives`.
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


def generate_noindex_automodule(module: str) -> str:
    """Generate a no-members automodule directive for a submodule section.

    All public members are documented in dedicated pages, so only the module
    docstring is rendered on ``extra_platforms.html``. Uses ``{eval-rst}`` for the
    same reason as :func:`generate_sphinx_directives`.
    """
    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: {module}
           :noindex:
           :no-members:
        ```""")


def generate_group_module_automodule() -> str:
    """Generate the extra_platforms.group automodule for groups.md.

    Excludes Group class and utility functions that are documented separately
    in the same file. Uses ``{eval-rst}`` for the same reason as
    :func:`generate_sphinx_directives`.
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
    :func:`generate_sphinx_directives`.

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


def generate_extra_platforms_automodule(objects: Iterable[Trait | Group]) -> str:
    """Generate the extra_platforms automodule directive with excluded members.

    This excludes detection functions, utility functions, and core classes from the
    automodule output, since they are documented in other files:

    - Detection functions in detection.md.
    - Utility functions in detection.md and groups.md.
    - Core classes in trait.md and groups.md.

    Uses ``{eval-rst}`` for the same reason as :func:`generate_sphinx_directives`.

    :param objects: The traits and groups whose detection functions should be
        excluded.
    """
    objects_list = list(objects)

    # Exclude all detection functions so detection.md is the canonical location.
    exclude_list = [
        obj.detection_func_id for obj in sorted(objects_list, key=attrgetter("id"))
    ]

    # Also exclude utility functions documented in detection.md.
    exclude_list.extend([
        "current_agent",
        "current_architecture",
        "current_ci",
        "current_platform",
        "current_shell",
        "current_shell_path",
        "current_terminal",
        "current_traits",
        "invalidate_caches",
    ])

    # Also exclude group utility functions documented in groups.md.
    exclude_list.extend(_GROUP_API_FUNCTIONS)

    # Also exclude core classes documented in trait.md and groups.md.
    exclude_list.extend([
        "Agent",
        "Architecture",
        "CI",
        "Group",
        "Platform",
        "Shell",
        "Terminal",
        "Trait",
    ])

    exclude_members = ", ".join(sorted(exclude_list))

    return dedent(f"""\
        ```{{eval-rst}}
        .. automodule:: extra_platforms
           :members:
           :show-inheritance:
           :undoc-members:
           :exclude-members: {exclude_members}
        ```""")


def update_docs(*, check: bool = False) -> list[Path]:
    """Materialize the regions that cannot render live at build time.

    Applies the marker-region replacements to ``readme.md`` and every
    ``docs/**/*.md`` file through
    :func:`click_extra.sphinx._base.update_blocks` — the same walk/write/``check``
    primitive the ``:mirror:`` and ``{matrix}`` directives use, so this shares
    their dry-run contract. Scope is limited to the ``readme.md`` mindmaps and
    the reST autodoc regions; the trait and group pages render their own tables
    and diagrams via ``{python:render}`` ``:mirror:`` blocks (see the module
    docstring).

    :param check: When ``True``, report the files that are out of date without
        writing anything (for CI drift detection).
    :return: The files that were (or, under ``check``, would be) rewritten.

    .. todo::
        Maybe one day we'll be able to generate [Euler diagrams](https://xkcd.com/2721/)
        instead of Sankey diagrams for the group visualizations.

        There's still a chance to [have them supported by
        Mermaid](https://github.com/mermaid-js/mermaid/issues/2583).
    """
    # Define all replacement rules as (start_tag, end_tag, content) tuples.
    # Tags are simple names that will be wrapped in HTML comments automatically.
    replacement_rules = [
        # Mindmaps for readme.md only. The docs pages render their own trait
        # tables, group tables, sankeys and mindmaps live via {python:render};
        # readme.md keeps static markers because GitHub cannot execute the
        # render directives when browsing the file.
        (
            "architecture-mindmap-start",
            "architecture-mindmap-end",
            generate_traits_mindmap(
                list(CANONICAL_GROUPS & ALL_ARCHITECTURE_GROUPS) + [ALL_ARCHITECTURES]
            ),
        ),
        (
            "platform-mindmap-start",
            "platform-mindmap-end",
            generate_traits_mindmap(
                list(CANONICAL_GROUPS & ALL_PLATFORM_GROUPS) + [ALL_PLATFORMS]
            ),
        ),
        (
            "shell-mindmap-start",
            "shell-mindmap-end",
            generate_traits_mindmap(
                list(CANONICAL_GROUPS & ALL_SHELL_GROUPS) + [ALL_SHELLS]
            ),
        ),
        (
            "terminal-mindmap-start",
            "terminal-mindmap-end",
            generate_traits_mindmap(
                list(CANONICAL_GROUPS & ALL_TERMINAL_GROUPS) + [ALL_TERMINALS]
            ),
        ),
        (
            "ci-mindmap-start",
            "ci-mindmap-end",
            generate_traits_mindmap(list(CANONICAL_GROUPS & ALL_CI_GROUPS) + [ALL_CI]),
        ),
        (
            "agent-mindmap-start",
            "agent-mindmap-end",
            generate_traits_mindmap(
                list(CANONICAL_GROUPS & ALL_AGENT_GROUPS) + [ALL_AGENTS]
            ),
        ),
        # Autodata directives for Sphinx documentation of module-level constants.
        (
            "architecture-data-autodata-start",
            "architecture-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_ARCHITECTURES) + [UNKNOWN_ARCHITECTURE],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "platform-data-autodata-start",
            "platform-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_PLATFORMS) + [UNKNOWN_PLATFORM],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "shell-data-autodata-start",
            "shell-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_SHELLS) + [UNKNOWN_SHELL],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "terminal-data-autodata-start",
            "terminal-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_TERMINALS) + [UNKNOWN_TERMINAL],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "ci-data-autodata-start",
            "ci-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_CI) + [UNKNOWN_CI],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "agent-data-autodata-start",
            "agent-data-autodata-end",
            generate_sphinx_directives(
                list(ALL_AGENTS) + [UNKNOWN_AGENT],
                "autodata",
                "symbol_id",
            ),
        ),
        (
            "group-data-autodata-start",
            "group-data-autodata-end",
            generate_sphinx_directives(
                ALL_GROUPS,
                "autodata",
                "symbol_id",
            ),
        ),
        # Autofunction directives for all detection functions (traits and groups).
        (
            "trait-detection-autofunction-start",
            "trait-detection-autofunction-end",
            generate_sphinx_directives(ALL_TRAITS, "autofunction", "detection_func_id"),
        ),
        (
            "group-detection-autofunction-start",
            "group-detection-autofunction-end",
            generate_sphinx_directives(ALL_GROUPS, "autofunction", "detection_func_id"),
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
            generate_noindex_automodule("extra_platforms.group"),
        ),
        # Trait automodule directive (excludes core classes).
        (
            "trait-automodule-start",
            "trait-automodule-end",
            generate_noindex_automodule("extra_platforms.trait"),
        ),
        # Group module automodule for groups.md (excludes Group class and utilities).
        (
            "group-module-automodule-start",
            "group-module-automodule-end",
            generate_group_module_automodule(),
        ),
        # Group data module automodule for groups.md (excludes all groups and
        # collections).
        (
            "group-data-module-automodule-start",
            "group-data-module-automodule-end",
            generate_group_data_module_automodule(ALL_GROUPS),
        ),
    ]

    def rewrite(text: str, path: Path) -> str:
        for start_tag, end_tag, content in replacement_rules:
            text = replace_region(text, start_tag, end_tag, content)
        return text

    # readme.md plus every docs/**/*.md; a rule whose markers are absent from a
    # file leaves it untouched.
    return update_blocks([README_PATH, DOCS_ROOT], rewrite, check=check)


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    changed = update_docs(check=check_mode)
    if check_mode:
        if changed:
            print("Out-of-date documentation, run `python docs/docs_update.py`:")
            for path in changed:
                print(f"  {path}")
            sys.exit(1)
        print("Documentation is up to date.")
    else:
        print(f"Updated documentation ({len(changed)} file(s) changed).")
