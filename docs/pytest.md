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

### Examples

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

## Decorators reference

<!-- decorators-table-start -->

| Skip decorator               | Unless decorator               | Source symbol                                                                   | Description                                 |
| :--------------------------- | :----------------------------- | :------------------------------------------------------------------------------ | :------------------------------------------ |
| `@skip_aarch64`              | `@unless_aarch64`              | [`AARCH64`](architectures.md#extra_platforms.AARCH64)                           | ARM64 (AArch64)                             |
| `@skip_aix`                  | `@unless_aix`                  | [`AIX`](platforms.md#extra_platforms.AIX)                                       | IBM AIX                                     |
| `@skip_all_architectures`    | `@unless_all_architectures`    | [`ALL_ARCHITECTURES`](groups.md#extra_platforms.ALL_ARCHITECTURES)              | All architectures                           |
| `@skip_all_ci`               | `@unless_all_ci`               | [`ALL_CI`](groups.md#extra_platforms.ALL_CI)                                    | All CI systems                              |
| `@skip_all_platforms`        | `@unless_all_platforms`        | [`ALL_PLATFORMS`](groups.md#extra_platforms.ALL_PLATFORMS)                      | All platforms                               |
| `@skip_all_traits`           | `@unless_all_traits`           | [`ALL_TRAITS`](groups.md#extra_platforms.ALL_TRAITS)                            | Any architectures, platforms and CI systems |
| `@skip_altlinux`             | `@unless_altlinux`             | [`ALTLINUX`](platforms.md#extra_platforms.ALTLINUX)                             | ALT Linux                                   |
| `@skip_amzn`                 | `@unless_amzn`                 | [`AMZN`](platforms.md#extra_platforms.AMZN)                                     | Amazon Linux                                |
| `@skip_android`              | `@unless_android`              | [`ANDROID`](platforms.md#extra_platforms.ANDROID)                               | Android                                     |
| `@skip_any_arm`              | `@unless_any_arm`              | [`ANY_ARM`](groups.md#extra_platforms.ANY_ARM)                                  | Any ARM architecture                        |
| `@skip_any_mips`             | `@unless_any_mips`             | [`ANY_MIPS`](groups.md#extra_platforms.ANY_MIPS)                                | Any MIPS architecture                       |
| `@skip_any_sparc`            | `@unless_any_sparc`            | [`ANY_SPARC`](groups.md#extra_platforms.ANY_SPARC)                              | Any SPARC architecture                      |
| `@skip_any_windows`          | `@unless_any_windows`          | [`ANY_WINDOWS`](groups.md#extra_platforms.ANY_WINDOWS)                          | Any Windows                                 |
| `@skip_arch`                 | `@unless_arch`                 | [`ARCH`](platforms.md#extra_platforms.ARCH)                                     | Arch Linux                                  |
| `@skip_arch_32_bit`          | `@unless_arch_32_bit`          | [`ARCH_32_BIT`](groups.md#extra_platforms.ARCH_32_BIT)                          | 32-bit architectures                        |
| `@skip_arch_64_bit`          | `@unless_arch_64_bit`          | [`ARCH_64_BIT`](groups.md#extra_platforms.ARCH_64_BIT)                          | 64-bit architectures                        |
| `@skip_arm`                  | `@unless_arm`                  | [`ARM`](architectures.md#extra_platforms.ARM)                                   | ARM (32-bit)                                |
| `@skip_armv6l`               | `@unless_armv6l`               | [`ARMV6L`](architectures.md#extra_platforms.ARMV6L)                             | ARMv6 (little-endian)                       |
| `@skip_armv7l`               | `@unless_armv7l`               | [`ARMV7L`](architectures.md#extra_platforms.ARMV7L)                             | ARMv7 (little-endian)                       |
| `@skip_armv8l`               | `@unless_armv8l`               | [`ARMV8L`](architectures.md#extra_platforms.ARMV8L)                             | ARMv8 (32-bit, little-endian)               |
| `@skip_azure_pipelines`      | `@unless_azure_pipelines`      | [`AZURE_PIPELINES`](ci.md#extra_platforms.AZURE_PIPELINES)                      | Azure Pipelines                             |
| `@skip_bamboo`               | `@unless_bamboo`               | [`BAMBOO`](ci.md#extra_platforms.BAMBOO)                                        | Bamboo                                      |
| `@skip_bsd`                  | `@unless_bsd`                  | [`BSD`](groups.md#extra_platforms.BSD)                                          | Any BSD                                     |
| `@skip_bsd_without_macos`    | `@unless_bsd_without_macos`    | [`BSD_WITHOUT_MACOS`](groups.md#extra_platforms.BSD_WITHOUT_MACOS)              | Any BSD excluding macOS                     |
| `@skip_buildkite`            | `@unless_buildkite`            | [`BUILDKITE`](ci.md#extra_platforms.BUILDKITE)                                  | Buildkite                                   |
| `@skip_buildroot`            | `@unless_buildroot`            | [`BUILDROOT`](platforms.md#extra_platforms.BUILDROOT)                           | Buildroot                                   |
| `@skip_cachyos`              | `@unless_cachyos`              | [`CACHYOS`](platforms.md#extra_platforms.CACHYOS)                               | CachyOS                                     |
| `@skip_centos`               | `@unless_centos`               | [`CENTOS`](platforms.md#extra_platforms.CENTOS)                                 | CentOS                                      |
| `@skip_circle_ci`            | `@unless_circle_ci`            | [`CIRCLE_CI`](ci.md#extra_platforms.CIRCLE_CI)                                  | Circle CI                                   |
| `@skip_cirrus_ci`            | `@unless_cirrus_ci`            | [`CIRRUS_CI`](ci.md#extra_platforms.CIRRUS_CI)                                  | Cirrus CI                                   |
| `@skip_cloudlinux`           | `@unless_cloudlinux`           | [`CLOUDLINUX`](platforms.md#extra_platforms.CLOUDLINUX)                         | CloudLinux OS                               |
| `@skip_codebuild`            | `@unless_codebuild`            | [`CODEBUILD`](ci.md#extra_platforms.CODEBUILD)                                  | CodeBuild                                   |
| `@skip_cygwin`               | `@unless_cygwin`               | [`CYGWIN`](platforms.md#extra_platforms.CYGWIN)                                 | Cygwin                                      |
| `@skip_debian`               | `@unless_debian`               | [`DEBIAN`](platforms.md#extra_platforms.DEBIAN)                                 | Debian                                      |
| `@skip_exherbo`              | `@unless_exherbo`              | [`EXHERBO`](platforms.md#extra_platforms.EXHERBO)                               | Exherbo Linux                               |
| `@skip_fedora`               | `@unless_fedora`               | [`FEDORA`](platforms.md#extra_platforms.FEDORA)                                 | Fedora                                      |
| `@skip_freebsd`              | `@unless_freebsd`              | [`FREEBSD`](platforms.md#extra_platforms.FREEBSD)                               | FreeBSD                                     |
| `@skip_gentoo`               | `@unless_gentoo`               | [`GENTOO`](platforms.md#extra_platforms.GENTOO)                                 | Gentoo Linux                                |
| `@skip_github_ci`            | `@unless_github_ci`            | [`GITHUB_CI`](ci.md#extra_platforms.GITHUB_CI)                                  | GitHub Actions runner                       |
| `@skip_gitlab_ci`            | `@unless_gitlab_ci`            | [`GITLAB_CI`](ci.md#extra_platforms.GITLAB_CI)                                  | GitLab CI                                   |
| `@skip_guix`                 | `@unless_guix`                 | [`GUIX`](platforms.md#extra_platforms.GUIX)                                     | Guix System                                 |
| `@skip_heroku_ci`            | `@unless_heroku_ci`            | [`HEROKU_CI`](ci.md#extra_platforms.HEROKU_CI)                                  | Heroku CI                                   |
| `@skip_hurd`                 | `@unless_hurd`                 | [`HURD`](platforms.md#extra_platforms.HURD)                                     | GNU/Hurd                                    |
| `@skip_i386`                 | `@unless_i386`                 | [`I386`](architectures.md#extra_platforms.I386)                                 | Intel 80386 (i386)                          |
| `@skip_i586`                 | `@unless_i586`                 | [`I586`](architectures.md#extra_platforms.I586)                                 | Intel Pentium (i586)                        |
| `@skip_i686`                 | `@unless_i686`                 | [`I686`](architectures.md#extra_platforms.I686)                                 | Intel Pentium Pro (i686)                    |
| `@skip_ibm_mainframe`        | `@unless_ibm_mainframe`        | [`IBM_MAINFRAME`](groups.md#extra_platforms.IBM_MAINFRAME)                      | IBM mainframe                               |
| `@skip_ibm_powerkvm`         | `@unless_ibm_powerkvm`         | [`IBM_POWERKVM`](platforms.md#extra_platforms.IBM_POWERKVM)                     | IBM PowerKVM                                |
| `@skip_kvmibm`               | `@unless_kvmibm`               | [`KVMIBM`](platforms.md#extra_platforms.KVMIBM)                                 | KVM for IBM z Systems                       |
| `@skip_linux`                | `@unless_linux`                | [`LINUX`](groups.md#extra_platforms.LINUX)                                      | Any Linux distribution                      |
| `@skip_linux_layers`         | `@unless_linux_layers`         | [`LINUX_LAYERS`](groups.md#extra_platforms.LINUX_LAYERS)                        | Any Linux compatibility layers              |
| `@skip_linux_like`           | `@unless_linux_like`           | [`LINUX_LIKE`](groups.md#extra_platforms.LINUX_LIKE)                            | Any Linux and compatibility layers          |
| `@skip_linuxmint`            | `@unless_linuxmint`            | [`LINUXMINT`](platforms.md#extra_platforms.LINUXMINT)                           | Linux Mint                                  |
| `@skip_loongarch`            | `@unless_loongarch`            | [`LOONGARCH`](groups.md#extra_platforms.LOONGARCH)                              | LoongArch                                   |
| `@skip_loongarch64`          | `@unless_loongarch64`          | [`LOONGARCH64`](architectures.md#extra_platforms.LOONGARCH64)                   | LoongArch (64-bit)                          |
| `@skip_macos`                | `@unless_macos`                | [`MACOS`](platforms.md#extra_platforms.MACOS)                                   | macOS                                       |
| `@skip_mageia`               | `@unless_mageia`               | [`MAGEIA`](platforms.md#extra_platforms.MAGEIA)                                 | Mageia                                      |
| `@skip_mandriva`             | `@unless_mandriva`             | [`MANDRIVA`](platforms.md#extra_platforms.MANDRIVA)                             | Mandriva Linux                              |
| `@skip_midnightbsd`          | `@unless_midnightbsd`          | [`MIDNIGHTBSD`](platforms.md#extra_platforms.MIDNIGHTBSD)                       | MidnightBSD                                 |
| `@skip_mips`                 | `@unless_mips`                 | [`MIPS`](architectures.md#extra_platforms.MIPS)                                 | MIPS (32-bit, big-endian)                   |
| `@skip_mips64`               | `@unless_mips64`               | [`MIPS64`](architectures.md#extra_platforms.MIPS64)                             | MIPS64 (big-endian)                         |
| `@skip_mips64el`             | `@unless_mips64el`             | [`MIPS64EL`](architectures.md#extra_platforms.MIPS64EL)                         | MIPS64 (little-endian)                      |
| `@skip_mipsel`               | `@unless_mipsel`               | [`MIPSEL`](architectures.md#extra_platforms.MIPSEL)                             | MIPS (32-bit, little-endian)                |
| `@skip_netbsd`               | `@unless_netbsd`               | [`NETBSD`](platforms.md#extra_platforms.NETBSD)                                 | NetBSD                                      |
| `@skip_nobara`               | `@unless_nobara`               | [`NOBARA`](platforms.md#extra_platforms.NOBARA)                                 | Nobara                                      |
| `@skip_openbsd`              | `@unless_openbsd`              | [`OPENBSD`](platforms.md#extra_platforms.OPENBSD)                               | OpenBSD                                     |
| `@skip_opensuse`             | `@unless_opensuse`             | [`OPENSUSE`](platforms.md#extra_platforms.OPENSUSE)                             | openSUSE                                    |
| `@skip_oracle`               | `@unless_oracle`               | [`ORACLE`](platforms.md#extra_platforms.ORACLE)                                 | Oracle Linux                                |
| `@skip_other_unix`           | `@unless_other_unix`           | [`OTHER_UNIX`](groups.md#extra_platforms.OTHER_UNIX)                            | Any other Unix                              |
| `@skip_parallels`            | `@unless_parallels`            | [`PARALLELS`](platforms.md#extra_platforms.PARALLELS)                           | Parallels                                   |
| `@skip_pidora`               | `@unless_pidora`               | [`PIDORA`](platforms.md#extra_platforms.PIDORA)                                 | Pidora                                      |
| `@skip_powerpc`              | `@unless_powerpc`              | [`POWERPC`](groups.md#extra_platforms.POWERPC)                                  | PowerPC family                              |
| `@skip_ppc`                  | `@unless_ppc`                  | [`PPC`](architectures.md#extra_platforms.PPC)                                   | PowerPC (32-bit)                            |
| `@skip_ppc64`                | `@unless_ppc64`                | [`PPC64`](architectures.md#extra_platforms.PPC64)                               | PowerPC 64-bit (big-endian)                 |
| `@skip_ppc64le`              | `@unless_ppc64le`              | [`PPC64LE`](architectures.md#extra_platforms.PPC64LE)                           | PowerPC 64-bit (little-endian)              |
| `@skip_raspbian`             | `@unless_raspbian`             | [`RASPBIAN`](platforms.md#extra_platforms.RASPBIAN)                             | Raspbian                                    |
| `@skip_rhel`                 | `@unless_rhel`                 | [`RHEL`](platforms.md#extra_platforms.RHEL)                                     | RedHat Enterprise Linux                     |
| `@skip_riscv`                | `@unless_riscv`                | [`RISCV`](groups.md#extra_platforms.RISCV)                                      | RISC-V family                               |
| `@skip_riscv32`              | `@unless_riscv32`              | [`RISCV32`](architectures.md#extra_platforms.RISCV32)                           | RISC-V (32-bit)                             |
| `@skip_riscv64`              | `@unless_riscv64`              | [`RISCV64`](architectures.md#extra_platforms.RISCV64)                           | RISC-V (64-bit)                             |
| `@skip_rocky`                | `@unless_rocky`                | [`ROCKY`](platforms.md#extra_platforms.ROCKY)                                   | Rocky Linux                                 |
| `@skip_s390x`                | `@unless_s390x`                | [`S390X`](architectures.md#extra_platforms.S390X)                               | IBM z/Architecture (s390x)                  |
| `@skip_scientific`           | `@unless_scientific`           | [`SCIENTIFIC`](platforms.md#extra_platforms.SCIENTIFIC)                         | Scientific Linux                            |
| `@skip_slackware`            | `@unless_slackware`            | [`SLACKWARE`](platforms.md#extra_platforms.SLACKWARE)                           | Slackware                                   |
| `@skip_sles`                 | `@unless_sles`                 | [`SLES`](platforms.md#extra_platforms.SLES)                                     | SUSE Linux Enterprise Server                |
| `@skip_solaris`              | `@unless_solaris`              | [`SOLARIS`](platforms.md#extra_platforms.SOLARIS)                               | Solaris                                     |
| `@skip_sparc`                | `@unless_sparc`                | [`SPARC`](architectures.md#extra_platforms.SPARC)                               | SPARC (32-bit)                              |
| `@skip_sparc64`              | `@unless_sparc64`              | [`SPARC64`](architectures.md#extra_platforms.SPARC64)                           | SPARC (64-bit)                              |
| `@skip_sunos`                | `@unless_sunos`                | [`SUNOS`](platforms.md#extra_platforms.SUNOS)                                   | SunOS                                       |
| `@skip_system_v`             | `@unless_system_v`             | [`SYSTEM_V`](groups.md#extra_platforms.SYSTEM_V)                                | AT&T System Five                            |
| `@skip_teamcity`             | `@unless_teamcity`             | [`TEAMCITY`](ci.md#extra_platforms.TEAMCITY)                                    | TeamCity                                    |
| `@skip_travis_ci`            | `@unless_travis_ci`            | [`TRAVIS_CI`](ci.md#extra_platforms.TRAVIS_CI)                                  | Travis CI                                   |
| `@skip_tumbleweed`           | `@unless_tumbleweed`           | [`TUMBLEWEED`](platforms.md#extra_platforms.TUMBLEWEED)                         | openSUSE Tumbleweed                         |
| `@skip_tuxedo`               | `@unless_tuxedo`               | [`TUXEDO`](platforms.md#extra_platforms.TUXEDO)                                 | Tuxedo OS                                   |
| `@skip_ubuntu`               | `@unless_ubuntu`               | [`UBUNTU`](platforms.md#extra_platforms.UBUNTU)                                 | Ubuntu                                      |
| `@skip_ultramarine`          | `@unless_ultramarine`          | [`ULTRAMARINE`](platforms.md#extra_platforms.ULTRAMARINE)                       | Ultramarine                                 |
| `@skip_unix`                 | `@unless_unix`                 | [`UNIX`](groups.md#extra_platforms.UNIX)                                        | Any Unix                                    |
| `@skip_unix_layers`          | `@unless_unix_layers`          | [`UNIX_LAYERS`](groups.md#extra_platforms.UNIX_LAYERS)                          | Any Unix compatibility layers               |
| `@skip_unix_without_macos`   | `@unless_unix_without_macos`   | [`UNIX_WITHOUT_MACOS`](groups.md#extra_platforms.UNIX_WITHOUT_MACOS)            | Any Unix excluding macOS                    |
| `@skip_unknown`              | `@unless_unknown`              | [`UNKNOWN`](groups.md#extra_platforms.UNKNOWN)                                  | Unknown                                     |
| `@skip_unknown_architecture` | `@unless_unknown_architecture` | [`UNKNOWN_ARCHITECTURE`](architectures.md#extra_platforms.UNKNOWN_ARCHITECTURE) | Unknown architecture                        |
| `@skip_unknown_ci`           | `@unless_unknown_ci`           | [`UNKNOWN_CI`](ci.md#extra_platforms.UNKNOWN_CI)                                | Unknown CI                                  |
| `@skip_unknown_platform`     | `@unless_unknown_platform`     | [`UNKNOWN_PLATFORM`](platforms.md#extra_platforms.UNKNOWN_PLATFORM)             | Unknown platform                            |
| `@skip_wasm32`               | `@unless_wasm32`               | [`WASM32`](architectures.md#extra_platforms.WASM32)                             | WebAssembly (32-bit)                        |
| `@skip_wasm64`               | `@unless_wasm64`               | [`WASM64`](architectures.md#extra_platforms.WASM64)                             | WebAssembly (64-bit)                        |
| `@skip_webassembly`          | `@unless_webassembly`          | [`WEBASSEMBLY`](groups.md#extra_platforms.WEBASSEMBLY)                          | WebAssembly                                 |
| `@skip_windows`              | `@unless_windows`              | [`WINDOWS`](platforms.md#extra_platforms.WINDOWS)                               | Windows                                     |
| `@skip_wsl1`                 | `@unless_wsl1`                 | [`WSL1`](platforms.md#extra_platforms.WSL1)                                     | Windows Subsystem for Linux v1              |
| `@skip_wsl2`                 | `@unless_wsl2`                 | [`WSL2`](platforms.md#extra_platforms.WSL2)                                     | Windows Subsystem for Linux v2              |
| `@skip_x86`                  | `@unless_x86`                  | [`X86`](groups.md#extra_platforms.X86)                                          | x86 family                                  |
| `@skip_x86_64`               | `@unless_x86_64`               | [`X86_64`](architectures.md#extra_platforms.X86_64)                             | x86-64 (AMD64)                              |
| `@skip_xenserver`            | `@unless_xenserver`            | [`XENSERVER`](platforms.md#extra_platforms.XENSERVER)                           | XenServer                                   |

<!-- decorators-table-end -->

## `extra_platforms.pytest` API

```{eval-rst}
.. autoclasstree:: extra_platforms.pytest
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.pytest
   :members:
   :undoc-members:
   :show-inheritance:
```
