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
"""CLI entry point for ``python -m extra_platforms`` and ``extra-platforms``."""

from __future__ import annotations

import logging
import sys
import unicodedata

from collections.abc import Iterable

from . import (
    Group,
    Trait,
    __version__,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
    current_terminal,
    current_traits,
)

# Section separator width.
_SEPARATOR_WIDTH = 60


_ZERO_WIDTH = frozenset((
    0xFE0E,  # VS15 — text presentation selector.
    0xFE0F,  # VS16 — emoji presentation selector.
    0x200D,  # ZWJ — zero-width joiner.
))


def _display_width(text: str) -> int:
    """Return the terminal display width of a string.

    Zero-width characters (variation selectors, ZWJ) are skipped.  Remaining
    characters are measured via ``east_asian_width``: **W** and **F** count as
    two columns, everything else as one.  This matches the cursor-advance
    behaviour of most terminal emulators, which follow the East Asian Width
    property rather than the emoji-presentation flag.
    """
    width = 0
    for ch in text:
        if ord(ch) in _ZERO_WIDTH:
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def _pad(text: str, target: int) -> str:
    """Pad ``text`` with spaces to reach ``target`` display columns."""
    return text + " " * max(0, target - _display_width(text))


def _column_widths(items: Iterable[Trait | Group]) -> tuple[int, int, int, int]:
    """Compute column widths for a set of traits or groups."""
    rows = list(items)
    if not rows:
        return (0, 0, 0, 0)
    return (
        max(_display_width(r.icon) for r in rows),
        max(len(r.symbol_id) for r in rows),
        max(len(r.detection_func_id) + 2 for r in rows),
        max(len(r.skip_decorator_id) + 1 for r in rows),
    )


def _merge_widths(*widths: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Return the element-wise maximum of multiple width tuples."""
    return tuple(max(col) for col in zip(*widths))  # type: ignore[return-value]


def _print_table(
    items: Iterable[Trait | Group],
    widths: tuple[int, int, int, int],
) -> None:
    """Print a columnar table of traits or groups.

    Columns: icon, symbol ID, marker, detection function, skip/unless decorators.
    Groups get a ``⬥`` marker when canonical; traits get no marker.
    """
    icon_w, sym_w, det_w, skip_w = widths

    for row in items:
        marker = "⬥" if isinstance(row, Group) and row.canonical else " "
        icon = _pad(row.icon, icon_w)
        sym = f"{row.symbol_id:{sym_w}}"
        det = f"{row.detection_func_id}()"
        skip = f"@{row.skip_decorator_id}"
        unless = f"@{row.unless_decorator_id}"
        print(f"  {marker} {icon}  {sym}  {det:{det_w}}  {skip:{skip_w}}  {unless}")


def _print_trait(label: str, trait: Trait) -> None:
    """Print a detected trait with its info and group memberships.

    :param label: The section label (e.g., "Architecture", "Platform").
    :param trait: The detected trait instance.
    """
    # Section header with integrated separator. Right-align the label so the
    # colon lines up with the info key-value colons at column 18.
    header = f"── {label} ── {trait.icon} {trait.name} ──[{trait.symbol_id}]──"
    print(f"\n{header}{'─' * max(0, _SEPARATOR_WIDTH - len(header))}")

    # Print all info key-value pairs, skipping None values.
    info = trait.info()
    for key, value in info.items():
        if value is None:
            continue
        if key == "id":
            print(f"{key:>14}: {value}")
            # Print aliases right after the ID.
            aliases = ", ".join(sorted(trait.aliases)) if trait.aliases else "-"
            print(f"{'aliases':>14}: {aliases}")
        elif isinstance(value, dict):
            # Print nested dicts inline.
            inner = ", ".join(f"{k}={v}" for k, v in value.items() if v is not None)
            if inner:
                print(f"{key:>14}: {inner}")
        else:
            print(f"{key:>14}: {value}")

    # Print importable references.
    print(f"{'symbol':>14}: {trait.symbol_id}")
    print(f"{'detection':>14}: {trait.detection_func_id}()")
    print(f"{'pytest':>14}: @{trait.skip_decorator_id}, @{trait.unless_decorator_id}")

    # Print group memberships.
    groups = trait.groups
    if groups:
        group_symbols = sorted(g.symbol_id for g in groups)
        print(f"{'groups':>14}: {', '.join(group_symbols)}")


def main() -> None:
    """Print detected environment traits."""
    # Force UTF-8 output on Windows where the default console encoding
    # (e.g. cp1252) cannot represent Unicode box-drawing characters and emoji.
    for stream in (sys.stdout, sys.stderr):
        if stream.encoding and stream.encoding.lower().replace("-", "") != "utf8":
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    # Add a trailing newline to log messages so warnings are visually
    # separated from the CLI output.
    logging.basicConfig(
        stream=sys.stderr,
        format="%(levelname)s: %(message)s\n",
    )

    # Run all detection first so any warnings are emitted before our output.
    arch = current_architecture()
    plat = current_platform()
    shell = current_shell()
    terminal = current_terminal()
    # Suppress the "Unrecognized CI" warning: not running in a CI
    # environment is the common case, not an issue worth reporting.
    logging.disable(logging.WARNING)
    ci = current_ci()
    logging.disable(logging.NOTSET)

    print(f"extra-platforms {__version__}")

    _print_trait("Architecture", arch)
    _print_trait("Platform", plat)
    _print_trait("Shell", shell)
    _print_trait("Terminal", terminal)
    _print_trait("CI", ci)

    # Summary of all detected traits and their groups.
    all_detected = current_traits()
    sorted_traits = sorted(all_detected, key=lambda t: t.id)

    all_groups: set[Group] = set()
    for trait in all_detected:
        all_groups.update(trait.groups)
    sorted_groups = sorted(all_groups, key=lambda g: g.id)

    # Compute column widths across both tables for alignment.
    widths = _merge_widths(
        _column_widths(sorted_traits),
        _column_widths(sorted_groups),
    )

    header = "── Detected traits ──"
    print(f"\n{header}{'─' * max(0, _SEPARATOR_WIDTH - len(header))}")
    _print_table(sorted_traits, widths)

    header = "── Detected groups ──"
    print(f"\n{header}{'─' * max(0, _SEPARATOR_WIDTH - len(header))}")
    _print_table(sorted_groups, widths)


if __name__ == "__main__":
    main()
