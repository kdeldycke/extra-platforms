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
"""Test all terminal definitions, detection and terminal-specific groups."""

from __future__ import annotations

from extra_platforms import (
    ALL_TERMINALS,
    UNKNOWN_TERMINAL,
    current_terminal,
    is_unknown_terminal,
)


def test_terminal_detection():
    """Basic terminal detection sanity checks.

    Family partitions and canonical flags are enforced generically in
    ``test_trait_data.py`` and ``test_group_data.py``.
    """
    current_terminal_result = current_terminal()
    assert current_terminal_result
    if is_unknown_terminal():
        assert current_terminal_result is UNKNOWN_TERMINAL
        assert current_terminal_result not in ALL_TERMINALS
    else:
        assert current_terminal_result is not UNKNOWN_TERMINAL
        assert current_terminal_result in ALL_TERMINALS
