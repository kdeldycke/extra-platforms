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
"""

from __future__ import annotations

import platform
import sys
from functools import cache
from os import environ

import distro

# =============================================================================
# Architecture detection heuristics
# =============================================================================


@cache
def is_aarch64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.AARCH64`.

    .. note::
        ``platform.machine()`` returns different values depending on the OS:

        - Linux: ``aarch64``
        - macOS: ``arm64``
        - Windows: ``ARM64``
    """
    return platform.machine().lower() in ("aarch64", "arm64")


@cache
def is_armv5tel() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.ARMV5TEL`."""
    return platform.machine() == "armv5tel"


@cache
def is_armv6l() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.ARMV6L`."""
    return platform.machine() == "armv6l"


@cache
def is_armv7l() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.ARMV7L`."""
    return platform.machine() == "armv7l"


@cache
def is_armv8l() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.ARMV8L`."""
    return platform.machine() == "armv8l"


@cache
def is_arm() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.ARM`.

    This matches ARM architectures not covered by more specific variants.
    """
    if platform.machine().startswith("arm") and not any((
        is_armv5tel(),
        is_armv6l(),
        is_armv7l(),
        is_armv8l(),
        is_aarch64(),
    )):
        return True
    return False


@cache
def is_i386() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.I386`."""
    return platform.machine() in ("i386", "i486")


@cache
def is_i586() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.I586`."""
    return platform.machine() == "i586"


@cache
def is_i686() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.I686`."""
    return platform.machine() == "i686"


@cache
def is_x86_64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.X86_64`.

    .. note::
        Windows returns ``AMD64`` in uppercase, so we normalize to lowercase.
    """
    return platform.machine().lower() in ("x86_64", "amd64")


@cache
def is_mips() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.MIPS`."""
    return platform.machine() == "mips"


@cache
def is_mipsel() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.MIPSEL`."""
    return platform.machine() == "mipsel"


@cache
def is_mips64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.MIPS64`."""
    return platform.machine() == "mips64"


@cache
def is_mips64el() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.MIPS64EL`."""
    return platform.machine() == "mips64el"


@cache
def is_ppc() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.PPC`."""
    return platform.machine() in ("ppc", "powerpc")


@cache
def is_ppc64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.PPC64`."""
    return platform.machine() == "ppc64"


@cache
def is_ppc64le() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.PPC64LE`."""
    return platform.machine() == "ppc64le"


@cache
def is_riscv32() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.RISCV32`."""
    return platform.machine() == "riscv32"


@cache
def is_riscv64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.RISCV64`."""
    return platform.machine() == "riscv64"


@cache
def is_sparc() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.SPARC`."""
    return platform.machine() == "sparc"


@cache
def is_sparc64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.SPARC64`."""
    return platform.machine() in ("sparc64", "sun4u", "sun4v")


@cache
def is_s390x() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.S390X`."""
    return platform.machine() == "s390x"


@cache
def is_loongarch64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.LOONGARCH64`."""
    return platform.machine() == "loongarch64"


@cache
def is_wasm32() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.WASM32`.

    .. note::
        WebAssembly detection is based on Emscripten's platform identifier.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "32bit"


@cache
def is_wasm64() -> bool:
    """Return ``True`` if current architecture is :data:`~extra_platforms.WASM64`.

    .. note::
        WebAssembly 64-bit (memory64) is still experimental.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "64bit"


# =============================================================================
# Platform detection heuristics
# =============================================================================


@cache
def is_aix() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.AIX`."""
    return sys.platform.startswith("aix") or distro.id() == "aix"


@cache
def is_altlinux() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ALTLINUX`."""
    return distro.id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.AMZN`."""
    return distro.id() == "amzn"


@cache
def is_android() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ANDROID`.

    Source: https://github.com/kivy/kivy/blob/master/kivy/utils.py#L429
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ARCH`."""
    return distro.id() == "arch"


@cache
def is_buildroot() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.BUILDROOT`."""
    return distro.id() == "buildroot"


@cache
def is_cachyos() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.CACHYOS`."""
    return distro.id() == "cachyos"


@cache
def is_centos() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.CENTOS`."""
    return distro.id() == "centos"


@cache
def is_cloudlinux() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.CLOUDLINUX`."""
    return distro.id() == "cloudlinux"


@cache
def is_cygwin() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.CYGWIN`."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.DEBIAN`."""
    return distro.id() == "debian"


@cache
def is_dragonfly_bsd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.DRAGONFLY_BSD`."""
    return sys.platform.startswith("dragonfly")


@cache
def is_exherbo() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.EXHERBO`."""
    return distro.id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.FEDORA`."""
    return distro.id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.FREEBSD`."""
    return sys.platform.startswith("freebsd") or distro.id() == "freebsd"


@cache
def is_gentoo() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.GENTOO`."""
    return distro.id() == "gentoo"


@cache
def is_guix() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.GUIX`."""
    return distro.id() == "guix"


@cache
def is_haiku() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.HAIKU`."""
    return sys.platform.startswith("haiku")


@cache
def is_hurd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.HURD`.

    ``sys.platform`` can returns ``GNU`` or ``gnu0``, see:
    https://github.com/kdeldycke/extra-platforms/issues/308
    """
    return sys.platform.lower().startswith("gnu")


@cache
def is_ibm_powerkvm() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.IBM_POWERKVM`."""
    return distro.id() == "ibm_powerkvm"


