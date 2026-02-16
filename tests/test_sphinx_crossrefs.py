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
"""Tests for Sphinx cross-reference rendering in the real documentation.

These tests verify that cross-references in the built documentation (./docs/html/)
resolve to actual links with correct href attributes. Unlike mock-based tests,
these catch real regressions in the actual documentation.
"""

from __future__ import annotations

import inspect
import re
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_TRAITS,
    CI,
    Architecture,
    Group,
    Platform,
    Shell,
    Trait,
)

# Path to the built documentation.
DOCS_HTML_DIR = Path(__file__).parent.parent / "docs" / "html"


@pytest.fixture(scope="module")
def built_docs() -> Path:
    """Ensure the documentation is built and return the path to the HTML directory.

    This fixture builds the documentation if it doesn't exist or is outdated.
    """
    if not DOCS_HTML_DIR.exists():
        # Build the documentation.
        subprocess.run(
            ["uv", "run", "sphinx-build", "-b", "html", "./docs", "./docs/html"],
            check=True,
            cwd=Path(__file__).parent.parent,
        )
    return DOCS_HTML_DIR


def read_html(built_docs: Path, filename: str) -> str:
    """Read an HTML file from the built documentation."""
    html_path = built_docs / filename
    assert html_path.exists(), f"HTML file not found: {html_path}"
    return html_path.read_text(encoding="utf-8")


def find_links_with_text(html: str, link_text: str) -> list[str]:
    """Find all href values for links containing the given text.

    Returns a list of href values for <a> tags that contain the specified text.
    The function handles nested tags like <a href="..."><code><span>text</span></code></a>.
    """
    results = []
    # Pattern to match <a ...href="..."...>...</a> including nested tags.
    pattern = r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    for match in re.finditer(pattern, html, re.DOTALL):
        href, content = match.groups()
        # Strip HTML tags from content to get plain text.
        plain_text = re.sub(r"<[^>]+>", "", content)
        if link_text in plain_text:
            results.append(href)
    return results


def has_linked_reference(html: str, text: str, expected_href_fragment: str) -> bool:
    """Check if the HTML contains a link with the given text pointing to the expected href.

    Args:
        html: The HTML content to search.
        text: The link text to find (e.g., "AARCH64", "is_linux()").
        expected_href_fragment: A fragment that should be in the href (e.g.,
            "architectures.html#extra_platforms.AARCH64").

    Returns:
        True if a matching link is found.
    """
    hrefs = find_links_with_text(html, text)
    return any(expected_href_fragment in href for href in hrefs)


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
        ("pytest.html", "AARCH64", "architectures.html#extra_platforms.AARCH64"),
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


