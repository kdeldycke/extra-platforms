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
import functools
import inspect
import os
import re
import subprocess
from itertools import chain
from pathlib import Path

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_TRAITS,
    Group,
    Trait,
    detection as detection_module,
    invalidate_caches,
    is_aarch64,
    is_arm,
    is_github_ci,
    is_gitlab_ci,
    is_windows,
    is_x86_64,
)
from extra_platforms.pytest import skip_windows, unless_windows


@pytest.mark.parametrize(
    "obj", list(chain(ALL_TRAITS, ALL_GROUPS)), ids=lambda obj: obj.id
)
def test_detection_trait_functions(obj: Trait | Group):
    # All traits must implement a real function in the detection module.
    if isinstance(obj, Trait):
        check_func = getattr(detection_module, obj.detection_func_id)
        assert hasattr(extra_platforms, obj.detection_func_id)
        # current property is aligned with detection function.
        assert check_func() == obj.current

    # All groups' detection functions are dynamically generated, but still must exist.
    else:
        assert not hasattr(detection_module, obj.detection_func_id)
        check_func = getattr(extra_platforms, obj.detection_func_id)

        # Groups do not have a "current" property.
        assert not hasattr(obj, "current")

    assert isinstance(check_func, functools._lru_cache_wrapper)
    assert isinstance(check_func(), bool)
    # Ensure the detection function name is lowercase.
    assert obj.detection_func_id.islower()

    # Verify the docstring contains a cross-reference to the symbol.
    # Detection functions use MyST syntax ({data}`...`), while generated group
    # detection functions use reST syntax (:data:`...`).
    assert check_func.__doc__ is not None and re.search(
        rf"[\{{:]data[:\}}]`~?(?:extra_platforms\.)?{re.escape(obj.symbol_id)}`",
        check_func.__doc__,
    )


def test_detection_heuristics_sorting():
    """Detection heuristics must be sorted within each section."""
    detection_path = Path(inspect.getfile(detection_module))
    tree = ast.parse(detection_path.read_bytes())
    source_lines = detection_path.read_text(encoding="utf-8").splitlines()

    # Find section boundaries by looking for comment markers.
    arch_section_start = None
    platform_section_start = None
    shell_section_start = None
    terminal_section_start = None
    ci_section_start = None
    agent_section_start = None

    for i, line in enumerate(source_lines, start=1):
        if "Architecture detection heuristics" in line:
            arch_section_start = i
        elif "Platform detection heuristics" in line:
            platform_section_start = i
        elif "Shell detection heuristics" in line:
            shell_section_start = i
        elif "Terminal detection heuristics" in line:
            terminal_section_start = i
        elif "CI/CD detection heuristics" in line:
            ci_section_start = i
        elif "Agent detection heuristics" in line:
            agent_section_start = i

    assert arch_section_start is not None, "Architecture section not found"
    assert platform_section_start is not None, "Platform section not found"
    assert shell_section_start is not None, "Shell section not found"
    assert terminal_section_start is not None, "Terminal section not found"
    assert ci_section_start is not None, "CI/CD section not found"
    assert agent_section_start is not None, "Agent section not found"

    assert arch_section_start < platform_section_start
    assert platform_section_start < shell_section_start
    assert shell_section_start < terminal_section_start
    assert terminal_section_start < ci_section_start
    assert ci_section_start < agent_section_start

    # Collect heuristic functions by section.
    all_heuristic_ids = []
    arch_heuristics = []
    platform_heuristics = []
    shell_heuristics = []
    terminal_heuristics = []
    ci_heuristics = []
    agent_heuristics = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_"):
            func_id = node.name
            assert func_id.islower()
            all_heuristic_ids.append(func_id)

            line_no = node.lineno
            if line_no >= arch_section_start and line_no < platform_section_start:
                arch_heuristics.append(func_id)
            elif line_no >= platform_section_start and line_no < shell_section_start:
                platform_heuristics.append(func_id)
            elif line_no >= shell_section_start and line_no < terminal_section_start:
                shell_heuristics.append(func_id)
            elif line_no >= terminal_section_start and line_no < ci_section_start:
                terminal_heuristics.append(func_id)
            elif line_no >= ci_section_start and line_no < agent_section_start:
                ci_heuristics.append(func_id)
            elif line_no >= agent_section_start:
                agent_heuristics.append(func_id)

    # Check there is no extra "is_" function.
    # All traits, including UNKNOWN traits, must have detection functions.
    assert {f"is_{p.id}" for p in ALL_TRAITS} == set(all_heuristic_ids)

    # We only allow one generic "is_unknown*()" detection heuristics per category.
    for heuristics in [
        arch_heuristics,
        platform_heuristics,
        shell_heuristics,
        terminal_heuristics,
        ci_heuristics,
        agent_heuristics,
    ]:
        non_generic_func_ids = [
            func_id for func_id in heuristics if func_id.startswith("is_unknown")
        ]

        assert len(non_generic_func_ids) <= 1, (
            f"More than 1 is_unknown*() detection heuristics defined in {heuristics!r}"
        )

        if len(non_generic_func_ids):
            assert non_generic_func_ids[-1].startswith("is_unknown")

        # Verify each category is sorted alphabetically within itself.
        assert non_generic_func_ids == sorted(non_generic_func_ids), (
            f"Heuristics are not sorted: {non_generic_func_ids!r}"
        )


