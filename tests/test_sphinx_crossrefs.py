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


def test_detection_table_functions_are_linked(built_docs):
    """Test that detection functions in the table link correctly."""
    html = read_html(built_docs, "detection.html")

    # Test a sample of detection functions (they should link to themselves).
    functions_to_check = [
        ("is_aarch64()", "#extra_platforms.is_aarch64"),
        ("is_ubuntu()", "#extra_platforms.is_ubuntu"),
        ("is_github_ci()", "#extra_platforms.is_github_ci"),
        ("is_linux()", "#extra_platforms.is_linux"),
    ]

    for func_text, href_fragment in functions_to_check:
        assert has_linked_reference(html, func_text, href_fragment), (
            f"Detection function {func_text} is not linked to {href_fragment}"
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
