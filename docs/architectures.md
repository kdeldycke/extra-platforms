# {octicon}`cpu` Architectures

## Recognized architectures

<!-- architecture-table-start -->

| Icon | Name | Architecture ID |
|:----:|:------|:-------------|
| 🔋 | [ARM64 (AArch64)](https://en.wikipedia.org/wiki/AArch64) | `aarch64` |
| 📱 | [ARM (32-bit)](https://en.wikipedia.org/wiki/ARM_architecture_family) | `arm` |
| 📱 | [ARMv6 (little-endian)](https://en.wikipedia.org/wiki/ARM11) | `armv6l` |
| 📱 | [ARMv7 (little-endian)](https://en.wikipedia.org/wiki/ARM_Cortex-A) | `armv7l` |
| 📱 | [ARMv8 (32-bit, little-endian)](https://en.wikipedia.org/wiki/ARM_Cortex-A) | `armv8l` |
| 🔲 | [Intel 80386 (i386)](https://en.wikipedia.org/wiki/Intel_80386) | `i386` |
| 🔲 | [Intel Pentium (i586)](https://en.wikipedia.org/wiki/P5_(microarchitecture)) | `i586` |
| 🔲 | [Intel Pentium Pro (i686)](https://en.wikipedia.org/wiki/P6_(microarchitecture)) | `i686` |
| 🐉 | [LoongArch (64-bit)](https://en.wikipedia.org/wiki/Loongson#LoongArch) | `loongarch64` |
| 🔧 | [MIPS (32-bit, big-endian)](https://en.wikipedia.org/wiki/MIPS_architecture) | `mips` |
| 🔧 | [MIPS64 (big-endian)](https://en.wikipedia.org/wiki/MIPS_architecture) | `mips64` |
| 🔧 | [MIPS64 (little-endian)](https://en.wikipedia.org/wiki/MIPS_architecture) | `mips64el` |
| 🔧 | [MIPS (32-bit, little-endian)](https://en.wikipedia.org/wiki/MIPS_architecture) | `mipsel` |
| ⚡ | [PowerPC (32-bit)](https://en.wikipedia.org/wiki/PowerPC) | `ppc` |
| ⚡ | [PowerPC 64-bit (big-endian)](https://en.wikipedia.org/wiki/Ppc64) | `ppc64` |
| ⚡ | [PowerPC 64-bit (little-endian)](https://en.wikipedia.org/wiki/Ppc64) | `ppc64le` |
| 🌱 | [RISC-V (32-bit)](https://en.wikipedia.org/wiki/RISC-V) | `riscv32` |
| 🌱 | [RISC-V (64-bit)](https://en.wikipedia.org/wiki/RISC-V) | `riscv64` |
| 🏢 | [IBM z/Architecture (s390x)](https://en.wikipedia.org/wiki/Z/Architecture) | `s390x` |
| ☀️ | [SPARC (32-bit)](https://en.wikipedia.org/wiki/SPARC) | `sparc` |
| ☀️ | [SPARC (64-bit)](https://en.wikipedia.org/wiki/SPARC) | `sparc64` |
| ❓ | [Unknown architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture) | `unknown_architecture` |
| 🌐 | [WebAssembly (32-bit)](https://en.wikipedia.org/wiki/WebAssembly) | `wasm32` |
| 🌐 | [WebAssembly (64-bit)](https://en.wikipedia.org/wiki/WebAssembly) | `wasm64` |
| 💻 | [x86-64 (AMD64)](https://en.wikipedia.org/wiki/X86-64) | `x86_64` |

<!-- architecture-table-end -->

## Groups of architectures

All recognized architectures are grouped in non-overlapping families.

Here is their relationship visualized as a Sankey diagram:

<!-- architecture-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

ALL_ARCHITECTURES,aarch64,1
ALL_ARCHITECTURES,arm,1
ALL_ARCHITECTURES,armv6l,1
ALL_ARCHITECTURES,armv7l,1
ALL_ARCHITECTURES,armv8l,1
ALL_ARCHITECTURES,i386,1
ALL_ARCHITECTURES,i586,1
ALL_ARCHITECTURES,i686,1
ALL_ARCHITECTURES,loongarch64,1
ALL_ARCHITECTURES,mips,1
ALL_ARCHITECTURES,mips64,1
ALL_ARCHITECTURES,mips64el,1
ALL_ARCHITECTURES,mipsel,1
ALL_ARCHITECTURES,ppc,1
ALL_ARCHITECTURES,ppc64,1
ALL_ARCHITECTURES,ppc64le,1
ALL_ARCHITECTURES,riscv32,1
ALL_ARCHITECTURES,riscv64,1
ALL_ARCHITECTURES,s390x,1
ALL_ARCHITECTURES,sparc,1
ALL_ARCHITECTURES,sparc64,1
ALL_ARCHITECTURES,unknown_architecture,1
ALL_ARCHITECTURES,wasm32,1
ALL_ARCHITECTURES,wasm64,1
ALL_ARCHITECTURES,x86_64,1
```

<!-- architecture-sankey-end -->

## `extra_platforms.architecture` API

```{eval-rst}
.. autoclasstree:: extra_platforms.architecture
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.architecture
   :members:
   :undoc-members:
   :show-inheritance:
```

## `extra_platforms.architecture_data` API

```{eval-rst}
.. autoclasstree:: extra_platforms.architecture_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.architecture_data
   :members:
   :undoc-members:
   :show-inheritance:
```
