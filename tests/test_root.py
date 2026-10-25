# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import ast
import inspect
import json
import os
import re
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from textwrap import dedent

import pytest

import extra_platforms
from extra_platforms import (
    ALL_AGENTS,
    ALL_ARCHITECTURES,
    ALL_CI,
    ALL_GROUPS,
    ALL_PLATFORMS,
    ALL_SHELLS,
    ALL_TERMINALS,
    ALL_TRAITS,
    POWERSHELL,
    SYSTEM_V,
    UNIX,
    UNKNOWN,
    UNKNOWN_AGENT,
    UNKNOWN_ARCHITECTURE,
    UNKNOWN_CI,
    UNKNOWN_PLATFORM,
    UNKNOWN_SHELL,
    UNKNOWN_TERMINAL,
    WSL1,
    WSL2,
    Shell,
    agent_data as agent_data_module,
    architecture_data as architecture_data_module,
    ci_data as ci_data_module,
    current_agent,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
    current_terminal,
    current_traits,
    detection as detection_module,
    group as group_module,
    group_data as group_data_module,
    invalidate_caches,
    is_any_agent,
    is_any_ci,
    is_any_terminal,
    is_github_ci,
    is_unknown_shell,
    platform_data as platform_data_module,
    shell_data as shell_data_module,
    shell_from_path,
    terminal_data as terminal_data_module,
    trait as trait_module,
)
from extra_platforms._deprecated import DEPRECATED_ALIASES, REMOVAL_VERSION
from extra_platforms.detection import _CATEGORY_ENV_SIGNALS, _unrecognized_message
from extra_platforms.pytest import skip_hermetic_build

from .conftest import github_runner_os

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]


PROJECT_ROOT = Path(__file__).parent.parent
"""The root path of the project."""

PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
"""The path to the ``pyproject.toml`` file."""

PYPROJECT = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
"""The parsed content of the ``pyproject.toml`` file."""


def test_pyproject_keywords():
    """Check that keywords in ``pyproject.toml`` are correct."""
    # Add all platforms and architectures.
    ideal_keywords = [
        p.name
        for p in (
            ALL_TRAITS
            # Remove versioned WSL platforms.
            - WSL1
            - WSL2
            # Remove UNKNOWN_* traits.
            - UNKNOWN
        )
    ]
    # Re-add un-versioned platform names.
    ideal_keywords.append("Windows Subsystem for Linux")
    # Manually add group names that are not platforms per se.
    ideal_keywords.extend((
        UNIX.name.split(" ", 1)[1],
        SYSTEM_V.name,
    ))
    # Manually add extra keywords. AIX, Hurd, Platform and sysinfo mirror GitHub
    # topics: `repomatic lint-repo` warns on a topic missing from the keywords.
    ideal_keywords.extend((
        "Agent detection",
        "AIX",
        "Architecture detection",
        "CI detection",
        "CPU architecture",
        "Distro detection",
        "Hardware detection",
        "Hurd",
        "Linux distribution",
        "multiplatform",
        "OS detection",
        "OS info",
        "Platform",
        "Platform detection",
        "Pytest",
        "Pytest fixtures",
        "Pytest plugin",
        "Shell detection",
        "sysinfo",
        "System information",
        "Terminal detection",
    ))
    # Sort and deduplicate keywords (case-insensitive).
    ideal_keywords = sorted(set(ideal_keywords), key=lambda k: k.lower())

    # Load our keywords from pyproject.toml.
    keywords = PYPROJECT["project"]["keywords"]

    assert keywords == ideal_keywords


