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
"""Test all shell definitions, detection and shell-specific groups."""

from __future__ import annotations

from extra_platforms import (
    ALL_SHELLS,
    BOURNE_SHELLS,
    C_SHELLS,
    OTHER_SHELLS,
    UNKNOWN_SHELL,
    WINDOWS_SHELLS,
    current_shell,
    is_unknown_shell,
)


def test_shell_detection():
    """Basic shell detection sanity checks."""
    current_shell_result = current_shell()
    assert current_shell_result
    if is_unknown_shell():
        assert current_shell_result is UNKNOWN_SHELL
        assert current_shell_result not in ALL_SHELLS
    else:
        assert current_shell_result is not UNKNOWN_SHELL
        assert current_shell_result in ALL_SHELLS


def test_shell_logical_grouping():
    # All shells are divided into families.
    assert ALL_SHELLS.fullyintersects(
        BOURNE_SHELLS | C_SHELLS | OTHER_SHELLS | WINDOWS_SHELLS
    )
    assert not ALL_SHELLS.canonical
    assert BOURNE_SHELLS.canonical
    assert C_SHELLS.canonical
    assert OTHER_SHELLS.canonical
    assert WINDOWS_SHELLS.canonical


