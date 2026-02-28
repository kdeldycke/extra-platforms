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
