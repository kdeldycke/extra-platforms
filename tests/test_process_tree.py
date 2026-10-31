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
"""Test the walk of the parent process tree."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from extra_platforms import (
    NUSHELL,
    POWERSHELL,
    _process_tree,
    _windows,
    invalidate_caches,
)
from extra_platforms.pytest import skip_windows, unless_windows


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
    assert _process_tree._shell_name(command) == expected


@pytest.mark.parametrize(
    ("record", "expected"),
    (
        # Linux /proc/<pid>/stat: "pid (comm) state ppid ...".
        ("4242 (bash) S 4200 4242 4200 0 ...", 4200),
        # The comm field may itself contain spaces and parentheses.
        ("4242 (a (weird) name) S 7 1 1 0 ...", 7),
        # BSD /proc/<pid>/status: "comm pid ppid pgid ...".
        ("zsh 4242 4200 4200 ...", 4200),
        # NetBSD /proc/<pid>/stat (Linux-compat format from
        # sys/miscfs/procfs/procfs_linux.c). Confirmed in
        # https://github.com/sarugaku/shellingham/issues/99 where shellingham's
        # Linux-style /proc parsing fails but extra-platforms detects ksh.
        (
            (
                "1500 (ksh) S 1 1500 1500 1280 1500 0 0 0 0 0 50 100 0 0 "
                "20 0 1 0 1234567 4194304 512 18446744073709551615 0 0 0 0 0 "
                "0 0 0 0 0 0 0 0 0 0 0 0 0"
            ),
            1,
        ),
        # NetBSD /proc/<pid>/status (BSD format from procfs_status.c):
        # "comm pid ppid pgid sid tdev,minor flags,flags start,ns ...".
        ("ksh 1500 1 1500 1500 -1,-1 noflags,noflags 1234567,890 - 1000", 1),
    ),
)
def test_parse_proc_ppid(record, expected):
    assert _process_tree._parse_proc_ppid(record) == expected


def _mock_ps(monkeypatch, table: str, links: dict[int, str] | None = None) -> None:
    """Serve ``table`` as the output of ``ps``, seen from process 300.

    ``links`` stands in for the System V procfs link to the binary of each PID.
    Every process gets one, empty by default, so the real procfs of an illumos
    host stays out of these made-up processes.
    """
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout=table),
    )
    monkeypatch.setattr(os, "getpid", lambda: 300)
    monkeypatch.setattr(
        _process_tree, "_system_v_executable", lambda pid: (links or {}).get(pid, "")
    )


@pytest.mark.parametrize(
    ("table", "links", "expected"),
    (
        pytest.param(
            # pid ppid command: argv[0] is a path, except a login shell's "-zsh".
            "  100     1 /sbin/launchd\n"
            "  200   100 -zsh\n"
            "  300   200 /usr/bin/python3 -m pytest\n",
            None,
            # The login shell's argv[0] yields no path, and "-m pytest" must not
            # be mistaken for an interpreter-hosted shell.
            (
                ("python3", "/usr/bin/python3"),
                ("zsh", ""),
                ("launchd", "/sbin/launchd"),
            ),
            id="login_shell",
        ),
        pytest.param(
            # System V procfs names the binary a bare argv[0] hides, as on illumos.
            "  100     1 /usr/lib/ssh/sshd\n"
            "  200   100 sh probe.sh\n"
            "  300   200 /usr/bin/python3.14 report.py\n",
            {200: "/usr/bin/i86/ksh93", 300: "/usr/bin/python3.14"},
            (
                ("python3", "/usr/bin/python3.14"),
                ("python3", "/usr/bin/python3.14"),
                ("ksh93", "/usr/bin/i86/ksh93"),
                ("sh", ""),
                ("sshd", "/usr/lib/ssh/sshd"),
            ),
            id="system_v_executable",
        ),
        pytest.param(
            # An emulated shell is seen as the real one, and its qemu wrapper is
            # no process of its own.
            "  300   200 qemu-aarch64 /bin/bash\n  200     1 /sbin/launchd\n",
            None,
            (("bash", "/bin/bash"), ("launchd", "/sbin/launchd")),
            id="emulated_shell",
        ),
    ),
)
def test_tree_from_ps(table, links, expected, monkeypatch):
    """The ps-based walk (macOS/BSD) climbs from the current process to root.

    The pairs come nearest-first.
    """
    _mock_ps(monkeypatch, table, links)
    assert _process_tree._tree_from_ps() == expected


def test_tree_from_ps_tolerates_mocked_run(monkeypatch):
    """A globally mocked subprocess.run must not break the walk."""

    class _Sentinel:
        stdout = object()  # Non-string stdout, like a MagicMock attribute.

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: _Sentinel())
    assert _process_tree._tree_from_ps() == ()

    def _boom(*args, **kwargs):
        raise FileNotFoundError("ps")

    monkeypatch.setattr(subprocess, "run", _boom)
    assert _process_tree._tree_from_ps() == ()


def test_interpreter_shell_specs_includes_xonsh():
    """Xonsh declares python as its interpreter, so it appears in the specs."""
    launchers = {launcher for _, launcher in _process_tree._interpreter_shell_specs()}
    assert "xonsh" in launchers


def test_interpreter_shell(tmp_path):
    """An interpreter running a launcher file named after a shell is detected."""
    launcher = tmp_path / "xonsh"
    launcher.write_text("#!/usr/bin/python\n")
    launcher_str = str(launcher)

    # A python interpreter running the xonsh launcher file.
    assert _process_tree._interpreter_shell(["/usr/bin/python3", launcher_str]) == (
        "xonsh",
        launcher_str,
    )
    # The version-tolerant pattern also matches python3.11.
    assert _process_tree._interpreter_shell([
        "/usr/bin/python3.11",
        launcher_str,
    ]) == ("xonsh", launcher_str)

    # `-m xonsh` names a module, not a file: no match.
    assert _process_tree._interpreter_shell(["/usr/bin/python3", "-m", "xonsh"]) is None
    # A non-interpreter argv[0] is not scanned.
    assert _process_tree._interpreter_shell(["/bin/zsh", launcher_str]) is None
    # A file whose basename is not exactly the launcher (xonsh.py) is ignored.
    script = tmp_path / "xonsh.py"
    script.write_text("")
    assert _process_tree._interpreter_shell(["/usr/bin/python3", str(script)]) is None
    # Empty argv.
    assert _process_tree._interpreter_shell([]) is None


def test_tree_from_ps_detects_interpreter_shell(tmp_path, monkeypatch):
    """The ps walk surfaces xonsh when python runs its launcher script."""
    launcher = tmp_path / "xonsh"
    launcher.write_text("", encoding="UTF-8")
    _mock_ps(
        monkeypatch,
        f"  300   200 /usr/bin/python3 {launcher}\n  200     1 /sbin/launchd\n",
    )
    assert _process_tree._tree_from_ps() == (
        ("python3", "/usr/bin/python3"),
        ("xonsh", str(launcher)),
        ("launchd", "/sbin/launchd"),
    )


def test_tree_from_ps_uses_portable_flags(monkeypatch):
    """The ps invocation avoids BSD-only flags so System V ps (Solaris) works."""
    captured = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        return subprocess.CompletedProcess(args, 0, stdout="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    _process_tree._tree_from_ps()
    # `args` (POSIX), not `command` (absent on Solaris/AIX); no `-ww` (rejected
    # by the System V ps on Solaris and AIX). One `-o` per field: FreeBSD reads
    # `-o pid=,ppid=,args=` as a single `pid` column with a `,ppid=,args=` header.
    assert captured["args"] == ("ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "args=")


@skip_windows
def test_tree_from_ps_replaces_undecodable_bytes(tmp_path, monkeypatch):
    """A byte that is no UTF-8, in the arguments of another process, is replaced.

    The fake `ps` lists the current process, and a second one whose argument is
    a Latin-1 `piña`.
    """
    ps = tmp_path / "ps"
    # A Python shebang, not /bin/sh, as for write_fake_executable(). -S skips the
    # site module and the coverage hook it loads: their start-up can outlast the
    # timeout of the `ps` call on a busy runner.
    ps.write_text(
        f"#!{sys.executable} -S\n"
        "import sys\n"
        "sys.stdout.buffer.write(\n"
        "    b'  300     1 /bin/zsh\\n  400     1 /usr/bin/python3 pi\\xf1a\\n'\n"
        ")\n",
        encoding="UTF-8",
    )
    ps.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)
    monkeypatch.setattr(os, "getpid", lambda: 300)
    monkeypatch.setattr(_process_tree, "_system_v_executable", lambda pid: "")
    assert _process_tree._tree_from_ps() == (("zsh", "/bin/zsh"),)


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
    assert _process_tree._unwrap_emulator(argv) == expected


@pytest.mark.parametrize(
    ("executable", "argv", "expected"),
    (
        # BusyBox called by its own name runs the applet its argument names.
        ("", ["/usr/bin/busybox", "sh", "-c", "x"], [("ash", "")]),
        ("", ["busybox", "ash"], [("ash", "")]),
        ("", ["busybox", "hush", "-c", "x"], [("hush", "")]),
        # BusyBox called through a link, as its resolved executable reveals.
        (
            "/bin/busybox",
            ["/bin/sh", "script.sh"],
            [("busybox", "/bin/busybox"), ("ash", "/bin/sh")],
        ),
        ("/bin/busybox", ["-sh"], [("busybox", "/bin/busybox"), ("ash", "")]),
        # Any other sh keeps its name.
        (
            "/usr/bin/dash",
            ["/bin/sh", "script.sh"],
            [("dash", "/usr/bin/dash"), ("sh", "/bin/sh")],
        ),
    ),
)
def test_pairs_from_process_busybox(executable, argv, expected):
    """BusyBox's sh and ash applets both run its Almquist shell."""
    assert _process_tree._pairs_from_process(executable, argv) == expected


