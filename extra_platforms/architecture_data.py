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

.. todo::
    Add mapping of architecture to manylinux Python targets? As per:
    - https://github.com/zaniebot/uv/blob/6e9a42e31b19f56abb69352c9e5b3b17a013ad45/crates/uv-platform-tags/src/platform.rs#L182-L199
    - https://github.com/pypa/manylinux
"""

from __future__ import annotations

from .trait import Architecture

AARCH64 = Architecture(
    "aarch64",
    "ARM64 (AArch64)",
    "📱",
    "https://en.wikipedia.org/wiki/AArch64",
)
"""
.. warning::
    Although ``aarch64`` is the canonical ID for this architecture, some
    platforms may use the alias ``arm64`` instead (e.g., macOS on Apple Silicon).

.. todo::
    Consider adding ``arm64`` as an alias in the future.
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
.. note::
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
)
"""
.. note::
    This architecture is commonly referred to as ``armhf`` (ARM hard-float) in
    Debian-based distributions, or simply ``armv7`` in other contexts.
"""

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
"""
.. todo::
    Alias this to ``i486``.
"""

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
"""
.. note::
    Also known as ``powerpc64le`` or ``ppc64el`` in some distributions.
"""

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
"""
.. warning::
    Although ``x86_64`` is the canonical ID for this architecture, some
    platforms may use the alias ``amd64`` instead (e.g., Windows on x86-64).

.. todo::
    Consider adding ``amd64`` as an alias in the future.
"""
