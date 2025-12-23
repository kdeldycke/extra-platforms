# {octicon}`codespaces` Platforms

To add a new Linux distribution, you can get inspiration from these pull requests:

- https://github.com/kdeldycke/extra-platforms/pull/156
- https://github.com/kdeldycke/extra-platforms/pull/94

## Recognized platforms

<!-- platform-table-start -->

| Icon | Name | Platform ID |
|:----:|:------|:-------------|
| ➿ | [IBM AIX](https://ibm.com/products/aix/) | `aix` |
| 🐧 | [ALT Linux](https://altlinux.org) | `altlinux` |
| ⤻ | [Amazon Linux](https://aws.amazon.com/amazon-linux-ami/) | `amzn` |
| 🤖 | [Android](https://android.com) | `android` |
| 🎗️ | [Arch Linux](https://archlinux.org) | `arch` |
| ⛑️ | [Buildroot](https://buildroot.org) | `buildroot` |
| ⌬ | [CachyOS](https://cachyos.org) | `cachyos` |
| 💠 | [CentOS](https://centos.org) | `centos` |
| ꩜ | [CloudLinux OS](https://cloudlinux.com) | `cloudlinux` |
| Ͼ | [Cygwin](https://cygwin.com) | `cygwin` |
| 🌀 | [Debian](https://debian.org) | `debian` |
| 🐽 | [Exherbo Linux](https://exherbolinux.org) | `exherbo` |
| 🎩 | [Fedora](https://fedoraproject.org) | `fedora` |
| 😈 | [FreeBSD](https://freebsd.org) | `freebsd` |
| 🗜️ | [Gentoo Linux](https://gentoo.org) | `gentoo` |
| 🐃 | [Guix System](https://guix.gnu.org) | `guix` |
| 🐃 | [GNU/Hurd](https://gnu.org/software/hurd/) | `hurd` |
| 🤹 | [IBM PowerKVM](https://ibm.com/mysupport/s/topic/0TO50000000QkyPGAS/) | `ibm_powerkvm` |
| 🤹 | [KVM for IBM z Systems](https://ibm.com/products/kvm/) | `kvmibm` |
| 🌿 | [Linux Mint](https://linuxmint.com) | `linuxmint` |
| 🍎 | [macOS](https://apple.com/macos/) | `macos` |
| ⍥ | [Mageia](https://mageia.org) | `mageia` |
| 💫 | [Mandriva Linux](https://web.archive.org/web/20150522203942/https://mandriva.com/en/mbs/) | `mandriva` |
| 🌘 | [MidnightBSD](https://midnightbsd.org) | `midnightbsd` |
| 🚩 | [NetBSD](https://netbsd.org) | `netbsd` |
|  | [Nobara](https://nobaraproject.org) | `nobara` |
| 🐡 | [OpenBSD](https://openbsd.org) | `openbsd` |
| 🦎 | [openSUSE](https://opensuse.org) | `opensuse` |
| 🦴 | [Oracle Linux](https://oracle.com/linux/) | `oracle` |
| ∥ | [Parallels](https://parallels.com) | `parallels` |
| 🍓 | [Pidora](https://web.archive.org/web/20200227132047/http://pidora.ca:80/) | `pidora` |
| 🍓 | [Raspbian](https://raspberrypi.com/software/) | `raspbian` |
| 🎩 | [RedHat Enterprise Linux](https://redhat.com/rhel/) | `rhel` |
| ⛰️ | [Rocky Linux](https://rockylinux.org) | `rocky` |
| ⚛️ | [Scientific Linux](https://scientificlinux.org) | `scientific` |
| 🚬 | [Slackware](https://www.slackware.com) | `slackware` |
| 🦎 | [SUSE Linux Enterprise Server](https://suse.com/products/server/) | `sles` |
| 🌞 | [Solaris](https://oracle.com/solaris) | `solaris` |
| ☀️ | [SunOS](https://wikipedia.org/wiki/SunOS) | `sunos` |
| ↻ | [openSUSE Tumbleweed](https://get.opensuse.org/tumbleweed/) | `tumbleweed` |
| 🤵 | [Tuxedo OS](https://tuxedocomputers.com/os) | `tuxedo` |
| 🎯 | [Ubuntu](https://ubuntu.com) | `ubuntu` |
| 🌊 | [Ultramarine](https://ultramarine-linux.org) | `ultramarine` |
| 🐧 | [Unknown Linux](https://kernel.org) | `unknown_linux` |
| 🪟 | [Windows](https://windows.com) | `windows` |
| ⊞ | [Windows Subsystem for Linux v1](https://learn.microsoft.com/windows/wsl) | `wsl1` |
| ⊞ | [Windows Subsystem for Linux v2](https://learn.microsoft.com/windows/wsl) | `wsl2` |
| Ⓧ | [XenServer](https://xenproject.org) | `xenserver` |

<!-- platform-table-end -->

## Groups of platforms

All recognized platforms are grouped in families.

### Non-overlapping groups

All platforms are distributed in groups that are guaranteed to be non-overlapping.

Here is the list of non-overlapping groups that encompass all recognized platforms, visualized as a Sankey diagram:

<!-- platform-multi-level-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 800}}
---
sankey-beta

ALL_PLATFORMS,LINUX,35
ALL_PLATFORMS,BSD,6
ALL_PLATFORMS,SYSTEM_V,2
ALL_PLATFORMS,LINUX_LAYERS,2
ALL_PLATFORMS,UNIX_LAYERS,1
ALL_PLATFORMS,OTHER_UNIX,1
ALL_PLATFORMS,ANY_WINDOWS,1
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
BSD,freebsd,1
BSD,macos,1
BSD,midnightbsd,1
BSD,netbsd,1
BSD,openbsd,1
BSD,sunos,1
SYSTEM_V,aix,1
SYSTEM_V,solaris,1
LINUX_LAYERS,wsl1,1
LINUX_LAYERS,wsl2,1
UNIX_LAYERS,cygwin,1
OTHER_UNIX,hurd,1
ANY_WINDOWS,windows,1
```

<!-- platform-multi-level-sankey-end -->

### Overlapping groups

For convenience, other groups are defined, but without guarantee of non-overlapping platforms:

<!-- extra-platform-groups-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

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
```

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

BSD_WITHOUT_MACOS,freebsd,1
BSD_WITHOUT_MACOS,midnightbsd,1
BSD_WITHOUT_MACOS,netbsd,1
BSD_WITHOUT_MACOS,openbsd,1
BSD_WITHOUT_MACOS,sunos,1
```

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

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
```

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

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
```

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

ALL_PLATFORMS,aix,1
ALL_PLATFORMS,altlinux,1
ALL_PLATFORMS,amzn,1
ALL_PLATFORMS,android,1
ALL_PLATFORMS,arch,1
ALL_PLATFORMS,buildroot,1
ALL_PLATFORMS,cachyos,1
ALL_PLATFORMS,centos,1
ALL_PLATFORMS,cloudlinux,1
ALL_PLATFORMS,cygwin,1
ALL_PLATFORMS,debian,1
ALL_PLATFORMS,exherbo,1
ALL_PLATFORMS,fedora,1
ALL_PLATFORMS,freebsd,1
ALL_PLATFORMS,gentoo,1
ALL_PLATFORMS,guix,1
ALL_PLATFORMS,hurd,1
ALL_PLATFORMS,ibm_powerkvm,1
ALL_PLATFORMS,kvmibm,1
ALL_PLATFORMS,linuxmint,1
ALL_PLATFORMS,macos,1
ALL_PLATFORMS,mageia,1
ALL_PLATFORMS,mandriva,1
ALL_PLATFORMS,midnightbsd,1
ALL_PLATFORMS,netbsd,1
ALL_PLATFORMS,nobara,1
ALL_PLATFORMS,openbsd,1
ALL_PLATFORMS,opensuse,1
ALL_PLATFORMS,oracle,1
ALL_PLATFORMS,parallels,1
ALL_PLATFORMS,pidora,1
ALL_PLATFORMS,raspbian,1
ALL_PLATFORMS,rhel,1
ALL_PLATFORMS,rocky,1
ALL_PLATFORMS,scientific,1
ALL_PLATFORMS,slackware,1
ALL_PLATFORMS,sles,1
ALL_PLATFORMS,solaris,1
ALL_PLATFORMS,sunos,1
ALL_PLATFORMS,tumbleweed,1
ALL_PLATFORMS,tuxedo,1
ALL_PLATFORMS,ubuntu,1
ALL_PLATFORMS,ultramarine,1
ALL_PLATFORMS,unknown_linux,1
ALL_PLATFORMS,windows,1
ALL_PLATFORMS,wsl1,1
ALL_PLATFORMS,wsl2,1
ALL_PLATFORMS,xenserver,1
```

<!-- extra-platform-groups-sankey-end -->

## `extra_platforms.platform` API

```{eval-rst}
.. autoclasstree:: extra_platforms.platform
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.platform
   :members:
   :undoc-members:
   :show-inheritance:
```

## `extra_platforms.platform_data` API

```{eval-rst}
.. autoclasstree:: extra_platforms.platform_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.platform_data
   :members:
   :undoc-members:
   :show-inheritance:
```
