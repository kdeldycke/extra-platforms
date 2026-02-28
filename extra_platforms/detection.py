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
"""Heuristics to detect all traits of the current environment.

This collection of heuristics is designed as a set of separate function with minimal
logic and dependencies. They're the building blocks to evaluate the current environment.

All these heuristics can be hard-cached as the underlying system is not changing
between code execution. They are still allowed to depends on each others, as long as
you're careful of not implementing circular dependencies.

.. warning::
    Even if highly unlikely, it is possible to have multiple platforms detected for the
    same environment.

    Typical example is `Ubuntu WSL <https://documentation.ubuntu.com/wsl/>`_, which
    will make both the :func:`~extra_platforms.is_wsl2` and
    :func:`~extra_platforms.is_ubuntu` functions return ``True`` at the same time.

    That's because of the environment metadata, where:

    .. code-block:: shell-session

        $ uname -a
        Linux 5.15.167.4-microsoft-standard-WSL2

        $ cat /etc/os-release
        PRETTY_NAME="Ubuntu 22.04.5 LTS"

    That way we have the possibility elsewhere in ``extra-platforms`` to either decide
    if we only allow one, and only one, heuristic to match the current system, or allow
    for considering multiple systems at the same time.

Detection of Linux distributions relies on ``/etc/os-release``, as specified by the
`os-release specification
<https://www.freedesktop.org/software/systemd/man/latest/os-release.html>`_.
Every modern Linux distribution (since 2012) ships this file.

For all other traits, we either rely on:

- `sys.platform
  <https://docs.python.org/3/library/sys.html#sys.platform>`_
- `platform.platform
  <https://docs.python.org/3/library/platform.html#platform.platform>`_
- `platform.release
  <https://docs.python.org/3/library/platform.html#platform.release>`_
- environment variables

.. seealso::
    Other source of inspiration for platform detection:

    - `Rust's sysinfo crate
      <https://github.com/stanislav-tkach/os_info/tree/master/os_info/src>`_.

.. currentmodule:: extra_platforms
"""

from __future__ import annotations

import logging
import os
import platform
import sys
from functools import cache
from os import environ
from pathlib import Path, PurePosixPath

from .platform_info import os_release_id

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Iterable

    from .trait import CI, Agent, Architecture, Platform, Shell, Terminal, Trait


def _unrecognized_message(report: bool = True) -> str:
    """Generate a message for unrecognized environments.

    .. important::
        This message must contain all the primitives used in the ``detection`` module so
        maintainers can debug heuristics from user reports.

    :param report: If ``True``, append a request to report the issue on GitHub.
        Set to ``False`` for environments where the trait is legitimately absent
        (e.g., no terminal in CI, no CI locally).
    """
    msg = (
        "Environment:\n"
        f"  sys.platform:          {sys.platform!r}\n"
        "  platform.platform:     "
        f"{platform.platform(aliased=True, terse=True)!r}\n"
        f"  platform.release:      {platform.release()!r}\n"
        f"  platform.uname:        {platform.uname()!r}\n"
        f"  platform.machine:      {platform.machine()!r}\n"
        f"  platform.architecture: {platform.architecture()!r}\n"
        f"  os_release_id:         {os_release_id()!r}"
    )
    if report:
        msg += (
            "\n\nPlease report this at "
            "https://github.com/kdeldycke/extra-platforms/issues "
            "to improve detection heuristics."
        )
    return msg


def _report_unrecognized(
    trait_name: str,
    *,
    strict: bool,
    expected: bool = True,
) -> None:
    """Log or raise on unrecognized trait detection.

    :param trait_name: Human-readable name of the trait type (e.g., ``"architecture"``).
    :param strict: If ``True``, raise :exc:`SystemError` instead of logging.
    :param expected: If ``True``, the trait is always expected to be detected
        (architecture, platform, shell), so an unrecognized result logs a ``WARNING``
        and asks users to report the issue. If ``False`` (terminal, CI), the trait may
        legitimately be absent, so only ``INFO`` is logged without a report request.
    """
    msg = f"Unrecognized {trait_name}: {_unrecognized_message(report=expected)}"
    if strict:
        raise SystemError(msg)
    if expected:
        logging.warning(msg)
    else:
        logging.info(msg)


# =============================================================================
# Architecture detection heuristics
# =============================================================================


@cache
def is_aarch64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.AARCH64`.

    .. caution::
        ``platform.machine()`` returns different values depending on the OS:

        - Linux: ``aarch64``
        - macOS: ``arm64``
        - Windows: ``ARM64``
    """
    return platform.machine().lower() in ("aarch64", "arm64")


@cache
def is_armv5tel() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.ARMV5TEL`."""
    return platform.machine() == "armv5tel"


@cache
def is_armv6l() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.ARMV6L`."""
    return platform.machine() == "armv6l"


