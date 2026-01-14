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

   **Associated trait**: `AARCH64 <architectures.html#extra_platforms.AARCH64>`_

.. autofunction:: extra_platforms.is_aix

   **Associated trait**: `AIX <platforms.html#extra_platforms.AIX>`_

.. autofunction:: extra_platforms.is_altlinux

   **Associated trait**: `ALTLINUX <platforms.html#extra_platforms.ALTLINUX>`_

.. autofunction:: extra_platforms.is_amzn

   **Associated trait**: `AMZN <platforms.html#extra_platforms.AMZN>`_

.. autofunction:: extra_platforms.is_android

   **Associated trait**: `ANDROID <platforms.html#extra_platforms.ANDROID>`_

.. autofunction:: extra_platforms.is_arch

   **Associated trait**: `ARCH <platforms.html#extra_platforms.ARCH>`_

.. autofunction:: extra_platforms.is_arm

   **Associated trait**: `ARM <architectures.html#extra_platforms.ARM>`_

.. autofunction:: extra_platforms.is_armv6l

   **Associated trait**: `ARMV6L <architectures.html#extra_platforms.ARMV6L>`_

.. autofunction:: extra_platforms.is_armv7l

   **Associated trait**: `ARMV7L <architectures.html#extra_platforms.ARMV7L>`_

.. autofunction:: extra_platforms.is_armv8l

   **Associated trait**: `ARMV8L <architectures.html#extra_platforms.ARMV8L>`_

.. autofunction:: extra_platforms.is_azure_pipelines

   **Associated trait**: `AZURE_PIPELINES <ci.html#extra_platforms.AZURE_PIPELINES>`_

.. autofunction:: extra_platforms.is_bamboo

   **Associated trait**: `BAMBOO <ci.html#extra_platforms.BAMBOO>`_

.. autofunction:: extra_platforms.is_buildkite

   **Associated trait**: `BUILDKITE <ci.html#extra_platforms.BUILDKITE>`_

.. autofunction:: extra_platforms.is_buildroot

   **Associated trait**: `BUILDROOT <platforms.html#extra_platforms.BUILDROOT>`_

.. autofunction:: extra_platforms.is_cachyos

   **Associated trait**: `CACHYOS <platforms.html#extra_platforms.CACHYOS>`_

.. autofunction:: extra_platforms.is_centos

   **Associated trait**: `CENTOS <platforms.html#extra_platforms.CENTOS>`_

.. autofunction:: extra_platforms.is_circle_ci

   **Associated trait**: `CIRCLE_CI <ci.html#extra_platforms.CIRCLE_CI>`_

.. autofunction:: extra_platforms.is_cirrus_ci

   **Associated trait**: `CIRRUS_CI <ci.html#extra_platforms.CIRRUS_CI>`_

.. autofunction:: extra_platforms.is_cloudlinux

   **Associated trait**: `CLOUDLINUX <platforms.html#extra_platforms.CLOUDLINUX>`_

.. autofunction:: extra_platforms.is_codebuild

   **Associated trait**: `CODEBUILD <ci.html#extra_platforms.CODEBUILD>`_

.. autofunction:: extra_platforms.is_cygwin

   **Associated trait**: `CYGWIN <platforms.html#extra_platforms.CYGWIN>`_

.. autofunction:: extra_platforms.is_debian

   **Associated trait**: `DEBIAN <platforms.html#extra_platforms.DEBIAN>`_

.. autofunction:: extra_platforms.is_exherbo

   **Associated trait**: `EXHERBO <platforms.html#extra_platforms.EXHERBO>`_

.. autofunction:: extra_platforms.is_fedora

   **Associated trait**: `FEDORA <platforms.html#extra_platforms.FEDORA>`_

.. autofunction:: extra_platforms.is_freebsd

   **Associated trait**: `FREEBSD <platforms.html#extra_platforms.FREEBSD>`_

.. autofunction:: extra_platforms.is_gentoo

   **Associated trait**: `GENTOO <platforms.html#extra_platforms.GENTOO>`_

.. autofunction:: extra_platforms.is_github_ci

   **Associated trait**: `GITHUB_CI <ci.html#extra_platforms.GITHUB_CI>`_

.. autofunction:: extra_platforms.is_gitlab_ci

   **Associated trait**: `GITLAB_CI <ci.html#extra_platforms.GITLAB_CI>`_

.. autofunction:: extra_platforms.is_guix

   **Associated trait**: `GUIX <platforms.html#extra_platforms.GUIX>`_

