# {octicon}`tag` Traits

All aspects of a system are represented as *traits*.

There are three main types of traits:

- **[Architectures](architectures.md)**: CPU architectures (e.g., x86_64, ARM64)
- **[Platforms](platforms.md)**: Operating systems (e.g., Windows, macOS, Ubuntu)
- **[CI systems](ci.md)**: Continuous Integration environments (e.g., GitHub Actions, Travis CI)

## Trait usage

### Current traits

You can get all currently detected traits via the [`current_traits()`](detection.md#extra_platforms.current_traits) function.

```pycon
>>> from extra_platforms import current_traits
>>> current_traits()
{
   Architecture(id='aarch64', name='ARM64 (AArch64)'),
   Platform(id='macos', name='macOS'),
   CI(id='github_ci', name='GitHub Actions runner'),
}
```

This function returns a set of all [predefined traits](#all-traits) that match the current system.

Other current traits can be specifically checked via their dedicated [`current_*()` functions](detection.md#current-trait-functions):

```pycon
>>> from extra_platforms import current_architectures, current_platforms, current_ci
>>> current_architectures()
{Architecture(id='aarch64', name='ARM64 (AArch64)')}
>>> current_platforms()
{Platform(id='macos', name='macOS')}
>>> current_ci()
{CI(id='github_ci', name='GitHub Actions runner')}
```

### Predefined traits

All traits are available at the root of the `extra_platforms` package, as an uppercase symbol:

```pycon
>>> from extra_platforms import X86_64  # import an architecture
>>> X86_64
Architecture(id='x86_64', name='x86-64 (AMD64)')
>>> from extra_platforms import DEBIAN  # import a platform
>>> DEBIAN
Platform(id='debian', name='Debian')
>>> from extra_platforms import GITHUB_CI  # import a CI system
>>> GITHUB_CI
CI(id='github_ci', name='GitHub Actions runner')
```

They all inherit from the [`Trait` base class](#extra_platforms.trait.Trait), and share a common interface.

### Current property

Each trait has a [`current` property](#extra_platforms.trait.Trait.current) that calls the corresponding [detection function](detection.md):

```pycon
>>> X86_64.current
True
>>> DEBIAN.current
False
>>> GITHUB_CI.current
False
```

### Detection functions

Each trait is associated with a [detection function](detection.md), which returns `True` if the current system matches that trait.

These functions are also exposed at the root of the `extra_platforms` package:

```pycon
>>> from extra_platforms import is_x86_64, is_debian, is_github_ci
>>> is_x86_64()
True
>>> is_debian()
False
>>> is_github_ci()
False
```

### Groups

Traits are combined into [groups](groups.md) for easier detection of related traits.

You can get all groups a trait belongs to via the [`groups` property](#extra_platforms.trait.Trait.groups):

```pycon
>>> X86_64.groups
frozenset({
   Group(id='x86', name='x86 family'),
   Group(id='all_architectures', name='All architectures'),
   Group(id='arch_64_bit', name='64-bit architectures'),
   Group(id='all_traits', name='Any architectures, platforms and CI systems')})
```

### Additional information

Each trait provides an [`info()` method](#extra_platforms.trait.Trait.info) that returns a dictionary containing all available metadata about that trait:

```pycon
>>> from extra_platforms import AARCH64, MACOS
>>> AARCH64.info()
{'id': 'aarch64', 'name': 'ARM64 (AArch64)', 'icon': '📱', 'url': 'https://en.wikipedia.org/wiki/AArch64', 'current': True, 'machine': 'arm64', 'processor': None}
>>> MACOS.info()
{'id': 'macos', 'name': 'macOS', 'icon': '🍎', 'url': 'https://apple.com/macos/', 'current': True, 'distro_id': 'darwin', 'version': '26.2', 'version_parts': {'major': '26', 'minor': '2', 'build_number': None}, 'like': None, 'codename': 'Tahoe'}
```

The exact structure depends on the trait type.

## All traits

All recognized traits and their properties:

<!-- all-traits-table-start -->

| Icon | Symbol                                        | Name                           | Detection function                               | Type         |
| :--: | :-------------------------------------------- | :----------------------------- | :----------------------------------------------- | :----------- |
|  📱  | {data}`~extra_platforms.AARCH64`              | ARM64 (AArch64)                | {func}`~extra_platforms.is_aarch64`              | Architecture |
|  ➿  | {data}`~extra_platforms.AIX`                  | IBM AIX                        | {func}`~extra_platforms.is_aix`                  | Platform     |
|  🐧  | {data}`~extra_platforms.ALTLINUX`             | ALT Linux                      | {func}`~extra_platforms.is_altlinux`             | Platform     |
|  ⤻   | {data}`~extra_platforms.AMZN`                 | Amazon Linux                   | {func}`~extra_platforms.is_amzn`                 | Platform     |
|  🤖  | {data}`~extra_platforms.ANDROID`              | Android                        | {func}`~extra_platforms.is_android`              | Platform     |
|  🎗️  | {data}`~extra_platforms.ARCH`                 | Arch Linux                     | {func}`~extra_platforms.is_arch`                 | Platform     |
|  📱  | {data}`~extra_platforms.ARM`                  | ARM (32-bit)                   | {func}`~extra_platforms.is_arm`                  | Architecture |
|  📱  | {data}`~extra_platforms.ARMV5TEL`             | ARMv5TE (little-endian)        | {func}`~extra_platforms.is_armv5tel`             | Architecture |
|  📱  | {data}`~extra_platforms.ARMV6L`               | ARMv6 (little-endian)          | {func}`~extra_platforms.is_armv6l`               | Architecture |
|  📱  | {data}`~extra_platforms.ARMV7L`               | ARMv7 (little-endian)          | {func}`~extra_platforms.is_armv7l`               | Architecture |
|  📱  | {data}`~extra_platforms.ARMV8L`               | ARMv8 (32-bit, little-endian)  | {func}`~extra_platforms.is_armv8l`               | Architecture |
|  ═   | {data}`~extra_platforms.AZURE_PIPELINES`      | Azure Pipelines                | {func}`~extra_platforms.is_azure_pipelines`      | CI           |
|  ⟲   | {data}`~extra_platforms.BAMBOO`               | Bamboo                         | {func}`~extra_platforms.is_bamboo`               | CI           |
|  🪁  | {data}`~extra_platforms.BUILDKITE`            | Buildkite                      | {func}`~extra_platforms.is_buildkite`            | CI           |
|  ⛑️  | {data}`~extra_platforms.BUILDROOT`            | Buildroot                      | {func}`~extra_platforms.is_buildroot`            | Platform     |
|  ⌬   | {data}`~extra_platforms.CACHYOS`              | CachyOS                        | {func}`~extra_platforms.is_cachyos`              | Platform     |
|  💠  | {data}`~extra_platforms.CENTOS`               | CentOS                         | {func}`~extra_platforms.is_centos`               | Platform     |
|  ⪾   | {data}`~extra_platforms.CIRCLE_CI`            | Circle CI                      | {func}`~extra_platforms.is_circle_ci`            | CI           |
|  ≋   | {data}`~extra_platforms.CIRRUS_CI`            | Cirrus CI                      | {func}`~extra_platforms.is_cirrus_ci`            | CI           |
|  ꩜   | {data}`~extra_platforms.CLOUDLINUX`           | CloudLinux OS                  | {func}`~extra_platforms.is_cloudlinux`           | Platform     |
|  ᚙ   | {data}`~extra_platforms.CODEBUILD`            | CodeBuild                      | {func}`~extra_platforms.is_codebuild`            | CI           |
|  Ͼ   | {data}`~extra_platforms.CYGWIN`               | Cygwin                         | {func}`~extra_platforms.is_cygwin`               | Platform     |
|  🌀  | {data}`~extra_platforms.DEBIAN`               | Debian                         | {func}`~extra_platforms.is_debian`               | Platform     |
|  🪰  | {data}`~extra_platforms.DRAGONFLY_BSD`        | DragonFly BSD                  | {func}`~extra_platforms.is_dragonfly_bsd`        | Platform     |
|  🐽  | {data}`~extra_platforms.EXHERBO`              | Exherbo Linux                  | {func}`~extra_platforms.is_exherbo`              | Platform     |
|  🎩  | {data}`~extra_platforms.FEDORA`               | Fedora                         | {func}`~extra_platforms.is_fedora`               | Platform     |
|  😈  | {data}`~extra_platforms.FREEBSD`              | FreeBSD                        | {func}`~extra_platforms.is_freebsd`              | Platform     |
|  🗜️  | {data}`~extra_platforms.GENTOO`               | Gentoo Linux                   | {func}`~extra_platforms.is_gentoo`               | Platform     |
|  🐙  | {data}`~extra_platforms.GITHUB_CI`            | GitHub Actions runner          | {func}`~extra_platforms.is_github_ci`            | CI           |
|  🦊  | {data}`~extra_platforms.GITLAB_CI`            | GitLab CI                      | {func}`~extra_platforms.is_gitlab_ci`            | CI           |
|  🐃  | {data}`~extra_platforms.GUIX`                 | Guix System                    | {func}`~extra_platforms.is_guix`                 | Platform     |
|  🍂  | {data}`~extra_platforms.HAIKU`                | Haiku                          | {func}`~extra_platforms.is_haiku`                | Platform     |
|  ⥁   | {data}`~extra_platforms.HEROKU_CI`            | Heroku CI                      | {func}`~extra_platforms.is_heroku_ci`            | CI           |
|  🐃  | {data}`~extra_platforms.HURD`                 | GNU/Hurd                       | {func}`~extra_platforms.is_hurd`                 | Platform     |
|  𝗶   | {data}`~extra_platforms.I386`                 | Intel 80386 (i386)             | {func}`~extra_platforms.is_i386`                 | Architecture |
|  𝗶   | {data}`~extra_platforms.I586`                 | Intel Pentium (i586)           | {func}`~extra_platforms.is_i586`                 | Architecture |
|  𝗶   | {data}`~extra_platforms.I686`                 | Intel Pentium Pro (i686)       | {func}`~extra_platforms.is_i686`                 | Architecture |
|  🤹  | {data}`~extra_platforms.IBM_POWERKVM`         | IBM PowerKVM                   | {func}`~extra_platforms.is_ibm_powerkvm`         | Platform     |
|  🔥  | {data}`~extra_platforms.ILLUMOS`              | illumos                        | {func}`~extra_platforms.is_illumos`              | Platform     |
|  🤹  | {data}`~extra_platforms.KVMIBM`               | KVM for IBM z Systems          | {func}`~extra_platforms.is_kvmibm`               | Platform     |
|  🌿  | {data}`~extra_platforms.LINUXMINT`            | Linux Mint                     | {func}`~extra_platforms.is_linuxmint`            | Platform     |
|  🐉  | {data}`~extra_platforms.LOONGARCH64`          | LoongArch (64-bit)             | {func}`~extra_platforms.is_loongarch64`          | Architecture |
|  🍎  | {data}`~extra_platforms.MACOS`                | macOS                          | {func}`~extra_platforms.is_macos`                | Platform     |
|  ⍥   | {data}`~extra_platforms.MAGEIA`               | Mageia                         | {func}`~extra_platforms.is_mageia`               | Platform     |
|  💫  | {data}`~extra_platforms.MANDRIVA`             | Mandriva Linux                 | {func}`~extra_platforms.is_mandriva`             | Platform     |
|  🌘  | {data}`~extra_platforms.MIDNIGHTBSD`          | MidnightBSD                    | {func}`~extra_platforms.is_midnightbsd`          | Platform     |
|  🔲  | {data}`~extra_platforms.MIPS`                 | MIPS (32-bit, big-endian)      | {func}`~extra_platforms.is_mips`                 | Architecture |
|  🔲  | {data}`~extra_platforms.MIPS64`               | MIPS64 (big-endian)            | {func}`~extra_platforms.is_mips64`               | Architecture |
|  🔲  | {data}`~extra_platforms.MIPS64EL`             | MIPS64 (little-endian)         | {func}`~extra_platforms.is_mips64el`             | Architecture |
|  🔲  | {data}`~extra_platforms.MIPSEL`               | MIPS (32-bit, little-endian)   | {func}`~extra_platforms.is_mipsel`               | Architecture |
|  🚩  | {data}`~extra_platforms.NETBSD`               | NetBSD                         | {func}`~extra_platforms.is_netbsd`               | Platform     |
|     | {data}`~extra_platforms.NOBARA`               | Nobara                         | {func}`~extra_platforms.is_nobara`               | Platform     |
|  🐡  | {data}`~extra_platforms.OPENBSD`              | OpenBSD                        | {func}`~extra_platforms.is_openbsd`              | Platform     |
|  🦎  | {data}`~extra_platforms.OPENSUSE`             | openSUSE                       | {func}`~extra_platforms.is_opensuse`             | Platform     |
|  🦴  | {data}`~extra_platforms.ORACLE`               | Oracle Linux                   | {func}`~extra_platforms.is_oracle`               | Platform     |
|  ∥   | {data}`~extra_platforms.PARALLELS`            | Parallels                      | {func}`~extra_platforms.is_parallels`            | Platform     |
|  🍓  | {data}`~extra_platforms.PIDORA`               | Pidora                         | {func}`~extra_platforms.is_pidora`               | Platform     |
|  ⚡  | {data}`~extra_platforms.PPC`                  | PowerPC (32-bit)               | {func}`~extra_platforms.is_ppc`                  | Architecture |
|  ⚡  | {data}`~extra_platforms.PPC64`                | PowerPC 64-bit (big-endian)    | {func}`~extra_platforms.is_ppc64`                | Architecture |
|  ⚡  | {data}`~extra_platforms.PPC64LE`              | PowerPC 64-bit (little-endian) | {func}`~extra_platforms.is_ppc64le`              | Architecture |
|  🍓  | {data}`~extra_platforms.RASPBIAN`             | Raspbian                       | {func}`~extra_platforms.is_raspbian`             | Platform     |
|  🎩  | {data}`~extra_platforms.RHEL`                 | RedHat Enterprise Linux        | {func}`~extra_platforms.is_rhel`                 | Platform     |
|  Ⅴ   | {data}`~extra_platforms.RISCV32`              | RISC-V (32-bit)                | {func}`~extra_platforms.is_riscv32`              | Architecture |
|  Ⅴ   | {data}`~extra_platforms.RISCV64`              | RISC-V (64-bit)                | {func}`~extra_platforms.is_riscv64`              | Architecture |
|  ⛰️  | {data}`~extra_platforms.ROCKY`                | Rocky Linux                    | {func}`~extra_platforms.is_rocky`                | Platform     |
|  🏢  | {data}`~extra_platforms.S390X`                | IBM z/Architecture (s390x)     | {func}`~extra_platforms.is_s390x`                | Architecture |
|  ⚛️  | {data}`~extra_platforms.SCIENTIFIC`           | Scientific Linux               | {func}`~extra_platforms.is_scientific`           | Platform     |
|  🚬  | {data}`~extra_platforms.SLACKWARE`            | Slackware                      | {func}`~extra_platforms.is_slackware`            | Platform     |
|  🦎  | {data}`~extra_platforms.SLES`                 | SUSE Linux Enterprise Server   | {func}`~extra_platforms.is_sles`                 | Platform     |
|  🌞  | {data}`~extra_platforms.SOLARIS`              | Solaris                        | {func}`~extra_platforms.is_solaris`              | Platform     |
|  ☀️  | {data}`~extra_platforms.SPARC`                | SPARC (32-bit)                 | {func}`~extra_platforms.is_sparc`                | Architecture |
|  ☀️  | {data}`~extra_platforms.SPARC64`              | SPARC (64-bit)                 | {func}`~extra_platforms.is_sparc64`              | Architecture |
|  ☀️  | {data}`~extra_platforms.SUNOS`                | SunOS                          | {func}`~extra_platforms.is_sunos`                | Platform     |
|  🏙️  | {data}`~extra_platforms.TEAMCITY`             | TeamCity                       | {func}`~extra_platforms.is_teamcity`             | CI           |
|  👷  | {data}`~extra_platforms.TRAVIS_CI`            | Travis CI                      | {func}`~extra_platforms.is_travis_ci`            | CI           |
|  ↻   | {data}`~extra_platforms.TUMBLEWEED`           | openSUSE Tumbleweed            | {func}`~extra_platforms.is_tumbleweed`           | Platform     |
|  🤵  | {data}`~extra_platforms.TUXEDO`               | Tuxedo OS                      | {func}`~extra_platforms.is_tuxedo`               | Platform     |
|  🎯  | {data}`~extra_platforms.UBUNTU`               | Ubuntu                         | {func}`~extra_platforms.is_ubuntu`               | Platform     |
|  🌊  | {data}`~extra_platforms.ULTRAMARINE`          | Ultramarine                    | {func}`~extra_platforms.is_ultramarine`          | Platform     |
|  ❓  | {data}`~extra_platforms.UNKNOWN_ARCHITECTURE` | Unknown architecture           | {func}`~extra_platforms.is_unknown_architecture` | Architecture |
|  ❓  | {data}`~extra_platforms.UNKNOWN_CI`           | Unknown CI                     | {func}`~extra_platforms.is_unknown_ci`           | CI           |
|  ❓  | {data}`~extra_platforms.UNKNOWN_PLATFORM`     | Unknown platform               | {func}`~extra_platforms.is_unknown_platform`     | Platform     |
|  🌐  | {data}`~extra_platforms.WASM32`               | WebAssembly (32-bit)           | {func}`~extra_platforms.is_wasm32`               | Architecture |
|  🌐  | {data}`~extra_platforms.WASM64`               | WebAssembly (64-bit)           | {func}`~extra_platforms.is_wasm64`               | Architecture |
|  🪟  | {data}`~extra_platforms.WINDOWS`              | Windows                        | {func}`~extra_platforms.is_windows`              | Platform     |
|  ⊞   | {data}`~extra_platforms.WSL1`                 | Windows Subsystem for Linux v1 | {func}`~extra_platforms.is_wsl1`                 | Platform     |
|  ⊞   | {data}`~extra_platforms.WSL2`                 | Windows Subsystem for Linux v2 | {func}`~extra_platforms.is_wsl2`                 | Platform     |
|  🖥️  | {data}`~extra_platforms.X86_64`               | x86-64 (AMD64)                 | {func}`~extra_platforms.is_x86_64`               | Architecture |
|  Ⓧ   | {data}`~extra_platforms.XENSERVER`            | XenServer                      | {func}`~extra_platforms.is_xenserver`            | Platform     |

<!-- all-traits-table-end -->

## Trait implementation

```{eval-rst}
.. autoclasstree:: extra_platforms.trait
   :strict:
```

```{eval-rst}
.. autoclass:: extra_platforms.Trait
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Platform
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Architecture
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.CI
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:
```
