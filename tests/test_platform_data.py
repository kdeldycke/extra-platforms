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
