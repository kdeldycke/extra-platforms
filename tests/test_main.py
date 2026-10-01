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
"""Test the rendering helpers of the command-line interface."""

from __future__ import annotations

from operator import attrgetter

import pytest

from extra_platforms import ALL_TRAITS
from extra_platforms.__main__ import _SEPARATOR_WIDTH, _display_width, _print_trait


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
