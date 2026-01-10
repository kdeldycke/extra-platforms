from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]

from extra_platforms import Group
from extra_platforms.group_data import ALL_GROUPS
from extra_platforms.trait import Trait

project_path = Path(__file__).parent.parent.resolve()

# Fetch general information about the project from pyproject.toml.
toml_path = project_path / "pyproject.toml"
toml_config = tomllib.loads(toml_path.read_text())

# Redistribute pyproject.toml config to Sphinx.
project_id = toml_config["project"]["name"]
version = release = toml_config["project"]["version"]
url = toml_config["project"]["urls"]["Homepage"]
author = ", ".join(author["name"] for author in toml_config["project"]["authors"])

# Title-case each word of the project ID.
project = " ".join(word.title() for word in project_id.split("-"))
htmlhelp_basename = project_id

# Addons.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # Adds a copy button to code blocks.
    "sphinx_copybutton",
    "sphinx_design",
    # Link to GitHub issues and PRs.
    "sphinx_issues",
    "sphinxext.opengraph",
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx_autodoc_typehints",
    "click_extra.sphinx",
    "sphinxcontrib.mermaid",
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "attrs_block",
    "attrs_inline",
    "deflist",
    "replacements",
    "smartquotes",
    "strikethrough",
    "tasklist",
    # XXX Only enabled so we can support GitHub admonitions.
    "colon_fence",
]
# XXX Allow ```mermaid``` directive to be used without curly braces (```{mermaid}```), see:
# https://github.com/mgaitan/sphinxcontrib-mermaid/issues/99#issuecomment-2339587001
myst_fence_as_directive = ["mermaid"]

mermaid_d3_zoom = True

master_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

nitpicky = True

# Concatenates the docstrings of the class and the __init__ method.
autoclass_content = "both"
# Keep the same ordering as in original source code.
autodoc_member_order = "bysource"
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"]

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# GitHub pre-implemented shortcuts.
github_user = "kdeldycke"
issues_github_path = f"{github_user}/{project_id}"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Prefix document path to section labels, to use:
# `path/to/file:heading` instead of just `heading`
autosectionlabel_prefix_document = True

# Theme config.
html_theme = "furo"
html_title = project
html_theme_options = {
    # Activates edit links.
    "source_repository": f"https://github.com/{issues_github_path}",
    "source_branch": "main",
    "source_directory": "docs/",
    "announcement": (
        f"{project} works fine, but is <em>maintained by only one person</em> "
        "😶‍🌫️.<br/>You can help if you "
        "<strong><a class='reference external' "
        f"href='https://github.com/sponsors/{github_user}'>"
        "purchase business support 🤝</a></strong> or "
        "<strong><a class='reference external' "
        f"href='https://github.com/sponsors/{github_user}'>"
        "sponsor the project 🫶</a></strong>."
    ),
}

# Footer content.
html_last_updated_fmt = "%Y-%m-%d"
copyright = f"{author} and contributors"
html_show_copyright = True
html_show_sphinx = False


# Type mapping for trait classes
TRAIT_TYPE_INFO = {
    "Architecture": {
        "page": "architectures.html",
        "module": "architecture_data",
        "class_anchor": "architectures.html#extra_platforms.architecture.Architecture",
    },
    "Platform": {
        "page": "platforms.html",
        "module": "platform_data",
        "class_anchor": "platforms.html#extra_platforms.platform.Platform",
    },
    "CI": {
        "page": "ci.html",
        "module": "ci_data",
        "class_anchor": "ci.html#extra_platforms.ci.CI",
    },
}


def make_rst_link(text, url):
    """Create a reStructuredText link."""
    return f"`{text} <{url}>`_"


def make_pytest_decorator_line(obj_id):
    """Create pytest decorator documentation line."""
    return f"- **Pytest decorators**: {make_rst_link(f'@skip_{obj_id} / @unless_{obj_id}', 'pytest.html#decorators-reference')}"