.. autofunction:: extra_platforms.is_heroku_ci

   **Associated trait**: `HEROKU_CI <ci.html#extra_platforms.HEROKU_CI>`_

.. autofunction:: extra_platforms.is_hurd

   **Associated trait**: `HURD <platforms.html#extra_platforms.HURD>`_

.. autofunction:: extra_platforms.is_i386

   **Associated trait**: `I386 <architectures.html#extra_platforms.I386>`_

.. autofunction:: extra_platforms.is_i586

   **Associated trait**: `I586 <architectures.html#extra_platforms.I586>`_

.. autofunction:: extra_platforms.is_i686

   **Associated trait**: `I686 <architectures.html#extra_platforms.I686>`_

.. autofunction:: extra_platforms.is_ibm_powerkvm

   **Associated trait**: `IBM_POWERKVM <platforms.html#extra_platforms.IBM_POWERKVM>`_

.. autofunction:: extra_platforms.is_kvmibm

   **Associated trait**: `KVMIBM <platforms.html#extra_platforms.KVMIBM>`_

.. autofunction:: extra_platforms.is_linuxmint

   **Associated trait**: `LINUXMINT <platforms.html#extra_platforms.LINUXMINT>`_

.. autofunction:: extra_platforms.is_loongarch64

   **Associated trait**: `LOONGARCH64 <architectures.html#extra_platforms.LOONGARCH64>`_

.. autofunction:: extra_platforms.is_macos

   **Associated trait**: `MACOS <platforms.html#extra_platforms.MACOS>`_

.. autofunction:: extra_platforms.is_mageia

   **Associated trait**: `MAGEIA <platforms.html#extra_platforms.MAGEIA>`_

.. autofunction:: extra_platforms.is_mandriva

   **Associated trait**: `MANDRIVA <platforms.html#extra_platforms.MANDRIVA>`_

.. autofunction:: extra_platforms.is_midnightbsd

   **Associated trait**: `MIDNIGHTBSD <platforms.html#extra_platforms.MIDNIGHTBSD>`_

.. autofunction:: extra_platforms.is_mips

   **Associated trait**: `MIPS <architectures.html#extra_platforms.MIPS>`_

.. autofunction:: extra_platforms.is_mips64

   **Associated trait**: `MIPS64 <architectures.html#extra_platforms.MIPS64>`_

.. autofunction:: extra_platforms.is_mips64el

   **Associated trait**: `MIPS64EL <architectures.html#extra_platforms.MIPS64EL>`_

.. autofunction:: extra_platforms.is_mipsel

   **Associated trait**: `MIPSEL <architectures.html#extra_platforms.MIPSEL>`_

.. autofunction:: extra_platforms.is_netbsd

   **Associated trait**: `NETBSD <platforms.html#extra_platforms.NETBSD>`_

.. autofunction:: extra_platforms.is_nobara

   **Associated trait**: `NOBARA <platforms.html#extra_platforms.NOBARA>`_

.. autofunction:: extra_platforms.is_openbsd

   **Associated trait**: `OPENBSD <platforms.html#extra_platforms.OPENBSD>`_

.. autofunction:: extra_platforms.is_opensuse

   **Associated trait**: `OPENSUSE <platforms.html#extra_platforms.OPENSUSE>`_

.. autofunction:: extra_platforms.is_oracle

   **Associated trait**: `ORACLE <platforms.html#extra_platforms.ORACLE>`_

.. autofunction:: extra_platforms.is_parallels

   **Associated trait**: `PARALLELS <platforms.html#extra_platforms.PARALLELS>`_

.. autofunction:: extra_platforms.is_pidora

   **Associated trait**: `PIDORA <platforms.html#extra_platforms.PIDORA>`_

.. autofunction:: extra_platforms.is_ppc

   **Associated trait**: `PPC <architectures.html#extra_platforms.PPC>`_

.. autofunction:: extra_platforms.is_ppc64

   **Associated trait**: `PPC64 <architectures.html#extra_platforms.PPC64>`_

.. autofunction:: extra_platforms.is_ppc64le

   **Associated trait**: `PPC64LE <architectures.html#extra_platforms.PPC64LE>`_

.. autofunction:: extra_platforms.is_raspbian

   **Associated trait**: `RASPBIAN <platforms.html#extra_platforms.RASPBIAN>`_

.. autofunction:: extra_platforms.is_rhel

   **Associated trait**: `RHEL <platforms.html#extra_platforms.RHEL>`_

