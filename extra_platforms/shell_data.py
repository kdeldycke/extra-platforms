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
    "©",
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
    "⚡",
    "https://learn.microsoft.com/en-us/powershell/",
)

TCSH = Shell(
    "tcsh",
    "tcsh",
    "🌊",
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
    "🐚",
    "https://xon.sh",
)

ZSH = Shell(
    "zsh",
    "Zsh",
    "ℤ",
    "https://www.zsh.org",
)
