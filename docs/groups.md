# {octicon}`apps` Groups

```{py:currentmodule} extra_platforms
```

## Group usage

A {class}`~Group` is a collection of {class}`~Trait` instances (platforms, architectures, or CI systems). Groups support membership testing, iteration, and set-like operations.

### Membership testing

Check whether the current environment matches any member of a group:

```pycon
>>> from extra_platforms import is_linux
>>> is_linux()
True
```

Test if a specific trait belongs to a group. You can you both {class}`~Trait` instances and their string IDs:

```pycon
>>> from extra_platforms import LINUX, UBUNTU, MACOS
>>> UBUNTU in LINUX
True
>>> MACOS in LINUX
False
>>> "ubuntu" in LINUX
True
```

### Iteration

Groups are iterable and sized:

```pycon
>>> from extra_platforms import BSD
>>> len(BSD)
7
>>> for platform in BSD:
...     print(platform.id)
dragonfly_bsd
freebsd
macos
midnightbsd
netbsd
openbsd
sunos
```

### Set operations

Groups support standard set operations, returning new {class}`~Group` instances:

```pycon
>>> from extra_platforms import BSD, BSD_WITHOUT_MACOS, LINUX, MACOS
>>> only_macos = BSD.difference(BSD_WITHOUT_MACOS)
>>> only_macos.member_ids
frozenset({'macos'})
>>> combined = BSD.union(LINUX)
>>> MACOS in combined
True
```

Set operations also have operator overloads for more concise syntax:

```pycon
>>> from extra_platforms import BSD, BSD_WITHOUT_MACOS, LINUX, MACOS
>>> only_macos = BSD - BSD_WITHOUT_MACOS
>>> only_macos.member_ids
frozenset({'macos'})
>>> combined = BSD | LINUX
>>> MACOS in combined
True
```

Available operations: {meth}`~Group.union` (`|`), {meth}`~Group.intersection` (`&`), {meth}`~Group.difference` (`-`), {meth}`~Group.symmetric_difference` (`^`), {meth}`~Group.issubset`, {meth}`~Group.issuperset`, and {meth}`~Group.isdisjoint`.

### Mutating-style operations

Groups are immutable (frozen dataclasses), but provide methods that return new instances:

```pycon
>>> from extra_platforms import BSD, AIX
>>> extended = BSD.add(AIX)
>>> AIX in extended
True
>>> AIX in BSD
False
>>> shrunk = BSD.remove("macos")
>>> "macos" in shrunk
False
```

See also: {meth}`~Group.discard`, {meth}`~Group.pop`, {meth}`~Group.clear`, and {meth}`~Group.copy`.

### Creating custom groups

Build new groups from scratch or by combining existing ones:

```pycon
>>> from extra_platforms import Group, UBUNTU, DEBIAN, MACOS
>>> my_targets = Group("my_targets", "My Targets", "🎯", (UBUNTU, DEBIAN, MACOS))
>>> len(my_targets)
3
```

```{hint}
You can check my other Meta Package Manager project for a real life example, where I use {class}`~Group` to [manage families of target platforms](https://github.com/kdeldycke/meta-package-manager/blob/2c68ae19b4d3e5fee57c880168ca6c268f834275/meta_package_manager/inventory.py#L42-L62) for software packaging.
```

### Reducing traits to groups

The {func}`~reduce` function finds the minimal set of groups and traits that covers a given collection:

```pycon
>>> from extra_platforms import reduce, FREEBSD, NETBSD, OPENBSD, MACOS
>>> reduce([FREEBSD, NETBSD, OPENBSD, MACOS])
frozenset({BSD})
```

## All groups

All recognized groups and their properties:

<!-- groups-table-start -->