.. autofunction:: extra_platforms.is_riscv32

   **Associated trait**: `RISCV32 <architectures.html#extra_platforms.RISCV32>`_

.. autofunction:: extra_platforms.is_riscv64

   **Associated trait**: `RISCV64 <architectures.html#extra_platforms.RISCV64>`_

.. autofunction:: extra_platforms.is_rocky

   **Associated trait**: `ROCKY <platforms.html#extra_platforms.ROCKY>`_

.. autofunction:: extra_platforms.is_s390x

   **Associated trait**: `S390X <architectures.html#extra_platforms.S390X>`_

.. autofunction:: extra_platforms.is_scientific

   **Associated trait**: `SCIENTIFIC <platforms.html#extra_platforms.SCIENTIFIC>`_

.. autofunction:: extra_platforms.is_slackware

   **Associated trait**: `SLACKWARE <platforms.html#extra_platforms.SLACKWARE>`_

.. autofunction:: extra_platforms.is_sles

   **Associated trait**: `SLES <platforms.html#extra_platforms.SLES>`_

.. autofunction:: extra_platforms.is_solaris

   **Associated trait**: `SOLARIS <platforms.html#extra_platforms.SOLARIS>`_

.. autofunction:: extra_platforms.is_sparc

   **Associated trait**: `SPARC <architectures.html#extra_platforms.SPARC>`_

.. autofunction:: extra_platforms.is_sparc64

   **Associated trait**: `SPARC64 <architectures.html#extra_platforms.SPARC64>`_

.. autofunction:: extra_platforms.is_sunos

   **Associated trait**: `SUNOS <platforms.html#extra_platforms.SUNOS>`_

.. autofunction:: extra_platforms.is_teamcity

   **Associated trait**: `TEAMCITY <ci.html#extra_platforms.TEAMCITY>`_

.. autofunction:: extra_platforms.is_travis_ci

   **Associated trait**: `TRAVIS_CI <ci.html#extra_platforms.TRAVIS_CI>`_

.. autofunction:: extra_platforms.is_tumbleweed

   **Associated trait**: `TUMBLEWEED <platforms.html#extra_platforms.TUMBLEWEED>`_

.. autofunction:: extra_platforms.is_tuxedo

   **Associated trait**: `TUXEDO <platforms.html#extra_platforms.TUXEDO>`_

.. autofunction:: extra_platforms.is_ubuntu

   **Associated trait**: `UBUNTU <platforms.html#extra_platforms.UBUNTU>`_

.. autofunction:: extra_platforms.is_ultramarine

   **Associated trait**: `ULTRAMARINE <platforms.html#extra_platforms.ULTRAMARINE>`_

.. autofunction:: extra_platforms.is_unknown_architecture

   **Associated trait**: `UNKNOWN_ARCHITECTURE <architectures.html#extra_platforms.UNKNOWN_ARCHITECTURE>`_

.. autofunction:: extra_platforms.is_unknown_ci

   **Associated trait**: `UNKNOWN_CI <ci.html#extra_platforms.UNKNOWN_CI>`_

.. autofunction:: extra_platforms.is_unknown_platform

   **Associated trait**: `UNKNOWN_PLATFORM <platforms.html#extra_platforms.UNKNOWN_PLATFORM>`_

.. autofunction:: extra_platforms.is_wasm32

   **Associated trait**: `WASM32 <architectures.html#extra_platforms.WASM32>`_

.. autofunction:: extra_platforms.is_wasm64

   **Associated trait**: `WASM64 <architectures.html#extra_platforms.WASM64>`_

.. autofunction:: extra_platforms.is_windows

   **Associated trait**: `WINDOWS <platforms.html#extra_platforms.WINDOWS>`_

.. autofunction:: extra_platforms.is_wsl1

   **Associated trait**: `WSL1 <platforms.html#extra_platforms.WSL1>`_

.. autofunction:: extra_platforms.is_wsl2

   **Associated trait**: `WSL2 <platforms.html#extra_platforms.WSL2>`_

.. autofunction:: extra_platforms.is_x86_64

   **Associated trait**: `X86_64 <architectures.html#extra_platforms.X86_64>`_

.. autofunction:: extra_platforms.is_xenserver

   **Associated trait**: `XENSERVER <platforms.html#extra_platforms.XENSERVER>`_
```

<!-- trait-detection-autofunction-end -->

## Group detection functions

Contrary to individual trait detection functions like `is_linux()` or `is_x86_64()`, group detection functions check for membership in a collection of traits.

These functions are dynamically generated for each [group](groups.md) and test whether **at least one trait** from the group matches the current system:

<!-- group-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_all_architectures

   **Associated group**: `ALL_ARCHITECTURES <groups.html#extra_platforms.ALL_ARCHITECTURES>`_