@pytest.mark.network
def test_pyproject_classifiers():
    """Check that Trove classifiers in ``pyproject.toml`` are correct."""
    # Import requests lazily so this module still collects when the package is
    # absent. Pytest imports the module to collect it, so a top-level import
    # would break the whole file even when this network test is deselected with
    # -m 'not network'.
    import requests

    # A runner that loses DNS or egress is an environment failure, not a defect
    # in our metadata: skip rather than redden a required matrix cell.
    try:
        response = requests.get(
            "https://pypi.org/pypi?%3Aaction=list_classifiers", timeout=30
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        pytest.skip(f"PyPI classifier list is unreachable: {error}")

    official_classifiers = response.text.splitlines()

    # Load our trove classifiers from pyproject.toml.
    classifiers = PYPROJECT["project"]["classifiers"]

    for classifier in classifiers:
        assert classifier in official_classifiers, (
            f"Classifier '{classifier}' is not an official trove classifier."
        )

    assert len(classifiers) == len(set(classifiers)), (
        "Classifiers must not contain duplicates."
    )

    os_classifiers = [
        c for c in official_classifiers if c.startswith("Operating System :: ")
    ]
    assert {c for c in classifiers if c.startswith("Operating System :: ")} == set(
        os_classifiers
    ), "All Operating System classifiers must be present in our metadata."


def test_module_root_declarations():
    def fetch_module_implements(module) -> set[str]:
        """Fetch all methods, classes and constants implemented locally in a module's file."""
        members = set()
        tree = ast.parse(Path(inspect.getfile(module)).read_bytes())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    # Skip subscript targets like sys.modules["..."] = ...
                    if not isinstance(target, ast.Name):
                        continue
                    # Skip TYPE_CHECKING variable. See _types.py for more details.
                    if target.id == "TYPE_CHECKING":
                        continue
                    members.add(target.id)
            elif isinstance(node, ast.AnnAssign):
                members.add(node.target.id)  # type: ignore[union-attr]
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                members.add(node.name)
        return {m for m in members if not m.startswith("_")}

    agent_data_members = fetch_module_implements(agent_data_module)
    architecture_data_members = fetch_module_implements(architecture_data_module)
    ci_data_members = fetch_module_implements(ci_data_module)
    detection_members = fetch_module_implements(detection_module)
    group_data_members = fetch_module_implements(group_data_module)
    group_members = fetch_module_implements(group_module)
    platform_data_members = fetch_module_implements(platform_data_module)
    root_members = fetch_module_implements(extra_platforms)
    shell_data_members = fetch_module_implements(shell_data_module)
    terminal_data_members = fetch_module_implements(terminal_data_module)
    trait_members = fetch_module_implements(trait_module)
    # Update root members with auto-generated group detection function names.
    root_members.update(g.detection_func_id for g in ALL_GROUPS)

    # Check all members are exposed at the module root.
    tree = ast.parse(Path(inspect.getfile(extra_platforms)).read_bytes())
    extra_platforms_members: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    assert isinstance(node.value, (ast.List, ast.Tuple))
                    extra_platforms_members.extend(
                        element.value
                        for element in node.value.elts
                        if isinstance(element, ast.Constant)
                        and isinstance(element.value, str)
                    )

    # Sorting of __all__ is enforced by ruff (RUF022). Here we only check
    # completeness: every submodule's public members must appear in __all__,
    # and __all__ must contain nothing extra.
    all_members_set = set(extra_platforms_members)

    assert agent_data_members <= all_members_set
    assert architecture_data_members <= all_members_set
    assert ci_data_members <= all_members_set
    assert detection_members <= all_members_set
    assert group_data_members <= all_members_set
    assert group_members <= all_members_set
    assert platform_data_members <= all_members_set
    assert shell_data_members <= all_members_set
    assert terminal_data_members <= all_members_set
    assert trait_members <= all_members_set

    expected_members = (
        detection_members
        | agent_data_members
        | architecture_data_members
        | ci_data_members
        | group_data_members
        | group_members
        | platform_data_members
        | root_members
        | shell_data_members
        | terminal_data_members
        | trait_members
    )
    assert expected_members == all_members_set


# Trait detection (platform, shell, terminal, CI) reads a real runtime
# environment; a hermetic build sandbox (Guix, Nix; HOME=/homeless-shelter)
# detects none of them, so the exact-count assertions cannot hold.
@skip_hermetic_build
def test_current_funcs():
    current_traits_results = current_traits()
    assert ALL_TRAITS.issuperset(current_traits_results)

    # 1 architecture + 1 platform = 2 traits always detected.
    detected_traits = 2
    # Shell is optional: minimal sandboxes (Guix builders, BusyBox-only images)
    # may have no recognizable shell.
    if not is_unknown_shell():
        detected_traits += 1
        # XXX Shells nest: each extra shell backed by a real ancestor process
        # is a legitimate detection alongside the primary shell. A packager
        # running an `osc build` chroot from a fish terminal gets fish in the
        # ancestor tree, above the bash chain rpmbuild runs the tests with.
        ancestor_names = detection_module._parent_process_exe_names()
        extra_shells = {
            shell
            for shell in ALL_SHELLS
            if isinstance(shell, Shell)
            and shell.current
            and not ancestor_names.isdisjoint(shell.executable_names)
        }
        # XXX The configured login shell is detected too when another shell
        # runs the suite, like a Debian package build calling pytest from
        # `/bin/sh` (dash) while SHELL names bash.
        if os.environ.get("SHELL"):
            login_shell = shell_from_path(os.environ["SHELL"])
            if login_shell.current:
                extra_shells.add(login_shell)
        # XXX PSModulePath detects PowerShell wherever it is set: Windows sets it
        # machine-wide, and Azure leaks it into GitHub's Ubuntu runners.
        if "PSModulePath" in os.environ:
            extra_shells.add(POWERSHELL)
        detected_traits += len(extra_shells - {current_shell(), UNKNOWN_SHELL})
    # Terminal is optional: headless/CI environments may not have one.
    if is_any_terminal():
        detected_traits += 1
    # CI is optional: we may not be running in a CI environment.
    if is_any_ci():
        # +1 CI.
        detected_traits += 1
        # XXX GitHub's ubuntu-slim runner is a WSL2 container.
        if is_github_ci() and github_runner_os() == "ubuntu-slim":
            # +1 platform (WSL2).
            detected_traits += 1
    # Agent is optional: we may not be running under an AI agent.
    if is_any_agent():
        detected_traits += 1
    assert len(current_traits_results) == detected_traits

    current_architecture_result = current_architecture()
    assert current_architecture_result in ALL_ARCHITECTURES
    assert current_architecture_result in current_traits_results
    assert current_architecture_result is not UNKNOWN_ARCHITECTURE

    current_platform_result = current_platform()
    assert current_platform_result in ALL_PLATFORMS
    assert current_platform_result in current_traits_results
    assert current_platform_result is not UNKNOWN_PLATFORM

    current_shell_result = current_shell()
    assert current_shell_result in ALL_SHELLS | {UNKNOWN_SHELL}
    if current_shell_result is not UNKNOWN_SHELL:
        assert current_shell_result in current_traits_results

    current_terminal_result = current_terminal()
    assert current_terminal_result in ALL_TERMINALS | {UNKNOWN_TERMINAL}
    if current_terminal_result is not UNKNOWN_TERMINAL:
        assert current_terminal_result in current_traits_results

    current_ci_result = current_ci()
    assert current_ci_result in ALL_CI | {UNKNOWN_CI}
    if current_ci_result is not UNKNOWN_CI:
        assert current_ci_result in current_traits_results

    current_agent_result = current_agent()
    assert current_agent_result in ALL_AGENTS | {UNKNOWN_AGENT}
    if current_agent_result is not UNKNOWN_AGENT:
        assert current_agent_result in current_traits_results


@pytest.mark.parametrize(
    "current_func,all_collection,unknown_constant,trait_type,error_message",
    [
        (
            current_architecture,
            ALL_ARCHITECTURES,
            UNKNOWN_ARCHITECTURE,
            "architecture",
            "Unrecognized architecture",
        ),
        (
            current_platform,
            ALL_PLATFORMS,
            UNKNOWN_PLATFORM,
            "platform",
            "Unrecognized platform",
        ),
        (
            current_shell,
            ALL_SHELLS,
            UNKNOWN_SHELL,
            "shell",
            "Unrecognized shell",
        ),
        (
            current_terminal,
            ALL_TERMINALS,
            UNKNOWN_TERMINAL,
            "terminal",
            "Unrecognized terminal",
        ),
        (
            current_ci,
            ALL_CI,
            UNKNOWN_CI,
            "CI",
            "Unrecognized CI",
        ),
        (
            current_agent,
            ALL_AGENTS,
            UNKNOWN_AGENT,
            "agent",
            "Unrecognized agent",
        ),
    ],
)
def test_current_strict_mode(
    current_func,
    all_collection,
    unknown_constant,
    trait_type,
    error_message,
    monkeypatch,
    fresh_caches,
):
    """Test that ``current_*(strict=True)`` raises an error when unrecognized."""
    # First verify that without mocking, current_* works normally.
    # Skip this check for CI, terminal, agent, and shell since they may
    # legitimately be unknown (minimal sandboxes often have no recognizable
    # shell).
    if trait_type not in ("CI", "terminal", "agent", "shell"):
        invalidate_caches()
        result = current_func()
        assert result in all_collection
        assert result is not unknown_constant

    # Now mock all traits to not match.
    invalidate_caches()
    for trait in all_collection:
        monkeypatch.setattr(type(trait), "current", property(lambda self: False))

    # Without strict mode, we get UNKNOWN_*.
    result = current_func(strict=False)
    assert result is unknown_constant

    # With strict mode, we get a SystemError.
    invalidate_caches()
    with pytest.raises(SystemError, match=error_message):
        current_func(strict=True)


def test_group_membership_funcs():
    for group in ALL_GROUPS:
        assert group.detection_func_id in extra_platforms.__dict__

        func = extra_platforms.__dict__[group.detection_func_id]
        assert getattr(extra_platforms, group.detection_func_id) is func

        assert isinstance(func(), bool)
        assert func() == any(t in group for t in current_traits())

        assert group.symbol_id in func.__doc__


def test_group_detection_type_stubs():
    """Check all is_*() group detection type stubs are defined and sorted."""
    init_file = Path(inspect.getfile(extra_platforms))
    tree = ast.parse(init_file.read_text(encoding="utf-8"))

    # Collect all function definitions in the TYPE_CHECKING block.
    stub_names: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "TYPE_CHECKING"
        ):
            stub_names.extend(
                line.name for line in node.body if isinstance(line, ast.FunctionDef)
            )

    assert len(stub_names), "No group detection type stubs found."
    assert stub_names == sorted(stub_names), (
        "Group detection type stubs not sorted alphabetically."
    )

    expected_stubs = sorted(g.detection_func_id for g in ALL_GROUPS)
    assert stub_names == expected_stubs, (
        f"Group detection type stubs don't match expectations:\n"
        f"- Missing: {set(expected_stubs) - set(stub_names)}\n"
        f"- Extra: {set(stub_names) - set(expected_stubs)}"
    )


