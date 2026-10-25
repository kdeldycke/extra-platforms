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
"""Tests for Sphinx cross-reference rendering in the real documentation.

These tests verify that cross-references in the built documentation (./docs/_build/)
resolve to actual links with correct href attributes. Unlike mock-based tests,
these catch real regressions in the actual documentation.
"""

from __future__ import annotations

import functools
import importlib.util
import inspect
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_TRAITS,
    CI,
    Agent,
    Architecture,
    Group,
    Platform,
    Shell,
    Terminal,
    Trait,
)
from extra_platforms.pytest import unless_linux

# Third-party modules the docs build imports: the theme and every extension
# docs/conf.py loads that Sphinx does not ship.
DOCS_BUILD_MODULES = (
    "click_extra",
    "furo",
    "myst_parser",
    "sphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinxext.opengraph",
)


def importable(module: str) -> bool:
    """Tell whether ``module`` resolves in the running interpreter."""
    try:
        return importlib.util.find_spec(module) is not None
    except ModuleNotFoundError:
        # A dotted name whose parent package is missing.
        return False


# The docs workflow builds on ubuntu-slim with Python >= 3.12 (the docs dependency
# group minimum). Only run sphinx tests under the same conditions.
pytestmark = [
    unless_linux,
    pytest.mark.skipif(
        sys.version_info < (3, 12),
        reason="docs dependency group requires Python >= 3.12",
    ),
    # The docs are built with the running interpreter, so its environment must
    # hold the docs group.
    pytest.mark.skipif(
        not all(map(importable, DOCS_BUILD_MODULES)),
        reason="needs the docs dependency group to build the docs",
    ),
    # Sphinx crashes with a FileNotFoundError on searchindex.js.tmp when
    # concurrent builds share the same output directory (sphinx-doc/sphinx#13702).
    # Force all tests in this module onto a single xdist worker.
    pytest.mark.xdist_group("sphinx"),
]

# Path to the built documentation. Matches the CI docs workflow output
# directory, which is already covered by the stock .gitignore rules.
DOCS_HTML_DIR = Path(__file__).parent.parent / "docs" / "_build"

# Modules absent from every autodoc directive in ./docs/, so their docstring
# cross-references have no rendered anchors to resolve against. Remove an
# entry to re-arm anchor checks the day its module joins the documentation.
UNRENDERED_MODULES = frozenset((
    "extra_platforms/__main__.py",
    "extra_platforms/_deprecated.py",
    "extra_platforms/_docs.py",
))


@pytest.fixture(scope="module")
def built_docs() -> Path:
    """Ensure the documentation is built and return the path to the HTML directory.

    This fixture builds the documentation if it doesn't exist or is outdated.
    """
    if not DOCS_HTML_DIR.exists():
        # Build the documentation with the interpreter the module gate checked.
        subprocess.run(
            [sys.executable, "-m", "sphinx", "-b", "html", "./docs", "./docs/_build"],
            check=True,
            cwd=Path(__file__).parent.parent,
        )
    return DOCS_HTML_DIR


@functools.cache
def read_html(built_docs: Path, filename: str) -> str:
    """Read an HTML file from the built documentation, once per session.

    Only the top level of the build is read: `_modules/` holds viewcode pages
    sharing the basenames of the real pages, like `detection.html`.
    """
    html_path = built_docs / filename
    assert html_path.exists(), f"HTML file not found: {html_path}"
    return html_path.read_text(encoding="utf-8")


def find_links_with_text(html: str, link_text: str) -> list[str]:
    """Find all href values for links whose text is exactly the given text.

    Returns a list of href values for <a> tags whose plain text equals the
    specified text, so a link to `LINUX_LIKE` never stands in for one to `LINUX`.
    The function handles nested tags like <a href="..."><code><span>text</span></code></a>.
    """
    results = []
    # Pattern to match <a ...href="..."...>...</a> including nested tags.
    pattern = r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    for match in re.finditer(pattern, html, re.DOTALL):
        href, content = match.groups()
        # Strip HTML tags from content to get plain text.
        plain_text = re.sub(r"<[^>]+>", "", content)
        if plain_text.strip() == link_text:
            results.append(href)
    return results


