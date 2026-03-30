# {octicon}`tag` Traits

```{py:module} extra_platforms.trait
:no-typesetting:
:no-contents-entry:
```

```{py:currentmodule} extra_platforms
```

All aspects of a system are represented as *traits*.

There are six types of traits:

- **[Architectures](architectures.md)**: CPU architectures (e.g., x86_64, ARM64)
- **[Platforms](platforms.md)**: Operating systems (e.g., Windows, macOS, Ubuntu)
- **[Shells](shells.md)**: Command-line interpreters (e.g., Bash, Zsh, Fish)
- **[Terminals](terminals.md)**: Terminal emulators (e.g., Kitty, Alacritty, iTerm2)
- **[CI systems](ci.md)**: Continuous Integration environments (e.g., GitHub Actions, Travis CI)
- **[Agents](agents.md)**: AI coding agent environments (e.g., Claude Code, Cursor, Cline)

## Trait usage

### Current traits

You can get all currently detected traits via the {func}`~current_traits` function.

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

Other current traits can be specifically checked via their dedicated [`current_*()` functions](detection.md#current-trait-functions):

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

They all inherit from the {class}`~Trait` base class, and share a common interface.

### Current property

Each trait has a {attr}`~Trait.current` property that calls the corresponding [detection function](detection.md):

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

You can get all groups a trait belongs to via the {attr}`~Trait.groups` property:

```pycon
>>> X86_64.groups
frozenset({
   Group(id='x86', name='x86 family'),
   Group(id='all_architectures', name='All architectures'),
   Group(id='arch_64_bit', name='64-bit architectures'),
   Group(id='all_traits', name='Any architectures, platforms and CI systems')})
```

### Additional information

Each trait provides an {meth}`~Trait.info` method that returns a dictionary containing all available metadata about that trait:

```pycon
>>> from extra_platforms import AARCH64, MACOS
>>> AARCH64.info()
{'id': 'aarch64', 'name': 'ARM64 (AArch64)', 'icon': '📱', 'url': 'https://en.wikipedia.org/wiki/AArch64', 'current': True, 'machine': 'arm64', 'processor': None}
>>> MACOS.info()
{'id': 'macos', 'name': 'macOS', 'icon': '🍎', 'url': 'https://apple.com/macos/', 'current': True, 'distro_id': None, 'version': '26.2', 'version_parts': {'major': '26', 'minor': '2', 'build_number': None}, 'like': None, 'codename': 'Tahoe'}
```

The exact structure depends on the trait type.

## All traits

All recognized traits and their properties:

<!-- all-traits-table-start -->

| Icon | Symbol                        | Name                           | Detection function               | Type         |
| :--: | :---------------------------- | :----------------------------- | :------------------------------- | :----------- |
|  📱  | {data}`~AARCH64`              | ARM64 (AArch64)                | {func}`~is_aarch64`              | Architecture |
|  ➿  | {data}`~AIX`                  | IBM AIX                        | {func}`~is_aix`                  | Platform     |
|  🔳  | {data}`~ALACRITTY`            | Alacritty                      | {func}`~is_alacritty`            | Terminal     |
|  🏔️  | {data}`~ALPINE`               | Alpine Linux                   | {func}`~is_alpine`               | Platform     |
|  Δ   | {data}`~ALTLINUX`             | ALT Linux                      | {func}`~is_altlinux`             | Platform     |
|  ⤻   | {data}`~AMZN`                 | Amazon Linux                   | {func}`~is_amzn`                 | Platform     |
|  🤖  | {data}`~ANDROID`              | Android                        | {func}`~is_android`              | Platform     |
|  🍏  | {data}`~APPLE_TERMINAL`       | Apple Terminal                 | {func}`~is_apple_terminal`       | Terminal     |
|  🎗️  | {data}`~ARCH`                 | Arch Linux                     | {func}`~is_arch`                 | Platform     |
|  📱  | {data}`~ARM`                  | ARM (32-bit)                   | {func}`~is_arm`                  | Architecture |
|  📱  | {data}`~ARMV5TEL`             | ARMv5TE (little-endian)        | {func}`~is_armv5tel`             | Architecture |
|  📱  | {data}`~ARMV6L`               | ARMv6 (little-endian)          | {func}`~is_armv6l`               | Architecture |
|  📱  | {data}`~ARMV7L`               | ARMv7 (little-endian)          | {func}`~is_armv7l`               | Architecture |
|  📱  | {data}`~ARMV8L`               | ARMv8 (32-bit, little-endian)  | {func}`~is_armv8l`               | Architecture |
|  🪶  | {data}`~ASH`                  | Almquist Shell                 | {func}`~is_ash`                  | Shell        |
|  ═   | {data}`~AZURE_PIPELINES`      | Azure Pipelines                | {func}`~is_azure_pipelines`      | CI           |
|  ⟲   | {data}`~BAMBOO`               | Bamboo                         | {func}`~is_bamboo`               | CI           |
|  ＃  | {data}`~BASH`                 | Bash                           | {func}`~is_bash`                 | Shell        |
|  🪁  | {data}`~BUILDKITE`            | Buildkite                      | {func}`~is_buildkite`            | CI           |
|  ⛑️  | {data}`~BUILDROOT`            | Buildroot                      | {func}`~is_buildroot`            | Platform     |
|  ⌬   | {data}`~CACHYOS`              | CachyOS                        | {func}`~is_cachyos`              | Platform     |
|  💠  | {data}`~CENTOS`               | CentOS                         | {func}`~is_centos`               | Platform     |
|  ⪾   | {data}`~CIRCLE_CI`            | Circle CI                      | {func}`~is_circle_ci`            | CI           |
|  ≋   | {data}`~CIRRUS_CI`            | Cirrus CI                      | {func}`~is_cirrus_ci`            | CI           |
|  ✴️  | {data}`~CLAUDE_CODE`          | Claude Code                    | {func}`~is_claude_code`          | Agent        |
|  👾  | {data}`~CLINE`                | Cline                          | {func}`~is_cline`                | Agent        |
|  ꩜   | {data}`~CLOUDLINUX`           | CloudLinux OS                  | {func}`~is_cloudlinux`           | Platform     |
|  ▶   | {data}`~CMD`                  | Command Prompt                 | {func}`~is_cmd`                  | Shell        |
|  ᚙ   | {data}`~CODEBUILD`            | CodeBuild                      | {func}`~is_codebuild`            | CI           |
|  ◰   | {data}`~CONTOUR`              | Contour                        | {func}`~is_contour`              | Terminal     |
|  𝐂   | {data}`~CSH`                  | C shell                        | {func}`~is_csh`                  | Shell        |
|  ➤   | {data}`~CURSOR`               | Cursor                         | {func}`~is_cursor`               | Agent        |
|  Ͼ   | {data}`~CYGWIN`               | Cygwin                         | {func}`~is_cygwin`               | Platform     |
|  💨  | {data}`~DASH`                 | Dash                           | {func}`~is_dash`                 | Shell        |
|  🌀  | {data}`~DEBIAN`               | Debian                         | {func}`~is_debian`               | Platform     |
|  🪰  | {data}`~DRAGONFLY_BSD`        | DragonFly BSD                  | {func}`~is_dragonfly_bsd`        | Platform     |
|  🐽  | {data}`~EXHERBO`              | Exherbo Linux                  | {func}`~is_exherbo`              | Platform     |
|  🎩  | {data}`~FEDORA`               | Fedora                         | {func}`~is_fedora`               | Platform     |
|  🐟  | {data}`~FISH`                 | Fish                           | {func}`~is_fish`                 | Shell        |
|  🦶  | {data}`~FOOT`                 | foot                           | {func}`~is_foot`                 | Terminal     |
|  😈  | {data}`~FREEBSD`              | FreeBSD                        | {func}`~is_freebsd`              | Platform     |
|  🥚  | {data}`~GENERIC_LINUX`        | Generic Linux                  | {func}`~is_generic_linux`        | Platform     |
|  🗜️  | {data}`~GENTOO`               | Gentoo Linux                   | {func}`~is_gentoo`               | Platform     |
|  👻  | {data}`~GHOSTTY`              | Ghostty                        | {func}`~is_ghostty`              | Terminal     |
|  🐙  | {data}`~GITHUB_CI`            | GitHub Actions runner          | {func}`~is_github_ci`            | CI           |
|  🦊  | {data}`~GITLAB_CI`            | GitLab CI                      | {func}`~is_gitlab_ci`            | CI           |
|  𝐆   | {data}`~GNOME_TERMINAL`       | GNOME Terminal                 | {func}`~is_gnome_terminal`       | Terminal     |
|  📺  | {data}`~GNU_SCREEN`           | GNU Screen                     | {func}`~is_gnu_screen`           | Terminal     |
|  🐃  | {data}`~GUIX`                 | Guix System                    | {func}`~is_guix`                 | Platform     |
|  🍂  | {data}`~HAIKU`                | Haiku                          | {func}`~is_haiku`                | Platform     |
|  ⥁   | {data}`~HEROKU_CI`            | Heroku CI                      | {func}`~is_heroku_ci`            | CI           |
|  🦬  | {data}`~HURD`                 | GNU/Hurd                       | {func}`~is_hurd`                 | Platform     |
|  ⬡   | {data}`~HYPER`                | Hyper                          | {func}`~is_hyper`                | Terminal     |
|  𝗶   | {data}`~I386`                 | Intel 80386 (i386)             | {func}`~is_i386`                 | Architecture |
|  𝗶   | {data}`~I586`                 | Intel Pentium (i586)           | {func}`~is_i586`                 | Architecture |
|  𝗶   | {data}`~I686`                 | Intel Pentium Pro (i686)       | {func}`~is_i686`                 | Architecture |
|  🤹  | {data}`~IBM_POWERKVM`         | IBM PowerKVM                   | {func}`~is_ibm_powerkvm`         | Platform     |
|  🔥  | {data}`~ILLUMOS`              | illumos                        | {func}`~is_illumos`              | Platform     |
|  ⬛  | {data}`~ITERM2`               | iTerm2                         | {func}`~is_iterm2`               | Terminal     |
|  🔱  | {data}`~KALI`                 | Kali Linux                     | {func}`~is_kali`                 | Platform     |
|  🐱  | {data}`~KITTY`                | Kitty                          | {func}`~is_kitty`                | Terminal     |
|  💎  | {data}`~KONSOLE`              | Konsole                        | {func}`~is_konsole`              | Terminal     |
|  𝐊   | {data}`~KSH`                  | Korn shell                     | {func}`~is_ksh`                  | Shell        |
|  🤹  | {data}`~KVMIBM`               | KVM for IBM z Systems          | {func}`~is_kvmibm`               | Platform     |
|  🌿  | {data}`~LINUXMINT`            | Linux Mint                     | {func}`~is_linuxmint`            | Platform     |
|  🐉  | {data}`~LOONGARCH64`          | LoongArch (64-bit)             | {func}`~is_loongarch64`          | Architecture |
|  🍎  | {data}`~MACOS`                | macOS                          | {func}`~is_macos`                | Platform     |
|  ⍥   | {data}`~MAGEIA`               | Mageia                         | {func}`~is_mageia`               | Platform     |
|  💫  | {data}`~MANDRIVA`             | Mandriva Linux                 | {func}`~is_mandriva`             | Platform     |
|  ▲   | {data}`~MANJARO`              | Manjaro Linux                  | {func}`~is_manjaro`              | Platform     |
|  🌘  | {data}`~MIDNIGHTBSD`          | MidnightBSD                    | {func}`~is_midnightbsd`          | Platform     |
|  🔲  | {data}`~MIPS`                 | MIPS (32-bit, big-endian)      | {func}`~is_mips`                 | Architecture |
|  🔲  | {data}`~MIPS64`               | MIPS64 (big-endian)            | {func}`~is_mips64`               | Architecture |
|  🔲  | {data}`~MIPS64EL`             | MIPS64 (little-endian)         | {func}`~is_mips64el`             | Architecture |
|  🔲  | {data}`~MIPSEL`               | MIPS (32-bit, little-endian)   | {func}`~is_mipsel`               | Architecture |
|  🚩  | {data}`~NETBSD`               | NetBSD                         | {func}`~is_netbsd`               | Platform     |
|     | {data}`~NOBARA`               | Nobara                         | {func}`~is_nobara`               | Platform     |
|  𝜈   | {data}`~NUSHELL`              | Nushell                        | {func}`~is_nushell`              | Shell        |
|  🐡  | {data}`~OPENBSD`              | OpenBSD                        | {func}`~is_openbsd`              | Platform     |
|  🦎  | {data}`~OPENSUSE`             | openSUSE                       | {func}`~is_opensuse`             | Platform     |
|  📶  | {data}`~OPENWRT`              | OpenWrt                        | {func}`~is_openwrt`              | Platform     |
|  🦴  | {data}`~ORACLE`               | Oracle Linux                   | {func}`~is_oracle`               | Platform     |
|  ∥   | {data}`~PARALLELS`            | Parallels                      | {func}`~is_parallels`            | Platform     |
|  🍓  | {data}`~PIDORA`               | Pidora                         | {func}`~is_pidora`               | Platform     |
|  🔷  | {data}`~POWERSHELL`           | PowerShell                     | {func}`~is_powershell`           | Shell        |
|  ⚡  | {data}`~PPC`                  | PowerPC (32-bit)               | {func}`~is_ppc`                  | Architecture |
|  ⚡  | {data}`~PPC64`                | PowerPC 64-bit (big-endian)    | {func}`~is_ppc64`                | Architecture |
|  ⚡  | {data}`~PPC64LE`              | PowerPC 64-bit (little-endian) | {func}`~is_ppc64le`              | Architecture |
|  🍓  | {data}`~RASPBIAN`             | Raspbian                       | {func}`~is_raspbian`             | Platform     |
|  🎩  | {data}`~RHEL`                 | RedHat Enterprise Linux        | {func}`~is_rhel`                 | Platform     |
|  🏞️  | {data}`~RIO`                  | Rio                            | {func}`~is_rio`                  | Terminal     |
|  Ⅴ   | {data}`~RISCV32`              | RISC-V (32-bit)                | {func}`~is_riscv32`              | Architecture |
|  Ⅴ   | {data}`~RISCV64`              | RISC-V (64-bit)                | {func}`~is_riscv64`              | Architecture |
|  ⛰️  | {data}`~ROCKY`                | Rocky Linux                    | {func}`~is_rocky`                | Platform     |
|  🏢  | {data}`~S390X`                | IBM z/Architecture (s390x)     | {func}`~is_s390x`                | Architecture |
|  ⚛️  | {data}`~SCIENTIFIC`           | Scientific Linux               | {func}`~is_scientific`           | Platform     |
|  🚬  | {data}`~SLACKWARE`            | Slackware                      | {func}`~is_slackware`            | Platform     |
|  🦎  | {data}`~SLES`                 | SUSE Linux Enterprise Server   | {func}`~is_sles`                 | Platform     |
|  🌞  | {data}`~SOLARIS`              | Solaris                        | {func}`~is_solaris`              | Platform     |
|  ☀️  | {data}`~SPARC`                | SPARC (32-bit)                 | {func}`~is_sparc`                | Architecture |
|  ☀️  | {data}`~SPARC64`              | SPARC (64-bit)                 | {func}`~is_sparc64`              | Architecture |
|  🌅  | {data}`~SUNOS`                | SunOS                          | {func}`~is_sunos`                | Platform     |
|  🐈  | {data}`~TABBY`                | Tabby                          | {func}`~is_tabby`                | Terminal     |
|  𝐓   | {data}`~TCSH`                 | tcsh                           | {func}`~is_tcsh`                 | Shell        |
|  🏙️  | {data}`~TEAMCITY`             | TeamCity                       | {func}`~is_teamcity`             | CI           |
|  🔀  | {data}`~TILIX`                | Tilix                          | {func}`~is_tilix`                | Terminal     |
|  📟  | {data}`~TMUX`                 | tmux                           | {func}`~is_tmux`                 | Terminal     |
|  👷  | {data}`~TRAVIS_CI`            | Travis CI                      | {func}`~is_travis_ci`            | CI           |
|  ↻   | {data}`~TUMBLEWEED`           | openSUSE Tumbleweed            | {func}`~is_tumbleweed`           | Platform     |
|  🤵  | {data}`~TUXEDO`               | Tuxedo OS                      | {func}`~is_tuxedo`               | Platform     |
|  🎯  | {data}`~UBUNTU`               | Ubuntu                         | {func}`~is_ubuntu`               | Platform     |
|  🌊  | {data}`~ULTRAMARINE`          | Ultramarine                    | {func}`~is_ultramarine`          | Platform     |
|  ∅   | {data}`~VOID`                 | Void Linux                     | {func}`~is_void`                 | Platform     |
|  ❓  | {data}`~UNKNOWN_AGENT`        | Unknown agent                  | {func}`~is_unknown_agent`        | Agent        |
|  ❓  | {data}`~UNKNOWN_ARCHITECTURE` | Unknown architecture           | {func}`~is_unknown_architecture` | Architecture |
|  ❓  | {data}`~UNKNOWN_CI`           | Unknown CI                     | {func}`~is_unknown_ci`           | CI           |
|  ❓  | {data}`~UNKNOWN_PLATFORM`     | Unknown platform               | {func}`~is_unknown_platform`     | Platform     |
|  ❓  | {data}`~UNKNOWN_SHELL`        | Unknown shell                  | {func}`~is_unknown_shell`        | Shell        |
|  ❓  | {data}`~UNKNOWN_TERMINAL`     | Unknown terminal               | {func}`~is_unknown_terminal`     | Terminal     |
|  🔵  | {data}`~VSCODE_TERMINAL`      | VS Code Terminal               | {func}`~is_vscode_terminal`      | Terminal     |
|  🌐  | {data}`~WASM32`               | WebAssembly (32-bit)           | {func}`~is_wasm32`               | Architecture |
|  🌐  | {data}`~WASM64`               | WebAssembly (64-bit)           | {func}`~is_wasm64`               | Architecture |
|  🔡  | {data}`~WEZTERM`              | WezTerm                        | {func}`~is_wezterm`              | Terminal     |
|  🪟  | {data}`~WINDOWS`              | Windows                        | {func}`~is_windows`              | Platform     |
|  ⊡   | {data}`~WINDOWS_TERMINAL`     | Windows Terminal               | {func}`~is_windows_terminal`     | Terminal     |
|  ⊞   | {data}`~WSL1`                 | Windows Subsystem for Linux v1 | {func}`~is_wsl1`                 | Platform     |
|  ⊞   | {data}`~WSL2`                 | Windows Subsystem for Linux v2 | {func}`~is_wsl2`                 | Platform     |
|  🖥️  | {data}`~X86_64`               | x86-64 (AMD64)                 | {func}`~is_x86_64`               | Architecture |
|  Ⓧ   | {data}`~XENSERVER`            | XenServer                      | {func}`~is_xenserver`            | Platform     |
|  🐍  | {data}`~XONSH`                | Xonsh                          | {func}`~is_xonsh`                | Shell        |
|  𝐗   | {data}`~XTERM`                | xterm                          | {func}`~is_xterm`                | Terminal     |
|  🪵  | {data}`~ZELLIJ`               | Zellij                         | {func}`~is_zellij`               | Terminal     |
|  ℤ   | {data}`~ZSH`                  | Zsh                            | {func}`~is_zsh`                  | Shell        |

<!-- all-traits-table-end -->

## Trait implementation

```{eval-rst}
.. autoclasstree:: extra_platforms.trait
   :strict:
```

```{eval-rst}
.. autoclass:: extra_platforms.Trait
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Platform
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Architecture
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Shell
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Terminal
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.CI
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: extra_platforms.Agent
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:
```
