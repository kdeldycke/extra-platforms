# {octicon}`cpu` Architectures

Each architecture represents a CPU instruction set, and is associated with:

- a unique architecture ID
- a human-readable name
- an icon (emoji / unicode character)
- a [detection function](detection.md)
- various metadata in its `info()` method

Each architecture is materialized by an [`Architecture` object](#extra_platforms.architecture.Architecture), from which you can access various metadata:

```pycon
>>> from extra_platforms import X86_64
>>> X86_64
Architecture(id='x86_64', name='x86-64 (AMD64)')
>>> X86_64.id
'x86_64'
>>> X86_64.current
True
>>> X86_64.info()
{'id': 'x86_64', 'name': 'x86-64 (AMD64)', 'icon': '💻', 'url': 'https://en.wikipedia.org/wiki/X86-64', 'current': True, 'machine': None, 'processor': None}
```

To check if the current architecture matches a specific architecture, use the corresponding [detection function](detection.md):

```pycon
>>> from extra_platforms import is_x86_64
>>> is_x86_64()
True
```

The current architecture can be obtained via the `current_architecture()` function:

```pycon
>>> from extra_platforms import current_architecture
>>> current_architecture()
Architecture(id='x86_64', name='x86-64 (AMD64)')
```

## Recognized architectures

<!-- architecture-table-start -->

|  Icon  | Name                                                                               | ID                     | Detection function                                                                            |
| :--: | :--------------------------------------------------------------------------------- | :--------------------- | :-------------------------------------------------------------------------------------------- |
|   📱   | [ARM64 (AArch64)](https://en.wikipedia.org/wiki/AArch64)                           | `aarch64`              | [`is_aarch64()`](detection.md#extra_platforms.detection.is_aarch64)                           |
|   📱   | [ARM (32-bit)](https://en.wikipedia.org/wiki/ARM_architecture_family)              | `arm`                  | [`is_arm()`](detection.md#extra_platforms.detection.is_arm)                                   |
|   📱   | [ARMv6 (little-endian)](https://en.wikipedia.org/wiki/ARM11)                       | `armv6l`               | [`is_armv6l()`](detection.md#extra_platforms.detection.is_armv6l)                             |
|   📱   | [ARMv7 (little-endian)](https://en.wikipedia.org/wiki/ARM_Cortex-A)                | `armv7l`               | [`is_armv7l()`](detection.md#extra_platforms.detection.is_armv7l)                             |
|   📱   | [ARMv8 (32-bit, little-endian)](https://en.wikipedia.org/wiki/ARM_Cortex-A)        | `armv8l`               | [`is_armv8l()`](detection.md#extra_platforms.detection.is_armv8l)                             |
|   𝗶    | [Intel 80386 (i386)](https://en.wikipedia.org/wiki/Intel_80386)                    | `i386`                 | [`is_i386()`](detection.md#extra_platforms.detection.is_i386)                                 |
|   𝗶    | [Intel Pentium (i586)](https://en.wikipedia.org/wiki/P5_(microarchitecture))       | `i586`                 | [`is_i586()`](detection.md#extra_platforms.detection.is_i586)                                 |
|   𝗶    | [Intel Pentium Pro (i686)](https://en.wikipedia.org/wiki/P6_(microarchitecture))   | `i686`                 | [`is_i686()`](detection.md#extra_platforms.detection.is_i686)                                 |
|   🐉   | [LoongArch (64-bit)](https://en.wikipedia.org/wiki/Loongson#LoongArch)             | `loongarch64`          | [`is_loongarch64()`](detection.md#extra_platforms.detection.is_loongarch64)                   |
|   🔲   | [MIPS (32-bit, big-endian)](https://en.wikipedia.org/wiki/MIPS_architecture)       | `mips`                 | [`is_mips()`](detection.md#extra_platforms.detection.is_mips)                                 |
|   🔲   | [MIPS64 (big-endian)](https://en.wikipedia.org/wiki/MIPS_architecture)             | `mips64`               | [`is_mips64()`](detection.md#extra_platforms.detection.is_mips64)                             |
|   🔲   | [MIPS64 (little-endian)](https://en.wikipedia.org/wiki/MIPS_architecture)          | `mips64el`             | [`is_mips64el()`](detection.md#extra_platforms.detection.is_mips64el)                         |
|   🔲   | [MIPS (32-bit, little-endian)](https://en.wikipedia.org/wiki/MIPS_architecture)    | `mipsel`               | [`is_mipsel()`](detection.md#extra_platforms.detection.is_mipsel)                             |
|   ⚡   | [PowerPC (32-bit)](https://en.wikipedia.org/wiki/PowerPC)                          | `ppc`                  | [`is_ppc()`](detection.md#extra_platforms.detection.is_ppc)                                   |
|   ⚡   | [PowerPC 64-bit (big-endian)](https://en.wikipedia.org/wiki/Ppc64)                 | `ppc64`                | [`is_ppc64()`](detection.md#extra_platforms.detection.is_ppc64)                               |
|   ⚡   | [PowerPC 64-bit (little-endian)](https://en.wikipedia.org/wiki/Ppc64)              | `ppc64le`              | [`is_ppc64le()`](detection.md#extra_platforms.detection.is_ppc64le)                           |
|   Ⅴ    | [RISC-V (32-bit)](https://en.wikipedia.org/wiki/RISC-V)                            | `riscv32`              | [`is_riscv32()`](detection.md#extra_platforms.detection.is_riscv32)                           |
|   Ⅴ    | [RISC-V (64-bit)](https://en.wikipedia.org/wiki/RISC-V)                            | `riscv64`              | [`is_riscv64()`](detection.md#extra_platforms.detection.is_riscv64)                           |
|   🏢   | [IBM z/Architecture (s390x)](https://en.wikipedia.org/wiki/Z/Architecture)         | `s390x`                | [`is_s390x()`](detection.md#extra_platforms.detection.is_s390x)                               |
|   ☀️   | [SPARC (32-bit)](https://en.wikipedia.org/wiki/SPARC)                              | `sparc`                | [`is_sparc()`](detection.md#extra_platforms.detection.is_sparc)                               |
|   ☀️   | [SPARC (64-bit)](https://en.wikipedia.org/wiki/SPARC)                              | `sparc64`              | [`is_sparc64()`](detection.md#extra_platforms.detection.is_sparc64)                           |
|   ❓   | [Unknown architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture) | `unknown_architecture` | [`is_unknown_architecture()`](detection.md#extra_platforms.detection.is_unknown_architecture) |
|   🌐   | [WebAssembly (32-bit)](https://en.wikipedia.org/wiki/WebAssembly)                  | `wasm32`               | [`is_wasm32()`](detection.md#extra_platforms.detection.is_wasm32)                             |
|   🌐   | [WebAssembly (64-bit)](https://en.wikipedia.org/wiki/WebAssembly)                  | `wasm64`               | [`is_wasm64()`](detection.md#extra_platforms.detection.is_wasm64)                             |
|   🖥️   | [x86-64 (AMD64)](https://en.wikipedia.org/wiki/X86-64)                             | `x86_64`               | [`is_x86_64()`](detection.md#extra_platforms.detection.is_x86_64)                             |

<!-- architecture-table-end -->

## Groups of architectures

All recognized architectures are grouped in families, with each architecture belonging to exactly one family.

Here are the non-overlapping families that encompass all recognized architectures, visualized as a Sankey diagram:

<!-- architecture-multi-level-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 800}}
---
sankey-beta

ALL_ARCHITECTURES,ANY_ARM,5
ALL_ARCHITECTURES,X86,4
ALL_ARCHITECTURES,ANY_MIPS,4
ALL_ARCHITECTURES,POWERPC,3
ALL_ARCHITECTURES,WEBASSEMBLY,2
ALL_ARCHITECTURES,RISCV,2
ALL_ARCHITECTURES,ANY_SPARC,2
ALL_ARCHITECTURES,LOONGARCH,1
ALL_ARCHITECTURES,IBM_MAINFRAME,1
ANY_ARM,aarch64,1
ANY_ARM,arm,1
ANY_ARM,armv6l,1
ANY_ARM,armv7l,1
ANY_ARM,armv8l,1
X86,i386,1
X86,i586,1
X86,i686,1
X86,x86_64,1
ANY_MIPS,mips,1
ANY_MIPS,mips64,1
ANY_MIPS,mips64el,1
ANY_MIPS,mipsel,1
POWERPC,ppc,1
POWERPC,ppc64,1
POWERPC,ppc64le,1
WEBASSEMBLY,wasm32,1
WEBASSEMBLY,wasm64,1
RISCV,riscv32,1
RISCV,riscv64,1
ANY_SPARC,sparc,1
ANY_SPARC,sparc64,1
LOONGARCH,loongarch64,1
IBM_MAINFRAME,s390x,1
ALL_ARCHITECTURES,unknown_architecture,1
```

<!-- architecture-multi-level-sankey-end -->

And the same families visualized as a mindmap:

<!-- architecture-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((🏛️ all_architectures))
        )𝘅 X86(
            (𝗶 i386)
            (𝗶 i586)
            (𝗶 i686)
            (🖥️ x86_64)
        )🌐 WEBASSEMBLY(
            (🌐 wasm32)
            (🌐 wasm64)
        )Ⅴ RISCV(
            (Ⅴ riscv32)
            (Ⅴ riscv64)
        )⚡ POWERPC(
            (⚡ ppc)
            (⚡ ppc64)
            (⚡ ppc64le)
        )🐉 LOONGARCH(
            (🐉 loongarch64)
        )🏢 IBM_MAINFRAME(
            (🏢 s390x)
        )☀️ ANY_SPARC(
            (☀️ sparc)
            (☀️ sparc64)
        )🔲 ANY_MIPS(
            (🔲 mips)
            (🔲 mips64)
            (🔲 mips64el)
            (🔲 mipsel)
        )📱 ANY_ARM(
            (📱 aarch64)
            (📱 arm)
            (📱 armv6l)
            (📱 armv7l)
            (📱 armv8l)
        (❓ unknown_architecture)
```

<!-- architecture-mindmap-end -->

### All architecture groups

<!-- architecture-groups-table-start -->

|  Icon  | Group ID                                                                      | Description            |  Canonical  |   Member count |
| :--: | :---------------------------------------------------------------------------- | :--------------------- | :-------: | -----------: |
|   🏛️   | [`all_architectures`](groups.md#extra_platforms.group_data.ALL_ARCHITECTURES) | All architectures      |             |             25 |
|   📱   | [`any_arm`](groups.md#extra_platforms.group_data.ANY_ARM)                     | Any ARM architecture   |     ✅      |              5 |
|   🔲   | [`any_mips`](groups.md#extra_platforms.group_data.ANY_MIPS)                   | Any MIPS architecture  |     ✅      |              4 |
|   ☀️   | [`any_sparc`](groups.md#extra_platforms.group_data.ANY_SPARC)                 | Any SPARC architecture |     ✅      |              2 |
|   🏢   | [`ibm_mainframe`](groups.md#extra_platforms.group_data.IBM_MAINFRAME)         | IBM mainframe          |     ✅      |              1 |
|   🐉   | [`loongarch`](groups.md#extra_platforms.group_data.LOONGARCH)                 | LoongArch              |     ✅      |              1 |
|   ⚡   | [`powerpc`](groups.md#extra_platforms.group_data.POWERPC)                     | PowerPC family         |     ✅      |              3 |
|   Ⅴ    | [`riscv`](groups.md#extra_platforms.group_data.RISCV)                         | RISC-V family          |     ✅      |              2 |
|   🌐   | [`webassembly`](groups.md#extra_platforms.group_data.WEBASSEMBLY)             | WebAssembly            |     ✅      |              2 |
|   𝘅    | [`x86`](groups.md#extra_platforms.group_data.X86)                             | x86 family             |     ✅      |              4 |

<!-- architecture-groups-table-end -->

```{hint}
Canonical groups are non-overlapping groups that together cover all recognized architectures. They are marked with a ✅ icon in the table above.

Other groups are provided for convenience, but overlap with each other or with canonical groups.
```

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
