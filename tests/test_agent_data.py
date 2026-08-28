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

import logging

import pytest

from extra_platforms import (
    ALL_AGENTS,
    UNKNOWN_AGENT,
    current_agent,
    detection,
    invalidate_caches,
    is_any_agent,
    is_unknown_agent,
)
from extra_platforms.detection import _AGENT_PRESENCE_ENV_VARS


def test_agent_detection():
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


def test_agent_mutual_exclusion():
    """At most one agent matches the current environment."""
    matching = {agent for agent in ALL_AGENTS if agent.current}
    assert len(matching) <= 1


def _agent_log_levels(fake_environ, caplog):
    """Resolve the current agent against ``fake_environ`` and collect log levels.

    Detection reads ``detection.environ`` and caches every answer, so the
    environment is swapped wholesale and the caches are cleared on both sides of
    the call: on entry so nothing carries over from the real environment, and on
    exit so the next caller recomputes against it.
    """
    invalidate_caches()
    caplog.set_level(logging.INFO)
    try:
        agent = current_agent()
        return agent, [record.levelno for record in caplog.records]
    finally:
        invalidate_caches()


@pytest.mark.parametrize("env_var", _AGENT_PRESENCE_ENV_VARS)
def test_agent_presence_var_escalates_unrecognized(env_var, monkeypatch, caplog):
    """Each generic presence variable raises an unrecognized agent to a warning.

    Covers every member of {data}`~extra_platforms.detection._AGENT_PRESENCE_ENV_VARS`,
    so a variable added there without being read by the gate fails here.
    """
    monkeypatch.setattr(detection, "environ", {env_var: "some-unreleased-agent"})
    agent, levels = _agent_log_levels(detection.environ, caplog)
    assert agent is UNKNOWN_AGENT
    assert levels == [logging.WARNING]


def test_no_agent_presence_var_stays_informational(monkeypatch, caplog):
    """An environment naming no agent at all logs at INFO, not WARNING."""
    monkeypatch.setattr(detection, "environ", {})
    agent, levels = _agent_log_levels(detection.environ, caplog)
    assert agent is UNKNOWN_AGENT
    assert levels == [logging.INFO]


@pytest.mark.parametrize("env_var", _AGENT_PRESENCE_ENV_VARS)
def test_agent_presence_vars_are_reported(env_var, monkeypatch, caplog):
    """Each generic presence variable is surfaced in the unrecognized report."""
    monkeypatch.setattr(detection, "environ", {env_var: "some-unreleased-agent"})
    _agent, _levels = _agent_log_levels(detection.environ, caplog)
    assert f"{env_var}:" in caplog.text
    assert "some-unreleased-agent" in caplog.text
