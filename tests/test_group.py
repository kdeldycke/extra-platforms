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

from __future__ import annotations

import pytest

from extra_platforms import (
    AIX,
    ALL_CI,
    ALL_PLATFORMS,
    ANY_WINDOWS,
    BSD,
    BSD_WITHOUT_MACOS,
    LINUX,
    LINUX_LAYERS,
    PIDORA,
    RHEL,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    Group,
)


def test_platform_deduplication():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    assert len(my_group) == 1
    assert len(my_group.members) == 1
    assert len(my_group.member_ids) == 1

    assert my_group.members == (AIX,)
    assert my_group.member_ids == frozenset({"aix"})


def test_platform_membership():
    my_group = Group("my_group", "My Group", "✅", (AIX, PIDORA))

    # Test iteration.
    assert list(my_group) == [AIX, PIDORA]
    assert tuple(my_group) == (AIX, PIDORA)
    assert set(my_group) == {AIX, PIDORA}

    # Test platform membership.
    assert AIX in my_group
    assert PIDORA in my_group
    assert RHEL not in my_group

    # Test platform ID membership.
    assert "aix" in my_group
    assert "pidora" in my_group
    assert "rhel" not in my_group

    # Test platform ID getter.
    assert my_group["aix"] == AIX
    assert my_group["pidora"] == PIDORA
    with pytest.raises(KeyError):
        my_group["rhel"]

    # Test platform items getter.
    assert list(my_group.items()) == [("aix", AIX), ("pidora", PIDORA)]


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], []),
        (tuple(), tuple()),
        (set(), set()),
        (frozenset(), frozenset()),
        (None, []),
        ([None], []),
        ([None, None, None], []),
        ([None, (None, None, [])], []),
        (AIX, [AIX]),
        ("aix", [AIX]),
        ([AIX], [AIX]),
        ([AIX, AIX], [AIX, AIX]),
        ([AIX, (AIX, AIX)], [AIX, AIX, AIX]),
        ([AIX, ("aix", AIX)], [AIX, AIX, AIX]),
        (LINUX_LAYERS, LINUX_LAYERS.members),
        (LINUX_LAYERS, LINUX_LAYERS),
        ("linux_layers", LINUX_LAYERS),
        ([LINUX_LAYERS], LINUX_LAYERS),
        ([LINUX_LAYERS, LINUX_LAYERS], LINUX_LAYERS.members * 2),
        ([LINUX_LAYERS, (LINUX_LAYERS, LINUX_LAYERS)], LINUX_LAYERS.members * 3),
        ([LINUX_LAYERS, ("linux_layers", LINUX_LAYERS)], LINUX_LAYERS.members * 3),
    ],
)
def test_extract_members(items, expected):
    assert tuple(Group._extract_members(items)) == tuple(expected)


@pytest.mark.parametrize(
    "item", (42, 42.0, object(), lambda: None, [42], [42, 42], [42, [42, 42]])
)
def test_extract_members_bad_type(item):
    with pytest.raises(TypeError):
        tuple(Group._extract_members(item))


def test_simple_union():
    new_group = ANY_WINDOWS.union(LINUX_LAYERS)

    assert ANY_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert new_group.issuperset(ANY_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)

    assert new_group.id == ANY_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.name == ANY_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.icon == ANY_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon

    assert set(new_group.members) != set(ANY_WINDOWS.members)
    assert set(new_group.member_ids) != set(ANY_WINDOWS.member_ids)
    assert set(new_group.members) != set(LINUX_LAYERS.members)
    assert set(new_group.member_ids) != set(LINUX_LAYERS.member_ids)

    assert set(new_group.members) == set(ANY_WINDOWS.members).union(
        LINUX_LAYERS.members
    )
    assert set(new_group.member_ids) == set(ANY_WINDOWS.member_ids).union(
        LINUX_LAYERS.member_ids
    )


