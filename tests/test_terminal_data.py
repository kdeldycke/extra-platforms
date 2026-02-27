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
"""Test all terminal definitions, detection and terminal-specific groups."""

from __future__ import annotations

from extra_platforms import (
    ALL_TERMINALS,
    GPU_TERMINALS,
    MULTIPLEXERS,
    NATIVE_TERMINALS,
    UNKNOWN_TERMINAL,
    WEB_TERMINALS,
    current_terminal,
    is_unknown_terminal,
)


def test_terminal_detection():
    """Basic terminal detection sanity checks."""
    current_terminal_result = current_terminal()
    assert current_terminal_result
    if is_unknown_terminal():
        assert current_terminal_result is UNKNOWN_TERMINAL
        assert current_terminal_result not in ALL_TERMINALS
    else:
        assert current_terminal_result is not UNKNOWN_TERMINAL
        assert current_terminal_result in ALL_TERMINALS


def test_terminal_logical_grouping():
    # All terminals are divided into families.
    assert ALL_TERMINALS.fullyintersects(
        GPU_TERMINALS | MULTIPLEXERS | NATIVE_TERMINALS | WEB_TERMINALS
    )
    assert not ALL_TERMINALS.canonical
    assert GPU_TERMINALS.canonical
    assert MULTIPLEXERS.canonical
    assert NATIVE_TERMINALS.canonical
    assert WEB_TERMINALS.canonical
