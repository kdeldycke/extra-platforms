# Changelog

## [9.2.1.dev0 (unreleased)](https://github.com/kdeldycke/extra-platforms/compare/v9.2.0...main)

> [!IMPORTANT]
> This version is not released yet and is under active development.

- Replace `distro` dependency with built-in `/etc/os-release` parser, making the package dependency-free. macOS `Platform.info()` now returns `distro_id: None` instead of `distro_id: "darwin"`.
- Add new `Agent` trait type for detecting AI coding agents.
- Add 3 agent definitions: `CLAUDE_CODE`, `CLINE`, `CURSOR`.
- Add `current_agent()` detection function.
- Add agent group: `ALL_AGENTS`.
- Add `@skip_<agent>` and `@unless_<agent>` pytest decorators for all agents and agent groups.
- Add `GENERIC_LINUX` platform for Linux environments where `distro` cannot identify the specific distribution (e.g., minimal containers or build chroots without `/etc/os-release`). Closes #479.
- Use `TERM`, `CI`, and `LLM` environment variables to distinguish unrecognized terminals, CI systems, and agents from absent ones.

## [`9.2.0` (2026-02-16)](https://github.com/kdeldycke/extra-platforms/compare/v9.1.0...v9.2.0)

> [!NOTE]
> `9.2.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/9.2.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v9.2.0).

- Add new `Terminal` trait type for detecting terminal emulators. Closes #459.
- Add 20 terminal definitions: `ALACRITTY`, `APPLE_TERMINAL`, `CONTOUR`, `FOOT`, `GHOSTTY`, `GNOME_TERMINAL`, `GNU_SCREEN`, `HYPER`, `ITERM2`, `KITTY`, `KONSOLE`, `RIO`, `TABBY`, `TILIX`, `TMUX`, `VSCODE_TERMINAL`, `WEZTERM`, `WINDOWS_TERMINAL`, `XTERM`, `ZELLIJ`.
- Add `current_terminal()` detection function.
- Add terminal groups: `ALL_TERMINALS`, `GPU_TERMINALS`, `MULTIPLEXERS`, `NATIVE_TERMINALS`, `WEB_TERMINALS`.
- Add `@skip_<terminal>` and `@unless_<terminal>` pytest decorators for all terminals and terminal groups.
- Display all detected traits and groups in `extra-platforms` CLI.
- Fix emoji column alignment in CLI.

## [`9.1.0` (2026-02-15)](https://github.com/kdeldycke/extra-platforms/compare/v9.0.0...v9.1.0)

> [!NOTE]
> `9.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/9.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v9.1.0).

- Add `extra-platforms` CLI command.
- Skip Nuitka binary builds.
- Add new `ALPINE`, `KALI`, `MANJARO`, `OPENWRT` platform definitions.
- Replace filesystem-based shell detection with parent process tree walking via `/proc` on Linux.
- Make `is_powershell()` detection cross-platform (Linux, macOS, Windows) via `PSModulePath` environment variable and process tree inspection.
- Fix CLI crash on Windows due to `cp1252` encoding not supporting Unicode output.
- Tweak some icons.
- Add issue template with detection results reporting.

## [`9.0.0` (2026-02-12)](https://github.com/kdeldycke/extra-platforms/compare/v8.0.0...v9.0.0)

