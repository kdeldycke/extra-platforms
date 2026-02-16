# CLAUDE.md

This file provides guidance to [Claude Code](https://claude.ai/code) when working with code in this repository.

## Project overview

Extra Platforms is a Python library for detecting and managing platform/OS information.

It provides:

- Detection of architectures, platforms (operating systems), shells, terminals, and CI systems
- Grouping of platforms into families (e.g., `LINUX`, `BSD`, `UNIX`)
- Pytest decorators for conditional test skipping (`@skip_<id>`, `@unless_<id>`)

## Upstream conventions

This repository uses reusable workflows from [`kdeldycke/workflows`](https://github.com/kdeldycke/workflows) and follows the conventions established there. For code style, documentation, testing, and design principles, refer to the upstream `claude.md` as the canonical reference.

**Contributing upstream:** If you spot inefficiencies, improvements, or missing features in the reusable workflows, propose changes via a pull request or issue at [`kdeldycke/workflows`](https://github.com/kdeldycke/workflows/issues).

## Commands

### Testing

```shell-session
# Run all tests with coverage.
$ uv run --group test pytest

# Run a single test file.
$ uv run --group test pytest tests/test_platform_data.py

# Run a specific test.
$ uv run --group test pytest tests/test_platform_data.py::test_function_name

# Run tests in parallel.
$ uv run --group test pytest -n auto
```

### Type checking

```shell-session
$ uv run --group typing mypy extra_platforms
```

### Documentation

Build Sphinx documentation locally:

```shell-session
$ uv run sphinx-build -b html ./docs ./docs/html
```

## Architecture

### Core classes

All core classes are defined in `trait.py`:

```
Trait (ABC) - Base class for all detectable traits
├── Architecture - CPU architectures
├── Platform - Operating systems
├── Shell - Command-line shells
├── Terminal - Terminal emulators
└── CI - CI/CD systems

Group - Collection of Traits with set-like operations (group.py)
```

### Module layout

| Module                 | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| `trait.py`             | Base classes: `Trait`, `Architecture`, `Platform`, `Shell`, `Terminal`, `CI` |
| `detection.py`         | All `is_<id>()` detection functions                                          |
| `group.py`             | `Group` class, `reduce()`, `traits_from_ids()`, `groups_from_ids()`          |
| `architecture_data.py` | All `Architecture` instances (X86_64, AARCH64, etc.)                         |
| `platform_data.py`     | All `Platform` instances (MACOS, UBUNTU, WINDOWS, etc.)                      |
| `shell_data.py`        | All `Shell` instances (BASH, ZSH, FISH, etc.)                               |
| `terminal_data.py`     | All `Terminal` instances (KITTY, ALACRITTY, TMUX, etc.)                      |
| `ci_data.py`           | All `CI` instances (GITHUB_CI, GITLAB_CI, etc.)                              |
| `group_data.py`        | All `Group` instances and ID collections                            |
| `pytest.py`            | Generates `@skip_<id>` and `@unless_<id>` decorators                |
| `_utils.py`            | Internal utilities                                                  |
| `_types.py`            | Type aliases                                                        |

### Detection pattern

Each trait has a corresponding `is_<id>()` function in `detection.py`. The `Trait.current` cached property calls `detection.is_{self.id}()` to check if the trait matches the current environment.

### Dynamic code generation

- `__init__.py` generates `is_<group_id>()` functions for all groups at import time
- `pytest.py` generates `skip_<id>` and `unless_<id>` decorators for all traits and groups

## Documentation requirements

### Changelog and readme updates

Always update documentation when making changes:

- **`changelog.md`**: Add a bullet point describing user-facing changes (new features, bug fixes, behavior changes).
- **`readme.md`**: Update relevant sections when adding/modifying public API, classes, or functions.

## Code style

### Comments and docstrings

- All comments in Python files must end with a period.
- Docstrings use reStructuredText format (vanilla style, not Google/NumPy).
- Documentation in `./docs/` uses MyST markdown format where possible. Fallback to reStructuredText if necessary.
- Keep lines within 88 characters in Python files, including docstrings and comments (ruff default). Markdown files have no line-length limit.
- Titles in markdown use sentence case.

### Documenting code decisions

Document design decisions, trade-offs, and non-obvious implementation choices directly in the code:

- Use **docstring admonitions** for important notes:

  ```python
  """Extract metadata from repository.

  .. warning::
      This method temporarily modifies repository state during execution.

  .. note::
      The commit range is inclusive on both ends.
  """
  ```

- Use **inline comments** for explaining specific code blocks:

  ```python
  # We use a frozenset for O(1) lookups and immutability.
  SKIP_BRANCHES: Final[frozenset[str]] = frozenset(("branch-a", "branch-b"))
  ```

### `TYPE_CHECKING` block

Place a module-level `TYPE_CHECKING` block immediately after the module docstring:

```python
TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterator
    from ._types import _T, _TNestedReferences
```

### Imports

- Import from the root package (`from extra_platforms import CI`), not submodules (`from extra_platforms.trait import CI`).
- Place imports at the top of the file, unless avoiding circular imports or improving data registry clarity.

## Testing guidelines

- Use `@pytest.mark.parametrize` when testing the same logic for multiple traits/groups.
- Keep test logic simple with straightforward asserts.
- Tests should be sorted logically and alphabetically where applicable.
- Enforce naming conventions for traits and groups via tests.

## Design principles

### Philosophy

1. Create something that works (to provide business value).
1. Create something that's beautiful (to lower maintenance costs).
1. Work on performance.

### Linting and formatting

Linting and formatting are automated via GitHub workflows. Developers don't need to run these manually during development, but are still expected to do best effort. Push your changes and the workflows will catch any issues.

### Data registry priority

The `*_data.py` files (trait and group definitions) should be clean and easy to maintain. It's acceptable to use indirections elsewhere (like function-level imports) to achieve this.

### Icon conventions

Icons are inspired by [Starship](https://starship.rs/) and [NerdFonts](https://www.nerdfonts.com/). Each trait and group has a single-glyph icon (1–2 Python `len()` characters, accounting for variation selectors like `U+FE0F`).

**General rules:**

- Icons must be unique across all traits and groups, with one exception: a canonical group may share its icon with its members, but only if *all* members use that same icon (e.g., all ARM architectures share `📱` with the `ALL_ARM` group).
- Never use a multi-character suffix like `+` to derive a group icon from a related icon.
- When proposing a new icon, always check for conflicts against existing traits *and* groups.

**Traits** use pictographic, brand-representative icons:

- Prefer mascots, logos, or symbols associated with the project (e.g., `🍎` macOS, `😈` FreeBSD, `🐙` GitHub Actions, `🎩` Fedora/RHEL).
- Fall back to a thematic pictographic emoji when no obvious brand symbol exists (e.g., `🌅` SunOS, `🦬` GNU/Hurd).
- Traits in the same canonical group may share the same icon when they are closely related variants (e.g., `📱` for all ARM architectures, `🔲` for all MIPS, `☀️` for SPARC/SPARC64).

**Groups** use boxy, abstract, or geometric icons:

- Prefer enclosed/squared letters and geometric symbols: `🅱️`, `🅲`, `🅟`, `Ⓑ`, `⊞`.
- Arrows and mathematical symbols work well: `⬆️`, `⬇️`, `⨷`, `⨂`, `≚`, `≛`, `♺`.
- Superscript/subscript characters for numeric concepts: `⁶⁴`, `³²`.
- Stylized letters for named families: `𝐕` (System V), `𝘅` (x86), `Ⅴ` (RISC-V).
- Emoji are acceptable for top-level "all" groups: `🏛️` (all architectures), `⚙️` (all platforms), `🐚` (all shells).

### Ordering and uniqueness

- **Trait category ordering**: When trait categories appear together (in code sections, imports, collections, documentation, tests, etc.), they must follow this canonical order: **Architecture → Platform → Shell → Terminal → CI**. This applies to class definitions, detection function sections, group collections, `__all__` exports, documentation pages, and test files.
- All IDs must be unique across traits and groups.
- High-level objects in data files must be sorted alphabetically by ID.
- Tests should verify this ordering.

### Caching

- Detection functions are cached with `@cache` decorator.
- Use `invalidate_caches()` to reset all cached detection results.

### Optional dependencies

Pytest integration requires the `extra_platforms[pytest]` extra.
