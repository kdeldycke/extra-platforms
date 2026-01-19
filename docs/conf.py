from __future__ import annotations

import ast
import importlib
import inspect
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]

from extra_platforms import Group
from extra_platforms.trait import Trait


def get_attribute_docstring(module_name: str, attr_name: str) -> str | None:
    """Extract attribute docstring from a module's source file.

    Attribute docstrings are string literals that immediately follow an assignment.
    This function parses the source file using AST to find such docstrings.

    Args:
        module_name: The full module name (e.g., 'extra_platforms.platform_data').
        attr_name: The attribute name to look for (e.g., 'NOBARA').

    Returns:
        The attribute docstring if found, or None.
    """
    try:
        module = importlib.import_module(module_name)
        source_file = inspect.getsourcefile(module)
        if not source_file:
            return None

        source = Path(source_file).read_text(encoding="utf-8")
        tree = ast.parse(source)

        # Look for assignment (or annotated assignment) followed by a string literal.
        for i, node in enumerate(tree.body):
            # Handle both regular assignments and annotated assignments
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == attr_name:
                        # Check if the next statement is a string expression.
                        if i + 1 < len(tree.body):
                            next_node = tree.body[i + 1]
                            if isinstance(next_node, ast.Expr) and isinstance(
                                next_node.value, ast.Constant
                            ):
                                if isinstance(next_node.value.value, str):
                                    return next_node.value.value
            elif isinstance(node, ast.AnnAssign):
                # Handle annotated assignments like: x: type = value
                if isinstance(node.target, ast.Name) and node.target.id == attr_name:
                    # Check if the next statement is a string expression.
                    if i + 1 < len(tree.body):
                        next_node = tree.body[i + 1]
                        if isinstance(next_node, ast.Expr) and isinstance(
                            next_node.value, ast.Constant
                        ):
                            if isinstance(next_node.value.value, str):
                                return next_node.value.value
        return None
    except Exception:
        return None


project_path = Path(__file__).parent.parent.resolve()

# Fetch general information about the project from pyproject.toml.
toml_path = project_path / "pyproject.toml"
toml_config = tomllib.loads(toml_path.read_text())

# Redistribute pyproject.toml config to Sphinx.
project_id = toml_config["project"]["name"]
version = release = toml_config["project"]["version"]
url = toml_config["project"]["urls"]["Homepage"]
author = ", ".join(author["name"] for author in toml_config["project"]["authors"])

# Title-case each word of the project ID.
project = " ".join(word.title() for word in project_id.split("-"))
htmlhelp_basename = project_id

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

master_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

nitpicky = True

# Concatenates the docstrings of the class and the __init__ method.
autoclass_content = "both"
# Keep the same ordering as in original source code.
autodoc_member_order = "bysource"
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"]

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
html_show_copyright = True
html_show_sphinx = False


def make_pytest_decorator_line(obj):
    """Create pytest decorator documentation line."""
    return (
        "- **Pytest decorators**: "
        f":data:`~pytest.{obj.skip_decorator_id}` / "
        f":data:`~pytest.{obj.unless_decorator_id}`"
    )


