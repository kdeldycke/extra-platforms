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
"""Terminal definitions and metadata."""

from __future__ import annotations

from .trait import Terminal

ALACRITTY = Terminal(
    "alacritty",
    "Alacritty",
    "🔳",
    "https://alacritty.org",
)

APPLE_TERMINAL = Terminal(
    "apple_terminal",
    "Apple Terminal",
    "🍏",
    "https://support.apple.com/guide/terminal/welcome/mac",
)

CONTOUR = Terminal(
    "contour",
    "Contour",
    "◰",
    "https://contour-terminal.org",
)

FOOT = Terminal(
    "foot",
    "foot",
    "🦶",
    "https://codeberg.org/dnkl/foot",
)

GHOSTTY = Terminal(
    "ghostty",
    "Ghostty",
    "👻",
    "https://ghostty.org",
)

GNOME_TERMINAL = Terminal(
    "gnome_terminal",
    "GNOME Terminal",
    "𝐆",
    "https://help.gnome.org/users/gnome-terminal/stable/",
)

GNU_SCREEN = Terminal(
    "gnu_screen",
    "GNU Screen",
    "📺",
    "https://www.gnu.org/software/screen/",
)

HYPER = Terminal(
    "hyper",
    "Hyper",
    "⬡",
    "https://hyper.is",
)

ITERM2 = Terminal(
    "iterm2",
    "iTerm2",
    "⬛",
    "https://iterm2.com",
)

KITTY = Terminal(
    "kitty",
    "Kitty",
    "🐱",
    "https://sw.kovidgoyal.net/kitty/",
)

KONSOLE = Terminal(
    "konsole",
    "Konsole",
    "💎",
    "https://konsole.kde.org",
)

RIO = Terminal(
    "rio",
    "Rio",
    "🏞️",
    "https://rioterm.com",
)

TABBY = Terminal(
    "tabby",
    "Tabby",
    "🐈",
    "https://tabby.sh",
)

TILIX = Terminal(
    "tilix",
    "Tilix",
    "🔀",
    "https://gnunn1.github.io/tilix-web/",
)

TMUX = Terminal(
    "tmux",
    "tmux",
    "📟",
    "https://github.com/tmux/tmux/wiki",
)

UNKNOWN_TERMINAL = Terminal(
    "unknown_terminal",
    "Unknown terminal",
    "❓",
    "https://en.wikipedia.org/wiki/Terminal_emulator",
)

VSCODE_TERMINAL = Terminal(
    "vscode_terminal",
    "VS Code Terminal",
    "🔵",
    "https://code.visualstudio.com/docs/terminal/basics",
)

WEZTERM = Terminal(
    "wezterm",
    "WezTerm",
    "🔡",
    "https://wezfurlong.org/wezterm/",
)

WINDOWS_TERMINAL = Terminal(
    "windows_terminal",
    "Windows Terminal",
    "⊡",
    "https://github.com/microsoft/terminal",
)

XTERM = Terminal(
    "xterm",
    "xterm",
    "𝐗",
    "https://invisible-island.net/xterm/",
)

ZELLIJ = Terminal(
    "zellij",
    "Zellij",
    "🪵",
    "https://zellij.dev",
)
