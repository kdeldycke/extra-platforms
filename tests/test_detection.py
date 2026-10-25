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
import sys
from itertools import chain, pairwise
from operator import attrgetter
from pathlib import Path
from types import SimpleNamespace

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUPS,
    ALL_PLATFORMS,
    ALL_SHELLS,
    ALL_TRAITS,
    ILLUMOS,
    Group,
    Shell,
    Trait,
    current_platform,
    detection as detection_module,
    invalidate_caches,
    is_aarch64,
    is_arm,
    is_armv7l,
    is_github_ci,
    is_gitlab_ci,
    is_illumos,
    is_opensuse,
    is_oracle,
    is_solaris,
    is_windows,
    is_x86_64,
)
from extra_platforms.pytest import skip_windows, unless_windows


@pytest.mark.parametrize(
    "obj",
    sorted(chain(ALL_TRAITS, ALL_GROUPS), key=attrgetter("id")),
    ids=attrgetter("id"),
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


DETECTION_SECTIONS = (
    "Architecture detection heuristics",
    "Platform detection heuristics",
    "Shell detection heuristics",
    "Terminal detection heuristics",
    "CI/CD detection heuristics",
    "Agent detection heuristics",
)
"""Comment headers splitting `detection.py`, in trait category order."""


def test_detection_heuristics_sorting():
    """Each section sorts its heuristics by ID, then closes on its generic one."""
    detection_path = Path(inspect.getfile(detection_module))
    source_lines = detection_path.read_text(encoding="utf-8").splitlines()

    starts = []
    for header in DETECTION_SECTIONS:
        found = [i for i, line in enumerate(source_lines, start=1) if header in line]
        assert len(found) == 1, f"{header!r} heads {len(found)} sections"
        starts.append(found[0])
    assert starts == sorted(starts), "Sections are out of the trait category order"

    heuristics = [
        node
        for node in ast.parse(detection_path.read_bytes()).body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_")
    ]
    # Every trait, unknown ones included, has exactly one heuristic.
    assert sorted(node.name for node in heuristics) == sorted(
        trait.detection_func_id for trait in ALL_TRAITS
    )

    for start, end in pairwise([*starts, len(source_lines) + 1]):
        *specific, generic = [
            node.name for node in heuristics if start <= node.lineno < end
        ]
        assert generic.startswith("is_unknown_"), (
            f"Section at line {start} does not end on its is_unknown_*() heuristic"
        )
        assert specific == sorted(specific), f"Heuristics are not sorted: {specific}"
        assert not any(name.startswith("is_unknown_") for name in specific)


def test_is_arm_depends_on_arm_variants(monkeypatch, fresh_caches):
    """Test that is_arm() is a fallback excluded by specific ARM variants."""
    # A machine claimed by a specific variant is not generic ARM.
    monkeypatch.setattr("platform.machine", lambda: "armv7l")
    assert is_armv7l()
    assert not is_arm()

    # An ARM machine unclaimed by any specific variant is generic ARM.
    invalidate_caches()
    monkeypatch.setattr("platform.machine", lambda: "armv4tl")
    assert not is_armv7l()
    assert is_arm()


@pytest.mark.parametrize(
    "distro_id",
    (
        "opensuse",
        "opensuse-aeon",
        "opensuse-leap",
        "opensuse-microos",
        "opensuse-slowroll",
        "opensuse-tumbleweed",
    ),
)
def test_opensuse_channel_folding(monkeypatch, distro_id, fresh_caches):
    """Any openSUSE release channel is detected as the OPENSUSE platform."""
    monkeypatch.setattr("extra_platforms.detection.os_release_id", lambda: distro_id)
    assert is_opensuse()


def test_oracle_raw_id_detection(monkeypatch, fresh_caches):
    """Oracle Linux is detected from its raw ``ol`` os-release ID."""
    monkeypatch.setattr("extra_platforms.detection.os_release_id", lambda: "ol")
    assert is_oracle()


@pytest.mark.parametrize("machine", ("x86_64", "AMD64", "amd64", "i86pc"))
def test_x86_64_machine_aliases(monkeypatch, machine, fresh_caches):
    """Every string reported for 64-bit x86 resolves to X86_64.

    Solaris and illumos answer ``i86pc``, which names the machine family and not
    the ISA, mirroring the ``sun4u`` and ``sun4v`` aliases
    :func:`~extra_platforms.is_sparc64` already accepts. Captured on
    OpenIndiana Hipster 2026.04.
    """
    monkeypatch.setattr(detection_module.platform, "machine", lambda: machine)
    assert is_x86_64()


PLATFORM_HOST_SIGNALS = frozenset((
    "Path",
    "environ",
    "os_release_id",
    "platform.platform",
    "platform.release",
    "platform.uname",
    "sys.platform",
))
"""Every host signal the platform detection heuristics read.

:func:`mock_platform_host` controls exactly these, and
:func:`test_platform_signals_are_all_mocked` keeps the two in step.
"""


@functools.cache
def _platform_heuristic_signals() -> frozenset[str]:
    """Collect the host signals read by every ``is_<platform>()`` heuristic.

    Walks the source of the heuristic backing each member of
    :data:`~extra_platforms.ALL_PLATFORMS`, and keeps the module-level names it
    reads: an attribute of an imported module (``sys.platform``), or an imported
    object (``os_release_id``). Names bound inside the function are skipped, and
    so are calls to sibling ``is_*()`` heuristics, which this walk covers on
    their own. Upper-case names are skipped too: they name module-level
    constants (``_CHROMEOS_IDS``), which hold fixed data and read nothing from
    the host.
    """
    heuristic_ids = {f"is_{plat.id}" for plat in ALL_PLATFORMS}
    signals = set()

    for node in ast.parse(inspect.getsource(detection_module)).body:
        if not isinstance(node, ast.FunctionDef) or node.name not in heuristic_ids:
            continue
        # Walk statements rather than the function node, to skip its decorators.
        nodes = [sub for stmt in node.body for sub in ast.walk(stmt)]

        bound = {
            sub.id
            for sub in nodes
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store)
        }
        bound |= {
            alias.asname or alias.name
            for sub in nodes
            if isinstance(sub, ast.ImportFrom)
            for alias in sub.names
        }

        for sub in nodes:
            if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name):
                module_id = sub.value.id
                if module_id not in bound and inspect.ismodule(
                    getattr(detection_module, module_id, None)
                ):
                    signals.add(f"{module_id}.{sub.attr}")
            elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                if (
                    sub.id in bound
                    or sub.id.startswith("is_")
                    or sub.id.lstrip("_").isupper()
                ):
                    continue
                imported = getattr(detection_module, sub.id, None)
                if imported is not None and not inspect.ismodule(imported):
                    signals.add(sub.id)

    return frozenset(signals)


