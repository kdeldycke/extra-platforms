# {octicon}`apps` Groups

## Group usage

```{todo}
Explain high-level usage of groups here. Including membership testing and set operations. And how to create custom groups (from scratch or by combining existing groups).
```

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

| Icon | Symbol                                      | Description                                 | [Detection](detection.md)                    | [Canonical](groups.md#extra_platforms.group.Group.canonical) |
| :--: | :------------------------------------------ | :------------------------------------------ | :------------------------------------------- | :----------------------------------------------------------: |
|  🏛️  | {data}`~extra_platforms.ALL_ARCHITECTURES`  | All architectures                           | {func}`~extra_platforms.is_any_architecture` |                                                              |
|  📱  | {data}`~extra_platforms.ALL_ARM`            | ARM architectures                           | {func}`~extra_platforms.is_any_arm`          |                              ⬥                               |
|  ♺   | {data}`~extra_platforms.ALL_CI`             | CI systems                                  | {func}`~extra_platforms.is_any_ci`           |                              ⬥                               |
|  🔲  | {data}`~extra_platforms.ALL_MIPS`           | MIPS architectures                          | {func}`~extra_platforms.is_any_mips`         |                              ⬥                               |
|  ⚙️  | {data}`~extra_platforms.ALL_PLATFORMS`      | All platforms                               | {func}`~extra_platforms.is_any_platform`     |                                                              |
|  ☀️  | {data}`~extra_platforms.ALL_SPARC`          | SPARC architectures                         | {func}`~extra_platforms.is_any_sparc`        |                              ⬥                               |
|  ⁕   | {data}`~extra_platforms.ALL_TRAITS`         | All architectures, platforms and CI systems | {func}`~extra_platforms.is_any_trait`        |                                                              |
|  🪟  | {data}`~extra_platforms.ALL_WINDOWS`        | All Windows                                 | {func}`~extra_platforms.is_any_windows`      |                              ⬥                               |
|  ³²  | {data}`~extra_platforms.ARCH_32_BIT`        | 32-bit architectures                        | {func}`~extra_platforms.is_arch_32_bit`      |                                                              |
|  ⁶⁴  | {data}`~extra_platforms.ARCH_64_BIT`        | 64-bit architectures                        | {func}`~extra_platforms.is_arch_64_bit`      |                                                              |
| 🅱️+  | {data}`~extra_platforms.BSD`                | All BSD                                     | {func}`~extra_platforms.is_bsd`              |                              ⬥                               |
|  🅱️  | {data}`~extra_platforms.BSD_WITHOUT_MACOS`  | All BSD excluding macOS                     | {func}`~extra_platforms.is_bsd_not_macos`    |                                                              |
|  🏢  | {data}`~extra_platforms.IBM_MAINFRAME`      | IBM mainframe                               | {func}`~extra_platforms.is_ibm_mainframe`    |                              ⬥                               |
|  🐧  | {data}`~extra_platforms.LINUX`              | Linux distributions                         | {func}`~extra_platforms.is_linux`            |                              ⬥                               |
|  ≚   | {data}`~extra_platforms.LINUX_LAYERS`       | Linux compatibility layers                  | {func}`~extra_platforms.is_linux_layers`     |                              ⬥                               |
| 🐧+  | {data}`~extra_platforms.LINUX_LIKE`         | All Linux & compatibility layers            | {func}`~extra_platforms.is_linux_like`       |                                                              |
|  🐉  | {data}`~extra_platforms.LOONGARCH`          | LoongArch                                   | {func}`~extra_platforms.is_loongarch`        |                              ⬥                               |
|  🅟   | {data}`~extra_platforms.OTHER_POSIX`        | Other POSIX-compliant platforms             | {func}`~extra_platforms.is_other_posix`      |                              ⬥                               |
|  ⚡  | {data}`~extra_platforms.POWERPC`            | PowerPC family                              | {func}`~extra_platforms.is_powerpc`          |                              ⬥                               |
|  Ⅴ   | {data}`~extra_platforms.RISCV`              | RISC-V family                               | {func}`~extra_platforms.is_riscv`            |                              ⬥                               |
|  𝐕   | {data}`~extra_platforms.SYSTEM_V`           | AT&T System Five                            | {func}`~extra_platforms.is_system_v`         |                              ⬥                               |
|  ⨷   | {data}`~extra_platforms.UNIX`               | All Unix                                    | {func}`~extra_platforms.is_unix`             |                                                              |
|  ≛   | {data}`~extra_platforms.UNIX_LAYERS`        | Unix compatibility layers                   | {func}`~extra_platforms.is_unix_layers`      |                              ⬥                               |
|  ⨂   | {data}`~extra_platforms.UNIX_WITHOUT_MACOS` | All Unix excluding macOS                    | {func}`~extra_platforms.is_unix_not_macos`   |                                                              |
|  ❓  | {data}`~extra_platforms.UNKNOWN`            | Unknown                                     | {func}`~extra_platforms.is_unknown`          |                              ⬥                               |
|  🌐  | {data}`~extra_platforms.WEBASSEMBLY`        | WebAssembly                                 | {func}`~extra_platforms.is_webassembly`      |                              ⬥                               |
|  𝘅   | {data}`~extra_platforms.X86`                | x86 family                                  | {func}`~extra_platforms.is_x86`              |                              ⬥                               |

```{hint}
Canonical groups are non-overlapping groups that together cover all
recognized traits. They are marked with a ⬥ icon in the table above.

Other groups are provided for convenience, but overlap with each other or
with canonical groups.
```

<!-- groups-table-end -->

## Predefined groups

<!-- group-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.ALL_ARCHITECTURES
.. autodata:: extra_platforms.ALL_ARM
.. autodata:: extra_platforms.ALL_CI
.. autodata:: extra_platforms.ALL_MIPS
.. autodata:: extra_platforms.ALL_PLATFORMS
.. autodata:: extra_platforms.ALL_SPARC
.. autodata:: extra_platforms.ALL_TRAITS
.. autodata:: extra_platforms.ALL_WINDOWS
.. autodata:: extra_platforms.ARCH_32_BIT
.. autodata:: extra_platforms.ARCH_64_BIT
.. autodata:: extra_platforms.BSD
.. autodata:: extra_platforms.BSD_WITHOUT_MACOS
.. autodata:: extra_platforms.IBM_MAINFRAME
.. autodata:: extra_platforms.LINUX
.. autodata:: extra_platforms.LINUX_LAYERS
.. autodata:: extra_platforms.LINUX_LIKE
.. autodata:: extra_platforms.LOONGARCH
.. autodata:: extra_platforms.OTHER_POSIX
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
