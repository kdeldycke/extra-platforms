# {octicon}`meter` Pytest

````{important}
For these helpers to work, you need to install ``extra_platforms``'s additional dependencies from the ``pytest`` extra group:

```shell-session
$ pip install extra_platforms[pytest]
```
````

## Usage

- `@skip_<id>` — Skips the test when running on that platform/architecture/CI system
- `@unless_<id>` — Skips the test *unless* running on that platform/architecture/CI system

Skip a test on Windows:

```python
import pytest
from extra_platforms.pytest import skip_windows


@skip_windows
def test_unix_only():
    # This test will be skipped on Windows
    pass
```

Run a test only on Linux:

```python
import pytest
from extra_platforms.pytest import unless_linux


@unless_linux
def test_linux_only():
    # This test will be skipped unless running on Linux
    pass
```

Skip a test on specific architectures:

```python
import pytest
from extra_platforms.pytest import skip_aarch64


@skip_aarch64
def test_not_on_arm64():
    # This test will be skipped on ARM64 (AArch64)
    pass
```

Skip a test in CI environments:

```python
import pytest
from extra_platforms.pytest import skip_github_ci


@skip_github_ci
def test_not_in_github_actions():
    # This test will be skipped when running in GitHub Actions
    pass
```

## All decorators

<!-- decorators-table-start -->

