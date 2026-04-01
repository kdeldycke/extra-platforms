# {octicon}`download` Installation

```{sidebar}
[![Packaging status](https://repology.org/badge/vertical-allrepos/python%3Aextra-platforms.svg)](https://repology.org/project/python%3Aextra-platforms/versions)
```

This package is [available on PyPI](https://pypi.python.org/pypi/extra-platforms), so you can install the latest stable release with you favorite package manager:

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
$ uvx extra-platforms@9.0.1
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
Installed 3 packages in 5ms
Python 3.11.11 (main, Mar 17 2025, 21:33:08) [Clang 20.1.0 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import extra_platforms
>>> extra_platforms.__version__
'3.2.3'
>>>
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
