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

from itertools import combinations
from string import ascii_lowercase, digits

import pytest

from extra_platforms import (
    AIX,
    ALL_GROUPS,
    ALL_PLATFORMS,
    ALTLINUX,
    AMZN,
    ANDROID,
    ANY_WINDOWS,
    ARCH,
    BSD,
    BSD_WITHOUT_MACOS,
    BUILDROOT,
    CENTOS,
    CLOUDLINUX,
    CYGWIN,
    DEBIAN,
    EXHERBO,
    EXTRA_GROUPS,
    FEDORA,
    FREEBSD,
    GENTOO,
    GUIX,
    HURD,
    IBM_POWERKVM,
    KVMIBM,
    LINUX,
    LINUX_LAYERS,
    LINUXMINT,
    MACOS,
    MAGEIA,
    MANDRIVA,
    MIDNIGHTBSD,
    NETBSD,
    NON_OVERLAPPING_GROUPS,
    OPENBSD,
    OPENSUSE,
    ORACLE,
    OTHER_UNIX,
    PARALLELS,
    PIDORA,
    RASPBIAN,
    RHEL,
    ROCKY,
    SCIENTIFIC,
    SLACKWARE,
    SLES,
    SOLARIS,
    SUNOS,
    SYSTEM_V,
    TUXEDO,
    UBUNTU,
    UNIX,
    UNIX_LAYERS,
    UNIX_WITHOUT_MACOS,
    UNKNOWN_LINUX,
    WINDOWS,
    WSL1,
    WSL2,
    XENSERVER,
    Group,
    reduce,
)
from extra_platforms import groups as groups_module


def test_platform_deduplication():
    my_group = Group("my_group", "My Group", "✅", (AIX, AIX))
    assert len(my_group) == 1
    assert len(my_group.platforms) == 1
    assert len(my_group.platform_ids) == 1

    assert my_group.platforms == (AIX,)
    assert my_group.platform_ids == frozenset({"aix"})


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

    assert set(new_group.platforms) == set(ANY_WINDOWS.platforms) | set(
        LINUX_LAYERS.platforms
    )
    assert set(new_group.platform_ids) == set(ANY_WINDOWS.platform_ids) | set(
        LINUX_LAYERS.platform_ids
    )


def test_multiple_union():
    new_group = ANY_WINDOWS.union(LINUX_LAYERS, UNIX_LAYERS)

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

    assert set(new_group.platforms) == set(ANY_WINDOWS.platforms) | set(
        LINUX_LAYERS.platforms
    ) | set(UNIX_LAYERS.platforms)
    assert set(new_group.platform_ids) == set(ANY_WINDOWS.platform_ids) | set(
        LINUX_LAYERS.platform_ids
    ) | set(UNIX_LAYERS.platform_ids)


def test_group_definitions():
    for group in ALL_GROUPS:
        # ID.
        assert group.id
        assert group.id.isascii()
        assert group.id[0] in ascii_lowercase
        assert group.id[-1] in ascii_lowercase + digits
        assert set(group.id).issubset(ascii_lowercase + digits + "_")
        assert group.id.islower()
        # Only the group referencing all platforms is allowed to starts with "all_"
        # prefix.
        assert group.id == "all_platforms" or not group.id.startswith("all_")

        # Name.
        assert group.name
        assert group.name.isascii()
        assert group.name.isprintable()

        # Icon.
        assert group.icon
        assert 2 >= len(group.icon) >= 1


def test_group_constants():
    """Group constants and IDs must be aligned."""
    for group in ALL_GROUPS:
        group_constant = group.id.upper()
        assert group_constant in groups_module.__dict__
        assert getattr(groups_module, group_constant) is group


def test_groups_content():
    for groups in (NON_OVERLAPPING_GROUPS, EXTRA_GROUPS, ALL_GROUPS):
        assert isinstance(groups, frozenset)
        for group in groups:
            assert isinstance(group, Group)

            assert len(group) > 0
            assert len(group.platforms) == len(group.platform_ids)
            assert group.platform_ids.issubset(ALL_PLATFORMS.platform_ids)

            # Check general subset properties.
            assert group.issubset(ALL_PLATFORMS)
            assert ALL_PLATFORMS.issuperset(group)

            # Each group is both a subset and a superset of itself.
            assert group.issubset(group)
            assert group.issuperset(group)
            assert group.issubset(group.platforms)
            assert group.issuperset(group.platforms)

            # Test against empty iterables.
            assert group.issuperset(())
            assert group.issuperset([])
            assert group.issuperset({})
            assert group.issuperset(set())
            assert group.issuperset(frozenset())
            assert not group.issubset(())
            assert not group.issubset([])
            assert not group.issubset({})
            assert not group.issubset(set())
            assert not group.issubset(frozenset())

            for platform in group.platforms:
                assert platform in group
                assert platform in ALL_PLATFORMS
                assert platform.id in group.platform_ids
                assert group.issuperset([platform])
                if len(group) == 1:
                    assert group.issubset([platform])
                else:
                    assert not group.issubset([platform])

            # A group cannot be disjoint from itself.
            assert not group.isdisjoint(group)
            assert not group.isdisjoint(group.platforms)
            assert group.fullyintersects(group)
            assert group.fullyintersects(group.platforms)