| Skip decorator                                                                             | Unless decorator                                                                               | Icon | Associated symbol                                                               |
| :----------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- | :--: | :------------------------------------------------------------------------------ |
| [`@skip_aarch64`](pytest.md#extra_platforms.pytest.skip_aarch64)                           | [`@unless_aarch64`](pytest.md#extra_platforms.pytest.unless_aarch64)                           |  📱  | [`AARCH64`](architectures.md#extra_platforms.AARCH64)                           |
| [`@skip_aix`](pytest.md#extra_platforms.pytest.skip_aix)                                   | [`@unless_aix`](pytest.md#extra_platforms.pytest.unless_aix)                                   |  ➿  | [`AIX`](platforms.md#extra_platforms.AIX)                                       |
| [`@skip_all_architectures`](pytest.md#extra_platforms.pytest.skip_all_architectures)       | [`@unless_any_architecture`](pytest.md#extra_platforms.pytest.unless_any_architecture)         |  🏛️  | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.ALL_ARCHITECTURES)              |
| [`@skip_all_arm`](pytest.md#extra_platforms.pytest.skip_all_arm)                           | [`@unless_any_arm`](pytest.md#extra_platforms.pytest.unless_any_arm)                           |  📱  | [`ALL_ARM`](groups.md#extra_platforms.ALL_ARM)                                  |
| [`@skip_all_ci`](pytest.md#extra_platforms.pytest.skip_all_ci)                             | [`@unless_any_ci`](pytest.md#extra_platforms.pytest.unless_any_ci)                             |  ♺   | [`ALL_CI`](groups.md#extra_platforms.ALL_CI)                                    |
| [`@skip_all_mips`](pytest.md#extra_platforms.pytest.skip_all_mips)                         | [`@unless_any_mips`](pytest.md#extra_platforms.pytest.unless_any_mips)                         |  🔲  | [`ALL_MIPS`](groups.md#extra_platforms.ALL_MIPS)                                |
| [`@skip_all_platforms`](pytest.md#extra_platforms.pytest.skip_all_platforms)               | [`@unless_any_platform`](pytest.md#extra_platforms.pytest.unless_any_platform)                 |  ⚙️  | [`ALL_PLATFORMS`](groups.md#extra_platforms.ALL_PLATFORMS)                      |
| [`@skip_all_sparc`](pytest.md#extra_platforms.pytest.skip_all_sparc)                       | [`@unless_any_sparc`](pytest.md#extra_platforms.pytest.unless_any_sparc)                       |  ☀️  | [`ALL_SPARC`](groups.md#extra_platforms.ALL_SPARC)                              |
| [`@skip_all_traits`](pytest.md#extra_platforms.pytest.skip_all_traits)                     | [`@unless_any_trait`](pytest.md#extra_platforms.pytest.unless_any_trait)                       |  ⁕   | [`ALL_TRAITS`](groups.md#extra_platforms.ALL_TRAITS)                            |
| [`@skip_all_windows`](pytest.md#extra_platforms.pytest.skip_all_windows)                   | [`@unless_any_windows`](pytest.md#extra_platforms.pytest.unless_any_windows)                   |  🪟  | [`ALL_WINDOWS`](groups.md#extra_platforms.ALL_WINDOWS)                          |
| [`@skip_altlinux`](pytest.md#extra_platforms.pytest.skip_altlinux)                         | [`@unless_altlinux`](pytest.md#extra_platforms.pytest.unless_altlinux)                         |  🐧  | [`ALTLINUX`](platforms.md#extra_platforms.ALTLINUX)                             |
| [`@skip_amzn`](pytest.md#extra_platforms.pytest.skip_amzn)                                 | [`@unless_amzn`](pytest.md#extra_platforms.pytest.unless_amzn)                                 |  ⤻   | [`AMZN`](platforms.md#extra_platforms.AMZN)                                     |
| [`@skip_android`](pytest.md#extra_platforms.pytest.skip_android)                           | [`@unless_android`](pytest.md#extra_platforms.pytest.unless_android)                           |  🤖  | [`ANDROID`](platforms.md#extra_platforms.ANDROID)                               |
| [`@skip_arch`](pytest.md#extra_platforms.pytest.skip_arch)                                 | [`@unless_arch`](pytest.md#extra_platforms.pytest.unless_arch)                                 |  🎗️  | [`ARCH`](platforms.md#extra_platforms.ARCH)                                     |
| [`@skip_arch_32_bit`](pytest.md#extra_platforms.pytest.skip_arch_32_bit)                   | [`@unless_arch_32_bit`](pytest.md#extra_platforms.pytest.unless_arch_32_bit)                   |  ³²  | [`ARCH_32_BIT`](groups.md#extra_platforms.ARCH_32_BIT)                          |
| [`@skip_arch_64_bit`](pytest.md#extra_platforms.pytest.skip_arch_64_bit)                   | [`@unless_arch_64_bit`](pytest.md#extra_platforms.pytest.unless_arch_64_bit)                   |  ⁶⁴  | [`ARCH_64_BIT`](groups.md#extra_platforms.ARCH_64_BIT)                          |
| [`@skip_arm`](pytest.md#extra_platforms.pytest.skip_arm)                                   | [`@unless_arm`](pytest.md#extra_platforms.pytest.unless_arm)                                   |  📱  | [`ARM`](architectures.md#extra_platforms.ARM)                                   |
| [`@skip_armv5tel`](pytest.md#extra_platforms.pytest.skip_armv5tel)                         | [`@unless_armv5tel`](pytest.md#extra_platforms.pytest.unless_armv5tel)                         |  📱  | [`ARMV5TEL`](architectures.md#extra_platforms.ARMV5TEL)                         |
| [`@skip_armv6l`](pytest.md#extra_platforms.pytest.skip_armv6l)                             | [`@unless_armv6l`](pytest.md#extra_platforms.pytest.unless_armv6l)                             |  📱  | [`ARMV6L`](architectures.md#extra_platforms.ARMV6L)                             |
| [`@skip_armv7l`](pytest.md#extra_platforms.pytest.skip_armv7l)                             | [`@unless_armv7l`](pytest.md#extra_platforms.pytest.unless_armv7l)                             |  📱  | [`ARMV7L`](architectures.md#extra_platforms.ARMV7L)                             |
| [`@skip_armv8l`](pytest.md#extra_platforms.pytest.skip_armv8l)                             | [`@unless_armv8l`](pytest.md#extra_platforms.pytest.unless_armv8l)                             |  📱  | [`ARMV8L`](architectures.md#extra_platforms.ARMV8L)                             |
| [`@skip_azure_pipelines`](pytest.md#extra_platforms.pytest.skip_azure_pipelines)           | [`@unless_azure_pipelines`](pytest.md#extra_platforms.pytest.unless_azure_pipelines)           |  ═   | [`AZURE_PIPELINES`](ci.md#extra_platforms.AZURE_PIPELINES)                      |
| [`@skip_bamboo`](pytest.md#extra_platforms.pytest.skip_bamboo)                             | [`@unless_bamboo`](pytest.md#extra_platforms.pytest.unless_bamboo)                             |  ⟲   | [`BAMBOO`](ci.md#extra_platforms.BAMBOO)                                        |
| [`@skip_bsd`](pytest.md#extra_platforms.pytest.skip_bsd)                                   | [`@unless_bsd`](pytest.md#extra_platforms.pytest.unless_bsd)                                   | 🅱️+  | [`BSD`](groups.md#extra_platforms.BSD)                                          |
| [`@skip_bsd_without_macos`](pytest.md#extra_platforms.pytest.skip_bsd_without_macos)       | [`@unless_bsd_without_macos`](pytest.md#extra_platforms.pytest.unless_bsd_without_macos)       |  🅱️  | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.BSD_WITHOUT_MACOS)              |
| [`@skip_buildkite`](pytest.md#extra_platforms.pytest.skip_buildkite)                       | [`@unless_buildkite`](pytest.md#extra_platforms.pytest.unless_buildkite)                       |  🪁  | [`BUILDKITE`](ci.md#extra_platforms.BUILDKITE)                                  |
| [`@skip_buildroot`](pytest.md#extra_platforms.pytest.skip_buildroot)                       | [`@unless_buildroot`](pytest.md#extra_platforms.pytest.unless_buildroot)                       |  ⛑️  | [`BUILDROOT`](platforms.md#extra_platforms.BUILDROOT)                           |
| [`@skip_cachyos`](pytest.md#extra_platforms.pytest.skip_cachyos)                           | [`@unless_cachyos`](pytest.md#extra_platforms.pytest.unless_cachyos)                           |  ⌬   | [`CACHYOS`](platforms.md#extra_platforms.CACHYOS)                               |
| [`@skip_centos`](pytest.md#extra_platforms.pytest.skip_centos)                             | [`@unless_centos`](pytest.md#extra_platforms.pytest.unless_centos)                             |  💠  | [`CENTOS`](platforms.md#extra_platforms.CENTOS)                                 |
| [`@skip_circle_ci`](pytest.md#extra_platforms.pytest.skip_circle_ci)                       | [`@unless_circle_ci`](pytest.md#extra_platforms.pytest.unless_circle_ci)                       |  ⪾   | [`CIRCLE_CI`](ci.md#extra_platforms.CIRCLE_CI)                                  |
| [`@skip_cirrus_ci`](pytest.md#extra_platforms.pytest.skip_cirrus_ci)                       | [`@unless_cirrus_ci`](pytest.md#extra_platforms.pytest.unless_cirrus_ci)                       |  ≋   | [`CIRRUS_CI`](ci.md#extra_platforms.CIRRUS_CI)                                  |
| [`@skip_cloudlinux`](pytest.md#extra_platforms.pytest.skip_cloudlinux)                     | [`@unless_cloudlinux`](pytest.md#extra_platforms.pytest.unless_cloudlinux)                     |  ꩜   | [`CLOUDLINUX`](platforms.md#extra_platforms.CLOUDLINUX)                         |
| [`@skip_codebuild`](pytest.md#extra_platforms.pytest.skip_codebuild)                       | [`@unless_codebuild`](pytest.md#extra_platforms.pytest.unless_codebuild)                       |  ᚙ   | [`CODEBUILD`](ci.md#extra_platforms.CODEBUILD)                                  |
| [`@skip_cygwin`](pytest.md#extra_platforms.pytest.skip_cygwin)                             | [`@unless_cygwin`](pytest.md#extra_platforms.pytest.unless_cygwin)                             |  Ͼ   | [`CYGWIN`](platforms.md#extra_platforms.CYGWIN)                                 |
| [`@skip_debian`](pytest.md#extra_platforms.pytest.skip_debian)                             | [`@unless_debian`](pytest.md#extra_platforms.pytest.unless_debian)                             |  🌀  | [`DEBIAN`](platforms.md#extra_platforms.DEBIAN)                                 |
| [`@skip_dragonflybsd`](pytest.md#extra_platforms.pytest.skip_dragonflybsd)                 | [`@unless_dragonflybsd`](pytest.md#extra_platforms.pytest.unless_dragonflybsd)                 |  🪰  | [`DRAGONFLYBSD`](platforms.md#extra_platforms.DRAGONFLYBSD)                     |
| [`@skip_exherbo`](pytest.md#extra_platforms.pytest.skip_exherbo)                           | [`@unless_exherbo`](pytest.md#extra_platforms.pytest.unless_exherbo)                           |  🐽  | [`EXHERBO`](platforms.md#extra_platforms.EXHERBO)                               |
| [`@skip_fedora`](pytest.md#extra_platforms.pytest.skip_fedora)                             | [`@unless_fedora`](pytest.md#extra_platforms.pytest.unless_fedora)                             |  🎩  | [`FEDORA`](platforms.md#extra_platforms.FEDORA)                                 |
| [`@skip_freebsd`](pytest.md#extra_platforms.pytest.skip_freebsd)                           | [`@unless_freebsd`](pytest.md#extra_platforms.pytest.unless_freebsd)                           |  😈  | [`FREEBSD`](platforms.md#extra_platforms.FREEBSD)                               |
| [`@skip_gentoo`](pytest.md#extra_platforms.pytest.skip_gentoo)                             | [`@unless_gentoo`](pytest.md#extra_platforms.pytest.unless_gentoo)                             |  🗜️  | [`GENTOO`](platforms.md#extra_platforms.GENTOO)                                 |
| [`@skip_github_ci`](pytest.md#extra_platforms.pytest.skip_github_ci)                       | [`@unless_github_ci`](pytest.md#extra_platforms.pytest.unless_github_ci)                       |  🐙  | [`GITHUB_CI`](ci.md#extra_platforms.GITHUB_CI)                                  |
| [`@skip_gitlab_ci`](pytest.md#extra_platforms.pytest.skip_gitlab_ci)                       | [`@unless_gitlab_ci`](pytest.md#extra_platforms.pytest.unless_gitlab_ci)                       |  🦊  | [`GITLAB_CI`](ci.md#extra_platforms.GITLAB_CI)                                  |
| [`@skip_guix`](pytest.md#extra_platforms.pytest.skip_guix)                                 | [`@unless_guix`](pytest.md#extra_platforms.pytest.unless_guix)                                 |  🐃  | [`GUIX`](platforms.md#extra_platforms.GUIX)                                     |
| [`@skip_haiku`](pytest.md#extra_platforms.pytest.skip_haiku)                               | [`@unless_haiku`](pytest.md#extra_platforms.pytest.unless_haiku)                               |  🍂  | [`HAIKU`](platforms.md#extra_platforms.HAIKU)                                   |
| [`@skip_heroku_ci`](pytest.md#extra_platforms.pytest.skip_heroku_ci)                       | [`@unless_heroku_ci`](pytest.md#extra_platforms.pytest.unless_heroku_ci)                       |  ⥁   | [`HEROKU_CI`](ci.md#extra_platforms.HEROKU_CI)                                  |
| [`@skip_hurd`](pytest.md#extra_platforms.pytest.skip_hurd)                                 | [`@unless_hurd`](pytest.md#extra_platforms.pytest.unless_hurd)                                 |  🐃  | [`HURD`](platforms.md#extra_platforms.HURD)                                     |
| [`@skip_i386`](pytest.md#extra_platforms.pytest.skip_i386)                                 | [`@unless_i386`](pytest.md#extra_platforms.pytest.unless_i386)                                 |  𝗶   | [`I386`](architectures.md#extra_platforms.I386)                                 |
| [`@skip_i586`](pytest.md#extra_platforms.pytest.skip_i586)                                 | [`@unless_i586`](pytest.md#extra_platforms.pytest.unless_i586)                                 |  𝗶   | [`I586`](architectures.md#extra_platforms.I586)                                 |
| [`@skip_i686`](pytest.md#extra_platforms.pytest.skip_i686)                                 | [`@unless_i686`](pytest.md#extra_platforms.pytest.unless_i686)                                 |  𝗶   | [`I686`](architectures.md#extra_platforms.I686)                                 |
| [`@skip_ibm_mainframe`](pytest.md#extra_platforms.pytest.skip_ibm_mainframe)               | [`@unless_ibm_mainframe`](pytest.md#extra_platforms.pytest.unless_ibm_mainframe)               |  🏢  | [`IBM_MAINFRAME`](groups.md#extra_platforms.IBM_MAINFRAME)                      |
| [`@skip_ibm_powerkvm`](pytest.md#extra_platforms.pytest.skip_ibm_powerkvm)                 | [`@unless_ibm_powerkvm`](pytest.md#extra_platforms.pytest.unless_ibm_powerkvm)                 |  🤹  | [`IBM_POWERKVM`](platforms.md#extra_platforms.IBM_POWERKVM)                     |
| [`@skip_illumos`](pytest.md#extra_platforms.pytest.skip_illumos)                           | [`@unless_illumos`](pytest.md#extra_platforms.pytest.unless_illumos)                           |  🔥  | [`ILLUMOS`](platforms.md#extra_platforms.ILLUMOS)                               |
| [`@skip_kvmibm`](pytest.md#extra_platforms.pytest.skip_kvmibm)                             | [`@unless_kvmibm`](pytest.md#extra_platforms.pytest.unless_kvmibm)                             |  🤹  | [`KVMIBM`](platforms.md#extra_platforms.KVMIBM)                                 |
| [`@skip_linux`](pytest.md#extra_platforms.pytest.skip_linux)                               | [`@unless_linux`](pytest.md#extra_platforms.pytest.unless_linux)                               |  🐧  | [`LINUX`](groups.md#extra_platforms.LINUX)                                      |
| [`@skip_linux_layers`](pytest.md#extra_platforms.pytest.skip_linux_layers)                 | [`@unless_linux_layers`](pytest.md#extra_platforms.pytest.unless_linux_layers)                 |  ≚   | [`LINUX_LAYERS`](groups.md#extra_platforms.LINUX_LAYERS)                        |
| [`@skip_linux_like`](pytest.md#extra_platforms.pytest.skip_linux_like)                     | [`@unless_linux_like`](pytest.md#extra_platforms.pytest.unless_linux_like)                     | 🐧+  | [`LINUX_LIKE`](groups.md#extra_platforms.LINUX_LIKE)                            |
| [`@skip_linuxmint`](pytest.md#extra_platforms.pytest.skip_linuxmint)                       | [`@unless_linuxmint`](pytest.md#extra_platforms.pytest.unless_linuxmint)                       |  🌿  | [`LINUXMINT`](platforms.md#extra_platforms.LINUXMINT)                           |
| [`@skip_loongarch`](pytest.md#extra_platforms.pytest.skip_loongarch)                       | [`@unless_loongarch`](pytest.md#extra_platforms.pytest.unless_loongarch)                       |  🐉  | [`LOONGARCH`](groups.md#extra_platforms.LOONGARCH)                              |
| [`@skip_loongarch64`](pytest.md#extra_platforms.pytest.skip_loongarch64)                   | [`@unless_loongarch64`](pytest.md#extra_platforms.pytest.unless_loongarch64)                   |  🐉  | [`LOONGARCH64`](architectures.md#extra_platforms.LOONGARCH64)                   |
| [`@skip_macos`](pytest.md#extra_platforms.pytest.skip_macos)                               | [`@unless_macos`](pytest.md#extra_platforms.pytest.unless_macos)                               |  🍎  | [`MACOS`](platforms.md#extra_platforms.MACOS)                                   |
| [`@skip_mageia`](pytest.md#extra_platforms.pytest.skip_mageia)                             | [`@unless_mageia`](pytest.md#extra_platforms.pytest.unless_mageia)                             |  ⍥   | [`MAGEIA`](platforms.md#extra_platforms.MAGEIA)                                 |
| [`@skip_mandriva`](pytest.md#extra_platforms.pytest.skip_mandriva)                         | [`@unless_mandriva`](pytest.md#extra_platforms.pytest.unless_mandriva)                         |  💫  | [`MANDRIVA`](platforms.md#extra_platforms.MANDRIVA)                             |
| [`@skip_midnightbsd`](pytest.md#extra_platforms.pytest.skip_midnightbsd)                   | [`@unless_midnightbsd`](pytest.md#extra_platforms.pytest.unless_midnightbsd)                   |  🌘  | [`MIDNIGHTBSD`](platforms.md#extra_platforms.MIDNIGHTBSD)                       |
| [`@skip_mips`](pytest.md#extra_platforms.pytest.skip_mips)                                 | [`@unless_mips`](pytest.md#extra_platforms.pytest.unless_mips)                                 |  🔲  | [`MIPS`](architectures.md#extra_platforms.MIPS)                                 |
| [`@skip_mips64`](pytest.md#extra_platforms.pytest.skip_mips64)                             | [`@unless_mips64`](pytest.md#extra_platforms.pytest.unless_mips64)                             |  🔲  | [`MIPS64`](architectures.md#extra_platforms.MIPS64)                             |
| [`@skip_mips64el`](pytest.md#extra_platforms.pytest.skip_mips64el)                         | [`@unless_mips64el`](pytest.md#extra_platforms.pytest.unless_mips64el)                         |  🔲  | [`MIPS64EL`](architectures.md#extra_platforms.MIPS64EL)                         |
| [`@skip_mipsel`](pytest.md#extra_platforms.pytest.skip_mipsel)                             | [`@unless_mipsel`](pytest.md#extra_platforms.pytest.unless_mipsel)                             |  🔲  | [`MIPSEL`](architectures.md#extra_platforms.MIPSEL)                             |
| [`@skip_netbsd`](pytest.md#extra_platforms.pytest.skip_netbsd)                             | [`@unless_netbsd`](pytest.md#extra_platforms.pytest.unless_netbsd)                             |  🚩  | [`NETBSD`](platforms.md#extra_platforms.NETBSD)                                 |
| [`@skip_nobara`](pytest.md#extra_platforms.pytest.skip_nobara)                             | [`@unless_nobara`](pytest.md#extra_platforms.pytest.unless_nobara)                             |     | [`NOBARA`](platforms.md#extra_platforms.NOBARA)                                 |
| [`@skip_openbsd`](pytest.md#extra_platforms.pytest.skip_openbsd)                           | [`@unless_openbsd`](pytest.md#extra_platforms.pytest.unless_openbsd)                           |  🐡  | [`OPENBSD`](platforms.md#extra_platforms.OPENBSD)                               |
| [`@skip_opensuse`](pytest.md#extra_platforms.pytest.skip_opensuse)                         | [`@unless_opensuse`](pytest.md#extra_platforms.pytest.unless_opensuse)                         |  🦎  | [`OPENSUSE`](platforms.md#extra_platforms.OPENSUSE)                             |
| [`@skip_oracle`](pytest.md#extra_platforms.pytest.skip_oracle)                             | [`@unless_oracle`](pytest.md#extra_platforms.pytest.unless_oracle)                             |  🦴  | [`ORACLE`](platforms.md#extra_platforms.ORACLE)                                 |
| [`@skip_other_unix`](pytest.md#extra_platforms.pytest.skip_other_unix)                     | [`@unless_other_unix`](pytest.md#extra_platforms.pytest.unless_other_unix)                     |  ⊎   | [`OTHER_UNIX`](groups.md#extra_platforms.OTHER_UNIX)                            |
| [`@skip_parallels`](pytest.md#extra_platforms.pytest.skip_parallels)                       | [`@unless_parallels`](pytest.md#extra_platforms.pytest.unless_parallels)                       |  ∥   | [`PARALLELS`](platforms.md#extra_platforms.PARALLELS)                           |
| [`@skip_pidora`](pytest.md#extra_platforms.pytest.skip_pidora)                             | [`@unless_pidora`](pytest.md#extra_platforms.pytest.unless_pidora)                             |  🍓  | [`PIDORA`](platforms.md#extra_platforms.PIDORA)                                 |
| [`@skip_powerpc`](pytest.md#extra_platforms.pytest.skip_powerpc)                           | [`@unless_powerpc`](pytest.md#extra_platforms.pytest.unless_powerpc)                           |  ⚡  | [`POWERPC`](groups.md#extra_platforms.POWERPC)                                  |
| [`@skip_ppc`](pytest.md#extra_platforms.pytest.skip_ppc)                                   | [`@unless_ppc`](pytest.md#extra_platforms.pytest.unless_ppc)                                   |  ⚡  | [`PPC`](architectures.md#extra_platforms.PPC)                                   |
| [`@skip_ppc64`](pytest.md#extra_platforms.pytest.skip_ppc64)                               | [`@unless_ppc64`](pytest.md#extra_platforms.pytest.unless_ppc64)                               |  ⚡  | [`PPC64`](architectures.md#extra_platforms.PPC64)                               |
| [`@skip_ppc64le`](pytest.md#extra_platforms.pytest.skip_ppc64le)                           | [`@unless_ppc64le`](pytest.md#extra_platforms.pytest.unless_ppc64le)                           |  ⚡  | [`PPC64LE`](architectures.md#extra_platforms.PPC64LE)                           |
| [`@skip_raspbian`](pytest.md#extra_platforms.pytest.skip_raspbian)                         | [`@unless_raspbian`](pytest.md#extra_platforms.pytest.unless_raspbian)                         |  🍓  | [`RASPBIAN`](platforms.md#extra_platforms.RASPBIAN)                             |
| [`@skip_rhel`](pytest.md#extra_platforms.pytest.skip_rhel)                                 | [`@unless_rhel`](pytest.md#extra_platforms.pytest.unless_rhel)                                 |  🎩  | [`RHEL`](platforms.md#extra_platforms.RHEL)                                     |
| [`@skip_riscv`](pytest.md#extra_platforms.pytest.skip_riscv)                               | [`@unless_riscv`](pytest.md#extra_platforms.pytest.unless_riscv)                               |  Ⅴ   | [`RISCV`](groups.md#extra_platforms.RISCV)                                      |
| [`@skip_riscv32`](pytest.md#extra_platforms.pytest.skip_riscv32)                           | [`@unless_riscv32`](pytest.md#extra_platforms.pytest.unless_riscv32)                           |  Ⅴ   | [`RISCV32`](architectures.md#extra_platforms.RISCV32)                           |
| [`@skip_riscv64`](pytest.md#extra_platforms.pytest.skip_riscv64)                           | [`@unless_riscv64`](pytest.md#extra_platforms.pytest.unless_riscv64)                           |  Ⅴ   | [`RISCV64`](architectures.md#extra_platforms.RISCV64)                           |
| [`@skip_rocky`](pytest.md#extra_platforms.pytest.skip_rocky)                               | [`@unless_rocky`](pytest.md#extra_platforms.pytest.unless_rocky)                               |  ⛰️  | [`ROCKY`](platforms.md#extra_platforms.ROCKY)                                   |
| [`@skip_s390x`](pytest.md#extra_platforms.pytest.skip_s390x)                               | [`@unless_s390x`](pytest.md#extra_platforms.pytest.unless_s390x)                               |  🏢  | [`S390X`](architectures.md#extra_platforms.S390X)                               |
| [`@skip_scientific`](pytest.md#extra_platforms.pytest.skip_scientific)                     | [`@unless_scientific`](pytest.md#extra_platforms.pytest.unless_scientific)                     |  ⚛️  | [`SCIENTIFIC`](platforms.md#extra_platforms.SCIENTIFIC)                         |
| [`@skip_slackware`](pytest.md#extra_platforms.pytest.skip_slackware)                       | [`@unless_slackware`](pytest.md#extra_platforms.pytest.unless_slackware)                       |  🚬  | [`SLACKWARE`](platforms.md#extra_platforms.SLACKWARE)                           |
| [`@skip_sles`](pytest.md#extra_platforms.pytest.skip_sles)                                 | [`@unless_sles`](pytest.md#extra_platforms.pytest.unless_sles)                                 |  🦎  | [`SLES`](platforms.md#extra_platforms.SLES)                                     |
| [`@skip_solaris`](pytest.md#extra_platforms.pytest.skip_solaris)                           | [`@unless_solaris`](pytest.md#extra_platforms.pytest.unless_solaris)                           |  🌞  | [`SOLARIS`](platforms.md#extra_platforms.SOLARIS)                               |
| [`@skip_sparc`](pytest.md#extra_platforms.pytest.skip_sparc)                               | [`@unless_sparc`](pytest.md#extra_platforms.pytest.unless_sparc)                               |  ☀️  | [`SPARC`](architectures.md#extra_platforms.SPARC)                               |
| [`@skip_sparc64`](pytest.md#extra_platforms.pytest.skip_sparc64)                           | [`@unless_sparc64`](pytest.md#extra_platforms.pytest.unless_sparc64)                           |  ☀️  | [`SPARC64`](architectures.md#extra_platforms.SPARC64)                           |
| [`@skip_sunos`](pytest.md#extra_platforms.pytest.skip_sunos)                               | [`@unless_sunos`](pytest.md#extra_platforms.pytest.unless_sunos)                               |  ☀️  | [`SUNOS`](platforms.md#extra_platforms.SUNOS)                                   |
| [`@skip_system_v`](pytest.md#extra_platforms.pytest.skip_system_v)                         | [`@unless_system_v`](pytest.md#extra_platforms.pytest.unless_system_v)                         |  𝐕   | [`SYSTEM_V`](groups.md#extra_platforms.SYSTEM_V)                                |
| [`@skip_teamcity`](pytest.md#extra_platforms.pytest.skip_teamcity)                         | [`@unless_teamcity`](pytest.md#extra_platforms.pytest.unless_teamcity)                         |  🏙️  | [`TEAMCITY`](ci.md#extra_platforms.TEAMCITY)                                    |
| [`@skip_travis_ci`](pytest.md#extra_platforms.pytest.skip_travis_ci)                       | [`@unless_travis_ci`](pytest.md#extra_platforms.pytest.unless_travis_ci)                       |  👷  | [`TRAVIS_CI`](ci.md#extra_platforms.TRAVIS_CI)                                  |
| [`@skip_tumbleweed`](pytest.md#extra_platforms.pytest.skip_tumbleweed)                     | [`@unless_tumbleweed`](pytest.md#extra_platforms.pytest.unless_tumbleweed)                     |  ↻   | [`TUMBLEWEED`](platforms.md#extra_platforms.TUMBLEWEED)                         |
| [`@skip_tuxedo`](pytest.md#extra_platforms.pytest.skip_tuxedo)                             | [`@unless_tuxedo`](pytest.md#extra_platforms.pytest.unless_tuxedo)                             |  🤵  | [`TUXEDO`](platforms.md#extra_platforms.TUXEDO)                                 |
| [`@skip_ubuntu`](pytest.md#extra_platforms.pytest.skip_ubuntu)                             | [`@unless_ubuntu`](pytest.md#extra_platforms.pytest.unless_ubuntu)                             |  🎯  | [`UBUNTU`](platforms.md#extra_platforms.UBUNTU)                                 |
| [`@skip_ultramarine`](pytest.md#extra_platforms.pytest.skip_ultramarine)                   | [`@unless_ultramarine`](pytest.md#extra_platforms.pytest.unless_ultramarine)                   |  🌊  | [`ULTRAMARINE`](platforms.md#extra_platforms.ULTRAMARINE)                       |
| [`@skip_unix`](pytest.md#extra_platforms.pytest.skip_unix)                                 | [`@unless_unix`](pytest.md#extra_platforms.pytest.unless_unix)                                 |  ⨷   | [`UNIX`](groups.md#extra_platforms.UNIX)                                        |
| [`@skip_unix_layers`](pytest.md#extra_platforms.pytest.skip_unix_layers)                   | [`@unless_unix_layers`](pytest.md#extra_platforms.pytest.unless_unix_layers)                   |  ≛   | [`UNIX_LAYERS`](groups.md#extra_platforms.UNIX_LAYERS)                          |
| [`@skip_unix_without_macos`](pytest.md#extra_platforms.pytest.skip_unix_without_macos)     | [`@unless_unix_without_macos`](pytest.md#extra_platforms.pytest.unless_unix_without_macos)     |  ⨂   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.UNIX_WITHOUT_MACOS)            |
| [`@skip_unknown`](pytest.md#extra_platforms.pytest.skip_unknown)                           | [`@unless_unknown`](pytest.md#extra_platforms.pytest.unless_unknown)                           |  ❓  | [`UNKNOWN`](groups.md#extra_platforms.UNKNOWN)                                  |
| [`@skip_unknown_architecture`](pytest.md#extra_platforms.pytest.skip_unknown_architecture) | [`@unless_unknown_architecture`](pytest.md#extra_platforms.pytest.unless_unknown_architecture) |  ❓  | [`UNKNOWN_ARCHITECTURE`](architectures.md#extra_platforms.UNKNOWN_ARCHITECTURE) |
| [`@skip_unknown_ci`](pytest.md#extra_platforms.pytest.skip_unknown_ci)                     | [`@unless_unknown_ci`](pytest.md#extra_platforms.pytest.unless_unknown_ci)                     |  ❓  | [`UNKNOWN_CI`](ci.md#extra_platforms.UNKNOWN_CI)                                |
| [`@skip_unknown_platform`](pytest.md#extra_platforms.pytest.skip_unknown_platform)         | [`@unless_unknown_platform`](pytest.md#extra_platforms.pytest.unless_unknown_platform)         |  ❓  | [`UNKNOWN_PLATFORM`](platforms.md#extra_platforms.UNKNOWN_PLATFORM)             |
| [`@skip_wasm32`](pytest.md#extra_platforms.pytest.skip_wasm32)                             | [`@unless_wasm32`](pytest.md#extra_platforms.pytest.unless_wasm32)                             |  🌐  | [`WASM32`](architectures.md#extra_platforms.WASM32)                             |
| [`@skip_wasm64`](pytest.md#extra_platforms.pytest.skip_wasm64)                             | [`@unless_wasm64`](pytest.md#extra_platforms.pytest.unless_wasm64)                             |  🌐  | [`WASM64`](architectures.md#extra_platforms.WASM64)                             |
| [`@skip_webassembly`](pytest.md#extra_platforms.pytest.skip_webassembly)                   | [`@unless_webassembly`](pytest.md#extra_platforms.pytest.unless_webassembly)                   |  🌐  | [`WEBASSEMBLY`](groups.md#extra_platforms.WEBASSEMBLY)                          |
| [`@skip_windows`](pytest.md#extra_platforms.pytest.skip_windows)                           | [`@unless_windows`](pytest.md#extra_platforms.pytest.unless_windows)                           |  🪟  | [`WINDOWS`](platforms.md#extra_platforms.WINDOWS)                               |
| [`@skip_wsl1`](pytest.md#extra_platforms.pytest.skip_wsl1)                                 | [`@unless_wsl1`](pytest.md#extra_platforms.pytest.unless_wsl1)                                 |  ⊞   | [`WSL1`](platforms.md#extra_platforms.WSL1)                                     |
| [`@skip_wsl2`](pytest.md#extra_platforms.pytest.skip_wsl2)                                 | [`@unless_wsl2`](pytest.md#extra_platforms.pytest.unless_wsl2)                                 |  ⊞   | [`WSL2`](platforms.md#extra_platforms.WSL2)                                     |
| [`@skip_x86`](pytest.md#extra_platforms.pytest.skip_x86)                                   | [`@unless_x86`](pytest.md#extra_platforms.pytest.unless_x86)                                   |  𝘅   | [`X86`](groups.md#extra_platforms.X86)                                          |
| [`@skip_x86_64`](pytest.md#extra_platforms.pytest.skip_x86_64)                             | [`@unless_x86_64`](pytest.md#extra_platforms.pytest.unless_x86_64)                             |  🖥️  | [`X86_64`](architectures.md#extra_platforms.X86_64)                             |
| [`@skip_xenserver`](pytest.md#extra_platforms.pytest.skip_xenserver)                       | [`@unless_xenserver`](pytest.md#extra_platforms.pytest.unless_xenserver)                       |  Ⓧ   | [`XENSERVER`](platforms.md#extra_platforms.XENSERVER)                           |

<!-- decorators-table-end -->

## Decorator reference

<!-- pytest-decorators-autodata-start -->

### Skip decorators

```{eval-rst}
.. autodata:: extra_platforms.pytest.skip_aarch64
.. autodata:: extra_platforms.pytest.skip_aix
.. autodata:: extra_platforms.pytest.skip_all_architectures
.. autodata:: extra_platforms.pytest.skip_all_arm
.. autodata:: extra_platforms.pytest.skip_all_ci
.. autodata:: extra_platforms.pytest.skip_all_mips
.. autodata:: extra_platforms.pytest.skip_all_platforms
.. autodata:: extra_platforms.pytest.skip_all_sparc
.. autodata:: extra_platforms.pytest.skip_all_traits
.. autodata:: extra_platforms.pytest.skip_all_windows
.. autodata:: extra_platforms.pytest.skip_altlinux
.. autodata:: extra_platforms.pytest.skip_amzn
.. autodata:: extra_platforms.pytest.skip_android
.. autodata:: extra_platforms.pytest.skip_arch
.. autodata:: extra_platforms.pytest.skip_arch_32_bit
.. autodata:: extra_platforms.pytest.skip_arch_64_bit
.. autodata:: extra_platforms.pytest.skip_arm
.. autodata:: extra_platforms.pytest.skip_armv5tel
.. autodata:: extra_platforms.pytest.skip_armv6l
.. autodata:: extra_platforms.pytest.skip_armv7l
.. autodata:: extra_platforms.pytest.skip_armv8l
.. autodata:: extra_platforms.pytest.skip_azure_pipelines
.. autodata:: extra_platforms.pytest.skip_bamboo
.. autodata:: extra_platforms.pytest.skip_bsd
.. autodata:: extra_platforms.pytest.skip_bsd_without_macos
.. autodata:: extra_platforms.pytest.skip_buildkite
.. autodata:: extra_platforms.pytest.skip_buildroot
.. autodata:: extra_platforms.pytest.skip_cachyos
.. autodata:: extra_platforms.pytest.skip_centos
.. autodata:: extra_platforms.pytest.skip_circle_ci
.. autodata:: extra_platforms.pytest.skip_cirrus_ci
.. autodata:: extra_platforms.pytest.skip_cloudlinux
.. autodata:: extra_platforms.pytest.skip_codebuild
.. autodata:: extra_platforms.pytest.skip_cygwin
.. autodata:: extra_platforms.pytest.skip_debian
.. autodata:: extra_platforms.pytest.skip_dragonflybsd
.. autodata:: extra_platforms.pytest.skip_exherbo
.. autodata:: extra_platforms.pytest.skip_fedora
.. autodata:: extra_platforms.pytest.skip_freebsd
.. autodata:: extra_platforms.pytest.skip_gentoo
.. autodata:: extra_platforms.pytest.skip_github_ci
.. autodata:: extra_platforms.pytest.skip_gitlab_ci
.. autodata:: extra_platforms.pytest.skip_guix
.. autodata:: extra_platforms.pytest.skip_haiku
.. autodata:: extra_platforms.pytest.skip_heroku_ci
.. autodata:: extra_platforms.pytest.skip_hurd
.. autodata:: extra_platforms.pytest.skip_i386
.. autodata:: extra_platforms.pytest.skip_i586
.. autodata:: extra_platforms.pytest.skip_i686
.. autodata:: extra_platforms.pytest.skip_ibm_mainframe
.. autodata:: extra_platforms.pytest.skip_ibm_powerkvm
.. autodata:: extra_platforms.pytest.skip_illumos
.. autodata:: extra_platforms.pytest.skip_kvmibm
.. autodata:: extra_platforms.pytest.skip_linux
.. autodata:: extra_platforms.pytest.skip_linux_layers
.. autodata:: extra_platforms.pytest.skip_linux_like
.. autodata:: extra_platforms.pytest.skip_linuxmint
.. autodata:: extra_platforms.pytest.skip_loongarch
.. autodata:: extra_platforms.pytest.skip_loongarch64
.. autodata:: extra_platforms.pytest.skip_macos
.. autodata:: extra_platforms.pytest.skip_mageia
.. autodata:: extra_platforms.pytest.skip_mandriva
.. autodata:: extra_platforms.pytest.skip_midnightbsd
.. autodata:: extra_platforms.pytest.skip_mips
.. autodata:: extra_platforms.pytest.skip_mips64
.. autodata:: extra_platforms.pytest.skip_mips64el
.. autodata:: extra_platforms.pytest.skip_mipsel
.. autodata:: extra_platforms.pytest.skip_netbsd
.. autodata:: extra_platforms.pytest.skip_nobara
.. autodata:: extra_platforms.pytest.skip_openbsd
.. autodata:: extra_platforms.pytest.skip_opensuse
.. autodata:: extra_platforms.pytest.skip_oracle
.. autodata:: extra_platforms.pytest.skip_other_unix
.. autodata:: extra_platforms.pytest.skip_parallels
.. autodata:: extra_platforms.pytest.skip_pidora
.. autodata:: extra_platforms.pytest.skip_powerpc
.. autodata:: extra_platforms.pytest.skip_ppc
.. autodata:: extra_platforms.pytest.skip_ppc64
.. autodata:: extra_platforms.pytest.skip_ppc64le
.. autodata:: extra_platforms.pytest.skip_raspbian
.. autodata:: extra_platforms.pytest.skip_rhel
.. autodata:: extra_platforms.pytest.skip_riscv
.. autodata:: extra_platforms.pytest.skip_riscv32
.. autodata:: extra_platforms.pytest.skip_riscv64
.. autodata:: extra_platforms.pytest.skip_rocky
.. autodata:: extra_platforms.pytest.skip_s390x
.. autodata:: extra_platforms.pytest.skip_scientific
.. autodata:: extra_platforms.pytest.skip_slackware
.. autodata:: extra_platforms.pytest.skip_sles
.. autodata:: extra_platforms.pytest.skip_solaris
.. autodata:: extra_platforms.pytest.skip_sparc
.. autodata:: extra_platforms.pytest.skip_sparc64
.. autodata:: extra_platforms.pytest.skip_sunos
.. autodata:: extra_platforms.pytest.skip_system_v
.. autodata:: extra_platforms.pytest.skip_teamcity
.. autodata:: extra_platforms.pytest.skip_travis_ci
.. autodata:: extra_platforms.pytest.skip_tumbleweed
.. autodata:: extra_platforms.pytest.skip_tuxedo
.. autodata:: extra_platforms.pytest.skip_ubuntu
.. autodata:: extra_platforms.pytest.skip_ultramarine
.. autodata:: extra_platforms.pytest.skip_unix
.. autodata:: extra_platforms.pytest.skip_unix_layers
.. autodata:: extra_platforms.pytest.skip_unix_without_macos
.. autodata:: extra_platforms.pytest.skip_unknown
.. autodata:: extra_platforms.pytest.skip_unknown_architecture
.. autodata:: extra_platforms.pytest.skip_unknown_ci
.. autodata:: extra_platforms.pytest.skip_unknown_platform
.. autodata:: extra_platforms.pytest.skip_wasm32
.. autodata:: extra_platforms.pytest.skip_wasm64
.. autodata:: extra_platforms.pytest.skip_webassembly
.. autodata:: extra_platforms.pytest.skip_windows
.. autodata:: extra_platforms.pytest.skip_wsl1
.. autodata:: extra_platforms.pytest.skip_wsl2
.. autodata:: extra_platforms.pytest.skip_x86
.. autodata:: extra_platforms.pytest.skip_x86_64
.. autodata:: extra_platforms.pytest.skip_xenserver
```

### Unless decorators

```{eval-rst}
.. autodata:: extra_platforms.pytest.unless_aarch64
.. autodata:: extra_platforms.pytest.unless_aix
.. autodata:: extra_platforms.pytest.unless_any_architecture
.. autodata:: extra_platforms.pytest.unless_any_arm
.. autodata:: extra_platforms.pytest.unless_any_ci
.. autodata:: extra_platforms.pytest.unless_any_mips
.. autodata:: extra_platforms.pytest.unless_any_platform
.. autodata:: extra_platforms.pytest.unless_any_sparc
.. autodata:: extra_platforms.pytest.unless_any_trait
.. autodata:: extra_platforms.pytest.unless_any_windows
.. autodata:: extra_platforms.pytest.unless_altlinux
.. autodata:: extra_platforms.pytest.unless_amzn
.. autodata:: extra_platforms.pytest.unless_android
.. autodata:: extra_platforms.pytest.unless_arch
.. autodata:: extra_platforms.pytest.unless_arch_32_bit
.. autodata:: extra_platforms.pytest.unless_arch_64_bit
.. autodata:: extra_platforms.pytest.unless_arm
.. autodata:: extra_platforms.pytest.unless_armv5tel
.. autodata:: extra_platforms.pytest.unless_armv6l
.. autodata:: extra_platforms.pytest.unless_armv7l
.. autodata:: extra_platforms.pytest.unless_armv8l
.. autodata:: extra_platforms.pytest.unless_azure_pipelines
.. autodata:: extra_platforms.pytest.unless_bamboo
.. autodata:: extra_platforms.pytest.unless_bsd
.. autodata:: extra_platforms.pytest.unless_bsd_without_macos
.. autodata:: extra_platforms.pytest.unless_buildkite
.. autodata:: extra_platforms.pytest.unless_buildroot
.. autodata:: extra_platforms.pytest.unless_cachyos
.. autodata:: extra_platforms.pytest.unless_centos
.. autodata:: extra_platforms.pytest.unless_circle_ci
.. autodata:: extra_platforms.pytest.unless_cirrus_ci
.. autodata:: extra_platforms.pytest.unless_cloudlinux
.. autodata:: extra_platforms.pytest.unless_codebuild
.. autodata:: extra_platforms.pytest.unless_cygwin
.. autodata:: extra_platforms.pytest.unless_debian
.. autodata:: extra_platforms.pytest.unless_dragonflybsd
.. autodata:: extra_platforms.pytest.unless_exherbo
.. autodata:: extra_platforms.pytest.unless_fedora
.. autodata:: extra_platforms.pytest.unless_freebsd
.. autodata:: extra_platforms.pytest.unless_gentoo
.. autodata:: extra_platforms.pytest.unless_github_ci
.. autodata:: extra_platforms.pytest.unless_gitlab_ci
.. autodata:: extra_platforms.pytest.unless_guix
.. autodata:: extra_platforms.pytest.unless_haiku
.. autodata:: extra_platforms.pytest.unless_heroku_ci
.. autodata:: extra_platforms.pytest.unless_hurd
.. autodata:: extra_platforms.pytest.unless_i386
.. autodata:: extra_platforms.pytest.unless_i586
.. autodata:: extra_platforms.pytest.unless_i686
.. autodata:: extra_platforms.pytest.unless_ibm_mainframe
.. autodata:: extra_platforms.pytest.unless_ibm_powerkvm
.. autodata:: extra_platforms.pytest.unless_illumos
.. autodata:: extra_platforms.pytest.unless_kvmibm
.. autodata:: extra_platforms.pytest.unless_linux
.. autodata:: extra_platforms.pytest.unless_linux_layers
.. autodata:: extra_platforms.pytest.unless_linux_like
.. autodata:: extra_platforms.pytest.unless_linuxmint
.. autodata:: extra_platforms.pytest.unless_loongarch
.. autodata:: extra_platforms.pytest.unless_loongarch64
.. autodata:: extra_platforms.pytest.unless_macos
.. autodata:: extra_platforms.pytest.unless_mageia
.. autodata:: extra_platforms.pytest.unless_mandriva
.. autodata:: extra_platforms.pytest.unless_midnightbsd
.. autodata:: extra_platforms.pytest.unless_mips
.. autodata:: extra_platforms.pytest.unless_mips64
.. autodata:: extra_platforms.pytest.unless_mips64el
.. autodata:: extra_platforms.pytest.unless_mipsel
.. autodata:: extra_platforms.pytest.unless_netbsd
.. autodata:: extra_platforms.pytest.unless_nobara
.. autodata:: extra_platforms.pytest.unless_openbsd
.. autodata:: extra_platforms.pytest.unless_opensuse
.. autodata:: extra_platforms.pytest.unless_oracle
.. autodata:: extra_platforms.pytest.unless_other_unix
.. autodata:: extra_platforms.pytest.unless_parallels
.. autodata:: extra_platforms.pytest.unless_pidora
.. autodata:: extra_platforms.pytest.unless_powerpc
.. autodata:: extra_platforms.pytest.unless_ppc
.. autodata:: extra_platforms.pytest.unless_ppc64
.. autodata:: extra_platforms.pytest.unless_ppc64le
.. autodata:: extra_platforms.pytest.unless_raspbian
.. autodata:: extra_platforms.pytest.unless_rhel
.. autodata:: extra_platforms.pytest.unless_riscv
.. autodata:: extra_platforms.pytest.unless_riscv32
.. autodata:: extra_platforms.pytest.unless_riscv64
.. autodata:: extra_platforms.pytest.unless_rocky
.. autodata:: extra_platforms.pytest.unless_s390x
.. autodata:: extra_platforms.pytest.unless_scientific
.. autodata:: extra_platforms.pytest.unless_slackware
.. autodata:: extra_platforms.pytest.unless_sles
.. autodata:: extra_platforms.pytest.unless_solaris
.. autodata:: extra_platforms.pytest.unless_sparc
.. autodata:: extra_platforms.pytest.unless_sparc64
.. autodata:: extra_platforms.pytest.unless_sunos
.. autodata:: extra_platforms.pytest.unless_system_v
.. autodata:: extra_platforms.pytest.unless_teamcity
.. autodata:: extra_platforms.pytest.unless_travis_ci
.. autodata:: extra_platforms.pytest.unless_tumbleweed
.. autodata:: extra_platforms.pytest.unless_tuxedo
.. autodata:: extra_platforms.pytest.unless_ubuntu
.. autodata:: extra_platforms.pytest.unless_ultramarine
.. autodata:: extra_platforms.pytest.unless_unix
.. autodata:: extra_platforms.pytest.unless_unix_layers
.. autodata:: extra_platforms.pytest.unless_unix_without_macos
.. autodata:: extra_platforms.pytest.unless_unknown
.. autodata:: extra_platforms.pytest.unless_unknown_architecture
.. autodata:: extra_platforms.pytest.unless_unknown_ci
.. autodata:: extra_platforms.pytest.unless_unknown_platform
.. autodata:: extra_platforms.pytest.unless_wasm32
.. autodata:: extra_platforms.pytest.unless_wasm64
.. autodata:: extra_platforms.pytest.unless_webassembly
.. autodata:: extra_platforms.pytest.unless_windows
.. autodata:: extra_platforms.pytest.unless_wsl1
.. autodata:: extra_platforms.pytest.unless_wsl2
.. autodata:: extra_platforms.pytest.unless_x86
.. autodata:: extra_platforms.pytest.unless_x86_64
.. autodata:: extra_platforms.pytest.unless_xenserver
```

<!-- pytest-decorators-autodata-end -->