@cache
def is_armv7l() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.ARMV7L`."""
    return platform.machine() == "armv7l"


@cache
def is_armv8l() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.ARMV8L`."""
    return platform.machine() == "armv8l"


@cache
def is_arm() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.ARM`.

    .. hint::
        This is a fallback detection for generic ARM architecture. It will return
        ``True`` for any ARM architecture not specifically covered by the more precise
        variants: :func:`~extra_platforms.is_aarch64`, :func:`~extra_platforms.is_armv5tel`, :func:`~extra_platforms.is_armv6l`,
        :func:`~extra_platforms.is_armv7l` or :func:`~extra_platforms.is_armv8l`.
    """
    if platform.machine().startswith("arm") and not any((
        is_aarch64(),
        is_armv5tel(),
        is_armv6l(),
        is_armv7l(),
        is_armv8l(),
    )):
        return True
    return False


@cache
def is_i386() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.I386`."""
    return platform.machine() in ("i386", "i486")


@cache
def is_i586() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.I586`."""
    return platform.machine() == "i586"


@cache
def is_i686() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.I686`."""
    return platform.machine() == "i686"


@cache
def is_x86_64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.X86_64`.

    .. caution::
        Windows returns ``AMD64`` in uppercase, so we normalize to lowercase.
    """
    return platform.machine().lower() in ("x86_64", "amd64")


@cache
def is_mips() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.MIPS`."""
    return platform.machine() == "mips"


@cache
def is_mipsel() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.MIPSEL`."""
    return platform.machine() == "mipsel"


@cache
def is_mips64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.MIPS64`."""
    return platform.machine() == "mips64"


@cache
def is_mips64el() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.MIPS64EL`."""
    return platform.machine() == "mips64el"


@cache
def is_ppc() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.PPC`."""
    return platform.machine() in ("ppc", "powerpc")


@cache
def is_ppc64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.PPC64`."""
    return platform.machine() == "ppc64"


@cache
def is_ppc64le() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.PPC64LE`."""
    return platform.machine() == "ppc64le"


@cache
def is_riscv32() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.RISCV32`."""
    return platform.machine() == "riscv32"


@cache
def is_riscv64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.RISCV64`."""
    return platform.machine() == "riscv64"


@cache
def is_sparc() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.SPARC`."""
    return platform.machine() == "sparc"


@cache
def is_sparc64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.SPARC64`."""
    return platform.machine() in ("sparc64", "sun4u", "sun4v")


@cache
def is_s390x() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.S390X`."""
    return platform.machine() == "s390x"


@cache
def is_loongarch64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.LOONGARCH64`."""
    return platform.machine() == "loongarch64"


@cache
def is_wasm32() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.WASM32`.

    .. hint::
        WebAssembly detection is based on Emscripten's platform identifier.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "32bit"


@cache
def is_wasm64() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.WASM64`.

    .. hint::
        WebAssembly detection is based on Emscripten's platform identifier.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "64bit"


@cache
def is_unknown_architecture() -> bool:
    """Return :data:`True` if current architecture is :data:`~extra_platforms.UNKNOWN_ARCHITECTURE`."""
    # Lazy import to avoid circular dependencies.
    from .architecture_data import UNKNOWN_ARCHITECTURE

    return current_architecture() is UNKNOWN_ARCHITECTURE


# =============================================================================
# Platform detection heuristics
# =============================================================================


@cache
def is_aix() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.AIX`."""
    return sys.platform.startswith("aix") or os_release_id() == "aix"


@cache
def is_alpine() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ALPINE`."""
    return os_release_id() == "alpine"


@cache
def is_altlinux() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ALTLINUX`."""
    return os_release_id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.AMZN`."""
    return os_release_id() == "amzn"


@cache
def is_android() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ANDROID`.

    .. seealso::
        Source:
        <https://github.com/kivy/kivy/blob/master/kivy/utils.py>
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ARCH`."""
    return os_release_id() == "arch"


@cache
def is_buildroot() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.BUILDROOT`."""
    return os_release_id() == "buildroot"


@cache
def is_cachyos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CACHYOS`."""
    return os_release_id() == "cachyos"


@cache
def is_centos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CENTOS`."""
    return os_release_id() == "centos"


@cache
def is_cloudlinux() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CLOUDLINUX`."""
    return os_release_id() == "cloudlinux"


@cache
def is_cygwin() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CYGWIN`."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.DEBIAN`."""
    return os_release_id() == "debian"


@cache
def is_dragonfly_bsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.DRAGONFLY_BSD`."""
    return sys.platform.startswith("dragonfly")


@cache
def is_exherbo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.EXHERBO`."""
    return os_release_id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.FEDORA`."""
    return os_release_id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.FREEBSD`."""
    return sys.platform.startswith("freebsd") or os_release_id() == "freebsd"


@cache
def is_generic_linux() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.GENERIC_LINUX`.

    Matches when running on a Linux kernel but ``distro`` cannot identify the specific
    distribution (e.g., minimal containers or build chroots without ``/etc/os-release``).
    """
    return sys.platform == "linux" and not os_release_id()


@cache
def is_gentoo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.GENTOO`."""
    return os_release_id() == "gentoo"


@cache
def is_guix() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.GUIX`."""
    return os_release_id() == "guix"