> [!NOTE]
> `9.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/9.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v9.0.0).

- Add new `Shell` trait type for detecting command-line interpreters.
- Add 12 shell definitions: `ASH`, `BASH`, `CMD`, `CSH`, `DASH`, `FISH`, `KSH`, `NUSHELL`, `POWERSHELL`, `TCSH`, `XONSH`, `ZSH`.
- Add `current_shell()` detection function.
- Add shell groups: `ALL_SHELLS`, `BOURNE_SHELLS`, `C_SHELLS`, `OTHER_SHELLS`, `WINDOWS_SHELLS`.
- Add `@skip_<shell>` and `@unless_<shell>` pytest decorators for all shells and shell groups.
- Fix icons conflicts.
- Fix crash in compiled binaries (Nuitka, PyInstaller, cx_Freeze) caused by missing source files for docstring extraction.
- Force Sphinx documentation builds to use Python >= 3.12 via `[tool.uv.dependency-groups]`.
- Remove all deprecated backward-compatibility aliases:
  - Remove `ALL_PLATFORM_IDS` (use `ALL_TRAIT_IDS`).
  - Remove `ALL_PLATFORMS_WITHOUT_CI` (use `ALL_PLATFORMS`).
  - Remove `UNKNOWN_LINUX` (use `UNKNOWN_PLATFORM`).
  - Remove `ANY_ARM`, `ANY_MIPS`, `ANY_SPARC`, `ANY_WINDOWS` (use `ALL_ARM`, `ALL_MIPS`, `ALL_SPARC`, `ALL_WINDOWS`).
  - Remove `OTHER_UNIX` (use `OTHER_POSIX`).
  - Remove `current_os()` (use `current_platform()`).
  - Remove `current_platforms()` (use `current_traits()`).
  - Remove `platforms_from_ids()` (use `traits_from_ids()`).
  - Remove `is_unknown_linux()` (use `is_unknown_platform()`).
  - Remove `is_all_architectures()`, `is_all_platforms()`, `is_all_ci()`, `is_all_traits()` (use `is_any_architecture()`, `is_any_platform()`, `is_any_ci()`, `is_any_trait()`).
  - Remove `is_all_platforms_without_ci()` (use `is_any_platform()`).
  - Remove `is_ci()` (use `is_any_ci()`).
  - Remove `is_other_unix()` (use `is_other_posix()`).
  - Remove `is_bsd_without_macos()` (use `is_bsd_not_macos()`).
  - Remove `is_unix_without_macos()` (use `is_unix_not_macos()`).
  - Remove `Group._extract_members()` and `Group._extract_platforms()` (use `extract_members()`).
  - Remove deprecated module shims for `extra_platforms.platform` and `extra_platforms.operations`.
- Remove `_deprecated.py` module.

## [`8.0.0` (2026-02-02)](https://github.com/kdeldycke/extra-platforms/compare/v7.0.0...v8.0.0)

> [!NOTE]
> `8.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/8.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v8.0.0).

- Add `aliases` field to `Trait` class, allowing alternative IDs that resolve to the canonical ID.
- Add aliases for common architecture names:
  - `arm64` → `aarch64`
  - `amd64` → `x86_64`
  - `armhf`, `armv7` → `armv7l`
  - `i486` → `i386`
  - `powerpc64le`, `ppc64el` → `ppc64le`
- Emit a `UserWarning` when an alias is used, encouraging use of the canonical ID.
- Change `Trait.aliases` type from `tuple` to `frozenset` for better semantics.
- Add new `BIG_ENDIAN` and `LITTLE_ENDIAN` groups to classify architectures by endianness, with `is_big_endian()` and `is_little_endian()` detection functions.
- Remove `operations.py` and move content to `group` and `group_data` modules.
- Rename `Group._extract_members()` to `extract_members()` and make it public.
- Simplify `reduce()` algorithm from brute-force enumeration to a greedy approximation for better performance.
- Move `current_*()` and `is_unknown_*()` functions to `detection.py` module.
- Create new `platform_info.py` module for platform-specific info gathering.
- Add `claude.md` documentation file.

## [`7.0.0` (2026-01-18)](https://github.com/kdeldycke/extra-platforms/compare/v6.0.0...v7.0.0)