def test_multiple_union():
    new_group = ANY_WINDOWS.union(LINUX_LAYERS, UNIX_LAYERS)

    assert new_group.member_ids == frozenset(("windows", "wsl1", "wsl2", "cygwin"))

    assert ANY_WINDOWS.issubset(new_group)
    assert LINUX_LAYERS.issubset(new_group)
    assert UNIX_LAYERS.issubset(new_group)

    assert new_group.issuperset(ANY_WINDOWS)
    assert new_group.issuperset(LINUX_LAYERS)
    assert new_group.issuperset(UNIX_LAYERS)

    assert new_group.id == ANY_WINDOWS.id
    assert new_group.id != LINUX_LAYERS.id
    assert new_group.id != UNIX_LAYERS.id
    assert new_group.name == ANY_WINDOWS.name
    assert new_group.name != LINUX_LAYERS.name
    assert new_group.name != UNIX_LAYERS.name
    assert new_group.icon == ANY_WINDOWS.icon
    assert new_group.icon != LINUX_LAYERS.icon
    assert new_group.icon != UNIX_LAYERS.icon

    assert set(new_group.members) != set(ANY_WINDOWS.members)
    assert set(new_group.member_ids) != set(ANY_WINDOWS.member_ids)
    assert set(new_group.members) != set(LINUX_LAYERS.members)
    assert set(new_group.member_ids) != set(LINUX_LAYERS.member_ids)
    assert set(new_group.members) != set(UNIX_LAYERS.members)
    assert set(new_group.member_ids) != set(UNIX_LAYERS.member_ids)

    assert set(new_group.members) == set(ANY_WINDOWS.members).union(
        LINUX_LAYERS.members
    ).union(UNIX_LAYERS.members)
    assert set(new_group.member_ids) == set(ANY_WINDOWS.member_ids).union(
        LINUX_LAYERS.member_ids
    ).union(UNIX_LAYERS.member_ids)


def test_single_intersection():
    new_group = ALL_PLATFORMS.intersection(ANY_WINDOWS)

    assert new_group.member_ids == frozenset(("windows",))

    assert ANY_WINDOWS.issubset(new_group)
    assert not ALL_PLATFORMS.issubset(new_group)
    assert new_group.issuperset(ANY_WINDOWS)
    assert not new_group.issuperset(ALL_PLATFORMS)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != ANY_WINDOWS.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != ANY_WINDOWS.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != ANY_WINDOWS.icon

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)

    assert set(new_group.members) == set(ANY_WINDOWS.members)
    assert set(new_group.member_ids) == set(ANY_WINDOWS.member_ids)


def test_multiple_intersection():
    new_group = ALL_PLATFORMS.intersection(UNIX_WITHOUT_MACOS, BSD_WITHOUT_MACOS)

    assert new_group.member_ids == frozenset((
        "freebsd",
        "midnightbsd",
        "netbsd",
        "openbsd",
        "sunos",
    ))

    assert new_group.issubset(ALL_PLATFORMS)
    assert new_group.issubset(UNIX_WITHOUT_MACOS)
    assert new_group.issubset(BSD_WITHOUT_MACOS)
    assert ALL_PLATFORMS.issuperset(new_group)
    assert UNIX_WITHOUT_MACOS.issuperset(new_group)
    assert BSD_WITHOUT_MACOS.issuperset(new_group)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != UNIX_WITHOUT_MACOS.id
    assert new_group.id != BSD_WITHOUT_MACOS.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != UNIX_WITHOUT_MACOS.name
    assert new_group.name != BSD_WITHOUT_MACOS.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != UNIX_WITHOUT_MACOS.icon
    assert new_group.icon != BSD_WITHOUT_MACOS.icon

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)
    assert set(new_group.members) != set(UNIX_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) != set(UNIX_WITHOUT_MACOS.member_ids)

    assert set(new_group.members) == set(BSD_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) == set(BSD_WITHOUT_MACOS.member_ids)


def test_single_difference():
    new_group = BSD.difference(BSD_WITHOUT_MACOS)

    assert new_group.member_ids == frozenset(("macos",))

    assert not BSD.issubset(new_group)
    assert BSD.issuperset(new_group)
    assert not BSD_WITHOUT_MACOS.issubset(new_group)
    assert not BSD_WITHOUT_MACOS.issuperset(new_group)

    assert not new_group.issuperset(BSD)
    assert not new_group.issuperset(BSD_WITHOUT_MACOS)
    assert new_group.issubset(BSD)
    assert not new_group.issubset(BSD_WITHOUT_MACOS)

    assert new_group.id == BSD.id
    assert new_group.id != BSD_WITHOUT_MACOS.id
    assert new_group.name == BSD.name
    assert new_group.name != BSD_WITHOUT_MACOS.name
    assert new_group.icon == BSD.icon
    assert new_group.icon != BSD_WITHOUT_MACOS.icon

    assert set(new_group.members) != set(BSD.members)
    assert set(new_group.member_ids) != set(BSD.member_ids)
    assert set(new_group.members) != set(BSD_WITHOUT_MACOS.members)
    assert set(new_group.member_ids) != set(BSD_WITHOUT_MACOS.member_ids)

    assert set(new_group.members) == set(BSD.members).difference(
        BSD_WITHOUT_MACOS.members
    )
    assert set(new_group.member_ids) == set(BSD.member_ids).difference(
        BSD_WITHOUT_MACOS.member_ids
    )