@cache
def is_haiku() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.HAIKU`."""
    return sys.platform.startswith("haiku")


@cache
def is_hurd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.HURD`.

    .. caution::
        ``sys.platform`` can returns ``GNU`` or ``gnu0``, see:
        <https://github.com/kdeldycke/extra-platforms/issues/308>
    """
    return sys.platform.lower().startswith("gnu")


@cache
def is_ibm_powerkvm() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.IBM_POWERKVM`."""
    return os_release_id() == "ibm_powerkvm"


@cache
def is_illumos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ILLUMOS`.

    .. hint::
        Illumos is a Unix OS derived from OpenSolaris. It shares
        ``sys.platform == 'sunos5'`` with Solaris, but can be distinguished by checking
        ``platform.uname().version`` which contains "illumos" on Illumos-based systems
        (like OpenIndiana, SmartOS, OmniOS).
    """
    return "illumos" in platform.uname().version.lower()


@cache
def is_kali() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.KALI`."""
    return os_release_id() == "kali"


@cache
def is_kvmibm() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.KVMIBM`."""
    return os_release_id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.LINUXMINT`."""
    return os_release_id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MACOS`."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MAGEIA`."""
    return os_release_id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MANDRIVA`."""
    return os_release_id() == "mandriva"


@cache
def is_manjaro() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MANJARO`."""
    return os_release_id() == "manjaro"


@cache
def is_midnightbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MIDNIGHTBSD`."""
    return sys.platform.startswith("midnightbsd") or os_release_id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.NETBSD`."""
    return sys.platform.startswith("netbsd") or os_release_id() == "netbsd"


@cache
def is_nobara() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.NOBARA`."""
    return os_release_id() == "nobara"


@cache
def is_openbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.OPENBSD`."""
    return sys.platform.startswith("openbsd") or os_release_id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.OPENSUSE`."""
    return os_release_id() == "opensuse"


@cache
def is_openwrt() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.OPENWRT`."""
    return os_release_id() == "openwrt"


@cache
def is_oracle() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ORACLE`."""
    return os_release_id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.PARALLELS`."""
    return os_release_id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.PIDORA`."""
    return os_release_id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.RASPBIAN`."""
    return os_release_id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.RHEL`."""
    return os_release_id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ROCKY`."""
    return os_release_id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SCIENTIFIC`."""
    return os_release_id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SLACKWARE`."""
    return os_release_id() == "slackware"


@cache
def is_sles() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SLES`."""
    return os_release_id() == "sles"


@cache
def is_solaris() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SOLARIS`."""
    return platform.platform(aliased=True, terse=True).startswith("Solaris")


@cache
def is_sunos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SUNOS`."""
    return platform.platform(aliased=True, terse=True).startswith("SunOS")


@cache
def is_tumbleweed() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.TUMBLEWEED`."""
    return os_release_id() == "opensuse-tumbleweed"


@cache
def is_tuxedo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.TUXEDO`."""
    return os_release_id() == "tuxedo"


@cache
def is_ubuntu() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.UBUNTU`."""
    return os_release_id() == "ubuntu"


@cache
def is_ultramarine() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ULTRAMARINE`."""
    return os_release_id() == "ultramarine"


@cache
def is_windows() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.WINDOWS`."""
    return sys.platform.startswith("win32")


@cache
def is_wsl1() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.WSL1`.

    .. caution::
        The only difference between WSL1 and WSL2 is `the case of the kernel release
        version <https://github.com/andweeb/presence.nvim/pull/64#issue-1174430662>`_:

        - WSL 1:

          .. code-block:: shell-session

                $ uname -r
                4.4.0-22572-Microsoft

        - WSL 2:

          .. code-block:: shell-session

                $ uname -r
                5.10.102.1-microsoft-standard-WSL2
    """
    return "Microsoft" in platform.release()


@cache
def is_wsl2() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.WSL2`."""
    return "microsoft" in platform.release()


