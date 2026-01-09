# {octicon}`apps` Groups

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

|  Icon  | Group ID                                                                        | Description                                 |  Canonical  |   Member count |
| :--: | :------------------------------------------------------------------------------ | :------------------------------------------ | :-------: | -----------: |
|   🏛️   | [`all_architectures`](groups.md#extra_platforms.group_data.ALL_ARCHITECTURES)   | All architectures                           |             |             25 |
|   ♺    | [`all_ci`](groups.md#extra_platforms.group_data.ALL_CI)                         | All CI systems                              |     ✅      |             12 |
|   ⚙️   | [`all_platforms`](groups.md#extra_platforms.group_data.ALL_PLATFORMS)           | All platforms                               |             |             48 |
|   ⁕    | [`all_traits`](groups.md#extra_platforms.group_data.ALL_TRAITS)                 | Any architectures, platforms and CI systems |             |             85 |
|   📱   | [`any_arm`](groups.md#extra_platforms.group_data.ANY_ARM)                       | Any ARM architecture                        |     ✅      |              5 |
|   🔲   | [`any_mips`](groups.md#extra_platforms.group_data.ANY_MIPS)                     | Any MIPS architecture                       |     ✅      |              4 |
|   ☀️   | [`any_sparc`](groups.md#extra_platforms.group_data.ANY_SPARC)                   | Any SPARC architecture                      |     ✅      |              2 |
|   🪟   | [`any_windows`](groups.md#extra_platforms.group_data.ANY_WINDOWS)               | Any Windows                                 |     ✅      |              1 |
|  🅱️+   | [`bsd`](groups.md#extra_platforms.group_data.BSD)                               | Any BSD                                     |     ✅      |              6 |
|   🅱️   | [`bsd_without_macos`](groups.md#extra_platforms.group_data.BSD_WITHOUT_MACOS)   | Any BSD excluding macOS                     |             |              5 |
|   🏢   | [`ibm_mainframe`](groups.md#extra_platforms.group_data.IBM_MAINFRAME)           | IBM mainframe                               |     ✅      |              1 |
|   🐧   | [`linux`](groups.md#extra_platforms.group_data.LINUX)                           | Any Linux distribution                      |     ✅      |             35 |
|   ≚    | [`linux_layers`](groups.md#extra_platforms.group_data.LINUX_LAYERS)             | Any Linux compatibility layers              |     ✅      |              2 |
|  🐧+   | [`linux_like`](groups.md#extra_platforms.group_data.LINUX_LIKE)                 | Any Linux and compatibility layers          |             |             37 |
|   🐉   | [`loongarch`](groups.md#extra_platforms.group_data.LOONGARCH)                   | LoongArch                                   |     ✅      |              1 |
|   ⊎    | [`other_unix`](groups.md#extra_platforms.group_data.OTHER_UNIX)                 | Any other Unix                              |     ✅      |              1 |
|   ⚡   | [`powerpc`](groups.md#extra_platforms.group_data.POWERPC)                       | PowerPC family                              |     ✅      |              3 |
|   Ⅴ    | [`riscv`](groups.md#extra_platforms.group_data.RISCV)                           | RISC-V family                               |     ✅      |              2 |
|   𝐕    | [`system_v`](groups.md#extra_platforms.group_data.SYSTEM_V)                     | AT&T System Five                            |     ✅      |              2 |
|   ⨷    | [`unix`](groups.md#extra_platforms.group_data.UNIX)                             | Any Unix                                    |             |             47 |
|   ≛    | [`unix_layers`](groups.md#extra_platforms.group_data.UNIX_LAYERS)               | Any Unix compatibility layers               |     ✅      |              1 |
|   ⨂    | [`unix_without_macos`](groups.md#extra_platforms.group_data.UNIX_WITHOUT_MACOS) | Any Unix excluding macOS                    |             |             46 |
|   🌐   | [`webassembly`](groups.md#extra_platforms.group_data.WEBASSEMBLY)               | WebAssembly                                 |     ✅      |              2 |
|   𝘅    | [`x86`](groups.md#extra_platforms.group_data.X86)                               | x86 family                                  |     ✅      |              4 |

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
.. autodata:: extra_platforms.group_data.WEBASSEMBLY
.. autodata:: extra_platforms.group_data.X86
```

<!-- group-data-autodata-end -->
