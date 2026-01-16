# {octicon}`pulse` Detection

## All detection functions

<!-- all-detection-function-table-start -->

| Detection function                                                                  | Icon | Associated symbol                                                               |
| :---------------------------------------------------------------------------------- | :--: | :------------------------------------------------------------------------------ |
| [`is_aarch64()`](detection.md#extra_platforms.is_aarch64)                           |  📱  | [`AARCH64`](architectures.md#extra_platforms.AARCH64)                           |
| [`is_aix()`](detection.md#extra_platforms.is_aix)                                   |  ➿  | [`AIX`](platforms.md#extra_platforms.AIX)                                       |
| [`is_altlinux()`](detection.md#extra_platforms.is_altlinux)                         |  🐧  | [`ALTLINUX`](platforms.md#extra_platforms.ALTLINUX)                             |
| [`is_amzn()`](detection.md#extra_platforms.is_amzn)                                 |  ⤻   | [`AMZN`](platforms.md#extra_platforms.AMZN)                                     |
| [`is_android()`](detection.md#extra_platforms.is_android)                           |  🤖  | [`ANDROID`](platforms.md#extra_platforms.ANDROID)                               |
| [`is_any_architecture()`](detection.md#extra_platforms.is_any_architecture)         |  🏛️  | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.ALL_ARCHITECTURES)              |
| [`is_any_arm()`](detection.md#extra_platforms.is_any_arm)                           |  📱  | [`ALL_ARM`](groups.md#extra_platforms.ALL_ARM)                                  |
| [`is_any_ci()`](detection.md#extra_platforms.is_any_ci)                             |  ♺   | [`ALL_CI`](groups.md#extra_platforms.ALL_CI)                                    |
| [`is_any_mips()`](detection.md#extra_platforms.is_any_mips)                         |  🔲  | [`ALL_MIPS`](groups.md#extra_platforms.ALL_MIPS)                                |
| [`is_any_platform()`](detection.md#extra_platforms.is_any_platform)                 |  ⚙️  | [`ALL_PLATFORMS`](groups.md#extra_platforms.ALL_PLATFORMS)                      |
| [`is_any_sparc()`](detection.md#extra_platforms.is_any_sparc)                       |  ☀️  | [`ALL_SPARC`](groups.md#extra_platforms.ALL_SPARC)                              |
| [`is_any_trait()`](detection.md#extra_platforms.is_any_trait)                       |  ⁕   | [`ALL_TRAITS`](groups.md#extra_platforms.ALL_TRAITS)                            |
| [`is_any_windows()`](detection.md#extra_platforms.is_any_windows)                   |  🪟  | [`ALL_WINDOWS`](groups.md#extra_platforms.ALL_WINDOWS)                          |
| [`is_arch()`](detection.md#extra_platforms.is_arch)                                 |  🎗️  | [`ARCH`](platforms.md#extra_platforms.ARCH)                                     |
| [`is_arch_32_bit()`](detection.md#extra_platforms.is_arch_32_bit)                   |  ³²  | [`ARCH_32_BIT`](groups.md#extra_platforms.ARCH_32_BIT)                          |
| [`is_arch_64_bit()`](detection.md#extra_platforms.is_arch_64_bit)                   |  ⁶⁴  | [`ARCH_64_BIT`](groups.md#extra_platforms.ARCH_64_BIT)                          |
| [`is_arm()`](detection.md#extra_platforms.is_arm)                                   |  📱  | [`ARM`](architectures.md#extra_platforms.ARM)                                   |
| [`is_armv5tel()`](detection.md#extra_platforms.is_armv5tel)                         |  📱  | [`ARMV5TEL`](architectures.md#extra_platforms.ARMV5TEL)                         |
| [`is_armv6l()`](detection.md#extra_platforms.is_armv6l)                             |  📱  | [`ARMV6L`](architectures.md#extra_platforms.ARMV6L)                             |
| [`is_armv7l()`](detection.md#extra_platforms.is_armv7l)                             |  📱  | [`ARMV7L`](architectures.md#extra_platforms.ARMV7L)                             |
| [`is_armv8l()`](detection.md#extra_platforms.is_armv8l)                             |  📱  | [`ARMV8L`](architectures.md#extra_platforms.ARMV8L)                             |
| [`is_azure_pipelines()`](detection.md#extra_platforms.is_azure_pipelines)           |  ═   | [`AZURE_PIPELINES`](ci.md#extra_platforms.AZURE_PIPELINES)                      |
| [`is_bamboo()`](detection.md#extra_platforms.is_bamboo)                             |  ⟲   | [`BAMBOO`](ci.md#extra_platforms.BAMBOO)                                        |
| [`is_bsd()`](detection.md#extra_platforms.is_bsd)                                   | 🅱️+  | [`BSD`](groups.md#extra_platforms.BSD)                                          |
| [`is_bsd_without_macos()`](detection.md#extra_platforms.is_bsd_without_macos)       |  🅱️  | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.BSD_WITHOUT_MACOS)              |
| [`is_buildkite()`](detection.md#extra_platforms.is_buildkite)                       |  🪁  | [`BUILDKITE`](ci.md#extra_platforms.BUILDKITE)                                  |
| [`is_buildroot()`](detection.md#extra_platforms.is_buildroot)                       |  ⛑️  | [`BUILDROOT`](platforms.md#extra_platforms.BUILDROOT)                           |
| [`is_cachyos()`](detection.md#extra_platforms.is_cachyos)                           |  ⌬   | [`CACHYOS`](platforms.md#extra_platforms.CACHYOS)                               |
| [`is_centos()`](detection.md#extra_platforms.is_centos)                             |  💠  | [`CENTOS`](platforms.md#extra_platforms.CENTOS)                                 |
| [`is_circle_ci()`](detection.md#extra_platforms.is_circle_ci)                       |  ⪾   | [`CIRCLE_CI`](ci.md#extra_platforms.CIRCLE_CI)                                  |
| [`is_cirrus_ci()`](detection.md#extra_platforms.is_cirrus_ci)                       |  ≋   | [`CIRRUS_CI`](ci.md#extra_platforms.CIRRUS_CI)                                  |
| [`is_cloudlinux()`](detection.md#extra_platforms.is_cloudlinux)                     |  ꩜   | [`CLOUDLINUX`](platforms.md#extra_platforms.CLOUDLINUX)                         |
| [`is_codebuild()`](detection.md#extra_platforms.is_codebuild)                       |  ᚙ   | [`CODEBUILD`](ci.md#extra_platforms.CODEBUILD)                                  |
| [`is_cygwin()`](detection.md#extra_platforms.is_cygwin)                             |  Ͼ   | [`CYGWIN`](platforms.md#extra_platforms.CYGWIN)                                 |
| [`is_debian()`](detection.md#extra_platforms.is_debian)                             |  🌀  | [`DEBIAN`](platforms.md#extra_platforms.DEBIAN)                                 |
| [`is_dragonfly_bsd()`](detection.md#extra_platforms.is_dragonfly_bsd)               |  🪰  | [`DRAGONFLY_BSD`](platforms.md#extra_platforms.DRAGONFLY_BSD)                   |
| [`is_exherbo()`](detection.md#extra_platforms.is_exherbo)                           |  🐽  | [`EXHERBO`](platforms.md#extra_platforms.EXHERBO)                               |
| [`is_fedora()`](detection.md#extra_platforms.is_fedora)                             |  🎩  | [`FEDORA`](platforms.md#extra_platforms.FEDORA)                                 |
| [`is_freebsd()`](detection.md#extra_platforms.is_freebsd)                           |  😈  | [`FREEBSD`](platforms.md#extra_platforms.FREEBSD)                               |
| [`is_gentoo()`](detection.md#extra_platforms.is_gentoo)                             |  🗜️  | [`GENTOO`](platforms.md#extra_platforms.GENTOO)                                 |
| [`is_github_ci()`](detection.md#extra_platforms.is_github_ci)                       |  🐙  | [`GITHUB_CI`](ci.md#extra_platforms.GITHUB_CI)                                  |
| [`is_gitlab_ci()`](detection.md#extra_platforms.is_gitlab_ci)                       |  🦊  | [`GITLAB_CI`](ci.md#extra_platforms.GITLAB_CI)                                  |
| [`is_guix()`](detection.md#extra_platforms.is_guix)                                 |  🐃  | [`GUIX`](platforms.md#extra_platforms.GUIX)                                     |
| [`is_haiku()`](detection.md#extra_platforms.is_haiku)                               |  🍂  | [`HAIKU`](platforms.md#extra_platforms.HAIKU)                                   |
| [`is_heroku_ci()`](detection.md#extra_platforms.is_heroku_ci)                       |  ⥁   | [`HEROKU_CI`](ci.md#extra_platforms.HEROKU_CI)                                  |
| [`is_hurd()`](detection.md#extra_platforms.is_hurd)                                 |  🐃  | [`HURD`](platforms.md#extra_platforms.HURD)                                     |
| [`is_i386()`](detection.md#extra_platforms.is_i386)                                 |  𝗶   | [`I386`](architectures.md#extra_platforms.I386)                                 |
| [`is_i586()`](detection.md#extra_platforms.is_i586)                                 |  𝗶   | [`I586`](architectures.md#extra_platforms.I586)                                 |
| [`is_i686()`](detection.md#extra_platforms.is_i686)                                 |  𝗶   | [`I686`](architectures.md#extra_platforms.I686)                                 |
| [`is_ibm_mainframe()`](detection.md#extra_platforms.is_ibm_mainframe)               |  🏢  | [`IBM_MAINFRAME`](groups.md#extra_platforms.IBM_MAINFRAME)                      |
| [`is_ibm_powerkvm()`](detection.md#extra_platforms.is_ibm_powerkvm)                 |  🤹  | [`IBM_POWERKVM`](platforms.md#extra_platforms.IBM_POWERKVM)                     |
| [`is_illumos()`](detection.md#extra_platforms.is_illumos)                           |  🔥  | [`ILLUMOS`](platforms.md#extra_platforms.ILLUMOS)                               |
| [`is_kvmibm()`](detection.md#extra_platforms.is_kvmibm)                             |  🤹  | [`KVMIBM`](platforms.md#extra_platforms.KVMIBM)                                 |
| [`is_linux()`](detection.md#extra_platforms.is_linux)                               |  🐧  | [`LINUX`](groups.md#extra_platforms.LINUX)                                      |
| [`is_linux_layers()`](detection.md#extra_platforms.is_linux_layers)                 |  ≚   | [`LINUX_LAYERS`](groups.md#extra_platforms.LINUX_LAYERS)                        |
| [`is_linux_like()`](detection.md#extra_platforms.is_linux_like)                     | 🐧+  | [`LINUX_LIKE`](groups.md#extra_platforms.LINUX_LIKE)                            |
| [`is_linuxmint()`](detection.md#extra_platforms.is_linuxmint)                       |  🌿  | [`LINUXMINT`](platforms.md#extra_platforms.LINUXMINT)                           |
| [`is_loongarch()`](detection.md#extra_platforms.is_loongarch)                       |  🐉  | [`LOONGARCH`](groups.md#extra_platforms.LOONGARCH)                              |
| [`is_loongarch64()`](detection.md#extra_platforms.is_loongarch64)                   |  🐉  | [`LOONGARCH64`](architectures.md#extra_platforms.LOONGARCH64)                   |
| [`is_macos()`](detection.md#extra_platforms.is_macos)                               |  🍎  | [`MACOS`](platforms.md#extra_platforms.MACOS)                                   |
| [`is_mageia()`](detection.md#extra_platforms.is_mageia)                             |  ⍥   | [`MAGEIA`](platforms.md#extra_platforms.MAGEIA)                                 |
| [`is_mandriva()`](detection.md#extra_platforms.is_mandriva)                         |  💫  | [`MANDRIVA`](platforms.md#extra_platforms.MANDRIVA)                             |
| [`is_midnightbsd()`](detection.md#extra_platforms.is_midnightbsd)                   |  🌘  | [`MIDNIGHTBSD`](platforms.md#extra_platforms.MIDNIGHTBSD)                       |
| [`is_mips()`](detection.md#extra_platforms.is_mips)                                 |  🔲  | [`MIPS`](architectures.md#extra_platforms.MIPS)                                 |
| [`is_mips64()`](detection.md#extra_platforms.is_mips64)                             |  🔲  | [`MIPS64`](architectures.md#extra_platforms.MIPS64)                             |
| [`is_mips64el()`](detection.md#extra_platforms.is_mips64el)                         |  🔲  | [`MIPS64EL`](architectures.md#extra_platforms.MIPS64EL)                         |
| [`is_mipsel()`](detection.md#extra_platforms.is_mipsel)                             |  🔲  | [`MIPSEL`](architectures.md#extra_platforms.MIPSEL)                             |
| [`is_netbsd()`](detection.md#extra_platforms.is_netbsd)                             |  🚩  | [`NETBSD`](platforms.md#extra_platforms.NETBSD)                                 |
| [`is_nobara()`](detection.md#extra_platforms.is_nobara)                             |     | [`NOBARA`](platforms.md#extra_platforms.NOBARA)                                 |
| [`is_openbsd()`](detection.md#extra_platforms.is_openbsd)                           |  🐡  | [`OPENBSD`](platforms.md#extra_platforms.OPENBSD)                               |
| [`is_opensuse()`](detection.md#extra_platforms.is_opensuse)                         |  🦎  | [`OPENSUSE`](platforms.md#extra_platforms.OPENSUSE)                             |
| [`is_oracle()`](detection.md#extra_platforms.is_oracle)                             |  🦴  | [`ORACLE`](platforms.md#extra_platforms.ORACLE)                                 |
| [`is_other_unix()`](detection.md#extra_platforms.is_other_unix)                     |  ⊎   | [`OTHER_UNIX`](groups.md#extra_platforms.OTHER_UNIX)                            |
| [`is_parallels()`](detection.md#extra_platforms.is_parallels)                       |  ∥   | [`PARALLELS`](platforms.md#extra_platforms.PARALLELS)                           |
| [`is_pidora()`](detection.md#extra_platforms.is_pidora)                             |  🍓  | [`PIDORA`](platforms.md#extra_platforms.PIDORA)                                 |
| [`is_powerpc()`](detection.md#extra_platforms.is_powerpc)                           |  ⚡  | [`POWERPC`](groups.md#extra_platforms.POWERPC)                                  |
| [`is_ppc()`](detection.md#extra_platforms.is_ppc)                                   |  ⚡  | [`PPC`](architectures.md#extra_platforms.PPC)                                   |
| [`is_ppc64()`](detection.md#extra_platforms.is_ppc64)                               |  ⚡  | [`PPC64`](architectures.md#extra_platforms.PPC64)                               |
| [`is_ppc64le()`](detection.md#extra_platforms.is_ppc64le)                           |  ⚡  | [`PPC64LE`](architectures.md#extra_platforms.PPC64LE)                           |
| [`is_raspbian()`](detection.md#extra_platforms.is_raspbian)                         |  🍓  | [`RASPBIAN`](platforms.md#extra_platforms.RASPBIAN)                             |
| [`is_rhel()`](detection.md#extra_platforms.is_rhel)                                 |  🎩  | [`RHEL`](platforms.md#extra_platforms.RHEL)                                     |
| [`is_riscv()`](detection.md#extra_platforms.is_riscv)                               |  Ⅴ   | [`RISCV`](groups.md#extra_platforms.RISCV)                                      |
| [`is_riscv32()`](detection.md#extra_platforms.is_riscv32)                           |  Ⅴ   | [`RISCV32`](architectures.md#extra_platforms.RISCV32)                           |
| [`is_riscv64()`](detection.md#extra_platforms.is_riscv64)                           |  Ⅴ   | [`RISCV64`](architectures.md#extra_platforms.RISCV64)                           |
| [`is_rocky()`](detection.md#extra_platforms.is_rocky)                               |  ⛰️  | [`ROCKY`](platforms.md#extra_platforms.ROCKY)                                   |
| [`is_s390x()`](detection.md#extra_platforms.is_s390x)                               |  🏢  | [`S390X`](architectures.md#extra_platforms.S390X)                               |
| [`is_scientific()`](detection.md#extra_platforms.is_scientific)                     |  ⚛️  | [`SCIENTIFIC`](platforms.md#extra_platforms.SCIENTIFIC)                         |
| [`is_slackware()`](detection.md#extra_platforms.is_slackware)                       |  🚬  | [`SLACKWARE`](platforms.md#extra_platforms.SLACKWARE)                           |
| [`is_sles()`](detection.md#extra_platforms.is_sles)                                 |  🦎  | [`SLES`](platforms.md#extra_platforms.SLES)                                     |
| [`is_solaris()`](detection.md#extra_platforms.is_solaris)                           |  🌞  | [`SOLARIS`](platforms.md#extra_platforms.SOLARIS)                               |
| [`is_sparc()`](detection.md#extra_platforms.is_sparc)                               |  ☀️  | [`SPARC`](architectures.md#extra_platforms.SPARC)                               |
| [`is_sparc64()`](detection.md#extra_platforms.is_sparc64)                           |  ☀️  | [`SPARC64`](architectures.md#extra_platforms.SPARC64)                           |
| [`is_sunos()`](detection.md#extra_platforms.is_sunos)                               |  ☀️  | [`SUNOS`](platforms.md#extra_platforms.SUNOS)                                   |
| [`is_system_v()`](detection.md#extra_platforms.is_system_v)                         |  𝐕   | [`SYSTEM_V`](groups.md#extra_platforms.SYSTEM_V)                                |
| [`is_teamcity()`](detection.md#extra_platforms.is_teamcity)                         |  🏙️  | [`TEAMCITY`](ci.md#extra_platforms.TEAMCITY)                                    |
| [`is_travis_ci()`](detection.md#extra_platforms.is_travis_ci)                       |  👷  | [`TRAVIS_CI`](ci.md#extra_platforms.TRAVIS_CI)                                  |
| [`is_tumbleweed()`](detection.md#extra_platforms.is_tumbleweed)                     |  ↻   | [`TUMBLEWEED`](platforms.md#extra_platforms.TUMBLEWEED)                         |
| [`is_tuxedo()`](detection.md#extra_platforms.is_tuxedo)                             |  🤵  | [`TUXEDO`](platforms.md#extra_platforms.TUXEDO)                                 |
| [`is_ubuntu()`](detection.md#extra_platforms.is_ubuntu)                             |  🎯  | [`UBUNTU`](platforms.md#extra_platforms.UBUNTU)                                 |
| [`is_ultramarine()`](detection.md#extra_platforms.is_ultramarine)                   |  🌊  | [`ULTRAMARINE`](platforms.md#extra_platforms.ULTRAMARINE)                       |
| [`is_unix()`](detection.md#extra_platforms.is_unix)                                 |  ⨷   | [`UNIX`](groups.md#extra_platforms.UNIX)                                        |
| [`is_unix_layers()`](detection.md#extra_platforms.is_unix_layers)                   |  ≛   | [`UNIX_LAYERS`](groups.md#extra_platforms.UNIX_LAYERS)                          |
| [`is_unix_without_macos()`](detection.md#extra_platforms.is_unix_without_macos)     |  ⨂   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.UNIX_WITHOUT_MACOS)            |
| [`is_unknown()`](detection.md#extra_platforms.is_unknown)                           |  ❓  | [`UNKNOWN`](groups.md#extra_platforms.UNKNOWN)                                  |
| [`is_unknown_architecture()`](detection.md#extra_platforms.is_unknown_architecture) |  ❓  | [`UNKNOWN_ARCHITECTURE`](architectures.md#extra_platforms.UNKNOWN_ARCHITECTURE) |
| [`is_unknown_ci()`](detection.md#extra_platforms.is_unknown_ci)                     |  ❓  | [`UNKNOWN_CI`](ci.md#extra_platforms.UNKNOWN_CI)                                |
| [`is_unknown_platform()`](detection.md#extra_platforms.is_unknown_platform)         |  ❓  | [`UNKNOWN_PLATFORM`](platforms.md#extra_platforms.UNKNOWN_PLATFORM)             |
| [`is_wasm32()`](detection.md#extra_platforms.is_wasm32)                             |  🌐  | [`WASM32`](architectures.md#extra_platforms.WASM32)                             |
| [`is_wasm64()`](detection.md#extra_platforms.is_wasm64)                             |  🌐  | [`WASM64`](architectures.md#extra_platforms.WASM64)                             |
| [`is_webassembly()`](detection.md#extra_platforms.is_webassembly)                   |  🌐  | [`WEBASSEMBLY`](groups.md#extra_platforms.WEBASSEMBLY)                          |
| [`is_windows()`](detection.md#extra_platforms.is_windows)                           |  🪟  | [`WINDOWS`](platforms.md#extra_platforms.WINDOWS)                               |
| [`is_wsl1()`](detection.md#extra_platforms.is_wsl1)                                 |  ⊞   | [`WSL1`](platforms.md#extra_platforms.WSL1)                                     |
| [`is_wsl2()`](detection.md#extra_platforms.is_wsl2)                                 |  ⊞   | [`WSL2`](platforms.md#extra_platforms.WSL2)                                     |
| [`is_x86()`](detection.md#extra_platforms.is_x86)                                   |  𝘅   | [`X86`](groups.md#extra_platforms.X86)                                          |
| [`is_x86_64()`](detection.md#extra_platforms.is_x86_64)                             |  🖥️  | [`X86_64`](architectures.md#extra_platforms.X86_64)                             |
| [`is_xenserver()`](detection.md#extra_platforms.is_xenserver)                       |  Ⓧ   | [`XENSERVER`](platforms.md#extra_platforms.XENSERVER)                           |

<!-- all-detection-function-table-end -->

## Trait detection functions

<!-- trait-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_aarch64
.. autofunction:: extra_platforms.is_aix
.. autofunction:: extra_platforms.is_altlinux
.. autofunction:: extra_platforms.is_amzn
.. autofunction:: extra_platforms.is_android
.. autofunction:: extra_platforms.is_arch
.. autofunction:: extra_platforms.is_arm
.. autofunction:: extra_platforms.is_armv5tel
.. autofunction:: extra_platforms.is_armv6l
.. autofunction:: extra_platforms.is_armv7l
.. autofunction:: extra_platforms.is_armv8l
.. autofunction:: extra_platforms.is_azure_pipelines
.. autofunction:: extra_platforms.is_bamboo
.. autofunction:: extra_platforms.is_buildkite
.. autofunction:: extra_platforms.is_buildroot
.. autofunction:: extra_platforms.is_cachyos
.. autofunction:: extra_platforms.is_centos
.. autofunction:: extra_platforms.is_circle_ci
.. autofunction:: extra_platforms.is_cirrus_ci
.. autofunction:: extra_platforms.is_cloudlinux
.. autofunction:: extra_platforms.is_codebuild
.. autofunction:: extra_platforms.is_cygwin
.. autofunction:: extra_platforms.is_debian
.. autofunction:: extra_platforms.is_dragonfly_bsd
.. autofunction:: extra_platforms.is_exherbo
.. autofunction:: extra_platforms.is_fedora
.. autofunction:: extra_platforms.is_freebsd
.. autofunction:: extra_platforms.is_gentoo
.. autofunction:: extra_platforms.is_github_ci
.. autofunction:: extra_platforms.is_gitlab_ci
.. autofunction:: extra_platforms.is_guix
.. autofunction:: extra_platforms.is_haiku
.. autofunction:: extra_platforms.is_heroku_ci
.. autofunction:: extra_platforms.is_hurd
.. autofunction:: extra_platforms.is_i386
.. autofunction:: extra_platforms.is_i586
.. autofunction:: extra_platforms.is_i686
.. autofunction:: extra_platforms.is_ibm_powerkvm
.. autofunction:: extra_platforms.is_illumos
.. autofunction:: extra_platforms.is_kvmibm
.. autofunction:: extra_platforms.is_linuxmint
.. autofunction:: extra_platforms.is_loongarch64
.. autofunction:: extra_platforms.is_macos
.. autofunction:: extra_platforms.is_mageia
.. autofunction:: extra_platforms.is_mandriva
.. autofunction:: extra_platforms.is_midnightbsd
.. autofunction:: extra_platforms.is_mips
.. autofunction:: extra_platforms.is_mips64
.. autofunction:: extra_platforms.is_mips64el
.. autofunction:: extra_platforms.is_mipsel
.. autofunction:: extra_platforms.is_netbsd
.. autofunction:: extra_platforms.is_nobara
.. autofunction:: extra_platforms.is_openbsd
.. autofunction:: extra_platforms.is_opensuse
.. autofunction:: extra_platforms.is_oracle
.. autofunction:: extra_platforms.is_parallels
.. autofunction:: extra_platforms.is_pidora
.. autofunction:: extra_platforms.is_ppc
.. autofunction:: extra_platforms.is_ppc64
.. autofunction:: extra_platforms.is_ppc64le
.. autofunction:: extra_platforms.is_raspbian
.. autofunction:: extra_platforms.is_rhel
.. autofunction:: extra_platforms.is_riscv32
.. autofunction:: extra_platforms.is_riscv64
.. autofunction:: extra_platforms.is_rocky
.. autofunction:: extra_platforms.is_s390x
.. autofunction:: extra_platforms.is_scientific
.. autofunction:: extra_platforms.is_slackware
.. autofunction:: extra_platforms.is_sles
.. autofunction:: extra_platforms.is_solaris
.. autofunction:: extra_platforms.is_sparc
.. autofunction:: extra_platforms.is_sparc64
.. autofunction:: extra_platforms.is_sunos
.. autofunction:: extra_platforms.is_teamcity
.. autofunction:: extra_platforms.is_travis_ci
.. autofunction:: extra_platforms.is_tumbleweed
.. autofunction:: extra_platforms.is_tuxedo
.. autofunction:: extra_platforms.is_ubuntu
.. autofunction:: extra_platforms.is_ultramarine
.. autofunction:: extra_platforms.is_unknown_architecture
.. autofunction:: extra_platforms.is_unknown_ci
.. autofunction:: extra_platforms.is_unknown_platform
.. autofunction:: extra_platforms.is_wasm32
.. autofunction:: extra_platforms.is_wasm64
.. autofunction:: extra_platforms.is_windows
.. autofunction:: extra_platforms.is_wsl1
.. autofunction:: extra_platforms.is_wsl2
.. autofunction:: extra_platforms.is_x86_64
.. autofunction:: extra_platforms.is_xenserver
```

<!-- trait-detection-autofunction-end -->

## Group detection functions

Contrary to individual trait detection functions like `is_linux()` or `is_x86_64()`, group detection functions check for membership in a collection of traits.

These functions are dynamically generated for each [group](groups.md) and test whether **at least one trait** from the group matches the current system:

<!-- group-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_any_architecture
.. autofunction:: extra_platforms.is_any_arm
.. autofunction:: extra_platforms.is_any_ci
.. autofunction:: extra_platforms.is_any_mips
.. autofunction:: extra_platforms.is_any_platform
.. autofunction:: extra_platforms.is_any_sparc
.. autofunction:: extra_platforms.is_any_trait
.. autofunction:: extra_platforms.is_any_windows
.. autofunction:: extra_platforms.is_arch_32_bit
.. autofunction:: extra_platforms.is_arch_64_bit
.. autofunction:: extra_platforms.is_bsd
.. autofunction:: extra_platforms.is_bsd_without_macos
.. autofunction:: extra_platforms.is_ibm_mainframe
.. autofunction:: extra_platforms.is_linux
.. autofunction:: extra_platforms.is_linux_layers
.. autofunction:: extra_platforms.is_linux_like
.. autofunction:: extra_platforms.is_loongarch
.. autofunction:: extra_platforms.is_other_unix
.. autofunction:: extra_platforms.is_powerpc
.. autofunction:: extra_platforms.is_riscv
.. autofunction:: extra_platforms.is_system_v
.. autofunction:: extra_platforms.is_unix
.. autofunction:: extra_platforms.is_unix_layers
.. autofunction:: extra_platforms.is_unix_without_macos
.. autofunction:: extra_platforms.is_unknown
.. autofunction:: extra_platforms.is_webassembly
.. autofunction:: extra_platforms.is_x86
```

<!-- group-detection-autofunction-end -->

## Current trait functions

These functions retrieve the currently detected traits:

```{eval-rst}
.. autofunction:: extra_platforms.current_traits
.. autofunction:: extra_platforms.current_architecture
.. autofunction:: extra_platforms.current_platform
.. autofunction:: extra_platforms.current_ci
```