@cache
def is_xenserver() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.XENSERVER`."""
    return os_release_id() == "xenserver"


@cache
def is_unknown_platform() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.UNKNOWN_PLATFORM`."""
    # Lazy import to avoid circular dependencies.
    from .platform_data import UNKNOWN_PLATFORM

    return current_platform() is UNKNOWN_PLATFORM


# =============================================================================
# Shell detection heuristics
# =============================================================================


@cache
def _parent_process_shells(shell_ids: str | tuple[str, ...]) -> bool:
    """Check if any parent process in the tree matches the given shell IDs.

    On Linux, reads ``/proc/<pid>/exe`` symlinks up the process tree via
    ``/proc/<pid>/stat`` to find the parent PID. This identifies the *active*
    shell, not merely installed ones.

    Args:
        shell_ids: Shell executable name(s) to match. Can be a single string
            (e.g., ``"bash"``) or a tuple of strings (e.g., ``("powershell", "pwsh")``).

    Returns:
        ``True`` if a matching shell is found in the parent process tree,
        ``False`` otherwise or on non-Linux platforms where ``/proc`` is unavailable.
    """
    # Normalize shell_ids to a set for efficient lookup.
    id_set = (
        frozenset({shell_ids}) if isinstance(shell_ids, str) else frozenset(shell_ids)
    )

    try:
        pid = os.getpid()
        visited: set[int] = set()
        while pid > 1 and pid not in visited:
            visited.add(pid)
            # Read the executable path of the process.
            try:
                exe = Path(os.readlink(f"/proc/{pid}/exe")).stem.lower()
                if exe in id_set:
                    return True
            except OSError:
                pass
            # Read the parent PID from /proc/<pid>/stat.
            try:
                stat_content = Path(f"/proc/{pid}/stat").read_text()
                # Format: "pid (comm) state ppid ...". The comm field may
                # contain spaces and parentheses, so find the last ')'.
                ppid_str = stat_content[stat_content.rfind(")") + 2 :].split()[1]
                pid = int(ppid_str)
            except (OSError, ValueError, IndexError):
                break
    except OSError:
        pass
    return False


def _detect_shell(
    version_env_var: str | None = None,
    shell_ids: str | Iterable[str] | None = None,
) -> bool:
    """Detect a specific shell from the environment.

    .. caution::
        This function is designed primarily for POSIX/Unix systems. The ``SHELL``
        environment variable and ``/proc`` filesystem are Unix-specific conventions.
        For Windows shells like :data:`~extra_platforms.CMD`, use platform-specific
        detection instead.

    Uses a tiered detection strategy:

    1. Checks for shell-specific version environment variable (most reliable).
    2. Parses the ``SHELL`` environment variable path against known shell executable
       names.
    3. Falls back to walking the parent process tree via ``/proc`` to find the
       active shell (for stripped environments without shell env vars).

    Args:
        version_env_var: Shell-specific environment variable name
            (e.g., ``"BASH_VERSION"``).
        shell_ids: Shell executable name(s) to match. Can be a single string
            (e.g., ``"bash"``) or a tuple of strings (e.g., ``("powershell", "pwsh")``).

    Returns:
        ``True`` if the shell is detected, ``False`` otherwise.
    """
    # Check shell-specific version environment variable.
    if version_env_var and version_env_var in environ:
        return True

    # Normalize shell_ids for consistent handling.
    if shell_ids is None:
        return False

    ids = (
        frozenset((shell_ids,)) if isinstance(shell_ids, str) else frozenset(shell_ids)
    )

    # Check SHELL environment variable against known shell IDs.
    shell_path = environ.get("SHELL", "")
    if shell_path:
        shell_id = PurePosixPath(shell_path).stem.lower()
        if shell_id in ids:
            return True

    # Fallback: walk the parent process tree to find the active shell. This
    # covers two cases:
    # - SHELL is not set at all (stripped containers like ubuntu-slim).
    # - SHELL is set to a generic value like /bin/sh that doesn't match any
    #   specific shell (e.g. ubuntu-24.04-arm where SHELL=/bin/sh but the
    #   GitHub Actions runner actually executes steps via /usr/bin/bash).
    normalized_ids = (shell_ids,) if isinstance(shell_ids, str) else tuple(shell_ids)
    return _parent_process_shells(normalized_ids)


@cache
def is_ash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.ASH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path, as Almquist
        Shell does not set its own version variable.

    .. note::
        `BusyBox <https://busybox.net>`_'s built-in shell is an :data:`~extra_platforms.ASH`
        derivative. On BusyBox-based systems (:data:`~extra_platforms.ALPINE`,
        :data:`~extra_platforms.OPENWRT`), ``$SHELL`` typically resolves to ``/bin/ash``,
        so BusyBox environments are detected as :data:`~extra_platforms.ASH`.
    """
    return _detect_shell(shell_ids="ash")


@cache
def is_bash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.BASH`.

    .. hint::
        Detected via the ``BASH_VERSION`` environment variable (set by Bash
        on startup), or via the ``SHELL`` path as a fallback.

    .. attention::
        GitHub's ``ubuntu-slim`` runner is a `stripped-down environments, running as
        a WSL2 container <https://docs.github.com/en/actions/reference/runners/github-hosted-runners#single-cpu-runners>`_
        on top of Windows. It `uses Bash as the default shell <https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md>`_,
        but does not set neither ``BASH_VERSION`` nor ``SHELL``.
        In that case we fall back to walking the parent process tree via ``/proc`` to find it.
    """
    return _detect_shell(version_env_var="BASH_VERSION", shell_ids="bash")


@cache
def is_cmd() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.CMD`.

    .. hint::
        Detected on Windows when the ``PROMPT`` environment variable is set
        and ``PSModulePath`` is not (to exclude PowerShell).
    """
    return (
        sys.platform == "win32"
        and "PROMPT" in environ
        and "PSModulePath" not in environ
    )


@cache
def is_csh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.CSH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path.
    """
    return _detect_shell(shell_ids="csh")


@cache
def is_dash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.DASH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path, as Dash does
        not set its own version variable.
    """
    return _detect_shell(shell_ids="dash")