def test_platform_signals_are_all_mocked():
    """Every signal a platform heuristic reads is one the host mock pins.

    :func:`~extra_platforms.current_platform` evaluates all platform heuristics
    and raises as soon as two match. A signal left reading the real host
    therefore makes the result depend on where the suite runs. A heuristic
    added with a new signal fails here until :func:`mock_platform_host`
    controls that signal too.
    """
    assert _platform_heuristic_signals() == PLATFORM_HOST_SIGNALS


def mock_platform_host(
    monkeypatch,
    *,
    sys_platform: str,
    os_release: str = "",
    platform_string: str = "",
    release: str = "",
    uname: SimpleNamespace | None = None,
) -> None:
    """Make every :data:`PLATFORM_HOST_SIGNALS` entry answer for one host.

    A test asserting on :func:`~extra_platforms.current_platform` must set every
    signal, not only the ones its own heuristic reads: the resolver runs all of
    them, and a second match raises. Leaving
    :func:`~extra_platforms.platform_info.os_release_id` on the real host is what
    made ``test_illumos_excludes_solaris`` match UBUNTU next to ILLUMOS on the
    Linux runners, while it passed on the macOS and Windows ones, which carry no
    os-release file.

    Each default is the value an absent signal produces, so a caller states only
    what its simulated host reports.

    :param monkeypatch: Fixture undoing every patch at the end of the test.
    :param sys_platform: Value of :data:`sys.platform`.
    :param os_release: Distribution ID from
        :func:`~extra_platforms.platform_info.os_release_id`, empty on a host
        with no os-release file.
    :param platform_string: Return value of :func:`platform.platform`.
    :param release: Return value of :func:`platform.release`.
    :param uname: Return value of :func:`platform.uname`, defaulting to a record
        whose every field is empty.
    """
    if uname is None:
        uname = SimpleNamespace(system="", node="", release="", version="", machine="")

    monkeypatch.setattr(sys, "platform", sys_platform)
    monkeypatch.setattr(detection_module, "os_release_id", lambda: os_release)
    monkeypatch.setattr(detection_module.platform, "release", lambda: release)
    monkeypatch.setattr(detection_module.platform, "uname", lambda: uname)
    monkeypatch.setattr(
        detection_module.platform, "platform", lambda **kwargs: platform_string
    )

    # The simulated host sets no environment marker and carries no marker file.
    monkeypatch.setattr(detection_module, "environ", {})
    monkeypatch.setattr(detection_module.Path, "is_file", lambda self: False)


