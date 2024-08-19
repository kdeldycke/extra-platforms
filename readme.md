# Extra Platforms

[![Last release](https://img.shields.io/pypi/v/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Python versions](https://img.shields.io/pypi/pyversions/extra-platforms.svg)](https://pypi.python.org/pypi/extra-platforms)
[![Downloads](https://static.pepy.tech/badge/extra_platforms/month)](https://pepy.tech/project/extra_platforms)
[![Unittests status](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/tests.yaml?query=branch%3Amain)
[![Coverage status](https://codecov.io/gh/kdeldycke/extra-platforms/branch/main/graph/badge.svg)](https://app.codecov.io/gh/kdeldycke/extra-platforms)
[![Documentation status](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/extra-platforms/actions/workflows/docs.yaml?query=branch%3Amain)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13341712.svg)](https://doi.org/10.5281/zenodo.13341712)

## What is Extra Platforms?

> [!WARNING]
> TODO

> [!TIP]
> I wanted to call this package `platforms`, but it's already taken on PyPI. So I went with `extra-platforms` instead, to mark its affiliation with [Click Extra](https://github.com/kdeldycke/click-extra).

## Example

> [!WARNING]
> TODO

## Group → platforms mapping

Relationships between groups and platforms:

<!-- platform-sankey-start -->

```mermaid
sankey-beta

"🖥️ all_platforms","➿ aix",1
"🖥️ all_platforms","Ͼ cygwin",1
"🖥️ all_platforms","😈 freebsd",1
"🖥️ all_platforms","🐃 hurd",1
"🖥️ all_platforms","🐧 linux",1
"🖥️ all_platforms","🍎 macos",1
"🖥️ all_platforms","🚩 netbsd",1
"🖥️ all_platforms","🐡 openbsd",1
"🖥️ all_platforms","🌞 solaris",1
"🖥️ all_platforms","☀️ sunos",1
"🖥️ all_platforms","🪟 windows",1
"🖥️ all_platforms","⊞ wsl1",1
"🖥️ all_platforms","⊞ wsl2",1
"⨷ unix","➿ aix",1
"⨷ unix","Ͼ cygwin",1
"⨷ unix","😈 freebsd",1
"⨷ unix","🐃 hurd",1
"⨷ unix","🐧 linux",1
"⨷ unix","🍎 macos",1
"⨷ unix","🚩 netbsd",1
"⨷ unix","🐡 openbsd",1
"⨷ unix","🌞 solaris",1
"⨷ unix","☀️ sunos",1
"⨷ unix","⊞ wsl1",1
"⨷ unix","⊞ wsl2",1
"⨂ unix_without_macos","➿ aix",1
"⨂ unix_without_macos","Ͼ cygwin",1
"⨂ unix_without_macos","😈 freebsd",1
"⨂ unix_without_macos","🐃 hurd",1
"⨂ unix_without_macos","🐧 linux",1
"⨂ unix_without_macos","🚩 netbsd",1
"⨂ unix_without_macos","🐡 openbsd",1
"⨂ unix_without_macos","🌞 solaris",1
"⨂ unix_without_macos","☀️ sunos",1
"⨂ unix_without_macos","⊞ wsl1",1
"⨂ unix_without_macos","⊞ wsl2",1
"🅱️ bsd","😈 freebsd",1
"🅱️ bsd","🍎 macos",1
"🅱️ bsd","🚩 netbsd",1
"🅱️ bsd","🐡 openbsd",1
"🅱️ bsd","☀️ sunos",1
"🅱️ bsd_without_macos","😈 freebsd",1
"🅱️ bsd_without_macos","🚩 netbsd",1
"🅱️ bsd_without_macos","🐡 openbsd",1
"🅱️ bsd_without_macos","☀️ sunos",1
"Ⅴ system_v","➿ aix",1
"Ⅴ system_v","🌞 solaris",1
"≚ linux_layers","⊞ wsl1",1
"≚ linux_layers","⊞ wsl2",1
"≛ unix_layers","Ͼ cygwin",1
"⊎ other_unix","🐃 hurd",1
"🪟 all_windows","🪟 windows",1
"🐧 all_linux","🐧 linux",1
```

<!-- platform-sankey-end -->

## OS families

Each platform is assigned to a group of non-overlpaping families:

<!-- NON_OVERLAPPING_GROUPS-graph-start -->

{caption="`click_extra.platforms.NON_OVERLAPPING_GROUPS` - Non-overlapping groups."}
```mermaid
flowchart
    subgraph "<code>click_extra.platforms.ALL_LINUX</code><br/>🐧 <em>Any Linux</em>"
        all_linux_linux(<code>linux</code><br/>🐧 <em>Linux</em>)
    end
    subgraph "<code>click_extra.platforms.ALL_WINDOWS</code><br/>🪟 <em>Any Windows</em>"
        all_windows_windows(<code>windows</code><br/>🪟 <em>Windows</em>)
    end
    subgraph "<code>click_extra.platforms.BSD</code><br/>🅱️ <em>Any BSD</em>"
        bsd_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        bsd_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        bsd_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        bsd_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        bsd_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
    end
    subgraph "<code>click_extra.platforms.LINUX_LAYERS</code><br/>≚ <em>Any Linux compatibility layers</em>"
        linux_layers_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        linux_layers_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
    end
    subgraph "<code>click_extra.platforms.OTHER_UNIX</code><br/>⊎ <em>Any other Unix</em>"
        other_unix_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
    end
    subgraph "<code>click_extra.platforms.SYSTEM_V</code><br/>Ⅴ <em>Any Unix derived from AT&amp;T System Five</em>"
        system_v_aix(<code>aix</code><br/>➿ <em>AIX</em>)
        system_v_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
    end
    subgraph "<code>click_extra.platforms.UNIX_LAYERS</code><br/>≛ <em>Any Unix compatibility layers</em>"
        unix_layers_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
    end
```

<!-- NON_OVERLAPPING_GROUPS-graph-end -->

## Other groups

Other groups are available for convenience, but these overlaps:

<!-- EXTRA_GROUPS-graph-start -->

{caption="`click_extra.platforms.EXTRA_GROUPS` - Overlapping groups, defined for convenience."}
```mermaid
flowchart
    subgraph "<code>click_extra.platforms.ALL_PLATFORMS</code><br/>🖥️ <em>Any platforms</em>"
        all_platforms_aix(<code>aix</code><br/>➿ <em>AIX</em>)
        all_platforms_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        all_platforms_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        all_platforms_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        all_platforms_linux(<code>linux</code><br/>🐧 <em>Linux</em>)
        all_platforms_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        all_platforms_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        all_platforms_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        all_platforms_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        all_platforms_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        all_platforms_windows(<code>windows</code><br/>🪟 <em>Windows</em>)
        all_platforms_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        all_platforms_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
    end
    subgraph "<code>click_extra.platforms.BSD_WITHOUT_MACOS</code><br/>🅱️ <em>Any BSD but macOS</em>"
        bsd_without_macos_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        bsd_without_macos_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        bsd_without_macos_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        bsd_without_macos_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
    end
    subgraph "<code>click_extra.platforms.UNIX</code><br/>⨷ <em>Any Unix</em>"
        unix_aix(<code>aix</code><br/>➿ <em>AIX</em>)
        unix_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        unix_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        unix_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        unix_linux(<code>linux</code><br/>🐧 <em>Linux</em>)
        unix_macos(<code>macos</code><br/>🍎 <em>macOS</em>)
        unix_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        unix_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        unix_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        unix_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        unix_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        unix_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
    end
    subgraph "<code>click_extra.platforms.UNIX_WITHOUT_MACOS</code><br/>⨂ <em>Any Unix but macOS</em>"
        unix_without_macos_aix(<code>aix</code><br/>➿ <em>AIX</em>)
        unix_without_macos_cygwin(<code>cygwin</code><br/>Ͼ <em>Cygwin</em>)
        unix_without_macos_freebsd(<code>freebsd</code><br/>😈 <em>FreeBSD</em>)
        unix_without_macos_hurd(<code>hurd</code><br/>🐃 <em>GNU/Hurd</em>)
        unix_without_macos_linux(<code>linux</code><br/>🐧 <em>Linux</em>)
        unix_without_macos_netbsd(<code>netbsd</code><br/>🚩 <em>NetBSD</em>)
        unix_without_macos_openbsd(<code>openbsd</code><br/>🐡 <em>OpenBSD</em>)
        unix_without_macos_solaris(<code>solaris</code><br/>🌞 <em>Solaris</em>)
        unix_without_macos_sunos(<code>sunos</code><br/>☀️ <em>SunOS</em>)
        unix_without_macos_wsl1(<code>wsl1</code><br/>⊞ <em>Windows Subsystem for Linux v1</em>)
        unix_without_macos_wsl2(<code>wsl2</code><br/>⊞ <em>Windows Subsystem for Linux v2</em>)
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