@cache
def is_fish() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.FISH`.

    .. hint::
        Detected via the ``FISH_VERSION`` environment variable (set by Fish
        on startup), or via the ``SHELL`` path as a fallback.
    """
    return _detect_shell(version_env_var="FISH_VERSION", shell_ids="fish")


@cache
def is_ksh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.KSH`.

    .. hint::
        Detected via the ``KSH_VERSION`` environment variable (set by Korn
        shell on startup), or via the ``SHELL`` path as a fallback.
    """
    return _detect_shell(version_env_var="KSH_VERSION", shell_ids="ksh")


@cache
def is_nushell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.NUSHELL`.

    .. hint::
        Detected via the ``NU_VERSION`` environment variable (set by Nushell
        on startup), or via the ``SHELL`` path as a fallback.
    """
    return _detect_shell(version_env_var="NU_VERSION", shell_ids="nu")


@cache
def is_powershell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.POWERSHELL`.

    .. note::
        PowerShell is cross-platform and `available on Linux
        <https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-linux>`_
        and macOS. Detection covers all platforms via ``PSModulePath``,
        ``SHELL`` path, and parent process tree.

    .. attention::
        ``PSModulePath`` can leak into non-PowerShell child processes via two
        vectors:

        1. **Process-level inheritance** (all platforms): PowerShell modifies
           ``PSModulePath`` at startup, and `all non-PowerShell children inherit
           it <https://github.com/PowerShell/PowerShell/issues/9957>`_.
        2. **System-wide registry variable** (Windows only): ``PSModulePath``
           is a `persistent machine-level environment variable
           <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_psmodulepath>`_
           visible to all processes.

        This is the case for all GitHub Ubuntu runners, where
        ``PSModulePath`` leaks from Azure infrastructure. This leads to multiple
        shell detections, which is arbitraged by ``current_shell()``, which deprioritizes PowerShell when other shells are detected.
    """
    return _detect_shell(
        version_env_var="PSModulePath",
        shell_ids=("powershell", "powershell_ise", "pwsh"),
    )


@cache
def is_tcsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.TCSH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path.
    """
    return _detect_shell(shell_ids="tcsh")


@cache
def is_xonsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.XONSH`.

    .. hint::
        Detected via the ``XONSH_VERSION`` environment variable (set by Xonsh
        on startup), or via the ``SHELL`` path as a fallback.
    """
    return _detect_shell(version_env_var="XONSH_VERSION", shell_ids="xonsh")


@cache
def is_zsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.ZSH`.

    .. hint::
        Detected via the ``ZSH_VERSION`` environment variable (set by Zsh on
        startup), or via the ``SHELL`` path as a fallback.
    """
    return _detect_shell(version_env_var="ZSH_VERSION", shell_ids="zsh")


@cache
def is_unknown_shell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.UNKNOWN_SHELL`."""
    # Lazy import to avoid circular dependencies.
    from .shell_data import UNKNOWN_SHELL

    return current_shell() is UNKNOWN_SHELL


# =============================================================================
# Terminal detection heuristics
# =============================================================================


@cache
def is_alacritty() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.ALACRITTY`."""
    return "ALACRITTY_SOCKET" in environ or "ALACRITTY_WINDOW_ID" in environ


@cache
def is_apple_terminal() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.APPLE_TERMINAL`."""
    return environ.get("TERM_PROGRAM") == "Apple_Terminal"


@cache
def is_contour() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.CONTOUR`."""
    return environ.get("TERMINAL_NAME") == "contour"


@cache
def is_foot() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.FOOT`."""
    return environ.get("TERM", "").startswith("foot")


@cache
def is_ghostty() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.GHOSTTY`."""
    return "GHOSTTY_RESOURCES_DIR" in environ


@cache
def is_gnome_terminal() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.GNOME_TERMINAL`."""
    return "GNOME_TERMINAL_SCREEN" in environ


@cache
def is_gnu_screen() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.GNU_SCREEN`."""
    return "STY" in environ


@cache
def is_hyper() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.HYPER`."""
    return environ.get("TERM_PROGRAM") == "Hyper"


@cache
def is_iterm2() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.ITERM2`."""
    return "ITERM_SESSION_ID" in environ or environ.get("TERM_PROGRAM") == "iTerm.app"


@cache
def is_kitty() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.KITTY`."""
    return "KITTY_WINDOW_ID" in environ


@cache
def is_konsole() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.KONSOLE`."""
    return "KONSOLE_VERSION" in environ


@cache
def is_rio() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.RIO`."""
    return "RIO_WINDOW_ID" in environ


@cache
def is_tabby() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.TABBY`."""
    return "TABBY" in environ or environ.get("TERM_PROGRAM") == "Tabby"


@cache
def is_tilix() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.TILIX`."""
    return "TILIX_ID" in environ


@cache
def is_tmux() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.TMUX`."""
    return "TMUX" in environ


@cache
def is_unknown_terminal() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.UNKNOWN_TERMINAL`."""
    # Lazy import to avoid circular dependencies.
    from .terminal_data import UNKNOWN_TERMINAL

    return current_terminal() is UNKNOWN_TERMINAL


@cache
def is_vscode_terminal() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.VSCODE_TERMINAL`."""
    return environ.get("TERM_PROGRAM") == "vscode"


@cache
def is_wezterm() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.WEZTERM`."""
    return "WEZTERM_EXECUTABLE" in environ


