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
"""Fixtures, configuration and helpers for tests."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace


class SphinxAppWrapper:
    """Wrapper around Sphinx application with additional testing methods."""

    def __init__(self, app: Sphinx):
        self.app = app

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped Sphinx app."""
        return getattr(self.app, name)

    @classmethod
    def create(
        cls, tmp_path: Path
    ) -> Generator[SphinxAppWrapper, None, None]:
        """Factory method to create a SphinxAppWrapper for testing."""
        srcdir = tmp_path / "source"
        outdir = tmp_path / "build"
        doctreedir = outdir / ".doctrees"
        confdir = srcdir

        srcdir.mkdir()
        outdir.mkdir()

        # Sphinx's configuration is Python code.
        # Include sys.path modification to ensure extra_platforms is importable.
        conf = {
            "master_doc": "index",
            "extensions": [
                "sphinx.ext.autodoc",
                "sphinx.ext.intersphinx",
                "sphinx.ext.viewcode",
                "myst_parser",
            ],
            "myst_enable_extensions": ["colon_fence"],
            # Autodoc configuration.
            "autodoc_member_order": "bysource",
        }

        # Write the conf.py file.
        config_lines = [
            "import sys",
            "from pathlib import Path",
            "",
            "# Add parent directory to sys.path for imports.",
            "sys.path.insert(0, str(Path(__file__).parent.parent.parent))",
            "",
        ]
        config_lines.extend(
            f"{key} = {repr(value)}" for key, value in conf.items()
        )
        config_content = "\n".join(config_lines)
        (srcdir / "conf.py").write_text(config_content)

        with docutils_namespace():
            app = Sphinx(
                str(srcdir),
                str(confdir),
                str(outdir),
                str(doctreedir),
                "html",
                verbosity=0,
                warning=None,
            )
            wrapper = cls(app)
            yield wrapper

    def create_module_stubs(self, modules: list[str], include_root: bool = True) -> None:
        """Create stub RST files for modules to enable cross-referencing.

        Args:
            modules: List of module names (e.g., ['extra_platforms.detection']).
            include_root: Whether to include the root extra_platforms module stub.
        """
        srcdir = Path(self.app.srcdir)

        # Create the root module stub if requested.
        if include_root:
            root_rst = srcdir / "extra_platforms.rst"
            # Exclude members so they're indexed in their canonical module pages.
            # This matches the exclusion list in docs/extra_platforms.rst.
            excluded_members = (
                "Architecture, CI, Platform, Trait, Group, "
                "current_architecture, current_ci, current_platform, current_traits, "
                "is_aarch64, is_aix, is_altlinux, is_amzn, is_android, "
                "is_any_architecture, is_any_arm, is_any_ci, is_any_mips, "
                "is_any_platform, is_any_sparc, is_any_trait, is_any_windows, "
                "is_arch, is_arch_32_bit, is_arch_64_bit, is_arm, "
                "is_armv5tel, is_armv6l, is_armv7l, is_armv8l, "
                "is_azure_pipelines, is_bamboo, is_bsd, is_bsd_not_macos, "
                "is_buildkite, is_buildroot, is_cachyos, is_centos, "
                "is_circle_ci, is_cirrus_ci, is_cloudlinux, is_codebuild, "
                "is_cygwin, is_debian, is_dragonfly_bsd, is_exherbo, "
                "is_fedora, is_freebsd, is_gentoo, is_github_ci, is_gitlab_ci, "
                "is_guix, is_haiku, is_heroku_ci, is_hurd, "
                "is_i386, is_i586, is_i686, is_ibm_mainframe, is_ibm_powerkvm, "
                "is_illumos, is_kvmibm, is_linux, is_linux_layers, is_linux_like, "
                "is_linuxmint, is_loongarch, is_loongarch64, is_macos, is_mageia, "
                "is_mandriva, is_midnightbsd, is_mips, is_mips64, is_mips64el, "
                "is_mipsel, is_netbsd, is_nobara, is_openbsd, is_opensuse, "
                "is_oracle, is_other_posix, is_parallels, is_pidora, is_powerpc, "
                "is_ppc, is_ppc64, is_ppc64le, is_raspbian, is_rhel, is_riscv, "
                "is_riscv32, is_riscv64, is_rocky, is_s390x, is_scientific, "
                "is_slackware, is_sles, is_solaris, is_sparc, is_sparc64, "
                "is_sunos, is_system_v, is_teamcity, is_travis_ci, is_tumbleweed, "
                "is_tuxedo, is_ubuntu, is_ultramarine, is_unix, is_unix_layers, "
                "is_unix_not_macos, is_unknown, is_unknown_architecture, "
                "is_unknown_ci, is_unknown_platform, is_wasm32, is_wasm64, "
                "is_webassembly, is_windows, is_wsl1, is_wsl2, is_x86, is_x86_64, "
                "is_xenserver, invalidate_caches, reduce"
            )
            root_content = f"""extra_platforms module
======================

.. automodule:: extra_platforms
   :members:
   :undoc-members:
   :show-inheritance:
   :imported-members:
   :exclude-members: {excluded_members}
"""
            root_rst.write_text(root_content)

        # Define functions/classes to document in each module.
        # This mirrors the structure of the real documentation.
        # Note: Platform, Architecture, and CI classes are documented in trait module.
        module_members = {
            "extra_platforms.detection": [
                "current_traits",
                "current_architecture",
                "current_platform",
                "current_ci",
                "is_linux",
                "is_macos",
                "is_windows",
                "is_aarch64",
                "invalidate_caches",
            ],
            "extra_platforms.operations": ["reduce"],
            "extra_platforms.trait": ["Trait", "Platform", "Architecture", "CI"],
            "extra_platforms.group": ["Group"],
            "extra_platforms.architecture_data": ["AARCH64", "X86_64"],
            "extra_platforms.platform_data": ["MACOS", "UBUNTU", "WINDOWS"],
            "extra_platforms.ci_data": ["GITHUB_CI", "GITLAB_CI"],
            "extra_platforms.group_data": ["ALL_PLATFORMS", "LINUX", "UNIX"],
        }

        for module in modules:
            # Extract the last component for the filename.
            module_name = module.split(".")[-1]
            rst_file = srcdir / f"{module_name}.rst"

            # Build the RST content with autofunction/autoclass/autodata directives.
            rst_lines = [
                f"{module_name} module",
                "=" * (len(module_name) + 7),
                "",
            ]

            # Add specific member documentation if defined.
            if module in module_members:
                # Add automodule directive to create module-level cross-reference target.
                rst_lines.extend(
                    [
                        f".. automodule:: {module}",
                        "",
                    ]
                )

                for member in module_members[module]:
                    # Determine the directive type based on naming convention.
                    if member[0].isupper():
                        # Constants and classes start with uppercase.
                        if member in ["Trait", "Platform", "Architecture", "CI", "Group"]:
                            directive = "autoclass"
                        else:
                            directive = "autodata"
                    else:
                        directive = "autofunction"

                    rst_lines.append(f".. {directive}:: extra_platforms.{member}")
                    rst_lines.append("")
            else:
                # Fall back to automodule for modules without specific members.
                rst_lines.extend(
                    [
                        f".. automodule:: {module}",
                        "   :members:",
                        "   :undoc-members:",
                        "   :show-inheritance:",
                    ]
                )

            rst_content = "\n".join(rst_lines) + "\n"
            rst_file.write_text(rst_content)

    def build_document(
        self, content: str, filename: str = "index.md"
    ) -> str | None:
        """Build a Sphinx document with content and return the HTML output.

        Args:
            content: The content to write to the document.
            filename: The filename to use (default: index.md).

        Returns:
            The HTML output as a string, or None if the build failed.
        """
        doc_file = Path(self.app.srcdir) / filename
        doc_file.write_text(content)

        # Build the documentation.
        self.app.build()

        # Read the generated HTML.
        # Convert filename to .html (e.g., index.md -> index.html).
        html_filename = Path(filename).stem + ".html"
        output_file = Path(self.app.outdir) / html_filename
        if output_file.exists():
            html_output = output_file.read_text()
            assert html_output
            return html_output

        return None


@pytest.fixture
def sphinx_app(tmp_path):
    """Create a Sphinx application for testing."""
    yield from SphinxAppWrapper.create(tmp_path)
