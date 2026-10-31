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
"""Walk the parent process tree, to find the shells running the current process.

The walk reports each ancestor of the current process as a ``(name, path)`` pair,
nearest ancestor first. ``name`` is the lowercased stem of the program, the way
shells are named in the registry, and ``path`` is its executable, when known.

It reads what the platform exposes:

- ``/proc`` when present (Linux always, and the BSDs that mount procfs): no
  subprocess is spawned.
- ``ps`` otherwise (macOS, BSDs without procfs, and the System V ``/proc`` of
  illumos and Solaris).
- The Win32 Tool Help API on Windows, through {mod}`extra_platforms._windows`.
- Nothing on platforms exposing none of these.

A process can hide the shell it runs: BusyBox picks its applet from its name or
first argument, a user-mode emulator wraps the command it runs, and an
interpreter runs a shell written as a script, like Xonsh. Each process therefore
contributes every name it goes by.

```{seealso}
Mirrors the approach of [shellingham](https://github.com/sarugaku/shellingham).
```
"""

from __future__ import annotations

import os
import re
import sys
from functools import cache
from pathlib import Path, PurePosixPath

from .group_data import ALL_SHELLS
from .trait import Shell

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    _Tree = tuple[tuple[str, str], ...]


_BUSYBOX_ASH_APPLETS = frozenset(("ash", "sh"))
"""BusyBox applets running its Almquist shell.

[BusyBox](https://busybox.net) is a multi-call binary: it runs the applet named by
the name it is called by (Alpine links ``/bin/sh`` and ``/bin/ash`` to
``/bin/busybox``), or by its first argument when called by its own name
(``busybox sh -c ...``). Its ``sh`` applet is its ``ash``: on Alpine, both set
``BB_ASH_VERSION``. Both names therefore give {data}`~extra_platforms.ASH`.
"""


_EMULATOR_NAMES = re.compile(r"rosetta|qemu-[a-z0-9_]+(?:-static)?")
"""User-mode CPU emulators that wrap the real command in their arguments."""


def busybox_applet(name: str) -> str:
    """Name the shell a BusyBox applet runs.

    That is ``ash`` for its Almquist shell applets, the applet name otherwise.
    """
    return "ash" if name in _BUSYBOX_ASH_APPLETS else name


def _shell_name(command: str) -> str:
    """Normalize a process command into a comparable shell name.

    Strips a leading ``-`` (which marks a login shell, like ``-bash``), then
    returns the lowercased filename stem (``/usr/bin/bash`` becomes ``bash``).
    Returns an empty string when no name can be extracted.
    """
    return PurePosixPath(command.lstrip("-")).stem.lower()


def _ancestors(parent_of: Callable[[int], int | None], pid: int) -> Iterator[int]:
    """Yield ``pid`` and the PIDs of its ancestors, nearest first.

    ``parent_of`` returns the parent PID of a process, or {data}`None` when it
    cannot tell, which ends the walk. It is only asked about a PID once the
    consumer has read that process, so a consumer stopping on a process it
    knows nothing about never makes it look one up.

    The walk also stops at the root of the tree (PID 1, or the PID 0 that Windows
    gives its idle process), and on a PID it saw before: a parent can exit and its
    PID be reused, which can loop the parent links.
    """
    seen: set[int] = set()
    while pid > 1 and pid not in seen:
        seen.add(pid)
        yield pid
        parent = parent_of(pid)
        if parent is None:
            return
        pid = parent


@cache
def _interpreter_shell_specs() -> tuple[tuple[re.Pattern[str], str], ...]:
    """Compiled ``(interpreter pattern, launcher name)`` pairs from the registry.

    Built from {class}`~extra_platforms.Shell` instances that declare an
    {attr}`~extra_platforms.Shell.interpreter`. The interpreter base name
    becomes a version-tolerant pattern (so ``python`` matches ``python3`` and
    ``python3.11``); the launcher name to look for is the shell's ``id``.
    """
    return tuple(
        (re.compile(rf"{re.escape(shell.interpreter)}(\d+(\.\d+)?)?"), shell.id)
        for shell in ALL_SHELLS
        if isinstance(shell, Shell) and shell.interpreter
    )


