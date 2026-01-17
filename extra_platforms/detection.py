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
    will make both the ``is_wsl2()`` and ``is_ubuntu()`` functions return ``True`` at
    the same time.

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
    """Return ``True`` if current architecture is `AARCH64 <architectures.html#extra_platforms.AARCH64>`_.

    .. note::
        ``platform.machine()`` returns different values depending on the OS:

        - Linux: ``aarch64``
        - macOS: ``arm64``
        - Windows: ``ARM64``
    """
    return platform.machine().lower() in ("aarch64", "arm64")


@cache
def is_armv5tel() -> bool:
    """Return ``True`` if current architecture is `ARMV5TEL <architectures.html#extra_platforms.ARMV5TEL>`_."""
    return platform.machine() == "armv5tel"


@cache
def is_armv6l() -> bool:
    """Return ``True`` if current architecture is `ARMV6L <architectures.html#extra_platforms.ARMV6L>`_."""
    return platform.machine() == "armv6l"


@cache
def is_armv7l() -> bool:
    """Return ``True`` if current architecture is `ARMV7L <architectures.html#extra_platforms.ARMV7L>`_."""
    return platform.machine() == "armv7l"


@cache
def is_armv8l() -> bool:
    """Return ``True`` if current architecture is `ARMV8L <architectures.html#extra_platforms.ARMV8L>`_."""
    return platform.machine() == "armv8l"


@cache
def is_arm() -> bool:
    """Return ``True`` if current architecture is `ARM <architectures.html#extra_platforms.ARM>`_.

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
    """Return ``True`` if current architecture is `I386 <architectures.html#extra_platforms.I386>`_."""
    return platform.machine() in ("i386", "i486")


@cache
def is_i586() -> bool:
    """Return ``True`` if current architecture is `I586 <architectures.html#extra_platforms.I586>`_."""
    return platform.machine() == "i586"


@cache
def is_i686() -> bool:
    """Return ``True`` if current architecture is `I686 <architectures.html#extra_platforms.I686>`_."""
    return platform.machine() == "i686"


@cache
def is_x86_64() -> bool:
    """Return ``True`` if current architecture is `X86_64 <architectures.html#extra_platforms.X86_64>`_.

    .. note::
        Windows returns ``AMD64`` in uppercase, so we normalize to lowercase.
    """
    return platform.machine().lower() in ("x86_64", "amd64")


@cache
def is_mips() -> bool:
    """Return ``True`` if current architecture is `MIPS <architectures.html#extra_platforms.MIPS>`_."""
    return platform.machine() == "mips"


@cache
def is_mipsel() -> bool:
    """Return ``True`` if current architecture is `MIPSEL <architectures.html#extra_platforms.MIPSEL>`_."""
    return platform.machine() == "mipsel"


@cache
def is_mips64() -> bool:
    """Return ``True`` if current architecture is `MIPS64 <architectures.html#extra_platforms.MIPS64>`_."""
    return platform.machine() == "mips64"


@cache
def is_mips64el() -> bool:
    """Return ``True`` if current architecture is `MIPS64EL <architectures.html#extra_platforms.MIPS64EL>`_."""
    return platform.machine() == "mips64el"


@cache
def is_ppc() -> bool:
    """Return ``True`` if current architecture is `PPC <architectures.html#extra_platforms.PPC>`_."""
    return platform.machine() in ("ppc", "powerpc")


@cache
def is_ppc64() -> bool:
    """Return ``True`` if current architecture is `PPC64 <architectures.html#extra_platforms.PPC64>`_."""
    return platform.machine() == "ppc64"


@cache
def is_ppc64le() -> bool:
    """Return ``True`` if current architecture is `PPC64LE <architectures.html#extra_platforms.PPC64LE>`_."""
    return platform.machine() == "ppc64le"


@cache
def is_riscv32() -> bool:
    """Return ``True`` if current architecture is `RISCV32 <architectures.html#extra_platforms.RISCV32>`_."""
    return platform.machine() == "riscv32"


@cache
def is_riscv64() -> bool:
    """Return ``True`` if current architecture is `RISCV64 <architectures.html#extra_platforms.RISCV64>`_."""
    return platform.machine() == "riscv64"


@cache
def is_sparc() -> bool:
    """Return ``True`` if current architecture is `SPARC <architectures.html#extra_platforms.SPARC>`_."""
    return platform.machine() == "sparc"


@cache
def is_sparc64() -> bool:
    """Return ``True`` if current architecture is `SPARC64 <architectures.html#extra_platforms.SPARC64>`_."""
    return platform.machine() in ("sparc64", "sun4u", "sun4v")


@cache
def is_s390x() -> bool:
    """Return ``True`` if current architecture is `S390X <architectures.html#extra_platforms.S390X>`_."""
    return platform.machine() == "s390x"


@cache
def is_loongarch64() -> bool:
    """Return ``True`` if current architecture is `LOONGARCH64 <architectures.html#extra_platforms.LOONGARCH64>`_."""
    return platform.machine() == "loongarch64"


@cache
def is_wasm32() -> bool:
    """Return ``True`` if current architecture is `WASM32 <architectures.html#extra_platforms.WASM32>`_.

    .. note::
        WebAssembly detection is based on Emscripten's platform identifier.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "32bit"


