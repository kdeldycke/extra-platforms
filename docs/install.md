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

## Extra dependencies

To get additional utilities [for Pytest](pytest.md), you may need to install extra dependencies:

```shell-session
$ pip install extra-platforms[pytest]
```