def _interpreter_shell(argv: list[str]) -> tuple[str, str] | None:
    """Detect a shell hosted by an interpreter from a process command line.

    When ``argv[0]`` is a known interpreter (like ``python``) and a later
    argument is an existing file whose name is a hosted shell's launcher (like
    ``xonsh``), returns ``(shell_id, launcher_path)``, else {data}`None`.

    The three guards (interpreter-name pattern, exact launcher basename, and an
    {meth}`~pathlib.Path.is_file` check) keep unrelated invocations like
    ``python -m pytest test_xonsh.py`` from matching.
    """
    if not argv:
        return None
    proc_name = Path(argv[0]).name.lower()
    for pattern, launcher in _interpreter_shell_specs():
        if not pattern.fullmatch(proc_name):
            continue
        for arg in argv[1:]:
            if Path(arg).name.lower() == launcher and Path(arg).is_file():
                return launcher, arg
    return None


def _unwrap_emulator(argv: list[str]) -> list[str]:
    """Strip a leading user-mode emulator (``qemu-<arch>``, ``rosetta``) from argv.

    Under foreign-architecture emulation (like ``docker run --platform``), a
    process shows up as ``qemu-aarch64 /bin/bash …``; the real command is the
    remaining arguments. Returns ``argv`` with the emulator prefix removed, or
    ``argv`` unchanged when ``argv[0]`` is not an emulator (or nothing follows
    it). Composes with {func}`_interpreter_shell`: an emulated ``python`` running
    xonsh unwraps to ``python …`` first, then resolves to xonsh.
    """
    if len(argv) >= 2 and _EMULATOR_NAMES.fullmatch(_shell_name(argv[0])):
        return argv[1:]
    return argv


def _pairs_from_process(executable: str, argv: list[str]) -> list[tuple[str, str]]:
    """Derive the ``(name, path)`` pairs a single process contributes.

    Yields the pair of ``executable`` first, the resolved binary the process runs
    (``""`` when the walk cannot read it). Then unwraps a user-mode emulator
    prefix from ``argv`` (so the emulated shell is seen), and yields the
    ``argv[0]`` shell name (with its path only when absolute, since a login dash
    carries none) plus any interpreter-hosted shell found in the arguments (like
    xonsh run under python). Shared by the ``/proc`` and ``ps`` walks, which
    differ only in how they obtain ``executable`` and ``argv``.

    BusyBox runs the applet named by its first argument when called by its own
    name, and by ``argv[0]`` when called through a link, which only an
    ``executable`` resolving to BusyBox reveals. The applet then names the shell,
    see {data}`_BUSYBOX_ASH_APPLETS`.
    """
    pairs: list[tuple[str, str]] = []
    if exe_name := _shell_name(executable):
        pairs.append((exe_name, executable))
    busybox = exe_name == "busybox"
    argv = _unwrap_emulator(argv)
    if len(argv) >= 2 and _shell_name(argv[0]) == "busybox":
        argv, busybox = argv[1:], True
    if argv:
        # argv[0] recovers login shells and survives an unreadable exe; keep it
        # as a path only when absolute (a login dash carries none).
        if name := _shell_name(argv[0]):
            if busybox:
                name = busybox_applet(name)
            pairs.append((name, argv[0] if argv[0].startswith("/") else ""))
        # A shell hosted by an interpreter (like xonsh run under python).
        if hosted := _interpreter_shell(argv):
            pairs.append(hosted)
    return pairs


def _parse_proc_ppid(record: str) -> int:
    """Extract the parent PID from a ``/proc/<pid>`` process record.

    Two on-disk layouts are recognized, told apart by the presence of the
    parenthesized ``comm`` field:

    - Linux ``stat`` (and NetBSD's Linux-compatible ``stat``):
      ``"pid (comm) state ppid ..."``. The ``comm`` field may itself contain
      spaces and parentheses, so the PPID is taken as the second field after
      the last ``)``.
    - BSD ``status`` (FreeBSD, DragonFly): ``"comm pid ppid pgid ..."``, where
      the PPID is the third whitespace-separated field.

    Raises {class}`ValueError` or {class}`IndexError` on an unparsable record.
    """
    marker = record.rfind(")")
    if marker != -1:
        return int(record[marker + 2 :].split()[1])
    return int(record.split()[2])


def _ppid_from_proc(pid: int) -> int | None:
    """Read the parent PID of ``pid`` from ``/proc``.

    Tries the Linux-style ``stat`` file first, then the BSD-style ``status``
    file, so the same walk works across Linux, NetBSD, and FreeBSD. Returns
    {data}`None` when neither file can be read or parsed.

    ```{note}
    System V ``/proc`` (illumos, Solaris, AIX) exposes ``status`` as a binary
    ``pstatus_t`` rather than text. Bytes are decoded with ``errors="replace"``
    so a binary record degrades to an unparsable string (and {data}`None`)
    instead of raising {exc}`UnicodeDecodeError`. {func}`parent_process_tree`
    then falls back to ``ps`` on those systems.
    ```
    """
    for proc_file in ("stat", "status"):
        try:
            record = Path(f"/proc/{pid}/{proc_file}").read_bytes()
        except OSError:
            continue
        try:
            return _parse_proc_ppid(record.decode(errors="replace"))
        except (ValueError, IndexError):
            return None
    return None