def test_illumos_excludes_solaris(monkeypatch, fresh_caches):
    """An illumos distribution matches ILLUMOS alone, never SOLARIS as well.

    illumos inherits the SunOS 5.11 release string from OpenSolaris, so
    :func:`platform.platform` answers ``Solaris-2.11`` there. Both heuristics
    used to match at once, which made :func:`~extra_platforms.current_platform`
    raise on every illumos host. Values captured on OpenIndiana Hipster 2026.04.
    """
    mock_platform_host(
        monkeypatch,
        sys_platform="sunos5",
        platform_string="Solaris-2.11",
        release="5.11",
        uname=SimpleNamespace(
            system="SunOS",
            node="openindiana",
            release="5.11",
            version="illumos-4648b9b8c3",
            machine="i86pc",
        ),
    )

    assert is_illumos()
    assert not is_solaris()
    assert current_platform() is ILLUMOS


def test_detection_functions_cached(fresh_caches):
    """Test that detection functions are cached with @cache decorator."""
    # Clear caches first.

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


def test_environment_variable_ci_detection(monkeypatch, fresh_caches):
    """Test CI detection based on environment variables."""

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


def test_detection_no_circular_dependencies(fresh_caches):
    """Test that detection functions can all be called without circular dependency issues."""

    # Call all trait detection functions.
    for trait in ALL_TRAITS:
        # Access the current property, which calls the detection function.
        _ = trait.current


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
    # Keep the real procfs of an illumos host out of these made-up processes.
    monkeypatch.setattr(detection_module, "_system_v_executable", lambda pid: "")
    # Ordered nearest-first. The login shell's argv[0] (-zsh) yields no path, and
    # "-m pytest" must not be mistaken for an interpreter-hosted shell.
    assert detection_module._tree_from_ps() == (
        ("python3", "/usr/bin/python3"),
        ("zsh", ""),
        ("launchd", "/sbin/launchd"),
    )


