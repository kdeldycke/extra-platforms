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

## Groups → Platforms mapping

Relationships between groups and platforms (excluding the all-encompassing `ALL_PLATFORMS` group), represented as a Sankey diagram.

<!-- platform-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

ALL_TRAITS,aarch64,1
ALL_TRAITS,aix,1
ALL_TRAITS,altlinux,1
ALL_TRAITS,amzn,1
ALL_TRAITS,android,1
ALL_TRAITS,arch,1
ALL_TRAITS,arm,1
ALL_TRAITS,armv6l,1
ALL_TRAITS,armv7l,1
ALL_TRAITS,armv8l,1
ALL_TRAITS,azure_pipelines,1
ALL_TRAITS,bamboo,1
ALL_TRAITS,buildkite,1
ALL_TRAITS,buildroot,1
ALL_TRAITS,cachyos,1
ALL_TRAITS,centos,1
ALL_TRAITS,circle_ci,1
ALL_TRAITS,cirrus_ci,1
ALL_TRAITS,cloudlinux,1
ALL_TRAITS,codebuild,1
ALL_TRAITS,cygwin,1
ALL_TRAITS,debian,1
ALL_TRAITS,exherbo,1
ALL_TRAITS,fedora,1
ALL_TRAITS,freebsd,1
ALL_TRAITS,gentoo,1
ALL_TRAITS,github_ci,1
ALL_TRAITS,gitlab_ci,1
ALL_TRAITS,guix,1
ALL_TRAITS,heroku_ci,1
ALL_TRAITS,hurd,1
ALL_TRAITS,i386,1
ALL_TRAITS,i586,1
ALL_TRAITS,i686,1
ALL_TRAITS,ibm_powerkvm,1
ALL_TRAITS,kvmibm,1
ALL_TRAITS,linuxmint,1
ALL_TRAITS,loongarch64,1
ALL_TRAITS,macos,1
ALL_TRAITS,mageia,1
ALL_TRAITS,mandriva,1
ALL_TRAITS,midnightbsd,1
ALL_TRAITS,mips,1
ALL_TRAITS,mips64,1
ALL_TRAITS,mips64el,1
ALL_TRAITS,mipsel,1
ALL_TRAITS,netbsd,1
ALL_TRAITS,nobara,1
ALL_TRAITS,openbsd,1
ALL_TRAITS,opensuse,1
ALL_TRAITS,oracle,1
ALL_TRAITS,parallels,1
ALL_TRAITS,pidora,1
ALL_TRAITS,ppc,1
ALL_TRAITS,ppc64,1
ALL_TRAITS,ppc64le,1
ALL_TRAITS,raspbian,1
ALL_TRAITS,rhel,1
ALL_TRAITS,riscv32,1
ALL_TRAITS,riscv64,1
ALL_TRAITS,rocky,1
ALL_TRAITS,s390x,1
ALL_TRAITS,scientific,1
ALL_TRAITS,slackware,1
ALL_TRAITS,sles,1
ALL_TRAITS,solaris,1
ALL_TRAITS,sparc,1
ALL_TRAITS,sparc64,1
ALL_TRAITS,sunos,1
ALL_TRAITS,teamcity,1
ALL_TRAITS,travis_ci,1
ALL_TRAITS,tumbleweed,1
ALL_TRAITS,tuxedo,1
ALL_TRAITS,ubuntu,1
ALL_TRAITS,ultramarine,1
ALL_TRAITS,unknown_architecture,1
ALL_TRAITS,unknown_ci,1
ALL_TRAITS,unknown_linux,1
ALL_TRAITS,wasm32,1
ALL_TRAITS,wasm64,1
ALL_TRAITS,windows,1
ALL_TRAITS,wsl1,1
ALL_TRAITS,wsl2,1
ALL_TRAITS,x86_64,1
ALL_TRAITS,xenserver,1
UNIX,aix,1
UNIX,altlinux,1
UNIX,amzn,1
UNIX,android,1
UNIX,arch,1
UNIX,buildroot,1
UNIX,cachyos,1
UNIX,centos,1
UNIX,cloudlinux,1
UNIX,cygwin,1
UNIX,debian,1
UNIX,exherbo,1
UNIX,fedora,1
UNIX,freebsd,1
UNIX,gentoo,1
UNIX,guix,1
UNIX,hurd,1
UNIX,ibm_powerkvm,1
UNIX,kvmibm,1
UNIX,linuxmint,1
UNIX,macos,1
UNIX,mageia,1
UNIX,mandriva,1
UNIX,midnightbsd,1
UNIX,netbsd,1
UNIX,nobara,1
UNIX,openbsd,1
UNIX,opensuse,1
UNIX,oracle,1
UNIX,parallels,1
UNIX,pidora,1
UNIX,raspbian,1
UNIX,rhel,1
UNIX,rocky,1
UNIX,scientific,1
UNIX,slackware,1
UNIX,sles,1
UNIX,solaris,1
UNIX,sunos,1
UNIX,tumbleweed,1
UNIX,tuxedo,1
UNIX,ubuntu,1
UNIX,ultramarine,1
UNIX,unknown_linux,1
UNIX,wsl1,1
UNIX,wsl2,1
UNIX,xenserver,1
UNIX_WITHOUT_MACOS,aix,1
UNIX_WITHOUT_MACOS,altlinux,1
UNIX_WITHOUT_MACOS,amzn,1
UNIX_WITHOUT_MACOS,android,1
UNIX_WITHOUT_MACOS,arch,1
UNIX_WITHOUT_MACOS,buildroot,1
UNIX_WITHOUT_MACOS,cachyos,1
UNIX_WITHOUT_MACOS,centos,1
UNIX_WITHOUT_MACOS,cloudlinux,1
UNIX_WITHOUT_MACOS,cygwin,1
UNIX_WITHOUT_MACOS,debian,1
UNIX_WITHOUT_MACOS,exherbo,1
UNIX_WITHOUT_MACOS,fedora,1
UNIX_WITHOUT_MACOS,freebsd,1
UNIX_WITHOUT_MACOS,gentoo,1
UNIX_WITHOUT_MACOS,guix,1
UNIX_WITHOUT_MACOS,hurd,1
UNIX_WITHOUT_MACOS,ibm_powerkvm,1
UNIX_WITHOUT_MACOS,kvmibm,1
UNIX_WITHOUT_MACOS,linuxmint,1
UNIX_WITHOUT_MACOS,mageia,1
UNIX_WITHOUT_MACOS,mandriva,1
UNIX_WITHOUT_MACOS,midnightbsd,1
UNIX_WITHOUT_MACOS,netbsd,1
UNIX_WITHOUT_MACOS,nobara,1
UNIX_WITHOUT_MACOS,openbsd,1
UNIX_WITHOUT_MACOS,opensuse,1
UNIX_WITHOUT_MACOS,oracle,1
UNIX_WITHOUT_MACOS,parallels,1
UNIX_WITHOUT_MACOS,pidora,1
UNIX_WITHOUT_MACOS,raspbian,1
UNIX_WITHOUT_MACOS,rhel,1
UNIX_WITHOUT_MACOS,rocky,1
UNIX_WITHOUT_MACOS,scientific,1
UNIX_WITHOUT_MACOS,slackware,1
UNIX_WITHOUT_MACOS,sles,1
UNIX_WITHOUT_MACOS,solaris,1
UNIX_WITHOUT_MACOS,sunos,1
UNIX_WITHOUT_MACOS,tumbleweed,1
UNIX_WITHOUT_MACOS,tuxedo,1
UNIX_WITHOUT_MACOS,ubuntu,1
UNIX_WITHOUT_MACOS,ultramarine,1
UNIX_WITHOUT_MACOS,unknown_linux,1
UNIX_WITHOUT_MACOS,wsl1,1
UNIX_WITHOUT_MACOS,wsl2,1
UNIX_WITHOUT_MACOS,xenserver,1
LINUX_LIKE,altlinux,1
LINUX_LIKE,amzn,1
LINUX_LIKE,android,1
LINUX_LIKE,arch,1
LINUX_LIKE,buildroot,1
LINUX_LIKE,cachyos,1
LINUX_LIKE,centos,1
LINUX_LIKE,cloudlinux,1
LINUX_LIKE,debian,1
LINUX_LIKE,exherbo,1
LINUX_LIKE,fedora,1
LINUX_LIKE,gentoo,1
LINUX_LIKE,guix,1
LINUX_LIKE,ibm_powerkvm,1
LINUX_LIKE,kvmibm,1
LINUX_LIKE,linuxmint,1
LINUX_LIKE,mageia,1
LINUX_LIKE,mandriva,1
LINUX_LIKE,nobara,1
LINUX_LIKE,opensuse,1
LINUX_LIKE,oracle,1
LINUX_LIKE,parallels,1
LINUX_LIKE,pidora,1
LINUX_LIKE,raspbian,1
LINUX_LIKE,rhel,1
LINUX_LIKE,rocky,1
LINUX_LIKE,scientific,1
LINUX_LIKE,slackware,1
LINUX_LIKE,sles,1
LINUX_LIKE,tumbleweed,1
LINUX_LIKE,tuxedo,1
LINUX_LIKE,ubuntu,1
LINUX_LIKE,ultramarine,1
LINUX_LIKE,unknown_linux,1
LINUX_LIKE,wsl1,1
LINUX_LIKE,wsl2,1
LINUX_LIKE,xenserver,1
LINUX,altlinux,1
LINUX,amzn,1
LINUX,android,1
LINUX,arch,1
LINUX,buildroot,1
LINUX,cachyos,1
LINUX,centos,1
LINUX,cloudlinux,1
LINUX,debian,1
LINUX,exherbo,1
LINUX,fedora,1
LINUX,gentoo,1
LINUX,guix,1
LINUX,ibm_powerkvm,1
LINUX,kvmibm,1
LINUX,linuxmint,1
LINUX,mageia,1
LINUX,mandriva,1
LINUX,nobara,1
LINUX,opensuse,1
LINUX,oracle,1
LINUX,parallels,1
LINUX,pidora,1
LINUX,raspbian,1
LINUX,rhel,1
LINUX,rocky,1
LINUX,scientific,1
LINUX,slackware,1
LINUX,sles,1
LINUX,tumbleweed,1
LINUX,tuxedo,1
LINUX,ubuntu,1
LINUX,ultramarine,1
LINUX,unknown_linux,1
LINUX,xenserver,1
ALL_ARCHITECTURES,aarch64,1
ALL_ARCHITECTURES,arm,1
ALL_ARCHITECTURES,armv6l,1
ALL_ARCHITECTURES,armv7l,1
ALL_ARCHITECTURES,armv8l,1
ALL_ARCHITECTURES,i386,1
ALL_ARCHITECTURES,i586,1
ALL_ARCHITECTURES,i686,1
ALL_ARCHITECTURES,loongarch64,1
ALL_ARCHITECTURES,mips,1
ALL_ARCHITECTURES,mips64,1
ALL_ARCHITECTURES,mips64el,1
ALL_ARCHITECTURES,mipsel,1
ALL_ARCHITECTURES,ppc,1
ALL_ARCHITECTURES,ppc64,1
ALL_ARCHITECTURES,ppc64le,1
ALL_ARCHITECTURES,riscv32,1
ALL_ARCHITECTURES,riscv64,1
ALL_ARCHITECTURES,s390x,1
ALL_ARCHITECTURES,sparc,1
ALL_ARCHITECTURES,sparc64,1
ALL_ARCHITECTURES,unknown_architecture,1
ALL_ARCHITECTURES,wasm32,1
ALL_ARCHITECTURES,wasm64,1
ALL_ARCHITECTURES,x86_64,1
ALL_CI,azure_pipelines,1
ALL_CI,bamboo,1
ALL_CI,buildkite,1
ALL_CI,circle_ci,1
ALL_CI,cirrus_ci,1
ALL_CI,codebuild,1
ALL_CI,github_ci,1
ALL_CI,gitlab_ci,1
ALL_CI,heroku_ci,1
ALL_CI,teamcity,1
ALL_CI,travis_ci,1
ALL_CI,unknown_ci,1
BSD,freebsd,1
BSD,macos,1
BSD,midnightbsd,1
BSD,netbsd,1
BSD,openbsd,1
BSD,sunos,1
BSD_WITHOUT_MACOS,freebsd,1
BSD_WITHOUT_MACOS,midnightbsd,1
BSD_WITHOUT_MACOS,netbsd,1
BSD_WITHOUT_MACOS,openbsd,1
BSD_WITHOUT_MACOS,sunos,1
SYSTEM_V,aix,1
SYSTEM_V,solaris,1
LINUX_LAYERS,wsl1,1
LINUX_LAYERS,wsl2,1
UNIX_LAYERS,cygwin,1
OTHER_UNIX,hurd,1
ANY_WINDOWS,windows,1
```

<!-- platform-sankey-end -->

## OS families

Each platform is assigned to a group of non-overlpaping families:

<!-- platform-hierarchy-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((Extra Platforms))
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

<!-- platform-hierarchy-end -->

## Used in

Check these projects to get real-life examples of `extra-platforms` usage:

- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/meta-package-manager?label=%E2%AD%90&style=flat-square) [Meta Package Manager](https://github.com/kdeldycke/meta-package-manager) - A unifying CLI for multiple package managers.
- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/mail-deduplicate?label=%E2%AD%90&style=flat-square) [Mail Deduplicate](https://github.com/kdeldycke/mail-deduplicate) - Deduplicate emails in mail files and folders.
- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/click-extra?label=%E2%AD%90&style=flat-square) [Click Extra](https://github.com/kdeldycke/click-extra) - Drop-in replacement for Click to make user-friendly and colorful CLI.

Feel free to send a PR to add your project in this list if you are relying on Extra Platforms in any way.

## Development

[Development guidelines](https://github.com/kdeldycke/click-extra?tab=readme-ov-file#development) are the same as [parent project Click Extra](https://github.com/kdeldycke/click-extra), from which `extra-platforms` originated.