@cache
def is_wasm64() -> bool:
    """Return ``True`` if current architecture is `WASM64 <architectures.html#extra_platforms.WASM64>`_.

    .. note::
        WebAssembly 64-bit (memory64) is still experimental.
    """
    return sys.platform == "emscripten" and platform.architecture()[0] == "64bit"


# =============================================================================
# Platform detection heuristics
# =============================================================================


@cache
def is_aix() -> bool:
    """Return ``True`` if current platform is `AIX <platforms.html#extra_platforms.AIX>`_."""
    return sys.platform.startswith("aix") or distro.id() == "aix"


@cache
def is_altlinux() -> bool:
    """Return ``True`` if current platform is `ALTLINUX <platforms.html#extra_platforms.ALTLINUX>`_."""
    return distro.id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return ``True`` if current platform is `AMZN <platforms.html#extra_platforms.AMZN>`_."""
    return distro.id() == "amzn"


@cache
def is_android() -> bool:
    """Return ``True`` if current platform is `ANDROID <platforms.html#extra_platforms.ANDROID>`_.

    Source: https://github.com/kivy/kivy/blob/master/kivy/utils.py#L429
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return ``True`` if current platform is `ARCH <platforms.html#extra_platforms.ARCH>`_."""
    return distro.id() == "arch"


@cache
def is_buildroot() -> bool:
    """Return ``True`` if current platform is `BUILDROOT <platforms.html#extra_platforms.BUILDROOT>`_."""
    return distro.id() == "buildroot"


@cache
def is_cachyos() -> bool:
    """Return ``True`` if current platform is `CACHYOS <platforms.html#extra_platforms.CACHYOS>`_."""
    return distro.id() == "cachyos"


@cache
def is_centos() -> bool:
    """Return ``True`` if current platform is `CENTOS <platforms.html#extra_platforms.CENTOS>`_."""
    return distro.id() == "centos"


@cache
def is_cloudlinux() -> bool:
    """Return ``True`` if current platform is `CLOUDLINUX <platforms.html#extra_platforms.CLOUDLINUX>`_."""
    return distro.id() == "cloudlinux"


@cache
def is_cygwin() -> bool:
    """Return ``True`` if current platform is `CYGWIN <platforms.html#extra_platforms.CYGWIN>`_."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return ``True`` if current platform is `DEBIAN <platforms.html#extra_platforms.DEBIAN>`_."""
    return distro.id() == "debian"


@cache
def is_dragonfly_bsd() -> bool:
    """Return ``True`` if current platform is `DRAGONFLY_BSD <platforms.html#extra_platforms.DRAGONFLY_BSD>`_."""
    return sys.platform.startswith("dragonfly")


@cache
def is_exherbo() -> bool:
    """Return ``True`` if current platform is `EXHERBO <platforms.html#extra_platforms.EXHERBO>`_."""
    return distro.id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return ``True`` if current platform is `FEDORA <platforms.html#extra_platforms.FEDORA>`_."""
    return distro.id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return ``True`` if current platform is `FREEBSD <platforms.html#extra_platforms.FREEBSD>`_."""
    return sys.platform.startswith("freebsd") or distro.id() == "freebsd"


@cache
def is_gentoo() -> bool:
    """Return ``True`` if current platform is `GENTOO <platforms.html#extra_platforms.GENTOO>`_."""
    return distro.id() == "gentoo"


@cache
def is_guix() -> bool:
    """Return ``True`` if current platform is `GUIX <platforms.html#extra_platforms.GUIX>`_."""
    return distro.id() == "guix"


@cache
def is_haiku() -> bool:
    """Return ``True`` if current platform is `HAIKU <platforms.html#extra_platforms.HAIKU>`_."""
    return sys.platform.startswith("haiku")


@cache
def is_hurd() -> bool:
    """Return ``True`` if current platform is `HURD <platforms.html#extra_platforms.HURD>`_.

    ``sys.platform`` can returns ``GNU`` or ``gnu0``, see:
    https://github.com/kdeldycke/extra-platforms/issues/308
    """
    return sys.platform.lower().startswith("gnu")