> [!NOTE]
> `7.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/7.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v7.0.0).

- Add new `ARMV5TEL` architecture.
- Add new `DRAGONFLY_BSD`, `HAIKU` and `ILLUMOS` platforms.
- Add new `ARCH_32_BIT`, `ARCH_64_BIT` and `UNKNOWN` groups.
- Add new detection functions:
  - `is_armv5tel()`
  - `is_dragonfly_bsd()`
  - `is_haiku()`
  - `is_illumos()`
  - `is_arch_32_bit()`
  - `is_arch_64_bit()`
  - `is_unknown()`
- Fix detection of `AARCH64` on Windows ARM runners.
- Rename `UNKNOWN_LINUX` trait to `UNKNOWN_PLATFORM`.
- Remove `UNKNOWN_ARCHITECTURE` trait from `ALL_ARCHITECTURES` group.
- Remove `UNKNOWN_LINUX` trait from `ALL_PLATFORMS` group.
- Remove `UNKNOWN_CI` trait from `ALL_CI` group.
- `current_architecture()`, `current_platform()` and `current_ci()` functions now returns `UNKNOWN_ARCHITECTURE`, `UNKNOWN_PLATFORM` and `UNKNOWN_CI` if detection fails. Add strict mode to raise an exception instead.
- Rename groups:
  - `OTHER_UNIX` → `OTHER_POSIX`
  - `ANY_ARM` → `ALL_ARM`
  - `ANY_MIPS` → `ALL_MIPS`
  - `ANY_SPARC` → `ALL_SPARC`
  - `ANY_WINDOWS` → `ALL_WINDOWS`
- Rename detection functions:
  - `is_other_unix()` → `is_other_posix()`
  - `is_all_architectures()` → `is_any_architecture()`
  - `is_all_platforms()` → `is_any_platform()`
  - `is_all_ci()` → `is_any_ci()`
  - `is_all_traits()` → `is_any_trait()`
  - `is_unknown_linux()` → `is_unknown_platform()`
  - `is_bsd_without_macos()` → `is_bsd_not_macos()`
  - `is_unix_without_macos()` → `is_unix_not_macos()`
- Re-introduce aliases removed in v6.0.0 for backward compatibility:
  - `Group._extract_platforms()` → `Group._extract_members()`
  - `is_all_platforms_without_ci()` → `is_any_platform()`
  - `is_ci()` → `is_any_ci()`
- Rename Pytest decorators:
  - `@skip/@unless_unknown_linux` → `@skip/@unless_unknown_platform`
  - `@skip/@unless_bsd_without_macos` → `@skip/@unless_bsd_not_macos`
  - `@skip/@unless_unix_without_macos` → `@skip/@unless_unix_not_macos`
- Deprecate renamed symbols and detection functions with aliases.
- Pre-compute traits and groups metadata to enforce conventions for data definitions, detection functions, Pytest decorators and document generation.
- Mark all canonical groups with the ⬥ symbol everywhere in the documentation.
- Cross-link all traits, groups and detection functions in the documentation.

## [`6.0.0` (2026-01-02)](https://github.com/kdeldycke/extra-platforms/compare/v5.1.0...v6.0.0)

> [!NOTE]
> `6.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/6.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v6.0.0).

- Add architecture detection: `aarch64`, `arm`, `armv6l`, `armv7l`, `armv8l`, `i386`, `i586`, `i686`, `loongarch64`, `mips`, `mips64`, `mips64el`, `mipsel`, `ppc`, `ppc64`, `ppc64le`, `riscv32`, `riscv64`, `s390x`, `sparc`, `sparc64`, `unknown_architecture`, `wasm32`, `wasm64`, `x86_64`.
- Architectures, platforms and CI systems are now known as *traits*.
- Add new `current_traits()` method to return all traits matching the current environment: architecture, platforms and CI systems. Deprecate `current_platforms()` in favor of it.
- Add new `current_architecture()` and `current_ci()` methods to return the current architecture and CI system.
- Rename:
  - `current_os()` to `current_platform()`.
  - `platforms_from_ids()` to `traits_from_ids()`.
  - `CI` group to `ALL_CI`. `CI` now refers to the `CI(Trait)` class.
  - `ALL_PLATFORM_IDS` constant to `ALL_TRAIT_IDS`.
  - `Group.platforms` to `Group.members`.
  - `Group.platform_ids` to `Group.member_ids`.
  - `Group._extract_platforms()` to `Group._extract_members()`
