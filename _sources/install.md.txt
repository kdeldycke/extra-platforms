# Installation

## With `pip`

This package is [available on PyPi](https://pypi.python.org/pypi/extra-platforms), so you can install the latest stable release and its dependencies with a simple `pip` call:

```shell-session
$ pip install extra-platforms
```

See also [pip installation instructions](https://pip.pypa.io/en/stable/installing/).

## Main dependencies

This is a graph of the default, main dependencies of the Python package:

```mermaid assets/dependencies.mmd
:align: center
```

> [!IMPORTANT]
> Extra Platforms keep targeting Python 3.9 despite [back-pressure from underlying dependencies like `myst-reader`](https://github.com/kdeldycke/extra-platforms/pull/1), as [Python 3.9 will not be declared end-of-life until 2025-10](https://devguide.python.org/versions/).

## Extra dependencies

To get additional utilities [for Pytest](pytest.md), you may need to install extra dependencies:

```shell-session
$ pip install extra-platforms[pytest]
```

## Namning

> [!TIP]
> I wanted to call this package `platforms`, but it's already taken on PyPI. So I went with `extra-platforms` instead, to mark its affiliation with [Click Extra](https://github.com/kdeldycke/click-extra).