def autodoc_process_docstring(app, what, name, obj, options, lines):
    """Generate docstrings for Trait instances, Groups, and frozenset collections.

    Since autodata directives use ``extra_platforms.X`` paths but the attribute
    docstrings (string literals following assignments) are defined in submodules
    like ``platform_data.py``, ``group_data.py``, and ``operations.py``, this hook
    fetches those docstrings from the source files using AST parsing and injects them
    into the documentation along with additional metadata.
    """
    if isinstance(obj, Group):
        # Fetch attribute docstring from source module since autodata uses
        # extra_platforms.X but docstrings are in the submodules.
        source_docstring = get_attribute_docstring(
            f"extra_platforms.{obj.data_module_id}", obj.symbol_id
        )
        if source_docstring:
            # Clear any existing content and add the source docstring.
            lines.clear()
            lines.extend(source_docstring.strip().split("\n"))

        lines.append("")

        lines.append(f"- **ID**: ``{obj.id}``")
        lines.append(f"- **Name**: {obj.name}")
        lines.append(f"- **Icon**: {obj.icon}")
        lines.append(
            f"- **Canonical**: ``{obj.canonical}`` {'⬥' if obj.canonical else ''}"
        )

        lines.append(f"- **Detection function**: :func:`~{obj.detection_func_id}`")

        lines.append(make_pytest_decorator_line(obj))

        # Add list of members with links to their definitions.
        member_links = []
        type_counts = {}

        for _, member in obj.items():
            class_name = type(member).__name__

            # Count types.
            if class_name not in type_counts:
                type_counts[class_name] = {"count": 0}
            type_counts[class_name]["count"] += 1

            # Create member link using Sphinx role.
            member_links.append(f":data:`~{member.symbol_id}`")

        if member_links:
            # Format type information with links.
            type_parts = [
                f"{info['count']} :class:`~{class_name}`"
                for class_name, info in sorted(type_counts.items())
            ]
            type_info = ", ".join(type_parts)
            lines.append(f"- **Members** ({type_info}): {', '.join(member_links)}")

    elif isinstance(obj, Trait):
        # Fetch attribute docstring from source module since autodata uses
        # extra_platforms.X but docstrings are in the submodules.
        source_docstring = get_attribute_docstring(
            f"extra_platforms.{obj.data_module_id}", obj.symbol_id
        )
        if source_docstring:
            # Clear any existing content and add the source docstring.
            lines.clear()
            lines.extend(source_docstring.strip().split("\n"))

        lines.append("")

        lines.append(f"- **ID**: ``{obj.id}``")
        lines.append(f"- **Name**: {obj.name}")
        lines.append(f"- **Icon**: {obj.icon}")
        lines.append(f"- **Reference**: <{obj.url}>_")

        lines.append(f"- **Detection function**: :func:`~{obj.detection_func_id}`")

        lines.append(make_pytest_decorator_line(obj))

        # Add list of groups this trait belongs to.
        group_links = [
            f":data:`~{group.symbol_id}`" + (" ⬥" if group.canonical else "")
            for group in sorted(obj.groups, key=lambda g: g.id)
        ]
        lines.append(f"- **Groups** ({len(group_links)}): {', '.join(group_links)}")

    elif isinstance(obj, frozenset):
        # Handle frozenset collections - fetch their docstrings from source modules.
        # Map collection names to their source modules.
        collection_modules = {
            "ALL_GROUPS": "group_data",
            "ALL_PLATFORM_GROUPS": "group_data",
            "ALL_ARCHITECTURE_GROUPS": "group_data",
            "ALL_CI_GROUPS": "group_data",
            "EXTRA_GROUPS": "group_data",
            "NON_OVERLAPPING_GROUPS": "group_data",
            "ALL_GROUP_IDS": "operations",
            "ALL_TRAIT_IDS": "operations",
            "ALL_IDS": "operations",
        }

        # Extract the symbol name from the full qualified name.
        symbol_name = name.split(".")[-1]

        if symbol_name in collection_modules:
            source_module = collection_modules[symbol_name]
            source_docstring = get_attribute_docstring(
                f"extra_platforms.{source_module}", symbol_name
            )
            if source_docstring:
                # Clear the generic frozenset docstring and replace with the actual one.
                lines.clear()
                lines.extend(source_docstring.strip().split("\n"))


def autodoc_skip_member(app, what, name, obj, skip, options):
    """Force inclusion of Trait instances and Groups, skip detection functions from main module.

    By default, autodoc skips module-level constants without docstrings.
    Since our trait instances have dynamically generated docstrings, we need
    to explicitly include them.

    Also skip detection functions (is_*) when documenting the main extra_platforms
    module, since they're already documented in detection.md. This prevents duplicate
    documentation and ensures cross-references point to detection.html.
    """
    if isinstance(obj, (Trait, Group)):
        return False  # Don't skip - include in documentation

    # Skip detection functions, operations functions, and main classes when
    # documenting the root module via RST.
    # Detection functions fall into two categories:
    # 1. Trait detection functions (is_<trait>, current_*) defined in
    #    extra_platforms.detection
    # 2. Group detection functions (is_<group>) dynamically generated in
    #    extra_platforms.__init__
    #
    # Main classes (Trait, Group, Platform, Architecture, CI) are explicitly
    # documented in their respective pages (trait.md, groups.md) and should not
    # appear in extra_platforms.html to avoid duplicate documentation.
    if what == "module":
        obj_module = getattr(obj, "__module__", None)

        # Skip all detection functions (both from detection module and dynamically
        # generated group detection functions)
        if obj_module in (
            "extra_platforms.detection",
            "extra_platforms",
        ) and name.startswith(("is_", "current_")):
            return True  # Skip - already documented in detection.md

        # Skip invalidate_caches - documented in detection.md
        if name == "invalidate_caches" and obj_module in (
            "extra_platforms.detection",
            "extra_platforms",
        ):
            return True  # Skip - already documented in detection.md

        # Skip operations functions - documented in groups.md
        if obj_module == "extra_platforms.operations" and name in (
            "groups_from_ids",
            "traits_from_ids",
            "reduce",
        ):
            return True  # Skip - already documented in groups.md

        # Skip main trait and group classes - they're documented in their own pages
        if obj_module in (
            "extra_platforms.trait",
            "extra_platforms.group",
        ) and name in ("Trait", "Platform", "Architecture", "CI", "Group"):
            return True  # Skip - already documented in trait.md or groups.md

    return None  # Use default behavior for everything else


def setup(app):
    """Connect Sphinx events to custom handlers."""
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-skip-member", autodoc_skip_member)
