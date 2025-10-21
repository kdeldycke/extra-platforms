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
"""Heuristics to detect platforms.

This collection of heuristics is designed as a set of separate function with minimal
logic and dependencies.

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

For all other platforms, we either rely on:

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

import logging
import platform
import sys
from functools import cache
from os import environ

import distro

from . import _report_msg


@cache
def is_aix() -> bool:
    """Return ``True`` if current platform is AIX."""
    return sys.platform.startswith("aix") or distro.id() == "aix"


@cache
def is_altlinux() -> bool:
    """Return ``True`` if current platform is ALT Linux."""
    return distro.id() == "altlinux"


@cache
def is_amzn() -> bool:
    """Return ``True`` if current platform is Amazon Linux."""
    return distro.id() == "amzn"


@cache
def is_android() -> bool:
    """Return ``True`` if current platform is Android.

    Source: https://github.com/kivy/kivy/blob/master/kivy/utils.py#L429
    """
    return "ANDROID_ROOT" in environ or "P4A_BOOTSTRAP" in environ


@cache
def is_arch() -> bool:
    """Return ``True`` if current platform is Arch Linux."""
    return distro.id() == "arch"


@cache
def is_azure_pipelines() -> bool:
    """Return ``True`` if current platform is Azure Pipelines.

    `Environment variables reference
    <https://learn.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&viewFallbackFrom=vsts&tabs=yaml#system-variables>`_.
    """
    return "TF_BUILD" in environ


@cache
def is_bamboo() -> bool:
    """Return ``True`` if current platform is Bamboo.

    `Environment variables reference
    <https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html#Bamboovariables-Build-specificvariables>`_.
    """
    return "bamboo.buildKey" in environ


@cache
def is_buildkite() -> bool:
    """Return ``True`` if current platform is Buildkite.

    `Environment variables reference
    <https://buildkite.com/docs/pipelines/environment-variables>`_.
    """
    return "BUILDKITE" in environ


@cache
def is_buildroot() -> bool:
    """Return ``True`` if current platform is Buildroot."""
    return distro.id() == "buildroot"


@cache
def is_centos() -> bool:
    """Return ``True`` if current platform is CentOS."""
    return distro.id() == "centos"


@cache
def is_circle_ci() -> bool:
    """Return ``True`` if current platform is Circle CI.

    `Environment variables reference
    <https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables>`_.
    """
    return "CIRCLECI" in environ


@cache
def is_cirrus_ci() -> bool:
    """Return ``True`` if current platform is Cirrus CI.

    `Environment variables reference
    <https://cirrus-ci.org/guide/writing-tasks/#environment-variables>`_.
    """
    return "CIRRUS_CI" in environ


@cache
def is_cloudlinux() -> bool:
    """Return ``True`` if current platform is CloudLinux OS."""
    return distro.id() == "cloudlinux"


@cache
def is_codebuild() -> bool:
    """Return ``True`` if current platform is CodeBuild.

    `Environment variables reference
    <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html>`_.
    """
    return "CODEBUILD_BUILD_ID" in environ


@cache
def is_cygwin() -> bool:
    """Return ``True`` if current platform is Cygwin."""
    return sys.platform.startswith("cygwin")


@cache
def is_debian() -> bool:
    """Return ``True`` if current platform is Debian."""
    return distro.id() == "debian"


@cache
def is_exherbo() -> bool:
    """Return ``True`` if current platform is Exherbo Linux."""
    return distro.id() == "exherbo"


@cache
def is_fedora() -> bool:
    """Return ``True`` if current platform is Fedora."""
    return distro.id() == "fedora"


@cache
def is_freebsd() -> bool:
    """Return ``True`` if current platform is FreeBSD."""
    return sys.platform.startswith("freebsd") or distro.id() == "freebsd"


@cache
def is_gentoo() -> bool:
    """Return ``True`` if current platform is GenToo Linux."""
    return distro.id() == "gentoo"


@cache
def is_github_ci() -> bool:
    """Return ``True`` if current platform is GitHub Actions runner.

    `Environment variables reference
    <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables>`_.
    """
    return "GITHUB_ACTIONS" in environ or "GITHUB_RUN_ID" in environ


@cache
def is_gitlab_ci() -> bool:
    """Return ``True`` if current platform is GitLab CI.

    `Environment variables reference
    <https://docs.gitlab.com/ci/variables/predefined_variables/#predefined-variables>`_.
    """
    return "GITLAB_CI" in environ


@cache
def is_guix() -> bool:
    """Return ``True`` if current platform is Guix System."""
    return distro.id() == "guix"


@cache
def is_heroku_ci() -> bool:
    """Return ``True`` if current platform is Heroku CI.

    `Environment variables reference
    <https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables>`_.
    """
    return "HEROKU_TEST_RUN_ID" in environ


@cache
def is_hurd() -> bool:
    """Return ``True`` if current platform is GNU/Hurd.

    ``sys.platform`` can returns ``GNU`` or ``gnu0``, see:
    https://github.com/kdeldycke/extra-platforms/issues/308
    """
    return sys.platform.lower().startswith("gnu")


@cache
def is_ibm_powerkvm() -> bool:
    """Return ``True`` if current platform is IBM PowerKVM."""
    return distro.id() == "ibm_powerkvm"


@cache
def is_kvmibm() -> bool:
    """Return ``True`` if current platform is KVM for IBM z Systems."""
    return distro.id() == "kvmibm"


@cache
def is_linuxmint() -> bool:
    """Return ``True`` if current platform is Linux Mint."""
    return distro.id() == "linuxmint"


@cache
def is_macos() -> bool:
    """Return ``True`` if current platform is macOS."""
    return platform.platform(terse=True).startswith(("macOS", "Darwin"))


@cache
def is_mageia() -> bool:
    """Return ``True`` if current platform is Mageia."""
    return distro.id() == "mageia"


@cache
def is_mandriva() -> bool:
    """Return ``True`` if current platform is Mandriva Linux."""
    return distro.id() == "mandriva"


@cache
def is_midnightbsd() -> bool:
    """Return ``True`` if current platform is MidnightBSD."""
    return sys.platform.startswith("midnightbsd") or distro.id() == "midnightbsd"


@cache
def is_netbsd() -> bool:
    """Return ``True`` if current platform is NetBSD."""
    return sys.platform.startswith("netbsd") or distro.id() == "netbsd"


@cache
def is_nobara() -> bool:
    """Return ``True`` if current platform is Nobara Linux."""
    return distro.id() == "nobara"


@cache
def is_openbsd() -> bool:
    """Return ``True`` if current platform is OpenBSD."""
    return sys.platform.startswith("openbsd") or distro.id() == "openbsd"


@cache
def is_opensuse() -> bool:
    """Return ``True`` if current platform is openSUSE."""
    return distro.id() == "opensuse"


@cache
def is_oracle() -> bool:
    """Return ``True`` if current platform is Oracle Linux (and Oracle Enterprise Linux)."""
    return distro.id() == "oracle"


@cache
def is_parallels() -> bool:
    """Return ``True`` if current platform is Parallels."""
    return distro.id() == "parallels"


@cache
def is_pidora() -> bool:
    """Return ``True`` if current platform is Pidora."""
    return distro.id() == "pidora"


@cache
def is_raspbian() -> bool:
    """Return ``True`` if current platform is Raspbian."""
    return distro.id() == "raspbian"


@cache
def is_rhel() -> bool:
    """Return ``True`` if current platform is RedHat Enterprise Linux."""
    return distro.id() == "rhel"


@cache
def is_rocky() -> bool:
    """Return ``True`` if current platform is Rocky Linux."""
    return distro.id() == "rocky"


@cache
def is_scientific() -> bool:
    """Return ``True`` if current platform is Scientific Linux."""
    return distro.id() == "scientific"


@cache
def is_slackware() -> bool:
    """Return ``True`` if current platform is Slackware."""
    return distro.id() == "slackware"


@cache
def is_sles() -> bool:
    """Return ``True`` if current platform is SUSE Linux Enterprise Server."""
    return distro.id() == "sles"


@cache
def is_solaris() -> bool:
    """Return ``True`` if current platform is Solaris."""
    return platform.platform(aliased=True, terse=True).startswith("Solaris")


@cache
def is_sunos() -> bool:
    """Return ``True`` if current platform is SunOS."""
    return platform.platform(aliased=True, terse=True).startswith("SunOS")


@cache
def is_teamcity() -> bool:
    """Return ``True`` if current platform is TeamCity.

    `Environment variables reference
    <https://www.jetbrains.com/help/teamcity/predefined-build-parameters.html#PredefinedBuildParameters-ServerBuildProperties>`_.
    """
    return "TEAMCITY_VERSION" in environ


@cache
def is_travis_ci() -> bool:
    """Return ``True`` if current platform is Travis CI.

    `Environment variables reference
    <https://docs.travis-ci.com/user/environment-variables/#default-environment-variables>`_.
    """
    return "TRAVIS" in environ


@cache
def is_tumbleweed() -> bool:
    """Return ``True`` if current platform is openSUSE Tumbleweed."""
    return distro.id() == "opensuse-tumbleweed"


@cache
def is_tuxedo() -> bool:
    """Return ``True`` if current platform is Tuxedo OS."""
    return distro.id() == "tuxedo"


@cache
def is_ubuntu() -> bool:
    """Return ``True`` if current platform is Ubuntu."""
    return distro.id() == "ubuntu"


@cache
def is_unknown_ci() -> bool:
    """Return ``True`` if current platform is an unknown CI.

    Some CI systems relies on `generic environment variables to identify themselves
    <https://adamj.eu/tech/2020/03/09/detect-if-your-tests-are-running-on-ci/>`_:

    - ``CI``
    - ``BUILD_ID``
    """
    if any((
        is_azure_pipelines(),
        is_bamboo(),
        is_buildkite(),
        is_circle_ci(),
        is_cirrus_ci(),
        is_codebuild(),
        is_github_ci(),
        is_gitlab_ci(),
        is_heroku_ci(),
        is_teamcity(),
        is_travis_ci(),
    )):
        return False

    if "CI" in environ or "BUILD_ID" in environ:
        logging.warning(f"Unknown CI detected: {environ}. {_report_msg}")
        return True
    return False


@cache
def is_unknown_linux() -> bool:
    """Return ``True`` if current platform is an unknown Linux."""
    if any((
        is_altlinux(),
        is_amzn(),
        is_android(),
        is_arch(),
        is_buildroot(),
        is_centos(),
        is_cloudlinux(),
        is_debian(),
        is_exherbo(),
        is_fedora(),
        is_gentoo(),
        is_guix(),
        is_ibm_powerkvm(),
        is_kvmibm(),
        is_linuxmint(),
        is_mageia(),
        is_mandriva(),
        is_nobara(),
        is_opensuse(),
        is_oracle(),
        is_parallels(),
        is_pidora(),
        is_raspbian(),
        is_rhel(),
        is_rocky(),
        is_scientific(),
        is_slackware(),
        is_sles(),
        is_tumbleweed(),
        is_tuxedo(),
        is_ubuntu(),
        is_xenserver(),
    )):
        return False

    if sys.platform.startswith("linux"):
        logging.warning(f"Unknown Linux detected: {distro.info()!r}. {_report_msg}")
        return True
    return False  # type: ignore[unreachable,unused-ignore]


@cache
def is_windows() -> bool:
    """Return ``True`` if current platform is Windows."""
    return sys.platform.startswith("win32")


@cache
def is_wsl1() -> bool:
    """Return ``True`` if current platform is running over Windows Subsystem for Linux v1.

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
    """Return ``True`` if current platform is running over Windows Subsystem for Linux v2."""
    return "microsoft" in platform.release()


@cache
def is_xenserver() -> bool:
    """Return ``True`` if current platform is XenServer."""
    return distro.id() == "xenserver"
