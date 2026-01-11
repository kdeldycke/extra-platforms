# {octicon}`apps` Groups

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

|  Icon  | Symbol                                                                          | Description                                 |  Canonical  |   Member count |
| :--: | :------------------------------------------------------------------------------ | :------------------------------------------ | :-------: | -----------: |
|   🏛️   | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.group_data.ALL_ARCHITECTURES)   | All architectures                           |             |             24 |
|   ♺    | [`ALL_CI`](groups.md#extra_platforms.group_data.ALL_CI)                         | All CI systems                              |      ⬥      |             11 |
|   ⚙️   | [`ALL_PLATFORMS`](groups.md#extra_platforms.group_data.ALL_PLATFORMS)           | All platforms                               |             |             47 |
|   ⁕    | [`ALL_TRAITS`](groups.md#extra_platforms.group_data.ALL_TRAITS)                 | Any architectures, platforms and CI systems |             |             82 |
|   📱   | [`ANY_ARM`](groups.md#extra_platforms.group_data.ANY_ARM)                       | Any ARM architecture                        |      ⬥      |              5 |
|   🔲   | [`ANY_MIPS`](groups.md#extra_platforms.group_data.ANY_MIPS)                     | Any MIPS architecture                       |      ⬥      |              4 |
|   ☀️   | [`ANY_SPARC`](groups.md#extra_platforms.group_data.ANY_SPARC)                   | Any SPARC architecture                      |      ⬥      |              2 |
|   🪟   | [`ANY_WINDOWS`](groups.md#extra_platforms.group_data.ANY_WINDOWS)               | Any Windows                                 |      ⬥      |              1 |
|   ³²   | [`ARCH_32_BIT`](groups.md#extra_platforms.group_data.ARCH_32_BIT)               | 32-bit architectures                        |             |             13 |
|   ⁶⁴   | [`ARCH_64_BIT`](groups.md#extra_platforms.group_data.ARCH_64_BIT)               | 64-bit architectures                        |             |             11 |
|  🅱️+   | [`BSD`](groups.md#extra_platforms.group_data.BSD)                               | Any BSD                                     |      ⬥      |              6 |
|   🅱️   | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.group_data.BSD_WITHOUT_MACOS)   | Any BSD excluding macOS                     |             |              5 |
|   🏢   | [`IBM_MAINFRAME`](groups.md#extra_platforms.group_data.IBM_MAINFRAME)           | IBM mainframe                               |      ⬥      |              1 |
|   🐧   | [`LINUX`](groups.md#extra_platforms.group_data.LINUX)                           | Any Linux distribution                      |      ⬥      |             34 |
|   ≚    | [`LINUX_LAYERS`](groups.md#extra_platforms.group_data.LINUX_LAYERS)             | Any Linux compatibility layers              |      ⬥      |              2 |
|  🐧+   | [`LINUX_LIKE`](groups.md#extra_platforms.group_data.LINUX_LIKE)                 | Any Linux and compatibility layers          |             |             36 |
|   🐉   | [`LOONGARCH`](groups.md#extra_platforms.group_data.LOONGARCH)                   | LoongArch                                   |      ⬥      |              1 |
|   ⊎    | [`OTHER_UNIX`](groups.md#extra_platforms.group_data.OTHER_UNIX)                 | Any other Unix                              |      ⬥      |              1 |
|   ⚡   | [`POWERPC`](groups.md#extra_platforms.group_data.POWERPC)                       | PowerPC family                              |      ⬥      |              3 |
|   Ⅴ    | [`RISCV`](groups.md#extra_platforms.group_data.RISCV)                           | RISC-V family                               |      ⬥      |              2 |
|   𝐕    | [`SYSTEM_V`](groups.md#extra_platforms.group_data.SYSTEM_V)                     | AT&T System Five                            |      ⬥      |              2 |
|   ⨷    | [`UNIX`](groups.md#extra_platforms.group_data.UNIX)                             | Any Unix                                    |             |             46 |
|   ≛    | [`UNIX_LAYERS`](groups.md#extra_platforms.group_data.UNIX_LAYERS)               | Any Unix compatibility layers               |      ⬥      |              1 |
|   ⨂    | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.group_data.UNIX_WITHOUT_MACOS) | Any Unix excluding macOS                    |             |             45 |
|   ❓   | [`UNKNOWN`](groups.md#extra_platforms.group_data.UNKNOWN)                       | Unknown                                     |      ⬥      |              3 |
|   🌐   | [`WEBASSEMBLY`](groups.md#extra_platforms.group_data.WEBASSEMBLY)               | WebAssembly                                 |      ⬥      |              2 |
|   𝘅    | [`X86`](groups.md#extra_platforms.group_data.X86)                               | x86 family                                  |      ⬥      |              4 |

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
