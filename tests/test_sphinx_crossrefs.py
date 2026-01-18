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

import re
import subprocess
from pathlib import Path

import pytest

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


def test_group_symbols_are_linked(built_docs):
    """Test that group symbols in the table link to their definitions."""
    html = read_html(built_docs, "groups.html")

    # Test a sample of group symbols.
    groups_to_check = [
        ("ALL_ARCHITECTURES", "#extra_platforms.ALL_ARCHITECTURES"),
        ("ALL_PLATFORMS", "#extra_platforms.ALL_PLATFORMS"),
        ("LINUX", "#extra_platforms.LINUX"),
        ("BSD", "#extra_platforms.BSD"),
        ("UNIX", "#extra_platforms.UNIX"),
    ]

    for symbol, href_fragment in groups_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Group symbol {symbol} is not linked to {href_fragment}"
        )


def test_group_detection_functions_are_linked(built_docs):
    """Test that detection functions in the table link to detection.html."""
    html = read_html(built_docs, "groups.html")

    # Test a sample of detection functions.
    functions_to_check = [
        ("is_any_architecture()", "detection.html#extra_platforms.is_any_architecture"),
        ("is_any_platform()", "detection.html#extra_platforms.is_any_platform"),
        ("is_linux()", "detection.html#extra_platforms.is_linux"),
        ("is_bsd()", "detection.html#extra_platforms.is_bsd"),
        ("is_unix()", "detection.html#extra_platforms.is_unix"),
    ]

    for func_text, href_fragment in functions_to_check:
        assert has_linked_reference(html, func_text, href_fragment), (
            f"Detection function {func_text} is not linked to {href_fragment}"
        )


