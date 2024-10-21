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

import ast
import functools
import inspect
from itertools import combinations
from pathlib import Path
from string import ascii_lowercase, digits

import pytest

import extra_platforms
from extra_platforms import (
    AIX,
    ALL_GROUPS,
    ALL_OS_LABELS,
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
    CURRENT_OS_ID,
    CURRENT_OS_LABEL,
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
    current_os,
    is_aix,
    is_altlinux,
    is_amzn,
    is_android,
    is_arch,
    is_buildroot,
    is_centos,
    is_cloudlinux,
    is_cygwin,
    is_debian,
    is_exherbo,
    is_fedora,
    is_freebsd,
    is_gentoo,
    is_guix,
    is_hurd,
    is_ibm_powerkvm,
    is_kvmibm,
    is_linuxmint,
    is_macos,
    is_mageia,
    is_mandriva,
    is_midnightbsd,
    is_netbsd,
    is_openbsd,
    is_opensuse,
    is_oracle,
    is_parallels,
    is_pidora,
    is_raspbian,
    is_rhel,
    is_rocky,
    is_scientific,
    is_slackware,
    is_sles,
    is_solaris,
    is_sunos,
    is_tuxedo,
    is_ubuntu,
    is_unknown_linux,
    is_windows,
    is_wsl1,
    is_wsl2,
    is_xenserver,
    reduce,
)
from extra_platforms import detection as detection_module
from extra_platforms import groups as groups_module
from extra_platforms import platforms as platforms_module


def test_module_root_declarations():
    def fetch_module_implements(module) -> set[str]:
        """Fetch all methods, classes and constants implemented locally in a module's file."""
        members = set()
        tree = ast.parse(Path(inspect.getfile(module)).read_bytes())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    members.add(target.id)  # type: ignore[attr-defined]
            elif isinstance(node, ast.AnnAssign):
                members.add(node.target.id)  # type: ignore[union-attr]
            elif isinstance(node, ast.FunctionDef):
                members.add(node.name)
            elif isinstance(node, ast.ClassDef):
                members.add(node.name)
        return {m for m in members if not m.startswith("_")}

    detection_members = fetch_module_implements(detection_module)
    groups_members = fetch_module_implements(groups_module)
    platforms_members = fetch_module_implements(platforms_module)
    root_members = fetch_module_implements(extra_platforms)
    # Update root members with auto-generated ``is_<group.id>`` variables.
    root_members.update((f"is_{group.id}" for group in ALL_GROUPS))

    # Check all members are exposed at the module root.
    tree = ast.parse(Path(inspect.getfile(extra_platforms)).read_bytes())
    extra_platforms_members = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if target.id == "__all__":
                    for element in node.value.elts:
                        extra_platforms_members.append(element.value)

    assert detection_members <= set(extra_platforms_members)
    assert groups_members <= set(extra_platforms_members)
    assert platforms_members <= set(extra_platforms_members)

    expected_members = sorted(
        detection_members.union(groups_members)
        .union(platforms_members)
        .union(root_members),
        key=lambda m: (m.lower(), m),
    )
    assert expected_members == extra_platforms_members


def test_mutual_exclusion():
    """Only directly tests OSes on which the test suite is running via GitHub
    actions."""
    if is_ubuntu():
        assert CURRENT_OS_ID == UBUNTU.id
        assert CURRENT_OS_LABEL == UBUNTU.name
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        assert not is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tuxedo()
        # assert not is_ubuntu()
        assert not is_unknown_linux()
        assert not is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()

    if is_macos():
        assert CURRENT_OS_ID == MACOS.id
        assert CURRENT_OS_LABEL == MACOS.name
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        # assert not is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tuxedo()
        assert not is_ubuntu()
        assert not is_unknown_linux()
        assert not is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()

    if is_windows():
        assert CURRENT_OS_ID == WINDOWS.id
        assert CURRENT_OS_LABEL == WINDOWS.name
        assert not is_aix()
        assert not is_altlinux()
        assert not is_amzn()
        assert not is_android()
        assert not is_arch()
        assert not is_buildroot()
        assert not is_centos()
        assert not is_cloudlinux()
        assert not is_cygwin()
        assert not is_debian()
        assert not is_exherbo()
        assert not is_fedora()
        assert not is_freebsd()
        assert not is_gentoo()
        assert not is_guix()
        assert not is_hurd()
        assert not is_ibm_powerkvm()
        assert not is_kvmibm()
        assert not is_linuxmint()
        assert not is_macos()
        assert not is_mageia()
        assert not is_mandriva()
        assert not is_midnightbsd()
        assert not is_netbsd()
        assert not is_openbsd()
        assert not is_opensuse()
        assert not is_oracle()
        assert not is_parallels()
        assert not is_pidora()
        assert not is_raspbian()
        assert not is_rhel()
        assert not is_rocky()
        assert not is_scientific()
        assert not is_slackware()
        assert not is_sles()
        assert not is_solaris()
        assert not is_sunos()
        assert not is_tuxedo()
        assert not is_ubuntu()
        assert not is_unknown_linux()
        # assert not is_windows()
        assert not is_wsl1()
        assert not is_wsl2()
        assert not is_xenserver()