@cache
def is_windows_terminal() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.WINDOWS_TERMINAL`."""
    return "WT_SESSION" in environ


@cache
def is_xterm() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.XTERM`.

    .. note::
        We check for ``XTERM_VERSION`` rather than ``TERM=xterm`` because many
        headless environments (e.g., GitHub Actions ``ubuntu-slim`` runners) set
        ``TERM=xterm`` for termcap/terminfo compatibility without actually running
        xterm.
    """
    return "XTERM_VERSION" in environ


@cache
def is_zellij() -> bool:
    """Return :data:`True` if current terminal is :data:`~extra_platforms.ZELLIJ`."""
    return "ZELLIJ" in environ


# =============================================================================
# CI/CD detection heuristics
# =============================================================================


@cache
def is_azure_pipelines() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.AZURE_PIPELINES`.

    .. seealso::
        Environment variables reference:
        <https://learn.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&viewFallbackFrom=vsts&tabs=yaml#system-variables>.
    """
    return "TF_BUILD" in environ


@cache
def is_bamboo() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.BAMBOO`.

    .. seealso::
        Environment variables reference:
        <https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html#Bamboovariables-Build-specificvariables>.
    """
    return "bamboo.buildKey" in environ


@cache
def is_buildkite() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.BUILDKITE`.

    .. seealso::
        Environment variables reference:
        <https://buildkite.com/docs/pipelines/environment-variables>.
    """
    return "BUILDKITE" in environ


@cache
def is_circle_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.CIRCLE_CI`.

    .. seealso::
        Environment variables reference:
        <https://circleci.com/docs/reference/variables/#built-in-environment-variables>.
    """
    return "CIRCLECI" in environ


@cache
def is_cirrus_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.CIRRUS_CI`.

    .. seealso::
        Environment variables reference:
        <https://cirrus-ci.org/guide/writing-tasks/#environment-variables>.
    """
    return "CIRRUS_CI" in environ


@cache
def is_codebuild() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.CODEBUILD`.

    .. seealso::
        Environment variables reference:
        <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html>.
    """
    return "CODEBUILD_BUILD_ID" in environ


@cache
def is_github_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.GITHUB_CI`.

    .. seealso::
        Environment variables reference:
        <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables>.
    """
    return "GITHUB_ACTIONS" in environ or "GITHUB_RUN_ID" in environ


@cache
def is_gitlab_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.GITLAB_CI`.

    .. seealso::
        Environment variables reference:
        <https://docs.gitlab.com/ci/variables/predefined_variables/#predefined-variables>.
    """
    return "GITLAB_CI" in environ


@cache
def is_heroku_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.HEROKU_CI`.

    .. seealso::
        Environment variables reference:
        <https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables>.
    """
    return "HEROKU_TEST_RUN_ID" in environ


@cache
def is_teamcity() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.TEAMCITY`.

    .. seealso::
        Environment variables reference:
        <https://www.jetbrains.com/help/teamcity/predefined-build-parameters.html#Predefined+Server+Build+Parameters>.
    """
    return "TEAMCITY_VERSION" in environ


