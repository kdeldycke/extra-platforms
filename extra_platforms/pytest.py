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
"""Pytest decorators to skip tests depending on the platform they're run on."""

from __future__ import annotations

try:
    import pytest  # noqa: F401
except ImportError:
    raise ImportError(
        "You need to install extra_platforms[pytest] extra dependencies to use this "
        "module."
    )


from . import ALL_LINUX, CURRENT_OS_ID, is_macos, is_windows

skip_linux = pytest.mark.skipif(
    CURRENT_OS_ID in ALL_LINUX.platform_ids, reason="Skip Linux"
)
"""Pytest mark to skip a test if run on a Linux system."""

skip_macos = pytest.mark.skipif(is_macos(), reason="Skip macOS")
"""Pytest mark to skip a test if run on a macOS system."""

skip_windows = pytest.mark.skipif(is_windows(), reason="Skip Windows")
"""Pytest mark to skip a test if run on a Windows system."""


unless_linux = pytest.mark.skipif(
    CURRENT_OS_ID not in ALL_LINUX.platform_ids, reason="Linux required"
)
"""Pytest mark to skip a test unless it is run on a Linux system."""

unless_macos = pytest.mark.skipif(not is_macos(), reason="macOS required")
"""Pytest mark to skip a test unless it is run on a macOS system."""

unless_windows = pytest.mark.skipif(not is_windows(), reason="Windows required")
"""Pytest mark to skip a test unless it is run on a Windows system."""
