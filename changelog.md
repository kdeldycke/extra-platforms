# Changelog

## [3.1.1 (unreleased)](https://github.com/kdeldycke/extra-platforms/compare/v3.1.0...main)

> [!IMPORTANT]
> This version is not released yet and is under active development.

- Move OS families diagrams to group documentation page.
- Remove `ALL_PLATFORMS` from Sankey diagram.
- Run tests on `windows-11-arm` runners.

## [3.1.0 (2025-03-04)](https://github.com/kdeldycke/extra-platforms/compare/v3.0.0...v3.1.0)

- Allow platform ID membership test on groups.
- Add `items()` method to `Group`.
- Allow `None` values in nested references to platforms and groups.
- Keep initial order of data from `platforms_from_ids()` and `groups_from_ids()` results.
- Allow arbitrary arguments number in `Group._extract_platforms()`.

## [3.0.0 (2025-03-02)](https://github.com/kdeldycke/extra-platforms/compare/v2.1.0...v3.0.0)

- Allow set operations to resolve group and Platform IDs.
- Make resolution of platform and group IDs case-insensitive.
- Only runs website tests on Linux to prevent DOSing them.
- Drop supports for Python 3.10.
- Remove `tomli` dependency.

## [2.1.0 (2025-02-20)](https://github.com/kdeldycke/extra-platforms/compare/v2.0.0...v2.1.0)

- Add new `platforms_from_ids` and `groups_from_ids` methods to retrieve platforms and groups from a collection of IDs.
- Allow a platform to be fetched by its ID from a group with the `group[platform_id]` item getter syntax.
- Add new `ALL_PLATFORM_IDS`, `ALL_GROUP_IDS` and `ALL_IDS` constants.
- Removes `ALL_OS_LABELS`.
- Add `windows-2025` to the test matrix.
- Mark Python 3.14 tests as stable.

## [2.0.0 (2024-12-27)](https://github.com/kdeldycke/extra-platforms/compare/v1.7.0...v2.0.0)

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

## [1.7.0 (2024-12-02)](https://github.com/kdeldycke/extra-platforms/compare/v1.6.0...v1.7.0)

- Display the hierarchy of non-overlapping groups as a mindmap.
- Add URL on all platforms.
- Add detection of openSUSE Tumbleweed. Closes #133.
- Do not allow icons on platforms and groups to be empty.
- Run tests in parallel to speed up CI.

## [1.6.0 (2024-11-11)](https://github.com/kdeldycke/extra-platforms/compare/v1.5.0...v1.6.0)

- Add a new `copy()` method to `Group`.
- New `target_pool` parameter on `reduce` method let you specify the subset of groups to reduce platforms to.
- Remove `CURRENT_OS_ID` and `CURRENT_OS_LABEL`.

## [1.5.0 (2024-11-10)](https://github.com/kdeldycke/extra-platforms/compare/v1.4.0...v1.5.0)

- Allow union, intersection, difference and symmetric difference of `Group`.
- Implements `<=`, `<`, `>=`, `>`, `|`, `&`, `-` and `^` operators for `Group`.
- Deduplicate platforms on `Group` instantiation.
- Allow testing for membership of individual platform in `Group`.

## [1.4.0 (2024-10-21)](https://github.com/kdeldycke/extra-platforms/compare/v1.3.1...v1.4.0)

- Allow set comparison between groups and single platform.
- Add detection of Tuxedo OS. Closes #93.
- Add support for Python 3.13.
- Drop supports for Python 3.9.
- Run jobs on `ubuntu-24.04` instead of `ubuntu-22.04`.
- Run tests on `macos-15`. Remove tests on `macos-12`.
- Run tests on Python 3.14-dev.

## [1.3.1 (2024-09-18)](https://github.com/kdeldycke/extra-platforms/compare/v1.3.0...v1.3.1)

- Fix conflicting detection heuristics for Linux distributions. Closes #72.
- Fix fetching of macOS version for releases without build number (like `15.0`).

## [1.3.0 (2024-09-11)](https://github.com/kdeldycke/extra-platforms/compare/v1.2.1...v1.3.0)

- Add detection of all versions of macOS and Windows. Closes #55.
- Drop supports for Python 3.8.
- Add `is_<group_id>` booleans to module root to test the membership of the current platform to that group.
- Rename `ALL_LINUX` group to `LINUX`.
- Rename `ALL_WINDOWS` group to `ANY_WINDOWS`.

## [1.2.1 (2024-09-04)](https://github.com/kdeldycke/extra-platforms/compare/v1.2.0...v1.2.1)

- Fix changelog update.

## [1.2.0 (2024-08-24)](https://github.com/kdeldycke/extra-platforms/compare/v1.1.1...v1.2.0)

- Add new `LINUX_LIKE` family that merge `ALL_LINUX` and `LINUX_LAYERS` groups.

## [1.1.1 (2024-08-21)](https://github.com/kdeldycke/extra-platforms/compare/v1.1.0...v1.1.1)

- Run tests on `ubuntu-24.04` and `macos-12`.
- Add missing typed marker.

## [1.1.0 (2024-08-20)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.2...v1.1.0)

- Add documentation.
- Expose all utilities at root level.
- Split code.

## [1.0.2 (2024-08-19)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.1...v1.0.2)

- Re-release.

## [1.0.1 (2024-08-19)](https://github.com/kdeldycke/extra-platforms/compare/v1.0.0...v1.0.1)

- Add `pytest` utilities.
- Reorganize code.
- Fix tests.

## [1.0.0 (2024-08-18)](https://github.com/kdeldycke/extra-platforms/compare/90ddb60...v1.0.0)

- First version as a stand alone package extracted from `click-extra`.
