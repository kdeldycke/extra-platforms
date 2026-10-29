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
    KSH,
    NUSHELL,
    POWERSHELL,
    Shell,
)


def test_executable_names():
    """The shells whose binary is not named after their ID declare it, and
    every other shell answers to its ID alone.
    """
    assert KSH.executable_names == {"ksh", "ksh93"}
    assert NUSHELL.executable_names == {"nushell", "nu"}
    assert POWERSHELL.executable_names == {"powershell", "pwsh", "powershell_ise"}
    for shell in ALL_SHELLS:
        assert isinstance(shell, Shell)
        if shell not in {KSH, NUSHELL, POWERSHELL}:
            assert shell.executable_names == {shell.id}
