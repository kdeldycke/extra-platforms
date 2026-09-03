# {octicon}`meter` Pytest

```{py:module} extra_platforms.pytest
:no-typesetting:
:no-contents-entry:
```

```{py:currentmodule} extra_platforms
```

````{important}
For these helpers to work, you need to install ``extra_platforms``'s additional dependencies from the ``pytest`` extra group:

```shell-session
$ uv pip install 'extra-platforms[pytest]'
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

## Test helpers

Beyond the per-trait decorators, the `extra_platforms.pytest` module ships helpers that are absent from the table below.

### Fake executables

Some tests drive a command through a real subprocess. `write_fake_executable` writes a stand-in that still runs in a sandbox shipping no `/bin/sh`:

```{eval-rst}
.. autofunction:: extra_platforms.pytest.write_fake_executable
```

## All decorators

```{python:render}
:mirror:
from itertools import chain

from extra_platforms import ALL_GROUPS, ALL_TRAITS
from extra_platforms._docs import generate_decorators_table

print(generate_decorators_table(chain(ALL_TRAITS, ALL_GROUPS)))
```

<!-- mirror -->

| Skip decorator                            | Unless decorator                            | Icon | Associated symbol             |
| :---------------------------------------- | :------------------------------------------ | :--: | :---------------------------- |
| {deco}`~pytest.skip_aarch64`              | {deco}`~pytest.unless_aarch64`              |  📱  | {data}`~AARCH64`              |
| {deco}`~pytest.skip_aix`                  | {deco}`~pytest.unless_aix`                  |  ➿  | {data}`~AIX`                  |
| {deco}`~pytest.skip_alacritty`            | {deco}`~pytest.unless_alacritty`            |  🔳  | {data}`~ALACRITTY`            |
| {deco}`~pytest.skip_all_agents`           | {deco}`~pytest.unless_any_agent`            |  🧠  | {data}`~ALL_AGENTS`           |
| {deco}`~pytest.skip_all_architectures`    | {deco}`~pytest.unless_any_architecture`     |  🏛️  | {data}`~ALL_ARCHITECTURES`    |
| {deco}`~pytest.skip_all_arm`              | {deco}`~pytest.unless_any_arm`              |  📱  | {data}`~ALL_ARM`              |
| {deco}`~pytest.skip_all_ci`               | {deco}`~pytest.unless_any_ci`               |  ♺   | {data}`~ALL_CI`               |
| {deco}`~pytest.skip_all_mips`             | {deco}`~pytest.unless_any_mips`             |  🔲  | {data}`~ALL_MIPS`             |
| {deco}`~pytest.skip_all_platforms`        | {deco}`~pytest.unless_any_platform`         |  ⚙️  | {data}`~ALL_PLATFORMS`        |
| {deco}`~pytest.skip_all_shells`           | {deco}`~pytest.unless_any_shell`            |  🐚  | {data}`~ALL_SHELLS`           |
| {deco}`~pytest.skip_all_sparc`            | {deco}`~pytest.unless_any_sparc`            |  ☀️  | {data}`~ALL_SPARC`            |
| {deco}`~pytest.skip_all_terminals`        | {deco}`~pytest.unless_any_terminal`         |  💻  | {data}`~ALL_TERMINALS`        |
| {deco}`~pytest.skip_all_traits`           | {deco}`~pytest.unless_any_trait`            |  ⁕   | {data}`~ALL_TRAITS`           |
| {deco}`~pytest.skip_all_windows`          | {deco}`~pytest.unless_any_windows`          |  🪟  | {data}`~ALL_WINDOWS`          |
| {deco}`~pytest.skip_almalinux`            | {deco}`~pytest.unless_almalinux`            |     | {data}`~ALMALINUX`            |
| {deco}`~pytest.skip_alpine`               | {deco}`~pytest.unless_alpine`               |  🏔️  | {data}`~ALPINE`               |
| {deco}`~pytest.skip_altlinux`             | {deco}`~pytest.unless_altlinux`             |  Δ   | {data}`~ALTLINUX`             |
| {deco}`~pytest.skip_amzn`                 | {deco}`~pytest.unless_amzn`                 |  ⤻   | {data}`~AMZN`                 |
| {deco}`~pytest.skip_android`              | {deco}`~pytest.unless_android`              |  🤖  | {data}`~ANDROID`              |
| {deco}`~pytest.skip_apple_terminal`       | {deco}`~pytest.unless_apple_terminal`       |  🍏  | {data}`~APPLE_TERMINAL`       |
| {deco}`~pytest.skip_arch`                 | {deco}`~pytest.unless_arch`                 |  🎗️  | {data}`~ARCH`                 |
| {deco}`~pytest.skip_arch_32_bit`          | {deco}`~pytest.unless_arch_32_bit`          |  ³²  | {data}`~ARCH_32_BIT`          |
| {deco}`~pytest.skip_arch_64_bit`          | {deco}`~pytest.unless_arch_64_bit`          |  ⁶⁴  | {data}`~ARCH_64_BIT`          |
| {deco}`~pytest.skip_arm`                  | {deco}`~pytest.unless_arm`                  |  📱  | {data}`~ARM`                  |
| {deco}`~pytest.skip_armv5tel`             | {deco}`~pytest.unless_armv5tel`             |  📱  | {data}`~ARMV5TEL`             |
| {deco}`~pytest.skip_armv6l`               | {deco}`~pytest.unless_armv6l`               |  📱  | {data}`~ARMV6L`               |
| {deco}`~pytest.skip_armv7l`               | {deco}`~pytest.unless_armv7l`               |  📱  | {data}`~ARMV7L`               |
| {deco}`~pytest.skip_armv8l`               | {deco}`~pytest.unless_armv8l`               |  📱  | {data}`~ARMV8L`               |
| {deco}`~pytest.skip_ash`                  | {deco}`~pytest.unless_ash`                  |  🪶  | {data}`~ASH`                  |
| {deco}`~pytest.skip_azure_pipelines`      | {deco}`~pytest.unless_azure_pipelines`      |  ═   | {data}`~AZURE_PIPELINES`      |
| {deco}`~pytest.skip_bamboo`               | {deco}`~pytest.unless_bamboo`               |  ⟲   | {data}`~BAMBOO`               |
| {deco}`~pytest.skip_bash`                 | {deco}`~pytest.unless_bash`                 |  ＃  | {data}`~BASH`                 |
| {deco}`~pytest.skip_big_endian`           | {deco}`~pytest.unless_big_endian`           |  ⬆️  | {data}`~BIG_ENDIAN`           |
| {deco}`~pytest.skip_bourne_shells`        | {deco}`~pytest.unless_bourne_shells`        |  💲  | {data}`~BOURNE_SHELLS`        |
| {deco}`~pytest.skip_bsd`                  | {deco}`~pytest.unless_bsd`                  |  Ⓑ   | {data}`~BSD`                  |
| {deco}`~pytest.skip_bsd_not_macos`        | {deco}`~pytest.unless_bsd_not_macos`        |  🅱️  | {data}`~BSD_WITHOUT_MACOS`    |
| {deco}`~pytest.skip_buildkite`            | {deco}`~pytest.unless_buildkite`            |  🪁  | {data}`~BUILDKITE`            |
| {deco}`~pytest.skip_buildroot`            | {deco}`~pytest.unless_buildroot`            |  ⛑️  | {data}`~BUILDROOT`            |
| {deco}`~pytest.skip_c_shells`             | {deco}`~pytest.unless_c_shells`             |  🅲   | {data}`~C_SHELLS`             |
| {deco}`~pytest.skip_cachyos`              | {deco}`~pytest.unless_cachyos`              |  ⌬   | {data}`~CACHYOS`              |
| {deco}`~pytest.skip_centos`               | {deco}`~pytest.unless_centos`               |  💠  | {data}`~CENTOS`               |
| {deco}`~pytest.skip_chromeos`             | {deco}`~pytest.unless_chromeos`             |  🧿  | {data}`~CHROMEOS`             |
| {deco}`~pytest.skip_circle_ci`            | {deco}`~pytest.unless_circle_ci`            |  ⪾   | {data}`~CIRCLE_CI`            |
| {deco}`~pytest.skip_cirrus_ci`            | {deco}`~pytest.unless_cirrus_ci`            |  ≋   | {data}`~CIRRUS_CI`            |
| {deco}`~pytest.skip_claude_code`          | {deco}`~pytest.unless_claude_code`          |  ✴️  | {data}`~CLAUDE_CODE`          |
| {deco}`~pytest.skip_clearlinux`           | {deco}`~pytest.unless_clearlinux`           |  ✳️  | {data}`~CLEARLINUX`           |
| {deco}`~pytest.skip_cline`                | {deco}`~pytest.unless_cline`                |  👾  | {data}`~CLINE`                |
| {deco}`~pytest.skip_cloudlinux`           | {deco}`~pytest.unless_cloudlinux`           |  ꩜   | {data}`~CLOUDLINUX`           |
| {deco}`~pytest.skip_cmd`                  | {deco}`~pytest.unless_cmd`                  |  ▶   | {data}`~CMD`                  |
| {deco}`~pytest.skip_codebuild`            | {deco}`~pytest.unless_codebuild`            |  ᚙ   | {data}`~CODEBUILD`            |
| {deco}`~pytest.skip_codex`                | {deco}`~pytest.unless_codex`                |  📕  | {data}`~CODEX`                |
| {deco}`~pytest.skip_contour`              | {deco}`~pytest.unless_contour`              |  ◰   | {data}`~CONTOUR`              |
| {deco}`~pytest.skip_copilot_cli`          | {deco}`~pytest.unless_copilot_cli`          |  ✈️  | {data}`~COPILOT_CLI`          |
| {deco}`~pytest.skip_crush`                | {deco}`~pytest.unless_crush`                |  💘  | {data}`~CRUSH`                |
| {deco}`~pytest.skip_csh`                  | {deco}`~pytest.unless_csh`                  |  𝐂   | {data}`~CSH`                  |
| {deco}`~pytest.skip_cursor`               | {deco}`~pytest.unless_cursor`               |  ➤   | {data}`~CURSOR`               |
| {deco}`~pytest.skip_cygwin`               | {deco}`~pytest.unless_cygwin`               |  Ͼ   | {data}`~CYGWIN`               |
| {deco}`~pytest.skip_dash`                 | {deco}`~pytest.unless_dash`                 |  💨  | {data}`~DASH`                 |
| {deco}`~pytest.skip_debian`               | {deco}`~pytest.unless_debian`               |  🌀  | {data}`~DEBIAN`               |
| {deco}`~pytest.skip_dragonfly_bsd`        | {deco}`~pytest.unless_dragonfly_bsd`        |  🪰  | {data}`~DRAGONFLY_BSD`        |
| {deco}`~pytest.skip_endeavouros`          | {deco}`~pytest.unless_endeavouros`          |  🚀  | {data}`~ENDEAVOUROS`          |
| {deco}`~pytest.skip_exherbo`              | {deco}`~pytest.unless_exherbo`              |  🐽  | {data}`~EXHERBO`              |
| {deco}`~pytest.skip_fedora`               | {deco}`~pytest.unless_fedora`               |  🎩  | {data}`~FEDORA`               |
| {deco}`~pytest.skip_fish`                 | {deco}`~pytest.unless_fish`                 |  🐟  | {data}`~FISH`                 |
| {deco}`~pytest.skip_foot`                 | {deco}`~pytest.unless_foot`                 |  🦶  | {data}`~FOOT`                 |
| {deco}`~pytest.skip_freebsd`              | {deco}`~pytest.unless_freebsd`              |  😈  | {data}`~FREEBSD`              |
| {deco}`~pytest.skip_gemini_cli`           | {deco}`~pytest.unless_gemini_cli`           |  ♊  | {data}`~GEMINI_CLI`           |
| {deco}`~pytest.skip_generic_linux`        | {deco}`~pytest.unless_generic_linux`        |  🥚  | {data}`~GENERIC_LINUX`        |
| {deco}`~pytest.skip_gentoo`               | {deco}`~pytest.unless_gentoo`               |  🗜️  | {data}`~GENTOO`               |
| {deco}`~pytest.skip_ghostty`              | {deco}`~pytest.unless_ghostty`              |  👻  | {data}`~GHOSTTY`              |
| {deco}`~pytest.skip_github_ci`            | {deco}`~pytest.unless_github_ci`            |  🐙  | {data}`~GITHUB_CI`            |
| {deco}`~pytest.skip_gitlab_ci`            | {deco}`~pytest.unless_gitlab_ci`            |  🦊  | {data}`~GITLAB_CI`            |
| {deco}`~pytest.skip_gnome_terminal`       | {deco}`~pytest.unless_gnome_terminal`       |  𝐆   | {data}`~GNOME_TERMINAL`       |
| {deco}`~pytest.skip_gnu_screen`           | {deco}`~pytest.unless_gnu_screen`           |  📺  | {data}`~GNU_SCREEN`           |
| {deco}`~pytest.skip_gpu_terminals`        | {deco}`~pytest.unless_gpu_terminals`        |  🎮  | {data}`~GPU_TERMINALS`        |
| {deco}`~pytest.skip_guix`                 | {deco}`~pytest.unless_guix`                 |  🐃  | {data}`~GUIX`                 |
| {deco}`~pytest.skip_haiku`                | {deco}`~pytest.unless_haiku`                |  🍂  | {data}`~HAIKU`                |
| {deco}`~pytest.skip_hermetic_build`       | {deco}`~pytest.unless_hermetic_build`       |  🥫  | {data}`~HERMETIC_BUILD`       |
| {deco}`~pytest.skip_heroku_ci`            | {deco}`~pytest.unless_heroku_ci`            |  ⥁   | {data}`~HEROKU_CI`            |
| {deco}`~pytest.skip_hurd`                 | {deco}`~pytest.unless_hurd`                 |  🦬  | {data}`~HURD`                 |
| {deco}`~pytest.skip_hyper`                | {deco}`~pytest.unless_hyper`                |  ⬡   | {data}`~HYPER`                |
| {deco}`~pytest.skip_i386`                 | {deco}`~pytest.unless_i386`                 |  𝗶   | {data}`~I386`                 |
| {deco}`~pytest.skip_i586`                 | {deco}`~pytest.unless_i586`                 |  𝗶   | {data}`~I586`                 |
| {deco}`~pytest.skip_i686`                 | {deco}`~pytest.unless_i686`                 |  𝗶   | {data}`~I686`                 |
| {deco}`~pytest.skip_ibm_mainframe`        | {deco}`~pytest.unless_ibm_mainframe`        |  🏢  | {data}`~IBM_MAINFRAME`        |
| {deco}`~pytest.skip_ibm_powerkvm`         | {deco}`~pytest.unless_ibm_powerkvm`         |  🤹  | {data}`~IBM_POWERKVM`         |
| {deco}`~pytest.skip_illumos`              | {deco}`~pytest.unless_illumos`              |  🔥  | {data}`~ILLUMOS`              |
| {deco}`~pytest.skip_iterm2`               | {deco}`~pytest.unless_iterm2`               |  ⬛  | {data}`~ITERM2`               |
| {deco}`~pytest.skip_kali`                 | {deco}`~pytest.unless_kali`                 |  🔱  | {data}`~KALI`                 |
| {deco}`~pytest.skip_kitty`                | {deco}`~pytest.unless_kitty`                |  🐱  | {data}`~KITTY`                |
| {deco}`~pytest.skip_konsole`              | {deco}`~pytest.unless_konsole`              |  💎  | {data}`~KONSOLE`              |
| {deco}`~pytest.skip_ksh`                  | {deco}`~pytest.unless_ksh`                  |  𝐊   | {data}`~KSH`                  |
| {deco}`~pytest.skip_kvmibm`               | {deco}`~pytest.unless_kvmibm`               |  🤹  | {data}`~KVMIBM`               |
| {deco}`~pytest.skip_linux`                | {deco}`~pytest.unless_linux`                |  🐧  | {data}`~LINUX`                |
| {deco}`~pytest.skip_linux_layers`         | {deco}`~pytest.unless_linux_layers`         |  ≚   | {data}`~LINUX_LAYERS`         |
| {deco}`~pytest.skip_linux_like`           | {deco}`~pytest.unless_linux_like`           |  🐣  | {data}`~LINUX_LIKE`           |
| {deco}`~pytest.skip_linuxmint`            | {deco}`~pytest.unless_linuxmint`            |  🌿  | {data}`~LINUXMINT`            |
| {deco}`~pytest.skip_little_endian`        | {deco}`~pytest.unless_little_endian`        |  ⬇️  | {data}`~LITTLE_ENDIAN`        |
| {deco}`~pytest.skip_loongarch`            | {deco}`~pytest.unless_loongarch`            |  🐉  | {data}`~LOONGARCH`            |
| {deco}`~pytest.skip_loongarch64`          | {deco}`~pytest.unless_loongarch64`          |  🐉  | {data}`~LOONGARCH64`          |
| {deco}`~pytest.skip_macos`                | {deco}`~pytest.unless_macos`                |  🍎  | {data}`~MACOS`                |
| {deco}`~pytest.skip_mageia`               | {deco}`~pytest.unless_mageia`               |  ⍥   | {data}`~MAGEIA`               |
| {deco}`~pytest.skip_mandriva`             | {deco}`~pytest.unless_mandriva`             |  💫  | {data}`~MANDRIVA`             |
| {deco}`~pytest.skip_manjaro`              | {deco}`~pytest.unless_manjaro`              |  ▲   | {data}`~MANJARO`              |
| {deco}`~pytest.skip_midnightbsd`          | {deco}`~pytest.unless_midnightbsd`          |  🌘  | {data}`~MIDNIGHTBSD`          |
| {deco}`~pytest.skip_mips`                 | {deco}`~pytest.unless_mips`                 |  🔲  | {data}`~MIPS`                 |
| {deco}`~pytest.skip_mips64`               | {deco}`~pytest.unless_mips64`               |  🔲  | {data}`~MIPS64`               |
| {deco}`~pytest.skip_mips64el`             | {deco}`~pytest.unless_mips64el`             |  🔲  | {data}`~MIPS64EL`             |
| {deco}`~pytest.skip_mipsel`               | {deco}`~pytest.unless_mipsel`               |  🔲  | {data}`~MIPSEL`               |
| {deco}`~pytest.skip_multiplexers`         | {deco}`~pytest.unless_multiplexers`         |  ⧉   | {data}`~MULTIPLEXERS`         |
| {deco}`~pytest.skip_native_terminals`     | {deco}`~pytest.unless_native_terminals`     |  ▦   | {data}`~NATIVE_TERMINALS`     |
| {deco}`~pytest.skip_netbsd`               | {deco}`~pytest.unless_netbsd`               |  🚩  | {data}`~NETBSD`               |
| {deco}`~pytest.skip_nixos`                | {deco}`~pytest.unless_nixos`                |  ❄️  | {data}`~NIXOS`                |
| {deco}`~pytest.skip_nobara`               | {deco}`~pytest.unless_nobara`               |     | {data}`~NOBARA`               |
| {deco}`~pytest.skip_nushell`              | {deco}`~pytest.unless_nushell`              |  𝜈   | {data}`~NUSHELL`              |
| {deco}`~pytest.skip_openbsd`              | {deco}`~pytest.unless_openbsd`              |  🐡  | {data}`~OPENBSD`              |
| {deco}`~pytest.skip_opensuse`             | {deco}`~pytest.unless_opensuse`             |  🦎  | {data}`~OPENSUSE`             |
| {deco}`~pytest.skip_openwrt`              | {deco}`~pytest.unless_openwrt`              |  📶  | {data}`~OPENWRT`              |
| {deco}`~pytest.skip_oracle`               | {deco}`~pytest.unless_oracle`               |  🦴  | {data}`~ORACLE`               |
| {deco}`~pytest.skip_os400`                | {deco}`~pytest.unless_os400`                |  🟦  | {data}`~OS400`                |
| {deco}`~pytest.skip_other_posix`          | {deco}`~pytest.unless_other_posix`          |  🅟   | {data}`~OTHER_POSIX`          |
| {deco}`~pytest.skip_other_shells`         | {deco}`~pytest.unless_other_shells`         |  ◇   | {data}`~OTHER_SHELLS`         |
| {deco}`~pytest.skip_parallels`            | {deco}`~pytest.unless_parallels`            |  ∥   | {data}`~PARALLELS`            |
| {deco}`~pytest.skip_pi`                   | {deco}`~pytest.unless_pi`                   |  π   | {data}`~PI`                   |
| {deco}`~pytest.skip_pidora`               | {deco}`~pytest.unless_pidora`               |  🍓  | {data}`~PIDORA`               |
| {deco}`~pytest.skip_pikaos`               | {deco}`~pytest.unless_pikaos`               |  🐹  | {data}`~PIKAOS`               |
| {deco}`~pytest.skip_powerpc`              | {deco}`~pytest.unless_powerpc`              |  ⚡  | {data}`~POWERPC`              |
| {deco}`~pytest.skip_powershell`           | {deco}`~pytest.unless_powershell`           |  🔷  | {data}`~POWERSHELL`           |
| {deco}`~pytest.skip_ppc`                  | {deco}`~pytest.unless_ppc`                  |  ⚡  | {data}`~PPC`                  |
| {deco}`~pytest.skip_ppc64`                | {deco}`~pytest.unless_ppc64`                |  ⚡  | {data}`~PPC64`                |
| {deco}`~pytest.skip_ppc64le`              | {deco}`~pytest.unless_ppc64le`              |  ⚡  | {data}`~PPC64LE`              |
| {deco}`~pytest.skip_raspbian`             | {deco}`~pytest.unless_raspbian`             |  🍓  | {data}`~RASPBIAN`             |
| {deco}`~pytest.skip_rhel`                 | {deco}`~pytest.unless_rhel`                 |  🎩  | {data}`~RHEL`                 |
| {deco}`~pytest.skip_rio`                  | {deco}`~pytest.unless_rio`                  |  🏞️  | {data}`~RIO`                  |
| {deco}`~pytest.skip_riscv`                | {deco}`~pytest.unless_riscv`                |  Ⅴ   | {data}`~RISCV`                |
| {deco}`~pytest.skip_riscv32`              | {deco}`~pytest.unless_riscv32`              |  Ⅴ   | {data}`~RISCV32`              |
| {deco}`~pytest.skip_riscv64`              | {deco}`~pytest.unless_riscv64`              |  Ⅴ   | {data}`~RISCV64`              |
| {deco}`~pytest.skip_rocky`                | {deco}`~pytest.unless_rocky`                |  ⛰️  | {data}`~ROCKY`                |
| {deco}`~pytest.skip_s390x`                | {deco}`~pytest.unless_s390x`                |  🏢  | {data}`~S390X`                |
| {deco}`~pytest.skip_scientific`           | {deco}`~pytest.unless_scientific`           |  ⚛️  | {data}`~SCIENTIFIC`           |
| {deco}`~pytest.skip_sh`                   | {deco}`~pytest.unless_sh`                   |  𝐒   | {data}`~SH`                   |
| {deco}`~pytest.skip_slackware`            | {deco}`~pytest.unless_slackware`            |  🚬  | {data}`~SLACKWARE`            |
| {deco}`~pytest.skip_sles`                 | {deco}`~pytest.unless_sles`                 |  🦎  | {data}`~SLES`                 |
| {deco}`~pytest.skip_slitaz`               | {deco}`~pytest.unless_slitaz`               |  🕷️  | {data}`~SLITAZ`               |
| {deco}`~pytest.skip_solaris`              | {deco}`~pytest.unless_solaris`              |  🌞  | {data}`~SOLARIS`              |
| {deco}`~pytest.skip_sourcemage`           | {deco}`~pytest.unless_sourcemage`           |  🧙  | {data}`~SOURCEMAGE`           |
| {deco}`~pytest.skip_sparc`                | {deco}`~pytest.unless_sparc`                |  ☀️  | {data}`~SPARC`                |
| {deco}`~pytest.skip_sparc64`              | {deco}`~pytest.unless_sparc64`              |  ☀️  | {data}`~SPARC64`              |
| {deco}`~pytest.skip_sunos`                | {deco}`~pytest.unless_sunos`                |  🌅  | {data}`~SUNOS`                |
| {deco}`~pytest.skip_system_v`             | {deco}`~pytest.unless_system_v`             |  𝐕   | {data}`~SYSTEM_V`             |
| {deco}`~pytest.skip_tabby`                | {deco}`~pytest.unless_tabby`                |  🐈  | {data}`~TABBY`                |
| {deco}`~pytest.skip_tcsh`                 | {deco}`~pytest.unless_tcsh`                 |  𝐓   | {data}`~TCSH`                 |
| {deco}`~pytest.skip_teamcity`             | {deco}`~pytest.unless_teamcity`             |  🏙️  | {data}`~TEAMCITY`             |
| {deco}`~pytest.skip_tilix`                | {deco}`~pytest.unless_tilix`                |  🔀  | {data}`~TILIX`                |
| {deco}`~pytest.skip_tmux`                 | {deco}`~pytest.unless_tmux`                 |  📟  | {data}`~TMUX`                 |
| {deco}`~pytest.skip_travis_ci`            | {deco}`~pytest.unless_travis_ci`            |  👷  | {data}`~TRAVIS_CI`            |
| {deco}`~pytest.skip_tuxedo`               | {deco}`~pytest.unless_tuxedo`               |  🤵  | {data}`~TUXEDO`               |
| {deco}`~pytest.skip_ubuntu`               | {deco}`~pytest.unless_ubuntu`               |  🎯  | {data}`~UBUNTU`               |
| {deco}`~pytest.skip_ultramarine`          | {deco}`~pytest.unless_ultramarine`          |  🌊  | {data}`~ULTRAMARINE`          |
| {deco}`~pytest.skip_unix`                 | {deco}`~pytest.unless_unix`                 |  ⨷   | {data}`~UNIX`                 |
| {deco}`~pytest.skip_unix_layers`          | {deco}`~pytest.unless_unix_layers`          |  ≛   | {data}`~UNIX_LAYERS`          |
| {deco}`~pytest.skip_unix_not_macos`       | {deco}`~pytest.unless_unix_not_macos`       |  ⨂   | {data}`~UNIX_WITHOUT_MACOS`   |
| {deco}`~pytest.skip_unknown`              | {deco}`~pytest.unless_unknown`              |  ❓  | {data}`~UNKNOWN`              |
| {deco}`~pytest.skip_unknown_agent`        | {deco}`~pytest.unless_unknown_agent`        |  ❓  | {data}`~UNKNOWN_AGENT`        |
| {deco}`~pytest.skip_unknown_architecture` | {deco}`~pytest.unless_unknown_architecture` |  ❓  | {data}`~UNKNOWN_ARCHITECTURE` |
| {deco}`~pytest.skip_unknown_ci`           | {deco}`~pytest.unless_unknown_ci`           |  ❓  | {data}`~UNKNOWN_CI`           |
| {deco}`~pytest.skip_unknown_platform`     | {deco}`~pytest.unless_unknown_platform`     |  ❓  | {data}`~UNKNOWN_PLATFORM`     |
| {deco}`~pytest.skip_unknown_shell`        | {deco}`~pytest.unless_unknown_shell`        |  ❓  | {data}`~UNKNOWN_SHELL`        |
| {deco}`~pytest.skip_unknown_terminal`     | {deco}`~pytest.unless_unknown_terminal`     |  ❓  | {data}`~UNKNOWN_TERMINAL`     |
| {deco}`~pytest.skip_void`                 | {deco}`~pytest.unless_void`                 |  ∅   | {data}`~VOID`                 |
| {deco}`~pytest.skip_vscode_terminal`      | {deco}`~pytest.unless_vscode_terminal`      |  🔵  | {data}`~VSCODE_TERMINAL`      |
| {deco}`~pytest.skip_wasm32`               | {deco}`~pytest.unless_wasm32`               |  🌐  | {data}`~WASM32`               |
| {deco}`~pytest.skip_wasm64`               | {deco}`~pytest.unless_wasm64`               |  🌐  | {data}`~WASM64`               |
| {deco}`~pytest.skip_web_terminals`        | {deco}`~pytest.unless_web_terminals`        |  ⬢   | {data}`~WEB_TERMINALS`        |
| {deco}`~pytest.skip_webassembly`          | {deco}`~pytest.unless_webassembly`          |  🌐  | {data}`~WEBASSEMBLY`          |
| {deco}`~pytest.skip_wezterm`              | {deco}`~pytest.unless_wezterm`              |  🔡  | {data}`~WEZTERM`              |
| {deco}`~pytest.skip_windows`              | {deco}`~pytest.unless_windows`              |  🪟  | {data}`~WINDOWS`              |
| {deco}`~pytest.skip_windows_shells`       | {deco}`~pytest.unless_windows_shells`       |  ⌨️  | {data}`~WINDOWS_SHELLS`       |
| {deco}`~pytest.skip_windows_terminal`     | {deco}`~pytest.unless_windows_terminal`     |  ⊡   | {data}`~WINDOWS_TERMINAL`     |
| {deco}`~pytest.skip_wsl1`                 | {deco}`~pytest.unless_wsl1`                 |  ⊞   | {data}`~WSL1`                 |
| {deco}`~pytest.skip_wsl2`                 | {deco}`~pytest.unless_wsl2`                 |  ⊞   | {data}`~WSL2`                 |
| {deco}`~pytest.skip_x86`                  | {deco}`~pytest.unless_x86`                  |  𝘅   | {data}`~X86`                  |
| {deco}`~pytest.skip_x86_64`               | {deco}`~pytest.unless_x86_64`               |  🖥️  | {data}`~X86_64`               |
| {deco}`~pytest.skip_xenserver`            | {deco}`~pytest.unless_xenserver`            |  Ⓧ   | {data}`~XENSERVER`            |
| {deco}`~pytest.skip_xonsh`                | {deco}`~pytest.unless_xonsh`                |  🐍  | {data}`~XONSH`                |
| {deco}`~pytest.skip_xterm`                | {deco}`~pytest.unless_xterm`                |  𝐗   | {data}`~XTERM`                |
| {deco}`~pytest.skip_zellij`               | {deco}`~pytest.unless_zellij`               |  🪵  | {data}`~ZELLIJ`               |
| {deco}`~pytest.skip_zsh`                  | {deco}`~pytest.unless_zsh`                  |  ℤ   | {data}`~ZSH`                  |

<!-- mirror-end -->

```{python:render}
from itertools import chain

from extra_platforms import ALL_GROUPS, ALL_TRAITS
from extra_platforms._docs import generate_pytest_decorator_autodata

print(generate_pytest_decorator_autodata(chain(ALL_TRAITS, ALL_GROUPS)))
```
