from __future__ import annotations

import tomllib
from datetime import date
from pathlib import Path

from click_extra.sphinx.announcement import years_since

from extra_platforms import is_github_ci

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

# Canonical origin of the published site, read from the one place that declares
# it. The trailing slash is mandatory: Sphinx joins page paths onto it verbatim
# to build each `<link rel="canonical">`, and sphinx-sitemap concatenates it with
# every page link.
docs_site_url = toml_config["project"]["urls"]["Documentation"].rstrip("/") + "/"
author = ", ".join(author["name"] for author in toml_config["project"]["authors"])

# Title-case each word of the project ID.
project = " ".join(word.title() for word in project_id.split("-"))

# GitHub account owning the project. Factored out so a rename touches one line
# instead of every URL built from it below (repository, sponsors).
github_user = "kdeldycke"

# Whole years since `1.0.0` (2024-08-19), the oldest entry of the changelog, for
# the announcement banner below.
maintained_years = years_since(date(2024, 8, 19))

# Addons.
extensions = [
    # Core Sphinx.
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # UI/UX add-ons.
    "sphinx_copybutton",
    "sphinx_design",
    # Emits sitemap.xml from html_baseurl, so crawlers find the API reference as
    # well as the guide pages.
    "sphinx_sitemap",
    "sphinxext.opengraph",
    # MyST and live rendering.
    "myst_parser",
    # Converts MyST-flavored docstrings to reST for autodoc. Must be listed
    # before sphinx_autodoc_typehints so the MyST→reST pass runs first; otherwise
    # the inline-code converter doubles the backticks inside domain-qualified roles
    # (like :py:obj:`None`) that sphinx_autodoc_typehints injects.
    "click_extra.sphinx.myst_docstrings",
    "sphinx_autodoc_typehints",
    "click_extra.sphinx",
    "sphinxcontrib.mermaid",
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
# Enable an extension only once the docs use its syntax.
myst_enable_extensions = [
    # Render GitHub-style alerts (> [!NOTE], > [!WARNING], …) as admonitions.
    # readme.md, changelog.md and install.md use them, and are pulled into the
    # docs via {include}; without this they degrade to plain blockquotes.
    "alert",
    "replacements",
    "smartquotes",
]
# XXX Allow ```mermaid``` directive to be used without curly braces
# (```{mermaid}```), see:
# https://github.com/mgaitan/sphinxcontrib-mermaid/issues/99#issuecomment-2339587001
myst_fence_as_directive = ["mermaid"]

# Register every heading as a resolvable cross-reference target so in-page
# `[text](#anchor)` links resolve at build time. The slug function is pinned
# to myst-parser's `docutils` preset, which returns the IDs of docutils'
# `make_id`, so MyST anchors match the section IDs docutils already emits,
# keeping existing anchor URLs stable.
myst_heading_anchors = 6
myst_heading_slug_func = "docutils"

# A fragment link that resolves nowhere fails the build: myst-parser only warns
# with `myst.xref_missing`, then ships the link dead. So does a docstring
# `{todo}` that no page renders, which the todolist page cannot list. CI fails on
# every warning through `[tool.repomatic] sphinx.fail-on-warning`, so this list
# is what still fails a local build run without `--fail-on-warning`.
click_extra_fail_on_warnings = ["click_extra.todo_unrendered", "myst.xref_missing"]

# Anchor each changelog release on its version, like `#v15-0-0`, in place of a
# positional `#idN`, which every new release moves down by one.
click_extra_release_anchors = True

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
    # Example: "Document headings start at H2, not H1"
    # Explanation: readme.md starts at H2 because GitHub supplies the H1 from
    # the repository name. The heading structure is intentional.
    "myst.header",
]

linkcheck_ignore = [
    # claude.ai/code requires authentication.
    r"https://claude\.ai/code",
    # These sites return 403/418 to bots but are valid.
    r"https://www\.slackware\.com",
    r"https://software\.opensuse\.org/",
    # Intermittently unreachable from CI.
    r"https://([^/]+\.)?gnu\.org",
    r"https://midnightbsd\.org",
]

