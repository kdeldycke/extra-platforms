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
"""Test all platform definitions and platform-specific groups."""

from __future__ import annotations

import ast
from pathlib import Path

from extra_platforms import (
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    CHROMEOS,
    LINUX,
    LINUX_LAYERS,
    LINUX_LIKE,
    OTHER_POSIX,
    SYSTEM_V,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_PLATFORM,
    WSL1,
    WSL2,
    current_platform,
    is_any_platform,
    is_any_trait,
    is_unknown_platform,
)
from extra_platforms.pytest import skip_hermetic_build


# Platform detection reads OS-release files that a hermetic build sandbox
# (Guix, Nix; both set HOME=/homeless-shelter) does not provide, so no real
# platform is detected there.
@skip_hermetic_build
def test_platform_detection():
    # We always expect to detect a platform.
    assert is_any_trait()
    assert is_any_platform()
    assert not is_unknown_platform()
    assert current_platform() is not UNKNOWN_PLATFORM


def test_platform_mutual_exclusion():
    """A single platform matches, apart from documented compatibility layers.

    WSL and ChromeOS legitimately match alongside the Linux distribution they
    host, as documented in `current_platform()`.
    """
    matching = {platform for platform in ALL_PLATFORMS if platform.current}
    layers = matching & {CHROMEOS, WSL1, WSL2}
    hosts = matching - layers
    assert len(hosts) <= 1
    # A detected layer either stands alone or hosts a Linux distribution.
    if layers:
        assert all(host in LINUX for host in hosts)


def test_platform_logical_grouping():
    """Check set relationships specific to platform groups.

    Family partitions and canonical flags are enforced generically in
    ``test_trait_data.py`` and ``test_group_data.py``. The relationships below
    involve the non-canonical UNIX, LINUX_LIKE and *_WITHOUT_MACOS groups, so
    they are only checked here.
    """
    # All platforms are divided into Windows and Unix at the highest level.
    assert ALL_PLATFORMS.fullyintersects(ALL_WINDOWS | UNIX)

    # Every group is a subset of UNIX except Windows and ALL_PLATFORMS.
    for group in ALL_PLATFORM_GROUPS:
        if group is ALL_WINDOWS or group is ALL_PLATFORMS:
            assert not group.issubset(UNIX)
            assert not UNIX.issuperset(group)
        else:
            assert group.issubset(UNIX)
            assert UNIX.issuperset(group)

    # All UNIX platforms are divided into BSD, Linux, and Unix families.
    assert UNIX.fullyintersects(
        BSD | LINUX | LINUX_LAYERS | SYSTEM_V | UNIX_LAYERS | OTHER_POSIX
    )

    # LINUX_LIKE is the union of LINUX and LINUX_LAYERS.
    assert LINUX.issubset(LINUX_LIKE)
    assert LINUX_LAYERS.issubset(LINUX_LIKE)
    assert LINUX_LIKE.issuperset(LINUX)
    assert LINUX_LIKE.issuperset(LINUX_LAYERS)

    # Relationships specific to UNIX_WITHOUT_MACOS.
    assert UNIX_WITHOUT_MACOS.issubset(UNIX)
    assert UNIX.issuperset(UNIX_WITHOUT_MACOS)

    # Relationships specific to BSD_WITHOUT_MACOS.
    assert BSD_WITHOUT_MACOS.issubset(UNIX)
    assert BSD_WITHOUT_MACOS.issubset(BSD)
    assert UNIX.issuperset(BSD_WITHOUT_MACOS)
    assert BSD.issuperset(BSD_WITHOUT_MACOS)


def _in_private_use_area(char: str) -> bool:
    """Return ``True`` for a Unicode Private Use Area codepoint.

    NerdFont glyphs live in the PUA. Ordinary emoji sit above ``U+E000`` as well, so
    a bare ``>= U+E000`` test misclassifies them; match the three PUA ranges instead.
    """
    codepoint = ord(char)
    return (
        0xE000 <= codepoint <= 0xF8FF
        or 0xF0000 <= codepoint <= 0xFFFFD
        or 0x100000 <= codepoint <= 0x10FFFD
    )


def test_nerdfont_icons_documented_in_source():
    """Every platform with a NerdFont icon embeds that glyph in its docstring.

    NerdFont glyphs live in the Unicode Private Use Area and render as an
    invisible or placeholder character without a patched font, so
    each such platform carries an attribute docstring warning about the font
    requirement, whose icon link repeats the glyph. Because the glyph is invisible
    in an editor, it is easy to drop from that link by accident, which then renders
    as broken plaintext instead of a hyperlink. Lock the invariant by parsing the
    source: every NerdFont-icon platform must have an attribute docstring, and that
    docstring must contain the glyph itself.
    """
    source = (
        Path(__file__).parent.parent / "extra_platforms" / "platform_data.py"
    ).read_text(encoding="utf-8")
    body = ast.parse(source).body

    checked = []
    for definition, following in zip(body, body[1:]):
        # Match a module-level "NAME = Platform(id, name, icon, url)" assignment.
        if not (
            isinstance(definition, ast.Assign)
            and len(definition.targets) == 1
            and isinstance(definition.targets[0], ast.Name)
            and isinstance(definition.value, ast.Call)
            and isinstance(definition.value.func, ast.Name)
            and definition.value.func.id == "Platform"
            and len(definition.value.args) >= 3
            and isinstance(definition.value.args[2], ast.Constant)
            and isinstance(definition.value.args[2].value, str)
        ):
            continue

        icon = definition.value.args[2].value
        # Only NerdFont icons (Private Use Area codepoints) are concerned.
        if not any(_in_private_use_area(char) for char in icon):
            continue

        name = definition.targets[0].id
        checked.append(name)

        # The assignment must be immediately followed by an attribute docstring.
        assert (
            isinstance(following, ast.Expr)
            and isinstance(following.value, ast.Constant)
            and isinstance(following.value.value, str)
        ), (
            f"Platform {name} uses NerdFont icon {icon!r} but has no attribute "
            f"docstring documenting the font requirement."
        )
        # The docstring must embed the glyph, or the icon link renders broken.
        assert icon in following.value.value, (
            f"Platform {name}'s NerdFont icon {icon!r} is missing from its "
            f"attribute docstring; the icon link renders as broken plaintext."
        )

    assert checked, "expected NerdFont-icon platforms such as ALMALINUX and NOBARA"
