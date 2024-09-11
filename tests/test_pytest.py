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

from __future__ import annotations

from extra_platforms import (
    CURRENT_OS_ID,
    LINUX,
    is_macos,
    is_windows,
)
from extra_platforms.pytest import (
    skip_linux,
    skip_macos,
    skip_windows,
    unless_linux,
    unless_macos,
    unless_windows,
)


@skip_linux
def test_skip_linux():
    assert CURRENT_OS_ID not in LINUX.platform_ids
    assert is_macos() or is_windows()


@skip_macos
def test_skip_macos():
    assert not is_macos()
    assert CURRENT_OS_ID in LINUX.platform_ids or is_windows()


@skip_windows
def test_skip_windows():
    assert not is_windows()
    assert CURRENT_OS_ID in LINUX.platform_ids or is_macos()


@unless_linux
def test_unless_linux():
    assert CURRENT_OS_ID in LINUX.platform_ids
    assert not is_macos()
    assert not is_windows()


@unless_macos
def test_unless_macos():
    assert CURRENT_OS_ID not in LINUX.platform_ids
    assert is_macos()
    assert not is_windows()


@unless_windows
def test_unless_windows():
    assert CURRENT_OS_ID not in LINUX.platform_ids
    assert not is_macos()
    assert is_windows()