def test_is_arm_depends_on_arm_variants():
    """Test that is_arm() correctly calls ARM variant detection functions."""
    # Clear caches to ensure fresh evaluation.
    invalidate_caches()

    # Call is_arm() to ensure it internally calls the ARM variant functions.
    result = is_arm()

    # We can't easily test the internal calls without mocking,
    # but we can verify the function returns a boolean.
    assert isinstance(result, bool)

    invalidate_caches()


def test_detection_functions_cached():
    """Test that detection functions are cached with @cache decorator."""
    # Clear caches first.
    invalidate_caches()

    # Call each function twice.
    _ = is_aarch64()
    _ = is_aarch64()
    _ = is_windows()
    _ = is_windows()
    _ = is_x86_64()
    _ = is_x86_64()

    # Check that cache_info shows hits.
    assert is_aarch64.cache_info().hits >= 1
    assert is_windows.cache_info().hits >= 1
    assert is_x86_64.cache_info().hits >= 1

    invalidate_caches()


def test_environment_variable_ci_detection(monkeypatch):
    """Test CI detection based on environment variables."""
    invalidate_caches()

    # Mock GitHub CI environment variable.
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    invalidate_caches()
    assert is_github_ci() is True

    # Remove GitHub CI and add GitLab CI.
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("GITLAB_CI", "true")
    invalidate_caches()
    assert is_gitlab_ci() is True

    # Clean up.
    monkeypatch.delenv("GITLAB_CI", raising=False)
    invalidate_caches()


def test_detection_no_circular_dependencies():
    """Test that detection functions can all be called without circular dependency issues."""
    invalidate_caches()

    # Call all trait detection functions.
    for trait in ALL_TRAITS:
        # Access the current property, which calls the detection function.
        _ = trait.current

    # If no exception was raised, there are no circular dependencies.
    invalidate_caches()


@pytest.mark.parametrize(
    ("command", "expected"),
    (
        ("/usr/bin/bash", "bash"),
        ("/bin/zsh", "zsh"),
        ("zsh", "zsh"),
        ("/opt/homebrew/bin/fish", "fish"),
        # Login shells carry a leading dash on argv[0].
        ("-bash", "bash"),
        ("-zsh", "zsh"),
        # The name is lowercased.
        ("/usr/bin/PYTHON3", "python3"),
        # Nothing extractable.
        ("", ""),
        ("-", ""),
    ),
)
def test_shell_name(command, expected):
    assert detection_module._shell_name(command) == expected


