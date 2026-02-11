# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
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

Detection of Linux distribution rely on `distro
<https://github.com/python-distro/distro>`_ to gather as much details as possible.
And also because it is the recommended replacement for Python's original
``platform.linux_distribution`` function (which was removed in Python 3.8).

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
import platform
import sys
from functools import cache
from os import environ
from pathlib import PurePosixPath

import distro

TYPE_CHECKING = False
if TYPE_CHECKING:
    from .trait import CI, Architecture, Platform, Shell, Trait


@cache
def _unrecognized_message() -> str:
    """Generate a consistent message for unrecognized environments.

    .. important::
        This message must contain all the primitives used in the ``detection`` module so
        maintainers can debug heuristics from user reports.
    """
    return (
        "Environment:\n"
        f"  sys.platform:          {sys.platform!r}\n"
        "  platform.platform:     "
        f"{platform.platform(aliased=True, terse=True)!r}\n"
        f"  platform.release:      {platform.release()!r}\n"
        f"  platform.uname:        {platform.uname()!r}\n"
        f"  platform.machine:      {platform.machine()!r}\n"
        f"  platform.architecture: {platform.architecture()!r}\n"
        f"  distro.id:             {distro.id()!r}\n"
        "\nPlease report this at https://github.com/kdeldycke/extra-platforms/issues to "
        "improve detection heuristics."
    )


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
    return sys.platform.startswith("aix") or distro.id() == "aix"


@cache
def is_altlinux() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ALTLINUX`."""
    return distro.id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.AMZN`."""
    return distro.id() == "amzn"


@cache
def is_android() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ANDROID`.

    .. seealso::
        Source:
        <https://github.com/kivy/kivy/blob/3c4b1dc84cdd930d352aab9be32c38e1c98bd5c6/kivy/utils.py#L435-L436>
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ARCH`."""
    return distro.id() == "arch"


@cache
def is_buildroot() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.BUILDROOT`."""
    return distro.id() == "buildroot"


@cache
def is_cachyos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CACHYOS`."""
    return distro.id() == "cachyos"


@cache
def is_centos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CENTOS`."""
    return distro.id() == "centos"


@cache
def is_cloudlinux() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CLOUDLINUX`."""
    return distro.id() == "cloudlinux"


@cache
def is_cygwin() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.CYGWIN`."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.DEBIAN`."""
    return distro.id() == "debian"


@cache
def is_dragonfly_bsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.DRAGONFLY_BSD`."""
    return sys.platform.startswith("dragonfly")


@cache
def is_exherbo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.EXHERBO`."""
    return distro.id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.FEDORA`."""
    return distro.id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.FREEBSD`."""
    return sys.platform.startswith("freebsd") or distro.id() == "freebsd"


@cache
def is_gentoo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.GENTOO`."""
    return distro.id() == "gentoo"


@cache
def is_guix() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.GUIX`."""
    return distro.id() == "guix"


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
    return distro.id() == "ibm_powerkvm"


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
def is_kvmibm() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.KVMIBM`."""
    return distro.id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.LINUXMINT`."""
    return distro.id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MACOS`."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MAGEIA`."""
    return distro.id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MANDRIVA`."""
    return distro.id() == "mandriva"


@cache
def is_midnightbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.MIDNIGHTBSD`."""
    return sys.platform.startswith("midnightbsd") or distro.id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.NETBSD`."""
    return sys.platform.startswith("netbsd") or distro.id() == "netbsd"


@cache
def is_nobara() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.NOBARA`."""
    return distro.id() == "nobara"


@cache
def is_openbsd() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.OPENBSD`."""
    return sys.platform.startswith("openbsd") or distro.id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.OPENSUSE`."""
    return distro.id() == "opensuse"