| Icon | Symbol                      | Description                                          | [Detection](detection.md)    | [Canonical](groups.md#extra_platforms.Group.canonical) |
| :--: | :-------------------------- | :--------------------------------------------------- | :--------------------------- | :----------------------------------------------------: |
|  🏛️  | {data}`~ALL_ARCHITECTURES`  | All architectures                                    | {func}`~is_any_architecture` |                                                        |
|  📱  | {data}`~ALL_ARM`            | ARM architectures                                    | {func}`~is_any_arm`          |                           ⬥                            |
|  ♺   | {data}`~ALL_CI`             | CI systems                                           | {func}`~is_any_ci`           |                           ⬥                            |
|  🔲  | {data}`~ALL_MIPS`           | MIPS architectures                                   | {func}`~is_any_mips`         |                           ⬥                            |
|  ⚙️  | {data}`~ALL_PLATFORMS`      | All platforms                                        | {func}`~is_any_platform`     |                                                        |
|  🐚  | {data}`~ALL_SHELLS`         | All shells                                           | {func}`~is_any_shell`        |                                                        |
|  ☀️  | {data}`~ALL_SPARC`          | SPARC architectures                                  | {func}`~is_any_sparc`        |                           ⬥                            |
|  ⁕   | {data}`~ALL_TRAITS`         | All architectures, platforms, shells, and CI systems | {func}`~is_any_trait`        |                                                        |
|  🪟  | {data}`~ALL_WINDOWS`        | All Windows                                          | {func}`~is_any_windows`      |                           ⬥                            |
|  ³²  | {data}`~ARCH_32_BIT`        | 32-bit architectures                                 | {func}`~is_arch_32_bit`      |                                                        |
|  ⁶⁴  | {data}`~ARCH_64_BIT`        | 64-bit architectures                                 | {func}`~is_arch_64_bit`      |                                                        |
|  ⬆️  | {data}`~BIG_ENDIAN`         | Big-endian architectures                             | {func}`~is_big_endian`       |                                                        |
|  💲  | {data}`~BOURNE_SHELLS`      | Bourne-compatible shells                             | {func}`~is_bourne_shells`    |                           ⬥                            |
|  Ⓑ   | {data}`~BSD`                | All BSD                                              | {func}`~is_bsd`              |                           ⬥                            |
|  🅱️  | {data}`~BSD_WITHOUT_MACOS`  | All BSD excluding macOS                              | {func}`~is_bsd_not_macos`    |                                                        |
|  🅲   | {data}`~C_SHELLS`           | C shells                                             | {func}`~is_c_shells`         |                           ⬥                            |
|  🏢  | {data}`~IBM_MAINFRAME`      | IBM mainframe                                        | {func}`~is_ibm_mainframe`    |                           ⬥                            |
|  🐧  | {data}`~LINUX`              | Linux distributions                                  | {func}`~is_linux`            |                           ⬥                            |
|  ≚   | {data}`~LINUX_LAYERS`       | Linux compatibility layers                           | {func}`~is_linux_layers`     |                           ⬥                            |
|  🐣  | {data}`~LINUX_LIKE`         | All Linux & compatibility layers                     | {func}`~is_linux_like`       |                                                        |
|  ⬇️  | {data}`~LITTLE_ENDIAN`      | Little-endian architectures                          | {func}`~is_little_endian`    |                                                        |
|  🐉  | {data}`~LOONGARCH`          | LoongArch                                            | {func}`~is_loongarch`        |                           ⬥                            |
|  🅟   | {data}`~OTHER_POSIX`        | Other POSIX-compliant platforms                      | {func}`~is_other_posix`      |                           ⬥                            |
|  ◇   | {data}`~OTHER_SHELLS`       | Other shells                                         | {func}`~is_other_shells`     |                           ⬥                            |
|  ⚡  | {data}`~POWERPC`            | PowerPC family                                       | {func}`~is_powerpc`          |                           ⬥                            |
|  Ⅴ   | {data}`~RISCV`              | RISC-V family                                        | {func}`~is_riscv`            |                           ⬥                            |
|  𝐕   | {data}`~SYSTEM_V`           | AT&T System Five                                     | {func}`~is_system_v`         |                           ⬥                            |
|  ⨷   | {data}`~UNIX`               | All Unix                                             | {func}`~is_unix`             |                                                        |
|  ≛   | {data}`~UNIX_LAYERS`        | Unix compatibility layers                            | {func}`~is_unix_layers`      |                           ⬥                            |
|  ⨂   | {data}`~UNIX_WITHOUT_MACOS` | All Unix excluding macOS                             | {func}`~is_unix_not_macos`   |                                                        |
|  ❓  | {data}`~UNKNOWN`            | Unknown                                              | {func}`~is_unknown`          |                           ⬥                            |
|  🌐  | {data}`~WEBASSEMBLY`        | WebAssembly                                          | {func}`~is_webassembly`      |                           ⬥                            |
|  ⌨️  | {data}`~WINDOWS_SHELLS`     | Windows shells                                       | {func}`~is_windows_shells`   |                           ⬥                            |
|  𝘅   | {data}`~X86`                | x86 family                                           | {func}`~is_x86`              |                           ⬥                            |

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
.. autodata:: extra_platforms.ALL_SHELLS
.. autodata:: extra_platforms.ALL_SPARC
.. autodata:: extra_platforms.ALL_TRAITS
.. autodata:: extra_platforms.ALL_WINDOWS
.. autodata:: extra_platforms.ARCH_32_BIT
.. autodata:: extra_platforms.ARCH_64_BIT
.. autodata:: extra_platforms.BIG_ENDIAN
.. autodata:: extra_platforms.BOURNE_SHELLS
.. autodata:: extra_platforms.BSD
.. autodata:: extra_platforms.BSD_WITHOUT_MACOS
.. autodata:: extra_platforms.C_SHELLS
.. autodata:: extra_platforms.IBM_MAINFRAME
.. autodata:: extra_platforms.LINUX
.. autodata:: extra_platforms.LINUX_LAYERS
.. autodata:: extra_platforms.LINUX_LIKE
.. autodata:: extra_platforms.LITTLE_ENDIAN
.. autodata:: extra_platforms.LOONGARCH
.. autodata:: extra_platforms.OTHER_POSIX
.. autodata:: extra_platforms.OTHER_SHELLS
.. autodata:: extra_platforms.POWERPC
.. autodata:: extra_platforms.RISCV
.. autodata:: extra_platforms.SYSTEM_V
.. autodata:: extra_platforms.UNIX
.. autodata:: extra_platforms.UNIX_LAYERS
.. autodata:: extra_platforms.UNIX_WITHOUT_MACOS
.. autodata:: extra_platforms.UNKNOWN
.. autodata:: extra_platforms.WEBASSEMBLY
.. autodata:: extra_platforms.WINDOWS_SHELLS
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
   :exclude-members: ALL_ARCHITECTURES, ALL_ARCHITECTURE_GROUPS, ALL_ARM, ALL_CI, ALL_CI_GROUPS, ALL_GROUPS, ALL_GROUP_IDS, ALL_IDS, ALL_MIPS, ALL_PLATFORMS, ALL_PLATFORM_GROUPS, ALL_SHELLS, ALL_SHELL_GROUPS, ALL_SPARC, ALL_TRAITS, ALL_TRAIT_IDS, ALL_WINDOWS, ARCH_32_BIT, ARCH_64_BIT, BIG_ENDIAN, BOURNE_SHELLS, BSD, BSD_WITHOUT_MACOS, C_SHELLS, EXTRA_GROUPS, IBM_MAINFRAME, LINUX, LINUX_LAYERS, LINUX_LIKE, LITTLE_ENDIAN, LOONGARCH, NON_OVERLAPPING_GROUPS, OTHER_POSIX, OTHER_SHELLS, POWERPC, RISCV, SYSTEM_V, UNIX, UNIX_LAYERS, UNIX_WITHOUT_MACOS, UNKNOWN, WEBASSEMBLY, WINDOWS_SHELLS, X86
```

<!-- group-data-module-automodule-end -->
