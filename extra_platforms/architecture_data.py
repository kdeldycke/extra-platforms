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
"""Architecture definitions and metadata.

.. seealso::
    Architecture variants from `Rust's target-lexicon
    <https://docs.rs/target-lexicon/latest/target_lexicon/enum.Architecture.html#variants>`_.
"""

from __future__ import annotations

from .architecture import Architecture

AARCH64 = Architecture(
    "aarch64",
    "ARM64 (AArch64)",
    "📱",
    "https://en.wikipedia.org/wiki/AArch64",
)

ARM = Architecture(
    "arm",
    "ARM (32-bit)",
    "📱",
    "https://en.wikipedia.org/wiki/ARM_architecture_family",
)

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
)