- `Group.members` is now an immutable `MappingProxyType`.
- Add more in-place operators (`|=`, `&=`, `-=`, `^=`) and set-like behavior to `Group`.
- Add `canonical` attribute to `Group`.
- Add new `ALL_ARCHITECTURES`, `ANY_ARM`, `X86`, `LOONGARCH`, `ANY_MIPS`, `POWERPC`, `RISCV`, `ANY_SPARC`, `IBM_MAINFRAME`, `WEBASSEMBLY` and `ALL_TRAITS` groups.
- Deprecate `ALL_PLATFORMS_WITHOUT_CI` group is favor of `ALL_PLATFORMS`.
- Add new `ALL_ARCHITECTURE_GROUPS`, `ALL_PLATFORM_GROUPS` and `ALL_CI_GROUPS` collections of groups.
- Remove utilization workaround for `macos-15-intel`.
- Replace deprecated `codecov/test-results-action` by `codecov/codecov-action`.
- Move auto-lock time from 8:43 to 4:43.

## [`5.1.0` (2025-12-06)](https://github.com/kdeldycke/extra-platforms/compare/v5.0.1...v5.1.0)

> [!NOTE]
> `5.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/5.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v5.1.0).

- Change Amazon Linux icon.
- Add cooldown period for dependabot and `uv.lock` updates.
- Merge all label jobs into a single one.
- Change the `test`, `typing` and `docs` extra dependency groups into development dependency groups.
- Uncap all dependencies.
- Run tests on Python `3.14t` and `3.15t` free-threaded variants.
- Run tests on `ubuntu-slim` GitHub Actions runner.
- Run docs update job on `ubuntu-slim` runner.
- Unlock a CPU core stuck at 100% utilization on `macos-15-intel`.

## [`5.0.1` (2025-11-15)](https://github.com/kdeldycke/extra-platforms/compare/v5.0.0...v5.0.1)

> [!NOTE]
> `5.0.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/5.0.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v5.0.1).

- Add detection of CachyOS. Closes #341.

## [`5.0.0` (2025-11-03)](https://github.com/kdeldycke/extra-platforms/compare/v4.1.1...v5.0.0)

> [!NOTE]
> `5.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/5.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v5.0.0).

- Relax dependencies to support Python 3.10.
- Re-introduce `tomli` dependency for Python 3.10 users.
- Skip tests on intermediate Python versions (`3.11`, `3.12` and `3.13`) to reduce CI load.

## [`4.1.1` (2025-11-02)](https://github.com/kdeldycke/extra-platforms/compare/v4.1.0...v4.1.1)

> [!NOTE]
> `4.1.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/4.1.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v4.1.1).

- Add detection of Ultramarine Linux. Closes #329.

## [`4.1.0` (2025-10-21)](https://github.com/kdeldycke/extra-platforms/compare/v4.0.0...v4.1.0)

> [!NOTE]
> `4.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/4.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v4.1.0).

- Add new `invalidate_caches()` method to invalidate internal caches used for platform detection.
- Remove dependency on `boltons`.
- Add all `Operating System ::` trove classifiers.
- Add all platform names as package keywords.

## [`4.0.0` (2025-10-21)](https://github.com/kdeldycke/extra-platforms/compare/v3.2.3...v4.0.0)

> [!NOTE]
> `4.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/4.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v4.0.0).

- Fix detection of GNU/Hurd. Closes #308.
- Move all typing-related imports behind a hard-coded `TYPE_CHECKING` guard to avoid runtime imports.
- Remove maximum capped version of all dependencies (relax all `~=` specifiers to `>=`). This gives more freedom to downstream and upstream packagers. Document each minimal version choice.
- Add official support of Python 3.14.
- Run tests on Python 3.15.
- Skip tests on Python 3.12 and 3.13 to reduce CI load.
- Use `astral-sh/setup-uv` action to install `uv` instead of manually installing it with `pip`.
- Run tests on `macos-26` and `macos-15-intel` runners.
- Remove tests on EOL'ed `windows-2019` and `macos-13`.
- Support GitHub admonitions in Sphinx/MyST documentation.

## [`3.2.3` (2025-08-05)](https://github.com/kdeldycke/extra-platforms/compare/v3.2.2...v3.2.3)

> [!NOTE]
> `3.2.3` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.2.3/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.2.3).

- Add detection of macOS Tahoe (v26.x).

## [`3.2.2` (2025-05-24)](https://github.com/kdeldycke/extra-platforms/compare/v3.2.1...v3.2.2)

> [!NOTE]
> `3.2.2` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.2.2/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.2.2).

