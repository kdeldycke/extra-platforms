# CLAUDE.md

This file provides guidance to [Claude Code](https://claude.ai/code) when working with code in this repository.

It carries only what is specific to Extra Platforms. The generic conventions (code style, typing, commit messages, changelog length, file naming, documentation and testing rules) come from the maintainer's machine-wide instructions file and from the conventions of [`kdeldycke/repomatic`](https://github.com/kdeldycke/repomatic), whose reusable workflows this repository consumes. A few rules below deliberately depart from those generic ones. Each says so, and names the reason.

## Project overview

Extra Platforms is a Python library for detecting and managing platform/OS information.

It provides:

- Detection of architectures, platforms (operating systems), shells, terminals, CI systems, and agents
- Grouping of platforms into families (like `LINUX`, `BSD`, `UNIX`)
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
$ uvx repomatic run mypy
```

Pass no file list. The tool runner resolves mypy's targets from the repository's Python file inventory, which covers `extra_platforms`, `tests` and `docs`. This is the exact command the Lint workflow runs, so naming a single package here would type-check less than CI does.

### Documentation

Build Sphinx documentation locally:

```shell-session
$ uv run sphinx-build -b html ./docs ./docs/_build
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

| Module                 | Purpose                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------- |
| `trait.py`             | Base classes: `Trait`, `Architecture`, `Platform`, `Shell`, `Terminal`, `CI`, `Agent` |
| `detection.py`         | All `is_<id>()` detection functions                                                   |
| `group.py`             | `Group` class, `reduce()`, `traits_from_ids()`, `groups_from_ids()`                   |
| `architecture_data.py` | All `Architecture` instances (X86_64, AARCH64, etc.)                                  |
| `platform_data.py`     | All `Platform` instances (MACOS, UBUNTU, WINDOWS, etc.)                               |
| `platform_info.py`     | Version, codename and CPE metadata behind `Platform.info()`                           |
| `shell_data.py`        | All `Shell` instances (BASH, ZSH, FISH, etc.)                                         |
| `terminal_data.py`     | All `Terminal` instances (KITTY, ALACRITTY, TMUX, etc.)                               |
| `ci_data.py`           | All `CI` instances (GITHUB_CI, GITLAB_CI, etc.)                                       |
| `agent_data.py`        | All `Agent` instances (CLAUDE_CODE, CLINE, CURSOR, etc.)                              |
| `group_data.py`        | All `Group` instances and ID collections                                              |
| `pytest.py`            | Generates `@skip_<id>` and `@unless_<id>` decorators                                  |
| `_utils.py`            | Internal utilities                                                                    |
| `_types.py`            | Type aliases                                                                          |

### Detection pattern

Each trait has a corresponding `is_<id>()` function in `detection.py`. The `Trait.current` cached property calls `detection.is_{self.id}()` to check if the trait matches the current environment.

### Dynamic code generation

- `__init__.py` generates `is_<group_id>()` functions for all groups at import time
- `pytest.py` generates `skip_<id>` and `unless_<id>` decorators for all traits and groups

## Documentation requirements

### Scope of `CLAUDE.md` versus `readme.md`

- **`CLAUDE.md`**: contributor and Claude-focused directives, covering code style, testing guidelines, design principles, and internal development guidance.
- **`readme.md`**: user-facing documentation, covering installation, usage, and the public API.

When adding new content, decide whether it helps end users (`readme.md`) or contributors and Claude working on the codebase (`CLAUDE.md`).

Update `readme.md` whenever you add or change a public API, class, or function.

## Code style

### Imports

Function-level imports are allowed in the `*_data.py` registries when they keep a registry readable. This is a deliberate exception to the general rule against local imports: see [§ Data registry priority](#data-registry-priority). Everywhere else, imports go at the top of the file.

## Testing guidelines

- Use `@pytest.mark.parametrize` when testing the same logic across multiple traits or groups.
- Enforce naming conventions for traits and groups via tests.
- Test coverage is measured with `pytest-cov` and gated by the `[tool.coverage] report.fail_under` ratchet. No external coverage service is involved: repomatic dropped its Codecov integration in `7.8.0`.
- **`@pytest.mark.once` is not used here yet.** Upstream repomatic tags matrix-insensitive tests with a custom `once` marker, filters them out of the main matrix, and runs them on a single runner. Nearly every test here exercises platform-sensitive behavior worth running on every cell. Adopt the full convention (marker in `[tool.pytest].markers`, `-m` filters in `tests.yaml`) the day a genuinely matrix-insensitive test appears.
- **Pytest flags needing an optional plugin belong in workflow steps, not `[tool.pytest].addopts`.** This departs from the generic rule, which puts `--cov` and `--numprocesses` in `addopts`. Here every coverage and xdist flag (`--cov`, `--cov-report`, `--numprocesses`, `--dist`) is passed by `tests.yaml` instead, so a from-source packager build (Guix, Nixpkgs, ...) can run a plain `pytest` without having to supply `pytest-cov` and `pytest-xdist` just to start. `addopts` carries only flags that need no extra dependency.
- **Write conformance tests when fixing a class of bugs.** Iterate over every member of the set (traits, groups, detection functions, data files) and assert the property uniformly. Model: `tests/test_group_data.py::test_each_trait_in_exactly_one_canonical_group`.

## Design principles

### Data registry priority

The `*_data.py` files (trait and group definitions) should be clean and easy to maintain. It is acceptable to use indirections elsewhere, like function-level imports, to achieve this.

### Platform granularity

- **Independent derivative distributions** get a dedicated `Platform` object, even when they build on a parent distribution. Ubuntu, Kali, Linux Mint, Raspbian and PikaOS are all Debian derivatives, but each is managed by its own organization.
- **Channels, variants and flavors of the same distribution**, managed by the same organization or maintainers as the parent, share the parent's platform object: match their `os-release` ID in the parent's detection function, like `is_opensuse()` matching every `opensuse-*` channel (Tumbleweed, Leap, Slowroll, MicroOS, ...). `os_release_id()` returns the raw sub-variant ID untouched, so `Platform.info()` still exposes the exact flavor.

The canonical statement of this policy lives in the `platform_data.py` module docstring.

### Icon conventions

Icons are inspired by [Starship](https://starship.rs/) and [NerdFonts](https://www.nerdfonts.com/). Each trait and group has a single-glyph icon (1–2 Python `len()` characters, accounting for variation selectors like `U+FE0F`).

**General rules:**

- Icons must be unique across all traits and groups, with one exception: a canonical group may share its icon with its members, but only if *all* members use that same icon (all ARM architectures share `📱` with the `ALL_ARM` group).
- Never use a multi-character suffix like `+` to derive a group icon from a related icon.
- When proposing a new icon, always check for conflicts against existing traits *and* groups.

**Traits** use pictographic, brand-representative icons:

- Prefer mascots, logos, or symbols associated with the project (`🍎` macOS, `😈` FreeBSD, `🐙` GitHub Actions, `🎩` Fedora/RHEL).
- Fall back to a thematic pictographic emoji when no obvious brand symbol exists (`🌅` SunOS, `🦬` GNU/Hurd).
- Traits in the same canonical group may share the same icon when they are closely related variants (`📱` for all ARM architectures, `🔲` for all MIPS, `☀️` for SPARC/SPARC64).

**Groups** use boxy, abstract, or geometric icons:

- Prefer enclosed or squared letters and geometric symbols: `🅱️`, `🅲`, `🅟`, `Ⓑ`, `⊞`.
- Arrows and mathematical symbols work well: `⬆️`, `⬇️`, `⨷`, `⨂`, `≚`, `≛`, `♺`.
- Superscript and subscript characters for numeric concepts: `⁶⁴`, `³²`.
- Stylized letters for named families: `𝐕` (System V), `𝘅` (x86), `Ⅴ` (RISC-V).
- Emoji are acceptable for top-level "all" groups: `🏛️` (all architectures), `⚙️` (all platforms), `🐚` (all shells).

### Ordering and uniqueness

- **Trait category ordering**: when trait categories appear together (in code sections, imports, collections, documentation, tests), they must follow this canonical order: **Architecture → Platform → Shell → Terminal → CI → Agent**. This applies to class definitions, detection function sections, group collections, `__all__` exports, documentation pages, and test files.
- All IDs must be unique across traits and groups.
- High-level objects in data files must be sorted alphabetically by ID.
- Tests should verify this ordering.

### Caching

- Detection functions are cached with the `@cache` decorator.
- Use `invalidate_caches()` to reset all cached detection results.

### Optional dependencies

Pytest integration requires the `extra_platforms[pytest]` extra.