def has_linked_reference(html: str, text: str, expected_href_fragment: str) -> bool:
    """Check if the HTML contains a link with the given text pointing to the expected href.

    :param html: The HTML content to search.
    :param text: The link text to find (like ``"AARCH64"``, ``"is_linux()"``).
    :param expected_href_fragment: The end of the expected href (like
        ``"architectures.html#extra_platforms.AARCH64"``), so an anchor that only
        starts with it, like ``#extra_platforms.ARMV6L`` for ``ARM``, does not match.
    :returns: ``True`` if a matching link is found.
    """
    hrefs = find_links_with_text(html, text)
    return any(href.endswith(expected_href_fragment) for href in hrefs)


@pytest.mark.parametrize(
    ("page", "link_text", "href_fragment"),
    [
        # Group symbols on groups.html.
        ("groups.html", "ALL_ARCHITECTURES", "#extra_platforms.ALL_ARCHITECTURES"),
        ("groups.html", "ALL_PLATFORMS", "#extra_platforms.ALL_PLATFORMS"),
        ("groups.html", "ALL_SHELLS", "#extra_platforms.ALL_SHELLS"),
        ("groups.html", "LINUX", "#extra_platforms.LINUX"),
        ("groups.html", "BSD", "#extra_platforms.BSD"),
        ("groups.html", "UNIX", "#extra_platforms.UNIX"),
        ("groups.html", "BOURNE_SHELLS", "#extra_platforms.BOURNE_SHELLS"),
        # Group detection functions on groups.html.
        (
            "groups.html",
            "is_any_architecture()",
            "detection.html#extra_platforms.is_any_architecture",
        ),
        (
            "groups.html",
            "is_any_platform()",
            "detection.html#extra_platforms.is_any_platform",
        ),
        (
            "groups.html",
            "is_any_shell()",
            "detection.html#extra_platforms.is_any_shell",
        ),
        ("groups.html", "is_linux()", "detection.html#extra_platforms.is_linux"),
        ("groups.html", "is_bsd()", "detection.html#extra_platforms.is_bsd"),
        ("groups.html", "is_unix()", "detection.html#extra_platforms.is_unix"),
        # Pytest decorator table symbols.
        ("pytest.html", "AARCH64", "architectures.html#extra_platforms.AARCH64"),
        ("pytest.html", "UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("pytest.html", "BASH", "shells.html#extra_platforms.BASH"),
        ("pytest.html", "GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        ("pytest.html", "LINUX", "groups.html#extra_platforms.LINUX"),
        # Pytest decorator docstrings.
        (
            "pytest.html",
            "is_aarch64()",
            "detection.html#extra_platforms.is_aarch64",
        ),
        # Detection table symbols.
        (
            "detection.html",
            "AARCH64",
            "architectures.html#extra_platforms.AARCH64",
        ),
        ("detection.html", "UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("detection.html", "BASH", "shells.html#extra_platforms.BASH"),
        ("detection.html", "GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        ("detection.html", "LINUX", "groups.html#extra_platforms.LINUX"),
        # Trait table symbols.
        ("trait.html", "AARCH64", "architectures.html#extra_platforms.AARCH64"),
        ("trait.html", "UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("trait.html", "BASH", "shells.html#extra_platforms.BASH"),
        ("trait.html", "GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        # Trait table detection functions.
        (
            "trait.html",
            "is_aarch64()",
            "detection.html#extra_platforms.is_aarch64",
        ),
        ("trait.html", "is_ubuntu()", "detection.html#extra_platforms.is_ubuntu"),
        ("trait.html", "is_bash()", "detection.html#extra_platforms.is_bash"),
        (
            "trait.html",
            "is_github_ci()",
            "detection.html#extra_platforms.is_github_ci",
        ),
        # Platform symbols.
        ("platforms.html", "UBUNTU", "#extra_platforms.UBUNTU"),
        ("platforms.html", "MACOS", "#extra_platforms.MACOS"),
        ("platforms.html", "WINDOWS", "#extra_platforms.WINDOWS"),
        ("platforms.html", "DEBIAN", "#extra_platforms.DEBIAN"),
        # Platform detection functions.
        (
            "platforms.html",
            "is_ubuntu()",
            "detection.html#extra_platforms.is_ubuntu",
        ),
        (
            "platforms.html",
            "is_macos()",
            "detection.html#extra_platforms.is_macos",
        ),
        (
            "platforms.html",
            "is_windows()",
            "detection.html#extra_platforms.is_windows",
        ),
        # Architecture symbols.
        ("architectures.html", "AARCH64", "#extra_platforms.AARCH64"),
        ("architectures.html", "X86_64", "#extra_platforms.X86_64"),
        ("architectures.html", "ARM", "#extra_platforms.ARM"),
        # Shell symbols.
        ("shells.html", "BASH", "#extra_platforms.BASH"),
        ("shells.html", "POWERSHELL", "#extra_platforms.POWERSHELL"),
        # CI symbols.
        ("ci.html", "GITHUB_CI", "#extra_platforms.GITHUB_CI"),
        ("ci.html", "GITLAB_CI", "#extra_platforms.GITLAB_CI"),
        ("ci.html", "TRAVIS_CI", "#extra_platforms.TRAVIS_CI"),
        # Terminal symbols.
        ("terminals.html", "KITTY", "#extra_platforms.KITTY"),
        ("terminals.html", "ALACRITTY", "#extra_platforms.ALACRITTY"),
        ("terminals.html", "TMUX", "#extra_platforms.TMUX"),
        # Agent symbols.
        ("agents.html", "CLAUDE_CODE", "#extra_platforms.CLAUDE_CODE"),
        ("agents.html", "CLINE", "#extra_platforms.CLINE"),
        ("agents.html", "CURSOR", "#extra_platforms.CURSOR"),
        # Cross-page references.
        ("platforms.html", "LINUX", "groups.html#extra_platforms.LINUX"),
        (
            "architectures.html",
            "is_aarch64()",
            "detection.html#extra_platforms.is_aarch64",
        ),
    ],
)
def test_rendered_links_point_to_correct_targets(
    built_docs, page, link_text, href_fragment
):
    """Smoke test: verify that specific rendered links point to expected targets."""
    html = read_html(built_docs, page)
    assert has_linked_reference(html, link_text, href_fragment), (
        f"{link_text} on {page} is not linked to {href_fragment}"
    )


def get_expected_page_for_symbol(role: str, symbol: str) -> str:
    """Determine the expected HTML page for a given symbol.

    :param role: The Sphinx role (func, data, class, etc.).
    :param symbol: The symbol name (like ``"UBUNTU"``, ``"is_linux"``,
        ``"Platform"``).
    :returns: The expected HTML filename (like ``"platforms.html"``).
    """
    # Clean symbol name (remove module prefix if present)
    symbol_clean = symbol.rsplit(".", maxsplit=1)[-1]

    # Detection functions always go to detection.html
    if role == "func" and (symbol_clean.startswith(("is_", "current_"))):
        return "detection.html"

    # Cache management functions go to detection.html
    if role == "func" and symbol_clean == "invalidate_caches":
        return "detection.html"

    # Platform information helpers are documented in platforms.html, next to
    # the Platform.info() method they feed.
    if symbol_clean in (
        "MACOS_CODENAMES",
        "get_macos_codename",
        "invalidate_os_release_cache",
        "linux_info",
        "macos_info",
        "os_release_id",
        "windows_info",
    ):
        return "platforms.html"

    # Shell path lookup is documented in shells.html, next to the shell usage
    # examples.
    if role == "func" and symbol_clean == "shell_from_path":
        return "shells.html"

    # Trait and group operations functions go to groups.html
    if role == "func" and symbol_clean in (
        "extract_members",
        "groups_from_ids",
        "traits_from_ids",
        "reduce",
    ):
        return "groups.html"

    # Classes - the base classes are documented in trait.html or groups.html
    if role == "class":
        # Group class is documented in groups.html
        if symbol_clean == "Group":
            return "groups.html"
        # All trait-related classes (Trait, Platform, Architecture, CI) are
        # documented in trait.html
        if symbol_clean in (
            "Trait",
            "Platform",
            "Architecture",
            "Shell",
            "Terminal",
            "CI",
            "Agent",
        ):
            return "trait.html"
        # Default to trait.html for other trait-related classes
        return "trait.html"

    # Group methods go to groups.html.
    if role == "meth" and symbol.startswith("Group."):
        return "groups.html"

    # Trait class methods/attributes go to trait.html.
    trait_classes = (
        "Trait.",
        "Architecture.",
        "Platform.",
        "Shell.",
        "Terminal.",
        "CI.",
        "Agent.",
    )
    if role in ("meth", "attr") and any(symbol.startswith(c) for c in trait_classes):
        return "trait.html"

    # Pytest decorators go to pytest.html
    if "pytest" in symbol or symbol_clean.startswith(("skip_", "unless_")):
        return "pytest.html"

    # Data symbols - look up the trait or group and use its doc_page
    if role == "data":
        # Group collections go to groups.html
        if symbol_clean in (
            "ALL_GROUPS",
            "ALL_PLATFORM_GROUPS",
            "ALL_ARCHITECTURE_GROUPS",
            "ALL_CI_GROUPS",
            "ALL_SHELL_GROUPS",
            "ALL_TERMINAL_GROUPS",
            "ALL_AGENT_GROUPS",
            "NON_CANONICAL_GROUPS",
            "CANONICAL_GROUPS",
        ):
            return "groups.html"

        # ID collections go to groups.html
        if symbol_clean in (
            "ALL_GROUP_IDS",
            "ALL_TRAIT_IDS",
            "ALL_IDS",
        ):
            return "groups.html"

        # Find the trait by symbol_id and use its doc_page
        for trait in ALL_TRAITS:
            if trait.symbol_id == symbol_clean:
                # Convert doc_page from .md to .html (e.g., "platforms.md" ->
                # "platforms.html")
                return trait.doc_page.replace(".md", ".html")

        # Find the group by symbol_id and use Group.doc_page
        for group in ALL_GROUPS:
            if group.symbol_id == symbol_clean:
                # All groups are documented in the same page (Group.doc_page =
                # "groups.md")
                return Group.doc_page.replace(".md", ".html")

    # Default to extra_platforms.html
    return "extra_platforms.html"


def _reference_matrix_rows() -> list[tuple[str, str, str]]:
    """Read the parameters of each example row of the Reference matrix.

    Each row of the table in `docs/sphinx.md` yields the MyST example of its first
    column, the text its rendered link must show, and the page and anchor that
    link must point to. Reading them from the page covers every row it holds,
    including one added later.
    """
    page = Path(__file__).parent.parent / "docs" / "sphinx.md"
    section = page.read_text(encoding="UTF-8").split("## Reference matrix", 1)[1]
    section = section.split("\n## ", 1)[0]
    rows = []
    for myst in re.findall(r"^\|\s*`` (\{\w+\}`[^`]+`) ``\s*\|", section, re.MULTILINE):
        role_match = re.fullmatch(r"\{(\w+)\}`~?([^`]+)`", myst)
        assert role_match, f"Unparsable Reference matrix example: {myst}"
        role, target = role_match.groups()
        leaf = target.rsplit(".", 1)[-1]
        text = f"{leaf}()" if role in ("func", "meth") else leaf
        link = f"{get_expected_page_for_symbol(role, target)}#extra_platforms.{target}"
        rows.append((myst, text, link))
    # An empty list would collect no case at all, and pass silently.
    assert rows, f"No Reference matrix example found in {page}"
    return rows


def _extract_reference_table_rows(html: str, myst: str) -> tuple[str, str, str]:
    """Return the (myst_html, rst_html, rendering_html) tuple for `myst`.

    Search the Reference matrix table and return the first row whose first
    column (stripped of HTML) exactly matches the provided `myst` directive
    string (e.g. ``"{data}`~UBUNTU`"``). The returned values are the raw HTML
    contents of the MyST, reST, and Rendering ``<td>`` cells for that row. If
    not found, fail the test.
    """
    idx = html.find("Reference matrix")
    assert idx != -1, "Reference matrix section not found in sphinx.html"
    table_start = html.find("<table", idx)
    assert table_start != -1, "Reference matrix table not found"
    table_end = html.find("</table>", table_start)
    assert table_end != -1, "Reference matrix table not terminated"
    table_html = html[table_start : table_end + len("</table>")]

    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(tds) < 3:
            continue
        first = re.sub(r"<[^>]+>", "", tds[0]).strip()
        if first == myst:
            return tds[0], tds[1], tds[2]

    pytest.fail(f"Reference matrix first-column entry not found: {myst}")


@pytest.mark.parametrize(
    ("myst", "expected_text", "expected_link"), _reference_matrix_rows()
)
def test_reference_matrix_links(built_docs, myst, expected_text, expected_link):
    """Parametrized check: the MyST directive in column 1 renders to a link in column 2.

    `myst` is the literal MyST role example as shown in the first column of the
    Reference matrix. `expected_link` is the expected href target used in the
    rendered Rendering column.
    """
    html = read_html(built_docs, "sphinx.html")
    first_html, rst_html, rendering_html = _extract_reference_table_rows(html, myst)

    # Ensure the first-column MyST example is wrapped in <span class="pre">...
    m1 = re.search(r'<span class="pre">(.*?)</span>', first_html, re.DOTALL)
    assert m1, (
        f"Reference matrix first-column for '{myst}' is not wrapped in "
        '<span class="pre">..."'
    )
    first_plain = re.sub(r"<[^>]+>", "", m1.group(1)).strip()
    assert first_plain == myst, (
        f"Reference matrix first-column span content '{first_plain}' does not "
        f"match expected myst '{myst}'"
    )

    # Verify the reST column contains the equivalent reST syntax.
    # The transformation is mechanical: {role} -> :role:.
    expected_rst = re.sub(r"\{(\w+)\}", r":\1:", myst)
    rst_span = re.search(r'<span class="pre">(.*?)</span>', rst_html, re.DOTALL)
    assert rst_span, f"Reference matrix reST column for '{myst}' holds no example"
    rst_plain = re.sub(r"<[^>]+>", "", rst_span.group(1)).strip()
    assert rst_plain == expected_rst, (
        f"Reference matrix reST column for '{myst}' has '{rst_plain}', "
        f"expected '{expected_rst}'"
    )

    # Ensure the rendering column is wrapped in <span class="pre">...
    m2 = re.search(r'<span class="pre">(.*?)</span>', rendering_html, re.DOTALL)
    assert m2, (
        f"Reference matrix rendering column for '{myst}' is not wrapped in "
        '<span class="pre">..."'
    )
    # The link may or may not sit inside the <span class="pre">: search the whole
    # rendering column.
    hrefs = re.findall(r'href="([^"]+)"', rendering_html)
    assert has_linked_reference(rendering_html, expected_text, expected_link), (
        f"Reference matrix example '{myst}' did not render a '{expected_text}' "
        f"link to {expected_link}; found {hrefs}"
    )


def _get_all_public_symbols() -> Iterator[str]:
    """Collect all public symbols from extra_platforms and pytest modules.

    Yields each symbol name as a string; ``pytest`` submodule symbols carry a
    ``pytest.`` prefix.
    """

    # Add all symbols exposed in extra_platforms root.
    for symbol_name in extra_platforms.__all__:
        yield symbol_name

    # Add all symbols exposed in extra_platforms.pytest.
    for symbol_name in dir(extra_platforms.pytest):
        if not symbol_name.startswith("_"):
            yield f"pytest.{symbol_name}"


@pytest.mark.parametrize("symbol_name", list(_get_all_public_symbols()))
def test_get_expected_page_for_symbol_handles_public_api(symbol_name):
    """Test that get_expected_page_for_symbol correctly handles each public symbol.

    This test validates that our logic correctly maps every symbol exposed in the
    public API from both extra_platforms and extra_platforms.pytest modules to the
    correct documentation page.

    :param symbol_name: The symbol name (like ``"UBUNTU"``, ``"is_linux"``,
        ``"pytest.skip_ubuntu"``).
    """
    if symbol_name.startswith("pytest."):
        role = "data"

    else:
        # Get the actual object to determine its role
        obj = getattr(extra_platforms, symbol_name)

        # Determine the role based on the object type
        # Order matters: check classes first, then instances, then functions
        if inspect.isclass(obj):
            role = "class"
        elif isinstance(
            obj, (Trait, Architecture, Platform, Shell, Terminal, CI, Agent, Group)
        ):
            # Trait and Group instances
            role = "data"
        elif inspect.isfunction(obj) or (
            callable(obj) and hasattr(obj, "__name__") and not inspect.isclass(obj)
        ):
            # Functions (including cached/wrapped functions)
            # Check __name__ to distinguish from other callables like modules
            role = "func"
        else:
            # Everything else is treated as data (constants, etc.)
            role = "data"

    expected_page = get_expected_page_for_symbol(role, symbol_name)

    assert expected_page != "extra_platforms.html", (
        f"Symbol {role}:`{symbol_name}` returned generic page: {expected_page}"
    )


def collect_all_refs() -> list[tuple[str, str, str]]:
    """Collect all cross-reference tuples (role, symbol, source_file).

    This helper is intentionally executed at collection time to generate
    parametrization values for the comprehensive cross-reference test. A file
    citing the same reference twice yields one tuple, and the tuples are sorted,
    so the order does not depend on the file system.
    """
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs"
    code_dir = project_root / "extra_platforms"

    all_refs: list[tuple[str, str, str]] = []

    myst_pattern = r"\{(\w+)\}`~?([^`]+)`"
    for md_file in docs_dir.glob("**/*.md"):
        content = md_file.read_text(encoding="utf-8")
        for role, symbol in re.findall(myst_pattern, content):
            all_refs.append((role, symbol, str(md_file.relative_to(project_root))))

    # Docstrings are MyST-flavored (rendered via
    # click_extra.sphinx.myst_docstrings), so code files are scanned for MyST
    # roles too. The reST pattern is kept for the rare reST-syntax roles that
    # survive the MyST→reST conversion pass.
    rst_pattern = r":(\w+):`~?([^`]+)`"
    for py_file in code_dir.glob("**/*.py"):
        content = py_file.read_text(encoding="utf-8")
        for pattern in (myst_pattern, rst_pattern):
            for role, symbol in re.findall(pattern, content):
                all_refs.append((role, symbol, str(py_file.relative_to(project_root))))

    return sorted(set(all_refs))


@pytest.mark.parametrize("role,symbol,source_file", collect_all_refs())
def test_all_crossreferences_point_to_correct_pages(
    built_docs, role, symbol, source_file
):
    """Parametrized check that a single cross-reference points to the expected page.

    The previous monolithic test iterated over all refs; this parametrized variant
    runs the same checks per-reference so failures are reported per-item.
    """
    # Skip documentation examples showing Sphinx role syntax (not actual
    # cross-references)
    if (
        "https://" in symbol
        or "http://" in symbol
        or "{" in symbol
        or "}" in symbol
        or symbol.startswith("](")
        or " " in symbol
        or "for inline" in symbol
    ):
        pytest.skip("Skipping documentation example syntax")

    # Skip certain roles that don't create cross-references to our code.
    # The ``attr`` role is skipped because attribute anchors include the class
    # name (e.g. ``extra_platforms.Group.canonical``) and the general anchor
    # construction logic does not handle that.
    if role in ("doc", "ref", "octicon", "mod", "attr"):
        pytest.skip(f"Skipping non-code role: {role}")

    # Skip references to external packages and Python builtins
    python_builtins = {
        "frozenset",
        "dict",
        "tuple",
        "list",
        "set",
        "str",
        "int",
        "float",
        "bool",
        "True",
        "False",
        "None",
        "SystemError",
        "NotImplementedError",
        "KeyError",
        "IndexError",
        "ValueError",
        "TypeError",
        "AttributeError",
        "RuntimeError",
        "DeprecationWarning",
        "UnicodeDecodeError",
        "Exception",
    }
    python_builtin_methods = {
        "remove",
        "add",
        "update",
        "pop",
        "clear",
        "copy",
        "fromkeys",
        "get",
        "items",
        "keys",
        "values",
        "append",
        "extend",
        "insert",
    }
    # Standard-library members (like ``os.environ``) resolve via intersphinx to the
    # Python docs, so they have no anchor on a local extra_platforms page to check.
    stdlib_symbols = {
        "os.environ",
    }
    if (
        symbol in python_builtins
        or symbol.split(".")[-1] in python_builtins
        or (role == "meth" and symbol in python_builtin_methods)
        or symbol in stdlib_symbols
    ):
        pytest.skip("Skipping builtin or standard-library symbol")

    if (
        symbol.startswith((
            "pytest.",
            "ast.",
            "collections.",
            "dict.",
            "frozenset.",
            "pathlib.",
            "platform.",
            "shlex.",
            "subprocess.",
            "sys.",
            "types.",
            "typing.",
        ))
        and not symbol.startswith("pytest.skip_")
        and not symbol.startswith("pytest.unless_")
    ):
        pytest.skip("External symbol reference")

    # Docstring references from modules the documentation never renders have
    # no anchors to check against.
    if source_file in UNRENDERED_MODULES:
        pytest.skip("Source module not rendered in the documentation")

    symbol_clean = symbol.split(".")[-1]
    if symbol_clean.startswith("ALL_") and symbol_clean.endswith(("_IDS", "_ID")):
        pytest.skip("Module-level ID collection")

    expected_page = get_expected_page_for_symbol(role, symbol)

    # Strip domain qualifier if present (e.g. "extra_platforms:extra_platforms.pytest.skip_linux"
    # becomes "extra_platforms.pytest.skip_linux").
    symbol_bare = symbol.split(":", 1)[-1] if ":" in symbol else symbol

    symbol_clean = symbol.split(".")[-1]
    if symbol_bare.startswith(("pytest.", "extra_platforms.pytest.")):
        if symbol_bare.startswith("extra_platforms."):
            expected_anchor = symbol_bare
        else:
            expected_anchor = f"extra_platforms.{symbol_bare}"
    elif role == "meth" and "." in symbol:
        # Method references like Group.union have anchors like
        # extra_platforms.Group.union.
        expected_anchor = f"extra_platforms.{symbol}"
    else:
        expected_anchor = f"extra_platforms.{symbol_clean}"

    # Symbols documented via automodule carry module-qualified anchors
    # (e.g. ``extra_platforms.group_data.ALL_GROUPS`` instead of
    # ``extra_platforms.ALL_GROUPS``), so accept either form. Derived from the
    # source file rather than listed per module, so a module joining the
    # documentation needs no entry here.
    possible_anchors = [
        expected_anchor,
        f"extra_platforms.{Path(source_file).stem}.{symbol_clean}",
    ]

    html_content = read_html(built_docs, expected_page)
    found = any(f'id="{anchor}"' in html_content for anchor in possible_anchors)

    if not found and symbol_clean.startswith(("_", "UNKNOWN_")):
        pytest.skip("Private and unknown-trait symbols carry no anchor of their own")
    assert found, (
        f"Symbol {role}:`{symbol}` from {source_file} "
        f"expected in {expected_page} but anchor {expected_anchor} not found"
    )


def extract_docstring_from_html(html: str, symbol_id: str) -> str:
    """Extract the docstring text for a symbol from HTML content.

    This function is used to verify that custom docstrings are properly rendered
    in the generated HTML documentation, particularly for frozenset collections
    where Sphinx's autodoc would normally show the generic frozenset description.

    :param html: The HTML content to search.
    :param symbol_id: The symbol ID (like ``"extra_platforms.ALL_GROUPS"``
        or ``"extra_platforms.group_data.ALL_GROUPS"``).
    :returns: The docstring text (stripped of HTML tags), or empty string if
        not found.
    """
    # Find the anchor for this symbol.
    pattern = rf'<dt[^>]*id="{re.escape(symbol_id)}"[^>]*>(.*?)</dt>\s*<dd>(.*?)</dd>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        return ""

    dd_content = match.group(2)

    # Extract text content, removing HTML tags.
    # First remove <script> and <style> tags entirely.
    dd_content = re.sub(r"<script[^>]*>.*?</script>", "", dd_content, flags=re.DOTALL)
    dd_content = re.sub(r"<style[^>]*>.*?</style>", "", dd_content, flags=re.DOTALL)

    # Remove HTML tags but preserve text content.
    text = re.sub(r"<[^>]+>", " ", dd_content)

    # Clean up whitespace.
    return re.sub(r"\s+", " ", text).strip()


@pytest.mark.parametrize(
    "symbol_name,expected_text_fragment",
    [
        ("ALL_ARCHITECTURE_GROUPS", "All groups whose members are Architecture"),
        ("ALL_PLATFORM_GROUPS", "All groups whose members are Platform"),
        ("ALL_CI_GROUPS", "All groups whose members are CI"),
        ("CANONICAL_GROUPS", "Canonical, non-overlapping groups"),
        (
            "NON_CANONICAL_GROUPS",
            "Non-canonical, overlapping groups, defined for convenience",
        ),
        ("ALL_GROUPS", "All predefined groups"),
        ("ALL_TRAIT_IDS", "frozenset of all recognized traits IDs"),
        ("ALL_GROUP_IDS", "frozenset of all recognized group IDs"),
        ("ALL_IDS", "frozenset of all recognized traits and group IDs"),
    ],
)
def test_frozenset_docstrings_are_custom(
    built_docs, symbol_name, expected_text_fragment
):
    """Test that frozenset collections have custom docstrings, not the generic one.

    This test verifies that the frozenset collections (ALL_GROUPS, ALL_TRAIT_IDS,
    etc.) are documented with their custom docstrings extracted from #: comments
    rather than the generic frozenset description.

    The canonical location for these symbols is ``groups.html``.
    """
    symbol_id = f"extra_platforms.group_data.{symbol_name}"

    groups_html = read_html(built_docs, "groups.html")
    docstring = extract_docstring_from_html(groups_html, symbol_id)

    # Verify we found a docstring.
    assert docstring, f"No docstring found for {symbol_name} in groups.html"

    # Verify it doesn't contain the generic frozenset description.
    assert (
        "Build an immutable unordered collection of unique elements" not in docstring
    ), f"{symbol_name} in groups.html has generic frozenset docstring"

    # Verify it contains the expected custom text.
    assert expected_text_fragment in docstring, (
        f"{symbol_name} in groups.html missing expected text: "
        f"'{expected_text_fragment}'. Got: {docstring[:200]}"
    )


#: Specialized documentation pages that should never leak links to the generic
#: auto-generated ``extra_platforms.html`` page.
SPECIALIZED_PAGES = (
    "agents.html",
    "architectures.html",
    "ci.html",
    "detection.html",
    "groups.html",
    "platforms.html",
    "pytest.html",
    "shells.html",
    "sphinx.html",
    "terminals.html",
    "trait.html",
)


@pytest.mark.parametrize("page", SPECIALIZED_PAGES)
def test_no_links_to_generic_api_page(built_docs, page):
    """Test that specialized doc pages never link to the generic extra_platforms.html.

    All cross-references from hand-written documentation pages should resolve to
    other specialized pages (e.g. ``architectures.html``, ``groups.html``,
    ``detection.html``), never to the catch-all ``extra_platforms.html`` produced
    by ``automodule``.
    """
    html = read_html(built_docs, page)

    # Find all internal links pointing to extra_platforms.html.
    pattern = r'href="(extra_platforms\.html#[^"]*)"'
    leaks = [
        href
        for href in re.findall(pattern, html)
        # Submodule references (e.g. :mod:`detection`) can only resolve to
        # extra_platforms.html because that is where automodule registers them.
        if "#module-" not in href
    ]

    assert not leaks, (
        f"{page} contains {len(leaks)} link(s) leaking to the generic "
        f"extra_platforms.html page:\n"
        + "\n".join(
            f"  - {href} ({count}x)"
            for href, count in sorted(
                {href: leaks.count(href) for href in set(leaks)}.items(),
                key=lambda item: -item[1],
            )
        )
    )


def test_generic_api_page_no_stolen_targets(built_docs):
    """Enforce the policy that extra_platforms.html does not steal targets from specialized pages.

    The ``extra_platforms.rst`` file uses ``:noindex:`` and ``:no-members:``
    on all submodule ``automodule`` directives to prevent members documented
    in specialized pages from appearing on the generic page. This test checks
    both anchors (``id=``) and rendered member signatures (``sig-name``) to
    catch leaks even when ``:noindex:`` suppresses the anchor.
    """
    html = read_html(built_docs, "extra_platforms.html")

    # Check 1: No anchored symbols that belong to specialized pages.
    all_anchors = re.findall(r'id="(extra_platforms\.[^"]+)"', html)

    stolen = []
    for anchor in all_anchors:
        # Skip module anchors (e.g. module-extra_platforms.detection).
        if anchor.startswith("module-"):
            continue

        # Determine the symbol and role from the anchor.
        symbol = anchor.removeprefix("extra_platforms.")

        # For submodule-qualified anchors (e.g. extra_platforms.group_data.X),
        # use the leaf name for the page lookup.
        symbol_clean = symbol.split(".")[-1]

        # Use existing logic to determine where this symbol should live.
        # Try common roles in priority order.
        for role in ("data", "func", "class", "deco"):
            expected_page = get_expected_page_for_symbol(role, symbol_clean)
            if expected_page != "extra_platforms.html":
                stolen.append((anchor, expected_page, role))
                break

    assert not stolen, (
        f"extra_platforms.html contains {len(stolen)} stolen target(s) that "
        f"belong to specialized pages:\n"
        + "\n".join(
            f"  - {anchor} → should be in {page} (role: {role})"
            for anchor, page, role in sorted(stolen)
        )
    )

    # Check 2: No rendered member signatures from submodule automodules.
    # With :noindex:, Sphinx omits the id= attribute but still renders
    # visible content. Detect leaked members by their sig-name spans.
    sig_pattern = (
        r'<span class="sig-prename descclassname">'
        r'<span class="pre">extra_platforms\.(\w+)\.</span></span>'
        r'<span class="sig-name descname">'
        r'<span class="pre">(\w+)</span></span>'
    )
    leaked = []
    for submodule, name in re.findall(sig_pattern, html):
        expected_page = get_expected_page_for_symbol("data", name)
        if expected_page != "extra_platforms.html":
            leaked.append((f"extra_platforms.{submodule}.{name}", expected_page))

    assert not leaked, (
        f"extra_platforms.html renders {len(leaked)} member(s) from submodule "
        f"automodules that belong to specialized pages:\n"
        + "\n".join(
            f"  - {symbol} → should be in {page}" for symbol, page in sorted(leaked)
        )
    )
