# {octicon}`tag` Traits

All aspects of a system are represented as *traits*.

There are three main types of traits:

- **[Architectures](architectures.md)**: CPU architectures (e.g., x86_64, ARM64)
- **[Platforms](platforms.md)**: Operating systems (e.g., Windows, macOS, Ubuntu)
- **[CI systems](ci.md)**: Continuous Integration environments (e.g., GitHub Actions, Travis CI)

## Trait usage

### Current traits

You can get all currently detected traits via the [`current_traits()` function](detection.md#extra_platforms.current_traits).

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

Other current traits can be specifically checked via their dedicated `current_*()` functions:

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

| Icon | Symbol                                                                          | Name                           | Detection function                                                                  | Type         |
| :--: | :------------------------------------------------------------------------------ | :----------------------------- | :---------------------------------------------------------------------------------- | :----------- |
|  📱  | [`AARCH64`](architectures.md#extra_platforms.AARCH64)                           | ARM64 (AArch64)                | [`is_aarch64()`](detection.md#extra_platforms.is_aarch64)                           | Architecture |
|  ➿  | [`AIX`](platforms.md#extra_platforms.AIX)                                       | IBM AIX                        | [`is_aix()`](detection.md#extra_platforms.is_aix)                                   | Platform     |
|  🐧  | [`ALTLINUX`](platforms.md#extra_platforms.ALTLINUX)                             | ALT Linux                      | [`is_altlinux()`](detection.md#extra_platforms.is_altlinux)                         | Platform     |
|  ⤻   | [`AMZN`](platforms.md#extra_platforms.AMZN)                                     | Amazon Linux                   | [`is_amzn()`](detection.md#extra_platforms.is_amzn)                                 | Platform     |
|  🤖  | [`ANDROID`](platforms.md#extra_platforms.ANDROID)                               | Android                        | [`is_android()`](detection.md#extra_platforms.is_android)                           | Platform     |
|  🎗️  | [`ARCH`](platforms.md#extra_platforms.ARCH)                                     | Arch Linux                     | [`is_arch()`](detection.md#extra_platforms.is_arch)                                 | Platform     |
|  📱  | [`ARM`](architectures.md#extra_platforms.ARM)                                   | ARM (32-bit)                   | [`is_arm()`](detection.md#extra_platforms.is_arm)                                   | Architecture |
|  📱  | [`ARMV5TEL`](architectures.md#extra_platforms.ARMV5TEL)                         | ARMv5TE (little-endian)        | [`is_armv5tel()`](detection.md#extra_platforms.is_armv5tel)                         | Architecture |
|  📱  | [`ARMV6L`](architectures.md#extra_platforms.ARMV6L)                             | ARMv6 (little-endian)          | [`is_armv6l()`](detection.md#extra_platforms.is_armv6l)                             | Architecture |
|  📱  | [`ARMV7L`](architectures.md#extra_platforms.ARMV7L)                             | ARMv7 (little-endian)          | [`is_armv7l()`](detection.md#extra_platforms.is_armv7l)                             | Architecture |
|  📱  | [`ARMV8L`](architectures.md#extra_platforms.ARMV8L)                             | ARMv8 (32-bit, little-endian)  | [`is_armv8l()`](detection.md#extra_platforms.is_armv8l)                             | Architecture |
|  ═   | [`AZURE_PIPELINES`](ci.md#extra_platforms.AZURE_PIPELINES)                      | Azure Pipelines                | [`is_azure_pipelines()`](detection.md#extra_platforms.is_azure_pipelines)           | CI           |
|  ⟲   | [`BAMBOO`](ci.md#extra_platforms.BAMBOO)                                        | Bamboo                         | [`is_bamboo()`](detection.md#extra_platforms.is_bamboo)                             | CI           |
|  🪁  | [`BUILDKITE`](ci.md#extra_platforms.BUILDKITE)                                  | Buildkite                      | [`is_buildkite()`](detection.md#extra_platforms.is_buildkite)                       | CI           |
|  ⛑️  | [`BUILDROOT`](platforms.md#extra_platforms.BUILDROOT)                           | Buildroot                      | [`is_buildroot()`](detection.md#extra_platforms.is_buildroot)                       | Platform     |
|  ⌬   | [`CACHYOS`](platforms.md#extra_platforms.CACHYOS)                               | CachyOS                        | [`is_cachyos()`](detection.md#extra_platforms.is_cachyos)                           | Platform     |
|  💠  | [`CENTOS`](platforms.md#extra_platforms.CENTOS)                                 | CentOS                         | [`is_centos()`](detection.md#extra_platforms.is_centos)                             | Platform     |
|  ⪾   | [`CIRCLE_CI`](ci.md#extra_platforms.CIRCLE_CI)                                  | Circle CI                      | [`is_circle_ci()`](detection.md#extra_platforms.is_circle_ci)                       | CI           |
|  ≋   | [`CIRRUS_CI`](ci.md#extra_platforms.CIRRUS_CI)                                  | Cirrus CI                      | [`is_cirrus_ci()`](detection.md#extra_platforms.is_cirrus_ci)                       | CI           |
|  ꩜   | [`CLOUDLINUX`](platforms.md#extra_platforms.CLOUDLINUX)                         | CloudLinux OS                  | [`is_cloudlinux()`](detection.md#extra_platforms.is_cloudlinux)                     | Platform     |
|  ᚙ   | [`CODEBUILD`](ci.md#extra_platforms.CODEBUILD)                                  | CodeBuild                      | [`is_codebuild()`](detection.md#extra_platforms.is_codebuild)                       | CI           |
|  Ͼ   | [`CYGWIN`](platforms.md#extra_platforms.CYGWIN)                                 | Cygwin                         | [`is_cygwin()`](detection.md#extra_platforms.is_cygwin)                             | Platform     |
|  🌀  | [`DEBIAN`](platforms.md#extra_platforms.DEBIAN)                                 | Debian                         | [`is_debian()`](detection.md#extra_platforms.is_debian)                             | Platform     |
|  🐽  | [`EXHERBO`](platforms.md#extra_platforms.EXHERBO)                               | Exherbo Linux                  | [`is_exherbo()`](detection.md#extra_platforms.is_exherbo)                           | Platform     |
|  🎩  | [`FEDORA`](platforms.md#extra_platforms.FEDORA)                                 | Fedora                         | [`is_fedora()`](detection.md#extra_platforms.is_fedora)                             | Platform     |
|  😈  | [`FREEBSD`](platforms.md#extra_platforms.FREEBSD)                               | FreeBSD                        | [`is_freebsd()`](detection.md#extra_platforms.is_freebsd)                           | Platform     |
|  🗜️  | [`GENTOO`](platforms.md#extra_platforms.GENTOO)                                 | Gentoo Linux                   | [`is_gentoo()`](detection.md#extra_platforms.is_gentoo)                             | Platform     |
|  🐙  | [`GITHUB_CI`](ci.md#extra_platforms.GITHUB_CI)                                  | GitHub Actions runner          | [`is_github_ci()`](detection.md#extra_platforms.is_github_ci)                       | CI           |
|  🦊  | [`GITLAB_CI`](ci.md#extra_platforms.GITLAB_CI)                                  | GitLab CI                      | [`is_gitlab_ci()`](detection.md#extra_platforms.is_gitlab_ci)                       | CI           |
|  🐃  | [`GUIX`](platforms.md#extra_platforms.GUIX)                                     | Guix System                    | [`is_guix()`](detection.md#extra_platforms.is_guix)                                 | Platform     |
|  ⥁   | [`HEROKU_CI`](ci.md#extra_platforms.HEROKU_CI)                                  | Heroku CI                      | [`is_heroku_ci()`](detection.md#extra_platforms.is_heroku_ci)                       | CI           |
|  🐃  | [`HURD`](platforms.md#extra_platforms.HURD)                                     | GNU/Hurd                       | [`is_hurd()`](detection.md#extra_platforms.is_hurd)                                 | Platform     |
|  𝗶   | [`I386`](architectures.md#extra_platforms.I386)                                 | Intel 80386 (i386)             | [`is_i386()`](detection.md#extra_platforms.is_i386)                                 | Architecture |
|  𝗶   | [`I586`](architectures.md#extra_platforms.I586)                                 | Intel Pentium (i586)           | [`is_i586()`](detection.md#extra_platforms.is_i586)                                 | Architecture |
|  𝗶   | [`I686`](architectures.md#extra_platforms.I686)                                 | Intel Pentium Pro (i686)       | [`is_i686()`](detection.md#extra_platforms.is_i686)                                 | Architecture |
|  🤹  | [`IBM_POWERKVM`](platforms.md#extra_platforms.IBM_POWERKVM)                     | IBM PowerKVM                   | [`is_ibm_powerkvm()`](detection.md#extra_platforms.is_ibm_powerkvm)                 | Platform     |
|  🤹  | [`KVMIBM`](platforms.md#extra_platforms.KVMIBM)                                 | KVM for IBM z Systems          | [`is_kvmibm()`](detection.md#extra_platforms.is_kvmibm)                             | Platform     |
|  🌿  | [`LINUXMINT`](platforms.md#extra_platforms.LINUXMINT)                           | Linux Mint                     | [`is_linuxmint()`](detection.md#extra_platforms.is_linuxmint)                       | Platform     |
|  🐉  | [`LOONGARCH64`](architectures.md#extra_platforms.LOONGARCH64)                   | LoongArch (64-bit)             | [`is_loongarch64()`](detection.md#extra_platforms.is_loongarch64)                   | Architecture |
|  🍎  | [`MACOS`](platforms.md#extra_platforms.MACOS)                                   | macOS                          | [`is_macos()`](detection.md#extra_platforms.is_macos)                               | Platform     |
|  ⍥   | [`MAGEIA`](platforms.md#extra_platforms.MAGEIA)                                 | Mageia                         | [`is_mageia()`](detection.md#extra_platforms.is_mageia)                             | Platform     |
|  💫  | [`MANDRIVA`](platforms.md#extra_platforms.MANDRIVA)                             | Mandriva Linux                 | [`is_mandriva()`](detection.md#extra_platforms.is_mandriva)                         | Platform     |
|  🌘  | [`MIDNIGHTBSD`](platforms.md#extra_platforms.MIDNIGHTBSD)                       | MidnightBSD                    | [`is_midnightbsd()`](detection.md#extra_platforms.is_midnightbsd)                   | Platform     |
|  🔲  | [`MIPS`](architectures.md#extra_platforms.MIPS)                                 | MIPS (32-bit, big-endian)      | [`is_mips()`](detection.md#extra_platforms.is_mips)                                 | Architecture |
|  🔲  | [`MIPS64`](architectures.md#extra_platforms.MIPS64)                             | MIPS64 (big-endian)            | [`is_mips64()`](detection.md#extra_platforms.is_mips64)                             | Architecture |
|  🔲  | [`MIPS64EL`](architectures.md#extra_platforms.MIPS64EL)                         | MIPS64 (little-endian)         | [`is_mips64el()`](detection.md#extra_platforms.is_mips64el)                         | Architecture |
|  🔲  | [`MIPSEL`](architectures.md#extra_platforms.MIPSEL)                             | MIPS (32-bit, little-endian)   | [`is_mipsel()`](detection.md#extra_platforms.is_mipsel)                             | Architecture |
|  🚩  | [`NETBSD`](platforms.md#extra_platforms.NETBSD)                                 | NetBSD                         | [`is_netbsd()`](detection.md#extra_platforms.is_netbsd)                             | Platform     |
|     | [`NOBARA`](platforms.md#extra_platforms.NOBARA)                                 | Nobara                         | [`is_nobara()`](detection.md#extra_platforms.is_nobara)                             | Platform     |
|  🐡  | [`OPENBSD`](platforms.md#extra_platforms.OPENBSD)                               | OpenBSD                        | [`is_openbsd()`](detection.md#extra_platforms.is_openbsd)                           | Platform     |
|  🦎  | [`OPENSUSE`](platforms.md#extra_platforms.OPENSUSE)                             | openSUSE                       | [`is_opensuse()`](detection.md#extra_platforms.is_opensuse)                         | Platform     |
|  🦴  | [`ORACLE`](platforms.md#extra_platforms.ORACLE)                                 | Oracle Linux                   | [`is_oracle()`](detection.md#extra_platforms.is_oracle)                             | Platform     |
|  ∥   | [`PARALLELS`](platforms.md#extra_platforms.PARALLELS)                           | Parallels                      | [`is_parallels()`](detection.md#extra_platforms.is_parallels)                       | Platform     |
|  🍓  | [`PIDORA`](platforms.md#extra_platforms.PIDORA)                                 | Pidora                         | [`is_pidora()`](detection.md#extra_platforms.is_pidora)                             | Platform     |
|  ⚡  | [`PPC`](architectures.md#extra_platforms.PPC)                                   | PowerPC (32-bit)               | [`is_ppc()`](detection.md#extra_platforms.is_ppc)                                   | Architecture |
|  ⚡  | [`PPC64`](architectures.md#extra_platforms.PPC64)                               | PowerPC 64-bit (big-endian)    | [`is_ppc64()`](detection.md#extra_platforms.is_ppc64)                               | Architecture |
|  ⚡  | [`PPC64LE`](architectures.md#extra_platforms.PPC64LE)                           | PowerPC 64-bit (little-endian) | [`is_ppc64le()`](detection.md#extra_platforms.is_ppc64le)                           | Architecture |
|  🍓  | [`RASPBIAN`](platforms.md#extra_platforms.RASPBIAN)                             | Raspbian                       | [`is_raspbian()`](detection.md#extra_platforms.is_raspbian)                         | Platform     |
|  🎩  | [`RHEL`](platforms.md#extra_platforms.RHEL)                                     | RedHat Enterprise Linux        | [`is_rhel()`](detection.md#extra_platforms.is_rhel)                                 | Platform     |
|  Ⅴ   | [`RISCV32`](architectures.md#extra_platforms.RISCV32)                           | RISC-V (32-bit)                | [`is_riscv32()`](detection.md#extra_platforms.is_riscv32)                           | Architecture |
|  Ⅴ   | [`RISCV64`](architectures.md#extra_platforms.RISCV64)                           | RISC-V (64-bit)                | [`is_riscv64()`](detection.md#extra_platforms.is_riscv64)                           | Architecture |
|  ⛰️  | [`ROCKY`](platforms.md#extra_platforms.ROCKY)                                   | Rocky Linux                    | [`is_rocky()`](detection.md#extra_platforms.is_rocky)                               | Platform     |
|  🏢  | [`S390X`](architectures.md#extra_platforms.S390X)                               | IBM z/Architecture (s390x)     | [`is_s390x()`](detection.md#extra_platforms.is_s390x)                               | Architecture |
|  ⚛️  | [`SCIENTIFIC`](platforms.md#extra_platforms.SCIENTIFIC)                         | Scientific Linux               | [`is_scientific()`](detection.md#extra_platforms.is_scientific)                     | Platform     |
|  🚬  | [`SLACKWARE`](platforms.md#extra_platforms.SLACKWARE)                           | Slackware                      | [`is_slackware()`](detection.md#extra_platforms.is_slackware)                       | Platform     |
|  🦎  | [`SLES`](platforms.md#extra_platforms.SLES)                                     | SUSE Linux Enterprise Server   | [`is_sles()`](detection.md#extra_platforms.is_sles)                                 | Platform     |
|  🌞  | [`SOLARIS`](platforms.md#extra_platforms.SOLARIS)                               | Solaris                        | [`is_solaris()`](detection.md#extra_platforms.is_solaris)                           | Platform     |
|  ☀️  | [`SPARC`](architectures.md#extra_platforms.SPARC)                               | SPARC (32-bit)                 | [`is_sparc()`](detection.md#extra_platforms.is_sparc)                               | Architecture |
|  ☀️  | [`SPARC64`](architectures.md#extra_platforms.SPARC64)                           | SPARC (64-bit)                 | [`is_sparc64()`](detection.md#extra_platforms.is_sparc64)                           | Architecture |
|  ☀️  | [`SUNOS`](platforms.md#extra_platforms.SUNOS)                                   | SunOS                          | [`is_sunos()`](detection.md#extra_platforms.is_sunos)                               | Platform     |
|  🏙️  | [`TEAMCITY`](ci.md#extra_platforms.TEAMCITY)                                    | TeamCity                       | [`is_teamcity()`](detection.md#extra_platforms.is_teamcity)                         | CI           |
|  👷  | [`TRAVIS_CI`](ci.md#extra_platforms.TRAVIS_CI)                                  | Travis CI                      | [`is_travis_ci()`](detection.md#extra_platforms.is_travis_ci)                       | CI           |
|  ↻   | [`TUMBLEWEED`](platforms.md#extra_platforms.TUMBLEWEED)                         | openSUSE Tumbleweed            | [`is_tumbleweed()`](detection.md#extra_platforms.is_tumbleweed)                     | Platform     |
|  🤵  | [`TUXEDO`](platforms.md#extra_platforms.TUXEDO)                                 | Tuxedo OS                      | [`is_tuxedo()`](detection.md#extra_platforms.is_tuxedo)                             | Platform     |
|  🎯  | [`UBUNTU`](platforms.md#extra_platforms.UBUNTU)                                 | Ubuntu                         | [`is_ubuntu()`](detection.md#extra_platforms.is_ubuntu)                             | Platform     |
|  🌊  | [`ULTRAMARINE`](platforms.md#extra_platforms.ULTRAMARINE)                       | Ultramarine                    | [`is_ultramarine()`](detection.md#extra_platforms.is_ultramarine)                   | Platform     |
|  ❓  | [`UNKNOWN_ARCHITECTURE`](architectures.md#extra_platforms.UNKNOWN_ARCHITECTURE) | Unknown architecture           | [`is_unknown_architecture()`](detection.md#extra_platforms.is_unknown_architecture) | Architecture |
|  ❓  | [`UNKNOWN_CI`](ci.md#extra_platforms.UNKNOWN_CI)                                | Unknown CI                     | [`is_unknown_ci()`](detection.md#extra_platforms.is_unknown_ci)                     | CI           |
|  ❓  | [`UNKNOWN_PLATFORM`](platforms.md#extra_platforms.UNKNOWN_PLATFORM)             | Unknown platform               | [`is_unknown_platform()`](detection.md#extra_platforms.is_unknown_platform)         | Platform     |
|  🌐  | [`WASM32`](architectures.md#extra_platforms.WASM32)                             | WebAssembly (32-bit)           | [`is_wasm32()`](detection.md#extra_platforms.is_wasm32)                             | Architecture |
|  🌐  | [`WASM64`](architectures.md#extra_platforms.WASM64)                             | WebAssembly (64-bit)           | [`is_wasm64()`](detection.md#extra_platforms.is_wasm64)                             | Architecture |
|  🪟  | [`WINDOWS`](platforms.md#extra_platforms.WINDOWS)                               | Windows                        | [`is_windows()`](detection.md#extra_platforms.is_windows)                           | Platform     |
|  ⊞   | [`WSL1`](platforms.md#extra_platforms.WSL1)                                     | Windows Subsystem for Linux v1 | [`is_wsl1()`](detection.md#extra_platforms.is_wsl1)                                 | Platform     |
|  ⊞   | [`WSL2`](platforms.md#extra_platforms.WSL2)                                     | Windows Subsystem for Linux v2 | [`is_wsl2()`](detection.md#extra_platforms.is_wsl2)                                 | Platform     |
|  🖥️  | [`X86_64`](architectures.md#extra_platforms.X86_64)                             | x86-64 (AMD64)                 | [`is_x86_64()`](detection.md#extra_platforms.is_x86_64)                             | Architecture |
|  Ⓧ   | [`XENSERVER`](platforms.md#extra_platforms.XENSERVER)                           | XenServer                      | [`is_xenserver()`](detection.md#extra_platforms.is_xenserver)                       | Platform     |

<!-- all-traits-table-end -->

## Trait details

All trait details and their properties are listed in their respective sections:
- [Architectures](architectures.md#architecture-details)
- [Platforms](platforms.md#platform-details)
- [CI systems](ci.md#ci-details)

## Trait implementation

```{eval-rst}
.. autoclasstree:: extra_platforms.trait
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.trait
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:
```
