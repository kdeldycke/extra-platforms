# {octicon}`apps` Groups

```{py:currentmodule} extra_platforms
```

## Group usage

```{todo}
Explain high-level usage of groups here. Including membership testing and set operations. And how to create custom groups (from scratch or by combining existing groups).
```

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

| Icon | Symbol                      | Description                                 | [Detection](detection.md)    | [Canonical](groups.md#extra_platforms.group.Group.canonical) |
| :--: | :-------------------------- | :------------------------------------------ | :--------------------------- | :----------------------------------------------------------: |
|  🏛️  | {data}`~ALL_ARCHITECTURES`  | All architectures                           | {func}`~is_any_architecture` |                                                              |
|  📱  | {data}`~ALL_ARM`            | ARM architectures                           | {func}`~is_any_arm`          |                              ⬥                               |
|  ♺   | {data}`~ALL_CI`             | CI systems                                  | {func}`~is_any_ci`           |                              ⬥                               |
|  🔲  | {data}`~ALL_MIPS`           | MIPS architectures                          | {func}`~is_any_mips`         |                              ⬥                               |
|  ⚙️  | {data}`~ALL_PLATFORMS`      | All platforms                               | {func}`~is_any_platform`     |                                                              |
|  ☀️  | {data}`~ALL_SPARC`          | SPARC architectures                         | {func}`~is_any_sparc`        |                              ⬥                               |
|  ⁕   | {data}`~ALL_TRAITS`         | All architectures, platforms and CI systems | {func}`~is_any_trait`        |                                                              |
|  🪟  | {data}`~ALL_WINDOWS`        | All Windows                                 | {func}`~is_any_windows`      |                              ⬥                               |
|  ³²  | {data}`~ARCH_32_BIT`        | 32-bit architectures                        | {func}`~is_arch_32_bit`      |                                                              |
|  ⁶⁴  | {data}`~ARCH_64_BIT`        | 64-bit architectures                        | {func}`~is_arch_64_bit`      |                                                              |
|  ⬆️  | {data}`~BIG_ENDIAN`         | Big-endian architectures                    | {func}`~is_big_endian`       |                                                              |
| 🅱️+  | {data}`~BSD`                | All BSD                                     | {func}`~is_bsd`              |                              ⬥                               |
|  🅱️  | {data}`~BSD_WITHOUT_MACOS`  | All BSD excluding macOS                     | {func}`~is_bsd_not_macos`    |                                                              |
|  🏢  | {data}`~IBM_MAINFRAME`      | IBM mainframe                               | {func}`~is_ibm_mainframe`    |                              ⬥                               |
|  🐧  | {data}`~LINUX`              | Linux distributions                         | {func}`~is_linux`            |                              ⬥                               |
|  ≚   | {data}`~LINUX_LAYERS`       | Linux compatibility layers                  | {func}`~is_linux_layers`     |                              ⬥                               |
| 🐧+  | {data}`~LINUX_LIKE`         | All Linux & compatibility layers            | {func}`~is_linux_like`       |                                                              |
|  ⬇️  | {data}`~LITTLE_ENDIAN`      | Little-endian architectures                 | {func}`~is_little_endian`    |                                                              |
|  🐉  | {data}`~LOONGARCH`          | LoongArch                                   | {func}`~is_loongarch`        |                              ⬥                               |
|  🅟   | {data}`~OTHER_POSIX`        | Other POSIX-compliant platforms             | {func}`~is_other_posix`      |                              ⬥                               |
|  ⚡  | {data}`~POWERPC`            | PowerPC family                              | {func}`~is_powerpc`          |                              ⬥                               |
|  Ⅴ   | {data}`~RISCV`              | RISC-V family                               | {func}`~is_riscv`            |                              ⬥                               |
|  𝐕   | {data}`~SYSTEM_V`           | AT&T System Five                            | {func}`~is_system_v`         |                              ⬥                               |
|  ⨷   | {data}`~UNIX`               | All Unix                                    | {func}`~is_unix`             |                                                              |
|  ≛   | {data}`~UNIX_LAYERS`        | Unix compatibility layers                   | {func}`~is_unix_layers`      |                              ⬥                               |
|  ⨂   | {data}`~UNIX_WITHOUT_MACOS` | All Unix excluding macOS                    | {func}`~is_unix_not_macos`   |                                                              |
|  ❓  | {data}`~UNKNOWN`            | Unknown                                     | {func}`~is_unknown`          |                              ⬥                               |
|  🌐  | {data}`~WEBASSEMBLY`        | WebAssembly                                 | {func}`~is_webassembly`      |                              ⬥                               |
|  𝘅   | {data}`~X86`                | x86 family                                  | {func}`~is_x86`              |                              ⬥                               |

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
.. autodata:: extra_platforms.BIG_ENDIAN
.. autodata:: extra_platforms.BSD
.. autodata:: extra_platforms.BSD_WITHOUT_MACOS
.. autodata:: extra_platforms.IBM_MAINFRAME
.. autodata:: extra_platforms.LINUX
.. autodata:: extra_platforms.LINUX_LAYERS
.. autodata:: extra_platforms.LINUX_LIKE
.. autodata:: extra_platforms.LITTLE_ENDIAN
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

## Group collections

```{eval-rst}
.. autodata:: extra_platforms.group_data.ALL_ARCHITECTURE_GROUPS
.. autodata:: extra_platforms.group_data.ALL_CI_GROUPS
.. autodata:: extra_platforms.group_data.ALL_GROUPS
.. autodata:: extra_platforms.group_data.ALL_PLATFORM_GROUPS
.. autodata:: extra_platforms.group_data.EXTRA_GROUPS
.. autodata:: extra_platforms.group_data.NON_OVERLAPPING_GROUPS
```

## ID collections

```{eval-rst}
.. autodata:: extra_platforms.group_data.ALL_GROUP_IDS
.. autodata:: extra_platforms.group_data.ALL_IDS
.. autodata:: extra_platforms.group_data.ALL_TRAIT_IDS
```

## Trait and group operations

```{eval-rst}
.. autofunction:: extra_platforms.extract_members
.. autofunction:: extra_platforms.traits_from_ids
.. autofunction:: extra_platforms.groups_from_ids
.. autofunction:: extra_platforms.reduce
```

## Deprecated groups

```{eval-rst}
.. autodata:: extra_platforms.ALL_PLATFORMS_WITHOUT_CI
.. autodata:: extra_platforms.ANY_ARM
.. autodata:: extra_platforms.ANY_MIPS
.. autodata:: extra_platforms.ANY_SPARC
.. autodata:: extra_platforms.ANY_WINDOWS
.. autodata:: extra_platforms.OTHER_UNIX
```

## Deprecated group utilities

```{eval-rst}
.. autofunction:: extra_platforms.platforms_from_ids
.. autodata:: extra_platforms.ALL_PLATFORM_IDS
```

## Group implementation

```{eval-rst}
.. autoclass:: extra_platforms.Group
   :members:
   :private-members:
   :special-members:
   :show-inheritance:
```

```{eval-rst}
.. autoclasstree:: extra_platforms.group
   :strict:
```

<!-- group-module-automodule-start -->

```{eval-rst}
.. automodule:: extra_platforms.group
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: Group, extract_members, groups_from_ids, reduce, traits_from_ids
```

<!-- group-module-automodule-end -->

```{eval-rst}
.. autoclasstree:: extra_platforms.group_data
   :strict:
```

<!-- group-data-module-automodule-start -->

```{eval-rst}
.. automodule:: extra_platforms.group_data
   :exclude-members: ALL_ARCHITECTURES, ALL_ARCHITECTURE_GROUPS, ALL_ARM, ALL_CI, ALL_CI_GROUPS, ALL_GROUPS, ALL_GROUP_IDS, ALL_IDS, ALL_MIPS, ALL_PLATFORMS, ALL_PLATFORM_GROUPS, ALL_SPARC, ALL_TRAITS, ALL_TRAIT_IDS, ALL_WINDOWS, ARCH_32_BIT, ARCH_64_BIT, BIG_ENDIAN, BSD, BSD_WITHOUT_MACOS, EXTRA_GROUPS, IBM_MAINFRAME, LINUX, LINUX_LAYERS, LINUX_LIKE, LITTLE_ENDIAN, LOONGARCH, NON_OVERLAPPING_GROUPS, OTHER_POSIX, POWERPC, RISCV, SYSTEM_V, UNIX, UNIX_LAYERS, UNIX_WITHOUT_MACOS, UNKNOWN, WEBASSEMBLY, X86
```

<!-- group-data-module-automodule-end -->