def _extract_reference_table_rows(html: str, myst: str) -> tuple[str, str]:
    """Return the (first_column_html, rendering_column_html) tuple for `myst`.

    Search the Reference matrix table and return the first row whose first
    column (stripped of HTML) exactly matches the provided `myst` directive
    string (e.g. "{data}`~UBUNTU`"). The returned values are the raw HTML
    contents of the first and second <td> cells for that row. If not found,
    fail the test.
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
        if len(tds) < 2:
            continue
        first = re.sub(r"<[^>]+>", "", tds[0]).strip()
        if first == myst:
            return tds[0], tds[1]

    pytest.fail(f"Reference matrix first-column entry not found: {myst}")


@pytest.mark.parametrize(
    "myst,expected_text,expected_link",
    [
        # Traits
        ("{data}`~UBUNTU`", "UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        (
            "{func}`~is_ubuntu`",
            "is_ubuntu()",
            "detection.html#extra_platforms.is_ubuntu",
        ),
        (
            "{data}`~pytest.skip_ubuntu`",
            "skip_ubuntu",
            "pytest.html#extra_platforms.pytest.skip_ubuntu",
        ),
        (
            "{data}`~pytest.unless_ubuntu`",
            "unless_ubuntu",
            "pytest.html#extra_platforms.pytest.unless_ubuntu",
        ),
        # Architectures
        ("{data}`~AARCH64`", "AARCH64", "architectures.html#extra_platforms.AARCH64"),
        (
            "{func}`~is_aarch64`",
            "is_aarch64()",
            "detection.html#extra_platforms.is_aarch64",
        ),
        (
            "{data}`~pytest.skip_aarch64`",
            "skip_aarch64",
            "pytest.html#extra_platforms.pytest.skip_aarch64",
        ),
        (
            "{data}`~pytest.unless_aarch64`",
            "unless_aarch64",
            "pytest.html#extra_platforms.pytest.unless_aarch64",
        ),
        # Shells
        ("{data}`~BASH`", "BASH", "shells.html#extra_platforms.BASH"),
        ("{func}`~is_bash`", "is_bash()", "detection.html#extra_platforms.is_bash"),
        (
            "{data}`~pytest.skip_bash`",
            "skip_bash",
            "pytest.html#extra_platforms.pytest.skip_bash",
        ),
        (
            "{data}`~pytest.unless_bash`",
            "unless_bash",
            "pytest.html#extra_platforms.pytest.unless_bash",
        ),
        # CI
        ("{data}`~GITHUB_CI`", "GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        (
            "{func}`~is_github_ci`",
            "is_github_ci()",
            "detection.html#extra_platforms.is_github_ci",
        ),
        (
            "{data}`~pytest.skip_github_ci`",
            "skip_github_ci",
            "pytest.html#extra_platforms.pytest.skip_github_ci",
        ),
        (
            "{data}`~pytest.unless_github_ci`",
            "unless_github_ci",
            "pytest.html#extra_platforms.pytest.unless_github_ci",
        ),
        # Groups
        ("{data}`~LINUX`", "LINUX", "groups.html#extra_platforms.LINUX"),
        ("{func}`~is_linux`", "is_linux()", "detection.html#extra_platforms.is_linux"),
        (
            "{data}`~pytest.skip_linux`",
            "skip_linux",
            "pytest.html#extra_platforms.pytest.skip_linux",
        ),
        (
            "{data}`~pytest.unless_linux`",
            "unless_linux",
            "pytest.html#extra_platforms.pytest.unless_linux",
        ),
        (
            "{data}`~ALL_PLATFORMS`",
            "ALL_PLATFORMS",
            "groups.html#extra_platforms.ALL_PLATFORMS",
        ),
        (
            "{func}`~is_any_platform`",
            "is_any_platform()",
            "detection.html#extra_platforms.is_any_platform",
        ),
        (
            "{data}`~pytest.skip_all_platforms`",
            "skip_all_platforms",
            "pytest.html#extra_platforms.pytest.skip_all_platforms",
        ),
        (
            "{data}`~pytest.unless_any_platform`",
            "unless_any_platform",
            "pytest.html#extra_platforms.pytest.unless_any_platform",
        ),
        (
            "{data}`~UNKNOWN_PLATFORM`",
            "UNKNOWN_PLATFORM",
            "platforms.html#extra_platforms.UNKNOWN_PLATFORM",
        ),
        (
            "{func}`~is_unknown_platform`",
            "is_unknown_platform()",
            "detection.html#extra_platforms.is_unknown_platform",
        ),
        (
            "{data}`~pytest.skip_unknown_platform`",
            "skip_unknown_platform",
            "pytest.html#extra_platforms.pytest.skip_unknown_platform",
        ),
        (
            "{data}`~pytest.unless_unknown_platform`",
            "unless_unknown_platform",
            "pytest.html#extra_platforms.pytest.unless_unknown_platform",
        ),
        (
            "{data}`~ALL_SHELLS`",
            "ALL_SHELLS",
            "groups.html#extra_platforms.ALL_SHELLS",
        ),
        (
            "{func}`~is_any_shell`",
            "is_any_shell()",
            "detection.html#extra_platforms.is_any_shell",
        ),
        (
            "{data}`~pytest.skip_all_shells`",
            "skip_all_shells",
            "pytest.html#extra_platforms.pytest.skip_all_shells",
        ),
        (
            "{data}`~pytest.unless_any_shell`",
            "unless_any_shell",
            "pytest.html#extra_platforms.pytest.unless_any_shell",
        ),
        (
            "{data}`~UNKNOWN_SHELL`",
            "UNKNOWN_SHELL",
            "shells.html#extra_platforms.UNKNOWN_SHELL",
        ),
        (
            "{func}`~is_unknown_shell`",
            "is_unknown_shell()",
            "detection.html#extra_platforms.is_unknown_shell",
        ),
        (
            "{data}`~pytest.skip_unknown_shell`",
            "skip_unknown_shell",
            "pytest.html#extra_platforms.pytest.skip_unknown_shell",
        ),
        (
            "{data}`~pytest.unless_unknown_shell`",
            "unless_unknown_shell",
            "pytest.html#extra_platforms.pytest.unless_unknown_shell",
        ),
        (
            "{data}`~UNKNOWN_ARCHITECTURE`",
            "UNKNOWN_ARCHITECTURE",
            "architectures.html#extra_platforms.UNKNOWN_ARCHITECTURE",
        ),
        (
            "{func}`~is_unknown_architecture`",
            "is_unknown_architecture()",
            "detection.html#extra_platforms.is_unknown_architecture",
        ),
        (
            "{data}`~pytest.skip_unknown_architecture`",
            "skip_unknown_architecture",
            "pytest.html#extra_platforms.pytest.skip_unknown_architecture",
        ),
        (
            "{data}`~pytest.unless_unknown_architecture`",
            "unless_unknown_architecture",
            "pytest.html#extra_platforms.pytest.unless_unknown_architecture",
        ),
        ("{data}`~UNKNOWN_CI`", "UNKNOWN_CI", "ci.html#extra_platforms.UNKNOWN_CI"),
        (
            "{func}`~is_unknown_ci`",
            "is_unknown_ci()",
            "detection.html#extra_platforms.is_unknown_ci",
        ),
        (
            "{data}`~pytest.skip_unknown_ci`",
            "skip_unknown_ci",
            "pytest.html#extra_platforms.pytest.skip_unknown_ci",
        ),
        (
            "{data}`~pytest.unless_unknown_ci`",
            "unless_unknown_ci",
            "pytest.html#extra_platforms.pytest.unless_unknown_ci",
        ),
        # UNIX_WITHOUT_MACOS / translation example
        (
            "{data}`~UNIX_WITHOUT_MACOS`",
            "UNIX_WITHOUT_MACOS",
            "groups.html#extra_platforms.UNIX_WITHOUT_MACOS",
        ),
        (
            "{func}`~is_unix_not_macos`",
            "is_unix_not_macos()",
            "detection.html#extra_platforms.is_unix_not_macos",
        ),
        # Detection Methods
        (
            "{func}`~current_platform`",
            "current_platform()",
            "detection.html#extra_platforms.current_platform",
        ),
        (
            "{func}`~current_architecture`",
            "current_architecture()",
            "detection.html#extra_platforms.current_architecture",
        ),
        (
            "{func}`~current_shell`",
            "current_shell()",
            "detection.html#extra_platforms.current_shell",
        ),
        (
            "{func}`~current_ci`",
            "current_ci()",
            "detection.html#extra_platforms.current_ci",
        ),
        (
            "{func}`~current_traits`",
            "current_traits()",
            "detection.html#extra_platforms.current_traits",
        ),
        # Classes
        ("{class}`~Platform`", "Platform", "trait.html#extra_platforms.Platform"),
        (
            "{class}`~Architecture`",
            "Architecture",
            "trait.html#extra_platforms.Architecture",
        ),
        ("{class}`~Shell`", "Shell", "trait.html#extra_platforms.Shell"),
        ("{class}`~CI`", "CI", "trait.html#extra_platforms.CI"),
        ("{class}`~Group`", "Group", "groups.html#extra_platforms.Group"),
        # Utilities
        ("{func}`~reduce`", "reduce()", "groups.html#extra_platforms.reduce"),
        (
            "{func}`~invalidate_caches`",
            "invalidate_caches()",
            "detection.html#extra_platforms.invalidate_caches",
        ),
    ],
)
def test_reference_matrix_links(built_docs, myst, expected_text, expected_link):
    """Parametrized check: the MyST directive in column 1 renders to a link in column 2.

    - `myst` is the literal MyST role example as shown in the first column of the
      Reference matrix (e.g. "{data}`~UBUNTU`").
    - `expected_link` is the expected href target used in the rendered
      second column (e.g. "platforms.html#extra_platforms.UBUNTU").
    """
    html = read_html(built_docs, "sphinx.html")
    first_html, rendering_html = _extract_reference_table_rows(html, myst)

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

    # Ensure the rendering column is wrapped in <span class="pre">...
    m2 = re.search(r'<span class="pre">(.*?)</span>', rendering_html, re.DOTALL)
    assert m2, (
        f"Reference matrix rendering column for '{myst}' is not wrapped in "
        '<span class="pre">..."'
    )
    # span exists (m2.group(1) available if needed for future checks)

    # Find the <a> tag that points to the expected href and check its text.
    # The anchor may or may not be inside the <span class="pre">; search
    # the entire rendering_html for robustness while still asserting the
    # presence of the <span class="pre"> wrapper above.
    pattern = r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    for m in re.finditer(pattern, rendering_html, re.DOTALL):
        href, content = m.groups()
        if expected_link in href:
            plain_text = re.sub(r"<[^>]+>", "", content).strip()
            assert plain_text == expected_text, (
                f"Reference matrix example '{myst}' rendered text '{plain_text}' "
                f"does not match expected '{expected_text}' for "
                f"{expected_link}"
            )
            break
    else:
        hrefs = re.findall(r'href="([^"]+)"', rendering_html)
        pytest.fail(
            f"Reference matrix example '{myst}' did not render to "
            f"{expected_link}; found {hrefs}"
        )


def get_expected_page_for_symbol(role: str, symbol: str) -> str:
    """Determine the expected HTML page for a given symbol.

    Args:
        role: The Sphinx role (func, data, class, etc.)
        symbol: The symbol name (e.g., 'UBUNTU', 'is_linux', 'Platform')

    Returns:
        The expected HTML filename (e.g., 'platforms.html')
    """
    # Clean symbol name (remove module prefix if present)
    symbol_clean = symbol.split(".")[-1]

    # Detection functions always go to detection.html
    if role == "func" and (
        symbol_clean.startswith("is_") or symbol_clean.startswith("current_")
    ):
        return "detection.html"

    # Cache management functions go to detection.html
    if role == "func" and symbol_clean == "invalidate_caches":
        return "detection.html"

    # Deprecated detection functions stay in detection.html
    if role == "func" and symbol_clean in (
        "current_os",  # Deprecated alias
        "current_platforms",  # Deprecated alias
    ):
        return "detection.html"

    # Trait and group operations functions go to groups.html
    if role == "func" and symbol_clean in (
        "extract_members",
        "groups_from_ids",
        "traits_from_ids",
        "reduce",
        "platforms_from_ids",  # Deprecated alias
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
    )
    if role in ("meth", "attr") and any(symbol.startswith(c) for c in trait_classes):
        return "trait.html"

    # Pytest decorators go to pytest.html
    if (
        "pytest" in symbol
        or symbol_clean.startswith("skip_")
        or symbol_clean.startswith("unless_")
    ):
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
            "EXTRA_GROUPS",
            "NON_OVERLAPPING_GROUPS",
        ):
            return "groups.html"

        # ID collections go to groups.html
        if symbol_clean in (
            "ALL_GROUP_IDS",
            "ALL_TRAIT_IDS",
            "ALL_IDS",
            "ALL_PLATFORM_IDS",  # Deprecated alias for ALL_TRAIT_IDS
        ):
            return "groups.html"

        # Deprecated group aliases go to groups.html
        if symbol_clean in (
            "ALL_PLATFORMS_WITHOUT_CI",
            "ANY_ARM",
            "ANY_MIPS",
            "ANY_SPARC",
            "ANY_WINDOWS",
            "OTHER_UNIX",
        ):
            return "groups.html"

        # Deprecated platform aliases go to platforms.html
        if symbol_clean in ("UNKNOWN_LINUX",):
            return "platforms.html"

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


def _get_all_public_symbols() -> Iterator[str]:
    """Collect all public symbols from extra_platforms and pytest modules.

    Returns a list of (symbol_name, is_pytest_decorator) tuples for parametrization.
    """

    # Add all symbols exposed in extra_platforms root.
    for symbol_name in extra_platforms.__all__:
        yield symbol_name

    # Add all symbols exposed in extra_platforms.pytest.
    for symbol_name in dir(extra_platforms.pytest):  # type: ignore[attr-defined]
        if not symbol_name.startswith("_"):
            yield f"pytest.{symbol_name}"


@pytest.mark.parametrize("symbol_name", _get_all_public_symbols())
def test_get_expected_page_for_symbol_handles_public_api(symbol_name):
    """Test that get_expected_page_for_symbol correctly handles each public symbol.

    This test validates that our logic correctly maps every symbol exposed in the
    public API from both extra_platforms and extra_platforms.pytest modules to the
    correct documentation page.

    Args:
        symbol_name: The symbol name (e.g., "UBUNTU", "is_linux", "pytest.skip_ubuntu")
        is_pytest_decorator: True if this is a pytest decorator, False otherwise
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
        elif isinstance(obj, (Trait, Architecture, Platform, Shell, CI, Group)):
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
    parametrization values for the comprehensive cross-reference test.
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

    rst_pattern = r":(\w+):`~?([^`]+)`"
    for py_file in code_dir.glob("**/*.py"):
        content = py_file.read_text(encoding="utf-8")
        for role, symbol in re.findall(rst_pattern, content):
            all_refs.append((role, symbol, str(py_file.relative_to(project_root))))

    return all_refs


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
        "ValueError",
        "TypeError",
        "AttributeError",
        "RuntimeError",
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
    if (
        symbol in python_builtins
        or symbol.split(".")[-1] in python_builtins
        or (role == "meth" and symbol in python_builtin_methods)
    ):
        pytest.skip("Skipping builtin symbol")

    if symbol.startswith((
        "pytest.",
        "typing.",
        "collections.",
        "types.",
        "dict.",
        "frozenset.",
    )):
        if not symbol.startswith("pytest.skip_") and not symbol.startswith(
            "pytest.unless_"
        ):
            pytest.skip("External symbol reference")

    if symbol_clean := symbol.split(".")[-1]:
        if symbol_clean.startswith("ALL_") and symbol_clean.endswith(("_IDS", "_ID")):
            pytest.skip("Module-level ID collection")

    expected_page = get_expected_page_for_symbol(role, symbol)

    symbol_clean = symbol.split(".")[-1]
    if symbol.startswith("pytest.") or symbol.startswith("extra_platforms.pytest."):
        if symbol.startswith("extra_platforms."):
            expected_anchor = symbol
        else:
            expected_anchor = f"extra_platforms.{symbol}"
    elif role == "meth" and "." in symbol:
        # Method references like Group.union have anchors like
        # extra_platforms.Group.union.
        expected_anchor = f"extra_platforms.{symbol}"
    else:
        expected_anchor = f"extra_platforms.{symbol_clean}"

    # Symbols documented via automodule may have module-qualified anchors
    # (e.g. ``extra_platforms.group_data.ALL_GROUPS`` instead of
    # ``extra_platforms.ALL_GROUPS``).
    possible_anchors = [expected_anchor]
    if "group_data" in source_file:
        possible_anchors.append(f"extra_platforms.group_data.{symbol_clean}")

    found = False
    for html_file in built_docs.glob("**/*.html"):
        if html_file.name != expected_page:
            continue
        html_content = html_file.read_text(encoding="utf-8")
        if any(f'id="{anchor}"' in html_content for anchor in possible_anchors):
            found = True
            break

    if not found:
        if (
            not symbol_clean.startswith("_")
            and "test" not in source_file.lower()
            and not symbol_clean.startswith("UNKNOWN_")
        ):
            assert found, (
                f"Symbol {role}:`{symbol}` from {source_file} "
                f"expected in {expected_page} but anchor {expected_anchor} not found"
            )


