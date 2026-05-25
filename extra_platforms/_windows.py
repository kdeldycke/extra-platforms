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
"""Windows process-tree inspection through the Win32 API.

Windows exposes neither ``/proc`` nor ``ps``, so the parent process tree is read
with the [Tool Help library](https://learn.microsoft.com/en-us/windows/win32/toolhelp/tool-help-library)
(a snapshot of every process) and
[``QueryFullProcessImageNameW``](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queryfullprocessimagenamew)
(to resolve executable paths).

```{note}
This module is imported lazily, and only on Windows: this keeps the `ctypes`
import out of the cold-load path, and keeps every Win32-only symbol behind a
``sys.platform == "win32"`` guard so the module stays importable as a no-op on
other platforms and type-checks under a single mypy run.
```

```{seealso}
Mirrors the Windows backend of
[shellingham](https://github.com/sarugaku/shellingham).
```
"""

from __future__ import annotations

import ctypes
import sys

if sys.platform == "win32":
    from ctypes import wintypes

    _TH32CS_SNAPPROCESS = 0x00000002
    """Tool Help snapshot flag: include all processes in the system."""

    _PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000
    """Access right sufficient for ``QueryFullProcessImageNameW`` (Vista+)."""

    _MAX_PATH = 32768
    """Buffer length for the full image path, covering extended-length paths."""

    class _ProcessEntry32W(ctypes.Structure):
        """Mirror of the Win32 ``PROCESSENTRY32W`` structure."""

        _fields_ = (
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_size_t),  # ULONG_PTR.
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),  # MAX_PATH.
        )

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    # Declare argument and return types. HANDLE is pointer-sized, so the default
    # c_int return type would truncate handles on 64-bit Windows.
    _entry_ptr = ctypes.POINTER(_ProcessEntry32W)
    _kernel32.CreateToolhelp32Snapshot.argtypes = (wintypes.DWORD, wintypes.DWORD)
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Process32FirstW.argtypes = (wintypes.HANDLE, _entry_ptr)
    _kernel32.Process32FirstW.restype = wintypes.BOOL
    _kernel32.Process32NextW.argtypes = (wintypes.HANDLE, _entry_ptr)
    _kernel32.Process32NextW.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.QueryFullProcessImageNameW.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    _kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL

    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    """Sentinel returned by ``CreateToolhelp32Snapshot`` on failure."""


def process_map() -> dict[int, tuple[int, str]]:
    """Snapshot every process as ``{pid: (ppid, executable basename)}``.

    Returns an empty mapping off Windows, or on any Win32 failure: detection
    must never raise.
    """
    if sys.platform == "win32":
        result: dict[int, tuple[int, str]] = {}
        try:
            snapshot = _kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPPROCESS, 0)
            if not snapshot or snapshot == _INVALID_HANDLE_VALUE:
                return {}
            try:
                entry = _ProcessEntry32W()
                entry.dwSize = ctypes.sizeof(_ProcessEntry32W)
                has_more = _kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
                while has_more:
                    result[entry.th32ProcessID] = (
                        entry.th32ParentProcessID,
                        entry.szExeFile,
                    )
                    has_more = _kernel32.Process32NextW(snapshot, ctypes.byref(entry))
            finally:
                _kernel32.CloseHandle(snapshot)
        except OSError:
            return {}
        return result
    else:
        return {}


def process_path(pid: int) -> str:
    """Return the full executable path of ``pid``, or an empty string.

    Empty off Windows, for inaccessible processes (owned by another user or
    elevated), or on any Win32 failure.
    """
    if sys.platform == "win32":
        try:
            handle = _kernel32.OpenProcess(
                _PROCESS_QUERY_LIMITED_INFORMATION, False, pid
            )
            if not handle:
                return ""
            try:
                size = wintypes.DWORD(_MAX_PATH)
                buffer = ctypes.create_unicode_buffer(size.value)
                ok = _kernel32.QueryFullProcessImageNameW(
                    handle, 0, buffer, ctypes.byref(size)
                )
                if ok:
                    return buffer.value
            finally:
                _kernel32.CloseHandle(handle)
        except OSError:
            return ""
        return ""
    else:
        return ""
