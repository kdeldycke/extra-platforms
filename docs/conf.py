from __future__ import annotations

from pathlib import Path

import tomllib  # type: ignore[import-not-found]  # stdlib >=3.11; docs require >=3.12.


project_path = Path(__file__).parent.parent.resolve()

# Fetch general information about the project from pyproject.toml.
toml_path = project_path / "pyproject.toml"
toml_config = tomllib.loads(toml_path.read_text(encoding="utf-8"))

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
    # Example: "local id not found in doc 'groups': 'extra_platforms.Group.canonical'"
    # Explanation: MyST validates cross-reference anchors before autodoc has generated
    # them. These are false positives — the anchors exist in the final output.
    "myst.xref_missing",
    # Example: "Domain 'click_extra.sphinx.click::click' has not implemented a
    # `resolve_any_xref` method"
    # Explanation: Upstream limitation in the click-extra Sphinx extension.
    "myst.domains",
]

nitpick_ignore = [
    # Private base class, excluded from public documentation.
    ("py:class", "extra_platforms.trait._Identifiable"),
]

# Concatenates the docstrings of the class and the __init__ method.
autoclass_content = "both"
# Keep the same ordering as in original source code.
autodoc_member_order = "bysource"
always_use_bars_union = True

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
html_show_sphinx = False