# GitHub renders issue comments, README tab anchors and blob line anchors with
# JavaScript, so the linkcheck builder cannot find them in the static HTML: skip
# anchor checks for the whole host.
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

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Prefix document path to section labels, to use:
# `path/to/file:heading` instead of just `heading`
autosectionlabel_prefix_document = True

# Point every page's `<link rel="canonical">` at the published site.
html_baseurl = docs_site_url
# sphinx-sitemap defaults to a `{lang}{version}{link}` layout meant for sites
# publishing several translations or versions side by side. This one publishes a
# single tree, so anything but the bare link yields sitemap entries that 404.
sitemap_url_scheme = "{link}"
# The generated navigation pages hold no content a crawler should index.
sitemap_excludes = ["genindex.html", "py-modindex.html", "search.html"]

# Theme config.
html_theme = "furo"
html_title = project
html_favicon = "assets/favicon.svg"
html_theme_options = {
    # Sidebar logo. Furo renders this pair as .only-light/.only-dark images
    # driven by its own theme state, so the logo follows the toggle. A single
    # html_logo cannot: assets/logo-square.svg is light-only, and its dark
    # wordmark nearly vanishes on the dark theme. Both files are 640x740 exports
    # of that SVG, so the swap holds geometry. Furo resolves them against
    # _static/, hence their html_static_path entries.
    "light_logo": "logo-square-light.png",
    "dark_logo": "logo-square-dark.png",
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

# OpenGraph social previews. sphinxext.opengraph joins ogp_image onto
# ogp_site_url, so every page emits the same absolute URL for its social card.
# The card is the site's own copy, served from _static/ (see below). Its alt text
# defaults to the site name, which is `project`.
ogp_site_url = docs_site_url
ogp_image = "_static/banner-social-light.png"

# Individual files are copied to the root of _static/, which is where Furo looks
# for the light_logo/dark_logo pair, and where the og:image card above lives.
# Listing docs/assets/ wholesale would drag every other asset along.
html_static_path = [
    "_static",
    "assets/banner-social-light.png",
    "assets/logo-square-dark.png",
    "assets/logo-square-light.png",
]
html_css_files = ["custom.css"]

# Copied verbatim to the root of the build, where GitHub Pages looks for the page
# it serves for a path the site does not publish. `html_static_path` would bury it
# under `_static/`.
html_extra_path = ["404.html"]

# Do not publish a copy of every source document under `_sources/`. Nothing links
# to it: no page this theme renders carries a source link. Both settings are
# named because they gate different halves of the feature, `html_copy_source`
# the files and `html_show_sourcelink` the link.
html_copy_source = False
html_show_sourcelink = False

# Copy only the commands of a session block, without their prompt: `$ ` for a
# shell, `>>> ` and `... ` for Python. A block holding no prompt is copied whole.
# Matching Pygments classes instead (`.gp`, `.go`) misses the output of a
# `{click:run}` block: its ANSI lexer draws colored lines as `-Ansi-*` spans and
# plain ones as bare text, so no output line carries `.go`.
copybutton_prompt_text = r"\$ |>>> |\.\.\. "
copybutton_prompt_is_regexp = True

# Footer content.
html_last_updated_fmt = "%Y-%m-%d"
copyright = f"{author} and contributors"
html_show_sphinx = False


def prune_build_artifacts(app: Sphinx, exception: Exception | None) -> None:
    """Delete what Sphinx leaves in the output tree that is not content.

    The HTML builder writes `.buildinfo` from a finish task unconditionally, and
    `.buildinfo.bak` when its configuration check fails, so removing them once
    the build ends is the only way to keep them out of the published tree. They
    go in a GitHub Actions build alone: that build starts from an empty output
    directory, and its tree is the one that gets published. A local incremental
    build needs `.buildinfo`: without it, Sphinx `9.2.0` compares file times only,
    so a changed html-only setting like `html_title` leaves every page as it was.
    `_sources/` is created before `html_copy_source` is consulted, so it is
    removed here only while empty.
    """
    if exception:
        return
    outdir = Path(app.outdir)
    if is_github_ci():
        for marker in (".buildinfo", ".buildinfo.bak"):
            (outdir / marker).unlink(missing_ok=True)
    sources = outdir / "_sources"
    if sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: Sphinx) -> None:
    """Connect the build hook defined above."""
    app.connect("build-finished", prune_build_artifacts)
