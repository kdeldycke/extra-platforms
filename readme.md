# Extra Platforms

[![Last release](https://img.shields.io/pypi/v/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Python versions](https://img.shields.io/pypi/pyversions/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Downloads](https://static.pepy.tech/badge/extra_platforms/month)](https://pepy.tech/project/extra_platforms)
[![Unittests status](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml?query=branch%3Amain)
[![Coverage status](https://codecov.io/gh/kdeldycke/extra-platforms/branch/main/graph/badge.svg)](https://app.codecov.io/gh/kdeldycke/extra-platforms)
[![Documentation status](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml?query=branch%3Amain)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13341712.svg)](https://doi.org/10.5281/zenodo.13341712)

## What is Extra Platforms?

- Provides a list of all known platforms
- Detect the current platform, at the distribution level
- Gather current platform metadata (version, codename, etc.)
- Group platforms into families
- Manage collection of platforms and groups
- Associate each platform and group to an emoji symbol
- New conditional markers for `pytest`:
  - `@skip_linux`, `@skip_macos` and `@skip_windows`
  - `@unless_linux`, `@unless_macos` and `@unless_windows`

## Examples

Get the current platform ID and name:

```pycon
>>> from extra_platforms import CURRENT_OS_ID, CURRENT_OS_LABEL

>>> CURRENT_OS_ID
'macos'

>>> CURRENT_OS_LABEL
'macOS'
```

Get the current platform object, from which you can access lots of metadata:

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
>>> from extra_platforms import is_windows

>>> is_windows()
False
```

Use groups to check if the current platform is part of a specific family:

```pycon
>>> from extra_platforms import ALL_LINUX, current_os

>>> current_os() in ALL_LINUX
False
```

List all platforms of a family:

```pycon
>>> from extra_platforms import ALL_LINUX

>>> ALL_LINUX
Group(id='all_linux', name='Any Linux', platform_ids=frozenset({'ibm_powerkvm', 'rocky', 'debian', 'ubuntu', 'mageia', 'xenserver', 'opensuse', 'buildroot', 'rhel', 'parallels', 'pidora', 'sles', 'amzn', 'scientific', 'linuxmint', 'centos', 'android', 'gentoo', 'raspbian', 'unknown_linux', 'mandriva', 'exherbo', 'cloudlinux', 'fedora', 'guix', 'arch', 'altlinux', 'slackware', 'oracle', 'kvmibm'}))

>>> print("\n".join([p.name for p in ALL_LINUX]))
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

## Group → platforms mapping

Relationships between groups and platforms:

<!-- platform-sankey-start -->

```mermaid
---
config:
  sankey:
    showValues: false
---
sankey-beta

all_platforms,aix,1
all_platforms,altlinux,1
all_platforms,amzn,1
all_platforms,android,1
all_platforms,arch,1
all_platforms,buildroot,1
all_platforms,centos,1
all_platforms,cloudlinux,1
all_platforms,cygwin,1
all_platforms,debian,1
all_platforms,exherbo,1
all_platforms,fedora,1
all_platforms,freebsd,1
all_platforms,gentoo,1
all_platforms,guix,1
all_platforms,hurd,1
all_platforms,ibm_powerkvm,1
all_platforms,kvmibm,1
all_platforms,linuxmint,1
all_platforms,macos,1
all_platforms,mageia,1
all_platforms,mandriva,1
all_platforms,midnightbsd,1
all_platforms,netbsd,1
all_platforms,openbsd,1
all_platforms,opensuse,1
all_platforms,oracle,1
all_platforms,parallels,1
all_platforms,pidora,1
all_platforms,raspbian,1
all_platforms,rhel,1
all_platforms,rocky,1
all_platforms,scientific,1
all_platforms,slackware,1
all_platforms,sles,1
all_platforms,solaris,1
all_platforms,sunos,1
all_platforms,ubuntu,1
all_platforms,unknown_linux,1
all_platforms,windows,1
all_platforms,wsl1,1
all_platforms,wsl2,1
all_platforms,xenserver,1
unix,aix,1
unix,altlinux,1
unix,amzn,1
unix,android,1
unix,arch,1
unix,buildroot,1
unix,centos,1
unix,cloudlinux,1
unix,cygwin,1
unix,debian,1
unix,exherbo,1
unix,fedora,1
unix,freebsd,1
unix,gentoo,1
unix,guix,1
unix,hurd,1
unix,ibm_powerkvm,1
unix,kvmibm,1
unix,linuxmint,1
unix,macos,1
unix,mageia,1
unix,mandriva,1
unix,midnightbsd,1
unix,netbsd,1
unix,openbsd,1
unix,opensuse,1
unix,oracle,1
unix,parallels,1
unix,pidora,1
unix,raspbian,1
unix,rhel,1
unix,rocky,1
unix,scientific,1
unix,slackware,1
unix,sles,1
unix,solaris,1
unix,sunos,1
unix,ubuntu,1
unix,unknown_linux,1
unix,wsl1,1
unix,wsl2,1
unix,xenserver,1
unix_without_macos,aix,1
unix_without_macos,altlinux,1
unix_without_macos,amzn,1
unix_without_macos,android,1
unix_without_macos,arch,1
unix_without_macos,buildroot,1
unix_without_macos,centos,1
unix_without_macos,cloudlinux,1
unix_without_macos,cygwin,1
unix_without_macos,debian,1
unix_without_macos,exherbo,1
unix_without_macos,fedora,1
unix_without_macos,freebsd,1
unix_without_macos,gentoo,1
unix_without_macos,guix,1
unix_without_macos,hurd,1
unix_without_macos,ibm_powerkvm,1
unix_without_macos,kvmibm,1
unix_without_macos,linuxmint,1
unix_without_macos,mageia,1
unix_without_macos,mandriva,1
unix_without_macos,midnightbsd,1
unix_without_macos,netbsd,1
unix_without_macos,openbsd,1
unix_without_macos,opensuse,1
unix_without_macos,oracle,1
unix_without_macos,parallels,1
unix_without_macos,pidora,1
unix_without_macos,raspbian,1
unix_without_macos,rhel,1
unix_without_macos,rocky,1
unix_without_macos,scientific,1
unix_without_macos,slackware,1
unix_without_macos,sles,1
unix_without_macos,solaris,1
unix_without_macos,sunos,1
unix_without_macos,ubuntu,1
unix_without_macos,unknown_linux,1
unix_without_macos,wsl1,1
unix_without_macos,wsl2,1
unix_without_macos,xenserver,1
linux_like,altlinux,1
linux_like,amzn,1
linux_like,android,1
linux_like,arch,1
linux_like,buildroot,1
linux_like,centos,1
linux_like,cloudlinux,1
linux_like,debian,1
linux_like,exherbo,1
linux_like,fedora,1
linux_like,gentoo,1
linux_like,guix,1
linux_like,ibm_powerkvm,1
linux_like,kvmibm,1
linux_like,linuxmint,1
linux_like,mageia,1
linux_like,mandriva,1
linux_like,opensuse,1
linux_like,oracle,1
linux_like,parallels,1
linux_like,pidora,1
linux_like,raspbian,1
linux_like,rhel,1
linux_like,rocky,1
linux_like,scientific,1
linux_like,slackware,1
linux_like,sles,1
linux_like,ubuntu,1
linux_like,unknown_linux,1
linux_like,wsl1,1
linux_like,wsl2,1
linux_like,xenserver,1
all_linux,altlinux,1
all_linux,amzn,1
all_linux,android,1
all_linux,arch,1
all_linux,buildroot,1
all_linux,centos,1
all_linux,cloudlinux,1
all_linux,debian,1
all_linux,exherbo,1
all_linux,fedora,1
all_linux,gentoo,1
all_linux,guix,1
all_linux,ibm_powerkvm,1
all_linux,kvmibm,1
all_linux,linuxmint,1
all_linux,mageia,1
all_linux,mandriva,1
all_linux,opensuse,1
all_linux,oracle,1
all_linux,parallels,1
all_linux,pidora,1
all_linux,raspbian,1
all_linux,rhel,1
all_linux,rocky,1
all_linux,scientific,1
all_linux,slackware,1
all_linux,sles,1
all_linux,ubuntu,1
all_linux,unknown_linux,1
all_linux,xenserver,1
bsd,freebsd,1
bsd,macos,1
bsd,midnightbsd,1
bsd,netbsd,1
bsd,openbsd,1
bsd,sunos,1
bsd_without_macos,freebsd,1
bsd_without_macos,midnightbsd,1
bsd_without_macos,netbsd,1
bsd_without_macos,openbsd,1
bsd_without_macos,sunos,1
system_v,aix,1
system_v,solaris,1
linux_layers,wsl1,1
linux_layers,wsl2,1
unix_layers,cygwin,1
other_unix,hurd,1
all_windows,windows,1
```

<!-- platform-sankey-end -->

## OS families

Each platform is assigned to a group of non-overlpaping families:

<!-- NON_OVERLAPPING_GROUPS-graph-start -->

#### `extra_platforms.NON_OVERLAPPING_GROUPS` - Non-overlapping groups.

```mermaid
flowchart
    subgraph "<code>extra_platforms.ALL_LINUX</code><br/>🐧 <em>Any Linux</em>"
        all_linux_altlinux(<code>altlinux</code><br/>❓ <em>ALT Linux</em>)
        all_linux_amzn(<code>amzn</code><br/>🙂 <em>Amazon Linux</em>)
        all_linux_android(<code>android</code><br/>🤖 <em>Android</em>)
        all_linux_arch(<code>arch</code><br/>🎗️ <em>Arch Linux</em>)
        all_linux_buildroot(<code>buildroot</code><br/>❓ <em>Buildroot</em>)
        all_linux_centos(<code>centos</code><br/>💠 <em>CentOS</em>)
        all_linux_cloudlinux(<code>cloudlinux</code><br/>❓ <em>CloudLinux OS</em>)
        all_linux_debian(<code>debian</code><br/>🌀 <em>Debian</em>)
        all_linux_exherbo(<code>exherbo</code><br/>❓ <em>Exherbo Linux</em>)
        all_linux_fedora(<code>fedora</code><br/>🎩 <em>Fedora</em>)
        all_linux_gentoo(<code>gentoo</code><br/>🗜️ <em>Gentoo Linux</em>)
        all_linux_guix(<code>guix</code><br/>❓ <em>Guix System</em>)
        all_linux_ibm_powerkvm(<code>ibm_powerkvm</code><br/>❓ <em>IBM PowerKVM</em>)
        all_linux_kvmibm(<code>kvmibm</code><br/>❓ <em>KVM for IBM z Systems</em>)
        all_linux_linuxmint(<code>linuxmint</code><br/>🌿 <em>Linux Mint</em>)
        all_linux_mageia(<code>mageia</code><br/>❓ <em>Mageia</em>)
        all_linux_mandriva(<code>mandriva</code><br/>❓ <em>Mandriva Linux</em>)
        all_linux_opensuse(<code>opensuse</code><br/>🦎 <em>openSUSE</em>)
        all_linux_oracle(<code>oracle</code><br/>🦴 <em>Oracle Linux</em>)
        all_linux_parallels(<code>parallels</code><br/>❓ <em>Parallels</em>)
        all_linux_pidora(<code>pidora</code><br/>❓ <em>Pidora</em>)
        all_linux_raspbian(<code>raspbian</code><br/>🍓 <em>Raspbian</em>)
        all_linux_rhel(<code>rhel</code><br/>🎩 <em>RedHat Enterprise Linux</em>)
        all_linux_rocky(<code>rocky</code><br/>💠 <em>Rocky Linux</em>)
        all_linux_scientific(<code>scientific</code><br/>❓ <em>Scientific Linux</em>)
        all_linux_slackware(<code>slackware</code><br/>❓ <em>Slackware</em>)
        all_linux_sles(<code>sles</code><br/>🦎 <em>SUSE Linux Enterprise Server</em>)
        all_linux_ubuntu(<code>ubuntu</code><br/>🎯 <em>Ubuntu</em>)
        all_linux_unknown_linux(<code>unknown_linux</code><br/>🐧 <em>Unknown Linux</em>)
        all_linux_xenserver(<code>xenserver</code><br/>❓ <em>XenServer</em>)
    end
    subgraph "<code>extra_platforms.ALL_WINDOWS</code><br/>🪟 <em>Any Windows</em>"
        all_windows_windows(<code>windows</code><br/>🪟 <em>Windows</em>)
    end
    subgraph "<code>extra_platforms.BSD</code><br/>🅱️ <em>Any BSD</em>"
        bsd_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        bsd_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        bsd_midnightbsd(<code>midnightbsd</code><br/>🌘 <em>MidnightBSD</em>)
        bsd_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        bsd_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        bsd_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
    end
    subgraph "<code>extra_platforms.LINUX_LAYERS</code><br/>≚ <em>Any Linux compatibility layers</em>"
        linux_layers_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        linux_layers_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
    end
    subgraph "<code>extra_platforms.OTHER_UNIX</code><br/>⊎ <em>Any other Unix</em>"
        other_unix_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
    end
    subgraph "<code>extra_platforms.SYSTEM_V</code><br/>Ⅴ <em>Any Unix derived from AT&amp;T System Five</em>"
        system_v_aix(<code>aix</code><br/>➿ <em>IBM AIX</em>)
        system_v_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
    end
    subgraph "<code>extra_platforms.UNIX_LAYERS</code><br/>≛ <em>Any Unix compatibility layers</em>"
        unix_layers_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
    end
```

<!-- NON_OVERLAPPING_GROUPS-graph-end -->

## Other groups

Other groups are available for convenience, but these overlaps:

<!-- EXTRA_GROUPS-graph-start -->

#### `extra_platforms.EXTRA_GROUPS` - Overlapping groups, defined for convenience.

```mermaid
flowchart
    subgraph "<code>extra_platforms.ALL_PLATFORMS</code><br/>🖥️ <em>Any platforms</em>"
        all_platforms_aix(<code>aix</code><br/>➿ <em>IBM AIX</em>)
        all_platforms_altlinux(<code>altlinux</code><br/>❓ <em>ALT Linux</em>)
        all_platforms_amzn(<code>amzn</code><br/>🙂 <em>Amazon Linux</em>)
        all_platforms_android(<code>android</code><br/>🤖 <em>Android</em>)
        all_platforms_arch(<code>arch</code><br/>🎗️ <em>Arch Linux</em>)
        all_platforms_buildroot(<code>buildroot</code><br/>❓ <em>Buildroot</em>)
        all_platforms_centos(<code>centos</code><br/>💠 <em>CentOS</em>)
        all_platforms_cloudlinux(<code>cloudlinux</code><br/>❓ <em>CloudLinux OS</em>)
        all_platforms_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        all_platforms_debian(<code>debian</code><br/>🌀 <em>Debian</em>)
        all_platforms_exherbo(<code>exherbo</code><br/>❓ <em>Exherbo Linux</em>)
        all_platforms_fedora(<code>fedora</code><br/>🎩 <em>Fedora</em>)
        all_platforms_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        all_platforms_gentoo(<code>gentoo</code><br/>🗜️ <em>Gentoo Linux</em>)
        all_platforms_guix(<code>guix</code><br/>❓ <em>Guix System</em>)
        all_platforms_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        all_platforms_ibm_powerkvm(<code>ibm_powerkvm</code><br/>❓ <em>IBM PowerKVM</em>)
        all_platforms_kvmibm(<code>kvmibm</code><br/>❓ <em>KVM for IBM z Systems</em>)
        all_platforms_linuxmint(<code>linuxmint</code><br/>🌿 <em>Linux Mint</em>)
        all_platforms_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        all_platforms_mageia(<code>mageia</code><br/>❓ <em>Mageia</em>)
        all_platforms_mandriva(<code>mandriva</code><br/>❓ <em>Mandriva Linux</em>)
        all_platforms_midnightbsd(<code>midnightbsd</code><br/>🌘 <em>MidnightBSD</em>)
        all_platforms_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        all_platforms_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        all_platforms_opensuse(<code>opensuse</code><br/>🦎 <em>openSUSE</em>)
        all_platforms_oracle(<code>oracle</code><br/>🦴 <em>Oracle Linux</em>)
        all_platforms_parallels(<code>parallels</code><br/>❓ <em>Parallels</em>)
        all_platforms_pidora(<code>pidora</code><br/>❓ <em>Pidora</em>)
        all_platforms_raspbian(<code>raspbian</code><br/>🍓 <em>Raspbian</em>)
        all_platforms_rhel(<code>rhel</code><br/>🎩 <em>RedHat Enterprise Linux</em>)
        all_platforms_rocky(<code>rocky</code><br/>💠 <em>Rocky Linux</em>)
        all_platforms_scientific(<code>scientific</code><br/>❓ <em>Scientific Linux</em>)
        all_platforms_slackware(<code>slackware</code><br/>❓ <em>Slackware</em>)
        all_platforms_sles(<code>sles</code><br/>🦎 <em>SUSE Linux Enterprise Server</em>)
        all_platforms_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        all_platforms_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        all_platforms_ubuntu(<code>ubuntu</code><br/>🎯 <em>Ubuntu</em>)
        all_platforms_unknown_linux(<code>unknown_linux</code><br/>🐧 <em>Unknown Linux</em>)
        all_platforms_windows(<code>windows</code><br/>🪟 <em>Windows</em>)
        all_platforms_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        all_platforms_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
        all_platforms_xenserver(<code>xenserver</code><br/>❓ <em>XenServer</em>)
    end
    subgraph "<code>extra_platforms.BSD_WITHOUT_MACOS</code><br/>🅱️ <em>Any BSD but macOS</em>"
        bsd_without_macos_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        bsd_without_macos_midnightbsd(<code>midnightbsd</code><br/>🌘 <em>MidnightBSD</em>)
        bsd_without_macos_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        bsd_without_macos_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        bsd_without_macos_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
    end
    subgraph "<code>extra_platforms.LINUX_LIKE</code><br/>🐧+ <em>Any Linux and compatibility layers</em>"
        linux_like_altlinux(<code>altlinux</code><br/>❓ <em>ALT Linux</em>)
        linux_like_amzn(<code>amzn</code><br/>🙂 <em>Amazon Linux</em>)
        linux_like_android(<code>android</code><br/>🤖 <em>Android</em>)
        linux_like_arch(<code>arch</code><br/>🎗️ <em>Arch Linux</em>)
        linux_like_buildroot(<code>buildroot</code><br/>❓ <em>Buildroot</em>)
        linux_like_centos(<code>centos</code><br/>💠 <em>CentOS</em>)
        linux_like_cloudlinux(<code>cloudlinux</code><br/>❓ <em>CloudLinux OS</em>)
        linux_like_debian(<code>debian</code><br/>🌀 <em>Debian</em>)
        linux_like_exherbo(<code>exherbo</code><br/>❓ <em>Exherbo Linux</em>)
        linux_like_fedora(<code>fedora</code><br/>🎩 <em>Fedora</em>)
        linux_like_gentoo(<code>gentoo</code><br/>🗜️ <em>Gentoo Linux</em>)
        linux_like_guix(<code>guix</code><br/>❓ <em>Guix System</em>)
        linux_like_ibm_powerkvm(<code>ibm_powerkvm</code><br/>❓ <em>IBM PowerKVM</em>)
        linux_like_kvmibm(<code>kvmibm</code><br/>❓ <em>KVM for IBM z Systems</em>)
        linux_like_linuxmint(<code>linuxmint</code><br/>🌿 <em>Linux Mint</em>)
        linux_like_mageia(<code>mageia</code><br/>❓ <em>Mageia</em>)
        linux_like_mandriva(<code>mandriva</code><br/>❓ <em>Mandriva Linux</em>)
        linux_like_opensuse(<code>opensuse</code><br/>🦎 <em>openSUSE</em>)
        linux_like_oracle(<code>oracle</code><br/>🦴 <em>Oracle Linux</em>)
        linux_like_parallels(<code>parallels</code><br/>❓ <em>Parallels</em>)
        linux_like_pidora(<code>pidora</code><br/>❓ <em>Pidora</em>)
        linux_like_raspbian(<code>raspbian</code><br/>🍓 <em>Raspbian</em>)
        linux_like_rhel(<code>rhel</code><br/>🎩 <em>RedHat Enterprise Linux</em>)
        linux_like_rocky(<code>rocky</code><br/>💠 <em>Rocky Linux</em>)
        linux_like_scientific(<code>scientific</code><br/>❓ <em>Scientific Linux</em>)
        linux_like_slackware(<code>slackware</code><br/>❓ <em>Slackware</em>)
        linux_like_sles(<code>sles</code><br/>🦎 <em>SUSE Linux Enterprise Server</em>)
        linux_like_ubuntu(<code>ubuntu</code><br/>🎯 <em>Ubuntu</em>)
        linux_like_unknown_linux(<code>unknown_linux</code><br/>🐧 <em>Unknown Linux</em>)
        linux_like_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        linux_like_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
        linux_like_xenserver(<code>xenserver</code><br/>❓ <em>XenServer</em>)
    end
    subgraph "<code>extra_platforms.UNIX</code><br/>⨷ <em>Any Unix</em>"
        unix_aix(<code>aix</code><br/>➿ <em>IBM AIX</em>)
        unix_altlinux(<code>altlinux</code><br/>❓ <em>ALT Linux</em>)
        unix_amzn(<code>amzn</code><br/>🙂 <em>Amazon Linux</em>)
        unix_android(<code>android</code><br/>🤖 <em>Android</em>)
        unix_arch(<code>arch</code><br/>🎗️ <em>Arch Linux</em>)
        unix_buildroot(<code>buildroot</code><br/>❓ <em>Buildroot</em>)
        unix_centos(<code>centos</code><br/>💠 <em>CentOS</em>)
        unix_cloudlinux(<code>cloudlinux</code><br/>❓ <em>CloudLinux OS</em>)
        unix_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        unix_debian(<code>debian</code><br/>🌀 <em>Debian</em>)
        unix_exherbo(<code>exherbo</code><br/>❓ <em>Exherbo Linux</em>)
        unix_fedora(<code>fedora</code><br/>🎩 <em>Fedora</em>)
        unix_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        unix_gentoo(<code>gentoo</code><br/>🗜️ <em>Gentoo Linux</em>)
        unix_guix(<code>guix</code><br/>❓ <em>Guix System</em>)
        unix_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        unix_ibm_powerkvm(<code>ibm_powerkvm</code><br/>❓ <em>IBM PowerKVM</em>)
        unix_kvmibm(<code>kvmibm</code><br/>❓ <em>KVM for IBM z Systems</em>)
        unix_linuxmint(<code>linuxmint</code><br/>🌿 <em>Linux Mint</em>)
        unix_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        unix_mageia(<code>mageia</code><br/>❓ <em>Mageia</em>)
        unix_mandriva(<code>mandriva</code><br/>❓ <em>Mandriva Linux</em>)
        unix_midnightbsd(<code>midnightbsd</code><br/>🌘 <em>MidnightBSD</em>)
        unix_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        unix_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        unix_opensuse(<code>opensuse</code><br/>🦎 <em>openSUSE</em>)
        unix_oracle(<code>oracle</code><br/>🦴 <em>Oracle Linux</em>)
        unix_parallels(<code>parallels</code><br/>❓ <em>Parallels</em>)
        unix_pidora(<code>pidora</code><br/>❓ <em>Pidora</em>)
        unix_raspbian(<code>raspbian</code><br/>🍓 <em>Raspbian</em>)
        unix_rhel(<code>rhel</code><br/>🎩 <em>RedHat Enterprise Linux</em>)
        unix_rocky(<code>rocky</code><br/>💠 <em>Rocky Linux</em>)
        unix_scientific(<code>scientific</code><br/>❓ <em>Scientific Linux</em>)
        unix_slackware(<code>slackware</code><br/>❓ <em>Slackware</em>)
        unix_sles(<code>sles</code><br/>🦎 <em>SUSE Linux Enterprise Server</em>)
        unix_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        unix_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        unix_ubuntu(<code>ubuntu</code><br/>🎯 <em>Ubuntu</em>)
        unix_unknown_linux(<code>unknown_linux</code><br/>🐧 <em>Unknown Linux</em>)
        unix_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        unix_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
        unix_xenserver(<code>xenserver</code><br/>❓ <em>XenServer</em>)
    end
    subgraph "<code>extra_platforms.UNIX_WITHOUT_MACOS</code><br/>⨂ <em>Any Unix but macOS</em>"
        unix_without_macos_aix(<code>aix</code><br/>➿ <em>IBM AIX</em>)
        unix_without_macos_altlinux(<code>altlinux</code><br/>❓ <em>ALT Linux</em>)
        unix_without_macos_amzn(<code>amzn</code><br/>🙂 <em>Amazon Linux</em>)
        unix_without_macos_android(<code>android</code><br/>🤖 <em>Android</em>)
        unix_without_macos_arch(<code>arch</code><br/>🎗️ <em>Arch Linux</em>)
        unix_without_macos_buildroot(<code>buildroot</code><br/>❓ <em>Buildroot</em>)
        unix_without_macos_centos(<code>centos</code><br/>💠 <em>CentOS</em>)
        unix_without_macos_cloudlinux(<code>cloudlinux</code><br/>❓ <em>CloudLinux OS</em>)
        unix_without_macos_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        unix_without_macos_debian(<code>debian</code><br/>🌀 <em>Debian</em>)
        unix_without_macos_exherbo(<code>exherbo</code><br/>❓ <em>Exherbo Linux</em>)
        unix_without_macos_fedora(<code>fedora</code><br/>🎩 <em>Fedora</em>)
        unix_without_macos_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        unix_without_macos_gentoo(<code>gentoo</code><br/>🗜️ <em>Gentoo Linux</em>)
        unix_without_macos_guix(<code>guix</code><br/>❓ <em>Guix System</em>)
        unix_without_macos_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        unix_without_macos_ibm_powerkvm(<code>ibm_powerkvm</code><br/>❓ <em>IBM PowerKVM</em>)
        unix_without_macos_kvmibm(<code>kvmibm</code><br/>❓ <em>KVM for IBM z Systems</em>)
        unix_without_macos_linuxmint(<code>linuxmint</code><br/>🌿 <em>Linux Mint</em>)
        unix_without_macos_mageia(<code>mageia</code><br/>❓ <em>Mageia</em>)
        unix_without_macos_mandriva(<code>mandriva</code><br/>❓ <em>Mandriva Linux</em>)
        unix_without_macos_midnightbsd(<code>midnightbsd</code><br/>🌘 <em>MidnightBSD</em>)
        unix_without_macos_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        unix_without_macos_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        unix_without_macos_opensuse(<code>opensuse</code><br/>🦎 <em>openSUSE</em>)
        unix_without_macos_oracle(<code>oracle</code><br/>🦴 <em>Oracle Linux</em>)
        unix_without_macos_parallels(<code>parallels</code><br/>❓ <em>Parallels</em>)
        unix_without_macos_pidora(<code>pidora</code><br/>❓ <em>Pidora</em>)
        unix_without_macos_raspbian(<code>raspbian</code><br/>🍓 <em>Raspbian</em>)
        unix_without_macos_rhel(<code>rhel</code><br/>🎩 <em>RedHat Enterprise Linux</em>)
        unix_without_macos_rocky(<code>rocky</code><br/>💠 <em>Rocky Linux</em>)
        unix_without_macos_scientific(<code>scientific</code><br/>❓ <em>Scientific Linux</em>)
        unix_without_macos_slackware(<code>slackware</code><br/>❓ <em>Slackware</em>)
        unix_without_macos_sles(<code>sles</code><br/>🦎 <em>SUSE Linux Enterprise Server</em>)
        unix_without_macos_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        unix_without_macos_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        unix_without_macos_ubuntu(<code>ubuntu</code><br/>🎯 <em>Ubuntu</em>)
        unix_without_macos_unknown_linux(<code>unknown_linux</code><br/>🐧 <em>Unknown Linux</em>)
        unix_without_macos_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        unix_without_macos_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
        unix_without_macos_xenserver(<code>xenserver</code><br/>❓ <em>XenServer</em>)
    end
```

<!-- EXTRA_GROUPS-graph-end -->

> [!IMPORTANT]
> All the graphs above would be better off if merged. Unfortunately Graphviz is not capable of producing [Euler diagrams](https://xkcd.com/2721/). Only non-overlapping clusters can be rendered.
>
> There's still a chance to [have them supported by Mermaid](https://github.com/mermaid-js/mermaid/issues/2583) so we can switch to that if the feature materialize.

## Used in

Check these projects to get real-life examples of `extra-platforms` usage:

- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/meta-package-manager?label=%E2%AD%90&style=flat-square) [Meta Package Manager](https://github.com/kdeldycke/meta-package-manager#readme) - A unifying CLI for multiple package managers.
- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/click-extra?label=%E2%AD%90&style=flat-square) [Click Extra](https://github.com/kdeldycke/click-extra#readme) - Drop-in replacement for Click to make user-friendly and colorful CLI.

Feel free to send a PR to add your project in this list if you are relying on Click Extra in any way.

## Development

[Development guidelines](https://github.com/kdeldycke/click-extra?tab=readme-ov-file#development) are the same as [parent project Click Extra](https://github.com/kdeldycke/click-extra), from which `extra-platforms` originated.