def test_tree_from_ps_reads_system_v_executable(monkeypatch):
    """System V procfs names the binary a bare ``argv[0]`` hides, as on illumos."""
    table = (
        "  100     1 /usr/lib/ssh/sshd\n"
        "  200   100 sh probe.sh\n"
        "  300   200 /usr/bin/python3.14 report.py\n"
    )
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout=table),
    )
    monkeypatch.setattr(os, "getpid", lambda: 300)
    links = {200: "/usr/bin/i86/ksh93", 300: "/usr/bin/python3.14"}
    monkeypatch.setattr(
        detection_module, "_system_v_executable", lambda pid: links.get(pid, "")
    )
    assert detection_module._tree_from_ps() == (
        ("python3", "/usr/bin/python3.14"),
        ("python3", "/usr/bin/python3.14"),
        ("ksh93", "/usr/bin/i86/ksh93"),
        ("sh", ""),
        ("sshd", "/usr/lib/ssh/sshd"),
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
    # by the System V ps on Solaris and AIX). One `-o` per field: FreeBSD reads
    # `-o pid=,ppid=,args=` as a single `pid` column with a `,ppid=,args=` header.
    assert captured["args"] == ("ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "args=")


@skip_windows
def test_tree_from_ps_replaces_undecodable_bytes(tmp_path, monkeypatch):
    """A byte that is no UTF-8, in the arguments of another process, is replaced.

    The fake `ps` lists the current process, and a second one whose argument is
    a Latin-1 `café`.
    """
    ps = tmp_path / "ps"
    ps.write_text(
        f"#!{sys.executable}\n"
        "import sys\n"
        "sys.stdout.buffer.write(\n"
        "    b'  300     1 /bin/zsh\\n  400     1 /usr/bin/python3 caf\\xe9\\n'\n"
        ")\n",
        encoding="UTF-8",
    )
    ps.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)
    monkeypatch.setattr(os, "getpid", lambda: 300)
    monkeypatch.setattr(detection_module, "_system_v_executable", lambda pid: "")
    assert detection_module._tree_from_ps() == (("zsh", "/bin/zsh"),)


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
    assert detection_module._pairs_from_process(executable, argv) == expected


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
    monkeypatch.setattr(detection_module.Path, "read_bytes", lambda self: netbsd_stat)
    assert detection_module._ppid_from_proc(1500) == 1


def test_ppid_from_proc_netbsd_status_fallback(monkeypatch):
    """When NetBSD's stat is unreadable, the BSD-style status fallback parses."""
    netbsd_status = b"ksh 1500 1 1500 1500 -1,-1 noflags,noflags 1234567,890 - 1000"

    def read_bytes(self):
        # Mimic a NetBSD /proc with only `status` readable (stat denied).
        if self.name == "stat":
            raise OSError("stat unreadable")
        return netbsd_status

    monkeypatch.setattr(detection_module.Path, "read_bytes", read_bytes)
    assert detection_module._ppid_from_proc(1500) == 1


@skip_windows
def test_parent_process_tree_falls_back_to_ps_when_proc_empty(
    monkeypatch, fresh_caches
):
    """System V /proc (illumos, Solaris) yields nothing, so fall back to ps."""
    monkeypatch.setattr(detection_module, "_tree_from_proc", lambda: ())
    sentinel = (("zsh", "/usr/bin/zsh"),)
    monkeypatch.setattr(detection_module, "_tree_from_ps", lambda: sentinel)
    # Simulate /proc being mounted, as it is on illumos and Solaris.
    monkeypatch.setattr(detection_module.Path, "is_dir", lambda self: True)
    invalidate_caches()
    assert detection_module._parent_process_tree() == sentinel


def test_parent_process_exe_names(fresh_caches):
    """The dispatcher returns a clean frozenset on every platform."""
    names = detection_module._parent_process_exe_names()
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
    """The nearest absolute path for a shell name wins; non-absolute is skipped."""
    tree = (
        ("python3", "/usr/bin/python3"),
        ("zsh", "/bin/zsh"),  # Nearest zsh.
        ("zsh", "/opt/zsh"),  # Farther zsh, must not win.
        ("launchd", "/sbin/launchd"),
    )
    monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: tree)
    running = detection_module._running_shell_path
    assert running(frozenset({"zsh"})) == "/bin/zsh"
    assert running(frozenset({"launchd"})) == "/sbin/launchd"
    assert running(frozenset({"fish"})) is None

    # A non-absolute name (a bare argv[0], a login dash) is not a path.
    monkeypatch.setattr(
        detection_module, "_parent_process_tree", lambda: (("zsh", "zsh"),)
    )
    assert running(frozenset({"zsh"})) is None


def test_running_shell_path_matches_every_executable_name(monkeypatch):
    """A shell is found under any of its executable names, not its ID alone."""
    from extra_platforms import NUSHELL, POWERSHELL

    tree = (
        ("python3", "/usr/bin/python3"),
        ("nu", "/opt/homebrew/bin/nu"),
        ("pwsh", "/usr/local/bin/pwsh"),
    )
    monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: tree)
    running = detection_module._running_shell_path
    assert running(NUSHELL.executable_names) == "/opt/homebrew/bin/nu"
    assert running(POWERSHELL.executable_names) == "/usr/local/bin/pwsh"
    assert running(frozenset({"powershell"})) is None


def unset_shell_startup_vars(monkeypatch) -> None:
    """Unset the variables shells set at startup, ``PSModulePath`` included.

    ``SHELL`` and the parent process tree are then the only shell signals, so
    the shell running the suite cannot leak into the test.

    :param monkeypatch: Fixture undoing every patch at the end of the test.
    """
    for shell in ALL_SHELLS:
        assert isinstance(shell, Shell)
        if shell.version_env_var:
            monkeypatch.delenv(shell.version_env_var, raising=False)
    monkeypatch.delenv("PSModulePath", raising=False)


