# {octicon}`meter` Pytest

```{py:currentmodule} extra_platforms
```

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

| Skip decorator                            | Unless decorator                            | Icon | Associated symbol             |
| :---------------------------------------- | :------------------------------------------ | :--: | :---------------------------- |
| {func}`~pytest.skip_aarch64`              | {func}`~pytest.unless_aarch64`              |  📱  | {data}`~AARCH64`              |
| {func}`~pytest.skip_aix`                  | {func}`~pytest.unless_aix`                  |  ➿  | {data}`~AIX`                  |
| {func}`~pytest.skip_all_architectures`    | {func}`~pytest.unless_any_architecture`     |  🏛️  | {data}`~ALL_ARCHITECTURES`    |
| {func}`~pytest.skip_all_arm`              | {func}`~pytest.unless_any_arm`              |  📱  | {data}`~ALL_ARM`              |
| {func}`~pytest.skip_all_ci`               | {func}`~pytest.unless_any_ci`               |  ♺   | {data}`~ALL_CI`               |
| {func}`~pytest.skip_all_mips`             | {func}`~pytest.unless_any_mips`             |  🔲  | {data}`~ALL_MIPS`             |
| {func}`~pytest.skip_all_platforms`        | {func}`~pytest.unless_any_platform`         |  ⚙️  | {data}`~ALL_PLATFORMS`        |
| {func}`~pytest.skip_all_sparc`            | {func}`~pytest.unless_any_sparc`            |  ☀️  | {data}`~ALL_SPARC`            |
| {func}`~pytest.skip_all_traits`           | {func}`~pytest.unless_any_trait`            |  ⁕   | {data}`~ALL_TRAITS`           |
| {func}`~pytest.skip_all_windows`          | {func}`~pytest.unless_any_windows`          |  🪟  | {data}`~ALL_WINDOWS`          |
| {func}`~pytest.skip_altlinux`             | {func}`~pytest.unless_altlinux`             |  🐧  | {data}`~ALTLINUX`             |
| {func}`~pytest.skip_amzn`                 | {func}`~pytest.unless_amzn`                 |  ⤻   | {data}`~AMZN`                 |
| {func}`~pytest.skip_android`              | {func}`~pytest.unless_android`              |  🤖  | {data}`~ANDROID`              |
| {func}`~pytest.skip_arch`                 | {func}`~pytest.unless_arch`                 |  🎗️  | {data}`~ARCH`                 |
| {func}`~pytest.skip_arch_32_bit`          | {func}`~pytest.unless_arch_32_bit`          |  ³²  | {data}`~ARCH_32_BIT`          |
| {func}`~pytest.skip_arch_64_bit`          | {func}`~pytest.unless_arch_64_bit`          |  ⁶⁴  | {data}`~ARCH_64_BIT`          |
| {func}`~pytest.skip_arm`                  | {func}`~pytest.unless_arm`                  |  📱  | {data}`~ARM`                  |
| {func}`~pytest.skip_armv5tel`             | {func}`~pytest.unless_armv5tel`             |  📱  | {data}`~ARMV5TEL`             |
| {func}`~pytest.skip_armv6l`               | {func}`~pytest.unless_armv6l`               |  📱  | {data}`~ARMV6L`               |
| {func}`~pytest.skip_armv7l`               | {func}`~pytest.unless_armv7l`               |  📱  | {data}`~ARMV7L`               |
| {func}`~pytest.skip_armv8l`               | {func}`~pytest.unless_armv8l`               |  📱  | {data}`~ARMV8L`               |
| {func}`~pytest.skip_azure_pipelines`      | {func}`~pytest.unless_azure_pipelines`      |  ═   | {data}`~AZURE_PIPELINES`      |
| {func}`~pytest.skip_bamboo`               | {func}`~pytest.unless_bamboo`               |  ⟲   | {data}`~BAMBOO`               |
| {func}`~pytest.skip_bsd`                  | {func}`~pytest.unless_bsd`                  | 🅱️+  | {data}`~BSD`                  |
| {func}`~pytest.skip_bsd_not_macos`        | {func}`~pytest.unless_bsd_not_macos`        |  🅱️  | {data}`~BSD_WITHOUT_MACOS`    |
| {func}`~pytest.skip_buildkite`            | {func}`~pytest.unless_buildkite`            |  🪁  | {data}`~BUILDKITE`            |
| {func}`~pytest.skip_buildroot`            | {func}`~pytest.unless_buildroot`            |  ⛑️  | {data}`~BUILDROOT`            |
| {func}`~pytest.skip_cachyos`              | {func}`~pytest.unless_cachyos`              |  ⌬   | {data}`~CACHYOS`              |
| {func}`~pytest.skip_centos`               | {func}`~pytest.unless_centos`               |  💠  | {data}`~CENTOS`               |
| {func}`~pytest.skip_circle_ci`            | {func}`~pytest.unless_circle_ci`            |  ⪾   | {data}`~CIRCLE_CI`            |
| {func}`~pytest.skip_cirrus_ci`            | {func}`~pytest.unless_cirrus_ci`            |  ≋   | {data}`~CIRRUS_CI`            |
| {func}`~pytest.skip_cloudlinux`           | {func}`~pytest.unless_cloudlinux`           |  ꩜   | {data}`~CLOUDLINUX`           |
| {func}`~pytest.skip_codebuild`            | {func}`~pytest.unless_codebuild`            |  ᚙ   | {data}`~CODEBUILD`            |
| {func}`~pytest.skip_cygwin`               | {func}`~pytest.unless_cygwin`               |  Ͼ   | {data}`~CYGWIN`               |
| {func}`~pytest.skip_debian`               | {func}`~pytest.unless_debian`               |  🌀  | {data}`~DEBIAN`               |
| {func}`~pytest.skip_dragonfly_bsd`        | {func}`~pytest.unless_dragonfly_bsd`        |  🪰  | {data}`~DRAGONFLY_BSD`        |
| {func}`~pytest.skip_exherbo`              | {func}`~pytest.unless_exherbo`              |  🐽  | {data}`~EXHERBO`              |
| {func}`~pytest.skip_fedora`               | {func}`~pytest.unless_fedora`               |  🎩  | {data}`~FEDORA`               |
| {func}`~pytest.skip_freebsd`              | {func}`~pytest.unless_freebsd`              |  😈  | {data}`~FREEBSD`              |
| {func}`~pytest.skip_gentoo`               | {func}`~pytest.unless_gentoo`               |  🗜️  | {data}`~GENTOO`               |
| {func}`~pytest.skip_github_ci`            | {func}`~pytest.unless_github_ci`            |  🐙  | {data}`~GITHUB_CI`            |
| {func}`~pytest.skip_gitlab_ci`            | {func}`~pytest.unless_gitlab_ci`            |  🦊  | {data}`~GITLAB_CI`            |
| {func}`~pytest.skip_guix`                 | {func}`~pytest.unless_guix`                 |  🐃  | {data}`~GUIX`                 |
| {func}`~pytest.skip_haiku`                | {func}`~pytest.unless_haiku`                |  🍂  | {data}`~HAIKU`                |
| {func}`~pytest.skip_heroku_ci`            | {func}`~pytest.unless_heroku_ci`            |  ⥁   | {data}`~HEROKU_CI`            |
| {func}`~pytest.skip_hurd`                 | {func}`~pytest.unless_hurd`                 |  🐃  | {data}`~HURD`                 |
| {func}`~pytest.skip_i386`                 | {func}`~pytest.unless_i386`                 |  𝗶   | {data}`~I386`                 |
| {func}`~pytest.skip_i586`                 | {func}`~pytest.unless_i586`                 |  𝗶   | {data}`~I586`                 |
| {func}`~pytest.skip_i686`                 | {func}`~pytest.unless_i686`                 |  𝗶   | {data}`~I686`                 |
| {func}`~pytest.skip_ibm_mainframe`        | {func}`~pytest.unless_ibm_mainframe`        |  🏢  | {data}`~IBM_MAINFRAME`        |
| {func}`~pytest.skip_ibm_powerkvm`         | {func}`~pytest.unless_ibm_powerkvm`         |  🤹  | {data}`~IBM_POWERKVM`         |
| {func}`~pytest.skip_illumos`              | {func}`~pytest.unless_illumos`              |  🔥  | {data}`~ILLUMOS`              |
| {func}`~pytest.skip_kvmibm`               | {func}`~pytest.unless_kvmibm`               |  🤹  | {data}`~KVMIBM`               |
| {func}`~pytest.skip_linux`                | {func}`~pytest.unless_linux`                |  🐧  | {data}`~LINUX`                |
| {func}`~pytest.skip_linux_layers`         | {func}`~pytest.unless_linux_layers`         |  ≚   | {data}`~LINUX_LAYERS`         |
| {func}`~pytest.skip_linux_like`           | {func}`~pytest.unless_linux_like`           | 🐧+  | {data}`~LINUX_LIKE`           |
| {func}`~pytest.skip_linuxmint`            | {func}`~pytest.unless_linuxmint`            |  🌿  | {data}`~LINUXMINT`            |
| {func}`~pytest.skip_loongarch`            | {func}`~pytest.unless_loongarch`            |  🐉  | {data}`~LOONGARCH`            |
| {func}`~pytest.skip_loongarch64`          | {func}`~pytest.unless_loongarch64`          |  🐉  | {data}`~LOONGARCH64`          |
| {func}`~pytest.skip_macos`                | {func}`~pytest.unless_macos`                |  🍎  | {data}`~MACOS`                |
| {func}`~pytest.skip_mageia`               | {func}`~pytest.unless_mageia`               |  ⍥   | {data}`~MAGEIA`               |
| {func}`~pytest.skip_mandriva`             | {func}`~pytest.unless_mandriva`             |  💫  | {data}`~MANDRIVA`             |
| {func}`~pytest.skip_midnightbsd`          | {func}`~pytest.unless_midnightbsd`          |  🌘  | {data}`~MIDNIGHTBSD`          |
| {func}`~pytest.skip_mips`                 | {func}`~pytest.unless_mips`                 |  🔲  | {data}`~MIPS`                 |
| {func}`~pytest.skip_mips64`               | {func}`~pytest.unless_mips64`               |  🔲  | {data}`~MIPS64`               |
| {func}`~pytest.skip_mips64el`             | {func}`~pytest.unless_mips64el`             |  🔲  | {data}`~MIPS64EL`             |
| {func}`~pytest.skip_mipsel`               | {func}`~pytest.unless_mipsel`               |  🔲  | {data}`~MIPSEL`               |
| {func}`~pytest.skip_netbsd`               | {func}`~pytest.unless_netbsd`               |  🚩  | {data}`~NETBSD`               |
| {func}`~pytest.skip_nobara`               | {func}`~pytest.unless_nobara`               |     | {data}`~NOBARA`               |
| {func}`~pytest.skip_openbsd`              | {func}`~pytest.unless_openbsd`              |  🐡  | {data}`~OPENBSD`              |
| {func}`~pytest.skip_opensuse`             | {func}`~pytest.unless_opensuse`             |  🦎  | {data}`~OPENSUSE`             |
| {func}`~pytest.skip_oracle`               | {func}`~pytest.unless_oracle`               |  🦴  | {data}`~ORACLE`               |
| {func}`~pytest.skip_other_posix`          | {func}`~pytest.unless_other_posix`          |  🅟   | {data}`~OTHER_POSIX`          |
| {func}`~pytest.skip_parallels`            | {func}`~pytest.unless_parallels`            |  ∥   | {data}`~PARALLELS`            |
| {func}`~pytest.skip_pidora`               | {func}`~pytest.unless_pidora`               |  🍓  | {data}`~PIDORA`               |
| {func}`~pytest.skip_powerpc`              | {func}`~pytest.unless_powerpc`              |  ⚡  | {data}`~POWERPC`              |
| {func}`~pytest.skip_ppc`                  | {func}`~pytest.unless_ppc`                  |  ⚡  | {data}`~PPC`                  |
| {func}`~pytest.skip_ppc64`                | {func}`~pytest.unless_ppc64`                |  ⚡  | {data}`~PPC64`                |
| {func}`~pytest.skip_ppc64le`              | {func}`~pytest.unless_ppc64le`              |  ⚡  | {data}`~PPC64LE`              |
| {func}`~pytest.skip_raspbian`             | {func}`~pytest.unless_raspbian`             |  🍓  | {data}`~RASPBIAN`             |
| {func}`~pytest.skip_rhel`                 | {func}`~pytest.unless_rhel`                 |  🎩  | {data}`~RHEL`                 |
| {func}`~pytest.skip_riscv`                | {func}`~pytest.unless_riscv`                |  Ⅴ   | {data}`~RISCV`                |
| {func}`~pytest.skip_riscv32`              | {func}`~pytest.unless_riscv32`              |  Ⅴ   | {data}`~RISCV32`              |
| {func}`~pytest.skip_riscv64`              | {func}`~pytest.unless_riscv64`              |  Ⅴ   | {data}`~RISCV64`              |
| {func}`~pytest.skip_rocky`                | {func}`~pytest.unless_rocky`                |  ⛰️  | {data}`~ROCKY`                |
| {func}`~pytest.skip_s390x`                | {func}`~pytest.unless_s390x`                |  🏢  | {data}`~S390X`                |
| {func}`~pytest.skip_scientific`           | {func}`~pytest.unless_scientific`           |  ⚛️  | {data}`~SCIENTIFIC`           |
| {func}`~pytest.skip_slackware`            | {func}`~pytest.unless_slackware`            |  🚬  | {data}`~SLACKWARE`            |
| {func}`~pytest.skip_sles`                 | {func}`~pytest.unless_sles`                 |  🦎  | {data}`~SLES`                 |
| {func}`~pytest.skip_solaris`              | {func}`~pytest.unless_solaris`              |  🌞  | {data}`~SOLARIS`              |
| {func}`~pytest.skip_sparc`                | {func}`~pytest.unless_sparc`                |  ☀️  | {data}`~SPARC`                |
| {func}`~pytest.skip_sparc64`              | {func}`~pytest.unless_sparc64`              |  ☀️  | {data}`~SPARC64`              |
| {func}`~pytest.skip_sunos`                | {func}`~pytest.unless_sunos`                |  ☀️  | {data}`~SUNOS`                |
| {func}`~pytest.skip_system_v`             | {func}`~pytest.unless_system_v`             |  𝐕   | {data}`~SYSTEM_V`             |
| {func}`~pytest.skip_teamcity`             | {func}`~pytest.unless_teamcity`             |  🏙️  | {data}`~TEAMCITY`             |
| {func}`~pytest.skip_travis_ci`            | {func}`~pytest.unless_travis_ci`            |  👷  | {data}`~TRAVIS_CI`            |
| {func}`~pytest.skip_tumbleweed`           | {func}`~pytest.unless_tumbleweed`           |  ↻   | {data}`~TUMBLEWEED`           |
| {func}`~pytest.skip_tuxedo`               | {func}`~pytest.unless_tuxedo`               |  🤵  | {data}`~TUXEDO`               |
| {func}`~pytest.skip_ubuntu`               | {func}`~pytest.unless_ubuntu`               |  🎯  | {data}`~UBUNTU`               |
| {func}`~pytest.skip_ultramarine`          | {func}`~pytest.unless_ultramarine`          |  🌊  | {data}`~ULTRAMARINE`          |
| {func}`~pytest.skip_unix`                 | {func}`~pytest.unless_unix`                 |  ⨷   | {data}`~UNIX`                 |
| {func}`~pytest.skip_unix_layers`          | {func}`~pytest.unless_unix_layers`          |  ≛   | {data}`~UNIX_LAYERS`          |
| {func}`~pytest.skip_unix_not_macos`       | {func}`~pytest.unless_unix_not_macos`       |  ⨂   | {data}`~UNIX_WITHOUT_MACOS`   |
| {func}`~pytest.skip_unknown`              | {func}`~pytest.unless_unknown`              |  ❓  | {data}`~UNKNOWN`              |
| {func}`~pytest.skip_unknown_architecture` | {func}`~pytest.unless_unknown_architecture` |  ❓  | {data}`~UNKNOWN_ARCHITECTURE` |
| {func}`~pytest.skip_unknown_ci`           | {func}`~pytest.unless_unknown_ci`           |  ❓  | {data}`~UNKNOWN_CI`           |
| {func}`~pytest.skip_unknown_platform`     | {func}`~pytest.unless_unknown_platform`     |  ❓  | {data}`~UNKNOWN_PLATFORM`     |
| {func}`~pytest.skip_wasm32`               | {func}`~pytest.unless_wasm32`               |  🌐  | {data}`~WASM32`               |
| {func}`~pytest.skip_wasm64`               | {func}`~pytest.unless_wasm64`               |  🌐  | {data}`~WASM64`               |
| {func}`~pytest.skip_webassembly`          | {func}`~pytest.unless_webassembly`          |  🌐  | {data}`~WEBASSEMBLY`          |
| {func}`~pytest.skip_windows`              | {func}`~pytest.unless_windows`              |  🪟  | {data}`~WINDOWS`              |
| {func}`~pytest.skip_wsl1`                 | {func}`~pytest.unless_wsl1`                 |  ⊞   | {data}`~WSL1`                 |
| {func}`~pytest.skip_wsl2`                 | {func}`~pytest.unless_wsl2`                 |  ⊞   | {data}`~WSL2`                 |
| {func}`~pytest.skip_x86`                  | {func}`~pytest.unless_x86`                  |  𝘅   | {data}`~X86`                  |
| {func}`~pytest.skip_x86_64`               | {func}`~pytest.unless_x86_64`               |  🖥️  | {data}`~X86_64`               |
| {func}`~pytest.skip_xenserver`            | {func}`~pytest.unless_xenserver`            |  Ⓧ   | {data}`~XENSERVER`            |

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
.. autodata:: extra_platforms.pytest.skip_bsd_not_macos
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
.. autodata:: extra_platforms.pytest.skip_dragonfly_bsd
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
.. autodata:: extra_platforms.pytest.skip_other_posix
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
.. autodata:: extra_platforms.pytest.skip_unix_not_macos
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
.. autodata:: extra_platforms.pytest.unless_bsd_not_macos
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
.. autodata:: extra_platforms.pytest.unless_dragonfly_bsd
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
.. autodata:: extra_platforms.pytest.unless_other_posix
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
.. autodata:: extra_platforms.pytest.unless_unix_not_macos
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
