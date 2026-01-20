# CLAUDE.md

This file provides guidance to [Claude Code](https://claude.ai/code) when working with code in this repository.

## Project overview

Extra Platforms is a Python library for detecting and managing platform/OS information.

It provides:

- Detection of architectures, platforms (operating systems), and CI systems
- Grouping of platforms into families (e.g., `LINUX`, `BSD`, `UNIX`)
- Pytest decorators for conditional test skipping (`@skip_<id>`, `@unless_<id>`)

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
├── Platform - Operating systems
├── Architecture - CPU architectures
└── CI - CI/CD systems

Group - Collection of Traits with set-like operations (group.py)
```

### Module layout

| Module | Purpose |
|--------|---------|
| `trait.py` | Base classes: `Trait`, `Platform`, `Architecture`, `CI` |
| `detection.py` | All `is_<id>()` detection functions |
| `group.py` | `Group` class, `reduce()`, `traits_from_ids()`, `groups_from_ids()` |
| `platform_data.py` | All `Platform` instances (MACOS, UBUNTU, WINDOWS, etc.) |
| `architecture_data.py` | All `Architecture` instances (X86_64, AARCH64, etc.) |
| `ci_data.py` | All `CI` instances (GITHUB_CI, GITLAB_CI, etc.) |
| `group_data.py` | All `Group` instances and ID collections |
| `pytest.py` | Generates `@skip_<id>` and `@unless_<id>` decorators |
| `_deprecated.py` | Backward-compatible aliases for renamed symbols |
| `_utils.py` | Internal utilities |
| `_types.py` | Type aliases |

### Detection pattern

Each trait has a corresponding `is_<id>()` function in `detection.py`. The `Trait.current` cached property calls `detection.is_{self.id}()` to check if the trait matches the current environment.

### Dynamic code generation

- `__init__.py` generates `is_<group_id>()` functions for all groups at import time
- `pytest.py` generates `skip_<id>` and `unless_<id>` decorators for all traits and groups

## Code style

### Comments and docstrings

- All comments in Python files must end with a period.
- Docstrings use reStructuredText format (vanilla style, not Google/NumPy).
- Documentation in `./docs/` uses MyST markdown format where possible. Fallback to reStructuredText if necessary.
- Keep lines within 88 characters.
- Titles in markdown use sentence case.

### Type checking

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

### Data registry priority

The `*_data.py` files (trait and group definitions) should be clean and easy to maintain. It's acceptable to use indirections elsewhere (like function-level imports) to achieve this.

### Ordering and uniqueness

- All IDs must be unique across traits and groups.
- High-level objects in data files must be sorted alphabetically by ID.
- Tests should verify this ordering.

### Caching

- Detection functions are cached with `@cache` decorator.
- Use `invalidate_caches()` to reset all cached detection results.

### Optional dependencies

Pytest integration requires the `extra_platforms[pytest]` extra.