def test_invalidate_caches():
    """`invalidate_caches()` empties every cache that detection fills."""
    registry = detection_module._detection_registry
    for func in registry.values():
        func()
    for trait in ALL_TRAITS:
        assert trait.current in (True, False)
    current_traits()

    # Every cached callable of the detection module, and the group detection
    # functions generated at the package root.
    cached = {
        name: func
        for name, func in (*vars(detection_module).items(), *registry.items())
        if callable(func) and hasattr(func, "cache_info")
    }
    assert all(
        func.cache_info().currsize  # type: ignore[attr-defined]
        for func in registry.values()
    )
    assert all("current" in vars(trait) for trait in ALL_TRAITS)

    invalidate_caches()

    assert not [name for name, func in cached.items() if func.cache_info().currsize]
    assert not [trait.id for trait in ALL_TRAITS if "current" in vars(trait)]


@pytest.mark.parametrize(
    ("traits", "current_func", "message"),
    (
        (ALL_ARCHITECTURES, current_architecture, "Multiple architectures match"),
        (ALL_PLATFORMS, current_platform, "Multiple platforms match"),
        (ALL_TERMINALS, current_terminal, "Multiple terminals match"),
        (ALL_CI, current_ci, "Multiple CI systems match"),
        (ALL_AGENTS, current_agent, "Multiple agents match"),
    ),
    ids=("architecture", "platform", "terminal", "ci", "agent"),
)
def test_multiple_traits_match(
    traits, current_func, message, monkeypatch, fresh_caches
):
    """A category whose traits all match at once raises, instead of picking one.

    Shells take their own test: their resolver breaks ties through running
    processes before it gives up.
    """
    # The traits of a category share one class, so this patches all of them.
    monkeypatch.setattr(
        type(next(iter(traits))), "current", property(lambda self: True)
    )
    with pytest.raises(RuntimeError, match=message):
        current_func()