@cache
def is_travis_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.TRAVIS_CI`.

    .. seealso::
        Environment variables reference:
        <https://docs.travis-ci.com/user/environment-variables/#default-environment-variables>.
    """
    return "TRAVIS" in environ


@cache
def is_unknown_ci() -> bool:
    """Return :data:`True` if current CI is :data:`~extra_platforms.UNKNOWN_CI`."""
    # Lazy import to avoid circular dependencies.
    from .ci_data import UNKNOWN_CI

    return current_ci() is UNKNOWN_CI


# =============================================================================
# Agent detection heuristics
# =============================================================================


@cache
def is_claude_code() -> bool:
    """Return :data:`True` if current agent is :data:`~extra_platforms.CLAUDE_CODE`.

    .. seealso::
        Claude Code sets the ``CLAUDECODE`` environment variable when running.
    """
    return "CLAUDECODE" in environ


@cache
def is_cline() -> bool:
    """Return :data:`True` if current agent is :data:`~extra_platforms.CLINE`.

    .. seealso::
        Cline sets the ``CLINE_ACTIVE`` environment variable when running.
    """
    return "CLINE_ACTIVE" in environ


@cache
def is_cursor() -> bool:
    """Return :data:`True` if current agent is :data:`~extra_platforms.CURSOR`.

    .. seealso::
        Cursor sets the ``CURSOR_AGENT`` environment variable when running.
    """
    return "CURSOR_AGENT" in environ


@cache
def is_unknown_agent() -> bool:
    """Return :data:`True` if current agent is :data:`~extra_platforms.UNKNOWN_AGENT`."""
    # Lazy import to avoid circular dependencies.
    from .agent_data import UNKNOWN_AGENT

    return current_agent() is UNKNOWN_AGENT


# =============================================================================
# Current environment detection
# =============================================================================


@cache
def current_architecture(strict: bool = False) -> Architecture:
    """Returns the :class:`~extra_platforms.Architecture` matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_ARCHITECTURE` if not running inside a
    recognized architecture. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        Always raises an error if multiple architectures match.

    .. warning::
        An architecture is always expected to be detected. An unrecognized result
        logs a ``WARNING`` and likely indicates a missing detection heuristic that
        should be `reported <https://github.com/kdeldycke/extra-platforms/issues>`_.
    """
    # Lazy imports to avoid circular dependencies.
    from .architecture_data import UNKNOWN_ARCHITECTURE
    from .group_data import ALL_ARCHITECTURES

    # Collect all matching architectures.
    matching: set[Architecture] = {
        arch  # type: ignore[misc]
        for arch in ALL_ARCHITECTURES
        if arch.current
    }

    # Return the only matching architecture.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple architectures matches: {matching!r}. {_unrecognized_message()}"
        )

    _report_unrecognized("architecture", strict=strict)
    return UNKNOWN_ARCHITECTURE


@cache
def current_platform(strict: bool = False) -> Platform:
    """Always returns the best matching :class:`~extra_platforms.Platform` for the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_PLATFORM` if not running inside a recognized
    platform. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        If multiple platforms match the current environment, this function will try to
        select the best, informative one. Raises an error if we can't decide on a single,
        appropriate platform.

    .. warning::
        A platform is always expected to be detected. An unrecognized result logs a
        ``WARNING`` and likely indicates a missing detection heuristic that should be
        `reported <https://github.com/kdeldycke/extra-platforms/issues>`_.
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_PLATFORMS
    from .platform_data import GENERIC_LINUX, UNKNOWN_PLATFORM, WSL1, WSL2

    # Collect all matching platforms.
    matching: set[Platform] = {
        plat  # type: ignore[misc]
        for plat in ALL_PLATFORMS
        if plat.current
    }

    # Return the only matching platform.
    if len(matching) == 1:
        (result,) = matching
        if result is GENERIC_LINUX:
            _report_unrecognized("Linux distribution", strict=False)
        return result

    # Removes some generic platforms from the matching, until we have a single match.
    # Starts by removing the least specific WSL1, then WSL2: WSL is a generic platform,
    # so we should prefer the remaining, more specific platform matches like Ubuntu. See:
    # - https://github.com/kdeldycke/extra-platforms/issues/158
    # - https://github.com/kdeldycke/meta-package-manager/issues/944
    for wsl in (WSL1, WSL2):
        if wsl in matching:
            matching.remove(wsl)
            if len(matching) == 1:
                return matching.pop()

    # Remove GENERIC_LINUX if a more specific platform was also detected.
    if GENERIC_LINUX in matching and len(matching) > 1:
        matching.remove(GENERIC_LINUX)
        if len(matching) == 1:
            return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple platforms matches: {matching!r}. {_unrecognized_message()}"
        )

    _report_unrecognized("platform", strict=strict)
    return UNKNOWN_PLATFORM