.. autofunction:: extra_platforms.is_all_ci

   **Associated group**: `ALL_CI <groups.html#extra_platforms.ALL_CI>`_

.. autofunction:: extra_platforms.is_all_platforms

   **Associated group**: `ALL_PLATFORMS <groups.html#extra_platforms.ALL_PLATFORMS>`_

.. autofunction:: extra_platforms.is_all_traits

   **Associated group**: `ALL_TRAITS <groups.html#extra_platforms.ALL_TRAITS>`_

.. autofunction:: extra_platforms.is_any_arm

   **Associated group**: `ANY_ARM <groups.html#extra_platforms.ANY_ARM>`_

.. autofunction:: extra_platforms.is_any_mips

   **Associated group**: `ANY_MIPS <groups.html#extra_platforms.ANY_MIPS>`_

.. autofunction:: extra_platforms.is_any_sparc

   **Associated group**: `ANY_SPARC <groups.html#extra_platforms.ANY_SPARC>`_

.. autofunction:: extra_platforms.is_any_windows

   **Associated group**: `ANY_WINDOWS <groups.html#extra_platforms.ANY_WINDOWS>`_

.. autofunction:: extra_platforms.is_arch_32_bit

   **Associated group**: `ARCH_32_BIT <groups.html#extra_platforms.ARCH_32_BIT>`_

.. autofunction:: extra_platforms.is_arch_64_bit

   **Associated group**: `ARCH_64_BIT <groups.html#extra_platforms.ARCH_64_BIT>`_

.. autofunction:: extra_platforms.is_bsd

   **Associated group**: `BSD <groups.html#extra_platforms.BSD>`_

.. autofunction:: extra_platforms.is_bsd_without_macos

   **Associated group**: `BSD_WITHOUT_MACOS <groups.html#extra_platforms.BSD_WITHOUT_MACOS>`_

.. autofunction:: extra_platforms.is_ibm_mainframe

   **Associated group**: `IBM_MAINFRAME <groups.html#extra_platforms.IBM_MAINFRAME>`_

.. autofunction:: extra_platforms.is_linux

   **Associated group**: `LINUX <groups.html#extra_platforms.LINUX>`_

.. autofunction:: extra_platforms.is_linux_layers

   **Associated group**: `LINUX_LAYERS <groups.html#extra_platforms.LINUX_LAYERS>`_

.. autofunction:: extra_platforms.is_linux_like

   **Associated group**: `LINUX_LIKE <groups.html#extra_platforms.LINUX_LIKE>`_

.. autofunction:: extra_platforms.is_loongarch

   **Associated group**: `LOONGARCH <groups.html#extra_platforms.LOONGARCH>`_

.. autofunction:: extra_platforms.is_other_unix

   **Associated group**: `OTHER_UNIX <groups.html#extra_platforms.OTHER_UNIX>`_

.. autofunction:: extra_platforms.is_powerpc

   **Associated group**: `POWERPC <groups.html#extra_platforms.POWERPC>`_

.. autofunction:: extra_platforms.is_riscv

   **Associated group**: `RISCV <groups.html#extra_platforms.RISCV>`_

.. autofunction:: extra_platforms.is_system_v

   **Associated group**: `SYSTEM_V <groups.html#extra_platforms.SYSTEM_V>`_

.. autofunction:: extra_platforms.is_unix

   **Associated group**: `UNIX <groups.html#extra_platforms.UNIX>`_

.. autofunction:: extra_platforms.is_unix_layers

   **Associated group**: `UNIX_LAYERS <groups.html#extra_platforms.UNIX_LAYERS>`_

.. autofunction:: extra_platforms.is_unix_without_macos

   **Associated group**: `UNIX_WITHOUT_MACOS <groups.html#extra_platforms.UNIX_WITHOUT_MACOS>`_

.. autofunction:: extra_platforms.is_unknown

   **Associated group**: `UNKNOWN <groups.html#extra_platforms.UNKNOWN>`_

.. autofunction:: extra_platforms.is_webassembly

   **Associated group**: `WEBASSEMBLY <groups.html#extra_platforms.WEBASSEMBLY>`_

.. autofunction:: extra_platforms.is_x86

   **Associated group**: `X86 <groups.html#extra_platforms.X86>`_
```

<!-- group-detection-autofunction-end -->