def test_multiple_shells_match(monkeypatch, fresh_caches):
    """Test RuntimeError when multiple shells match."""
    # Mock detection functions in the registry (where Trait.current looks
    # them up) so exactly BASH and FISH match. Disable cached signal helpers
    # so the disambiguation fast paths do not short-circuit.
    registry = detection_module._detection_registry
    for shell in ALL_SHELLS:
        func_name = f"is_{shell.id}"
        should_match = shell.id in ("bash", "fish")
        monkeypatch.setitem(registry, func_name, lambda m=should_match: m)
    monkeypatch.setattr(detection_module, "_active_env_var_shell_ids", frozenset)
    monkeypatch.setattr(detection_module, "_resolved_shell_id", lambda: None)
    monkeypatch.setattr(detection_module, "_parent_process_exe_names", frozenset)

    with pytest.raises(RuntimeError, match="Multiple shells match"):
        current_shell()


def test_unrecognized_message_format():
    """Test that _unrecognized_message contains expected fields."""
    # Default (report=True) includes the GitHub issue URL.
    message_with_report = _unrecognized_message()
    assert "github.com/kdeldycke/extra-platforms/issues" in message_with_report

    # Without report request (for legitimately absent traits like terminal/CI).
    message_without_report = _unrecognized_message(report=False)
    assert "github.com/kdeldycke/extra-platforms/issues" not in message_without_report

    # Both contain the environment dump primitives.
    for message in (message_with_report, message_without_report):
        assert "sys.platform:" in message
        assert "platform.platform:" in message
        assert "platform.release:" in message
        assert "platform.uname:" in message
        assert "platform.machine:" in message
        assert "platform.architecture:" in message
        assert "os_release_id:" in message