def extract_docstring_from_html(html: str, symbol_id: str) -> str:
    """Extract the docstring text for a symbol from HTML content.

    This function is used to verify that custom docstrings are properly rendered
    in the generated HTML documentation, particularly for frozenset collections
    where Sphinx's autodoc would normally show the generic frozenset description.

    Args:
        html: The HTML content to search.
        symbol_id: The symbol ID (e.g., "extra_platforms.ALL_GROUPS" or
            "extra_platforms.group_data.ALL_GROUPS").

    Returns:
        The docstring text (stripped of HTML tags), or empty string if not found.
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
    text = re.sub(r"\s+", " ", text).strip()

    return text


@pytest.mark.parametrize(
    "symbol_name,expected_text_fragment",
    [
        ("ALL_ARCHITECTURE_GROUPS", "All groups whose members are Architecture"),
        ("ALL_PLATFORM_GROUPS", "All groups whose members are Platform"),
        ("ALL_CI_GROUPS", "All groups whose members are CI"),
        ("NON_OVERLAPPING_GROUPS", "Non-overlapping groups"),
        ("EXTRA_GROUPS", "Overlapping groups, defined for convenience"),
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
    "architectures.html",
    "ci.html",
    "detection.html",
    "groups.html",
    "platforms.html",
    "pytest.html",
    "shells.html",
    "sphinx.html",
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