@cache
def is_oracle() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ORACLE`."""
    return distro.id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.PARALLELS`."""
    return distro.id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.PIDORA`."""
    return distro.id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.RASPBIAN`."""
    return distro.id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.RHEL`."""
    return distro.id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ROCKY`."""
    return distro.id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SCIENTIFIC`."""
    return distro.id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SLACKWARE`."""
    return distro.id() == "slackware"


@cache
def is_sles() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.SLES`."""
    return distro.id() == "sles"


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
    return distro.id() == "opensuse-tumbleweed"


@cache
def is_tuxedo() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.TUXEDO`."""
    return distro.id() == "tuxedo"


@cache
def is_ubuntu() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.UBUNTU`."""
    return distro.id() == "ubuntu"


@cache
def is_ultramarine() -> bool:
    """Return :data:`True` if current platform is :data:`~extra_platforms.ULTRAMARINE`."""
    return distro.id() == "ultramarine"


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
    return distro.id() == "xenserver"


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
def _parse_shell_from_path(shell_path: str) -> str | None:
    """Extract shell ID from a shell executable path.

    Parses the ``SHELL`` environment variable or process path to identify
    the shell.
    """
    stem = PurePosixPath(shell_path).stem.lower()
    return {
        "ash": "ash",
        "bash": "bash",
        "csh": "csh",
        "dash": "dash",
        "fish": "fish",
        "ksh": "ksh",
        "nu": "nushell",
        "powershell": "powershell",
        "powershell_ise": "powershell",
        "pwsh": "powershell",
        "tcsh": "tcsh",
        "xonsh": "xonsh",
        "zsh": "zsh",
    }.get(stem)


@cache
def is_ash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.ASH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path, as Almquist
        Shell does not set its own version variable.
    """
    return _parse_shell_from_path(environ.get("SHELL", "")) == "ash"


@cache
def is_bash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.BASH`.

    .. hint::
        Detected via the ``BASH_VERSION`` environment variable (set by Bash
        on startup), or via the ``SHELL`` path as a fallback.
    """
    return "BASH_VERSION" in environ or (
        _parse_shell_from_path(environ.get("SHELL", "")) == "bash"
    )


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
    return _parse_shell_from_path(environ.get("SHELL", "")) == "csh"


@cache
def is_dash() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.DASH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path, as Dash does
        not set its own version variable.
    """
    return _parse_shell_from_path(environ.get("SHELL", "")) == "dash"


@cache
def is_fish() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.FISH`.

    .. hint::
        Detected via the ``FISH_VERSION`` environment variable (set by Fish
        on startup), or via the ``SHELL`` path as a fallback.
    """
    return "FISH_VERSION" in environ or (
        _parse_shell_from_path(environ.get("SHELL", "")) == "fish"
    )


@cache
def is_ksh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.KSH`.

    .. hint::
        Detected via the ``KSH_VERSION`` environment variable (set by Korn
        shell on startup), or via the ``SHELL`` path as a fallback.
    """
    return "KSH_VERSION" in environ or (
        _parse_shell_from_path(environ.get("SHELL", "")) == "ksh"
    )


@cache
def is_nushell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.NUSHELL`.

    .. hint::
        Detected via the ``NU_VERSION`` environment variable, which is set
        by Nushell on startup.
    """
    return "NU_VERSION" in environ


@cache
def is_powershell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.POWERSHELL`.

    .. caution::
        ``PSModulePath`` can leak into non-PowerShell child processes via two
        vectors:

        1. **Process-level inheritance** (all platforms): PowerShell modifies
           ``PSModulePath`` at startup, and `all non-PowerShell children inherit
           it <https://github.com/PowerShell/PowerShell/issues/9957>`_.
        2. **System-wide registry variable** (Windows only): ``PSModulePath``
           is a `persistent machine-level environment variable
           <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_psmodulepath>`_
           visible to all processes.

        Because of this, ``PSModulePath`` is checked last among environment
        variable-based shells. If another shell is also detected, prefer that
        shell.
    """
    return "PSModulePath" in environ


@cache
def is_tcsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.TCSH`.

    .. hint::
        Detected via the ``SHELL`` environment variable path.
    """
    return _parse_shell_from_path(environ.get("SHELL", "")) == "tcsh"


