# {octicon}`terminal` Terminals

```{py:currentmodule} extra_platforms
```

Each terminal represents an application rendering the shell's output, and is associated with:

- a unique terminal ID
- a human-readable name
- an icon (emoji / unicode character)
- a [detection function](detection.md)
- various metadata in its `info()` method

## Terminal usage

Each terminal is materialized by a {class}`~Terminal` object, from which you can access various metadata:

```pycon
>>> from extra_platforms import KITTY
>>> KITTY
Terminal(id='kitty', name='Kitty')
>>> KITTY.id
'kitty'
>>> KITTY.current
False
>>> KITTY.info()
{'id': 'kitty', 'name': 'Kitty', 'icon': '🐱', 'url': 'https://sw.kovidgoyal.net/kitty/', 'current': False, 'version': None, 'color_support': None}
```

To check if the current environment is running in a specific terminal, use the corresponding [detection function](detection.md):

```pycon
>>> from extra_platforms import is_kitty
>>> is_kitty()
False
```

The current terminal can be obtained via the `current_terminal()` function:

```pycon
>>> from extra_platforms import current_terminal
>>> current_terminal()
Terminal(id='unknown_terminal', name='Unknown terminal')
```

## Recognized terminals

<!-- terminal-table-start -->

| Icon | Symbol                    | Name             | Detection function           |
| :--: | :------------------------ | :--------------- | :--------------------------- |
|  🔳  | {data}`~ALACRITTY`        | Alacritty        | {func}`~is_alacritty`        |
|  🍏  | {data}`~APPLE_TERMINAL`   | Apple Terminal   | {func}`~is_apple_terminal`   |
|  ◰   | {data}`~CONTOUR`          | Contour          | {func}`~is_contour`          |
|  🦶  | {data}`~FOOT`             | foot             | {func}`~is_foot`             |
|  👻  | {data}`~GHOSTTY`          | Ghostty          | {func}`~is_ghostty`          |
|  𝐆   | {data}`~GNOME_TERMINAL`   | GNOME Terminal   | {func}`~is_gnome_terminal`   |
|  📺  | {data}`~GNU_SCREEN`       | GNU Screen       | {func}`~is_gnu_screen`       |
|  ⬡   | {data}`~HYPER`            | Hyper            | {func}`~is_hyper`            |
|  ⬛  | {data}`~ITERM2`           | iTerm2           | {func}`~is_iterm2`           |
|  🐱  | {data}`~KITTY`            | Kitty            | {func}`~is_kitty`            |
|  💎  | {data}`~KONSOLE`          | Konsole          | {func}`~is_konsole`          |
|  🏞️  | {data}`~RIO`              | Rio              | {func}`~is_rio`              |
|  🐈  | {data}`~TABBY`            | Tabby            | {func}`~is_tabby`            |
|  🔀  | {data}`~TILIX`            | Tilix            | {func}`~is_tilix`            |
|  📟  | {data}`~TMUX`             | tmux             | {func}`~is_tmux`             |
|  🔵  | {data}`~VSCODE_TERMINAL`  | VS Code Terminal | {func}`~is_vscode_terminal`  |
|  🔡  | {data}`~WEZTERM`          | WezTerm          | {func}`~is_wezterm`          |
|  ⊡   | {data}`~WINDOWS_TERMINAL` | Windows Terminal | {func}`~is_windows_terminal` |
|  𝐗   | {data}`~XTERM`            | xterm            | {func}`~is_xterm`            |
|  🪵  | {data}`~ZELLIJ`           | Zellij           | {func}`~is_zellij`           |

```{hint}
The {data}`~UNKNOWN_TERMINAL` trait represents an unrecognized
terminal. It is not included in the {data}`~ALL_TERMINALS` group,
and will be returned by {func}`~current_terminal` if the current
terminal is not recognized.
```

<!-- terminal-table-end -->

## Groups of terminals

<!-- terminal-groups-table-start -->

