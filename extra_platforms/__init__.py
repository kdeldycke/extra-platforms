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
"""Expose package-wide elements."""

import sys

if sys.version_info >= (3, 9):
    from functools import cache
else:
    from functools import lru_cache

    def cache(user_function):
        """Simple lightweight unbounded cache. Sometimes called "memoize".

        .. important::

            This is a straight `copy of the functools.cache implementation
            <https://github.com/python/cpython/blob/55a26de/Lib/functools.py#L647-L653>`_,
            which is only `available in the standard library starting with Python v3.9
            <https://docs.python.org/3/library/functools.html?highlight=caching#functools.cache>`.
        """
        return lru_cache(maxsize=None)(user_function)


from platform import platform
from typing import FrozenSet

# XXX Exposing everything at package level motivates platforms and groups to have a
# unique and unambiguous ID. This constraint is enforced at the data-level and checked
# in unittests.
from .detection import (  # noqa: E402
    is_aix,
    is_altlinux,
    is_amzn,
    is_android,
    is_arch,
    is_buildroot,
    is_centos,
    is_cloudlinux,
    is_cygwin,
    is_debian,
    is_exherbo,
    is_fedora,
    is_freebsd,
    is_gentoo,
    is_guix,
    is_hurd,
    is_ibm_powerkvm,
    is_kvmibm,
    is_linuxmint,
    is_macos,
    is_mageia,
    is_mandriva,
    is_midnightbsd,
    is_netbsd,
    is_openbsd,
    is_opensuse,
    is_oracle,
    is_parallels,
    is_pidora,
    is_raspbian,
    is_rhel,
    is_rocky,
    is_scientific,
    is_slackware,
    is_sles,
    is_solaris,
    is_sunos,
    is_ubuntu,
    is_unknown_linux,
    is_windows,
    is_wsl1,
    is_wsl2,
    is_xenserver,
)
from .groups import (  # noqa: E402
    ALL_GROUPS,
    ALL_LINUX,
    ALL_PLATFORMS,
    ALL_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    EXTRA_GROUPS,
    LINUX_LAYERS,
    LINUX_LIKE,
    NON_OVERLAPPING_GROUPS,
    OTHER_UNIX,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    Group,
    reduce,
)
from .platforms import (  # noqa: E402
    AIX,
    ALTLINUX,
    AMZN,
    ANDROID,
    ARCH,
    BUILDROOT,
    CENTOS,
    CLOUDLINUX,
    CYGWIN,
    DEBIAN,
    EXHERBO,
    FEDORA,
    FREEBSD,
    GENTOO,
    GUIX,
    HURD,
    IBM_POWERKVM,
    KVMIBM,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    OPENBSD,
    OPENSUSE,
    ORACLE,
    PARALLELS,
    PIDORA,
    RASPBIAN,
    RHEL,
    ROCKY,
    SCIENTIFIC,
    SLACKWARE,
    SLES,
    SOLARIS,
    SUNOS,
    UBUNTU,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    Platform,
)

# XXX Not imported at package level so dependency on Pytest can stay optional.
# from .pytest import *

__version__ = "1.2.1"
"""Examples of valid version strings according :pep:`440#version-scheme`:

.. code-block:: python

    __version__ = "1.2.3.dev1"  # Development release 1
    __version__ = "1.2.3a1"  # Alpha Release 1
    __version__ = "1.2.3b1"  # Beta Release 1
    __version__ = "1.2.3rc1"  # RC Release 1
    __version__ = "1.2.3"  # Final Release
    __version__ = "1.2.3.post1"  # Post Release 1
"""


ALL_OS_LABELS: FrozenSet[str] = frozenset((p.name for p in ALL_PLATFORMS.platforms))
"""Sets of all recognized labels."""


@cache
def current_os() -> Platform:
    """Return the current platform."""
    matching = []
    for p in ALL_PLATFORMS.platforms:
        if p.current:
            matching.append(p)

    if len(matching) > 1:
        msg = f"Multiple platforms match current OS: {matching}"
        raise RuntimeError(msg)

    if not matching:
        msg = (
            f"Unrecognized {sys.platform} / "
            f"{platform(aliased=True, terse=True)} platform."
        )
        raise SystemError(msg)

    assert len(matching) == 1
    return matching.pop()


CURRENT_OS_ID: str = current_os().id
CURRENT_OS_LABEL: str = current_os().name
"""Constants about the current platform."""


