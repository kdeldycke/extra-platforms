# {octicon}`pulse` Detection

## All detection functions

<!-- all-detection-function-table-start -->

| Detection function                                                      | Icon | Associated symbol                                                               | Type         |
| :---------------------------------------------------------------------- | :--: | :------------------------------------------------------------------------------ | :----------- |
| [`is_aarch64()`](#extra_platforms.is_aarch64)                           |  📱  | [`AARCH64`](architectures.md#extra_platforms.AARCH64)                           | Architecture |
| [`is_aix()`](#extra_platforms.is_aix)                                   |  ➿  | [`AIX`](platforms.md#extra_platforms.AIX)                                       | Platform     |
| [`is_all_architectures()`](#extra_platforms.is_all_architectures)       |  🏛️  | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.ALL_ARCHITECTURES)              | Group        |
| [`is_all_ci()`](#extra_platforms.is_all_ci)                             |  ♺   | [`ALL_CI`](groups.md#extra_platforms.ALL_CI)                                    | Group        |
| [`is_all_platforms()`](#extra_platforms.is_all_platforms)               |  ⚙️  | [`ALL_PLATFORMS`](groups.md#extra_platforms.ALL_PLATFORMS)                      | Group        |
| [`is_all_traits()`](#extra_platforms.is_all_traits)                     |  ⁕   | [`ALL_TRAITS`](groups.md#extra_platforms.ALL_TRAITS)                            | Group        |
| [`is_altlinux()`](#extra_platforms.is_altlinux)                         |  🐧  | [`ALTLINUX`](platforms.md#extra_platforms.ALTLINUX)                             | Platform     |
| [`is_amzn()`](#extra_platforms.is_amzn)                                 |  ⤻   | [`AMZN`](platforms.md#extra_platforms.AMZN)                                     | Platform     |
| [`is_android()`](#extra_platforms.is_android)                           |  🤖  | [`ANDROID`](platforms.md#extra_platforms.ANDROID)                               | Platform     |
| [`is_any_arm()`](#extra_platforms.is_any_arm)                           |  📱  | [`ANY_ARM`](groups.md#extra_platforms.ANY_ARM)                                  | Group        |
| [`is_any_mips()`](#extra_platforms.is_any_mips)                         |  🔲  | [`ANY_MIPS`](groups.md#extra_platforms.ANY_MIPS)                                | Group        |
| [`is_any_sparc()`](#extra_platforms.is_any_sparc)                       |  ☀️  | [`ANY_SPARC`](groups.md#extra_platforms.ANY_SPARC)                              | Group        |
| [`is_any_windows()`](#extra_platforms.is_any_windows)                   |  🪟  | [`ANY_WINDOWS`](groups.md#extra_platforms.ANY_WINDOWS)                          | Group        |
| [`is_arch()`](#extra_platforms.is_arch)                                 |  🎗️  | [`ARCH`](platforms.md#extra_platforms.ARCH)                                     | Platform     |
| [`is_arch_32_bit()`](#extra_platforms.is_arch_32_bit)                   |  ³²  | [`ARCH_32_BIT`](groups.md#extra_platforms.ARCH_32_BIT)                          | Group        |
| [`is_arch_64_bit()`](#extra_platforms.is_arch_64_bit)                   |  ⁶⁴  | [`ARCH_64_BIT`](groups.md#extra_platforms.ARCH_64_BIT)                          | Group        |
| [`is_arm()`](#extra_platforms.is_arm)                                   |  📱  | [`ARM`](architectures.md#extra_platforms.ARM)                                   | Architecture |
| [`is_armv6l()`](#extra_platforms.is_armv6l)                             |  📱  | [`ARMV6L`](architectures.md#extra_platforms.ARMV6L)                             | Architecture |
| [`is_armv7l()`](#extra_platforms.is_armv7l)                             |  📱  | [`ARMV7L`](architectures.md#extra_platforms.ARMV7L)                             | Architecture |
| [`is_armv8l()`](#extra_platforms.is_armv8l)                             |  📱  | [`ARMV8L`](architectures.md#extra_platforms.ARMV8L)                             | Architecture |
| [`is_azure_pipelines()`](#extra_platforms.is_azure_pipelines)           |  ═   | [`AZURE_PIPELINES`](ci.md#extra_platforms.AZURE_PIPELINES)                      | CI           |
| [`is_bamboo()`](#extra_platforms.is_bamboo)                             |  ⟲   | [`BAMBOO`](ci.md#extra_platforms.BAMBOO)                                        | CI           |
| [`is_bsd()`](#extra_platforms.is_bsd)                                   | 🅱️+  | [`BSD`](groups.md#extra_platforms.BSD)                                          | Group        |
| [`is_bsd_without_macos()`](#extra_platforms.is_bsd_without_macos)       |  🅱️  | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.BSD_WITHOUT_MACOS)              | Group        |
| [`is_buildkite()`](#extra_platforms.is_buildkite)                       |  🪁  | [`BUILDKITE`](ci.md#extra_platforms.BUILDKITE)                                  | CI           |
| [`is_buildroot()`](#extra_platforms.is_buildroot)                       |  ⛑️  | [`BUILDROOT`](platforms.md#extra_platforms.BUILDROOT)                           | Platform     |
| [`is_cachyos()`](#extra_platforms.is_cachyos)                           |  ⌬   | [`CACHYOS`](platforms.md#extra_platforms.CACHYOS)                               | Platform     |
| [`is_centos()`](#extra_platforms.is_centos)                             |  💠  | [`CENTOS`](platforms.md#extra_platforms.CENTOS)                                 | Platform     |
| [`is_circle_ci()`](#extra_platforms.is_circle_ci)                       |  ⪾   | [`CIRCLE_CI`](ci.md#extra_platforms.CIRCLE_CI)                                  | CI           |
| [`is_cirrus_ci()`](#extra_platforms.is_cirrus_ci)                       |  ≋   | [`CIRRUS_CI`](ci.md#extra_platforms.CIRRUS_CI)                                  | CI           |
| [`is_cloudlinux()`](#extra_platforms.is_cloudlinux)                     |  ꩜   | [`CLOUDLINUX`](platforms.md#extra_platforms.CLOUDLINUX)                         | Platform     |
| [`is_codebuild()`](#extra_platforms.is_codebuild)                       |  ᚙ   | [`CODEBUILD`](ci.md#extra_platforms.CODEBUILD)                                  | CI           |
| [`is_cygwin()`](#extra_platforms.is_cygwin)                             |  Ͼ   | [`CYGWIN`](platforms.md#extra_platforms.CYGWIN)                                 | Platform     |
| [`is_debian()`](#extra_platforms.is_debian)                             |  🌀  | [`DEBIAN`](platforms.md#extra_platforms.DEBIAN)                                 | Platform     |
| [`is_exherbo()`](#extra_platforms.is_exherbo)                           |  🐽  | [`EXHERBO`](platforms.md#extra_platforms.EXHERBO)                               | Platform     |
| [`is_fedora()`](#extra_platforms.is_fedora)                             |  🎩  | [`FEDORA`](platforms.md#extra_platforms.FEDORA)                                 | Platform     |
| [`is_freebsd()`](#extra_platforms.is_freebsd)                           |  😈  | [`FREEBSD`](platforms.md#extra_platforms.FREEBSD)                               | Platform     |
| [`is_gentoo()`](#extra_platforms.is_gentoo)                             |  🗜️  | [`GENTOO`](platforms.md#extra_platforms.GENTOO)                                 | Platform     |
| [`is_github_ci()`](#extra_platforms.is_github_ci)                       |  🐙  | [`GITHUB_CI`](ci.md#extra_platforms.GITHUB_CI)                                  | CI           |
| [`is_gitlab_ci()`](#extra_platforms.is_gitlab_ci)                       |  🦊  | [`GITLAB_CI`](ci.md#extra_platforms.GITLAB_CI)                                  | CI           |
| [`is_guix()`](#extra_platforms.is_guix)                                 |  🐃  | [`GUIX`](platforms.md#extra_platforms.GUIX)                                     | Platform     |
| [`is_heroku_ci()`](#extra_platforms.is_heroku_ci)                       |  ⥁   | [`HEROKU_CI`](ci.md#extra_platforms.HEROKU_CI)                                  | CI           |
| [`is_hurd()`](#extra_platforms.is_hurd)                                 |  🐃  | [`HURD`](platforms.md#extra_platforms.HURD)                                     | Platform     |
| [`is_i386()`](#extra_platforms.is_i386)                                 |  𝗶   | [`I386`](architectures.md#extra_platforms.I386)                                 | Architecture |
| [`is_i586()`](#extra_platforms.is_i586)                                 |  𝗶   | [`I586`](architectures.md#extra_platforms.I586)                                 | Architecture |
| [`is_i686()`](#extra_platforms.is_i686)                                 |  𝗶   | [`I686`](architectures.md#extra_platforms.I686)                                 | Architecture |
| [`is_ibm_mainframe()`](#extra_platforms.is_ibm_mainframe)               |  🏢  | [`IBM_MAINFRAME`](groups.md#extra_platforms.IBM_MAINFRAME)                      | Group        |
| [`is_ibm_powerkvm()`](#extra_platforms.is_ibm_powerkvm)                 |  🤹  | [`IBM_POWERKVM`](platforms.md#extra_platforms.IBM_POWERKVM)                     | Platform     |
| [`is_kvmibm()`](#extra_platforms.is_kvmibm)                             |  🤹  | [`KVMIBM`](platforms.md#extra_platforms.KVMIBM)                                 | Platform     |
| [`is_linux()`](#extra_platforms.is_linux)                               |  🐧  | [`LINUX`](groups.md#extra_platforms.LINUX)                                      | Group        |
| [`is_linux_layers()`](#extra_platforms.is_linux_layers)                 |  ≚   | [`LINUX_LAYERS`](groups.md#extra_platforms.LINUX_LAYERS)                        | Group        |
| [`is_linux_like()`](#extra_platforms.is_linux_like)                     | 🐧+  | [`LINUX_LIKE`](groups.md#extra_platforms.LINUX_LIKE)                            | Group        |
| [`is_linuxmint()`](#extra_platforms.is_linuxmint)                       |  🌿  | [`LINUXMINT`](platforms.md#extra_platforms.LINUXMINT)                           | Platform     |
| [`is_loongarch()`](#extra_platforms.is_loongarch)                       |  🐉  | [`LOONGARCH`](groups.md#extra_platforms.LOONGARCH)                              | Group        |
| [`is_loongarch64()`](#extra_platforms.is_loongarch64)                   |  🐉  | [`LOONGARCH64`](architectures.md#extra_platforms.LOONGARCH64)                   | Architecture |
| [`is_macos()`](#extra_platforms.is_macos)                               |  🍎  | [`MACOS`](platforms.md#extra_platforms.MACOS)                                   | Platform     |
| [`is_mageia()`](#extra_platforms.is_mageia)                             |  ⍥   | [`MAGEIA`](platforms.md#extra_platforms.MAGEIA)                                 | Platform     |
| [`is_mandriva()`](#extra_platforms.is_mandriva)                         |  💫  | [`MANDRIVA`](platforms.md#extra_platforms.MANDRIVA)                             | Platform     |
| [`is_midnightbsd()`](#extra_platforms.is_midnightbsd)                   |  🌘  | [`MIDNIGHTBSD`](platforms.md#extra_platforms.MIDNIGHTBSD)                       | Platform     |
| [`is_mips()`](#extra_platforms.is_mips)                                 |  🔲  | [`MIPS`](architectures.md#extra_platforms.MIPS)                                 | Architecture |
| [`is_mips64()`](#extra_platforms.is_mips64)                             |  🔲  | [`MIPS64`](architectures.md#extra_platforms.MIPS64)                             | Architecture |
| [`is_mips64el()`](#extra_platforms.is_mips64el)                         |  🔲  | [`MIPS64EL`](architectures.md#extra_platforms.MIPS64EL)                         | Architecture |
| [`is_mipsel()`](#extra_platforms.is_mipsel)                             |  🔲  | [`MIPSEL`](architectures.md#extra_platforms.MIPSEL)                             | Architecture |
| [`is_netbsd()`](#extra_platforms.is_netbsd)                             |  🚩  | [`NETBSD`](platforms.md#extra_platforms.NETBSD)                                 | Platform     |
| [`is_nobara()`](#extra_platforms.is_nobara)                             |     | [`NOBARA`](platforms.md#extra_platforms.NOBARA)                                 | Platform     |
| [`is_openbsd()`](#extra_platforms.is_openbsd)                           |  🐡  | [`OPENBSD`](platforms.md#extra_platforms.OPENBSD)                               | Platform     |
| [`is_opensuse()`](#extra_platforms.is_opensuse)                         |  🦎  | [`OPENSUSE`](platforms.md#extra_platforms.OPENSUSE)                             | Platform     |
| [`is_oracle()`](#extra_platforms.is_oracle)                             |  🦴  | [`ORACLE`](platforms.md#extra_platforms.ORACLE)                                 | Platform     |
| [`is_other_unix()`](#extra_platforms.is_other_unix)                     |  ⊎   | [`OTHER_UNIX`](groups.md#extra_platforms.OTHER_UNIX)                            | Group        |
| [`is_parallels()`](#extra_platforms.is_parallels)                       |  ∥   | [`PARALLELS`](platforms.md#extra_platforms.PARALLELS)                           | Platform     |
| [`is_pidora()`](#extra_platforms.is_pidora)                             |  🍓  | [`PIDORA`](platforms.md#extra_platforms.PIDORA)                                 | Platform     |
| [`is_powerpc()`](#extra_platforms.is_powerpc)                           |  ⚡  | [`POWERPC`](groups.md#extra_platforms.POWERPC)                                  | Group        |
| [`is_ppc()`](#extra_platforms.is_ppc)                                   |  ⚡  | [`PPC`](architectures.md#extra_platforms.PPC)                                   | Architecture |
| [`is_ppc64()`](#extra_platforms.is_ppc64)                               |  ⚡  | [`PPC64`](architectures.md#extra_platforms.PPC64)                               | Architecture |
| [`is_ppc64le()`](#extra_platforms.is_ppc64le)                           |  ⚡  | [`PPC64LE`](architectures.md#extra_platforms.PPC64LE)                           | Architecture |
| [`is_raspbian()`](#extra_platforms.is_raspbian)                         |  🍓  | [`RASPBIAN`](platforms.md#extra_platforms.RASPBIAN)                             | Platform     |
| [`is_rhel()`](#extra_platforms.is_rhel)                                 |  🎩  | [`RHEL`](platforms.md#extra_platforms.RHEL)                                     | Platform     |
| [`is_riscv()`](#extra_platforms.is_riscv)                               |  Ⅴ   | [`RISCV`](groups.md#extra_platforms.RISCV)                                      | Group        |
| [`is_riscv32()`](#extra_platforms.is_riscv32)                           |  Ⅴ   | [`RISCV32`](architectures.md#extra_platforms.RISCV32)                           | Architecture |
| [`is_riscv64()`](#extra_platforms.is_riscv64)                           |  Ⅴ   | [`RISCV64`](architectures.md#extra_platforms.RISCV64)                           | Architecture |
| [`is_rocky()`](#extra_platforms.is_rocky)                               |  ⛰️  | [`ROCKY`](platforms.md#extra_platforms.ROCKY)                                   | Platform     |
| [`is_s390x()`](#extra_platforms.is_s390x)                               |  🏢  | [`S390X`](architectures.md#extra_platforms.S390X)                               | Architecture |
| [`is_scientific()`](#extra_platforms.is_scientific)                     |  ⚛️  | [`SCIENTIFIC`](platforms.md#extra_platforms.SCIENTIFIC)                         | Platform     |
| [`is_slackware()`](#extra_platforms.is_slackware)                       |  🚬  | [`SLACKWARE`](platforms.md#extra_platforms.SLACKWARE)                           | Platform     |
| [`is_sles()`](#extra_platforms.is_sles)                                 |  🦎  | [`SLES`](platforms.md#extra_platforms.SLES)                                     | Platform     |
| [`is_solaris()`](#extra_platforms.is_solaris)                           |  🌞  | [`SOLARIS`](platforms.md#extra_platforms.SOLARIS)                               | Platform     |
| [`is_sparc()`](#extra_platforms.is_sparc)                               |  ☀️  | [`SPARC`](architectures.md#extra_platforms.SPARC)                               | Architecture |
| [`is_sparc64()`](#extra_platforms.is_sparc64)                           |  ☀️  | [`SPARC64`](architectures.md#extra_platforms.SPARC64)                           | Architecture |
| [`is_sunos()`](#extra_platforms.is_sunos)                               |  ☀️  | [`SUNOS`](platforms.md#extra_platforms.SUNOS)                                   | Platform     |
| [`is_system_v()`](#extra_platforms.is_system_v)                         |  𝐕   | [`SYSTEM_V`](groups.md#extra_platforms.SYSTEM_V)                                | Group        |
| [`is_teamcity()`](#extra_platforms.is_teamcity)                         |  🏙️  | [`TEAMCITY`](ci.md#extra_platforms.TEAMCITY)                                    | CI           |
| [`is_travis_ci()`](#extra_platforms.is_travis_ci)                       |  👷  | [`TRAVIS_CI`](ci.md#extra_platforms.TRAVIS_CI)                                  | CI           |
| [`is_tumbleweed()`](#extra_platforms.is_tumbleweed)                     |  ↻   | [`TUMBLEWEED`](platforms.md#extra_platforms.TUMBLEWEED)                         | Platform     |
| [`is_tuxedo()`](#extra_platforms.is_tuxedo)                             |  🤵  | [`TUXEDO`](platforms.md#extra_platforms.TUXEDO)                                 | Platform     |
| [`is_ubuntu()`](#extra_platforms.is_ubuntu)                             |  🎯  | [`UBUNTU`](platforms.md#extra_platforms.UBUNTU)                                 | Platform     |
| [`is_ultramarine()`](#extra_platforms.is_ultramarine)                   |  🌊  | [`ULTRAMARINE`](platforms.md#extra_platforms.ULTRAMARINE)                       | Platform     |
| [`is_unix()`](#extra_platforms.is_unix)                                 |  ⨷   | [`UNIX`](groups.md#extra_platforms.UNIX)                                        | Group        |
| [`is_unix_layers()`](#extra_platforms.is_unix_layers)                   |  ≛   | [`UNIX_LAYERS`](groups.md#extra_platforms.UNIX_LAYERS)                          | Group        |
| [`is_unix_without_macos()`](#extra_platforms.is_unix_without_macos)     |  ⨂   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.UNIX_WITHOUT_MACOS)            | Group        |
| [`is_unknown()`](#extra_platforms.is_unknown)                           |  ❓  | [`UNKNOWN`](groups.md#extra_platforms.UNKNOWN)                                  | Group        |
| [`is_unknown_architecture()`](#extra_platforms.is_unknown_architecture) |  ❓  | [`UNKNOWN_ARCHITECTURE`](architectures.md#extra_platforms.UNKNOWN_ARCHITECTURE) | Architecture |
| [`is_unknown_ci()`](#extra_platforms.is_unknown_ci)                     |  ❓  | [`UNKNOWN_CI`](ci.md#extra_platforms.UNKNOWN_CI)                                | CI           |
| [`is_unknown_platform()`](#extra_platforms.is_unknown_platform)         |  ❓  | [`UNKNOWN_PLATFORM`](platforms.md#extra_platforms.UNKNOWN_PLATFORM)             | Platform     |
| [`is_wasm32()`](#extra_platforms.is_wasm32)                             |  🌐  | [`WASM32`](architectures.md#extra_platforms.WASM32)                             | Architecture |
| [`is_wasm64()`](#extra_platforms.is_wasm64)                             |  🌐  | [`WASM64`](architectures.md#extra_platforms.WASM64)                             | Architecture |
| [`is_webassembly()`](#extra_platforms.is_webassembly)                   |  🌐  | [`WEBASSEMBLY`](groups.md#extra_platforms.WEBASSEMBLY)                          | Group        |
| [`is_windows()`](#extra_platforms.is_windows)                           |  🪟  | [`WINDOWS`](platforms.md#extra_platforms.WINDOWS)                               | Platform     |
| [`is_wsl1()`](#extra_platforms.is_wsl1)                                 |  ⊞   | [`WSL1`](platforms.md#extra_platforms.WSL1)                                     | Platform     |
| [`is_wsl2()`](#extra_platforms.is_wsl2)                                 |  ⊞   | [`WSL2`](platforms.md#extra_platforms.WSL2)                                     | Platform     |
| [`is_x86()`](#extra_platforms.is_x86)                                   |  𝘅   | [`X86`](groups.md#extra_platforms.X86)                                          | Group        |
| [`is_x86_64()`](#extra_platforms.is_x86_64)                             |  🖥️  | [`X86_64`](architectures.md#extra_platforms.X86_64)                             | Architecture |
| [`is_xenserver()`](#extra_platforms.is_xenserver)                       |  Ⓧ   | [`XENSERVER`](platforms.md#extra_platforms.XENSERVER)                           | Platform     |

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
.. autofunction:: extra_platforms.is_exherbo
.. autofunction:: extra_platforms.is_fedora
.. autofunction:: extra_platforms.is_freebsd
.. autofunction:: extra_platforms.is_gentoo
.. autofunction:: extra_platforms.is_github_ci
.. autofunction:: extra_platforms.is_gitlab_ci
.. autofunction:: extra_platforms.is_guix
.. autofunction:: extra_platforms.is_heroku_ci
.. autofunction:: extra_platforms.is_hurd
.. autofunction:: extra_platforms.is_i386
.. autofunction:: extra_platforms.is_i586
.. autofunction:: extra_platforms.is_i686
.. autofunction:: extra_platforms.is_ibm_powerkvm
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
.. autofunction:: extra_platforms.is_all_architectures
.. autofunction:: extra_platforms.is_all_ci
.. autofunction:: extra_platforms.is_all_platforms
.. autofunction:: extra_platforms.is_all_traits
.. autofunction:: extra_platforms.is_any_arm
.. autofunction:: extra_platforms.is_any_mips
.. autofunction:: extra_platforms.is_any_sparc
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
