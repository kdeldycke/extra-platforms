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
"""Test the command-line interface and its rendering helpers."""

from __future__ import annotations

import json
import sys
from operator import attrgetter

import pytest

from extra_platforms import (
    ALL_TRAITS,
    __version__,
    current_agent,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
    current_terminal,
)
from extra_platforms.__main__ import (
    _SEPARATOR_WIDTH,
    _column_widths,
    _display_width,
    _print_trait,
    main,
)

CURRENT_FUNCS = {
    "architecture": current_architecture,
    "platform": current_platform,
    "shell": current_shell,
    "terminal": current_terminal,
    "ci": current_ci,
    "agent": current_agent,
}
"""The trait each section of the report covers, in report order."""


@pytest.mark.parametrize(
    "trait", sorted(ALL_TRAITS, key=attrgetter("id")), ids=attrgetter("id")
)
def test_trait_header_spans_separator_width(trait, capsys):
    """Each trait header rules out to the separator width, whatever its icon width."""
    _print_trait("Platform", trait)
    header = capsys.readouterr().out.splitlines()[1]
    # The header text itself ends on two rule characters.
    unruled_width = _display_width(header.rstrip("─")) + 2
    assert _display_width(header) == max(_SEPARATOR_WIDTH, unruled_width)


def test_column_widths_of_no_rows():
    """An empty table needs no column width."""
    assert _column_widths([]) == (0, 0, 0, 0)


def test_main_text_report(monkeypatch, capsys):
    """The text report covers each trait category, then the two tables."""
    monkeypatch.setattr(sys, "argv", ["extra-platforms"])
    main()
    lines = capsys.readouterr().out.splitlines()

    assert lines[0] == f"extra-platforms {__version__}"
    sections = [line[3:].split(" ──")[0] for line in lines if line.startswith("── ")]
    assert sections == [
        "Architecture",
        "Platform",
        "Shell",
        "Terminal",
        "CI",
        "Agent",
        "Detected traits",
        "Detected groups",
    ]
    for current in CURRENT_FUNCS.values():
        trait = current()
        assert any(
            f"── {trait.icon} {trait.name} ──[{trait.symbol_id}]" in line
            for line in lines
        )


def test_main_json_report(monkeypatch, capsys):
    """`--json` reports what the API detects, as a single JSON object."""
    monkeypatch.setattr(sys, "argv", ["extra-platforms", "--json"])
    main()
    data = json.loads(capsys.readouterr().out)

    assert list(data) == ["version", *CURRENT_FUNCS, "groups"]
    assert data["version"] == __version__
    for key, current in CURRENT_FUNCS.items():
        trait = current()
        assert data[key]["id"] == trait.id
        assert data[key]["symbol"] == trait.symbol_id
        assert data[key]["groups"] == sorted(g.symbol_id for g in trait.groups)

    group_ids = [group["id"] for group in data["groups"]]
    assert group_ids == sorted(group_ids)
    assert all(
        set(group) == {"id", "name", "icon", "symbol", "detection", "canonical"}
        for group in data["groups"]
    )