def test_multiple_difference():
    new_group = ALL_PLATFORMS.difference(LINUX, UNIX, ALL_CI)

    assert new_group.member_ids == frozenset(("windows",))

    assert not ALL_PLATFORMS.issubset(new_group)
    assert ALL_PLATFORMS.issuperset(new_group)
    assert not LINUX.issubset(new_group)
    assert not LINUX.issuperset(new_group)
    assert not UNIX.issubset(new_group)
    assert not UNIX.issuperset(new_group)

    assert not new_group.issuperset(ALL_PLATFORMS)
    assert not new_group.issuperset(LINUX)
    assert not new_group.issuperset(UNIX)
    assert new_group.issubset(ALL_PLATFORMS)
    assert not new_group.issubset(LINUX)
    assert not new_group.issubset(UNIX)

    assert new_group.id == ALL_PLATFORMS.id
    assert new_group.id != LINUX.id
    assert new_group.id != UNIX.id
    assert new_group.name == ALL_PLATFORMS.name
    assert new_group.name != LINUX.name
    assert new_group.name != UNIX.name
    assert new_group.icon == ALL_PLATFORMS.icon
    assert new_group.icon != LINUX.icon
    assert new_group.icon != UNIX.icon

    assert set(new_group.members) != set(ALL_PLATFORMS.members)
    assert set(new_group.member_ids) != set(ALL_PLATFORMS.member_ids)
    assert set(new_group.members) != set(LINUX.members)
    assert set(new_group.member_ids) != set(LINUX.member_ids)
    assert set(new_group.members) != set(UNIX.members)
    assert set(new_group.member_ids) != set(UNIX.member_ids)

    assert set(new_group.members) == set(ALL_PLATFORMS.members).difference(
        LINUX.members
    ).difference(UNIX.members).difference(ALL_CI.members)
    assert set(new_group.member_ids) == set(ALL_PLATFORMS.member_ids).difference(
        LINUX.member_ids
    ).difference(UNIX.member_ids).difference(ALL_CI.member_ids)


def test_symmetric_difference():
    win_and_bsd = ANY_WINDOWS.union(BSD_WITHOUT_MACOS)
    new_group = win_and_bsd.symmetric_difference(BSD)

    assert new_group.member_ids == frozenset((("macos", "windows")))

    assert not win_and_bsd.issubset(new_group)
    assert not win_and_bsd.issuperset(new_group)
    assert not BSD.issubset(new_group)
    assert not BSD.issuperset(new_group)

    assert not new_group.issuperset(win_and_bsd)
    assert not new_group.issuperset(BSD)
    assert not new_group.issubset(win_and_bsd)
    assert not new_group.issubset(BSD)

    assert new_group.id == win_and_bsd.id
    assert new_group.id != BSD.id
    assert new_group.name == win_and_bsd.name
    assert new_group.name != BSD.name
    assert new_group.icon == win_and_bsd.icon
    assert new_group.icon != BSD.icon

    assert set(new_group.members) != set(BSD.members)
    assert set(new_group.member_ids) != set(BSD.member_ids)
    assert set(new_group.members) != set(win_and_bsd.members)
    assert set(new_group.member_ids) != set(win_and_bsd.member_ids)

    assert set(new_group.members) == set(win_and_bsd.members).symmetric_difference(
        BSD.members
    )
    assert set(new_group.member_ids) == set(
        win_and_bsd.member_ids
    ).symmetric_difference(BSD.member_ids)


def test_copy():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    my_group_copy1 = my_group.copy()
    assert my_group == my_group_copy1
    assert my_group is not my_group_copy1

    my_group_copy2 = my_group.copy(
        id="my_group_copy2", name="My Group Copy 2", icon="🚀"
    )
    assert my_group_copy2 != my_group
    assert my_group_copy2 is not my_group
    assert my_group_copy2 != my_group_copy1
    assert my_group_copy2 is not my_group_copy1
    assert my_group_copy2.id == "my_group_copy2"
    assert my_group_copy2.name == "My Group Copy 2"
    assert my_group_copy2.icon == "🚀"
    assert my_group_copy2.members == my_group.members
    assert my_group_copy2.member_ids == my_group.member_ids
    assert my_group_copy2.members == my_group_copy1.members
    assert my_group_copy2.member_ids == my_group_copy1.member_ids