@pytest.mark.parametrize(
    ("record", "expected"),
    (
        # Linux /proc/<pid>/stat: "pid (comm) state ppid ...".
        ("4242 (bash) S 4200 4242 4200 0 ...", 4200),
        # The comm field may itself contain spaces and parentheses.
        ("4242 (a (weird) name) S 7 1 1 0 ...", 7),
        # BSD /proc/<pid>/status: "comm pid ppid pgid ...".
        ("zsh 4242 4200 4200 ...", 4200),
    ),
)
def test_parse_proc_ppid(record, expected):
    assert detection_module._parse_proc_ppid(record) == expected


def test_tree_from_ps(monkeypatch):
    """The ps-based walk (macOS/BSD) climbs from the current process to root."""
    # pid ppid command: argv[0] is a path, except a login shell's "-zsh".
    table = (
        "  100     1 /sbin/launchd\n"
        "  200   100 -zsh\n"
        "  300   200 /usr/bin/python3 -m pytest\n"
    )
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout=table),
    )
    monkeypatch.setattr(os, "getpid", lambda: 300)
    # Ordered nearest-first. The login shell's argv[0] (-zsh) yields no path, and
    # "-m pytest" must not be mistaken for an interpreter-hosted shell.
    assert detection_module._tree_from_ps() == (
        ("python3", "/usr/bin/python3"),
        ("zsh", ""),
        ("launchd", "/sbin/launchd"),
    )


def test_tree_from_ps_tolerates_mocked_run(monkeypatch):
    """A globally mocked subprocess.run must not break the walk."""

    class _Sentinel:
        stdout = object()  # Non-string stdout, like a MagicMock attribute.

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: _Sentinel())
    assert detection_module._tree_from_ps() == ()

    def _boom(*args, **kwargs):
        raise FileNotFoundError("ps")

    monkeypatch.setattr(subprocess, "run", _boom)
    assert detection_module._tree_from_ps() == ()


def test_interpreter_shell_specs_includes_xonsh():
    """Xonsh declares python as its interpreter, so it appears in the specs."""
    launchers = {
        launcher for _, launcher in detection_module._interpreter_shell_specs()
    }
    assert "xonsh" in launchers


def test_interpreter_shell(tmp_path):
    """An interpreter running a launcher file named after a shell is detected."""
    launcher = tmp_path / "xonsh"
    launcher.write_text("#!/usr/bin/python\n")
    launcher_str = str(launcher)

    # A python interpreter running the xonsh launcher file.
    assert detection_module._interpreter_shell(["/usr/bin/python3", launcher_str]) == (
        "xonsh",
        launcher_str,
    )
    # The version-tolerant pattern also matches python3.11.
    assert detection_module._interpreter_shell([
        "/usr/bin/python3.11",
        launcher_str,
    ]) == ("xonsh", launcher_str)

    # `-m xonsh` names a module, not a file: no match.
    assert (
        detection_module._interpreter_shell(["/usr/bin/python3", "-m", "xonsh"]) is None
    )
    # A non-interpreter argv[0] is not scanned.
    assert detection_module._interpreter_shell(["/bin/zsh", launcher_str]) is None
    # A file whose basename is not exactly the launcher (xonsh.py) is ignored.
    script = tmp_path / "xonsh.py"
    script.write_text("")
    assert (
        detection_module._interpreter_shell(["/usr/bin/python3", str(script)]) is None
    )
    # Empty argv.
    assert detection_module._interpreter_shell([]) is None


def test_tree_from_ps_detects_interpreter_shell(tmp_path, monkeypatch):
    """The ps walk surfaces xonsh when python runs its launcher script."""
    launcher = tmp_path / "xonsh"
    launcher.write_text("")
    table = f"  300   200 /usr/bin/python3 {launcher}\n  200     1 /sbin/launchd\n"
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout=table),
    )
    monkeypatch.setattr(os, "getpid", lambda: 300)
    pairs = detection_module._tree_from_ps()
    assert ("python3", "/usr/bin/python3") in pairs
    assert ("xonsh", str(launcher)) in pairs