__all__ = [
    "AIX",  # noqa: F405
    "ALL_GROUPS",  # noqa: F405
    "ALL_LINUX",  # noqa: F405
    "ALL_OS_LABELS",  # noqa: F405
    "ALL_PLATFORMS",  # noqa: F405
    "ALL_WINDOWS",  # noqa: F405
    "ALTLINUX",  # noqa: F405
    "AMZN",  # noqa: F405
    "ANDROID",  # noqa: F405
    "ARCH",  # noqa: F405
    "BSD",  # noqa: F405
    "BSD_WITHOUT_MACOS",  # noqa: F405
    "BUILDROOT",  # noqa: F405
    "CENTOS",  # noqa: F405
    "CLOUDLINUX",  # noqa: F405
    "current_os",  # noqa: F405
    "CURRENT_OS_ID",  # noqa: F405
    "CURRENT_OS_LABEL",  # noqa: F405
    "CYGWIN",  # noqa: F405
    "DEBIAN",  # noqa: F405
    "EXHERBO",  # noqa: F405
    "EXTRA_GROUPS",  # noqa: F405
    "FEDORA",  # noqa: F405
    "FREEBSD",  # noqa: F405
    "GENTOO",  # noqa: F405
    "Group",  # noqa: F405
    "GUIX",  # noqa: F405
    "HURD",  # noqa: F405
    "IBM_POWERKVM",  # noqa: F405
    "is_aix",  # noqa: F405
    "is_altlinux",  # noqa: F405
    "is_amzn",  # noqa: F405
    "is_android",  # noqa: F405
    "is_arch",  # noqa: F405
    "is_buildroot",  # noqa: F405
    "is_centos",  # noqa: F405
    "is_cloudlinux",  # noqa: F405
    "is_cygwin",  # noqa: F405
    "is_debian",  # noqa: F405
    "is_exherbo",  # noqa: F405
    "is_fedora",  # noqa: F405
    "is_freebsd",  # noqa: F405
    "is_gentoo",  # noqa: F405
    "is_guix",  # noqa: F405
    "is_hurd",  # noqa: F405
    "is_ibm_powerkvm",  # noqa: F405
    "is_kvmibm",  # noqa: F405
    "is_linuxmint",  # noqa: F405
    "is_macos",  # noqa: F405
    "is_mageia",  # noqa: F405
    "is_mandriva",  # noqa: F405
    "is_midnightbsd",  # noqa: F405
    "is_netbsd",  # noqa: F405
    "is_openbsd",  # noqa: F405
    "is_opensuse",  # noqa: F405
    "is_oracle",  # noqa: F405
    "is_parallels",  # noqa: F405
    "is_pidora",  # noqa: F405
    "is_raspbian",  # noqa: F405
    "is_rhel",  # noqa: F405
    "is_rocky",  # noqa: F405
    "is_scientific",  # noqa: F405
    "is_slackware",  # noqa: F405
    "is_sles",  # noqa: F405
    "is_solaris",  # noqa: F405
    "is_sunos",  # noqa: F405
    "is_ubuntu",  # noqa: F405
    "is_unknown_linux",  # noqa: F405
    "is_windows",  # noqa: F405
    "is_wsl1",  # noqa: F405
    "is_wsl2",  # noqa: F405
    "is_xenserver",  # noqa: F405
    "KVMIBM",  # noqa: F405
    "LINUX_LAYERS",  # noqa: F405
    "LINUX_LIKE",  # noqa: F405
    "LINUXMINT",  # noqa: F405
    "MACOS",  # noqa: F405
    "MAGEIA",  # noqa: F405
    "MANDRIVA",  # noqa: F405
    "MIDNIGHTBSD",  # noqa: F405
    "NETBSD",  # noqa: F405
    "NON_OVERLAPPING_GROUPS",  # noqa: F405
    "OPENBSD",  # noqa: F405
    "OPENSUSE",  # noqa: F405
    "ORACLE",  # noqa: F405
    "OTHER_UNIX",  # noqa: F405
    "PARALLELS",  # noqa: F405
    "PIDORA",  # noqa: F405
    "Platform",  # noqa: F405
    "RASPBIAN",  # noqa: F405
    "reduce",  # noqa: F405
    "RHEL",  # noqa: F405
    "ROCKY",  # noqa: F405
    "SCIENTIFIC",  # noqa: F405
    "SLACKWARE",  # noqa: F405
    "SLES",  # noqa: F405
    "SOLARIS",  # noqa: F405
    "SUNOS",  # noqa: F405
    "SYSTEM_V",  # noqa: F405
    "UBUNTU",  # noqa: F405
    "UNIX",  # noqa: F405
    "UNIX_LAYERS",  # noqa: F405
    "UNIX_WITHOUT_MACOS",  # noqa: F405
    "UNKNOWN_LINUX",  # noqa: F405
    "WINDOWS",  # noqa: F405
    "WSL1",  # noqa: F405
    "WSL2",  # noqa: F405
    "XENSERVER",  # noqa: F405
]
"""Expose all package-wide elements.

.. note::
    The content of ``__all__`` is checked and enforced in unittests.

.. todo::
    Test ruff __all__ formatting capabilities. And if good enough, remove ``__all__``
    checks in unittests.
"""
