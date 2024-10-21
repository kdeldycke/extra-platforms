# Changelog

## [1.4.1 (unreleased)](https://github.com/kdeldycke/extra-platforms/compare/v1.4.0...main)

> [!IMPORTANT]
> This version is not released yet and is under active development.

## [1.4.0 (2024-10-21)](https://github.com/kdeldycke/extra-platforms/compare/v1.3.1...v1.4.0)

- Allow set comparison between groups and single platform.
- Add support for Tuxedo OS detection.
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