@cache
def is_ibm_powerkvm() -> bool:
    """Return ``True`` if current platform is `IBM_POWERKVM <platforms.html#extra_platforms.IBM_POWERKVM>`_."""
    return distro.id() == "ibm_powerkvm"


@cache
def is_illumos() -> bool:
    """Return ``True`` if current platform is `ILLUMOS <platforms.html#extra_platforms.ILLUMOS>`_.

    Illumos is a Unix OS derived from OpenSolaris. It shares ``sys.platform == 'sunos5'``
    with Solaris, but can be distinguished by checking ``platform.uname().version`` which
    contains "illumos" on Illumos-based systems (like OpenIndiana, SmartOS, OmniOS).
    """
    return "illumos" in platform.uname().version.lower()


@cache
def is_kvmibm() -> bool:
    """Return ``True`` if current platform is `KVMIBM <platforms.html#extra_platforms.KVMIBM>`_."""
    return distro.id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return ``True`` if current platform is `LINUXMINT <platforms.html#extra_platforms.LINUXMINT>`_."""
    return distro.id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return ``True`` if current platform is `MACOS <platforms.html#extra_platforms.MACOS>`_."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return ``True`` if current platform is `MAGEIA <platforms.html#extra_platforms.MAGEIA>`_."""
    return distro.id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return ``True`` if current platform is `MANDRIVA <platforms.html#extra_platforms.MANDRIVA>`_."""
    return distro.id() == "mandriva"


@cache
def is_midnightbsd() -> bool:
    """Return ``True`` if current platform is `MIDNIGHTBSD <platforms.html#extra_platforms.MIDNIGHTBSD>`_."""
    return sys.platform.startswith("midnightbsd") or distro.id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return ``True`` if current platform is `NETBSD <platforms.html#extra_platforms.NETBSD>`_."""
    return sys.platform.startswith("netbsd") or distro.id() == "netbsd"


@cache
def is_nobara() -> bool:
    """Return ``True`` if current platform is `NOBARA <platforms.html#extra_platforms.NOBARA>`_."""
    return distro.id() == "nobara"


@cache
def is_openbsd() -> bool:
    """Return ``True`` if current platform is `OPENBSD <platforms.html#extra_platforms.OPENBSD>`_."""
    return sys.platform.startswith("openbsd") or distro.id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return ``True`` if current platform is `OPENSUSE <platforms.html#extra_platforms.OPENSUSE>`_."""
    return distro.id() == "opensuse"


@cache
def is_oracle() -> bool:
    """Return ``True`` if current platform is `ORACLE <platforms.html#extra_platforms.ORACLE>`_."""
    return distro.id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return ``True`` if current platform is `PARALLELS <platforms.html#extra_platforms.PARALLELS>`_."""
    return distro.id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return ``True`` if current platform is `PIDORA <platforms.html#extra_platforms.PIDORA>`_."""
    return distro.id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return ``True`` if current platform is `RASPBIAN <platforms.html#extra_platforms.RASPBIAN>`_."""
    return distro.id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return ``True`` if current platform is `RHEL <platforms.html#extra_platforms.RHEL>`_."""
    return distro.id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return ``True`` if current platform is `ROCKY <platforms.html#extra_platforms.ROCKY>`_."""
    return distro.id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return ``True`` if current platform is `SCIENTIFIC <platforms.html#extra_platforms.SCIENTIFIC>`_."""
    return distro.id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return ``True`` if current platform is `SLACKWARE <platforms.html#extra_platforms.SLACKWARE>`_."""
    return distro.id() == "slackware"


@cache
def is_sles() -> bool:
    """Return ``True`` if current platform is `SLES <platforms.html#extra_platforms.SLES>`_."""
    return distro.id() == "sles"


@cache
def is_solaris() -> bool:
    """Return ``True`` if current platform is `SOLARIS <platforms.html#extra_platforms.SOLARIS>`_."""
    return platform.platform(aliased=True, terse=True).startswith("Solaris")


@cache
def is_sunos() -> bool:
    """Return ``True`` if current platform is `SUNOS <platforms.html#extra_platforms.SUNOS>`_."""
    return platform.platform(aliased=True, terse=True).startswith("SunOS")


@cache
def is_tumbleweed() -> bool:
    """Return ``True`` if current platform is `TUMBLEWEED <platforms.html#extra_platforms.TUMBLEWEED>`_."""
    return distro.id() == "opensuse-tumbleweed"


@cache
def is_tuxedo() -> bool:
    """Return ``True`` if current platform is `TUXEDO <platforms.html#extra_platforms.TUXEDO>`_."""
    return distro.id() == "tuxedo"


