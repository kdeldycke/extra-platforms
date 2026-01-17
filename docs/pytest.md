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

| Skip decorator                                            | Unless decorator                                            | Icon | Associated symbol                             |
| :-------------------------------------------------------- | :---------------------------------------------------------- | :--: | :-------------------------------------------- |
| {func}`~extra_platforms.pytest.skip_aarch64`              | {func}`~extra_platforms.pytest.unless_aarch64`              |  📱  | {data}`~extra_platforms.AARCH64`              |
| {func}`~extra_platforms.pytest.skip_aix`                  | {func}`~extra_platforms.pytest.unless_aix`                  |  ➿  | {data}`~extra_platforms.AIX`                  |
| {func}`~extra_platforms.pytest.skip_all_architectures`    | {func}`~extra_platforms.pytest.unless_any_architecture`     |  🏛️  | {data}`~extra_platforms.ALL_ARCHITECTURES`    |
| {func}`~extra_platforms.pytest.skip_all_arm`              | {func}`~extra_platforms.pytest.unless_any_arm`              |  📱  | {data}`~extra_platforms.ALL_ARM`              |
| {func}`~extra_platforms.pytest.skip_all_ci`               | {func}`~extra_platforms.pytest.unless_any_ci`               |  ♺   | {data}`~extra_platforms.ALL_CI`               |
| {func}`~extra_platforms.pytest.skip_all_mips`             | {func}`~extra_platforms.pytest.unless_any_mips`             |  🔲  | {data}`~extra_platforms.ALL_MIPS`             |
| {func}`~extra_platforms.pytest.skip_all_platforms`        | {func}`~extra_platforms.pytest.unless_any_platform`         |  ⚙️  | {data}`~extra_platforms.ALL_PLATFORMS`        |
| {func}`~extra_platforms.pytest.skip_all_sparc`            | {func}`~extra_platforms.pytest.unless_any_sparc`            |  ☀️  | {data}`~extra_platforms.ALL_SPARC`            |
| {func}`~extra_platforms.pytest.skip_all_traits`           | {func}`~extra_platforms.pytest.unless_any_trait`            |  ⁕   | {data}`~extra_platforms.ALL_TRAITS`           |
| {func}`~extra_platforms.pytest.skip_all_windows`          | {func}`~extra_platforms.pytest.unless_any_windows`          |  🪟  | {data}`~extra_platforms.ALL_WINDOWS`          |
| {func}`~extra_platforms.pytest.skip_altlinux`             | {func}`~extra_platforms.pytest.unless_altlinux`             |  🐧  | {data}`~extra_platforms.ALTLINUX`             |
| {func}`~extra_platforms.pytest.skip_amzn`                 | {func}`~extra_platforms.pytest.unless_amzn`                 |  ⤻   | {data}`~extra_platforms.AMZN`                 |
| {func}`~extra_platforms.pytest.skip_android`              | {func}`~extra_platforms.pytest.unless_android`              |  🤖  | {data}`~extra_platforms.ANDROID`              |
| {func}`~extra_platforms.pytest.skip_arch`                 | {func}`~extra_platforms.pytest.unless_arch`                 |  🎗️  | {data}`~extra_platforms.ARCH`                 |
| {func}`~extra_platforms.pytest.skip_arch_32_bit`          | {func}`~extra_platforms.pytest.unless_arch_32_bit`          |  ³²  | {data}`~extra_platforms.ARCH_32_BIT`          |
| {func}`~extra_platforms.pytest.skip_arch_64_bit`          | {func}`~extra_platforms.pytest.unless_arch_64_bit`          |  ⁶⁴  | {data}`~extra_platforms.ARCH_64_BIT`          |
| {func}`~extra_platforms.pytest.skip_arm`                  | {func}`~extra_platforms.pytest.unless_arm`                  |  📱  | {data}`~extra_platforms.ARM`                  |
| {func}`~extra_platforms.pytest.skip_armv5tel`             | {func}`~extra_platforms.pytest.unless_armv5tel`             |  📱  | {data}`~extra_platforms.ARMV5TEL`             |
| {func}`~extra_platforms.pytest.skip_armv6l`               | {func}`~extra_platforms.pytest.unless_armv6l`               |  📱  | {data}`~extra_platforms.ARMV6L`               |
| {func}`~extra_platforms.pytest.skip_armv7l`               | {func}`~extra_platforms.pytest.unless_armv7l`               |  📱  | {data}`~extra_platforms.ARMV7L`               |
| {func}`~extra_platforms.pytest.skip_armv8l`               | {func}`~extra_platforms.pytest.unless_armv8l`               |  📱  | {data}`~extra_platforms.ARMV8L`               |
| {func}`~extra_platforms.pytest.skip_azure_pipelines`      | {func}`~extra_platforms.pytest.unless_azure_pipelines`      |  ═   | {data}`~extra_platforms.AZURE_PIPELINES`      |
| {func}`~extra_platforms.pytest.skip_bamboo`               | {func}`~extra_platforms.pytest.unless_bamboo`               |  ⟲   | {data}`~extra_platforms.BAMBOO`               |
| {func}`~extra_platforms.pytest.skip_bsd`                  | {func}`~extra_platforms.pytest.unless_bsd`                  | 🅱️+  | {data}`~extra_platforms.BSD`                  |
| {func}`~extra_platforms.pytest.skip_bsd_not_macos`        | {func}`~extra_platforms.pytest.unless_bsd_not_macos`        |  🅱️  | {data}`~extra_platforms.BSD_WITHOUT_MACOS`    |
| {func}`~extra_platforms.pytest.skip_buildkite`            | {func}`~extra_platforms.pytest.unless_buildkite`            |  🪁  | {data}`~extra_platforms.BUILDKITE`            |
| {func}`~extra_platforms.pytest.skip_buildroot`            | {func}`~extra_platforms.pytest.unless_buildroot`            |  ⛑️  | {data}`~extra_platforms.BUILDROOT`            |
| {func}`~extra_platforms.pytest.skip_cachyos`              | {func}`~extra_platforms.pytest.unless_cachyos`              |  ⌬   | {data}`~extra_platforms.CACHYOS`              |
| {func}`~extra_platforms.pytest.skip_centos`               | {func}`~extra_platforms.pytest.unless_centos`               |  💠  | {data}`~extra_platforms.CENTOS`               |
| {func}`~extra_platforms.pytest.skip_circle_ci`            | {func}`~extra_platforms.pytest.unless_circle_ci`            |  ⪾   | {data}`~extra_platforms.CIRCLE_CI`            |
| {func}`~extra_platforms.pytest.skip_cirrus_ci`            | {func}`~extra_platforms.pytest.unless_cirrus_ci`            |  ≋   | {data}`~extra_platforms.CIRRUS_CI`            |
| {func}`~extra_platforms.pytest.skip_cloudlinux`           | {func}`~extra_platforms.pytest.unless_cloudlinux`           |  ꩜   | {data}`~extra_platforms.CLOUDLINUX`           |
| {func}`~extra_platforms.pytest.skip_codebuild`            | {func}`~extra_platforms.pytest.unless_codebuild`            |  ᚙ   | {data}`~extra_platforms.CODEBUILD`            |
| {func}`~extra_platforms.pytest.skip_cygwin`               | {func}`~extra_platforms.pytest.unless_cygwin`               |  Ͼ   | {data}`~extra_platforms.CYGWIN`               |
| {func}`~extra_platforms.pytest.skip_debian`               | {func}`~extra_platforms.pytest.unless_debian`               |  🌀  | {data}`~extra_platforms.DEBIAN`               |
| {func}`~extra_platforms.pytest.skip_dragonfly_bsd`        | {func}`~extra_platforms.pytest.unless_dragonfly_bsd`        |  🪰  | {data}`~extra_platforms.DRAGONFLY_BSD`        |
| {func}`~extra_platforms.pytest.skip_exherbo`              | {func}`~extra_platforms.pytest.unless_exherbo`              |  🐽  | {data}`~extra_platforms.EXHERBO`              |
| {func}`~extra_platforms.pytest.skip_fedora`               | {func}`~extra_platforms.pytest.unless_fedora`               |  🎩  | {data}`~extra_platforms.FEDORA`               |
| {func}`~extra_platforms.pytest.skip_freebsd`              | {func}`~extra_platforms.pytest.unless_freebsd`              |  😈  | {data}`~extra_platforms.FREEBSD`              |
| {func}`~extra_platforms.pytest.skip_gentoo`               | {func}`~extra_platforms.pytest.unless_gentoo`               |  🗜️  | {data}`~extra_platforms.GENTOO`               |
| {func}`~extra_platforms.pytest.skip_github_ci`            | {func}`~extra_platforms.pytest.unless_github_ci`            |  🐙  | {data}`~extra_platforms.GITHUB_CI`            |
| {func}`~extra_platforms.pytest.skip_gitlab_ci`            | {func}`~extra_platforms.pytest.unless_gitlab_ci`            |  🦊  | {data}`~extra_platforms.GITLAB_CI`            |
| {func}`~extra_platforms.pytest.skip_guix`                 | {func}`~extra_platforms.pytest.unless_guix`                 |  🐃  | {data}`~extra_platforms.GUIX`                 |
| {func}`~extra_platforms.pytest.skip_haiku`                | {func}`~extra_platforms.pytest.unless_haiku`                |  🍂  | {data}`~extra_platforms.HAIKU`                |
| {func}`~extra_platforms.pytest.skip_heroku_ci`            | {func}`~extra_platforms.pytest.unless_heroku_ci`            |  ⥁   | {data}`~extra_platforms.HEROKU_CI`            |
| {func}`~extra_platforms.pytest.skip_hurd`                 | {func}`~extra_platforms.pytest.unless_hurd`                 |  🐃  | {data}`~extra_platforms.HURD`                 |
| {func}`~extra_platforms.pytest.skip_i386`                 | {func}`~extra_platforms.pytest.unless_i386`                 |  𝗶   | {data}`~extra_platforms.I386`                 |
| {func}`~extra_platforms.pytest.skip_i586`                 | {func}`~extra_platforms.pytest.unless_i586`                 |  𝗶   | {data}`~extra_platforms.I586`                 |
| {func}`~extra_platforms.pytest.skip_i686`                 | {func}`~extra_platforms.pytest.unless_i686`                 |  𝗶   | {data}`~extra_platforms.I686`                 |
| {func}`~extra_platforms.pytest.skip_ibm_mainframe`        | {func}`~extra_platforms.pytest.unless_ibm_mainframe`        |  🏢  | {data}`~extra_platforms.IBM_MAINFRAME`        |
| {func}`~extra_platforms.pytest.skip_ibm_powerkvm`         | {func}`~extra_platforms.pytest.unless_ibm_powerkvm`         |  🤹  | {data}`~extra_platforms.IBM_POWERKVM`         |
| {func}`~extra_platforms.pytest.skip_illumos`              | {func}`~extra_platforms.pytest.unless_illumos`              |  🔥  | {data}`~extra_platforms.ILLUMOS`              |
| {func}`~extra_platforms.pytest.skip_kvmibm`               | {func}`~extra_platforms.pytest.unless_kvmibm`               |  🤹  | {data}`~extra_platforms.KVMIBM`               |
| {func}`~extra_platforms.pytest.skip_linux`                | {func}`~extra_platforms.pytest.unless_linux`                |  🐧  | {data}`~extra_platforms.LINUX`                |
| {func}`~extra_platforms.pytest.skip_linux_layers`         | {func}`~extra_platforms.pytest.unless_linux_layers`         |  ≚   | {data}`~extra_platforms.LINUX_LAYERS`         |
| {func}`~extra_platforms.pytest.skip_linux_like`           | {func}`~extra_platforms.pytest.unless_linux_like`           | 🐧+  | {data}`~extra_platforms.LINUX_LIKE`           |
| {func}`~extra_platforms.pytest.skip_linuxmint`            | {func}`~extra_platforms.pytest.unless_linuxmint`            |  🌿  | {data}`~extra_platforms.LINUXMINT`            |
| {func}`~extra_platforms.pytest.skip_loongarch`            | {func}`~extra_platforms.pytest.unless_loongarch`            |  🐉  | {data}`~extra_platforms.LOONGARCH`            |
| {func}`~extra_platforms.pytest.skip_loongarch64`          | {func}`~extra_platforms.pytest.unless_loongarch64`          |  🐉  | {data}`~extra_platforms.LOONGARCH64`          |
| {func}`~extra_platforms.pytest.skip_macos`                | {func}`~extra_platforms.pytest.unless_macos`                |  🍎  | {data}`~extra_platforms.MACOS`                |
| {func}`~extra_platforms.pytest.skip_mageia`               | {func}`~extra_platforms.pytest.unless_mageia`               |  ⍥   | {data}`~extra_platforms.MAGEIA`               |
| {func}`~extra_platforms.pytest.skip_mandriva`             | {func}`~extra_platforms.pytest.unless_mandriva`             |  💫  | {data}`~extra_platforms.MANDRIVA`             |
| {func}`~extra_platforms.pytest.skip_midnightbsd`          | {func}`~extra_platforms.pytest.unless_midnightbsd`          |  🌘  | {data}`~extra_platforms.MIDNIGHTBSD`          |
| {func}`~extra_platforms.pytest.skip_mips`                 | {func}`~extra_platforms.pytest.unless_mips`                 |  🔲  | {data}`~extra_platforms.MIPS`                 |
| {func}`~extra_platforms.pytest.skip_mips64`               | {func}`~extra_platforms.pytest.unless_mips64`               |  🔲  | {data}`~extra_platforms.MIPS64`               |
| {func}`~extra_platforms.pytest.skip_mips64el`             | {func}`~extra_platforms.pytest.unless_mips64el`             |  🔲  | {data}`~extra_platforms.MIPS64EL`             |
| {func}`~extra_platforms.pytest.skip_mipsel`               | {func}`~extra_platforms.pytest.unless_mipsel`               |  🔲  | {data}`~extra_platforms.MIPSEL`               |
| {func}`~extra_platforms.pytest.skip_netbsd`               | {func}`~extra_platforms.pytest.unless_netbsd`               |  🚩  | {data}`~extra_platforms.NETBSD`               |
| {func}`~extra_platforms.pytest.skip_nobara`               | {func}`~extra_platforms.pytest.unless_nobara`               |     | {data}`~extra_platforms.NOBARA`               |
| {func}`~extra_platforms.pytest.skip_openbsd`              | {func}`~extra_platforms.pytest.unless_openbsd`              |  🐡  | {data}`~extra_platforms.OPENBSD`              |
| {func}`~extra_platforms.pytest.skip_opensuse`             | {func}`~extra_platforms.pytest.unless_opensuse`             |  🦎  | {data}`~extra_platforms.OPENSUSE`             |
| {func}`~extra_platforms.pytest.skip_oracle`               | {func}`~extra_platforms.pytest.unless_oracle`               |  🦴  | {data}`~extra_platforms.ORACLE`               |
| {func}`~extra_platforms.pytest.skip_other_posix`          | {func}`~extra_platforms.pytest.unless_other_posix`          |  🅟   | {data}`~extra_platforms.OTHER_POSIX`          |
| {func}`~extra_platforms.pytest.skip_parallels`            | {func}`~extra_platforms.pytest.unless_parallels`            |  ∥   | {data}`~extra_platforms.PARALLELS`            |
| {func}`~extra_platforms.pytest.skip_pidora`               | {func}`~extra_platforms.pytest.unless_pidora`               |  🍓  | {data}`~extra_platforms.PIDORA`               |
| {func}`~extra_platforms.pytest.skip_powerpc`              | {func}`~extra_platforms.pytest.unless_powerpc`              |  ⚡  | {data}`~extra_platforms.POWERPC`              |
| {func}`~extra_platforms.pytest.skip_ppc`                  | {func}`~extra_platforms.pytest.unless_ppc`                  |  ⚡  | {data}`~extra_platforms.PPC`                  |
| {func}`~extra_platforms.pytest.skip_ppc64`                | {func}`~extra_platforms.pytest.unless_ppc64`                |  ⚡  | {data}`~extra_platforms.PPC64`                |
| {func}`~extra_platforms.pytest.skip_ppc64le`              | {func}`~extra_platforms.pytest.unless_ppc64le`              |  ⚡  | {data}`~extra_platforms.PPC64LE`              |
| {func}`~extra_platforms.pytest.skip_raspbian`             | {func}`~extra_platforms.pytest.unless_raspbian`             |  🍓  | {data}`~extra_platforms.RASPBIAN`             |
| {func}`~extra_platforms.pytest.skip_rhel`                 | {func}`~extra_platforms.pytest.unless_rhel`                 |  🎩  | {data}`~extra_platforms.RHEL`                 |
| {func}`~extra_platforms.pytest.skip_riscv`                | {func}`~extra_platforms.pytest.unless_riscv`                |  Ⅴ   | {data}`~extra_platforms.RISCV`                |
| {func}`~extra_platforms.pytest.skip_riscv32`              | {func}`~extra_platforms.pytest.unless_riscv32`              |  Ⅴ   | {data}`~extra_platforms.RISCV32`              |
| {func}`~extra_platforms.pytest.skip_riscv64`              | {func}`~extra_platforms.pytest.unless_riscv64`              |  Ⅴ   | {data}`~extra_platforms.RISCV64`              |
| {func}`~extra_platforms.pytest.skip_rocky`                | {func}`~extra_platforms.pytest.unless_rocky`                |  ⛰️  | {data}`~extra_platforms.ROCKY`                |
| {func}`~extra_platforms.pytest.skip_s390x`                | {func}`~extra_platforms.pytest.unless_s390x`                |  🏢  | {data}`~extra_platforms.S390X`                |
| {func}`~extra_platforms.pytest.skip_scientific`           | {func}`~extra_platforms.pytest.unless_scientific`           |  ⚛️  | {data}`~extra_platforms.SCIENTIFIC`           |
| {func}`~extra_platforms.pytest.skip_slackware`            | {func}`~extra_platforms.pytest.unless_slackware`            |  🚬  | {data}`~extra_platforms.SLACKWARE`            |
| {func}`~extra_platforms.pytest.skip_sles`                 | {func}`~extra_platforms.pytest.unless_sles`                 |  🦎  | {data}`~extra_platforms.SLES`                 |
| {func}`~extra_platforms.pytest.skip_solaris`              | {func}`~extra_platforms.pytest.unless_solaris`              |  🌞  | {data}`~extra_platforms.SOLARIS`              |
| {func}`~extra_platforms.pytest.skip_sparc`                | {func}`~extra_platforms.pytest.unless_sparc`                |  ☀️  | {data}`~extra_platforms.SPARC`                |
| {func}`~extra_platforms.pytest.skip_sparc64`              | {func}`~extra_platforms.pytest.unless_sparc64`              |  ☀️  | {data}`~extra_platforms.SPARC64`              |
| {func}`~extra_platforms.pytest.skip_sunos`                | {func}`~extra_platforms.pytest.unless_sunos`                |  ☀️  | {data}`~extra_platforms.SUNOS`                |
| {func}`~extra_platforms.pytest.skip_system_v`             | {func}`~extra_platforms.pytest.unless_system_v`             |  𝐕   | {data}`~extra_platforms.SYSTEM_V`             |
| {func}`~extra_platforms.pytest.skip_teamcity`             | {func}`~extra_platforms.pytest.unless_teamcity`             |  🏙️  | {data}`~extra_platforms.TEAMCITY`             |
| {func}`~extra_platforms.pytest.skip_travis_ci`            | {func}`~extra_platforms.pytest.unless_travis_ci`            |  👷  | {data}`~extra_platforms.TRAVIS_CI`            |
| {func}`~extra_platforms.pytest.skip_tumbleweed`           | {func}`~extra_platforms.pytest.unless_tumbleweed`           |  ↻   | {data}`~extra_platforms.TUMBLEWEED`           |
| {func}`~extra_platforms.pytest.skip_tuxedo`               | {func}`~extra_platforms.pytest.unless_tuxedo`               |  🤵  | {data}`~extra_platforms.TUXEDO`               |
| {func}`~extra_platforms.pytest.skip_ubuntu`               | {func}`~extra_platforms.pytest.unless_ubuntu`               |  🎯  | {data}`~extra_platforms.UBUNTU`               |
| {func}`~extra_platforms.pytest.skip_ultramarine`          | {func}`~extra_platforms.pytest.unless_ultramarine`          |  🌊  | {data}`~extra_platforms.ULTRAMARINE`          |
| {func}`~extra_platforms.pytest.skip_unix`                 | {func}`~extra_platforms.pytest.unless_unix`                 |  ⨷   | {data}`~extra_platforms.UNIX`                 |
| {func}`~extra_platforms.pytest.skip_unix_layers`          | {func}`~extra_platforms.pytest.unless_unix_layers`          |  ≛   | {data}`~extra_platforms.UNIX_LAYERS`          |
| {func}`~extra_platforms.pytest.skip_unix_not_macos`       | {func}`~extra_platforms.pytest.unless_unix_not_macos`       |  ⨂   | {data}`~extra_platforms.UNIX_WITHOUT_MACOS`   |
| {func}`~extra_platforms.pytest.skip_unknown`              | {func}`~extra_platforms.pytest.unless_unknown`              |  ❓  | {data}`~extra_platforms.UNKNOWN`              |
| {func}`~extra_platforms.pytest.skip_unknown_architecture` | {func}`~extra_platforms.pytest.unless_unknown_architecture` |  ❓  | {data}`~extra_platforms.UNKNOWN_ARCHITECTURE` |
| {func}`~extra_platforms.pytest.skip_unknown_ci`           | {func}`~extra_platforms.pytest.unless_unknown_ci`           |  ❓  | {data}`~extra_platforms.UNKNOWN_CI`           |
| {func}`~extra_platforms.pytest.skip_unknown_platform`     | {func}`~extra_platforms.pytest.unless_unknown_platform`     |  ❓  | {data}`~extra_platforms.UNKNOWN_PLATFORM`     |
| {func}`~extra_platforms.pytest.skip_wasm32`               | {func}`~extra_platforms.pytest.unless_wasm32`               |  🌐  | {data}`~extra_platforms.WASM32`               |
| {func}`~extra_platforms.pytest.skip_wasm64`               | {func}`~extra_platforms.pytest.unless_wasm64`               |  🌐  | {data}`~extra_platforms.WASM64`               |
| {func}`~extra_platforms.pytest.skip_webassembly`          | {func}`~extra_platforms.pytest.unless_webassembly`          |  🌐  | {data}`~extra_platforms.WEBASSEMBLY`          |
| {func}`~extra_platforms.pytest.skip_windows`              | {func}`~extra_platforms.pytest.unless_windows`              |  🪟  | {data}`~extra_platforms.WINDOWS`              |
| {func}`~extra_platforms.pytest.skip_wsl1`                 | {func}`~extra_platforms.pytest.unless_wsl1`                 |  ⊞   | {data}`~extra_platforms.WSL1`                 |
| {func}`~extra_platforms.pytest.skip_wsl2`                 | {func}`~extra_platforms.pytest.unless_wsl2`                 |  ⊞   | {data}`~extra_platforms.WSL2`                 |
| {func}`~extra_platforms.pytest.skip_x86`                  | {func}`~extra_platforms.pytest.unless_x86`                  |  𝘅   | {data}`~extra_platforms.X86`                  |
| {func}`~extra_platforms.pytest.skip_x86_64`               | {func}`~extra_platforms.pytest.unless_x86_64`               |  🖥️  | {data}`~extra_platforms.X86_64`               |
| {func}`~extra_platforms.pytest.skip_xenserver`            | {func}`~extra_platforms.pytest.unless_xenserver`            |  Ⓧ   | {data}`~extra_platforms.XENSERVER`            |

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
