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
"""Shell definitions and metadata."""

from __future__ import annotations

from .trait import Shell

ASH = Shell(
    "ash",
    "Almquist Shell",
    "🪶",
    "https://en.wikipedia.org/wiki/Almquist_shell",
)

BASH = Shell(
    "bash",
    "Bash",
    "＃",
    "https://www.gnu.org/software/bash/",
)

CMD = Shell(
    "cmd",
    "Command Prompt",
    "▶",
    "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd",
)

CSH = Shell(
    "csh",
    "C shell",
    "𝐂",
    "https://en.wikipedia.org/wiki/C_shell",
)

DASH = Shell(
    "dash",
    "Dash",
    "💨",
    "https://en.wikipedia.org/wiki/Almquist_shell#dash",
)

FISH = Shell(
    "fish",
    "Fish",
    "🐟",
    "https://fishshell.com",
)

KSH = Shell(
    "ksh",
    "Korn shell",
    "𝐊",
    "https://en.wikipedia.org/wiki/KornShell",
)

NUSHELL = Shell(
    "nushell",
    "Nushell",
    "𝜈",
    "https://www.nushell.sh",
)

POWERSHELL = Shell(
    "powershell",
    "PowerShell",
    "🔷",
    "https://learn.microsoft.com/en-us/powershell/",
)

TCSH = Shell(
    "tcsh",
    "tcsh",
    "𝐓",
    "https://www.tcsh.org",
)

UNKNOWN_SHELL = Shell(
    "unknown_shell",
    "Unknown shell",
    "❓",
    "https://en.wikipedia.org/wiki/Shell_(computing)",
)

XONSH = Shell(
    "xonsh",
    "Xonsh",
    "🐍",
    "https://xon.sh",
)

ZSH = Shell(
    "zsh",
    "Zsh",
    "ℤ",
    "https://www.zsh.org",
)