@pytest.mark.parametrize(
    ("category", "gating_var"),
    (
        ("terminal", "TERM"),
        ("CI", "CI"),
        ("agent", "LLM"),
    ),
)
def test_category_env_signals_gating_var(category, gating_var):
    """The primary signal of each env-gated category is its ``expected=`` gate var."""
    assert _CATEGORY_ENV_SIGNALS[category][0] == gating_var


def test_shell_env_signals_cover_version_vars():
    """Every shell startup variable in the registry is reported on a shell miss."""
    version_vars = {
        env_var
        for shell in ALL_SHELLS
        if (env_var := getattr(shell, "version_env_var", None))
    }
    assert version_vars <= set(_CATEGORY_ENV_SIGNALS["shell"])


@pytest.mark.parametrize("category", ("shell", "terminal", "CI", "agent"))
def test_unrecognized_message_reports_set_category_vars(monkeypatch, category):
    """A set category variable, and its value, appear in that category's report."""
    primary_var = _CATEGORY_ENV_SIGNALS[category][0]
    monkeypatch.setenv(primary_var, "sentinel-value")
    message = _unrecognized_message(category=category)
    assert f"{primary_var}:" in message
    assert "sentinel-value" in message


def test_unrecognized_message_hides_unset_secondary_vars(monkeypatch):
    """Unset non-primary category variables are omitted, keeping the report concise."""
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    message = _unrecognized_message(category="terminal")
    assert "TERM_PROGRAM:" not in message


