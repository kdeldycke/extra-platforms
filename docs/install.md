# {octicon}`download` Installation

```{sidebar}
[![Packaging status](https://repology.org/badge/vertical-allrepos/python%3Aextra-platforms.svg)](https://repology.org/project/python%3Aextra-platforms/versions)
```

This package is [available on PyPI](https://pypi.python.org/pypi/extra-platforms) and in several OS distributions, so you can install the latest stable release with your favorite package manager:

`````{tab-set}

````{tab-item} uv
Easiest way is to [install `uv`](https://docs.astral.sh/uv/getting-started/installation/), then add it to your project:

```{code-block} shell-session
$ uv add extra-platforms
```

Or to install the CLI system-wide with [`uv tool`](https://docs.astral.sh/uv/guides/tools/#installing-tools):

```{code-block} shell-session
$ uv tool install extra-platforms
```
````

````{tab-item} pipx
[`pipx`](https://pipx.pypa.io/stable/how-to/install-pipx/) is a great way to install the CLI globally:

```{code-block} shell-session
$ pipx install extra-platforms
```
````

````{tab-item} pip
You can install the latest stable release and its dependencies with a simple `pip` call:

```shell-session
$ python -m pip install extra-platforms
```

See also [pip installation instructions](https://pip.pypa.io/en/stable/installing/).
````

````{tab-item} Arch Linux
A [`python-extra-platforms` package](https://aur.archlinux.org/packages/python-extra-platforms) is available on AUR and can be installed with any AUR helper:

```{code-block} shell-session
$ yay -S python-extra-platforms
```

```{code-block} shell-session
$ paru -S python-extra-platforms
```
````

````{tab-item} Guix
Extra Platforms is [available in GNU Guix](https://packages.guix.gnu.org/packages/python-extra-platforms/):

```{code-block} shell-session
$ guix install python-extra-platforms
```

```{tip}
The package [landed in Guix on 2026-06-28](https://codeberg.org/guix/guix/pulls/8047). If `guix install` cannot find it yet, refresh your channels first with `guix pull`.
```
````

````{tab-item} openSUSE
The [`python-extra-platforms` package](https://software.opensuse.org/package/python-extra-platforms) is available on openSUSE Tumbleweed:

```{code-block} shell-session
$ sudo zypper install python3-extra-platforms
```
````

````{tab-item} pkgsrc
The [`sysutils/py-extra-platforms` package](https://pkgsrc.se/sysutils/py-extra-platforms) is available in pkgsrc for NetBSD and all other [platforms supported by pkgsrc](https://www.pkgsrc.org):

```{code-block} shell-session
$ pkgin install py313-extra-platforms
```

Or build it from source:

```{code-block} shell-session
$ cd /usr/pkgsrc/sysutils/py-extra-platforms
$ make install clean
```
````
`````

## Try it now

You can try Extra Platforms right now in your terminal, without installing any dependency or virtual env [thanks to `uvx`](https://docs.astral.sh/uv/guides/tools/):

`````{tab-set}
````{tab-item} Latest version
```shell-session
$ uvx extra-platforms
```
````

````{tab-item} Specific version
```shell-session
$ uvx extra-platforms@13.1.0
```
````

````{tab-item} Development version
```shell-session
$ uvx --from git+https://github.com/kdeldycke/extra-platforms -- extra-platforms
```
````

````{tab-item} Local version
```shell-session
$ uvx --from file:///Users/me/code/extra-platforms -- extra-platforms
```
````
`````

## Try the library

You can also try the library itself in an interactive Python shell without installing anything on your system:

```{code-block} shell-session
$ uvx --with extra-platforms python
```

```{code-block} pycon
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

## Main dependencies

This is a graph of the default, main dependencies of the Python package:

```mermaid assets/dependencies.mmd
:align: center
```

## Extra dependencies

For additional features, you may need to install extra dependencies.

### For Pytest

Activate new [fixtures and utilities](pytest.md) for testing Click CLIs:

```{code-block} shell-session
$ pip install extra-platforms[pytest]
```

## Naming

> [!TIP]
> I wanted to call this package `platforms`, but it's already taken on PyPI. So I went with `extra-platforms` instead, to mark its affiliation with [Click Extra](https://github.com/kdeldycke/click-extra).
