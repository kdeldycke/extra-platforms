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
"""Test all architecture definitions, detection and architecture-specific groups."""

from __future__ import annotations

from extra_platforms import (
    ALL_ARCHITECTURES,
    ARCH_32_BIT,
    ARCH_64_BIT,
    BIG_ENDIAN,
    LITTLE_ENDIAN,
    UNKNOWN_ARCHITECTURE,
    current_architecture,
    is_any_architecture,
    is_any_trait,
    is_arch_32_bit,
    is_arch_64_bit,
    is_big_endian,
    is_little_endian,
    is_unknown_architecture,
)


def test_architecture_detection():
    # We always expect to detect an architecture.
    assert is_any_trait()
    assert is_any_architecture()
    assert not is_unknown_architecture()
    assert current_architecture() is not UNKNOWN_ARCHITECTURE

    # An architecture has exactly one bitness and one endianness.
    assert is_arch_32_bit() or is_arch_64_bit()
    assert is_little_endian() or is_big_endian()


def test_architecture_mutual_exclusion():
    """Exactly one architecture matches the current environment."""
    matching = {arch for arch in ALL_ARCHITECTURES if arch.current}
    assert len(matching) == 1


def test_architecture_logical_grouping():
    """Check partitions specific to architectures.

    Family partitions and canonical flags are enforced generically in
    ``test_trait_data.py`` and ``test_group_data.py``. Bitness and endianness
    are non-canonical groups, so their partition of all architectures is only
    checked here.
    """
    # All architectures are divided by bitness.
    assert ARCH_32_BIT.isdisjoint(ARCH_64_BIT)
    assert ARCH_64_BIT.isdisjoint(ARCH_32_BIT)
    assert ALL_ARCHITECTURES.fullyintersects(ARCH_32_BIT | ARCH_64_BIT)

    # All architectures are divided by endianness.
    assert BIG_ENDIAN.isdisjoint(LITTLE_ENDIAN)
    assert LITTLE_ENDIAN.isdisjoint(BIG_ENDIAN)
    assert ALL_ARCHITECTURES.fullyintersects(BIG_ENDIAN | LITTLE_ENDIAN)
