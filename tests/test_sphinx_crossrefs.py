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
# Foundation, Inc., 59 # Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Tests for Sphinx cross-reference rendering and link resolution."""

from __future__ import annotations

from textwrap import dedent

import pytest

# List of modules to create stubs for.
MODULES_TO_STUB = [
    "extra_platforms.architecture_data",
    "extra_platforms.ci_data",
    "extra_platforms.detection",
    "extra_platforms.group",
    "extra_platforms.group_data",
    "extra_platforms.operations",
    "extra_platforms.platform_data",
    "extra_platforms.trait",
]


@pytest.mark.parametrize(
    ("role", "expected_href", "expected_text"),
    [
        pytest.param(
            "{func}`~extra_platforms.current_traits`",
            "detection.html#extra_platforms.current_traits",
            "current_traits()",
            id="func_current_traits_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.current_architecture`",
            "detection.html#extra_platforms.current_architecture",
            "current_architecture()",
            id="func_current_architecture_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.current_platform`",
            "detection.html#extra_platforms.current_platform",
            "current_platform()",
            id="func_current_platform_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.current_ci`",
            "detection.html#extra_platforms.current_ci",
            "current_ci()",
            id="func_current_ci_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.is_aarch64`",
            "detection.html#extra_platforms.is_aarch64",
            "is_aarch64()",
            id="func_is_aarch64_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.is_linux`",
            "detection.html#extra_platforms.is_linux",
            "is_linux()",
            id="func_is_linux_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.is_macos`",
            "detection.html#extra_platforms.is_macos",
            "is_macos()",
            id="func_is_macos_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.is_windows`",
            "detection.html#extra_platforms.is_windows",
            "is_windows()",
            id="func_is_windows_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.invalidate_caches`",
            "detection.html#extra_platforms.invalidate_caches",
            "invalidate_caches()",
            id="func_invalidate_caches_in_detection",
        ),
        pytest.param(
            "{func}`~extra_platforms.reduce`",
            "operations.html#extra_platforms.reduce",
            "reduce()",
            id="func_reduce_in_operations",
        ),
        pytest.param(
            "{class}`~extra_platforms.Trait`",
            "trait.html#extra_platforms.Trait",
            "Trait",
            id="class_trait_in_trait",
        ),
        pytest.param(
            "{class}`~extra_platforms.Platform`",
            "trait.html#extra_platforms.Platform",
            "Platform",
            id="class_platform_in_trait",
        ),
        pytest.param(
            "{class}`~extra_platforms.Architecture`",
            "trait.html#extra_platforms.Architecture",
            "Architecture",
            id="class_architecture_in_trait",
        ),
        pytest.param(
            "{class}`~extra_platforms.CI`",
            "trait.html#extra_platforms.CI",
            "CI",
            id="class_ci_in_trait",
        ),
        pytest.param(
            "{class}`~extra_platforms.Group`",
            "group.html#extra_platforms.Group",
            "Group",
            id="class_group_in_group",
        ),
        pytest.param(
            "{data}`~extra_platforms.AARCH64`",
            "architecture_data.html#extra_platforms.AARCH64",
            "AARCH64",
            id="data_aarch64_in_architecture_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.X86_64`",
            "architecture_data.html#extra_platforms.X86_64",
            "X86_64",
            id="data_x86_64_in_architecture_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.MACOS`",
            "platform_data.html#extra_platforms.MACOS",
            "MACOS",
            id="data_macos_in_platform_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.UBUNTU`",
            "platform_data.html#extra_platforms.UBUNTU",
            "UBUNTU",
            id="data_ubuntu_in_platform_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.WINDOWS`",
            "platform_data.html#extra_platforms.WINDOWS",
            "WINDOWS",
            id="data_windows_in_platform_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.GITHUB_CI`",
            "ci_data.html#extra_platforms.GITHUB_CI",
            "GITHUB_CI",
            id="data_github_ci_in_ci_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.GITLAB_CI`",
            "ci_data.html#extra_platforms.GITLAB_CI",
            "GITLAB_CI",
            id="data_gitlab_ci_in_ci_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.ALL_PLATFORMS`",
            "group_data.html#extra_platforms.ALL_PLATFORMS",
            "ALL_PLATFORMS",
            id="data_all_platforms_in_group_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.LINUX`",
            "group_data.html#extra_platforms.LINUX",
            "LINUX",
            id="data_linux_in_group_data",
        ),
        pytest.param(
            "{data}`~extra_platforms.UNIX`",
            "group_data.html#extra_platforms.UNIX",
            "UNIX",
            id="data_unix_in_group_data",
        ),
    ],
)
def test_crossref_links_to_correct_page(sphinx_app, role, expected_href, expected_text):
    """Test that Sphinx cross-references link to the correct module page.

    This test ensures that symbols exposed in the root extra_platforms module
    link to their actual definition location, not to the root module page.
    For example, :func:`~extra_platforms.current_traits` should link to
    detection.html, not extra_platforms.html.
    """
    # Create module stubs for cross-referencing.
    sphinx_app.create_module_stubs(MODULES_TO_STUB)

    # Create a simple document with the cross-reference.
    content = dedent(f"""
        # Test Document

        Here is a reference: {role}
    """)

    html_output = sphinx_app.build_document(content)
    assert html_output is not None

    # Check that the link points to the correct page.
    assert f'href="{expected_href}"' in html_output

    # Check that the link text is as expected.
    assert f">{expected_text}<" in html_output


