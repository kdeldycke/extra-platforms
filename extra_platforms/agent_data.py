# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