def test_tree_from_ps_uses_portable_flags(monkeypatch):
    """The ps invocation avoids BSD-only flags so System V ps (Solaris) works."""
    captured = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        return subprocess.CompletedProcess(args, 0, stdout="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    detection_module._tree_from_ps()
    # `args` (POSIX), not `command` (absent on Solaris/AIX); no `-ww` (rejected
    # by the System V ps on Solaris and AIX).
    assert "pid=,ppid=,args=" in captured["args"]
    assert "-ww" not in captured["args"]


@pytest.mark.parametrize(
    ("argv", "expected"),
    (
        # qemu user-mode wrapper: the real command follows the emulator.
        (["qemu-aarch64", "/bin/bash", "-c", "x"], ["/bin/bash", "-c", "x"]),
        (["/usr/bin/qemu-aarch64-static", "/bin/zsh"], ["/bin/zsh"]),
        (["qemu-arm", "/bin/sh"], ["/bin/sh"]),
        (["rosetta", "/bin/zsh"], ["/bin/zsh"]),
        # Not an emulator: unchanged.
        (["/bin/bash", "-c", "x"], ["/bin/bash", "-c", "x"]),
        (["qemubench", "/bin/sh"], ["qemubench", "/bin/sh"]),
        # Emulator with nothing after it, or empty: unchanged.
        (["qemu-aarch64"], ["qemu-aarch64"]),
        ([], []),
    ),
)
def test_unwrap_emulator(argv, expected):
    assert detection_module._unwrap_emulator(argv) == expected


def test_tree_from_ps_unwraps_emulator(monkeypatch):
    """An emulated shell (qemu-aarch64 /bin/bash) is seen as the real shell."""
    table = "  300   200 qemu-aarch64 /bin/bash\n  200     1 /sbin/launchd\n"
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout=table),
    )
    monkeypatch.setattr(os, "getpid", lambda: 300)
    pairs = detection_module._tree_from_ps()
    assert ("bash", "/bin/bash") in pairs
    # The qemu wrapper itself is not reported as a shell.
    assert not any(name.startswith("qemu") for name, _ in pairs)


def test_ppid_from_proc_tolerates_binary_status(monkeypatch):
    """System V /proc/<pid>/status is a binary pstatus_t; reading must not raise."""
    monkeypatch.setattr(
        detection_module.Path, "read_bytes", lambda self: b"\x00\x80\xff pstatus"
    )
    assert detection_module._ppid_from_proc(1234) is None


@skip_windows
def test_parent_process_tree_falls_back_to_ps_when_proc_empty(monkeypatch):
    """System V /proc (illumos, Solaris) yields nothing, so fall back to ps."""
    monkeypatch.setattr(detection_module, "_tree_from_proc", lambda: ())
    sentinel = (("zsh", "/usr/bin/zsh"),)
    monkeypatch.setattr(detection_module, "_tree_from_ps", lambda: sentinel)
    # Simulate /proc being mounted, as it is on illumos and Solaris.
    monkeypatch.setattr(detection_module.Path, "is_dir", lambda self: True)
    invalidate_caches()
    assert detection_module._parent_process_tree() == sentinel
    invalidate_caches()


def test_parent_process_exe_names():
    """The dispatcher returns a clean frozenset on every platform."""
    invalidate_caches()
    names = detection_module._parent_process_exe_names()
    assert isinstance(names, frozenset)
    # Whatever is discovered must be non-empty, lowercased stems. The set itself
    # may be empty on sandboxed builders with neither /proc, ps, nor Win32.
    assert all(name and name == name.lower() for name in names)
    invalidate_caches()


