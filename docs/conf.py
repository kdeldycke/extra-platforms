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
    "sphinxext.opengraph",
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "click_extra.sphinx",
    "sphinxcontrib.mermaid",
    # Converts MyST-flavored docstrings to reST for autodoc. Must be listed
    # before sphinx_autodoc_typehints so the MyST→reST pass runs first; otherwise
    # the inline-code converter doubles the backticks inside domain-qualified roles
    # (like :py:obj:`None`) that sphinx_autodoc_typehints injects.
    "click_extra.sphinx.myst_docstrings",
    "sphinx_autodoc_typehints",
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    # Render GitHub-style alerts (> [!NOTE], > [!WARNING], …) as admonitions.
    # readme.md, changelog.md and install.md use them, and are pulled into the
    # docs via {include}; without this they degrade to plain blockquotes.
    "alert",
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "fieldlist",
    "replacements",
    "smartquotes",
    "strikethrough",
    "tasklist",
]
# XXX Allow ```mermaid``` directive to be used without curly braces (```{mermaid}```), see:
# https://github.com/mgaitan/sphinxcontrib-mermaid/issues/99#issuecomment-2339587001
myst_fence_as_directive = ["mermaid"]

# Register every heading as a resolvable cross-reference target so in-page
# `[text](#anchor)` links resolve at build time. The slug function is pinned
# to docutils' `make_id` so MyST anchors match the section IDs docutils
# already emits, keeping existing anchor URLs stable.
myst_heading_anchors = 6
myst_heading_slug_func = "docutils.nodes.make_id"

mermaid_d3_zoom = True

# Enable the `{python:run}` execution directive used by docs/cli.md to render
# the CLI `--help` screen live at build time. Disabled by default upstream since
# click-extra `v7.15.0` because these directives execute arbitrary Python at
# build time; without the flag every directive reference logs an "Unknown
# directive" warning and the live block renders empty.
click_extra_enable_exec_directives = True

exclude_patterns = ["_build", "_linkcheck", "html", "Thumbs.db", ".DS_Store"]

nitpicky = True

# Suppress specific warnings that are unavoidable or cosmetic.
suppress_warnings = [
    # Example: "WARNING: Cannot resolve forward reference in type annotations of
    # "extra_platforms.pytest.skip_aarch64": name 'Mark' is not defined"
    # Explanation: Pytest decorators are dynamically generated at import time, and the
    # pytest.Mark type is not available during Sphinx documentation build. These are
    # cosmetic warnings that don't affect the generated documentation.
    "sphinx_autodoc_typehints.forward_reference",
    # Example: "Ignoring "mermaid" directive without content. [myst.directive]"
    # Explanation: The autoclasstree extension sometimes generates empty mermaid
    # directives for certain module structures.
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
    # Example: "Strikethrough is currently only supported in HTML output"
    # Explanation: CLAUDE.md uses ~~text~~ for incorrect spellings. We only
    # build HTML, so the rendering is fine.
    "myst.strikethrough",
    # Example: "Document headings start at H2, not H1"
    # Explanation: readme.md starts at H2 because GitHub supplies the H1 from
    # the repository name. The heading structure is intentional.
    "myst.header",
]

linkcheck_ignore = [
    # These sites return 403/418 to bots but are valid.
    r"https://doi\.org/10\.5281/zenodo\.",
    r"https://claude\.ai/code",
    r"https://www\.freedesktop\.org/software/systemd/man/",
    r"https://www\.slackware\.com",
    r"https://zenodo\.org/",
    # Sites intermittently unreachable from CI runners.
    r"https://([^/]+\.)?gnu\.org",
    r"https://midnightbsd\.org",
]

# GitHub renders issue comments, README tab anchors and blob line anchors with
# JavaScript, so the linkcheck builder cannot find them in the static HTML.
linkcheck_anchors_ignore = [
    r"issuecomment-\d+",
    r"readme",
    r"L\d+",
]

# GitHub README anchors are JS-rendered and invisible to linkcheck.
linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/",
]

# Some links time out the linkcheck bot intermittently; retry before
# reporting them as broken.
linkcheck_retries = 3

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

github_user = "kdeldycke"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Prefix document path to section labels, to use:
# `path/to/file:heading` instead of just `heading`
autosectionlabel_prefix_document = True

# Theme config.
html_theme = "furo"
html_title = project
html_logo = "assets/logo-square.svg"
html_favicon = "assets/favicon.svg"
html_theme_options = {
    "sidebar_hide_name": True,
    # Activates edit links.
    "source_repository": f"https://github.com/{github_user}/{project_id}",
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

html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Footer content.
html_last_updated_fmt = "%Y-%m-%d"
copyright = f"{author} and contributors"
html_show_sphinx = False