def _tree_from_proc() -> _Tree:
    """Walk the parent process tree through ``/proc`` (Linux and BSD procfs).

    For each process it reads the resolved executable (``/proc/<pid>/exe``, an
    absolute path that follows a ``/bin/sh`` -> Bash symlink) and the full
    ``argv`` (``/proc/<pid>/cmdline``). Reading both means a login shell is still
    recognized when the ``exe`` symlink is unreadable (hardened ``/proc``
    mounted with ``hidepid``), and vice versa. ``argv`` also lets an
    interpreter-hosted shell (xonsh under python) or an emulated shell (under
    qemu/rosetta) be recognized. ``path`` is empty when only a non-absolute
    ``argv[0]`` is available.
    """
    pairs: list[tuple[str, str]] = []
    for pid in _ancestors(_ppid_from_proc, os.getpid()):
        # Resolved executable: an absolute path that follows symlinks.
        try:
            executable = os.readlink(f"/proc/{pid}/exe")
        except OSError:
            executable = ""
        # Full argv from the raw, null-separated command line.
        try:
            raw = Path(f"/proc/{pid}/cmdline").read_bytes()
            argv = [arg for arg in raw.decode(errors="replace").split("\0") if arg]
        except OSError:
            argv = []
        pairs.extend(_pairs_from_process(executable, argv))
    return tuple(pairs)


def _system_v_executable(pid: int) -> str:
    """Return the executable System V procfs links for ``pid``, or ``""``.

    illumos and Solaris link ``/proc/<pid>/path/a.out`` to the resolved binary a
    process runs: on illumos, a shell started as a bare ``sh`` runs
    ``/usr/bin/i86/ksh93``. A process of another user, or a system without that
    link, gives an empty string.
    """
    try:
        return os.readlink(f"/proc/{pid}/path/a.out")
    except OSError:
        return ""


