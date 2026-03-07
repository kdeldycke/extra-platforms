# CLAUDE.md

This file provides guidance to [Claude Code](https://claude.ai/code) when working with code in this repository.

## Project overview

Extra Platforms is a Python library for detecting and managing platform/OS information.

It provides:

- Detection of architectures, platforms (operating systems), shells, terminals, CI systems, and agents
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
├── CI - CI/CD systems
└── Agent - AI coding agents

Group - Collection of Traits with set-like operations (group.py)
```

### Module layout

| Module                 | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| `trait.py`             | Base classes: `Trait`, `Architecture`, `Platform`, `Shell`, `Terminal`, `CI`, `Agent` |
| `detection.py`         | All `is_<id>()` detection functions                                          |
| `group.py`             | `Group` class, `reduce()`, `traits_from_ids()`, `groups_from_ids()`          |
| `architecture_data.py` | All `Architecture` instances (X86_64, AARCH64, etc.)                         |
| `platform_data.py`     | All `Platform` instances (MACOS, UBUNTU, WINDOWS, etc.)                      |
| `shell_data.py`        | All `Shell` instances (BASH, ZSH, FISH, etc.)                               |
| `terminal_data.py`     | All `Terminal` instances (KITTY, ALACRITTY, TMUX, etc.)                      |
| `ci_data.py`           | All `CI` instances (GITHUB_CI, GITLAB_CI, etc.)                              |
| `agent_data.py`        | All `Agent` instances (CLAUDE_CODE, CLINE, CURSOR, etc.)                     |
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

### Terminology and spelling

Use correct capitalization for proper nouns and trademarked names:

- **PyPI** (not ~~PyPi~~) — the Python Package Index. The "I" is capitalized because it stands for "Index".
- **GitHub** (not ~~Github~~)
- **GitHub Actions** (not ~~Github Actions~~ or ~~GitHub actions~~)
- **JavaScript** (not ~~Javascript~~)
- **TypeScript** (not ~~Typescript~~)
- **macOS** (not ~~MacOS~~ or ~~macos~~)
- **iOS** (not ~~IOS~~ or ~~ios~~)

### Version formatting

The version string is always bare (e.g., `1.2.3`). The `v` prefix is a **tag namespace** — it only appears when the reference is to a git tag or something derived from a tag (action ref, comparison URL, commit message).

| Context                                | Format                          | Example                              | Rationale                         |
| :------------------------------------- | :------------------------------ | :----------------------------------- | :-------------------------------- |
| Python `__version__`, `pyproject.toml` | `1.2.3`                         | `version = "11.0.2"`                 | PEP 440 bare version.             |
| Git tags                               | `` `v1.2.3` ``                  | `` `v11.0.2` ``                      | Tag namespace convention.         |
| GitHub comparison URLs                 | `v1.2.3...v1.2.4`               | `compare/v11.0.1...v11.0.2`          | References tags.                  |
| GitHub action/workflow refs            | `` `@v1.2.3` ``                 | `actions/checkout@v6.0.2`            | References tags.                  |
| Commit messages                        | `v1.2.3`                        | `[changelog] Release v11.0.2`        | References the tag being created. |
| CLI `--version` output                 | `1.2.3`                         | `extra-platforms, version 11.0.2`    | Package version, not a tag.       |
| Changelog headings                     | `` `1.2.3` ``                   | `` ## [`11.0.2` (2026-03-04)] ``     | Package version, code-formatted.  |
| PyPI URLs                              | `1.2.3`                         | `pypi.org/project/extra-platforms/11.0.2/` | PyPI uses bare versions.    |
| PyPI admonitions                       | `` `1.2.3` ``                   | `` `11.0.2` is available on PyPI ``  | Package version, not a tag.       |
| PR titles                              | `` `v1.2.3` ``                  | `` Release `v11.0.2` ``              | References the tag.               |
| Prose/documentation                    | `` `v1.2.3` `` or `` `1.2.3` `` | Depends on referent                  | Match what is being referenced.   |

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

### Modern `typing` practices

Use modern equivalents from `collections.abc` and built-in types instead of `typing` imports. Use `X | Y` instead of `Union` and `X | None` instead of `Optional`. New modules should include `from __future__ import annotations`.

### Minimal inline type annotations

Omit type annotations on local variables, loop variables, and assignments when mypy can infer the type from the right-hand side. Always annotate function parameters and return types.

### Python 3.10 compatibility

This project supports Python 3.10+. Be aware of syntax features **not** available in Python 3.10:

- **Multi-line f-string expressions (Python 3.12+):** Cannot break an f-string after `{` onto the next line.
- **Exception groups and `except*` (Python 3.11+).**
- **`Self` type hint (Python 3.11+):** Use `from typing_extensions import Self` instead.

### YAML workflows

For single-line commands that fit on one line, use plain inline `run:` without any block scalar indicator:

```yaml
# Preferred for short commands: plain inline.
  - name: Install project
    run: uv --no-progress sync --frozen --all-extras --group test
```

When a command is too long for a single line, use the folded block scalar (`>`) to split it across multiple lines:

```yaml
# Preferred for long commands: folded block scalar joins lines with spaces.
  - name: Unittests
    run: >
      uv --no-progress run --frozen -- pytest
      --cov-report=xml
      --junitxml=junit.xml
```

Use literal block scalar (`|`) only when the command requires preserved newlines (e.g., multi-statement scripts, heredocs):

```yaml
# Use | for multi-statement scripts.
  - name: Install Python
    run: |
      set -e
      uv --no-progress venv --python "${{ matrix.python-version }}"
```

### Imports

- Import from the root package (`from extra_platforms import CI`), not submodules (`from extra_platforms.trait import CI`).
- Place imports at the top of the file, unless avoiding circular imports or improving data registry clarity.

## Testing guidelines

- Use `@pytest.mark.parametrize` when testing the same logic for multiple traits/groups.
- Keep test logic simple with straightforward asserts.
- Tests should be sorted logically and alphabetically where applicable.
- Enforce naming conventions for traits and groups via tests.
- Do not use classes for grouping tests. Write test functions as top-level module functions. Only use test classes when they provide shared fixtures, setup/teardown methods, or class-level state.

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

- **Trait category ordering**: When trait categories appear together (in code sections, imports, collections, documentation, tests, etc.), they must follow this canonical order: **Architecture → Platform → Shell → Terminal → CI → Agent**. This applies to class definitions, detection function sections, group collections, `__all__` exports, documentation pages, and test files.
- All IDs must be unique across traits and groups.
- High-level objects in data files must be sorted alphabetically by ID.
- Tests should verify this ordering.

### Caching

- Detection functions are cached with `@cache` decorator.
- Use `invalidate_caches()` to reset all cached detection results.

### Common maintenance pitfalls

- **Documentation drift** is the most frequent issue. CLI output, version references, and workflow job descriptions in `readme.md` go stale after every release or refactor. Always verify docs against actual output after changes.
- **CI debugging starts from the URL.** When a workflow fails, fetch the run logs first (`gh run view --log-failed`). Do not guess at the cause.
- **Type-checking divergence.** Code that passes `mypy` locally may fail in CI where `--python-version 3.10` is used. Always consider the minimum supported Python version.
- **Simplify before adding.** When asked to improve something, first ask whether existing code or tools already cover the case. Remove dead code and unused abstractions before introducing new ones.

### Optional dependencies

Pytest integration requires the `extra_platforms[pytest]` extra.
