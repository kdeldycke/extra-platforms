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
"""Test all agent definitions, detection and agent-specific groups."""

from __future__ import annotations

from extra_platforms import (
    ALL_AGENTS,
    UNKNOWN_AGENT,
    current_agent,
    is_any_agent,
    is_any_trait,  # type: ignore[attr-defined]
    is_claude_code,
    is_cline,
    is_cursor,
    is_unknown_agent,
)


def test_agent_detection():
    # We always expect to detect something.
    assert is_any_trait()

    # We don't always expect to detect an agent.
    assert current_agent()
    if is_unknown_agent():
        assert current_agent() is UNKNOWN_AGENT
        assert current_agent() not in ALL_AGENTS
        assert not is_any_agent()
    else:
        assert current_agent() is not UNKNOWN_AGENT
        assert current_agent() in ALL_AGENTS
        assert is_any_agent()

    if is_claude_code():
        assert not is_cline()
        assert not is_cursor()

    if is_cline():
        assert not is_claude_code()
        assert not is_cursor()

    if is_cursor():
        assert not is_claude_code()
        assert not is_cline()


def test_agent_logical_grouping():
    assert ALL_AGENTS.canonical