@pytest.mark.parametrize(
    ("content", "expected_fragments", "unexpected_fragments"),
    [
        pytest.param(
            dedent("""
                # Test Document

                The {func}`~extra_platforms.current_traits` function returns
                all traits detected for the current system.

                You can also check individual platforms using
                {func}`~extra_platforms.is_linux` or
                {func}`~extra_platforms.is_windows`.

                Platform constants like {data}`~extra_platforms.UBUNTU` and
                {data}`~extra_platforms.MACOS` are defined in the
                {mod}`extra_platforms.platform_data` module.
            """),
            [
                'href="detection.html#extra_platforms.current_traits"',
                'href="detection.html#extra_platforms.is_linux"',
                'href="detection.html#extra_platforms.is_windows"',
                'href="platform_data.html#extra_platforms.UBUNTU"',
                'href="platform_data.html#extra_platforms.MACOS"',
                'href="platform_data.html#module-extra_platforms.platform_data"',
            ],
            [
                # These should NOT appear (wrong module).
                'href="extra_platforms.html#extra_platforms.current_traits"',
                'href="extra_platforms.html#extra_platforms.is_linux"',
                'href="extra_platforms.html#extra_platforms.UBUNTU"',
            ],
            id="mixed_references_in_document",
        ),
        pytest.param(
            dedent("""
                # Architecture Detection

                Use {func}`~extra_platforms.current_architecture` to get the
                current architecture.

                The {class}`~extra_platforms.Architecture` class defines all
                architecture traits.

                Examples include {data}`~extra_platforms.X86_64` and
                {data}`~extra_platforms.AARCH64`.
            """),
            [
                'href="detection.html#extra_platforms.current_architecture"',
                'href="trait.html#extra_platforms.Architecture"',
                'href="architecture_data.html#extra_platforms.X86_64"',
                'href="architecture_data.html#extra_platforms.AARCH64"',
            ],
            [
                'href="extra_platforms.html#extra_platforms.current_architecture"',
                'href="extra_platforms.html#extra_platforms.X86_64"',
            ],
            id="architecture_references",
        ),
        pytest.param(
            dedent("""
                # CI Detection

                Check the current CI system with
                {func}`~extra_platforms.current_ci`.

                CI constants like {data}`~extra_platforms.GITHUB_CI` and
                {data}`~extra_platforms.GITLAB_CI` are available.

                The {class}`~extra_platforms.CI` class represents CI systems.
            """),
            [
                'href="detection.html#extra_platforms.current_ci"',
                'href="ci_data.html#extra_platforms.GITHUB_CI"',
                'href="ci_data.html#extra_platforms.GITLAB_CI"',
                'href="trait.html#extra_platforms.CI"',
            ],
            [
                'href="extra_platforms.html#extra_platforms.current_ci"',
                'href="extra_platforms.html#extra_platforms.GITHUB_CI"',
            ],
            id="ci_references",
        ),
        pytest.param(
            dedent("""
                # Groups

                The {data}`~extra_platforms.LINUX` group contains all Linux
                distributions.

                The {data}`~extra_platforms.UNIX` group is broader.

                Use {class}`~extra_platforms.Group` to create custom groups.

                Reduce platform lists with {func}`~extra_platforms.reduce`.
            """),
            [
                'href="group_data.html#extra_platforms.LINUX"',
                'href="group_data.html#extra_platforms.UNIX"',
                'href="group.html#extra_platforms.Group"',
                'href="operations.html#extra_platforms.reduce"',
            ],
            [
                'href="extra_platforms.html#extra_platforms.LINUX"',
                'href="extra_platforms.html#extra_platforms.reduce"',
            ],
            id="group_references",
        ),
    ],
)
def test_complex_document_crossrefs(
    sphinx_app, content, expected_fragments, unexpected_fragments
):
    """Test that complex documents with multiple cross-references work correctly.

    This ensures that when multiple types of cross-references are used together,
    they all resolve to the correct module pages.
    """
    # Create module stubs for cross-referencing.
    sphinx_app.create_module_stubs(MODULES_TO_STUB)

    html_output = sphinx_app.build_document(content)
    assert html_output is not None

    # Check that all expected fragments are present.
    for fragment in expected_fragments:
        assert fragment in html_output, f"Expected fragment not found: {fragment}"

    # Check that unexpected fragments are NOT present.
    for fragment in unexpected_fragments:
        assert fragment not in html_output, f"Unexpected fragment found: {fragment}"


def test_all_role_types_render_correctly(sphinx_app):
    """Test that all role types (func, class, data, mod) render correctly."""
    # Create module stubs for cross-referencing.
    sphinx_app.create_module_stubs(MODULES_TO_STUB)

    content = dedent("""
        # All Role Types

        - Function: {func}`~extra_platforms.is_linux`
        - Class: {class}`~extra_platforms.Platform`
        - Data: {data}`~extra_platforms.UBUNTU`
        - Module: {mod}`extra_platforms.detection`
    """)

    html_output = sphinx_app.build_document(content)
    assert html_output is not None

    # Check function reference.
    assert 'href="detection.html#extra_platforms.is_linux"' in html_output
    assert ">is_linux()<" in html_output

    # Check class reference (Platform is documented in trait.html).
    assert 'href="trait.html#extra_platforms.Platform"' in html_output
    assert ">Platform<" in html_output

    # Check data reference.
    assert 'href="platform_data.html#extra_platforms.UBUNTU"' in html_output
    assert ">UBUNTU<" in html_output

    # Check module reference.
    assert 'href="detection.html#module-extra_platforms.detection"' in html_output
