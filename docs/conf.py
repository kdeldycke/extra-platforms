from __future__ import annotations

import tomllib
from datetime import UTC, date, datetime
from pathlib import Path

TYPE_CHECKING = False
if TYPE_CHECKING:
    from sphinx.application import Sphinx

project_path = Path(__file__).parent.parent.resolve()

# Fetch general information about the project from pyproject.toml.
toml_path = project_path / "pyproject.toml"
toml_config = tomllib.loads(toml_path.read_text(encoding="UTF-8"))

# Redistribute pyproject.toml config to Sphinx.
project_id = toml_config["project"]["name"]
version = release = toml_config["project"]["version"]
author = ", ".join(author["name"] for author in toml_config["project"]["authors"])

# Title-case each word of the project ID.
project = " ".join(word.title() for word in project_id.split("-"))

# Whole years since `1.0.0` (2024-08-19), the oldest entry of the changelog, for
# the announcement banner below. Floored, so the figure is never ahead of the
# anniversary it claims.
maintained_years = (datetime.now(tz=UTC).date() - date(2024, 8, 19)).days // 365

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
# XXX Allow ```mermaid``` directive to be used without curly braces
# (```{mermaid}```), see:
# https://github.com/mgaitan/sphinxcontrib-mermaid/issues/99#issuecomment-2339587001
myst_fence_as_directive = ["mermaid"]

# Register every heading as a resolvable cross-reference target so in-page
# `[text](#anchor)` links resolve at build time. The slug function is pinned
# to docutils' `make_id` so MyST anchors match the section IDs docutils
# already emits, keeping existing anchor URLs stable.
myst_heading_anchors = 6
myst_heading_slug_func = "docutils.nodes.make_id"

# A fragment link that resolves nowhere fails the build: myst-parser only warns
# with `myst.xref_missing`, then ships the link dead.
click_extra_fail_on_warnings = ["myst.xref_missing"]

mermaid_d3_zoom = True

# Enable the `{python:render}` and `{python:run}` execution directives. They
# render the trait and group tables, the diagrams and the CLI `--help` screen
# live at build time. Disabled by default upstream since click-extra `v7.15.0`
# because these directives execute arbitrary Python at build time; without the
# flag every directive reference logs an "Unknown directive" warning and the
# live block renders empty.
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
    # Example: "docs/platforms.md:390: WARNING: Ignoring "mermaid" directive without
    # content. [docutils]"
    # Explanation: `autoclasstree` renders an empty mermaid diagram for each
    # `*_data` module, which defines no class.
    "docutils",
    # Example: "Domain 'click_extra.sphinx.click::click' has not implemented a
    # `resolve_any_xref` method"
    # Explanation: Upstream limitation in the click-extra Sphinx extension.
    "myst.domains",
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
    # Sits atop every page, so it stays a single line and leads with the track
    # record rather than pleading scarcity: how thin the maintenance is says
    # nothing to a reader who has not yet decided the project is worth funding.
    # The age is recomputed at build time, so the claim never goes stale. Each
    # call to action opens on its emoji, which gives the eye two markers to land
    # on in a line that is otherwise unbroken prose.
    "announcement": (
        f"{project} has been maintained for {maintained_years}+ years, and is "
        "free to use. You can help if you "
        "<strong><a class='reference external' "
        f"href='https://github.com/sponsors/{github_user}'>"
        "🤝 purchase business support</a></strong> or "
        "<strong><a class='reference external' "
        f"href='https://github.com/sponsors/{github_user}'>"
        "🫶 sponsor the project</a></strong>."
    ),
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Do not publish a copy of every source document under `_sources/`. Nothing links
# to it: no page this theme renders carries a source link. Both settings are
# named because they gate different halves of the feature, `html_copy_source`
# the files and `html_show_sourcelink` the link.
html_copy_source = False
html_show_sourcelink = False

# Footer content.
html_last_updated_fmt = "%Y-%m-%d"
copyright = f"{author} and contributors"
html_show_sphinx = False


def drop_unused_viewcode_modules(app: object, env: object) -> None:
    """Forget each module `sphinx.ext.viewcode` read but no document links.

    `viewcode` reads the source of every module a documented object may come
    from, and keeps an entry for that module even when none of its objects gets
    a `[source]` link. A serial read drops such an entry when it purges the next
    document. A parallel read merges the entries of its workers after every
    purge has run, so each unused module becomes a published page that nothing
    links to (sphinx-doc/sphinx#14675). Dropping the entries with no recorded
    use gives both reads the same output.
    """
    modules = getattr(env, "_viewcode_modules", {})
    for modname, entry in list(modules.items()):
        # A module viewcode could not read is `False`. A read one is a tuple of
        # its code, its tags, the objects documented from it, and its refname.
        if entry and not entry[2]:
            del modules[modname]


def prune_build_artifacts(app: Sphinx, exception: Exception | None) -> None:
    """Delete what Sphinx leaves in the output tree that is not content.

    The HTML builder writes `.buildinfo` from a finish task unconditionally, and
    `.buildinfo.bak` when its configuration check fails, so removing them once
    the build ends is the only way to keep them out of the published tree.
    `_sources/` is created before `html_copy_source` is consulted, so it is
    removed here only while empty. The next local incremental build then finds
    no marker and re-reads every document.
    """
    if exception:
        return
    outdir = Path(app.outdir)
    for marker in (".buildinfo", ".buildinfo.bak"):
        (outdir / marker).unlink(missing_ok=True)
    sources = outdir / "_sources"
    if sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: Sphinx) -> None:
    """Connect the build hooks defined above."""
    app.connect("env-updated", drop_unused_viewcode_modules)
    app.connect("build-finished", prune_build_artifacts)