def test_unrecognized_message_without_category_omits_env_block(monkeypatch):
    """Architecture and platform reports carry only the system primitives."""
    monkeypatch.setenv("TERM", "xterm-256color")
    message = _unrecognized_message(category="platform")
    assert "TERM:" not in message
    assert "os_release_id:" in message


@pytest.mark.skipif(
    sys.version_info < (3, 14), reason="platform.invalidate_caches added in Python 3.14"
)
def test_invalidate_caches_python_314(monkeypatch):
    """Test that invalidate_caches calls platform.invalidate_caches on Python 3.14+."""
    import platform as stdlib_platform

    # Track if the original or mock was called.
    called = []

    def mock_invalidate():
        called.append(True)

    # Always set the mock to track calls.
    monkeypatch.setattr(stdlib_platform, "invalidate_caches", mock_invalidate)

    invalidate_caches()

    # On Python 3.14+, platform.invalidate_caches should be called.
    assert len(called) > 0, "platform.invalidate_caches was not called"


@pytest.mark.benchmark
def test_import_time():
    """Guard against import time regressions.

    Spawns fresh subprocesses to measure cold import time, avoiding
    ``sys.modules`` cache effects from pytest's own imports.

    Asserts on the fastest of several samples. One sample on a shared CI runner
    measures that runner's worst moment rather than the code: the budget was
    doubled from 1000 ms to 2000 ms in the 13.3.0 cycle after macos-15-intel
    measured ~1088 ms on py3.14 with no code-level regression, and that same
    runner still reached 2236 ms on a single sample afterwards. Sampling
    targets the variance instead, because a real regression slows every sample
    while a scheduling stall slows one.

    The 2000 ms budget stays deliberately loose to absorb slower architectures
    (on i586 cold import measured ~340 ms in 11.x and ~613 ms in 12.0.0),
    against a local cold import of ~22 ms. This will not catch small drifts,
    but reliably prevents reintroducing expensive import-time operations (like
    the ~120 ms regression from redundant AST parsing that was fixed by
    caching in ``_docstrings.py``).

    Carries the ``benchmark`` marker because no budget can hold on every
    machine: an emulated architecture fails it with no code regression, as
    Alpine's loongarch64 builder did at 2176 ms. A distribution build excludes
    the class with ``-m "not benchmark"`` rather than deselecting this node by
    name.
    """
    timings = []
    for _ in range(3):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import time; t = time.perf_counter(); "
                    "import extra_platforms; print(time.perf_counter() - t)"
                ),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        timings.append(float(result.stdout.strip()) * 1000)

    elapsed_ms = min(timings)
    samples = ", ".join(f"{t:.1f}" for t in timings)
    assert elapsed_ms < 2000, (
        f"Fastest of {len(timings)} cold imports took {elapsed_ms:.1f} ms, "
        f"expected < 2000 ms (samples: {samples} ms)."
    )


