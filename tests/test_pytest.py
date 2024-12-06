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

from itertools import chain

import extra_platforms
from extra_platforms import (  # type: ignore[attr-defined]
    is_any_windows,
    is_linux,
    is_macos,
    is_ubuntu,
    is_windows,
)
from extra_platforms.group_data import ALL_GROUPS, ALL_PLATFORMS
from extra_platforms.pytest import (  # type: ignore[attr-defined]
    skip_linux,
    skip_macos,
    skip_ubuntu,
    skip_windows,
    unless_linux,
    unless_macos,
    unless_ubuntu,
    unless_windows,
)


def test_all_definition():
    all_decorator_ids = []
    for _obj in chain(ALL_PLATFORMS, ALL_GROUPS):
        skip_id = f"skip_{_obj.id}"
        unless_id = f"unless_{_obj.id}"
        all_decorator_ids.extend([skip_id, unless_id])
    assert extra_platforms.pytest.__all__ == tuple(sorted(all_decorator_ids))


@skip_linux
def test_skip_linux():
    assert not is_linux()
    assert not is_ubuntu()
    assert is_any_windows() or is_macos() or is_windows()


@skip_macos
def test_skip_macos():
    assert not is_macos()
    assert is_any_windows() or is_linux() or is_ubuntu() or is_windows()


@skip_ubuntu
def test_skip_ubuntu():
    assert not is_ubuntu()
    assert is_any_windows() or is_linux() or is_macos() or is_windows()


@skip_windows
def test_skip_windows():
    assert not is_windows()
    assert not is_any_windows()
    assert is_linux() or is_macos() or is_ubuntu()


@unless_linux
def test_unless_linux():
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    # assert is_ubuntu()
    assert not is_windows()


@unless_macos
def test_unless_macos():
    assert not is_any_windows()
    assert not is_linux()
    assert is_macos()
    assert not is_ubuntu()
    assert not is_windows()


@unless_ubuntu
def test_unless_ubuntu():
    assert not is_any_windows()
    assert is_linux()
    assert not is_macos()
    assert is_ubuntu()
    assert not is_windows()


@unless_windows
def test_unless_windows():
    # assert is_any_windows()
    assert not is_linux()
    assert not is_macos()
    assert not is_ubuntu()
    assert is_windows()