| Icon | Symbol                  | Description                | [Detection](detection.md)    | [Canonical](groups.md#extra_platforms.Group.canonical) |
| :--: | :---------------------- | :------------------------- | :--------------------------- | :----------------------------------------------------: |
|  💻  | {data}`~ALL_TERMINALS`  | All terminals              | {func}`~is_any_terminal`     |                                                        |
|  🎮  | {data}`~GPU_TERMINALS`  | GPU-accelerated terminals  | {func}`~is_gpu_terminals`    |                           ⬥                            |
|  ⧉   | {data}`~MULTIPLEXERS`   | Terminal multiplexers      | {func}`~is_multiplexers`     |                           ⬥                            |
|  ▦   | {data}`~NATIVE_TERMINALS` | Native terminal emulators | {func}`~is_native_terminals` |                           ⬥                            |
|  ⬢   | {data}`~WEB_TERMINALS`  | Web-based terminals        | {func}`~is_web_terminals`    |                           ⬥                            |

```{hint}
Canonical groups are non-overlapping groups that together cover all
recognized traits. They are marked with a ⬥ icon in the table above.

Other groups are provided for convenience, but overlap with each other or
with canonical groups.
```

<!-- terminal-groups-table-end -->

<!-- terminal-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 800}}
---
sankey-beta

GPU_TERMINALS,ALACRITTY,1
GPU_TERMINALS,CONTOUR,1
GPU_TERMINALS,FOOT,1
GPU_TERMINALS,GHOSTTY,1
GPU_TERMINALS,KITTY,1
GPU_TERMINALS,RIO,1
GPU_TERMINALS,WEZTERM,1
MULTIPLEXERS,GNU_SCREEN,1
MULTIPLEXERS,TMUX,1
MULTIPLEXERS,ZELLIJ,1
NATIVE_TERMINALS,APPLE_TERMINAL,1
NATIVE_TERMINALS,GNOME_TERMINAL,1
NATIVE_TERMINALS,ITERM2,1
NATIVE_TERMINALS,KONSOLE,1
NATIVE_TERMINALS,TILIX,1
NATIVE_TERMINALS,WINDOWS_TERMINAL,1
NATIVE_TERMINALS,XTERM,1
WEB_TERMINALS,HYPER,1
WEB_TERMINALS,TABBY,1
WEB_TERMINALS,VSCODE_TERMINAL,1
```

<!-- terminal-sankey-end -->

<!-- terminal-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((💻 ALL_TERMINALS))
        ((🎮 GPU_TERMINALS))
            (🔳 ALACRITTY)
            (◰ CONTOUR)
            (🦶 FOOT)
            (👻 GHOSTTY)
            (🐱 KITTY)
            (🏞️ RIO)
            (🔡 WEZTERM)
        ((⧉ MULTIPLEXERS))
            (📺 GNU_SCREEN)
            (📟 TMUX)
            (🪵 ZELLIJ)
        ((▦ NATIVE_TERMINALS))
            (🍏 APPLE_TERMINAL)
            (𝐆 GNOME_TERMINAL)
            (⬛ ITERM2)
            (💎 KONSOLE)
            (🔀 TILIX)
            (⊡ WINDOWS_TERMINAL)
            (𝐗 XTERM)
        ((⬢ WEB_TERMINALS))
            (⬡ HYPER)
            (🐈 TABBY)
            (🔵 VSCODE_TERMINAL)
```

<!-- terminal-mindmap-end -->

## Predefined terminals

```{eval-rst}
.. autoclasstree:: extra_platforms.terminal_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.terminal_data
   :no-index:
```

<!-- terminal-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.ALACRITTY
.. autodata:: extra_platforms.APPLE_TERMINAL
.. autodata:: extra_platforms.CONTOUR
.. autodata:: extra_platforms.FOOT
.. autodata:: extra_platforms.GHOSTTY
.. autodata:: extra_platforms.GNOME_TERMINAL
.. autodata:: extra_platforms.GNU_SCREEN
.. autodata:: extra_platforms.HYPER
.. autodata:: extra_platforms.ITERM2
.. autodata:: extra_platforms.KITTY
.. autodata:: extra_platforms.KONSOLE
.. autodata:: extra_platforms.RIO
.. autodata:: extra_platforms.TABBY
.. autodata:: extra_platforms.TILIX
.. autodata:: extra_platforms.TMUX
.. autodata:: extra_platforms.UNKNOWN_TERMINAL
.. autodata:: extra_platforms.VSCODE_TERMINAL
.. autodata:: extra_platforms.WEZTERM
.. autodata:: extra_platforms.WINDOWS_TERMINAL
.. autodata:: extra_platforms.XTERM
.. autodata:: extra_platforms.ZELLIJ
```

<!-- terminal-data-autodata-end -->
