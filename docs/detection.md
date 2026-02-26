# {octicon}`pulse` Detection

```{py:module} extra_platforms.detection
:no-typesetting:
:no-contents-entry:
```

```{py:currentmodule} extra_platforms
```

## All detection functions

<!-- all-detection-function-table-start -->

| Detection function               | Icon | Associated symbol             |
| :------------------------------- | :--: | :---------------------------- |
| {func}`~is_aarch64`              |  📱  | {data}`~AARCH64`              |
| {func}`~is_aix`                  |  ➿  | {data}`~AIX`                  |
| {func}`~is_alacritty`            |  🔳  | {data}`~ALACRITTY`            |
| {func}`~is_alpine`               |  🏔️  | {data}`~ALPINE`               |
| {func}`~is_altlinux`             |  Δ   | {data}`~ALTLINUX`             |
| {func}`~is_amzn`                 |  ⤻   | {data}`~AMZN`                 |
| {func}`~is_android`              |  🤖  | {data}`~ANDROID`              |
| {func}`~is_any_agent`            |  🧠  | {data}`~ALL_AGENTS`           |
| {func}`~is_any_architecture`     |  🏛️  | {data}`~ALL_ARCHITECTURES`    |
| {func}`~is_any_arm`              |  📱  | {data}`~ALL_ARM`              |
| {func}`~is_any_ci`               |  ♺   | {data}`~ALL_CI`               |
| {func}`~is_any_mips`             |  🔲  | {data}`~ALL_MIPS`             |
| {func}`~is_any_platform`         |  ⚙️  | {data}`~ALL_PLATFORMS`        |
| {func}`~is_any_shell`            |  🐚  | {data}`~ALL_SHELLS`           |
| {func}`~is_any_sparc`            |  ☀️  | {data}`~ALL_SPARC`            |
| {func}`~is_any_terminal`         |  💻  | {data}`~ALL_TERMINALS`        |
| {func}`~is_any_trait`            |  ⁕   | {data}`~ALL_TRAITS`           |
| {func}`~is_any_windows`          |  🪟  | {data}`~ALL_WINDOWS`          |
| {func}`~is_apple_terminal`       |  🍏  | {data}`~APPLE_TERMINAL`       |
| {func}`~is_arch`                 |  🎗️  | {data}`~ARCH`                 |
| {func}`~is_arch_32_bit`          |  ³²  | {data}`~ARCH_32_BIT`          |
| {func}`~is_arch_64_bit`          |  ⁶⁴  | {data}`~ARCH_64_BIT`          |
| {func}`~is_arm`                  |  📱  | {data}`~ARM`                  |
| {func}`~is_armv5tel`             |  📱  | {data}`~ARMV5TEL`             |
| {func}`~is_armv6l`               |  📱  | {data}`~ARMV6L`               |
| {func}`~is_armv7l`               |  📱  | {data}`~ARMV7L`               |
| {func}`~is_armv8l`               |  📱  | {data}`~ARMV8L`               |
| {func}`~is_ash`                  |  🪶  | {data}`~ASH`                  |
| {func}`~is_azure_pipelines`      |  ═   | {data}`~AZURE_PIPELINES`      |
| {func}`~is_bamboo`               |  ⟲   | {data}`~BAMBOO`               |
| {func}`~is_bash`                 |  ＃  | {data}`~BASH`                 |
| {func}`~is_big_endian`           |  ⬆️  | {data}`~BIG_ENDIAN`           |
| {func}`~is_bourne_shells`        |  💲  | {data}`~BOURNE_SHELLS`        |
| {func}`~is_bsd`                  |  Ⓑ   | {data}`~BSD`                  |
| {func}`~is_bsd_not_macos`        |  🅱️  | {data}`~BSD_WITHOUT_MACOS`    |
| {func}`~is_buildkite`            |  🪁  | {data}`~BUILDKITE`            |
| {func}`~is_buildroot`            |  ⛑️  | {data}`~BUILDROOT`            |
| {func}`~is_c_shells`             |  🅲   | {data}`~C_SHELLS`             |
| {func}`~is_cachyos`              |  ⌬   | {data}`~CACHYOS`              |
| {func}`~is_centos`               |  💠  | {data}`~CENTOS`               |
| {func}`~is_circle_ci`            |  ⪾   | {data}`~CIRCLE_CI`            |
| {func}`~is_cirrus_ci`            |  ≋   | {data}`~CIRRUS_CI`            |
| {func}`~is_claude_code`          |  ✴️  | {data}`~CLAUDE_CODE`          |
| {func}`~is_cline`                |  👾  | {data}`~CLINE`                |
| {func}`~is_cloudlinux`           |  ꩜   | {data}`~CLOUDLINUX`           |
| {func}`~is_cmd`                  |  ▶   | {data}`~CMD`                  |
| {func}`~is_codebuild`            |  ᚙ   | {data}`~CODEBUILD`            |
| {func}`~is_contour`              |  ◰   | {data}`~CONTOUR`              |
| {func}`~is_csh`                  |  𝐂   | {data}`~CSH`                  |
| {func}`~is_cursor`               |  ➤   | {data}`~CURSOR`               |
| {func}`~is_cygwin`               |  Ͼ   | {data}`~CYGWIN`               |
| {func}`~is_dash`                 |  💨  | {data}`~DASH`                 |
| {func}`~is_debian`               |  🌀  | {data}`~DEBIAN`               |
| {func}`~is_dragonfly_bsd`        |  🪰  | {data}`~DRAGONFLY_BSD`        |
| {func}`~is_exherbo`              |  🐽  | {data}`~EXHERBO`              |
| {func}`~is_fedora`               |  🎩  | {data}`~FEDORA`               |
| {func}`~is_fish`                 |  🐟  | {data}`~FISH`                 |
| {func}`~is_foot`                 |  🦶  | {data}`~FOOT`                 |
| {func}`~is_freebsd`              |  😈  | {data}`~FREEBSD`              |
| {func}`~is_gentoo`               |  🗜️  | {data}`~GENTOO`               |
| {func}`~is_ghostty`              |  👻  | {data}`~GHOSTTY`              |
| {func}`~is_github_ci`            |  🐙  | {data}`~GITHUB_CI`            |
| {func}`~is_gitlab_ci`            |  🦊  | {data}`~GITLAB_CI`            |
| {func}`~is_gnome_terminal`       |  𝐆   | {data}`~GNOME_TERMINAL`       |
| {func}`~is_gnu_screen`           |  📺  | {data}`~GNU_SCREEN`           |
| {func}`~is_gpu_terminals`        |  🎮  | {data}`~GPU_TERMINALS`        |
| {func}`~is_guix`                 |  🐃  | {data}`~GUIX`                 |
| {func}`~is_haiku`                |  🍂  | {data}`~HAIKU`                |
| {func}`~is_heroku_ci`            |  ⥁   | {data}`~HEROKU_CI`            |
| {func}`~is_hurd`                 |  🦬  | {data}`~HURD`                 |
| {func}`~is_hyper`                |  ⬡   | {data}`~HYPER`                |
| {func}`~is_i386`                 |  𝗶   | {data}`~I386`                 |
| {func}`~is_i586`                 |  𝗶   | {data}`~I586`                 |
| {func}`~is_i686`                 |  𝗶   | {data}`~I686`                 |
| {func}`~is_ibm_mainframe`        |  🏢  | {data}`~IBM_MAINFRAME`        |
| {func}`~is_ibm_powerkvm`         |  🤹  | {data}`~IBM_POWERKVM`         |
| {func}`~is_illumos`              |  🔥  | {data}`~ILLUMOS`              |
| {func}`~is_iterm2`               |  ⬛  | {data}`~ITERM2`               |
| {func}`~is_kali`                 |  🔱  | {data}`~KALI`                 |
| {func}`~is_kitty`                |  🐱  | {data}`~KITTY`                |
| {func}`~is_konsole`              |  💎  | {data}`~KONSOLE`              |
| {func}`~is_ksh`                  |  𝐊   | {data}`~KSH`                  |
| {func}`~is_kvmibm`               |  🤹  | {data}`~KVMIBM`               |
| {func}`~is_linux`                |  🐧  | {data}`~LINUX`                |
| {func}`~is_linux_layers`         |  ≚   | {data}`~LINUX_LAYERS`         |
| {func}`~is_linux_like`           |  🐣  | {data}`~LINUX_LIKE`           |
| {func}`~is_linuxmint`            |  🌿  | {data}`~LINUXMINT`            |
| {func}`~is_little_endian`        |  ⬇️  | {data}`~LITTLE_ENDIAN`        |
| {func}`~is_loongarch`            |  🐉  | {data}`~LOONGARCH`            |
| {func}`~is_loongarch64`          |  🐉  | {data}`~LOONGARCH64`          |
| {func}`~is_macos`                |  🍎  | {data}`~MACOS`                |
| {func}`~is_mageia`               |  ⍥   | {data}`~MAGEIA`               |
| {func}`~is_mandriva`             |  💫  | {data}`~MANDRIVA`             |
| {func}`~is_manjaro`              |  ▲   | {data}`~MANJARO`              |
| {func}`~is_midnightbsd`          |  🌘  | {data}`~MIDNIGHTBSD`          |
| {func}`~is_mips`                 |  🔲  | {data}`~MIPS`                 |
| {func}`~is_mips64`               |  🔲  | {data}`~MIPS64`               |
| {func}`~is_mips64el`             |  🔲  | {data}`~MIPS64EL`             |
| {func}`~is_mipsel`               |  🔲  | {data}`~MIPSEL`               |
| {func}`~is_multiplexers`         |  ⧉   | {data}`~MULTIPLEXERS`         |
| {func}`~is_native_terminals`     |  ▦   | {data}`~NATIVE_TERMINALS`     |
| {func}`~is_netbsd`               |  🚩  | {data}`~NETBSD`               |
| {func}`~is_nobara`               |     | {data}`~NOBARA`               |
| {func}`~is_nushell`              |  𝜈   | {data}`~NUSHELL`              |
| {func}`~is_openbsd`              |  🐡  | {data}`~OPENBSD`              |
| {func}`~is_opensuse`             |  🦎  | {data}`~OPENSUSE`             |
| {func}`~is_openwrt`              |  📶  | {data}`~OPENWRT`              |
| {func}`~is_oracle`               |  🦴  | {data}`~ORACLE`               |
| {func}`~is_other_posix`          |  🅟   | {data}`~OTHER_POSIX`          |
| {func}`~is_other_shells`         |  ◇   | {data}`~OTHER_SHELLS`         |
| {func}`~is_parallels`            |  ∥   | {data}`~PARALLELS`            |
| {func}`~is_pidora`               |  🍓  | {data}`~PIDORA`               |
| {func}`~is_powerpc`              |  ⚡  | {data}`~POWERPC`              |
| {func}`~is_powershell`           |  🔷  | {data}`~POWERSHELL`           |
| {func}`~is_ppc`                  |  ⚡  | {data}`~PPC`                  |
| {func}`~is_ppc64`                |  ⚡  | {data}`~PPC64`                |
| {func}`~is_ppc64le`              |  ⚡  | {data}`~PPC64LE`              |
| {func}`~is_raspbian`             |  🍓  | {data}`~RASPBIAN`             |
| {func}`~is_rhel`                 |  🎩  | {data}`~RHEL`                 |
| {func}`~is_rio`                  |  🏞️  | {data}`~RIO`                  |
| {func}`~is_riscv`                |  Ⅴ   | {data}`~RISCV`                |
| {func}`~is_riscv32`              |  Ⅴ   | {data}`~RISCV32`              |
| {func}`~is_riscv64`              |  Ⅴ   | {data}`~RISCV64`              |
| {func}`~is_rocky`                |  ⛰️  | {data}`~ROCKY`                |
| {func}`~is_s390x`                |  🏢  | {data}`~S390X`                |
| {func}`~is_scientific`           |  ⚛️  | {data}`~SCIENTIFIC`           |
| {func}`~is_slackware`            |  🚬  | {data}`~SLACKWARE`            |
| {func}`~is_sles`                 |  🦎  | {data}`~SLES`                 |
| {func}`~is_solaris`              |  🌞  | {data}`~SOLARIS`              |
| {func}`~is_sparc`                |  ☀️  | {data}`~SPARC`                |
| {func}`~is_sparc64`              |  ☀️  | {data}`~SPARC64`              |
| {func}`~is_sunos`                |  🌅  | {data}`~SUNOS`                |
| {func}`~is_system_v`             |  𝐕   | {data}`~SYSTEM_V`             |
| {func}`~is_tabby`                |  🐈  | {data}`~TABBY`                |
| {func}`~is_tcsh`                 |  𝐓   | {data}`~TCSH`                 |
| {func}`~is_teamcity`             |  🏙️  | {data}`~TEAMCITY`             |
| {func}`~is_tilix`                |  🔀  | {data}`~TILIX`                |
| {func}`~is_tmux`                 |  📟  | {data}`~TMUX`                 |
| {func}`~is_travis_ci`            |  👷  | {data}`~TRAVIS_CI`            |
| {func}`~is_tumbleweed`           |  ↻   | {data}`~TUMBLEWEED`           |
| {func}`~is_tuxedo`               |  🤵  | {data}`~TUXEDO`               |
| {func}`~is_ubuntu`               |  🎯  | {data}`~UBUNTU`               |
| {func}`~is_ultramarine`          |  🌊  | {data}`~ULTRAMARINE`          |
| {func}`~is_unix`                 |  ⨷   | {data}`~UNIX`                 |
| {func}`~is_unix_layers`          |  ≛   | {data}`~UNIX_LAYERS`          |
| {func}`~is_unix_not_macos`       |  ⨂   | {data}`~UNIX_WITHOUT_MACOS`   |
| {func}`~is_unknown`              |  ❓  | {data}`~UNKNOWN`              |
| {func}`~is_unknown_agent`        |  ❓  | {data}`~UNKNOWN_AGENT`        |
| {func}`~is_unknown_architecture` |  ❓  | {data}`~UNKNOWN_ARCHITECTURE` |
| {func}`~is_unknown_ci`           |  ❓  | {data}`~UNKNOWN_CI`           |
| {func}`~is_unknown_platform`     |  ❓  | {data}`~UNKNOWN_PLATFORM`     |
| {func}`~is_unknown_shell`        |  ❓  | {data}`~UNKNOWN_SHELL`        |
| {func}`~is_unknown_terminal`     |  ❓  | {data}`~UNKNOWN_TERMINAL`     |
| {func}`~is_vscode_terminal`      |  🔵  | {data}`~VSCODE_TERMINAL`      |
| {func}`~is_wasm32`               |  🌐  | {data}`~WASM32`               |
| {func}`~is_wasm64`               |  🌐  | {data}`~WASM64`               |
| {func}`~is_web_terminals`        |  ⬢   | {data}`~WEB_TERMINALS`        |
| {func}`~is_webassembly`          |  🌐  | {data}`~WEBASSEMBLY`          |
| {func}`~is_wezterm`              |  🔡  | {data}`~WEZTERM`              |
| {func}`~is_windows`              |  🪟  | {data}`~WINDOWS`              |
| {func}`~is_windows_shells`       |  ⌨️  | {data}`~WINDOWS_SHELLS`       |
| {func}`~is_windows_terminal`     |  ⊡   | {data}`~WINDOWS_TERMINAL`     |
| {func}`~is_wsl1`                 |  ⊞   | {data}`~WSL1`                 |
| {func}`~is_wsl2`                 |  ⊞   | {data}`~WSL2`                 |
| {func}`~is_x86`                  |  𝘅   | {data}`~X86`                  |
| {func}`~is_x86_64`               |  🖥️  | {data}`~X86_64`               |
| {func}`~is_xenserver`            |  Ⓧ   | {data}`~XENSERVER`            |
| {func}`~is_xonsh`                |  🐍  | {data}`~XONSH`                |
| {func}`~is_xterm`                |  𝐗   | {data}`~XTERM`                |
| {func}`~is_zellij`               |  🪵  | {data}`~ZELLIJ`               |
| {func}`~is_zsh`                  |  ℤ   | {data}`~ZSH`                  |