def test_ppid_from_proc_tolerates_binary_status(monkeypatch):
    """System V /proc/<pid>/status is a binary pstatus_t; reading must not raise."""
    monkeypatch.setattr(
        _process_tree.Path, "read_bytes", lambda self: b"\x00\x80\xff pstatus"
    )
    assert _process_tree._ppid_from_proc(1234) is None


def test_ppid_from_proc_netbsd_stat(monkeypatch):
    """NetBSD /proc/<pid>/stat is Linux-compatible: ksh detected as parent.

    Regression test for the scenario in
    https://github.com/sarugaku/shellingham/issues/99 where shellingham fails
    on NetBSD's procfs but extra-platforms walks it correctly.
    """
    netbsd_stat = (
        b"1500 (ksh) S 1 1500 1500 1280 1500 0 0 0 0 0 50 100 0 0 "
        b"20 0 1 0 1234567 4194304 512 18446744073709551615 0 0 0 0 0 "
        b"0 0 0 0 0 0 0 0 0 0 0 0 0"
    )
    monkeypatch.setattr(_process_tree.Path, "read_bytes", lambda self: netbsd_stat)
    assert _process_tree._ppid_from_proc(1500) == 1


def test_ppid_from_proc_netbsd_status_fallback(monkeypatch):
    """When NetBSD's stat is unreadable, the BSD-style status fallback parses."""
    netbsd_status = b"ksh 1500 1 1500 1500 -1,-1 noflags,noflags 1234567,890 - 1000"

    def read_bytes(self):
        # Mimic a NetBSD /proc with only `status` readable (stat denied).
        if self.name == "stat":
            raise OSError("stat unreadable")
        return netbsd_status

    monkeypatch.setattr(_process_tree.Path, "read_bytes", read_bytes)
    assert _process_tree._ppid_from_proc(1500) == 1