@cache
def current_shell(strict: bool = False) -> Shell:
    """Returns the :class:`~extra_platforms.Shell` matching the current environment.

    Uses a tiered detection strategy:

    1. Shell-specific environment variables (detects active shell).
    2. ``SHELL`` environment variable (detects login shell on Unix).
    3. Windows defaults (``PROMPT`` → :data:`~extra_platforms.CMD`, else → :data:`~extra_platforms.POWERSHELL`).

    Returns :data:`~extra_platforms.UNKNOWN_SHELL` if not running inside a
    recognized shell. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        If both :data:`~extra_platforms.POWERSHELL` and another shell are detected (because
        ``PSModulePath`` `leaks into child processes
        <https://github.com/PowerShell/PowerShell/issues/9957>`_), the other
        shell is preferred.

    .. warning::
        A shell is always expected to be detected. An unrecognized result logs a
        ``WARNING`` and likely indicates a missing detection heuristic that should be
        `reported <https://github.com/kdeldycke/extra-platforms/issues>`_.

    .. seealso::
        Inspired by `UV's cross-platform shell detection
        <https://github.com/astral-sh/uv/blob/0.10.2/crates/uv-shell/src/lib.rs>`_.
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_SHELLS
    from .shell_data import POWERSHELL, UNKNOWN_SHELL

    # Collect all matching shells.
    matching: set[Shell] = {
        shell  # type: ignore[misc]
        for shell in ALL_SHELLS
        if shell.current
    }

    # Return the only matching shell.
    if len(matching) == 1:
        return matching.pop()

    # If PowerShell is detected alongside another shell, prefer the other.
    if POWERSHELL in matching and len(matching) > 1:
        matching.discard(POWERSHELL)
        if len(matching) == 1:
            return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple shells matches: {matching!r}. {_unrecognized_message()}"
        )

    _report_unrecognized("shell", strict=strict)
    return UNKNOWN_SHELL


@cache
def current_terminal(strict: bool = False) -> Terminal:
    """Returns the :class:`~extra_platforms.Terminal` matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_TERMINAL` if not running inside a
    recognized terminal. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        If multiple terminals match (e.g., :data:`~extra_platforms.TMUX` inside
        :data:`~extra_platforms.KITTY`), multiplexers are filtered out first to
        identify the innermost terminal. If multiple non-multiplexer terminals still
        match, a :class:`RuntimeError` is raised.

    .. note::
        Unlike architectures, platforms, and shells, a terminal is not always present.
        Headless environments (CI runners, cron jobs, Docker containers, SSH
        non-interactive commands) have no terminal emulator attached.

        If the ``TERM`` environment variable is set, an unrecognized terminal logs at
        ``WARNING`` level, as it suggests a terminal emulator is present but not
        recognized. Otherwise, it logs at ``INFO`` level.
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_TERMINALS, MULTIPLEXERS
    from .terminal_data import UNKNOWN_TERMINAL

    # Collect all matching terminals.
    matching: set[Terminal] = {
        term  # type: ignore[misc]
        for term in ALL_TERMINALS
        if term.current
    }

    # Return the only matching terminal.
    if len(matching) == 1:
        return matching.pop()

    # If multiple terminals match, filter out multiplexers to find the innermost.
    if len(matching) > 1:
        non_mux = {t for t in matching if t not in MULTIPLEXERS}
        if len(non_mux) == 1:
            return non_mux.pop()
        raise RuntimeError(
            f"Multiple terminals matches: {matching!r}. {_unrecognized_message()}"
        )

    # TERM env var signals a terminal emulator is present.
    if "TERM" in environ:
        _report_unrecognized("terminal", strict=strict)
    else:
        _report_unrecognized("terminal", strict=strict, expected=False)
    return UNKNOWN_TERMINAL


@cache
def current_ci(strict: bool = False) -> CI:
    """Returns the :class:`~extra_platforms.CI` system matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_CI` if not running inside a recognized CI
    system. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        Always raises an error if multiple CI systems match.

    .. note::
        Unlike architectures, platforms, and shells, a CI system is not always present.
        Local development environments have no CI system running.

        If the ``CI`` environment variable is set, an unrecognized CI system logs at
        ``WARNING`` level, as it suggests a CI system is present but not recognized.
        Otherwise, it logs at ``INFO`` level.
    """
    # Lazy imports to avoid circular dependencies.
    from .ci_data import UNKNOWN_CI
    from .group_data import ALL_CI

    # Collect all matching CI systems.
    matching: set[CI] = {ci for ci in ALL_CI if ci.current}  # type: ignore[misc]

    # Return the only matching CI system.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple CI matches: {matching!r}. {_unrecognized_message()}"
        )

    # CI env var signals a CI system is present.
    if "CI" in environ:
        _report_unrecognized("CI", strict=strict)
    else:
        _report_unrecognized("CI", strict=strict, expected=False)
    return UNKNOWN_CI


@cache
def current_agent(strict: bool = False) -> Agent:
    """Returns the :class:`~extra_platforms.Agent` matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_AGENT` if not running inside a recognized
    agent. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        Always raises an error if multiple agents match.

    .. note::
        Unlike architectures, platforms, and shells, an agent is not always present.
        Local development without AI agents has no agent running.

        If the ``LLM`` environment variable is set, an unrecognized agent logs at
        ``WARNING`` level, as it suggests an AI agent is present but not recognized.
        Otherwise, it logs at ``INFO`` level.
    """
    # Lazy imports to avoid circular dependencies.
    from .agent_data import UNKNOWN_AGENT
    from .group_data import ALL_AGENTS

    # Collect all matching agents.
    matching: set[Agent] = {
        agent  # type: ignore[misc]
        for agent in ALL_AGENTS
        if agent.current
    }

    # Return the only matching agent.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple agent matches: {matching!r}. {_unrecognized_message()}"
        )

    # LLM env var signals an AI agent is present.
    if "LLM" in environ:
        _report_unrecognized("agent", strict=strict)
    else:
        _report_unrecognized("agent", strict=strict, expected=False)
    return UNKNOWN_AGENT


@cache
def current_traits() -> set[Trait]:
    """Returns all traits matching the current environment.

    This includes :class:`~extra_platforms.Architecture`,
    :class:`~extra_platforms.Platform`, :class:`~extra_platforms.Shell`,
    :class:`~extra_platforms.Terminal`, :class:`~extra_platforms.CI` systems,
    and :class:`~extra_platforms.Agent` environments.

    .. caution::
        Never returns :data:`~extra_platforms.UNKNOWN` traits.

    Raises :exc:`SystemError` if the current environment is not recognized at all.

    .. attention::
        At this point it is too late to worry about caching. This function has no
        choice but to evaluate all detection heuristics.
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_TRAITS, UNKNOWN

    # Collect all matching traits.
    matching = {trait for trait in ALL_TRAITS - UNKNOWN if trait.current}

    if not matching:
        raise SystemError(f"Unrecognized environment: {_unrecognized_message()}")

    return matching
