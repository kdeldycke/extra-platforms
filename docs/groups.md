# {octicon}`apps` Groups

## Group usage

```{todo}
Explain high-level usage of groups here. Including membership testing and set operations.
```

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

| Icon | Symbol                                                               | Description                                 | [Detection](detection.md)                                                       | [Canonical](groups.md#extra_platforms.group.Group.canonical) |
| :--: | :------------------------------------------------------------------- | :------------------------------------------ | :------------------------------------------------------------------------------ | :----------------------------------------------------------: |
|  🏛️  | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.ALL_ARCHITECTURES)   | All architectures                           | [`is_all_architectures()`](detection.md#extra_platforms.is_all_architectures)   |                                                              |
|  ♺   | [`ALL_CI`](groups.md#extra_platforms.ALL_CI)                         | All CI systems                              | [`is_all_ci()`](detection.md#extra_platforms.is_all_ci)                         |                              ⬥                               |
|  ⚙️  | [`ALL_PLATFORMS`](groups.md#extra_platforms.ALL_PLATFORMS)           | All platforms                               | [`is_all_platforms()`](detection.md#extra_platforms.is_all_platforms)           |                                                              |
|  ⁕   | [`ALL_TRAITS`](groups.md#extra_platforms.ALL_TRAITS)                 | Any architectures, platforms and CI systems | [`is_all_traits()`](detection.md#extra_platforms.is_all_traits)                 |                                                              |
|  📱  | [`ANY_ARM`](groups.md#extra_platforms.ANY_ARM)                       | Any ARM architecture                        | [`is_any_arm()`](detection.md#extra_platforms.is_any_arm)                       |                              ⬥                               |
|  🔲  | [`ANY_MIPS`](groups.md#extra_platforms.ANY_MIPS)                     | Any MIPS architecture                       | [`is_any_mips()`](detection.md#extra_platforms.is_any_mips)                     |                              ⬥                               |
|  ☀️  | [`ANY_SPARC`](groups.md#extra_platforms.ANY_SPARC)                   | Any SPARC architecture                      | [`is_any_sparc()`](detection.md#extra_platforms.is_any_sparc)                   |                              ⬥                               |
|  🪟  | [`ANY_WINDOWS`](groups.md#extra_platforms.ANY_WINDOWS)               | Any Windows                                 | [`is_any_windows()`](detection.md#extra_platforms.is_any_windows)               |                              ⬥                               |
|  ³²  | [`ARCH_32_BIT`](groups.md#extra_platforms.ARCH_32_BIT)               | 32-bit architectures                        | [`is_arch_32_bit()`](detection.md#extra_platforms.is_arch_32_bit)               |                                                              |
|  ⁶⁴  | [`ARCH_64_BIT`](groups.md#extra_platforms.ARCH_64_BIT)               | 64-bit architectures                        | [`is_arch_64_bit()`](detection.md#extra_platforms.is_arch_64_bit)               |                                                              |
| 🅱️+  | [`BSD`](groups.md#extra_platforms.BSD)                               | Any BSD                                     | [`is_bsd()`](detection.md#extra_platforms.is_bsd)                               |                              ⬥                               |
|  🅱️  | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.BSD_WITHOUT_MACOS)   | Any BSD excluding macOS                     | [`is_bsd_without_macos()`](detection.md#extra_platforms.is_bsd_without_macos)   |                                                              |
|  🏢  | [`IBM_MAINFRAME`](groups.md#extra_platforms.IBM_MAINFRAME)           | IBM mainframe                               | [`is_ibm_mainframe()`](detection.md#extra_platforms.is_ibm_mainframe)           |                              ⬥                               |
|  🐧  | [`LINUX`](groups.md#extra_platforms.LINUX)                           | Any Linux distribution                      | [`is_linux()`](detection.md#extra_platforms.is_linux)                           |                              ⬥                               |
|  ≚   | [`LINUX_LAYERS`](groups.md#extra_platforms.LINUX_LAYERS)             | Any Linux compatibility layers              | [`is_linux_layers()`](detection.md#extra_platforms.is_linux_layers)             |                              ⬥                               |
| 🐧+  | [`LINUX_LIKE`](groups.md#extra_platforms.LINUX_LIKE)                 | Any Linux and compatibility layers          | [`is_linux_like()`](detection.md#extra_platforms.is_linux_like)                 |                                                              |
|  🐉  | [`LOONGARCH`](groups.md#extra_platforms.LOONGARCH)                   | LoongArch                                   | [`is_loongarch()`](detection.md#extra_platforms.is_loongarch)                   |                              ⬥                               |
|  ⊎   | [`OTHER_UNIX`](groups.md#extra_platforms.OTHER_UNIX)                 | Any other Unix                              | [`is_other_unix()`](detection.md#extra_platforms.is_other_unix)                 |                              ⬥                               |
|  ⚡  | [`POWERPC`](groups.md#extra_platforms.POWERPC)                       | PowerPC family                              | [`is_powerpc()`](detection.md#extra_platforms.is_powerpc)                       |                              ⬥                               |
|  Ⅴ   | [`RISCV`](groups.md#extra_platforms.RISCV)                           | RISC-V family                               | [`is_riscv()`](detection.md#extra_platforms.is_riscv)                           |                              ⬥                               |
|  𝐕   | [`SYSTEM_V`](groups.md#extra_platforms.SYSTEM_V)                     | AT&T System Five                            | [`is_system_v()`](detection.md#extra_platforms.is_system_v)                     |                              ⬥                               |
|  ⨷   | [`UNIX`](groups.md#extra_platforms.UNIX)                             | Any Unix                                    | [`is_unix()`](detection.md#extra_platforms.is_unix)                             |                                                              |
|  ≛   | [`UNIX_LAYERS`](groups.md#extra_platforms.UNIX_LAYERS)               | Any Unix compatibility layers               | [`is_unix_layers()`](detection.md#extra_platforms.is_unix_layers)               |                              ⬥                               |
|  ⨂   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.UNIX_WITHOUT_MACOS) | Any Unix excluding macOS                    | [`is_unix_without_macos()`](detection.md#extra_platforms.is_unix_without_macos) |                                                              |
|  ❓  | [`UNKNOWN`](groups.md#extra_platforms.UNKNOWN)                       | Unknown                                     | [`is_unknown()`](detection.md#extra_platforms.is_unknown)                       |                              ⬥                               |
|  🌐  | [`WEBASSEMBLY`](groups.md#extra_platforms.WEBASSEMBLY)               | WebAssembly                                 | [`is_webassembly()`](detection.md#extra_platforms.is_webassembly)               |                              ⬥                               |
|  𝘅   | [`X86`](groups.md#extra_platforms.X86)                               | x86 family                                  | [`is_x86()`](detection.md#extra_platforms.is_x86)                               |                              ⬥                               |

```{hint}
Canonical groups are non-overlapping groups that together cover all recognized traits. They are marked with a ⬥ icon in the table above.

Other groups are provided for convenience, but overlap with each other or with canonical groups.
```

<!-- groups-table-end -->

## Group details

<!-- group-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.ALL_ARCHITECTURES
.. autodata:: extra_platforms.ALL_CI
.. autodata:: extra_platforms.ALL_PLATFORMS
.. autodata:: extra_platforms.ALL_TRAITS
.. autodata:: extra_platforms.ANY_ARM
.. autodata:: extra_platforms.ANY_MIPS
.. autodata:: extra_platforms.ANY_SPARC
.. autodata:: extra_platforms.ANY_WINDOWS
.. autodata:: extra_platforms.ARCH_32_BIT
.. autodata:: extra_platforms.ARCH_64_BIT
.. autodata:: extra_platforms.BSD
.. autodata:: extra_platforms.BSD_WITHOUT_MACOS
.. autodata:: extra_platforms.IBM_MAINFRAME
.. autodata:: extra_platforms.LINUX
.. autodata:: extra_platforms.LINUX_LAYERS
.. autodata:: extra_platforms.LINUX_LIKE
.. autodata:: extra_platforms.LOONGARCH
.. autodata:: extra_platforms.OTHER_UNIX
.. autodata:: extra_platforms.POWERPC
.. autodata:: extra_platforms.RISCV
.. autodata:: extra_platforms.SYSTEM_V
.. autodata:: extra_platforms.UNIX
.. autodata:: extra_platforms.UNIX_LAYERS
.. autodata:: extra_platforms.UNIX_WITHOUT_MACOS
.. autodata:: extra_platforms.UNKNOWN
.. autodata:: extra_platforms.WEBASSEMBLY
.. autodata:: extra_platforms.X86
```

<!-- group-data-autodata-end -->

```{todo}
List and document group collections: `ALL_GROUP_IDS`, `ALL_TRAIT_IDS`, `ALL_IDS`, ...
```

## Group implementation

```{eval-rst}
.. autoclasstree:: extra_platforms.group
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.group
   :members:
   :undoc-members:
   :show-inheritance:
```

```{eval-rst}
.. autoclasstree:: extra_platforms.group_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.group_data
```