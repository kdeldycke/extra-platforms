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
