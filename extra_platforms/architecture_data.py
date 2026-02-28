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
"""Architecture definitions and metadata.

.. hint::
    Architecture's canonical IDs are inspired by those `used in the auditwheel
    <https://github.com/pypa/auditwheel/blob/main/src/auditwheel/architecture.py>`_
    project to encode the `manylinux policies
    <https://github.com/pypa/auditwheel/blob/6.6.0/src/auditwheel/policy/manylinux-policy.json>`_.

.. seealso::
    Architecture variants from `Rust's target-lexicon
    <https://docs.rs/target-lexicon/latest/target_lexicon/enum.Architecture.html#variants>`_.

.. todo::
    Add mapping of architecture to manylinux Python targets? As per:

    - https://github.com/astral-sh/uv/blob/main/crates/uv-platform-tags/src/platform.rs
    - https://github.com/pypa/manylinux
"""

from __future__ import annotations

from .trait import Architecture

AARCH64 = Architecture(
    "aarch64",
    "ARM64 (AArch64)",
    "📱",
    "https://en.wikipedia.org/wiki/AArch64",
    aliases=frozenset({"arm64"}),
)
"""
.. hint::
    Although ``aarch64`` is the canonical ID for this architecture, some
    platforms may use the alias ``arm64`` instead (e.g., macOS on Apple Silicon).
"""

ARM = Architecture(
    "arm",
    "ARM (32-bit)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM_architecture_family",
)

ARMV5TEL = Architecture(
    "armv5tel",
    "ARMv5TE (little-endian)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM11",
)
"""
.. hint::
    ARMv5TE includes Thumb and DSP extensions. This architecture is found on
    older ARM devices and may appear in embedded systems or legacy platforms.
"""

ARMV6L = Architecture(
    "armv6l",
    "ARMv6 (little-endian)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM11",
)

ARMV7L = Architecture(
    "armv7l",
    "ARMv7 (little-endian)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM_Cortex-A",
    aliases=frozenset({"armhf", "armv7"}),
)

ARMV8L = Architecture(
    "armv8l",
    "ARMv8 (32-bit, little-endian)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM_Cortex-A",
)

I386 = Architecture(
    "i386",
    "Intel 80386 (i386)",
    "𝗶",
    "https://en.wikipedia.org/wiki/Intel_80386",
    aliases=frozenset({"i486"}),
)

I586 = Architecture(
    "i586",
    "Intel Pentium (i586)",
    "𝗶",
    "https://en.wikipedia.org/wiki/P5_(microarchitecture)",
)

I686 = Architecture(
    "i686",
    "Intel Pentium Pro (i686)",
    "𝗶",
    "https://en.wikipedia.org/wiki/P6_(microarchitecture)",
)

LOONGARCH64 = Architecture(
    "loongarch64",
    "LoongArch (64-bit)",
    "🐉",
    "https://en.wikipedia.org/wiki/Loongson#LoongArch",
)

MIPS = Architecture(
    "mips",
    "MIPS (32-bit, big-endian)",
    "🔲",
    "https://en.wikipedia.org/wiki/MIPS_architecture",
)

MIPS64 = Architecture(
    "mips64",
    "MIPS64 (big-endian)",
    "🔲",
    "https://en.wikipedia.org/wiki/MIPS_architecture",
)

MIPS64EL = Architecture(
    "mips64el",
    "MIPS64 (little-endian)",
    "🔲",
    "https://en.wikipedia.org/wiki/MIPS_architecture",
)

MIPSEL = Architecture(
    "mipsel",
    "MIPS (32-bit, little-endian)",
    "🔲",
    "https://en.wikipedia.org/wiki/MIPS_architecture",
)

PPC = Architecture(
    "ppc",
    "PowerPC (32-bit)",
    "⚡",
    "https://en.wikipedia.org/wiki/PowerPC",
)

PPC64 = Architecture(
    "ppc64",
    "PowerPC 64-bit (big-endian)",
    "⚡",
    "https://en.wikipedia.org/wiki/Ppc64",
)

PPC64LE = Architecture(
    "ppc64le",
    "PowerPC 64-bit (little-endian)",
    "⚡",
    "https://en.wikipedia.org/wiki/Ppc64",
    aliases=frozenset({"powerpc64le", "ppc64el"}),
)

RISCV32 = Architecture(
    "riscv32",
    "RISC-V (32-bit)",
    "Ⅴ",
    "https://en.wikipedia.org/wiki/RISC-V",
)

RISCV64 = Architecture(
    "riscv64",
    "RISC-V (64-bit)",
    "Ⅴ",
    "https://en.wikipedia.org/wiki/RISC-V",
)

S390X = Architecture(
    "s390x",
    "IBM z/Architecture (s390x)",
    "🏢",
    "https://en.wikipedia.org/wiki/Z/Architecture",
)

SPARC = Architecture(
    "sparc",
    "SPARC (32-bit)",
    "☀️",
    "https://en.wikipedia.org/wiki/SPARC",
)

SPARC64 = Architecture(
    "sparc64",
    "SPARC (64-bit)",
    "☀️",
    "https://en.wikipedia.org/wiki/SPARC",
)

UNKNOWN_ARCHITECTURE = Architecture(
    "unknown_architecture",
    "Unknown architecture",
    "❓",
    "https://en.wikipedia.org/wiki/Instruction_set_architecture",
)

WASM32 = Architecture(
    "wasm32",
    "WebAssembly (32-bit)",
    "🌐",
    "https://en.wikipedia.org/wiki/WebAssembly",
)

WASM64 = Architecture(
    "wasm64",
    "WebAssembly (64-bit)",
    "🌐",
    "https://en.wikipedia.org/wiki/WebAssembly",
)

X86_64 = Architecture(
    "x86_64",
    "x86-64 (AMD64)",
    "🖥️",
    "https://en.wikipedia.org/wiki/X86-64",
    aliases=frozenset({"amd64"}),
)
"""
.. hint::
    Although ``x86_64`` is the canonical ID for this architecture, some
    platforms may use the alias ``amd64`` instead (e.g., Windows on x86-64).
"""
