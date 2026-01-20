from __future__ import annotations

import sys
from pathlib import Path

from extra_platforms import Group, Trait
from extra_platforms._docstrings import get_attribute_docstring

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]


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

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

nitpicky = True

# Suppress specific warnings that are unavoidable or cosmetic.
suppress_warnings = [
    # Example: "WARNING: Cannot resolve forward reference in type annotations of
    # "extra_platforms.pytest.skip_aarch64": name 'Mark' is not defined"
    # Explanation: Pytest decorators are dynamically generated at import time, and the
    # pytest.Mark type is not available during Sphinx documentation build. These are
    # cosmetic warnings that don't affect the generated documentation.
    "sphinx_autodoc_typehints.forward_reference",
    # Example: "/Users/kde/code/extra-platforms/docs/architectures.md:305: WARNING:
    # Ignoring "mermaid" directive without content. [docutils]"
    # Explanation: The autoclasstree extension sometimes generates empty mermaid
    # directives for certain module structures. These are harmless and don't affect
    # the documentation output.
    "myst.directive",
    # Example: "/Users/kde/code/extra-platforms/tests/test_sphinx_crossrefs.py:docstring
    # of tests.test_sphinx_crossrefs.has_linked_reference:9: ERROR: Unexpected
    # indentation. [docutils]"
    # Explanation: Some code examples in docstrings may have indentation that triggers
    # reStructuredText parsing warnings. These are typically in test files and don't
    # affect the main documentation.
    "docutils",
]

# Concatenates the docstrings of the class and the __init__ method.
autoclass_content = "both"
# Keep the same ordering as in original source code.
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

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


def autodoc_process_docstring(app, what, name, obj, options, lines):
    """Process docstrings for Trait instances, Groups, and frozenset collections.

    Trait and Group instances have their docstrings generated at creation time
    via their generate_docstring() methods. This hook only needs to handle
    frozenset collections, which need their docstrings fetched from source files.
    """
    if isinstance(obj, frozenset):
        # Handle frozenset collections - fetch their docstrings from source modules.
        # Map collection names to their source modules.
        collection_modules = {
            "ALL_GROUPS": "group_data",
            "ALL_PLATFORM_GROUPS": "group_data",
            "ALL_ARCHITECTURE_GROUPS": "group_data",
            "ALL_CI_GROUPS": "group_data",
            "EXTRA_GROUPS": "group_data",
            "NON_OVERLAPPING_GROUPS": "group_data",
            "ALL_GROUP_IDS": "group_data",
            "ALL_TRAIT_IDS": "group_data",
            "ALL_IDS": "group_data",
        }

        # Extract the symbol name from the full qualified name.
        symbol_name = name.split(".")[-1]

        if symbol_name in collection_modules:
            source_module = collection_modules[symbol_name]
            source_docstring = get_attribute_docstring(
                f"extra_platforms.{source_module}", symbol_name
            )
            if source_docstring:
                # Clear the generic frozenset docstring and replace with the actual one.
                lines.clear()
                lines.extend(source_docstring.strip().split("\n"))


def autodoc_skip_member(app, what, name, obj, skip, options):
    """Force inclusion of Trait instances and Groups, skip detection functions from main module.

    By default, autodoc skips module-level constants without docstrings.
    Since our trait instances have dynamically generated docstrings, we need
    to explicitly include them.

    Also skip detection functions (is_*) when documenting the main extra_platforms
    module, since they're already documented in detection.md. This prevents duplicate
    documentation and ensures cross-references point to detection.html.
    """
    if isinstance(obj, (Trait, Group)):
        return False  # Don't skip - include in documentation

    # Skip detection functions, operations functions, and main classes when
    # documenting the root module via RST.
    # Detection functions fall into two categories:
    # 1. Trait detection functions (is_<trait>, current_*) defined in
    #    extra_platforms.detection
    # 2. Group detection functions (is_<group>) dynamically generated in
    #    extra_platforms.__init__
    #
    # Main classes (Trait, Group, Platform, Architecture, CI) are explicitly
    # documented in their respective pages (trait.md, groups.md) and should not
    # appear in extra_platforms.html to avoid duplicate documentation.
    if what == "module":
        obj_module = getattr(obj, "__module__", None)

        # Skip all detection functions (both from detection module and dynamically
        # generated group detection functions)
        if obj_module in (
            "extra_platforms.detection",
            "extra_platforms",
        ) and name.startswith(("is_", "current_")):
            return True  # Skip - already documented in detection.md

        # Skip invalidate_caches - documented in detection.md
        if name == "invalidate_caches" and obj_module in (
            "extra_platforms.detection",
            "extra_platforms",
        ):
            return True  # Skip - already documented in detection.md

        # Skip internal implementation functions that are wrapped
        if (
            name == "_current_platforms_impl"
            and obj_module == "extra_platforms._deprecated"
        ):
            return True  # Skip - internal implementation detail

        # Skip group utility functions - documented in groups.md
        if obj_module == "extra_platforms.group" and name in (
            "groups_from_ids",
            "traits_from_ids",
            "reduce",
        ):
            return True  # Skip - already documented in groups.md

        # Skip main trait and group classes - they're documented in their own pages
        if obj_module in (
            "extra_platforms.trait",
            "extra_platforms.group",
        ) and name in ("Trait", "Platform", "Architecture", "CI", "Group"):
            return True  # Skip - already documented in trait.md or groups.md

    return None  # Use default behavior for everything else


def setup(app):
    """Connect Sphinx events to custom handlers."""
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-skip-member", autodoc_skip_member)