@pytest.mark.parametrize(
    "flags",
    (
        pytest.param((), id="default"),
        # -OO strips every class docstring, and @dataclass then writes the
        # signature of the class in its place.
        pytest.param(("-OO",), id="no_docstrings"),
    ),
)
def test_docstrings_are_generated_on_first_read(flags):
    """Importing the package generates no docstring: the first read does.

    Runs in a fresh interpreter, because an earlier test of the session may
    have read a docstring already. The interpreter flags do not change the
    result: a generated docstring does not depend on the class docstring.
    """
    script = dedent(
        """\
        import json

        from extra_platforms import ALL_GROUPS, ALL_TRAITS, UBUNTU, _docstrings


        def state():
            return {
                "parsed_modules": sorted(_docstrings._module_docstrings_cache),
                "documented": sorted(
                    item.id
                    for item in (*ALL_TRAITS, *ALL_GROUPS)
                    if "__doc__" in vars(item)
                ),
            }


        at_import = state()
        _ = UBUNTU.__doc__
        print(json.dumps([at_import, state()]))
        """
    )
    result = subprocess.run(
        [sys.executable, *flags, "-c", script],
        capture_output=True,
        text=True,
        encoding="UTF-8",
        check=True,
    )
    at_import, after_read = json.loads(result.stdout)

    assert at_import == {"parsed_modules": [], "documented": []}
    assert after_read == {
        "parsed_modules": ["extra_platforms.platform_data"],
        "documented": ["ubuntu"],
    }


def test_subprocess_and_shutil_are_not_imported_at_module_level():
    """No module of the package imports `subprocess` or `shutil` when it loads.

    Both serve only the detection paths that spawn a process, which import them
    in the function body. The check reads the source, because `sys.modules`
    cannot tell: on Python 3.10 the standard library `platform` module imports
    `subprocess` itself.
    """
    offenders = []
    package_dir = Path(inspect.getfile(extra_platforms)).parent
    for path in package_dir.rglob("*.py"):
        pending: list[ast.AST] = [ast.parse(path.read_bytes())]
        while pending:
            node = pending.pop()
            # A function body runs when the function is called.
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            # The body of a TYPE_CHECKING block never runs. Its else branch does.
            if (
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Name)
                and node.test.id == "TYPE_CHECKING"
            ):
                pending.extend(node.orelse)
                continue
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imported = {alias.name for alias in node.names}
                else:
                    # A relative import names a module of the package.
                    imported = set() if node.level else {node.module or ""}
                if imported & {"shutil", "subprocess"}:
                    module = path.relative_to(package_dir).as_posix()
                    offenders.append(f"{module}:{node.lineno}")
            pending.extend(ast.iter_child_nodes(node))

    assert not offenders, (
        "subprocess or shutil imported at module level in "
        + ", ".join(sorted(offenders))
    )


# Registry-derived: every alias in DEPRECATED_ALIASES gets a case, so a new entry
# cannot slip in without test coverage.
@pytest.mark.parametrize(
    ("module_id", "deprecated_id", "replacement_id"),
    [
        (module_id, deprecated_id, replacement_id)
        for module_id, aliases in sorted(DEPRECATED_ALIASES.items())
        for deprecated_id, replacement_id in sorted(aliases.items())
    ],
)
def test_deprecated_aliases(module_id, deprecated_id, replacement_id):
    """A deprecated alias resolves to its replacement, with a warning at the caller.

    The alias stays out of the advertised API, unlike its replacement.
    """
    module = import_module(module_id)
    with pytest.deprecated_call(
        match=f"{re.escape(deprecated_id)} is deprecated and will be removed in "
        f"extra-platforms {re.escape(REMOVAL_VERSION)}, "
        f"use {re.escape(replacement_id)} instead."
    ) as record:
        assert getattr(module, deprecated_id) is getattr(module, replacement_id)
    assert record[0].filename == __file__

    advertised = getattr(module, "__all__", ())
    assert deprecated_id not in advertised
    if advertised:
        assert replacement_id in advertised


@pytest.mark.parametrize("module_id", sorted(DEPRECATED_ALIASES))
def test_unknown_attribute(module_id):
    """An unknown attribute still raises a standard AttributeError."""
    with pytest.raises(AttributeError, match="has no attribute 'DOES_NOT_EXIST'"):
        _ = import_module(module_id).DOES_NOT_EXIST