@cache
def is_ubuntu() -> bool:
    """Return ``True`` if current platform is `UBUNTU <platforms.html#extra_platforms.UBUNTU>`_."""
    return distro.id() == "ubuntu"


@cache
def is_ultramarine() -> bool:
    """Return ``True`` if current platform is `ULTRAMARINE <platforms.html#extra_platforms.ULTRAMARINE>`_."""
    return distro.id() == "ultramarine"


@cache
def is_windows() -> bool:
    """Return ``True`` if current platform is `WINDOWS <platforms.html#extra_platforms.WINDOWS>`_."""
    return sys.platform.startswith("win32")


@cache
def is_wsl1() -> bool:
    """Return ``True`` if current platform is `WSL1 <platforms.html#extra_platforms.WSL1>`_.

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
    """Return ``True`` if current platform is `WSL2 <platforms.html#extra_platforms.WSL2>`_."""
    return "microsoft" in platform.release()


@cache
def is_xenserver() -> bool:
    """Return ``True`` if current platform is `XENSERVER <platforms.html#extra_platforms.XENSERVER>`_."""
    return distro.id() == "xenserver"


# =============================================================================
# CI/CD detection heuristics
# =============================================================================


@cache
def is_azure_pipelines() -> bool:
    """Return ``True`` if current CI is `AZURE_PIPELINES <ci.html#extra_platforms.AZURE_PIPELINES>`_.

    `Environment variables reference
    <https://learn.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&viewFallbackFrom=vsts&tabs=yaml#system-variables>`_.
    """
    return "TF_BUILD" in environ


@cache
def is_bamboo() -> bool:
    """Return ``True`` if current CI is `BAMBOO <ci.html#extra_platforms.BAMBOO>`_.

    `Environment variables reference
    <https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html#Bamboovariables-Build-specificvariables>`_.
    """
    return "bamboo.buildKey" in environ


@cache
def is_buildkite() -> bool:
    """Return ``True`` if current CI is `BUILDKITE <ci.html#extra_platforms.BUILDKITE>`_.

    `Environment variables reference
    <https://buildkite.com/docs/pipelines/environment-variables>`_.
    """
    return "BUILDKITE" in environ


@cache
def is_circle_ci() -> bool:
    """Return ``True`` if current CI is `CIRCLE_CI <ci.html#extra_platforms.CIRCLE_CI>`_.

    `Environment variables reference
    <https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables>`_.
    """
    return "CIRCLECI" in environ


@cache
def is_cirrus_ci() -> bool:
    """Return ``True`` if current CI is `CIRRUS_CI <ci.html#extra_platforms.CIRRUS_CI>`_.

    `Environment variables reference
    <https://cirrus-ci.org/guide/writing-tasks/#environment-variables>`_.
    """
    return "CIRRUS_CI" in environ


@cache
def is_codebuild() -> bool:
    """Return ``True`` if current CI is `CODEBUILD <ci.html#extra_platforms.CODEBUILD>`_.

    `Environment variables reference
    <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html>`_.
    """
    return "CODEBUILD_BUILD_ID" in environ


@cache
def is_github_ci() -> bool:
    """Return ``True`` if current CI is `GITHUB_CI <ci.html#extra_platforms.GITHUB_CI>`_.

    `Environment variables reference
    <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables>`_.
    """
    return "GITHUB_ACTIONS" in environ or "GITHUB_RUN_ID" in environ


@cache
def is_gitlab_ci() -> bool:
    """Return ``True`` if current CI is `GITLAB_CI <ci.html#extra_platforms.GITLAB_CI>`_.

    `Environment variables reference
    <https://docs.gitlab.com/ci/variables/predefined_variables/#predefined-variables>`_.
    """
    return "GITLAB_CI" in environ


@cache
def is_heroku_ci() -> bool:
    """Return ``True`` if current CI is `HEROKU_CI <ci.html#extra_platforms.HEROKU_CI>`_.

    `Environment variables reference
    <https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables>`_.
    """
    return "HEROKU_TEST_RUN_ID" in environ


@cache
def is_teamcity() -> bool:
    """Return ``True`` if current CI is `TEAMCITY <ci.html#extra_platforms.TEAMCITY>`_.

    `Environment variables reference
    <https://www.jetbrains.com/help/teamcity/predefined-build-parameters.html#PredefinedBuildParameters-ServerBuildProperties>`_.
    """
    return "TEAMCITY_VERSION" in environ


@cache
def is_travis_ci() -> bool:
    """Return ``True`` if current CI is `TRAVIS_CI <ci.html#extra_platforms.TRAVIS_CI>`_.

    `Environment variables reference
    <https://docs.travis-ci.com/user/environment-variables/#default-environment-variables>`_.
    """
    return "TRAVIS" in environ
