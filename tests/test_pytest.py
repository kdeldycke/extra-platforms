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
    LINUX,
    current_os,
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
    assert current_os() not in LINUX
    assert is_macos() or is_windows()


@skip_macos
def test_skip_macos():
    assert not is_macos()
    assert current_os() in LINUX or is_windows()


@skip_windows
def test_skip_windows():
    assert not is_windows()
    assert current_os() in LINUX or is_macos()


@unless_linux
def test_unless_linux():
    assert current_os() in LINUX
    assert not is_macos()
    assert not is_windows()


@unless_macos
def test_unless_macos():
    assert current_os() not in LINUX
    assert is_macos()
    assert not is_windows()


@unless_windows
def test_unless_windows():
    assert current_os() not in LINUX
    assert not is_macos()
    assert is_windows()
