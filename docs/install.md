# {octicon}`download` Installation

This package is [available on PyPi](https://pypi.python.org/pypi/extra-platforms), so you can install the latest stable release with you favorite package manager:

`````{tab-set}

````{tab-item} uv
Easiest way is to [install `uv`](https://docs.astral.sh/uv/getting-started/installation/), then use it to add it to your project:

```{code-block} shell-session
$ uv add extra-platforms
```

Or to install it in your current virtual environment:

```{code-block} shell-session
$ uv venv add extra-platforms
```
````

````{tab-item} pip
```{code-block} shell-session
$ python -m pip install extra-platforms
```
````
`````

## Try Extra Platforms

Before you decide to permanently install Extra Platforms on your system, or before you add it as a dependency to your project, you may want to try it out first.

You can do so easily [with `uv`](https://docs.astral.sh/uv/guides/tools/#running-tools):

```shell-session
$ python -m pip install uv
...

```shell-session
$ uvx --with extra-platforms python
Installed 3 packages in 5ms
Python 3.11.11 (main, Mar 17 2025, 21:33:08) [Clang 20.1.0 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

```pycon
>>> import extra_platforms
>>> extra_platforms.__version__
'3.2.3'
>>>
```

````{tip}
The `uvx` command above is going to download the latest stable release of the `extra-platforms` package from PyPi. If you want to try the latest development version instead, you can do:

```shell-session
$ uvx --with git+https://github.com/kdeldycke/extra-platforms python
```
````

## Install with `pip`

This package is [available on PyPi](https://pypi.python.org/pypi/extra-platforms), so you can install the latest stable release and its dependencies with a simple `pip` call:

```shell-session
$ python -m pip install extra-platforms
```

See also [pip installation instructions](https://pip.pypa.io/en/stable/installing/).

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