@pytest.mark.parametrize(
    ("shell", "executable"),
    [
        pytest.param(shell, name, id=name)
        for shell in ALL_SHELLS
        if isinstance(shell, Shell)
        for name in shell.executables
    ],
)
@pytest.mark.parametrize("source", ["SHELL", "process tree"])
def test_shell_detected_by_every_executable_name(
    monkeypatch, shell, executable, source, fresh_caches
):
    """Each file name a shell's binary goes by detects it, as its ID does."""
    path = f"/nonexistent/bin/{executable}"
    unset_shell_startup_vars(monkeypatch)
    if source == "SHELL":
        monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: ())
        monkeypatch.setenv("SHELL", path)
    else:
        monkeypatch.setattr(
            detection_module, "_parent_process_tree", lambda: ((executable, path),)
        )
        monkeypatch.delenv("SHELL", raising=False)
    invalidate_caches()
    assert shell.current


def test_current_shell_prefers_a_running_pwsh_over_configured_shell(
    monkeypatch, fresh_caches
):
    """A ``pwsh`` parent process names PowerShell, whose ID is not its binary name."""
    from extra_platforms import POWERSHELL, current_shell

    monkeypatch.setattr(
        detection_module,
        "_parent_process_tree",
        lambda: (("pwsh", "/usr/local/bin/pwsh"),),
    )
    monkeypatch.setenv("SHELL", "/bin/zsh")
    unset_shell_startup_vars(monkeypatch)
    invalidate_caches()
    assert current_shell() is POWERSHELL


@pytest.mark.parametrize(
    ("path", "expected_id"),
    [
        ("/bin/zsh", "zsh"),
        ("/opt/homebrew/bin/pwsh", "powershell"),
        (r"C:\Program Files\PowerShell\7\pwsh.exe", "powershell"),
        ("/usr/local/bin/nu", "nushell"),
        ("/usr/local/bin/elvish", "unknown_shell"),
    ],
)
def test_shell_from_path(path, expected_id):
    """A shell path resolves to its catalog entry by file name, or to the
    unknown shell."""
    from extra_platforms import shell_from_path

    assert shell_from_path(path).id == expected_id


@skip_windows
def test_shell_from_path_resolves_symlinks(tmp_path):
    """``sh`` linking to ``bash`` names bash: the implementation, not the interface."""
    from extra_platforms import BASH, shell_from_path

    # Link to a file under tmp_path, never the host's /bin/bash: a hermetic build
    # sandbox may have no such file, and a missing target resolves to "sh".
    target = tmp_path / "bash"
    target.touch()
    link = tmp_path / "sh"
    link.symlink_to(target)
    assert shell_from_path(link) is BASH


@skip_windows
@pytest.mark.parametrize(
    ("target", "link", "expected_id"),
    [
        # Alpine links both to BusyBox, whose sh applet is its ash.
        ("busybox", "ash", "ash"),
        ("busybox", "sh", "ash"),
        # A link to a binary going by no shell's name keeps its own name.
        ("multicall", "sh", "sh"),
    ],
)
def test_shell_from_path_resolves_multicall_binary(tmp_path, target, link, expected_id):
    """A link to a multi-call binary names the program the link name picks."""
    from extra_platforms import shell_from_path

    (tmp_path / target).touch()
    (tmp_path / link).symlink_to(tmp_path / target)
    assert shell_from_path(tmp_path / link).id == expected_id


def test_current_shell_path(monkeypatch, fresh_caches):
    """current_shell_path() prefers the running binary, then falls back to SHELL."""
    from extra_platforms import ZSH, current_shell_path

    monkeypatch.setattr(detection_module, "current_shell", lambda strict=False: ZSH)

    # The process tree yields the running binary: prefer it over SHELL.
    monkeypatch.setattr(detection_module, "_running_shell_path", lambda _: "/bin/zsh")
    monkeypatch.setenv("SHELL", "/bin/sh")
    invalidate_caches()
    assert current_shell_path() == "/bin/zsh"

    # No running path: fall back to the configured login shell, when it names
    # the current shell. A path that does not exist here is read as text.
    monkeypatch.setattr(detection_module, "_running_shell_path", lambda _: None)
    monkeypatch.setenv("SHELL", "/nonexistent/bin/zsh")
    invalidate_caches()
    assert current_shell_path() == "/nonexistent/bin/zsh"

    # A login shell of another kind is no fallback: illumos runs the suite from
    # a bare `sh` under a bash login, and must not report bash's path for it.
    monkeypatch.setenv("SHELL", "/nonexistent/bin/bash")
    invalidate_caches()
    assert current_shell_path() is None

    # Neither source available.
    monkeypatch.delenv("SHELL", raising=False)
    invalidate_caches()
    assert current_shell_path() is None


