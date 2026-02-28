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
"""Test all agent definitions, detection and agent-specific groups."""

from __future__ import annotations

from extra_platforms import (  # type: ignore[attr-defined]
    ALL_AGENTS,
    UNKNOWN_AGENT,
    current_agent,
    is_any_agent,
    is_any_trait,
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