@cache
def is_xonsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.XONSH`.

    .. hint::
        Detected via the ``XONSH_VERSION`` environment variable, which is set
        by Xonsh on startup.
    """
    return "XONSH_VERSION" in environ


@cache
def is_zsh() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.ZSH`.

    .. hint::
        Detected via the ``ZSH_VERSION`` environment variable (set by Zsh on
        startup), or via the ``SHELL`` path as a fallback.
    """
    return "ZSH_VERSION" in environ or (
        _parse_shell_from_path(environ.get("SHELL", "")) == "zsh"
    )


@cache
def is_unknown_shell() -> bool:
    """Return :data:`True` if current shell is :data:`~extra_platforms.UNKNOWN_SHELL`."""
    # Lazy import to avoid circular dependencies.
    from .shell_data import UNKNOWN_SHELL

    return current_shell() is UNKNOWN_SHELL


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
        <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables>.
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
        <https://www.jetbrains.com/help/teamcity/predefined-build-parameters.html#PredefinedBuildParameters-ServerBuildProperties>.
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
# Current environment detection
# =============================================================================


@cache
def current_architecture(strict: bool = False) -> Architecture:
    """Returns the :class:`~extra_platforms.Architecture` matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_ARCHITECTURE` if not running inside a
    recognized architecture. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        Always raises an error if multiple architectures match.
    """
    # Lazy imports to avoid circular dependencies.
    from .architecture_data import UNKNOWN_ARCHITECTURE
    from .group_data import ALL_ARCHITECTURES

    # Collect all matching architectures.
    matching: set[Architecture] = {
        arch
        for arch in ALL_ARCHITECTURES
        if arch.current  # type: ignore[misc]
    }

    # Return the only matching architecture.
    if len(matching) == 1:
        return matching.pop()

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple architectures matches: {matching!r}. {_unrecognized_message()}"
        )

    # No matching architecture found.
    msg = f"Unrecognized architecture: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
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
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_PLATFORMS
    from .platform_data import UNKNOWN_PLATFORM, WSL1, WSL2

    # Collect all matching platforms.
    matching: set[Platform] = {
        plat
        for plat in ALL_PLATFORMS
        if plat.current  # type: ignore[misc]
    }

    # Return the only matching platform.
    if len(matching) == 1:
        return matching.pop()

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

    if len(matching) > 1:
        raise RuntimeError(
            f"Multiple platforms matches: {matching!r}. {_unrecognized_message()}"
        )

    # No matching platform found.
    msg = f"Unrecognized platform: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
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

    .. seealso::
        Inspired by `UV's cross-platform shell detection
        <https://github.com/astral-sh/uv/blob/0.10.2/crates/uv-shell/src/lib.rs>`_.
    """
    # Lazy imports to avoid circular dependencies.
    from .group_data import ALL_SHELLS
    from .shell_data import POWERSHELL, UNKNOWN_SHELL

    # Collect all matching shells.
    matching: set[Shell] = {
        shell
        for shell in ALL_SHELLS
        if shell.current  # type: ignore[misc]
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

    # No matching shell found.
    msg = f"Unrecognized shell: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
    return UNKNOWN_SHELL


@cache
def current_ci(strict: bool = False) -> CI:
    """Returns the :class:`~extra_platforms.CI` system matching the current environment.

    Returns :data:`~extra_platforms.UNKNOWN_CI` if not running inside a recognized CI
    system. To raise an error instead, set ``strict`` to ``True``.

    .. important::
        Always raises an error if multiple CI systems match.
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

    # No matching CI system found.
    msg = f"Unrecognized CI: {_unrecognized_message()}"
    if strict:
        raise SystemError(msg)
    logging.warning(msg)
    return UNKNOWN_CI


@cache
def current_traits() -> set[Trait]:
    """Returns all traits matching the current environment.

    This includes :class:`~extra_platforms.Platform`, :class:`~extra_platforms.Architecture`,
    and :class:`~extra_platforms.CI` systems.

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