def test_shell_info_path_ignores_another_login_shell(monkeypatch, fresh_caches):
    """``Shell.info()`` reports no path rather than the path of another shell."""
    from extra_platforms import SH

    monkeypatch.setitem(detection_module._detection_registry, "is_sh", lambda: True)
    # The running sh shows as a bare argv[0], the way illumos' ps reports it.
    monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: (("sh", ""),))
    monkeypatch.setenv("SHELL", "/nonexistent/bin/bash")
    invalidate_caches()
    assert SH.info()["path"] is None

    monkeypatch.setenv("SHELL", "/nonexistent/bin/sh")
    invalidate_caches()
    assert SH.info()["path"] == "/nonexistent/bin/sh"


def test_current_shell_prefers_running_shell_over_configured_shell(
    monkeypatch, fresh_caches
):
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
    unset_shell_startup_vars(monkeypatch)
    invalidate_caches()
    assert current_shell() is FISH


def test_nested_ancestor_shells_all_detected(monkeypatch, fresh_caches):
    """A session shell above the running shell chain is detected in parallel.

    Regression guard for openSUSE OBS chroot builds run from a fish terminal:
    the ``/proc`` walk escapes the build root into the packager's desktop
    session, so fish sits in the ancestor tree above the bash chain running
    the build. Both shells are detected, and the primary shell stays the
    nearest running one.
    """
    from extra_platforms import BASH, current_shell, is_bash, is_fish

    monkeypatch.setattr(
        detection_module,
        "_parent_process_tree",
        lambda: (
            ("python3", "/usr/bin/python3.11"),  # pytest.
            ("bash", "/usr/bin/bash"),  # rpmbuild %check scriptlet.
            ("rpmbuild", "/usr/bin/rpmbuild"),
            ("bash", "/usr/bin/bash"),  # obs-build script.
            ("python3", "/usr/bin/python3.11"),  # osc.
            ("fish", "/usr/bin/fish"),  # Packager's desktop shell.
        ),
    )
    # `su - abuild` reset SHELL to the build user's login shell.
    monkeypatch.setenv("SHELL", "/bin/bash")
    # No shell-startup version variables leak into the environment.
    unset_shell_startup_vars(monkeypatch)
    invalidate_caches()
    assert is_bash()
    assert is_fish()
    assert current_shell() is BASH


@pytest.mark.parametrize(
    ("tree", "login_shell", "expected_id"),
    [
        # A bash script run from a zsh session.
        (
            (
                ("python3", "/usr/bin/python3"),
                ("bash", "/bin/bash"),
                ("zsh", "/bin/zsh"),
            ),
            "/bin/zsh",
            "bash",
        ),
        # Dash invoked as sh from a bash session: the /proc walk yields the
        # resolved binary and the argv[0] of the same process.
        (
            (
                ("python3", "/usr/bin/python3.14"),
                ("dash", "/usr/bin/dash"),
                ("sh", ""),
                ("bash", "/usr/bin/bash"),
            ),
            "/bin/bash",
            "dash",
        ),
        # SH stays the fallback: a zsh session running `sh -c` reports zsh.
        (
            (
                ("python3", "/usr/bin/python3"),
                ("sh", "/bin/sh"),
                ("zsh", "/bin/zsh"),
            ),
            "/bin/zsh",
            "zsh",
        ),
    ],
)
def test_current_shell_prefers_nearest_running_shell(
    monkeypatch, tree, login_shell, expected_id, fresh_caches
):
    """When shells nest, the nearest one wins over the login shell above it."""
    from extra_platforms import current_shell

    monkeypatch.setattr(detection_module, "_parent_process_tree", lambda: tree)
    monkeypatch.setenv("SHELL", login_shell)
    unset_shell_startup_vars(monkeypatch)
    invalidate_caches()
    assert current_shell().id == expected_id
