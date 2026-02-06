# {octicon}`book` Sphinx

## Cross-referencing symbols

Sphinx provides several roles to create cross-references to Python symbols in the `extra_platforms` module. These roles work in both MyST Markdown and reStructuredText formats.

### Available roles

- [`{func}`](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-func) — Reference a function (e.g., {func}`~extra_platforms.is_linux`, {func}`~extra_platforms.current_traits`)
- [`{data}`](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-data) — Reference a module-level constant (e.g., {data}`~extra_platforms.UBUNTU`, {data}`~extra_platforms.pytest.skip_linux`)
- [`{class}`](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-class) — Reference a class (e.g., {class}`~extra_platforms.Platform`, {class}`~extra_platforms.Architecture`, {class}`~extra_platforms.Group`)
- [`{mod}`](https://www.sphinx-doc.org/en/master/usage/domains/python.html#role-py-mod) — Reference a module (e.g., {mod}`~extra_platforms.detection`)

```{note}
Pytest decorators like {data}`~extra_platforms.pytest.skip_linux` are `MarkDecorator` objects. Use `{data}` for inline cross-references. For API documentation, the built-in [`autodecorator`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autodecorator) directive renders them with the `@` prefix (see [pytest.md](pytest.md)).
```

### Syntax

`````{tab-set}

````{tab-item} MyST Markdown
:sync: myst
Use curly braces and backticks:

```markdown
Check the current platform with {func}`~extra_platforms.is_linux`.

The {class}`~extra_platforms.Platform` class represents operating systems.

Pre-defined platforms like {data}`~extra_platforms.UBUNTU` are available.

See the {mod}`extra_platforms.detection` module for detection functions.
```
````

````{tab-item} reStructuredText
:sync: rst
Use colons and backticks:

```rst
Check the current platform with :func:`~extra_platforms.is_linux`.

The :class:`~extra_platforms.Platform` class represents operating systems.

Pre-defined platforms like :data:`~extra_platforms.UBUNTU` are available.

See the :mod:`extra_platforms.detection` module for detection functions.
```
````

`````

Which renders as:

> Check the current platform with {func}`~extra_platforms.is_linux`.
>
> The {class}`~extra_platforms.Platform` class represents operating systems.
>
> Pre-defined platforms like {data}`~extra_platforms.UBUNTU` are available.
>
> See the {mod}`extra_platforms.detection` module for detection functions.

The tilde (`~`) prefix displays only the symbol name without the full module path:

- `` {func}`~extra_platforms.is_linux `` renders as {func}`~extra_platforms.is_linux`
- `` {func}`extra_platforms.is_linux `` renders as {func}`extra_platforms.is_linux`

### Setting a default module

To avoid repeating the module name, use the [`currentmodule`](https://www.sphinx-doc.org/en/master/usage/domains/python.html#directive-py-currentmodule) directive:

``````{tab-set}

`````{tab-item} MyST Markdown
:sync: myst
````markdown
```{py:currentmodule} extra_platforms
```

Use {func}`is_linux` or {func}`is_windows` to check platforms.
````
`````

````{tab-item} reStructuredText
:sync: rst
```rst
.. py:currentmodule:: extra_platforms

Use :func:`is_linux` or :func:`is_windows` to check platforms.
```
````

``````

```{py:currentmodule} extra_platforms
```

Which renders as:

> Use {func}`is_linux` or {func}`is_windows` to check platforms.

### Cross-reference resolution

Symbols exposed at the root `extra_platforms` module automatically link to their actual definition location:

- {func}`~extra_platforms.current_traits` links to `detection.html`
- {class}`~extra_platforms.Platform` links to `trait.html`
- {data}`~extra_platforms.UBUNTU` links to `platform_data.html`

This ensures documentation remains accurate even when symbols are re-exported from submodules.

## Reference matrix

This section demonstrates all syntax variations for referencing different object types in the `extra_platforms` module. All examples use the short-path format with the `currentmodule` directive.

```{py:currentmodule} extra_platforms
```

| MyST syntax                                       | Rendering                                   | Description                                                |
| ------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------- |
|                                                   |                                             | **Traits**                                                 |
| `` {data}`~UBUNTU` ``                             | {data}`~UBUNTU`                             | Platform trait symbol                                      |
| `` {func}`~is_ubuntu` ``                          | {func}`~is_ubuntu`                          | Platform trait detection function                          |
| `` {data}`~pytest.skip_ubuntu` ``                 | {data}`~pytest.skip_ubuntu`                 | Platform trait skip decorator                              |
| `` {data}`~pytest.unless_ubuntu` ``               | {data}`~pytest.unless_ubuntu`               | Platform trait unless decorator                            |
| `` {data}`~AARCH64` ``                            | {data}`~AARCH64`                            | Architecture trait symbol                                  |
| `` {func}`~is_aarch64` ``                         | {func}`~is_aarch64`                         | Architecture trait detection function                      |
| `` {data}`~pytest.skip_aarch64` ``                | {data}`~pytest.skip_aarch64`                | Architecture trait skip decorator                          |
| `` {data}`~pytest.unless_aarch64` ``              | {data}`~pytest.unless_aarch64`              | Architecture trait unless decorator                        |
| `` {data}`~GITHUB_CI` ``                          | {data}`~GITHUB_CI`                          | CI trait symbol                                            |
| `` {func}`~is_github_ci` ``                       | {func}`~is_github_ci`                       | CI trait detection function                                |
| `` {data}`~pytest.skip_github_ci` ``              | {data}`~pytest.skip_github_ci`              | CI trait skip decorator                                    |
| `` {data}`~pytest.unless_github_ci` ``            | {data}`~pytest.unless_github_ci`            | CI trait unless decorator                                  |
|                                                   |                                             | **Groups**                                                 |
| `` {data}`~LINUX` ``                              | {data}`~LINUX`                              | Regular group symbol                                       |
| `` {func}`~is_linux` ``                           | {func}`~is_linux`                           | Regular group detection function                           |
| `` {data}`~pytest.skip_linux` ``                  | {data}`~pytest.skip_linux`                  | Regular group skip decorator                               |
| `` {data}`~pytest.unless_linux` ``                | {data}`~pytest.unless_linux`                | Regular group unless decorator                             |
| `` {data}`~ALL_PLATFORMS` ``                      | {data}`~ALL_PLATFORMS`                      | `ALL_*` group symbol                                       |
| `` {func}`~is_any_platform` ``                    | {func}`~is_any_platform`                    | `ALL_*` group detection function                           |
| `` {data}`~pytest.skip_all_platforms` ``          | {data}`~pytest.skip_all_platforms`          | `ALL_*` group skip decorator                               |
| `` {data}`~pytest.unless_any_platform` ``         | {data}`~pytest.unless_any_platform`         | `ALL_*` group unless decorator                             |
| `` {data}`~UNKNOWN_PLATFORM` ``                   | {data}`~UNKNOWN_PLATFORM`                   | Unknown platform symbol                                    |
| `` {func}`~is_unknown_platform` ``                | {func}`~is_unknown_platform`                | Unknown platform detection function                        |
| `` {data}`~pytest.skip_unknown_platform` ``       | {data}`~pytest.skip_unknown_platform`       | Unknown platform skip decorator                            |
| `` {data}`~pytest.unless_unknown_platform` ``     | {data}`~pytest.unless_unknown_platform`     | Unknown platform unless decorator                          |
| `` {data}`~UNKNOWN_ARCHITECTURE` ``               | {data}`~UNKNOWN_ARCHITECTURE`               | Unknown architecture symbol                                |
| `` {func}`~is_unknown_architecture` ``            | {func}`~is_unknown_architecture`            | Unknown architecture detection function                    |
| `` {data}`~pytest.skip_unknown_architecture` ``   | {data}`~pytest.skip_unknown_architecture`   | Unknown architecture skip decorator                        |
| `` {data}`~pytest.unless_unknown_architecture` `` | {data}`~pytest.unless_unknown_architecture` | Unknown architecture unless decorator                      |
| `` {data}`~UNKNOWN_CI` ``                         | {data}`~UNKNOWN_CI`                         | Unknown CI symbol                                          |
| `` {func}`~is_unknown_ci` ``                      | {func}`~is_unknown_ci`                      | Unknown CI detection function                              |
| `` {data}`~pytest.skip_unknown_ci` ``             | {data}`~pytest.skip_unknown_ci`             | Unknown CI skip decorator                                  |
| `` {data}`~pytest.unless_unknown_ci` ``           | {data}`~pytest.unless_unknown_ci`           | Unknown CI unless decorator                                |
| `` {data}`~UNIX_WITHOUT_MACOS` ``                 | {data}`~UNIX_WITHOUT_MACOS`                 | Group with `_without_` (translated to `_not_` in function) |
| `` {func}`~is_unix_not_macos` ``                  | {func}`~is_unix_not_macos`                  | Group function with `_without_` → `_not_` translation      |
|                                                   |                                             | **Detection Methods**                                      |
| `` {func}`~current_platform` ``                   | {func}`~current_platform`                   | Current platform detection function                        |
| `` {func}`~current_architecture` ``               | {func}`~current_architecture`               | Current architecture detection function                    |
| `` {func}`~current_ci` ``                         | {func}`~current_ci`                         | Current CI detection function                              |
| `` {func}`~current_traits` ``                     | {func}`~current_traits`                     | All current traits detection function                      |
|                                                   |                                             | **Classes**                                                |
| `` {class}`~Platform` ``                          | {class}`~Platform`                          | Platform trait class                                       |
| `` {class}`~Architecture` ``                      | {class}`~Architecture`                      | Architecture trait class                                   |
| `` {class}`~CI` ``                                | {class}`~CI`                                | CI trait class                                             |
| `` {class}`~Group` ``                             | {class}`~Group`                             | Group class                                                |
|                                                   |                                             | **Utilities**                                              |
| `` {func}`~reduce` ``                             | {func}`~reduce`                             | Reduce utility function                                    |
| `` {func}`~invalidate_caches` ``                  | {func}`~invalidate_caches`                  | Cache invalidation utility function                        |

```{tip}
All the examples in this reference matrix are tested in [`tests/test_sphinx_crossrefs.py`](https://github.com/kdeldycke/extra-platforms/blob/main/tests/test_sphinx_crossrefs.py) to ensure cross-references resolve correctly in the built documentation.
```