def autodoc_process_docstring(app, what, name, obj, options, lines):
    """Generate docstrings for Trait instances and Groups.

    These dataclass instances have a dynamic ``__doc__`` attribute set in their
    ``__post_init__`` method, but Sphinx autodoc doesn't pick it up by default
    for module-level constants. This hook reads the instance's ``__doc__`` and
    injects it into the documentation.

    For Group instances, we preserve the original attribute docstring from the
    source file and only append the metadata.
    """
    if isinstance(obj, Group):
        # For groups, preserve original docstring and append metadata.
        # The original docstring is already in `lines` from the source file.
        lines.append("")
        lines.append(f"- **ID**: ``{obj.id}``")
        lines.append(f"- **Name**: {obj.name}")
        lines.append(f"- **Icon**: {obj.icon}")
        lines.append(
            f"- **Canonical**: ``{obj.canonical}`` {'⬥' if obj.canonical else ''}"
        )

        lines.append(make_pytest_decorator_line(obj.id))

        # Add list of members with links to their definitions.
        if obj.members:
            member_links = []
            type_counts = {}

            for member_id, member in obj.items():
                class_name = type(member).__name__
                type_info = TRAIT_TYPE_INFO.get(class_name)
                if not type_info:
                    continue  # Skip unknown types

                # Count types
                if class_name not in type_counts:
                    type_counts[class_name] = {
                        "count": 0,
                        "anchor": type_info["class_anchor"],
                    }
                type_counts[class_name]["count"] += 1

                # Create member link
                symbol_name = member_id.upper()
                member_url = f"{type_info['page']}#extra_platforms.{type_info['module']}.{symbol_name}"
                member_links.append(make_rst_link(symbol_name, member_url))

            if member_links:
                # Format type information with links
                type_parts = [
                    f"{info['count']} {make_rst_link(type_name, info['anchor'])}"
                    for type_name, info in sorted(type_counts.items())
                ]
                type_info = ", ".join(type_parts)
                lines.append(f"- **Members** ({type_info}): {', '.join(member_links)}")

    elif isinstance(obj, Trait):
        # For traits, replace with their dynamic docstring + metadata.
        lines.clear()
        if obj.__doc__:
            lines.append(obj.__doc__)
        lines.append("")
        lines.append(f"- **ID**: ``{obj.id}``")
        lines.append(f"- **Name**: {obj.name}")
        lines.append(f"- **Icon**: {obj.icon}")
        lines.append(f"- **Reference**: <{obj.url}>_")

        if obj.detection_function_name:
            detection_url = make_rst_link(
                f"{obj.detection_function_name}()",
                f"detection.html#extra_platforms.detection.{obj.detection_function_name}",
            )
        else:
            detection_url = "N/A"
        lines.append(f"- **Detection function**: {detection_url}")

        lines.append(make_pytest_decorator_line(obj.id))

        # Add list of groups this trait belongs to.
        trait_groups = [group for group in ALL_GROUPS if obj.id in group.member_ids]
        if trait_groups:
            group_links = [
                make_rst_link(
                    f"{group.id.upper()}{' ⬥' if group.canonical else ''}",
                    f"groups.html#extra_platforms.group_data.{group.id.upper()}",
                )
                for group in sorted(trait_groups, key=lambda g: g.id)
            ]
            lines.append(f"- **Groups** ({len(group_links)}): {', '.join(group_links)}")


def autodoc_skip_member(app, what, name, obj, skip, options):
    """Force inclusion of Trait instances and Groups.

    By default, autodoc skips module-level constants without docstrings.
    Since our trait instances have dynamically generated docstrings, we need
    to explicitly include them.
    """
    if isinstance(obj, (Trait, Group)):
        return False  # Don't skip - include in documentation
    return None  # Use default behavior for everything else


def setup(app):
    """Connect Sphinx events to custom handlers."""
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-skip-member", autodoc_skip_member)