@skip_windows
def test_parent_process_tree_falls_back_to_ps_when_proc_empty(
    monkeypatch, fresh_caches
):
    """System V /proc (illumos, Solaris) yields nothing, so fall back to ps."""
    monkeypatch.setattr(_process_tree, "_tree_from_proc", lambda: ())
    sentinel = (("zsh", "/usr/bin/zsh"),)
    monkeypatch.setattr(_process_tree, "_tree_from_ps", lambda: sentinel)
    # Simulate /proc being mounted, as it is on illumos and Solaris.
    monkeypatch.setattr(_process_tree.Path, "is_dir", lambda self: True)
    invalidate_caches()
    assert _process_tree.parent_process_tree() == sentinel


def test_parent_process_names(fresh_caches):
    """The dispatcher returns a clean frozenset on every platform."""
    names = _process_tree.parent_process_names()
    assert isinstance(names, frozenset)
    # Whatever is discovered must be non-empty, lowercased stems. The set itself
    # may be empty on sandboxed builders with neither /proc, ps, nor Win32.
    assert all(name and name == name.lower() for name in names)


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
    pairs = _process_tree._walk_process_map(
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
    assert _windows.process_map() == {}
    assert _windows.process_path(os.getpid()) == ""


@unless_windows
def test_tree_from_windows_smoke():
    """On Windows the tree is populated and includes the python interpreter."""
    pairs = _process_tree._tree_from_windows()
    assert isinstance(pairs, tuple)
    assert "python" in {name for name, _ in pairs}


def test_nearest_path(monkeypatch):
    """The nearest absolute path for a shell name wins; non-absolute is skipped."""
    tree = (
        ("python3", "/usr/bin/python3"),
        ("zsh", "/bin/zsh"),  # Nearest zsh.
        ("zsh", "/opt/zsh"),  # Farther zsh, must not win.
        ("launchd", "/sbin/launchd"),
    )
    monkeypatch.setattr(_process_tree, "parent_process_tree", lambda: tree)
    nearest = _process_tree.nearest_path
    assert nearest(frozenset({"zsh"})) == "/bin/zsh"
    assert nearest(frozenset({"launchd"})) == "/sbin/launchd"
    assert nearest(frozenset({"fish"})) is None

    # A non-absolute name (a bare argv[0], a login dash) is not a path.
    monkeypatch.setattr(_process_tree, "parent_process_tree", lambda: (("zsh", "zsh"),))
    assert nearest(frozenset({"zsh"})) is None


def test_nearest_path_matches_every_executable_name(monkeypatch):
    """A shell is found under any of its executable names, not its ID alone."""
    tree = (
        ("python3", "/usr/bin/python3"),
        ("nu", "/opt/homebrew/bin/nu"),
        ("pwsh", "/usr/local/bin/pwsh"),
    )
    monkeypatch.setattr(_process_tree, "parent_process_tree", lambda: tree)
    nearest = _process_tree.nearest_path
    assert nearest(NUSHELL.executable_names) == "/opt/homebrew/bin/nu"
    assert nearest(POWERSHELL.executable_names) == "/usr/local/bin/pwsh"
    assert nearest(frozenset({"powershell"})) is None