def test_platform_definitions():
    for platform in ALL_PLATFORMS.platforms:
        # ID.
        assert platform.id
        assert platform.id.isascii()
        assert platform.id[0] in ascii_lowercase
        assert platform.id[-1] in ascii_lowercase + digits
        assert set(platform.id).issubset(ascii_lowercase + digits + "_")
        assert platform.id.islower()
        # Platforms are not allowed to starts with all_ or any_, which is reserved
        # for groups. Use unknown_ prefix instead.
        assert not platform.id.startswith(("all_", "any_"))

        # Name.
        assert platform.name
        assert platform.name.isascii()
        assert platform.name.isprintable()
        assert platform.name in ALL_OS_LABELS

        # Icon.
        assert platform.icon
        assert 2 >= len(platform.icon) >= 1

        # Identification function.
        check_func_id = f"is_{platform.id}"
        assert check_func_id in globals()
        check_func = globals()[check_func_id]
        assert isinstance(check_func, functools._lru_cache_wrapper)
        assert isinstance(check_func(), bool)
        assert check_func() == platform.current

        # Info.
        assert platform.info()
        for k, v in platform.info().items():
            assert set(k).issubset(ascii_lowercase + "_")
            if v is not None:
                assert isinstance(v, (str, bool, dict))
                if isinstance(v, str):
                    assert v
                elif isinstance(v, dict):
                    assert v
                    for k1, v1 in v.items():
                        assert set(k1).issubset(ascii_lowercase + "_")
                        if v1 is not None:
                            assert v1
        assert platform.info()["id"] == platform.id


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


def test_code_sorting():
    """Implementation must have all its methods and objects sorted."""
    heuristic_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(detection_module)).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("is_"):
            func_id = node.name
            assert func_id.islower()
            heuristic_instance_ids.append(func_id)

    platform_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(platforms_module)).read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and node.value.func.id == "Platform"
        ):
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            platform_instance_ids.append(instance_id)

    group_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(groups_module)).read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and node.value.func.id == "Group"
        ):
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            group_instance_ids.append(instance_id)

    # Check there is no extra "is_" function.
    assert {f"is_{p.id}" for p in ALL_PLATFORMS.platforms} == set(
        heuristic_instance_ids
    )

    assert heuristic_instance_ids == sorted(heuristic_instance_ids)
    assert platform_instance_ids == sorted(platform_instance_ids)
    # XXX Group order is logical, not alphabetical.
    # assert group_instance_ids == sorted(group_instance_ids)


def test_unique_ids():
    """Platform and group IDs must be unique."""
    all_platform_ids = [p.id for p in ALL_PLATFORMS]

    # Platforms are expected to be sorted by ID.
    assert sorted(all_platform_ids) == all_platform_ids
    assert len(set(all_platform_ids)) == len(all_platform_ids)

    assert len(all_platform_ids) == len(ALL_PLATFORMS)
    assert len(all_platform_ids) == len(ALL_PLATFORMS.platform_ids)

    all_group_ids = {g.id for g in ALL_GROUPS}
    assert len(all_group_ids) == len(ALL_GROUPS)

    assert all_group_ids.isdisjoint(all_platform_ids)


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


def test_current_os_func():
    # Function.
    current_platform = current_os()
    assert current_platform in ALL_PLATFORMS.platforms
    # Constants.
    assert current_platform.id == CURRENT_OS_ID
    assert current_platform.name == CURRENT_OS_LABEL


def test_os_labels():
    assert len(ALL_OS_LABELS) == len(ALL_PLATFORMS)
