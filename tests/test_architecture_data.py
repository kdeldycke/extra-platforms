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

from extra_platforms import (  # type: ignore[attr-defined]
    ALL_ARCHITECTURES,
    ALL_ARM,
    ALL_MIPS,
    ALL_SPARC,
    ARCH_32_BIT,
    ARCH_64_BIT,
    BIG_ENDIAN,
    IBM_MAINFRAME,
    LITTLE_ENDIAN,
    LOONGARCH,
    POWERPC,
    RISCV,
    UNKNOWN_ARCHITECTURE,
    WEBASSEMBLY,
    X86,
    current_architecture,
    is_aarch64,
    is_any_architecture,
    is_any_trait,
    is_arch_32_bit,
    is_arch_64_bit,
    is_arm,
    is_big_endian,
    is_armv6l,
    is_armv7l,
    is_armv8l,
    is_i386,
    is_i586,
    is_i686,
    is_little_endian,
    is_loongarch64,
    is_mips,
    is_mips64,
    is_mips64el,
    is_mipsel,
    is_ppc,
    is_ppc64,
    is_ppc64le,
    is_riscv32,
    is_riscv64,
    is_s390x,
    is_sparc,
    is_sparc64,
    is_unknown_architecture,
    is_wasm32,
    is_wasm64,
    is_x86_64,
)


def test_architecture_detection():
    # We always expect to detect an architecture.
    assert is_any_trait()
    assert is_any_architecture()
    assert not is_unknown_architecture()
    assert current_architecture() is not UNKNOWN_ARCHITECTURE

    # Architecture bitness.
    assert is_arch_32_bit() or is_arch_64_bit()
    assert is_little_endian() or is_big_endian()

    if is_x86_64():
        assert not is_i386()
        assert not is_i586()
        assert not is_i686()
        assert is_x86_64()
        assert not is_arm()
        assert not is_armv6l()
        assert not is_armv7l()
        assert not is_armv8l()
        assert not is_aarch64()
        assert not is_mips()
        assert not is_mipsel()
        assert not is_mips64()
        assert not is_mips64el()
        assert not is_ppc()
        assert not is_ppc64()
        assert not is_ppc64le()
        assert not is_riscv32()
        assert not is_riscv64()
        assert not is_sparc()
        assert not is_sparc64()
        assert not is_s390x()
        assert not is_loongarch64()
        assert not is_wasm32()
        assert not is_wasm64()

    if is_aarch64():
        assert not is_i386()
        assert not is_i586()
        assert not is_i686()
        assert not is_x86_64()
        assert not is_arm()
        assert not is_armv6l()
        assert not is_armv7l()
        assert not is_armv8l()
        assert is_aarch64()
        assert not is_mips()
        assert not is_mipsel()
        assert not is_mips64()
        assert not is_mips64el()
        assert not is_ppc()
        assert not is_ppc64()
        assert not is_ppc64le()
        assert not is_riscv32()
        assert not is_riscv64()
        assert not is_sparc()
        assert not is_sparc64()
        assert not is_s390x()
        assert not is_loongarch64()
        assert not is_wasm32()
        assert not is_wasm64()


def test_architecture_logical_grouping():
    # All architectures are divided into families.
    assert ALL_ARCHITECTURES.fullyintersects(
        ALL_ARM
        | ALL_MIPS
        | ALL_SPARC
        | IBM_MAINFRAME
        | LOONGARCH
        | POWERPC
        | RISCV
        | WEBASSEMBLY
        | X86
    )
    assert not ALL_ARCHITECTURES.canonical
    assert ALL_ARM.canonical
    assert ALL_MIPS.canonical
    assert ALL_SPARC.canonical
    assert IBM_MAINFRAME.canonical
    assert LOONGARCH.canonical
    assert POWERPC.canonical
    assert RISCV.canonical
    assert WEBASSEMBLY.canonical
    assert X86.canonical

    # All architectures are divided by bitness.
    assert ARCH_32_BIT.isdisjoint(ARCH_64_BIT)
    assert ARCH_64_BIT.isdisjoint(ARCH_32_BIT)
    assert ALL_ARCHITECTURES.fullyintersects(ARCH_32_BIT | ARCH_64_BIT)

    # All architectures are divided by endianness.
    assert BIG_ENDIAN.isdisjoint(LITTLE_ENDIAN)
    assert LITTLE_ENDIAN.isdisjoint(BIG_ENDIAN)
    assert ALL_ARCHITECTURES.fullyintersects(BIG_ENDIAN | LITTLE_ENDIAN)
