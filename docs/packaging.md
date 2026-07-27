# Downstream packaging

This page is for distribution packagers building `extra-platforms` from source, either a PyPI sdist or a Git tag. To install it on your own system, use `pip install extra-platforms` or your distribution's package.

## Building

The wheel is built with [`uv_build`](https://docs.astral.sh/uv/), declared as the `[build-system]` backend. Distributions that do not yet package `uv-build` can fall back to `setuptools`: `extra-platforms` is a pure-Python, single-package project, so `setuptools.build_meta` builds it with no extra configuration (setuptools' own defaults exclude `tests/` and `docs/` from package discovery).

## Test suite

Since `extra-platforms` > `13.3.1`, the PyPI sdist ships `tests/` and `docs/`, so the suite runs straight from the sdist. Earlier releases shipped no tests; those builds must start from [a Git tag tarball](https://github.com/kdeldycke/extra-platforms/tags) instead.

A plain `pytest` run is friendly to a hermetic build sandbox:

- **No coverage or xdist plugins are required.** Coverage (`--cov`) and parallelism (`--numprocesses`, `--dist`) are passed by the project's own CI workflow, not baked into `addopts`, so a from-source build needs neither `pytest-cov` nor `pytest-xdist` just to start pytest.
- **Network tests are marked.** Exclude them with `-m "not network"`: the build sandbox has no outbound network.
- **Environment-detection tests self-skip in hermetic builds.** `test_platform_detection` and `test_current_funcs` read a real runtime environment (OS-release files, a shell, a terminal, a CI system) that a build sandbox does not provide, so they carry `@skip_hermetic_build`. That decorator fires whenever `HOME=/homeless-shelter`: the non-existent home directory Nix pioneered and GNU Guix inherited to seal a build off from the host.
- **The Sphinx cross-reference test needs `uv`.** `tests/test_sphinx_crossrefs.py` shells out to `uv run sphinx-build`, so it skips automatically when `uv` is not on `PATH`.

The recommended invocation for a hermetic builder is therefore just:

```{code-block} shell-session
$ pytest -m "not network"
```

No per-module ignore list is needed, and the selection stays correct as tests are added.

## Test helpers for downstream projects

The `extra_platforms.pytest` module (installed with the `[pytest]` extra) exposes utilities that other packages' test suites reuse:

- `@skip_<trait>` / `@unless_<trait>` decorators for every detected platform, architecture, shell, terminal, CI system and agent, including `@skip_hermetic_build` for tests that cannot run in a `HOME=/homeless-shelter` build sandbox.
- `write_fake_executable(path, *, stdout="", stderr="", returncode=0)` writes a portable fake command under a Python shebang (not `#!/bin/sh`), so a stand-in CLI a test drives through a real subprocess still execs in a sandbox that ships no `/bin/sh`.
