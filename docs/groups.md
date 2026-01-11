# {octicon}`apps` Groups

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

| Icon | Symbol                                                                          | Description                                 | Detection function                                                              | Canonical | Member count |
| :--: | :------------------------------------------------------------------------------ | :------------------------------------------ | :------------------------------------------------------------------------------ | :-------: | -----------: |
|  🏛️  | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.group_data.ALL_ARCHITECTURES)   | All architectures                           | [`is_all_architectures()`](detection.md#extra_platforms.is_all_architectures)   |           |           24 |
|  ♺   | [`ALL_CI`](groups.md#extra_platforms.group_data.ALL_CI)                         | All CI systems                              | [`is_all_ci()`](detection.md#extra_platforms.is_all_ci)                         |     ⬥     |           11 |
|  ⚙️  | [`ALL_PLATFORMS`](groups.md#extra_platforms.group_data.ALL_PLATFORMS)           | All platforms                               | [`is_all_platforms()`](detection.md#extra_platforms.is_all_platforms)           |           |           47 |
|  ⁕   | [`ALL_TRAITS`](groups.md#extra_platforms.group_data.ALL_TRAITS)                 | Any architectures, platforms and CI systems | [`is_all_traits()`](detection.md#extra_platforms.is_all_traits)                 |           |           82 |
|  📱  | [`ANY_ARM`](groups.md#extra_platforms.group_data.ANY_ARM)                       | Any ARM architecture                        | [`is_any_arm()`](detection.md#extra_platforms.is_any_arm)                       |     ⬥     |            5 |
|  🔲  | [`ANY_MIPS`](groups.md#extra_platforms.group_data.ANY_MIPS)                     | Any MIPS architecture                       | [`is_any_mips()`](detection.md#extra_platforms.is_any_mips)                     |     ⬥     |            4 |
|  ☀️  | [`ANY_SPARC`](groups.md#extra_platforms.group_data.ANY_SPARC)                   | Any SPARC architecture                      | [`is_any_sparc()`](detection.md#extra_platforms.is_any_sparc)                   |     ⬥     |            2 |
|  🪟  | [`ANY_WINDOWS`](groups.md#extra_platforms.group_data.ANY_WINDOWS)               | Any Windows                                 | [`is_any_windows()`](detection.md#extra_platforms.is_any_windows)               |     ⬥     |            1 |
|  ³²  | [`ARCH_32_BIT`](groups.md#extra_platforms.group_data.ARCH_32_BIT)               | 32-bit architectures                        | [`is_arch_32_bit()`](detection.md#extra_platforms.is_arch_32_bit)               |           |           13 |
|  ⁶⁴  | [`ARCH_64_BIT`](groups.md#extra_platforms.group_data.ARCH_64_BIT)               | 64-bit architectures                        | [`is_arch_64_bit()`](detection.md#extra_platforms.is_arch_64_bit)               |           |           11 |
| 🅱️+  | [`BSD`](groups.md#extra_platforms.group_data.BSD)                               | Any BSD                                     | [`is_bsd()`](detection.md#extra_platforms.is_bsd)                               |     ⬥     |            6 |
|  🅱️  | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.group_data.BSD_WITHOUT_MACOS)   | Any BSD excluding macOS                     | [`is_bsd_without_macos()`](detection.md#extra_platforms.is_bsd_without_macos)   |           |            5 |
|  🏢  | [`IBM_MAINFRAME`](groups.md#extra_platforms.group_data.IBM_MAINFRAME)           | IBM mainframe                               | [`is_ibm_mainframe()`](detection.md#extra_platforms.is_ibm_mainframe)           |     ⬥     |            1 |
|  🐧  | [`LINUX`](groups.md#extra_platforms.group_data.LINUX)                           | Any Linux distribution                      | [`is_linux()`](detection.md#extra_platforms.is_linux)                           |     ⬥     |           34 |
|  ≚   | [`LINUX_LAYERS`](groups.md#extra_platforms.group_data.LINUX_LAYERS)             | Any Linux compatibility layers              | [`is_linux_layers()`](detection.md#extra_platforms.is_linux_layers)             |     ⬥     |            2 |
| 🐧+  | [`LINUX_LIKE`](groups.md#extra_platforms.group_data.LINUX_LIKE)                 | Any Linux and compatibility layers          | [`is_linux_like()`](detection.md#extra_platforms.is_linux_like)                 |           |           36 |
|  🐉  | [`LOONGARCH`](groups.md#extra_platforms.group_data.LOONGARCH)                   | LoongArch                                   | [`is_loongarch()`](detection.md#extra_platforms.is_loongarch)                   |     ⬥     |            1 |
|  ⊎   | [`OTHER_UNIX`](groups.md#extra_platforms.group_data.OTHER_UNIX)                 | Any other Unix                              | [`is_other_unix()`](detection.md#extra_platforms.is_other_unix)                 |     ⬥     |            1 |
|  ⚡  | [`POWERPC`](groups.md#extra_platforms.group_data.POWERPC)                       | PowerPC family                              | [`is_powerpc()`](detection.md#extra_platforms.is_powerpc)                       |     ⬥     |            3 |
|  Ⅴ   | [`RISCV`](groups.md#extra_platforms.group_data.RISCV)                           | RISC-V family                               | [`is_riscv()`](detection.md#extra_platforms.is_riscv)                           |     ⬥     |            2 |
|  𝐕   | [`SYSTEM_V`](groups.md#extra_platforms.group_data.SYSTEM_V)                     | AT&T System Five                            | [`is_system_v()`](detection.md#extra_platforms.is_system_v)                     |     ⬥     |            2 |
|  ⨷   | [`UNIX`](groups.md#extra_platforms.group_data.UNIX)                             | Any Unix                                    | [`is_unix()`](detection.md#extra_platforms.is_unix)                             |           |           46 |
|  ≛   | [`UNIX_LAYERS`](groups.md#extra_platforms.group_data.UNIX_LAYERS)               | Any Unix compatibility layers               | [`is_unix_layers()`](detection.md#extra_platforms.is_unix_layers)               |     ⬥     |            1 |
|  ⨂   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.group_data.UNIX_WITHOUT_MACOS) | Any Unix excluding macOS                    | [`is_unix_without_macos()`](detection.md#extra_platforms.is_unix_without_macos) |           |           45 |
|  ❓  | [`UNKNOWN`](groups.md#extra_platforms.group_data.UNKNOWN)                       | Unknown                                     | [`is_unknown()`](detection.md#extra_platforms.is_unknown)                       |     ⬥     |            3 |
|  🌐  | [`WEBASSEMBLY`](groups.md#extra_platforms.group_data.WEBASSEMBLY)               | WebAssembly                                 | [`is_webassembly()`](detection.md#extra_platforms.is_webassembly)               |     ⬥     |            2 |
|  𝘅   | [`X86`](groups.md#extra_platforms.group_data.X86)                               | x86 family                                  | [`is_x86()`](detection.md#extra_platforms.is_x86)                               |     ⬥     |            4 |

```{hint}
Canonical groups are non-overlapping groups that together cover all recognized traits. They are marked with a ⬥ icon in the table above.

Other groups are provided for convenience, but overlap with each other or with canonical groups.
```

<!-- groups-table-end -->

## `extra_platforms.group` API

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

## `extra_platforms.group_data` API

```{eval-rst}
.. autoclasstree:: extra_platforms.group_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.group_data
```

<!-- group-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.group_data.ALL_ARCHITECTURES
.. autodata:: extra_platforms.group_data.ALL_CI
.. autodata:: extra_platforms.group_data.ALL_PLATFORMS
.. autodata:: extra_platforms.group_data.ALL_TRAITS
.. autodata:: extra_platforms.group_data.ANY_ARM
.. autodata:: extra_platforms.group_data.ANY_MIPS
.. autodata:: extra_platforms.group_data.ANY_SPARC
.. autodata:: extra_platforms.group_data.ANY_WINDOWS
.. autodata:: extra_platforms.group_data.ARCH_32_BIT
.. autodata:: extra_platforms.group_data.ARCH_64_BIT
.. autodata:: extra_platforms.group_data.BSD
.. autodata:: extra_platforms.group_data.BSD_WITHOUT_MACOS
.. autodata:: extra_platforms.group_data.IBM_MAINFRAME
.. autodata:: extra_platforms.group_data.LINUX
.. autodata:: extra_platforms.group_data.LINUX_LAYERS
.. autodata:: extra_platforms.group_data.LINUX_LIKE
.. autodata:: extra_platforms.group_data.LOONGARCH
.. autodata:: extra_platforms.group_data.OTHER_UNIX
.. autodata:: extra_platforms.group_data.POWERPC
.. autodata:: extra_platforms.group_data.RISCV
.. autodata:: extra_platforms.group_data.SYSTEM_V
.. autodata:: extra_platforms.group_data.UNIX
.. autodata:: extra_platforms.group_data.UNIX_LAYERS
.. autodata:: extra_platforms.group_data.UNIX_WITHOUT_MACOS
.. autodata:: extra_platforms.group_data.UNKNOWN
.. autodata:: extra_platforms.group_data.WEBASSEMBLY
.. autodata:: extra_platforms.group_data.X86
```

<!-- group-data-autodata-end -->
