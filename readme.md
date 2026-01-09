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
'6.0.0'
```

## Examples

Get the current platform, from which you can access lots of metadata:

```pycon
>>> from extra_platforms import current_platform
>>> my_os = current_platform()
>>> my_os
Platform(id='macos', name='macOS')
>>> my_os.id
'macos'
>>> my_os.name
'macOS'
>>> my_os.icon
'🍎'
>>> my_os.info()
{
    'id': 'macos',
    'name': 'macOS',
    'icon': '🍎',
    'url': 'https://apple.com/macos/',
    'current': True,
    'distro_id': 'darwin',
    'version': '26.2',
    'version_parts': {'major': '26', 'minor': '2', 'build_number': None},
    'like': None,
    'codename': 'Tahoe',
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
>>> from extra_platforms import current_platform, BSD, UNIX, LINUX
>>> current_platform()
Platform(id='macos', name='macOS')
>>> current_platform() in BSD
True
>>> current_platform() in UNIX
True
>>> current_platform() in LINUX
False
```

Or directly use the detection functions returning a boolean that is associated with each group:

```pycon
>>> from extra_platforms import is_bsd, is_unix, is_linux
>>> is_bsd()
True
>>> is_unix()
True
>>> is_linux()
False
```

List all platforms of a family:

```pycon
>>> from extra_platforms import LINUX
>>> LINUX.members
mappingproxy({
    'altlinux': Platform(id='altlinux', name='ALT Linux'),
    'amzn': Platform(id='amzn', name='Amazon Linux'),
    'android': Platform(id='android', name='Android'),
    'arch': Platform(id='arch', name='Arch Linux'),
    'buildroot': Platform(id='buildroot', name='Buildroot'),
    'cachyos': Platform(id='cachyos', name='CachyOS'),
    'centos': Platform(id='centos', name='CentOS'),
    'cloudlinux': Platform(id='cloudlinux', name='CloudLinux OS'),
    'debian': Platform(id='debian', name='Debian'),
    'exherbo': Platform(id='exherbo', name='Exherbo Linux'),
    'fedora': Platform(id='fedora', name='Fedora'),
    'gentoo': Platform(id='gentoo', name='Gentoo Linux'),
    'guix': Platform(id='guix', name='Guix System'),
    'ibm_powerkvm': Platform(id='ibm_powerkvm', name='IBM PowerKVM'),
    'kvmibm': Platform(id='kvmibm', name='KVM for IBM z Systems'),
    'linuxmint': Platform(id='linuxmint', name='Linux Mint'),
    'mageia': Platform(id='mageia', name='Mageia'),
    'mandriva': Platform(id='mandriva', name='Mandriva Linux'),
    'nobara': Platform(id='nobara', name='Nobara'),
    'opensuse': Platform(id='opensuse', name='openSUSE'),
    'oracle': Platform(id='oracle', name='Oracle Linux'),
    'parallels': Platform(id='parallels', name='Parallels'),
    'pidora': Platform(id='pidora', name='Pidora'),
    'raspbian': Platform(id='raspbian', name='Raspbian'),
    'rhel': Platform(id='rhel', name='RedHat Enterprise Linux'),
    'rocky': Platform(id='rocky', name='Rocky Linux'),
    'scientific': Platform(id='scientific', name='Scientific Linux'),
    'slackware': Platform(id='slackware', name='Slackware'),
    'sles': Platform(id='sles', name='SUSE Linux Enterprise Server'),
    'tumbleweed': Platform(id='tumbleweed', name='openSUSE Tumbleweed'),
    'tuxedo': Platform(id='tuxedo', name='Tuxedo OS'),
    'ubuntu': Platform(id='ubuntu', name='Ubuntu'),
    'ultramarine': Platform(id='ultramarine', name='Ultramarine'),
    'unknown_linux': Platform(id='unknown_linux', name='Unknown Linux'),
    'xenserver': Platform(id='xenserver', name='XenServer'),
})
>>> LINUX.member_ids
frozenset({'centos', 'mageia', 'unknown_linux', 'ultramarine', 'tuxedo', 'arch', 'buildroot', 'android', 'exherbo', 'mandriva', 'fedora', 'slackware', 'parallels', 'xenserver', 'kvmibm', 'nobara', 'amzn', 'guix', 'debian', 'oracle', 'cachyos', 'altlinux', 'rhel', 'ibm_powerkvm', 'rocky', 'scientific', 'sles', 'linuxmint', 'tumbleweed', 'ubuntu', 'pidora', 'cloudlinux', 'gentoo', 'raspbian', 'opensuse'})
>>> print("\n".join([p.name for p in LINUX]))
ALT Linux
Amazon Linux
Android
Arch Linux
Buildroot
CachyOS
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
openSUSE Tumbleweed
Tuxedo OS
Ubuntu
Ultramarine
Unknown Linux
XenServer
```

Reduce a disparate collection of groups and platforms into a minimal descriptive set, by grouping all platforms into families:

```pycon
>>> from extra_platforms import AIX, MACOS, SOLARIS, reduce
>>> reduce([AIX, MACOS])
frozenset({
    Platform(id='macos', name='macOS'),
    Platform(id='aix', name='IBM AIX'),
})
>>> reduce([AIX, MACOS, SOLARIS])
frozenset({
    Group(id='system_v', name='AT&T System Five'),
    Platform(id='macos', name='macOS'),
})
```

## Architectures

All recognized architectures and how they're grouped:

<!-- architecture-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((🏛️ all_architectures))
        )𝘅 X86(
            (𝗶 i386)
            (𝗶 i586)
            (𝗶 i686)
            (🖥️ x86_64)
        )🌐 WEBASSEMBLY(
            (🌐 wasm32)
            (🌐 wasm64)
        )Ⅴ RISCV(
            (Ⅴ riscv32)
            (Ⅴ riscv64)
        )⚡ POWERPC(
            (⚡ ppc)
            (⚡ ppc64)
            (⚡ ppc64le)
        )🐉 LOONGARCH(
            (🐉 loongarch64)
        )🏢 IBM_MAINFRAME(
            (🏢 s390x)
        )☀️ ANY_SPARC(
            (☀️ sparc)
            (☀️ sparc64)
        )🔲 ANY_MIPS(
            (🔲 mips)
            (🔲 mips64)
            (🔲 mips64el)
            (🔲 mipsel)
        )📱 ANY_ARM(
            (📱 aarch64)
            (📱 arm)
            (📱 armv6l)
            (📱 armv7l)
            (📱 armv8l)
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
        )𝐕 SYSTEM_V(
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

> [!TIP]
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