- Fix detection of `UNKNOWN_CI`.

## [`3.2.1` (2025-05-17)](https://github.com/kdeldycke/extra-platforms/compare/v3.2.0...v3.2.1)

> [!NOTE]
> `3.2.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.2.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.2.1).

- Add convenient `ALL_PLATFORMS_WITHOUT_CI` group to exclude all CI systems from `ALL_PLATFORMS`.

## [`3.2.0` (2025-05-17)](https://github.com/kdeldycke/extra-platforms/compare/v3.1.0...v3.2.0)

> [!NOTE]
> `3.2.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.2.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.2.0).

- Add detection of CI systems: `GITHUB_CI`, `GITLAB_CI` and `UNKNOWN_CI`.
- Add new `CI` group to group all CI platforms.
- Move OS families diagrams to group documentation page.
- Remove `ALL_PLATFORMS` from Sankey diagram.
- Run tests on `windows-11-arm` runners.
- Remove tests on EOL `ubuntu-20-04`.

## [`3.1.0` (2025-03-04)](https://github.com/kdeldycke/extra-platforms/compare/v3.0.0...v3.1.0)

> [!NOTE]
> `3.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.1.0).

- Allow platform ID membership test on groups.
- Add `items()` method to `Group`.
- Allow `None` values in nested references to platforms and groups.
- Keep initial order of data from `platforms_from_ids()` and `groups_from_ids()` results.
- Allow arbitrary arguments number in `Group._extract_platforms()`.

## [`3.0.0` (2025-03-02)](https://github.com/kdeldycke/extra-platforms/compare/v2.1.0...v3.0.0)

> [!NOTE]
> `3.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/3.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v3.0.0).

- Allow set operations to resolve group and Platform IDs.
- Make resolution of platform and group IDs case-insensitive.
- Only runs website tests on Linux to prevent DOSing them.
- Drop supports for Python 3.10.
- Remove `tomli` dependency.

## [`2.1.0` (2025-02-20)](https://github.com/kdeldycke/extra-platforms/compare/v2.0.0...v2.1.0)

> [!NOTE]
> `2.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/2.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v2.1.0).

- Add new `platforms_from_ids` and `groups_from_ids` methods to retrieve platforms and groups from a collection of IDs.
- Allow a platform to be fetched by its ID from a group with the `group[platform_id]` item getter syntax.
- Add new `ALL_PLATFORM_IDS`, `ALL_GROUP_IDS` and `ALL_IDS` constants.
- Removes `ALL_OS_LABELS`.
- Add `windows-2025` to the test matrix.
- Mark Python 3.14 tests as stable.

## [`2.0.0` (2025-01-02)](https://github.com/kdeldycke/extra-platforms/compare/v1.7.0...v2.0.0)

> [!NOTE]
> `2.0.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/2.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v2.0.0).

- Add detection of Nobara.
- Fix `current_os()` to always return a single platform. Closes #158.
- Add new `current_platforms()` method to return all platforms matching the current environment.
- Generate a pair of Pytest `@skip_<id>`/`@unless_<id>` decorators for each platform and group.
- Change all group membership check utilities to be functions instead of variables. You now have to call `is_<group_id>()` instead of `is_<group_id>`.
- Cache the result of `is_<group_id>()` group membership check utilities.
- Do not call all detection heuristics on module import. Instead, call them lazily when needed.
- Make URLs required on all platforms.
- Invite users in error messages and logs to contribute back edge-cases to improve detection heuristics.
- Upload test results to coverage.

## [`1.7.0` (2024-12-03)](https://github.com/kdeldycke/extra-platforms/compare/v1.6.0...v1.7.0)

> [!NOTE]
> `1.7.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.7.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.7.0).

- Display the hierarchy of non-overlapping groups as a mindmap.
- Add URL on all platforms.
- Add detection of openSUSE Tumbleweed. Closes #133.
- Do not allow icons on platforms and groups to be empty.
- Run tests in parallel to speed up CI.

## [`1.6.0` (2024-11-11)](https://github.com/kdeldycke/extra-platforms/compare/v1.5.0...v1.6.0)

> [!NOTE]
> `1.6.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.6.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.6.0).