@cache
def is_illumos() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ILLUMOS`.

    Illumos is a Unix OS derived from OpenSolaris. It shares ``sys.platform == 'sunos5'``
    with Solaris, but can be distinguished by checking ``platform.uname().version`` which
    contains "illumos" on Illumos-based systems (like OpenIndiana, SmartOS, OmniOS).
    """
    return "illumos" in platform.uname().version.lower()


@cache
def is_kvmibm() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.KVMIBM`."""
    return distro.id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.LINUXMINT`."""
    return distro.id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.MACOS`."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.MAGEIA`."""
    return distro.id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.MANDRIVA`."""
    return distro.id() == "mandriva"


@cache
def is_midnightbsd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.MIDNIGHTBSD`."""
    return sys.platform.startswith("midnightbsd") or distro.id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.NETBSD`."""
    return sys.platform.startswith("netbsd") or distro.id() == "netbsd"


@cache
def is_nobara() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.NOBARA`."""
    return distro.id() == "nobara"


@cache
def is_openbsd() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.OPENBSD`."""
    return sys.platform.startswith("openbsd") or distro.id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.OPENSUSE`."""
    return distro.id() == "opensuse"


@cache
def is_oracle() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ORACLE`."""
    return distro.id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.PARALLELS`."""
    return distro.id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.PIDORA`."""
    return distro.id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.RASPBIAN`."""
    return distro.id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.RHEL`."""
    return distro.id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ROCKY`."""
    return distro.id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.SCIENTIFIC`."""
    return distro.id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.SLACKWARE`."""
    return distro.id() == "slackware"


@cache
def is_sles() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.SLES`."""
    return distro.id() == "sles"


@cache
def is_solaris() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.SOLARIS`."""
    return platform.platform(aliased=True, terse=True).startswith("Solaris")


@cache
def is_sunos() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.SUNOS`."""
    return platform.platform(aliased=True, terse=True).startswith("SunOS")


@cache
def is_tumbleweed() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.TUMBLEWEED`."""
    return distro.id() == "opensuse-tumbleweed"


@cache
def is_tuxedo() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.TUXEDO`."""
    return distro.id() == "tuxedo"


@cache
def is_ubuntu() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.UBUNTU`."""
    return distro.id() == "ubuntu"


@cache
def is_ultramarine() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.ULTRAMARINE`."""
    return distro.id() == "ultramarine"


@cache
def is_windows() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.WINDOWS`."""
    return sys.platform.startswith("win32")


@cache
def is_wsl1() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.WSL1`.

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
    """Return ``True`` if current platform is :data:`~extra_platforms.WSL2`."""
    return "microsoft" in platform.release()


@cache
def is_xenserver() -> bool:
    """Return ``True`` if current platform is :data:`~extra_platforms.XENSERVER`."""
    return distro.id() == "xenserver"


# =============================================================================
# CI/CD detection heuristics
# =============================================================================


@cache
def is_azure_pipelines() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.AZURE_PIPELINES`.

    `Environment variables reference
    <https://learn.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&viewFallbackFrom=vsts&tabs=yaml#system-variables>`_.
    """
    return "TF_BUILD" in environ


@cache
def is_bamboo() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.BAMBOO`.

    `Environment variables reference
    <https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html#Bamboovariables-Build-specificvariables>`_.
    """
    return "bamboo.buildKey" in environ


@cache
def is_buildkite() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.BUILDKITE`.

    `Environment variables reference
    <https://buildkite.com/docs/pipelines/environment-variables>`_.
    """
    return "BUILDKITE" in environ


@cache
def is_circle_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.CIRCLE_CI`.

    `Environment variables reference
    <https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables>`_.
    """
    return "CIRCLECI" in environ


@cache
def is_cirrus_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.CIRRUS_CI`.

    `Environment variables reference
    <https://cirrus-ci.org/guide/writing-tasks/#environment-variables>`_.
    """
    return "CIRRUS_CI" in environ


@cache
def is_codebuild() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.CODEBUILD`.

    `Environment variables reference
    <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html>`_.
    """
    return "CODEBUILD_BUILD_ID" in environ


@cache
def is_github_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.GITHUB_CI`.

    `Environment variables reference
    <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables>`_.
    """
    return "GITHUB_ACTIONS" in environ or "GITHUB_RUN_ID" in environ


@cache
def is_gitlab_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.GITLAB_CI`.

    `Environment variables reference
    <https://docs.gitlab.com/ci/variables/predefined_variables/#predefined-variables>`_.
    """
    return "GITLAB_CI" in environ


@cache
def is_heroku_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.HEROKU_CI`.

    `Environment variables reference
    <https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables>`_.
    """
    return "HEROKU_TEST_RUN_ID" in environ


@cache
def is_teamcity() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.TEAMCITY`.

    `Environment variables reference
    <https://www.jetbrains.com/help/teamcity/predefined-build-parameters.html#PredefinedBuildParameters-ServerBuildProperties>`_.
    """
    return "TEAMCITY_VERSION" in environ


@cache
def is_travis_ci() -> bool:
    """Return ``True`` if current CI is :data:`~extra_platforms.TRAVIS_CI`.

    `Environment variables reference
    <https://docs.travis-ci.com/user/environment-variables/#default-environment-variables>`_.
    """
    return "TRAVIS" in environ
