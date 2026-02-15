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

from . import (
    Group,
    Trait,
    __version__,
    current_architecture,
    current_ci,
    current_platform,
    current_shell,
)

# Section separator width.
_SEPARATOR_WIDTH = 60


def _display_width(text: str) -> int:
    """Return the terminal display width of a string.

    Uses ``unicodedata.east_asian_width`` to account for wide characters
    (emoji, CJK) that occupy two columns in a monospace terminal.
    """
    width = 0
    for ch in text:
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def _pad(text: str, target: int) -> str:
    """Pad ``text`` with spaces to reach ``target`` display columns."""
    return text + " " * max(0, target - _display_width(text))


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
    # Suppress the "Unrecognized CI" warning: not running in a CI
    # environment is the common case, not an issue worth reporting.
    logging.disable(logging.WARNING)
    ci = current_ci()
    logging.disable(logging.NOTSET)

    print(f"extra-platforms {__version__}")

    _print_trait("Architecture", arch)
    _print_trait("Platform", plat)
    _print_trait("Shell", shell)
    _print_trait("CI", ci)

    # Collect all groups from detected traits, deduplicated and sorted.
    all_groups: set[Group] = set()
    for trait in (arch, plat, shell, ci):
        all_groups.update(trait.groups)

    header = "── Groups ──"
    print(f"\n{header}{'─' * max(0, _SEPARATOR_WIDTH - len(header))}")

    sorted_groups = sorted(all_groups, key=lambda g: g.id)

    # Compute column widths for alignment using display width.
    icon_w = max(_display_width(g.icon) for g in sorted_groups)
    sym_w = max(len(g.symbol_id) for g in sorted_groups)
    det_w = max(len(g.detection_func_id) + 2 for g in sorted_groups)
    skip_w = max(len(g.skip_decorator_id) + 1 for g in sorted_groups)

    for group in sorted_groups:
        canon = " ⬥" if group.canonical else "  "
        icon = _pad(group.icon, icon_w)
        sym = f"{group.symbol_id:{sym_w}}"
        det = f"{group.detection_func_id}()"
        skip = f"@{group.skip_decorator_id}"
        unless = f"@{group.unless_decorator_id}"
        print(f"  {icon} {sym}{canon}  {det:{det_w}}  {skip:{skip_w}}  {unless}")


if __name__ == "__main__":
    main()