- Add a new `copy()` method to `Group`.
- New `target_pool` parameter on `reduce` method let you specify the subset of groups to reduce platforms to.
- Remove `CURRENT_OS_ID` and `CURRENT_OS_LABEL`.

## [`1.5.0` (2024-11-10)](https://github.com/kdeldycke/extra-platforms/compare/v1.4.0...v1.5.0)

> [!NOTE]
> `1.5.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.5.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.5.0).

- Allow union, intersection, difference and symmetric difference of `Group`.
- Implements `<=`, `<`, `>=`, `>`, `|`, `&`, `-` and `^` operators for `Group`.
- Deduplicate platforms on `Group` instantiation.
- Allow testing for membership of individual platform in `Group`.

## [`1.4.0` (2024-10-27)](https://github.com/kdeldycke/extra-platforms/compare/v1.3.1...v1.4.0)

> [!NOTE]
> `1.4.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.4.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.4.0).

- Allow set comparison between groups and single platform.
- Add detection of Tuxedo OS. Closes #93.
- Add support for Python 3.13.
- Drop supports for Python 3.9.
- Run jobs on `ubuntu-24.04` instead of `ubuntu-22.04`.
- Run tests on `macos-15`. Remove tests on `macos-12`.
- Run tests on Python 3.14-dev.

## [`1.3.1` (2024-09-18)](https://github.com/kdeldycke/extra-platforms/compare/v1.3.0...v1.3.1)

> [!NOTE]
> `1.3.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.3.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.3.1).

- Fix conflicting detection heuristics for Linux distributions. Closes #72.
- Fix fetching of macOS version for releases without build number (like `15.0`).

## [`1.3.0` (2024-09-11)](https://github.com/kdeldycke/extra-platforms/compare/v1.2.1...v1.3.0)

> [!NOTE]
> `1.3.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.3.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.3.0).

- Add detection of all versions of macOS and Windows. Closes #55.
- Drop supports for Python 3.8.
- Add `is_<group_id>` booleans to module root to test the membership of the current platform to that group.
- Rename `ALL_LINUX` group to `LINUX`.
- Rename `ALL_WINDOWS` group to `ANY_WINDOWS`.

## [`1.2.1` (2024-09-04)](https://github.com/kdeldycke/extra-platforms/compare/v1.2.0...v1.2.1)

> [!NOTE]
> `1.2.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.2.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.2.1).

- Fix changelog update.

## [`1.2.0` (2024-08-24)](https://github.com/kdeldycke/extra-platforms/compare/v1.1.1...v1.2.0)

> [!NOTE]
> `1.2.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.2.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.2.0).

- Add new `LINUX_LIKE` family that merge `ALL_LINUX` and `LINUX_LAYERS` groups.

## [`1.1.1` (2024-08-21)](https://github.com/kdeldycke/extra-platforms/compare/v1.1.0...v1.1.1)

> [!NOTE]
> `1.1.1` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.1.1/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.1.1).

- Run tests on `ubuntu-24.04` and `macos-12`.
- Add missing typed marker.

## [`1.1.0` (2024-08-20)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.2...v1.1.0)

> [!NOTE]
> `1.1.0` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.1.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.1.0).

- Add documentation.
- Expose all utilities at root level.
- Split code.

## [`1.0.2` (2024-08-19)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.1...v1.0.2)

> [!NOTE]
> `1.0.2` is available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.0.2/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.0.2).

- Re-release.

## [`1.0.1` (2024-08-19)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.0...v1.0.1)

> [!WARNING]
> `1.0.1` is **not available** on 🐍 PyPI and 🐙 GitHub.

- Add `pytest` utilities.
- Reorganize code.
- Fix tests.

## [`1.0.0` (2024-08-19)](https://github.com/kdeldycke/extra-platforms/compare/90ddb60...v1.0.0)

> [!NOTE]
> `1.0.0` is the *first version* available on [🐍 PyPI](https://pypi.org/project/extra-platforms/1.0.0/) and [🐙 GitHub](https://github.com/kdeldycke/extra-platforms/releases/tag/v1.0.0).

- First version as a stand alone package extracted from `click-extra`.

