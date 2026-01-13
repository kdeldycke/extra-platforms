# {octicon}`tag` Traits

All aspects of a system are represented as *traits*.

There are three main types of traits:

- **[Architectures](architectures.md)**: CPU architectures (e.g., x86_64, ARM64)
- **[Platforms](platforms.md)**: Operating systems (e.g., Windows, macOS, Ubuntu)
- **[CI systems](ci.md)**: Continuous Integration environments (e.g., GitHub Actions, Travis CI)

## Trait usage

### Predefined traits

All traits are available at the root of the `extra_platforms` package, as an uppercase symbol:

```pycon
>>> from extra_platforms import X86_64  # import an architecture
>>> X86_64
Architecture(id='x86_64', name='x86-64 (AMD64)')
>>> from extra_platforms import DEBIAN  # import a platform
>>> DEBIAN
Platform(id='debian', name='Debian')
>>> from extra_platforms import GITHUB_CI  # import a CI system
>>> GITHUB_CI
CI(id='github_ci', name='GitHub Actions runner')
```

They all inherit from the [`Trait` base class](#extra_platforms.trait.Trait), and share a common interface.

### Detection functions

Each trait is associated with a [detection function](detection.md), which returns `True` if the current system matches that trait.

These functions are also exposed at the root of the `extra_platforms` package:

```pycon
>>> from extra_platforms import is_x86_64, is_debian, is_github_ci
>>> is_x86_64()
True
>>> is_debian()
False
>>> is_github_ci()
False
```

### Current property

Each trait has a [`current` property](#extra_platforms.trait.Trait.current) that calls the corresponding detection function:

```pycon
>>> X86_64.current
True
>>> DEBIAN.current
False
>>> GITHUB_CI.current
False
```

### Groups

Traits are combined into [groups](groups.md) for easier detection of related traits.

You can get all groups a trait belongs to via the [`groups` property](#extra_platforms.trait.Trait.groups):

```pycon
>>> X86_64.groups
frozenset({
   Group(id='x86', name='x86 family'),
   Group(id='all_architectures', name='All architectures'),
   Group(id='arch_64_bit', name='64-bit architectures'),
   Group(id='all_traits', name='Any architectures, platforms and CI systems')})
```

### Additional information

Each trait provides an [`info()` method](#extra_platforms.trait.Trait.info) that returns a dictionary containing all available metadata about that trait:

```pycon
>>> from extra_platforms import AARCH64, MACOS
>>> AARCH64.info()
{'id': 'aarch64', 'name': 'ARM64 (AArch64)', 'icon': '📱', 'url': 'https://en.wikipedia.org/wiki/AArch64', 'current': True, 'machine': 'arm64', 'processor': None}
>>> MACOS.info()
{'id': 'macos', 'name': 'macOS', 'icon': '🍎', 'url': 'https://apple.com/macos/', 'current': True, 'distro_id': 'darwin', 'version': '26.2', 'version_parts': {'major': '26', 'minor': '2', 'build_number': None}, 'like': None, 'codename': 'Tahoe'}
```

The exact structure depends on the trait type.

## Trait implementation

```{eval-rst}
.. autoclasstree:: extra_platforms.trait
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.trait
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:
```