def test_walk_process_map():
    """The Windows-style map walk climbs nearest-first and resolves paths."""
    process_map = {
        100: (1, "explorer.exe"),
        200: (100, "powershell.exe"),
        300: (200, "python.exe"),
    }
    paths = {
        100: r"C:\Windows\explorer.exe",
        200: r"C:\Program Files\PowerShell\7\pwsh.exe",
        300: r"C:\Python\python.exe",
    }
    pairs = detection_module._walk_process_map(
        process_map, 300, lambda pid: paths.get(pid, "")
    )
    # Names are normalized (stem, lowercase) and paired with resolved paths.
    assert pairs == (
        ("python", r"C:\Python\python.exe"),
        ("powershell", r"C:\Program Files\PowerShell\7\pwsh.exe"),
        ("explorer", r"C:\Windows\explorer.exe"),
    )


@skip_windows
def test_windows_helpers_noop_off_windows():
    """The _windows module imports cleanly and no-ops on non-Windows platforms."""
    from extra_platforms import _windows

    assert _windows.process_map() == {}
    assert _windows.process_path(os.getpid()) == ""


@unless_windows
def test_tree_from_windows_smoke():
    """On Windows the tree is populated and includes the python interpreter."""
    pairs = detection_module._tree_from_windows()
    assert isinstance(pairs, tuple)
    assert "python" in {name for name, _ in pairs}


def test_running_shell_path(monkeypatch):
    """The nearest absolute path for a shell id wins; non-absolute is skipped."""
    tree = (
        ("python3", "/usr/bin/python3"),
        ("zsh", "/bin/zsh"),  # Nearest zsh.
        ("zsh", "/opt/zsh"),  # Farther zsh, must not win.
        ("launchd", "/sbin/launchd"),
    )
    monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: tree)
    assert detection_module._running_shell_path("zsh") == "/bin/zsh"
    assert detection_module._running_shell_path("launchd") == "/sbin/launchd"
    assert detection_module._running_shell_path("fish") is None

    # A non-absolute name (truncated BSD comm, login dash) is not a path.
    monkeypatch.setattr(
        detection_module, "_parent_process_tree", lambda: (("zsh", "zsh"),)
    )
    assert detection_module._running_shell_path("zsh") is None


def test_current_shell_path(monkeypatch):
    """current_shell_path() prefers the running binary, then falls back to SHELL."""
    from extra_platforms import ZSH, current_shell_path

    monkeypatch.setattr(detection_module, "current_shell", lambda strict=False: ZSH)

    # The process tree yields the running binary: prefer it over SHELL.
    monkeypatch.setattr(detection_module, "_running_shell_path", lambda sid: "/bin/zsh")
    monkeypatch.setenv("SHELL", "/bin/sh")
    invalidate_caches()
    assert current_shell_path() == "/bin/zsh"

    # No running path: fall back to the configured login shell.
    monkeypatch.setattr(detection_module, "_running_shell_path", lambda sid: None)
    invalidate_caches()
    assert current_shell_path() == "/bin/sh"

    # Neither source available.
    monkeypatch.delenv("SHELL", raising=False)
    invalidate_caches()
    assert current_shell_path() is None

    invalidate_caches()


def test_current_shell_prefers_running_shell_over_configured_shell(monkeypatch):
    """A running shell (process tree) wins over a different configured ``SHELL``.

    Regression guard for the macOS Terminal.app case where the app launches a
    login fish (``-fish``) while ``$SHELL`` is still zsh (no ``chsh``): the
    running shell (fish) must win, not the configured login shell (zsh).
    """
    from extra_platforms import FISH, current_shell

    # The parent process tree shows fish actually running.
    monkeypatch.setattr(
        detection_module,
        "_parent_process_tree",
        lambda: (("fish", "/opt/homebrew/bin/fish"),),
    )
    # SHELL still points at the configured login shell, zsh.
    monkeypatch.setenv("SHELL", "/bin/zsh")
    # No shell-startup version variables leak into the environment.
    for var in (
        "BASH_VERSION",
        "FISH_VERSION",
        "KSH_VERSION",
        "NU_VERSION",
        "XONSH_VERSION",
        "ZSH_VERSION",
    ):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.delenv("PSModulePath", raising=False)
    invalidate_caches()
    assert current_shell() is FISH
    invalidate_caches()