def test_logical_grouping():
    """Test logical grouping of platforms."""
    for group in BSD, LINUX, LINUX_LAYERS, SYSTEM_V, UNIX_LAYERS, OTHER_UNIX:
        assert group.issubset(UNIX)
        assert UNIX.issuperset(group)

    assert UNIX_WITHOUT_MACOS.issubset(UNIX)
    assert UNIX.issuperset(UNIX_WITHOUT_MACOS)

    assert BSD_WITHOUT_MACOS.issubset(UNIX)
    assert BSD_WITHOUT_MACOS.issubset(BSD)
    assert UNIX.issuperset(BSD_WITHOUT_MACOS)
    assert BSD.issuperset(BSD_WITHOUT_MACOS)

    # All platforms are divided into Windows and Unix at the highest level.
    assert {p.id for p in ALL_PLATFORMS} == ANY_WINDOWS.platform_ids | UNIX.platform_ids

    # All UNIX platforms are divided into BSD, Linux, and Unix families.
    assert UNIX.platform_ids == (
        BSD.platform_ids
        | LINUX.platform_ids
        | LINUX_LAYERS.platform_ids
        | SYSTEM_V.platform_ids
        | UNIX_LAYERS.platform_ids
        | OTHER_UNIX.platform_ids
    )


def test_group_no_missing_platform():
    """Check all platform are attached to at least one group."""
    grouped_platforms = set()
    for group in ALL_GROUPS:
        grouped_platforms |= group.platform_ids
    assert grouped_platforms == ALL_PLATFORMS.platform_ids


def test_non_overlapping_groups():
    """Check non-overlapping groups are mutually exclusive."""
    for combination in combinations(NON_OVERLAPPING_GROUPS, 2):
        group1, group2 = combination
        assert group1.isdisjoint(group2)
        assert group2.isdisjoint(group1)


def test_overlapping_groups():
    """Check all extra groups overlaps with at least one non-overlapping."""
    for extra_group in EXTRA_GROUPS:
        overlap = False
        for group in NON_OVERLAPPING_GROUPS:
            if not extra_group.isdisjoint(group):
                overlap = True
                break
        assert overlap is True


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], set()),
        ((), set()),
        (set(), set()),
        ([AIX], {AIX}),
        ([AIX, AIX], {AIX}),
        ([UNIX], {UNIX}),
        ([UNIX, UNIX], {UNIX}),
        ([UNIX, AIX], {UNIX}),
        ([WINDOWS], {ANY_WINDOWS}),
        ([ALL_PLATFORMS, WINDOWS], {ALL_PLATFORMS}),
        ([UNIX, WINDOWS], {ALL_PLATFORMS}),
        ([UNIX, ANY_WINDOWS], {ALL_PLATFORMS}),
        ([BSD_WITHOUT_MACOS, UNIX], {UNIX}),
        ([BSD_WITHOUT_MACOS, MACOS], {BSD}),
        (
            [
                AIX,
                ALTLINUX,
                AMZN,
                ANDROID,
                ARCH,
                BUILDROOT,
                CENTOS,
                CLOUDLINUX,
                CYGWIN,
                DEBIAN,
                EXHERBO,
                FEDORA,
                FREEBSD,
                GENTOO,
                GUIX,
                HURD,
                IBM_POWERKVM,
                KVMIBM,
                LINUXMINT,
                MACOS,
                MAGEIA,
                MANDRIVA,
                MIDNIGHTBSD,
                NETBSD,
                OPENBSD,
                OPENSUSE,
                ORACLE,
                PARALLELS,
                PIDORA,
                RASPBIAN,
                RHEL,
                ROCKY,
                SCIENTIFIC,
                SLACKWARE,
                SLES,
                SOLARIS,
                SUNOS,
                TUXEDO,
                UBUNTU,
                UNKNOWN_LINUX,
                WINDOWS,
                WSL1,
                WSL2,
                XENSERVER,
            ],
            {ALL_PLATFORMS},
        ),
    ],
)
def test_reduction(items, expected):
    assert reduce(items) == expected
