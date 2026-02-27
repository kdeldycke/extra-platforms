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
"""Agent definitions and metadata."""

from __future__ import annotations

from .trait import Agent

CLAUDE_CODE = Agent("claude_code", "Claude Code", "✴️", "https://claude.ai/code")

CLINE = Agent("cline", "Cline", "👾", "https://cline.bot")

CURSOR = Agent("cursor", "Cursor", "➤", "https://cursor.com")

UNKNOWN_AGENT = Agent(
    "unknown_agent",
    "Unknown agent",
    "❓",
    "https://en.wikipedia.org/wiki/AI_agent",
)