def test_pytest_decorator_table_symbols_are_linked(built_docs):
    """Test that symbols in the decorator table link to their definitions."""
    html = read_html(built_docs, "pytest.html")

    # Test a sample of symbols in the decorator table.
    symbols_to_check = [
        ("AARCH64", "architectures.html#extra_platforms.AARCH64"),
        ("UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        ("LINUX", "groups.html#extra_platforms.LINUX"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Symbol {symbol} is not linked to {href_fragment}"
        )


def test_pytest_decorator_docstrings_have_linked_symbols(built_docs):
    """Test that decorator docstrings contain linked symbols."""
    html = read_html(built_docs, "pytest.html")

    # The docstrings should contain links like:
    # "Skip test if current environment is AARCH64 (i.e., when is_aarch64() ...)"
    # Both AARCH64 and is_aarch64() should be linked.

    # Check that AARCH64 in the skip_aarch64 docstring is linked.
    assert has_linked_reference(
        html, "AARCH64", "architectures.html#extra_platforms.AARCH64"
    ), "AARCH64 in skip_aarch64 docstring is not linked"

    # Check that is_aarch64() in the docstring is linked.
    assert has_linked_reference(
        html, "is_aarch64()", "detection.html#extra_platforms.is_aarch64"
    ), "is_aarch64() in skip_aarch64 docstring is not linked"


def test_detection_table_symbols_are_linked(built_docs):
    """Test that symbols in the detection table link to their definitions."""
    html = read_html(built_docs, "detection.html")

    # Test a sample of symbols.
    symbols_to_check = [
        ("AARCH64", "architectures.html#extra_platforms.AARCH64"),
        ("UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
        ("LINUX", "groups.html#extra_platforms.LINUX"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Symbol {symbol} is not linked to {href_fragment}"
        )


def test_trait_table_symbols_are_linked(built_docs):
    """Test that trait symbols in the table link to their definitions."""
    html = read_html(built_docs, "trait.html")

    # Test a sample of trait symbols linking to their data pages.
    symbols_to_check = [
        ("AARCH64", "architectures.html#extra_platforms.AARCH64"),
        ("UBUNTU", "platforms.html#extra_platforms.UBUNTU"),
        ("GITHUB_CI", "ci.html#extra_platforms.GITHUB_CI"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Trait symbol {symbol} is not linked to {href_fragment}"
        )


def test_trait_table_detection_functions_are_linked(built_docs):
    """Test that detection functions in the trait table link to detection.html."""
    html = read_html(built_docs, "trait.html")

    functions_to_check = [
        ("is_aarch64()", "detection.html#extra_platforms.is_aarch64"),
        ("is_ubuntu()", "detection.html#extra_platforms.is_ubuntu"),
        ("is_github_ci()", "detection.html#extra_platforms.is_github_ci"),
    ]

    for func_text, href_fragment in functions_to_check:
        assert has_linked_reference(html, func_text, href_fragment), (
            f"Detection function {func_text} is not linked to {href_fragment}"
        )


def test_platform_symbols_are_linked(built_docs):
    """Test that platform symbols link to their definitions."""
    html = read_html(built_docs, "platforms.html")

    symbols_to_check = [
        ("UBUNTU", "#extra_platforms.UBUNTU"),
        ("MACOS", "#extra_platforms.MACOS"),
        ("WINDOWS", "#extra_platforms.WINDOWS"),
        ("DEBIAN", "#extra_platforms.DEBIAN"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Platform symbol {symbol} is not linked to {href_fragment}"
        )


def test_platform_detection_functions_are_linked(built_docs):
    """Test that platform detection functions link to detection.html."""
    html = read_html(built_docs, "platforms.html")

    functions_to_check = [
        ("is_ubuntu()", "detection.html#extra_platforms.is_ubuntu"),
        ("is_macos()", "detection.html#extra_platforms.is_macos"),
        ("is_windows()", "detection.html#extra_platforms.is_windows"),
    ]

    for func_text, href_fragment in functions_to_check:
        assert has_linked_reference(html, func_text, href_fragment), (
            f"Detection function {func_text} is not linked to {href_fragment}"
        )


def test_architecture_symbols_are_linked(built_docs):
    """Test that architecture symbols link to their definitions."""
    html = read_html(built_docs, "architectures.html")

    symbols_to_check = [
        ("AARCH64", "#extra_platforms.AARCH64"),
        ("X86_64", "#extra_platforms.X86_64"),
        ("ARM", "#extra_platforms.ARM"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"Architecture symbol {symbol} is not linked to {href_fragment}"
        )


def test_ci_symbols_are_linked(built_docs):
    """Test that CI symbols link to their definitions."""
    html = read_html(built_docs, "ci.html")

    symbols_to_check = [
        ("GITHUB_CI", "#extra_platforms.GITHUB_CI"),
        ("GITLAB_CI", "#extra_platforms.GITLAB_CI"),
        ("TRAVIS_CI", "#extra_platforms.TRAVIS_CI"),
    ]

    for symbol, href_fragment in symbols_to_check:
        assert has_linked_reference(html, symbol, href_fragment), (
            f"CI symbol {symbol} is not linked to {href_fragment}"
        )


def test_group_data_references_from_other_pages(built_docs):
    """Test that references to groups from other pages link to groups.html."""
    # Check platforms.html links to groups.
    platforms_html = read_html(built_docs, "platforms.html")
    assert has_linked_reference(
        platforms_html, "LINUX", "groups.html#extra_platforms.LINUX"
    ), "LINUX group reference in platforms.html is not linked to groups.html"


def test_detection_references_from_trait_pages(built_docs):
    """Test that detection function refs from trait pages link to detection.html."""
    architectures_html = read_html(built_docs, "architectures.html")
    assert has_linked_reference(
        architectures_html,
        "is_aarch64()",
        "detection.html#extra_platforms.is_aarch64",
    ), "is_aarch64() reference in architectures.html is not linked to detection.html"


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
        ("{class}`~CI`", "CI", "trait.html#extra_platforms.CI"),
        ("{class}`~Group`", "Group", "extra_platforms.html#extra_platforms.Group"),
        # Utilities
        ("{func}`~reduce`", "reduce()", "extra_platforms.html#extra_platforms.reduce"),
        (
            "{func}`~invalidate_caches`",
            "invalidate_caches()",
            "extra_platforms.html#extra_platforms.invalidate_caches",
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