def _tree_from_ps() -> _Tree:
    """Walk the parent process tree through ``ps``.

    Used on POSIX systems without a usable text ``/proc`` (macOS and BSDs
    without procfs, plus the System V ``/proc`` of illumos, Solaris, and
    AIX/IBM i). Parses a single ``ps`` snapshot into a ``{pid: (ppid, args)}``
    table, then walks from the current process up to the root.

    The full argument list is requested (rather than just the executable) so
    that interpreter-hosted shells (like xonsh under python) can be recognized
    from their arguments. ``path`` is taken from ``argv[0]`` when absolute; a
    login shell (``-zsh``) or a bare name carries no path, so callers fall back
    to ``SHELL``. Where System V procfs links each process to its executable,
    that link adds the binary actually running, ahead of ``argv`` (see
    {func}`_system_v_executable`).

    The invocation is the portable POSIX form (``-A``, ``-o field=``, and the
    ``args`` specifier) with no ``-ww``, so it works across macOS, the BSDs,
    Linux, and the System V ``ps`` of illumos, Solaris, and AIX/IBM i. Those
    System V variants lack the ``command`` specifier (only ``args``) and reject
    ``-ww`` (AIX accepts ``-w`` only in Berkeley mode, which has no ``-o``);
    ``args`` may be truncated there, but ``argv[0]`` stays intact. Parsing reads
    positional columns from empty (``field=``) headers, sidestepping the
    header-name differences (``COMMAND`` vs ``CMD``) that complicate name-based
    parsing.

    ```{caution}
    Each field takes its own ``-o``. POSIX reads everything after a ``=`` as the
    header text, so FreeBSD's ``ps`` takes ``-o pid=,ppid=,args=`` as the
    ``pid`` column under a ``,ppid=,args=`` header, and prints nothing else.
    Linux and macOS accept the combined form, which hides the difference.
    ```

    ```{important}
    ``-A`` (select every process) is essential, not merely convenient. Without
    it, `ps` defaults to processes sharing the caller's controlling terminal,
    and macOS returns *nothing* when run outside a tty (as in CI or any
    non-interactive context, unlike Linux which lists all processes regardless).
    ``-A`` makes the snapshot tty-independent.
    ```
    """
    # Deferred import: keeps subprocess off the import path of the package.
    import subprocess

    try:
        result = subprocess.run(
            ("ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "args="),
            capture_output=True,
            text=True,
            # Any process on the host can hold bytes that are no UTF-8 in its
            # arguments: replace them, as _tree_from_proc does.
            encoding="UTF-8",
            errors="replace",
            check=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return ()

    # Parse "<pid> <ppid> <args...>" rows into {pid: (ppid, args)}. The
    # argument list is the last field and is kept whole. str() coerces an
    # unexpected stdout (like a globally mocked subprocess.run returning a Mock)
    # to text, so parsing degrades to an empty result instead of raising.
    table: dict[int, tuple[int, str]] = {}
    for line in str(result.stdout).splitlines():
        fields = line.split(maxsplit=2)
        if len(fields) < 3:
            continue
        try:
            table[int(fields[0])] = (int(fields[1]), fields[2])
        except ValueError:
            continue

    pairs: list[tuple[str, str]] = []
    for pid in _ancestors(lambda child: table[child][0], os.getpid()):
        if pid not in table:
            break
        command = table[pid][1]
        pairs.extend(_pairs_from_process(_system_v_executable(pid), command.split()))
    return tuple(pairs)


def _walk_process_map(
    process_map: dict[int, tuple[int, str]],
    start_pid: int,
    path_getter: Callable[[int], str],
) -> _Tree:
    """Walk a ``{pid: (ppid, executable)}`` map into ordered ``(name, path)`` pairs.

    Climbs from ``start_pid`` to the root, nearest ancestor first. Each
    ``executable`` is normalized into a shell name via {func}`_shell_name`, and
    ``path_getter`` resolves a matched pid's full executable path. This is the
    platform-agnostic core of the Windows walk: the snapshot acquisition is the
    only Win32-specific part.
    """
    pairs: list[tuple[str, str]] = []
    for pid in _ancestors(lambda child: process_map[child][0], start_pid):
        if pid not in process_map:
            break
        if name := _shell_name(process_map[pid][1]):
            pairs.append((name, path_getter(pid)))
    return tuple(pairs)


def _tree_from_windows() -> _Tree:
    """Walk the parent process tree through the Win32 Tool Help API.

    Used on Windows, which has neither ``/proc`` nor ``ps``. Snapshots every
    process into a ``{pid: (ppid, executable)}`` map (see
    {mod}`extra_platforms._windows`), then walks from the current process up to
    the root, resolving each ancestor's full path via
    ``QueryFullProcessImageNameW``.

    Returns an empty tuple off Windows or on any Win32 failure, so detection
    degrades to the environment-variable heuristics.
    """
    if sys.platform == "win32":
        try:
            from . import _windows

            return _walk_process_map(
                _windows.process_map(), os.getpid(), _windows.process_path
            )
        except (OSError, ImportError):
            pass
    return ()


@cache
def parent_process_tree() -> _Tree:
    """Ordered ``(name, path)`` pairs for the process tree, nearest first.

    ``name`` is the normalized shell name (see {func}`_shell_name`); ``path`` is
    the best-effort executable path, absolute when the source provides it and
    empty otherwise. See the module docstring for the source read on each
    platform.
    """
    # Linux (and procfs BSDs) expose a text /proc: this needs no subprocess.
    # System V procfs (illumos, Solaris, AIX) uses a binary layout the Linux
    # reader cannot parse, and yields nothing.
    if Path("/proc").is_dir() and (tree := _tree_from_proc()):
        return tree
    # macOS, procfs-less BSDs, and System V procfs systems.
    if os.name == "posix":
        return _tree_from_ps()
    return _tree_from_windows()


@cache
def parent_process_names() -> frozenset[str]:
    """Collect the names of the parent process tree.

    Returns a {class}`frozenset` of lowercased executable stems (like
    ``"bash"`` or ``"python3"``), derived from {func}`parent_process_tree`.
    """
    return frozenset(name for name, _ in parent_process_tree())


def nearest_path(names: frozenset[str]) -> str | None:
    r"""Return the executable path of the nearest ancestor named in ``names``.

    Returns the first (nearest) absolute path whose name is one of ``names``,
    like a shell's {attr}`~extra_platforms.Shell.executable_names`. Non-absolute
    sources (a login dash or a bare ``argv[0]``) are skipped so callers can fall
    back to ``SHELL``. A path is considered absolute when it starts with ``/``
    (POSIX) or satisfies ``os.path.isabs`` (Windows drive paths like ``C:\...``).
    Returns {data}`None` when no running path is found.
    """
    for name, path in parent_process_tree():
        if name in names and (path.startswith("/") or os.path.isabs(path)):
            return path
    return None
