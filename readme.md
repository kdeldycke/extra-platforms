# Extra Platforms

[![Last release](https://img.shields.io/pypi/v/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Python versions](https://img.shields.io/pypi/pyversions/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Downloads](https://static.pepy.tech/badge/extra_platforms/month)](https://pepy.tech/project/extra_platforms)
[![Unittests status](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml?query=branch%3Amain)
[![Coverage status](https://codecov.io/gh/kdeldycke/extra-platforms/branch/main/graph/badge.svg)](https://app.codecov.io/gh/kdeldycke/extra-platforms)
[![Documentation status](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml?query=branch%3Amain)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13341712.svg)](https://doi.org/10.5281/zenodo.13341712)

## What is Extra Platforms?

- Inventory of all known architectures, platforms and CI systems
- Detect the current architecture platform, at the distribution level
- Platform metadata (version, codename, etc.)
- Group platforms and architectures into families
- Manage collection of platforms and groups
- Associate each platform and group to an emoji symbol
- Conditional markers decorators for `pytest`: `@skip_<id>`/`@unless_<id>` for each platform and group (`@skip_android`, `@skip_any_windows`, `@skip_github_ci`, …)
- Fix [`distro#177` issue (support for Windows and Mac OS)](https://github.com/python-distro/distro/issues/177)

## Quick start

If you want to play with this library without contaminating your system, you can [use `uv`](https://docs.astral.sh/uv/guides/tools/#running-tools):

```shell-session
$ uvx --with extra-platforms python
```

```pycon
>>> import extra_platforms
>>> extra_platforms.__version__
'3.2.3'
```

## Examples

Get the current platform, from which you can access lots of metadata:

```pycon
>>> from extra_platforms import current_os
>>> my_os = current_os()
>>> my_os
Platform(id='macos', name='macOS', current=True)
>>> my_os.id
'macos'
>>> my_os.name
'macOS'
>>> my_os.icon
'🍎'
>>> my_os.info()
{
    "id": "macos",
    "name": "macOS",
    "icon": "🍎",
    "current": True,
    "distro_id": "darwin",
    "version": "23.6.0",
    "version_parts": {"major": "23", "minor": "6", "build_number": "0"},
    "like": None,
    "codename": None,
}
```

Check if a platform is a specific system:

```pycon
>>> from extra_platforms import is_gentoo
>>> is_gentoo()
False
```

Use groups to check if the current platform is part of a specific family:

```pycon
>>> from extra_platforms import UNIX, current_os
>>> current_os() in UNIX
False
```

Or directly use the boolean variables available for each family:

```pycon
>>> from extra_platforms import is_unix
>>> is_unix()
False
```

List all platforms of a family:

```pycon
>>> from extra_platforms import LINUX
>>> LINUX
Group(id='linux', name='Any Linux', platform_ids=frozenset({'ibm_powerkvm', 'rocky', 'debian', 'tuxedo', 'ubuntu', 'mageia', 'xenserver', 'opensuse', 'nobara', 'buildroot', 'rhel', 'parallels', 'pidora', 'sles', 'amzn', 'scientific', 'linuxmint', 'centos', 'android', 'gentoo', 'raspbian', 'unknown_linux', 'mandriva', 'exherbo', 'cloudlinux', 'fedora', 'guix', 'arch', 'altlinux', 'slackware', 'oracle', 'kvmibm'}))

>>> print("\n".join([p.name for p in LINUX]))
ALT Linux
Amazon Linux
Android
Arch Linux
Buildroot
CentOS
CloudLinux OS
Debian
Exherbo Linux
Fedora
Gentoo Linux
Guix System
IBM PowerKVM
KVM for IBM z Systems
Linux Mint
Mageia
Mandriva Linux
Nobara
openSUSE
Oracle Linux
Parallels
Pidora
Raspbian
RedHat Enterprise Linux
Rocky Linux
Scientific Linux
Slackware
SUSE Linux Enterprise Server
Tuxedo OS
Ubuntu
Unknown Linux
XenServer
```

Reduce a disparate collection of groups and platforms into a minimal descriptive set, by grouping all platforms into families:

```pycon
>>> from extra_platforms import AIX, MACOS, SOLARIS, reduce
>>> reduce([AIX, MACOS])
{
    Platform(id='aix', name='IBM AIX', current=False),
    Platform(id='macos', name='macOS', current=True),
}
>>> reduce([AIX, MACOS, SOLARIS])
{
    Group(id='system_v', name='Any Unix derived from AT&T System Five', platform_ids=frozenset({'aix', 'solaris'})),
    Platform(id='macos', name='macOS', current=True),
}
```

## Architectures

All recognized architectures:

<!-- architecture-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((🏛️ all_architectures))
        )🏛️ ALL_ARCHITECTURES(
            (🔋 aarch64)
            (📱 arm)
            (📱 armv6l)
            (📱 armv7l)
            (📱 armv8l)
            (🔲 i386)
            (🔲 i586)
            (🔲 i686)
            (🐉 loongarch64)
            (🔧 mips)
            (🔧 mips64)
            (🔧 mips64el)
            (🔧 mipsel)
            (⚡ ppc)
            (⚡ ppc64)
            (⚡ ppc64le)
            (🌱 riscv32)
            (🌱 riscv64)
            (🏢 s390x)
            (☀️ sparc)
            (☀️ sparc64)
            (❓ unknown_architecture)
            (🌐 wasm32)
            (🌐 wasm64)
            (💻 x86_64)
```

<!-- architecture-mindmap-end -->

## Platforms

All recognized platforms and how they're grouped:

<!-- platform-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((⚙️ all_platforms))
        )≛ UNIX_LAYERS(
            (Ͼ cygwin)
        )Ⅴ SYSTEM_V(
            (➿ aix)
            (🌞 solaris)
        )⊎ OTHER_UNIX(
            (🐃 hurd)
        )≚ LINUX_LAYERS(
            (⊞ wsl1)
            (⊞ wsl2)
        )🐧 LINUX(
            (🐧 altlinux)
            (⤻ amzn)
            (🤖 android)
            (🎗️ arch)
            (⛑️ buildroot)
            (⌬ cachyos)
            (💠 centos)
            (꩜ cloudlinux)
            (🌀 debian)
            (🐽 exherbo)
            (🎩 fedora)
            (🗜️ gentoo)
            (🐃 guix)
            (🤹 ibm_powerkvm)
            (🤹 kvmibm)
            (🌿 linuxmint)
            (⍥ mageia)
            (💫 mandriva)
            ( nobara)
            (🦎 opensuse)
            (🦴 oracle)
            (∥ parallels)
            (🍓 pidora)
            (🍓 raspbian)
            (🎩 rhel)
            (⛰️ rocky)
            (⚛️ scientific)
            (🚬 slackware)
            (🦎 sles)
            (↻ tumbleweed)
            (🤵 tuxedo)
            (🎯 ubuntu)
            (🌊 ultramarine)
            (🐧 unknown_linux)
            (Ⓧ xenserver)
        )🅱️+ BSD(
            (😈 freebsd)
            (🍎 macos)
            (🌘 midnightbsd)
            (🚩 netbsd)
            (🐡 openbsd)
            (☀️ sunos)
        )🪟 ANY_WINDOWS(
            (🪟 windows)
```

<!-- platform-mindmap-end -->

> [!NOTE]
> More groups exist beyond those shown in the diagram, and more utilities are available for each platform. See the [platform documentation](https://kdeldycke.github.io/extra-platforms/platforms.html#groups-of-platforms) for details.

## CI systems

All recognized CI systems:

<!-- ci-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((♺ all_ci))
        )♺ ALL_CI(
            (═ azure_pipelines)
            (⟲ bamboo)
            (🪁 buildkite)
            (⪾ circle_ci)
            (≋ cirrus_ci)
            (ᚙ codebuild)
            (🐙 github_ci)
            (🦊 gitlab_ci)
            (⥁ heroku_ci)
            (🏙️ teamcity)
            (👷 travis_ci)
            (♲ unknown_ci)
```

<!-- ci-mindmap-end -->

## Used in

Check these projects to get real-life examples of `extra-platforms` usage:

- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/meta-package-manager?label=%E2%AD%90&style=flat-square) [Meta Package Manager](https://github.com/kdeldycke/meta-package-manager) - A unifying CLI for multiple package managers.
- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/mail-deduplicate?label=%E2%AD%90&style=flat-square) [Mail Deduplicate](https://github.com/kdeldycke/mail-deduplicate) - Deduplicate emails in mail files and folders.
- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/click-extra?label=%E2%AD%90&style=flat-square) [Click Extra](https://github.com/kdeldycke/click-extra) - Drop-in replacement for Click to make user-friendly and colorful CLI.

Feel free to send a PR to add your project in this list if you are relying on Extra Platforms in any way.

## Development

[Development guidelines](https://github.com/kdeldycke/click-extra?tab=readme-ov-file#development) are the same as [parent project Click Extra](https://github.com/kdeldycke/click-extra), from which `extra-platforms` originated.