<!-- all-detection-function-table-end -->

## Trait detection functions

<!-- trait-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_aarch64
.. autofunction:: extra_platforms.is_aix
.. autofunction:: extra_platforms.is_alacritty
.. autofunction:: extra_platforms.is_alpine
.. autofunction:: extra_platforms.is_altlinux
.. autofunction:: extra_platforms.is_amzn
.. autofunction:: extra_platforms.is_android
.. autofunction:: extra_platforms.is_apple_terminal
.. autofunction:: extra_platforms.is_arch
.. autofunction:: extra_platforms.is_arm
.. autofunction:: extra_platforms.is_armv5tel
.. autofunction:: extra_platforms.is_armv6l
.. autofunction:: extra_platforms.is_armv7l
.. autofunction:: extra_platforms.is_armv8l
.. autofunction:: extra_platforms.is_ash
.. autofunction:: extra_platforms.is_azure_pipelines
.. autofunction:: extra_platforms.is_bamboo
.. autofunction:: extra_platforms.is_bash
.. autofunction:: extra_platforms.is_buildkite
.. autofunction:: extra_platforms.is_buildroot
.. autofunction:: extra_platforms.is_cachyos
.. autofunction:: extra_platforms.is_centos
.. autofunction:: extra_platforms.is_circle_ci
.. autofunction:: extra_platforms.is_cirrus_ci
.. autofunction:: extra_platforms.is_claude_code
.. autofunction:: extra_platforms.is_cline
.. autofunction:: extra_platforms.is_cloudlinux
.. autofunction:: extra_platforms.is_cmd
.. autofunction:: extra_platforms.is_codebuild
.. autofunction:: extra_platforms.is_contour
.. autofunction:: extra_platforms.is_csh
.. autofunction:: extra_platforms.is_cursor
.. autofunction:: extra_platforms.is_cygwin
.. autofunction:: extra_platforms.is_dash
.. autofunction:: extra_platforms.is_debian
.. autofunction:: extra_platforms.is_dragonfly_bsd
.. autofunction:: extra_platforms.is_exherbo
.. autofunction:: extra_platforms.is_fedora
.. autofunction:: extra_platforms.is_fish
.. autofunction:: extra_platforms.is_foot
.. autofunction:: extra_platforms.is_freebsd
.. autofunction:: extra_platforms.is_gentoo
.. autofunction:: extra_platforms.is_ghostty
.. autofunction:: extra_platforms.is_github_ci
.. autofunction:: extra_platforms.is_gitlab_ci
.. autofunction:: extra_platforms.is_gnome_terminal
.. autofunction:: extra_platforms.is_gnu_screen
.. autofunction:: extra_platforms.is_guix
.. autofunction:: extra_platforms.is_haiku
.. autofunction:: extra_platforms.is_heroku_ci
.. autofunction:: extra_platforms.is_hurd
.. autofunction:: extra_platforms.is_hyper
.. autofunction:: extra_platforms.is_i386
.. autofunction:: extra_platforms.is_i586
.. autofunction:: extra_platforms.is_i686
.. autofunction:: extra_platforms.is_ibm_powerkvm
.. autofunction:: extra_platforms.is_illumos
.. autofunction:: extra_platforms.is_iterm2
.. autofunction:: extra_platforms.is_kali
.. autofunction:: extra_platforms.is_kitty
.. autofunction:: extra_platforms.is_konsole
.. autofunction:: extra_platforms.is_ksh
.. autofunction:: extra_platforms.is_kvmibm
.. autofunction:: extra_platforms.is_linuxmint
.. autofunction:: extra_platforms.is_loongarch64
.. autofunction:: extra_platforms.is_macos
.. autofunction:: extra_platforms.is_mageia
.. autofunction:: extra_platforms.is_mandriva
.. autofunction:: extra_platforms.is_manjaro
.. autofunction:: extra_platforms.is_midnightbsd
.. autofunction:: extra_platforms.is_mips
.. autofunction:: extra_platforms.is_mips64
.. autofunction:: extra_platforms.is_mips64el
.. autofunction:: extra_platforms.is_mipsel
.. autofunction:: extra_platforms.is_netbsd
.. autofunction:: extra_platforms.is_nobara
.. autofunction:: extra_platforms.is_nushell
.. autofunction:: extra_platforms.is_openbsd
.. autofunction:: extra_platforms.is_opensuse
.. autofunction:: extra_platforms.is_openwrt
.. autofunction:: extra_platforms.is_oracle
.. autofunction:: extra_platforms.is_parallels
.. autofunction:: extra_platforms.is_pidora
.. autofunction:: extra_platforms.is_powershell
.. autofunction:: extra_platforms.is_ppc
.. autofunction:: extra_platforms.is_ppc64
.. autofunction:: extra_platforms.is_ppc64le
.. autofunction:: extra_platforms.is_raspbian
.. autofunction:: extra_platforms.is_rhel
.. autofunction:: extra_platforms.is_rio
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
.. autofunction:: extra_platforms.is_tabby
.. autofunction:: extra_platforms.is_tcsh
.. autofunction:: extra_platforms.is_teamcity
.. autofunction:: extra_platforms.is_tilix
.. autofunction:: extra_platforms.is_tmux
.. autofunction:: extra_platforms.is_travis_ci
.. autofunction:: extra_platforms.is_tumbleweed
.. autofunction:: extra_platforms.is_tuxedo
.. autofunction:: extra_platforms.is_ubuntu
.. autofunction:: extra_platforms.is_ultramarine
.. autofunction:: extra_platforms.is_unknown_agent
.. autofunction:: extra_platforms.is_unknown_architecture
.. autofunction:: extra_platforms.is_unknown_ci
.. autofunction:: extra_platforms.is_unknown_platform
.. autofunction:: extra_platforms.is_unknown_shell
.. autofunction:: extra_platforms.is_unknown_terminal
.. autofunction:: extra_platforms.is_vscode_terminal
.. autofunction:: extra_platforms.is_wasm32
.. autofunction:: extra_platforms.is_wasm64
.. autofunction:: extra_platforms.is_wezterm
.. autofunction:: extra_platforms.is_windows
.. autofunction:: extra_platforms.is_windows_terminal
.. autofunction:: extra_platforms.is_wsl1
.. autofunction:: extra_platforms.is_wsl2
.. autofunction:: extra_platforms.is_x86_64
.. autofunction:: extra_platforms.is_xenserver
.. autofunction:: extra_platforms.is_xonsh
.. autofunction:: extra_platforms.is_xterm
.. autofunction:: extra_platforms.is_zellij
.. autofunction:: extra_platforms.is_zsh
```

<!-- trait-detection-autofunction-end -->

## Group detection functions

Contrary to individual trait detection functions like `is_linux()` or `is_x86_64()`, group detection functions check for membership in a collection of traits.

These functions are dynamically generated for each [group](groups.md) and test whether **at least one trait** from the group matches the current system:

<!-- group-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_any_agent
.. autofunction:: extra_platforms.is_any_architecture
.. autofunction:: extra_platforms.is_any_arm
.. autofunction:: extra_platforms.is_any_ci
.. autofunction:: extra_platforms.is_any_mips
.. autofunction:: extra_platforms.is_any_platform
.. autofunction:: extra_platforms.is_any_shell
.. autofunction:: extra_platforms.is_any_sparc
.. autofunction:: extra_platforms.is_any_terminal
.. autofunction:: extra_platforms.is_any_trait
.. autofunction:: extra_platforms.is_any_windows
.. autofunction:: extra_platforms.is_arch_32_bit
.. autofunction:: extra_platforms.is_arch_64_bit
.. autofunction:: extra_platforms.is_big_endian
.. autofunction:: extra_platforms.is_bourne_shells
.. autofunction:: extra_platforms.is_bsd
.. autofunction:: extra_platforms.is_bsd_not_macos
.. autofunction:: extra_platforms.is_c_shells
.. autofunction:: extra_platforms.is_gpu_terminals
.. autofunction:: extra_platforms.is_ibm_mainframe
.. autofunction:: extra_platforms.is_linux
.. autofunction:: extra_platforms.is_linux_layers
.. autofunction:: extra_platforms.is_linux_like
.. autofunction:: extra_platforms.is_little_endian
.. autofunction:: extra_platforms.is_loongarch
.. autofunction:: extra_platforms.is_multiplexers
.. autofunction:: extra_platforms.is_native_terminals
.. autofunction:: extra_platforms.is_other_posix
.. autofunction:: extra_platforms.is_other_shells
.. autofunction:: extra_platforms.is_powerpc
.. autofunction:: extra_platforms.is_riscv
.. autofunction:: extra_platforms.is_system_v
.. autofunction:: extra_platforms.is_unix
.. autofunction:: extra_platforms.is_unix_layers
.. autofunction:: extra_platforms.is_unix_not_macos
.. autofunction:: extra_platforms.is_unknown
.. autofunction:: extra_platforms.is_web_terminals
.. autofunction:: extra_platforms.is_webassembly
.. autofunction:: extra_platforms.is_windows_shells
.. autofunction:: extra_platforms.is_x86
```

<!-- group-detection-autofunction-end -->

## Current trait functions

These functions retrieve the currently detected traits:

```{eval-rst}
.. autofunction:: extra_platforms.current_traits
.. autofunction:: extra_platforms.current_architecture
.. autofunction:: extra_platforms.current_platform
.. autofunction:: extra_platforms.current_shell
.. autofunction:: extra_platforms.current_terminal
.. autofunction:: extra_platforms.current_ci
.. autofunction:: extra_platforms.current_agent
```

## Cache management

```{eval-rst}
.. autofunction:: extra_platforms.invalidate_caches
```
