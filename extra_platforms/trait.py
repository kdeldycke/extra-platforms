# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Trait base class for architectures, platforms, shells, terminals, and more.

A trait represents a distinguishing characteristic of a runtime environment.
Each trait has a unique ID, a human-readable name, an icon, and the ability
to detect if it matches the current environment.

Data associated with traits can be aggressively cached and frozen, as they're only
computed based on environment-dependent values.

```{note}
No annotation in this module reads `typing.ClassVar`. A dataclass recognizes a
`ClassVar` field only once `typing` is imported, and nothing else in the package
needs `typing` at runtime. The class-level metadata lives on `_ClassMetadata`
instead, a plain class no dataclass reads fields from.
```
"""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from functools import cached_property
from operator import attrgetter
from os import environ

from ._docstrings import get_attribute_docstring
from ._utils import _recursive_update, _remove_blanks
from .platform_info import linux_info, macos_info, windows_info

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

    from .group import Group


class _LazyDocstring:
    """The class docstring, or a generated one on a predefined trait or group.

    {meth}`_Identifiable.__post_init__` installs one in place of the docstring
    of a class when the class gets its first instance. Read on the class, it
    hands back that docstring, so `help()` and autodoc see the class as written.

    The class definition is too early to install it. `@dataclass` runs after
    `__init_subclass__` and replaces an empty class docstring with the
    signature of the class, and `python -OO` leaves every class docstring
    empty.

    Read on a member of `ALL_TRAITS` or `ALL_GROUPS`, it calls the instance's
    `generate_docstring()` once and keeps the result in the instance's own
    `__dict__`, where later reads find it first. Membership is by equality: an
    equal copy of a predefined object reads the same generated docstring.

    Read on any other instance, it hands back the class docstring too. A
    generated docstring describes a predefined object: it links a detection
    function and Pytest decorators that only those have, and a derived group
    would borrow the attribute docstring of the predefined group whose ID it
    carries.

    Generating on first read spares `import extra_platforms` the parse of each
    data module's source and the membership walk of every trait.
    """

    __slots__ = ("class_doc",)

    def __init__(self, class_doc: str | None) -> None:
        self.class_doc = class_doc

    def __get__(
        self, instance: Trait | Group | None, owner: type | None = None
    ) -> str | None:
        if instance is None:
            return self.class_doc

        # Avoid circular import.
        from .group_data import ALL_GROUPS, ALL_TRAITS

        registry = ALL_TRAITS if isinstance(instance, Trait) else ALL_GROUPS
        if instance not in registry:
            return self.class_doc

        doc = instance.generate_docstring()
        # Bypasses the frozen dataclass guard, like the cached properties do.
        object.__setattr__(instance, "__doc__", doc)
        return doc


class _ClassMetadata:
    """Class-level documentation metadata of trait and group classes.

    {meth}`_Identifiable.__init_subclass__` derives each of them from the class
    name, unless the class definition passes it as a keyword argument, like
    `class CI(Trait, type_name="CI system")`, or sets it in the class body.
    """

    type_id = ""
    """Machine-readable type identifier used to derive module and symbol names."""

    type_name = ""
    """Human-readable type name for documentation, like `"CI system"`."""

    data_module_id = ""
    """The module name where instances of this type are defined."""

    unknown_symbol = ""
    """The symbol name for the unknown instance of this type."""

    all_group = ""
    """The symbol name for the group containing all instances of this type."""

    doc_page = ""
    """The documentation page filename."""


@dataclass(frozen=True)
class _Identifiable(_ClassMetadata):
    """Base class for identifiable objects with common documentation fields.

    Provides the fields, the derived names and the initialization logic shared
    by both {class}`~extra_platforms.Trait` and {class}`~extra_platforms.Group`
    classes:

    - `id`: Unique identifier
    - `name`: Human-readable name
    - `icon`: Visual representation
    - `symbol_id`: Uppercase version of ID for module-level constants
    - `detection_func_id`: Name of the `is_<id>()` detection function
    - `skip_decorator_id` and `unless_decorator_id`: Names of the Pytest
      decorators
    """

    id: str
    """Unique ID of the object."""

    name: str
    """User-friendly name of the object."""

    icon: str = field(repr=False, default="❓")
    """Icon of the object."""

    def __init_subclass__(cls, **metadata: str) -> None:
        """Set the `_ClassMetadata` of a subclass when it is defined.

        `type_id` defaults to the lowercased class name, `type_name` to the
        `type_id`, and the others derive from the `type_id`. A keyword argument of
        the class definition overrides any of them, and so does an attribute of
        the class body, which the keyword argument wins over.
        """
        super().__init_subclass__()

        derived_attrs = [attr for attr in vars(_ClassMetadata) if attr[0] != "_"]
        unexpected = sorted(metadata.keys() - set(derived_attrs))
        assert not unexpected, f"{cls.__name__} sets unknown metadata {unexpected}."
        explicit = {
            **{attr: vars(cls)[attr] for attr in derived_attrs if attr in vars(cls)},
            **metadata,
        }
        for attr, value in explicit.items():
            assert value, f"{cls.__name__} must define a non-empty {attr}."

        type_id = explicit.get("type_id", cls.__name__.lower())
        derived = {
            "type_id": type_id,
            "type_name": type_id,
            "data_module_id": f"{type_id}_data",
            "unknown_symbol": f"UNKNOWN_{type_id.upper()}",
            "all_group": f"ALL_{type_id.upper()}S",
            "doc_page": f"{type_id}s.md",
        }
        for attr, value in derived.items():
            setattr(cls, attr, explicit.get(attr, value))

    def __post_init__(self) -> None:
        """Validate the common fields, and install the lazy docstring on the class.

        Ensure the ID, name, and icon are not empty.
        """
        # Serve the docstring of each instance on first read: see _LazyDocstring.
        cls = type(self)
        class_doc = cls.__dict__.get("__doc__")
        if not isinstance(class_doc, _LazyDocstring):
            cls.__doc__ = _LazyDocstring(class_doc)  # type: ignore[assignment]

        assert self.id, f"{cls.__name__} ID cannot be empty."
        assert self.name, f"{cls.__name__} name cannot be empty."
        assert self.icon, f"{cls.__name__} icon cannot be empty."

    @cached_property
    def symbol_id(self) -> str:
        """Symbolic identifier.

        This is the variable name under which the instance can be accessed at the
        root of the `extra_platforms` module.

        Mainly useful for documentation generation.
        """
        return self.id.upper()

    @cached_property
    def detection_func_id(self) -> str:
        """ID of the detection function for this object.

        The detection function is expected to be named `is_<id>()` and available
        at the root of the `extra_platforms` module.
        """
        return f"is_{self.id}"

    @cached_property
    def skip_decorator_id(self) -> str:
        """ID of the Pytest skip decorator for this object.

        The decorator is expected to be named `@skip_<id>` and available from the
        `extra_platforms.pytest` module.
        """
        return f"skip_{self.id}"

    @cached_property
    def unless_decorator_id(self) -> str:
        """ID of the Pytest unless decorator for this object.

        The decorator is expected to be named `@unless_<id>` and available from the
        `extra_platforms.pytest` module.
        """
        return f"unless_{self.id}"

    def generate_docstring(self) -> str:
        """Generate the docstring of this predefined object.

        Combines the attribute docstring written under the object in its data
        module with the metadata lines of the object.
        """
        source = get_attribute_docstring(
            f"extra_platforms.{self.data_module_id}", self.symbol_id
        )
        lines = [*source.strip().splitlines(), ""] if source else []
        lines.extend(self._metadata_lines())
        return "\n".join(lines)

    def _metadata_lines(self) -> list[str]:
        """The metadata list closing the generated docstring, identity first.

        Subclasses extend it with their own fields.
        """
        return [
            f"- **ID**: ``{self.id}``",
            f"- **Name**: {self.name}",
            f"- **Icon**: {self.icon}",
        ]

    def _reference_lines(self) -> tuple[str, str]:
        """The metadata lines linking the detection function and Pytest decorators."""
        return (
            f"- **Detection function**: {{func}}`~{self.detection_func_id}`",
            (
                "- **Pytest decorators**: "
                f"{{deco}}`~pytest.{self.skip_decorator_id}` / "
                f"{{deco}}`~pytest.{self.unless_decorator_id}`"
            ),
        )


def _check_alternative_names(trait: Trait, kind: str, names: tuple[str, ...]) -> None:
    """Assert each of `names` is a lowercase alternative to the ID of `trait`.

    :param kind: What the names are, like `"alias"`, used in failure messages.
    """
    for name in names:
        assert name, f"{trait.id} {kind} cannot be empty."
        assert name == name.lower(), (
            f"{kind.capitalize()} {name!r} of {trait.id} must be lowercase."
        )
        assert name != trait.id, (
            f"{kind.capitalize()} {name!r} of {trait.id} is already its ID."
        )
    assert len(set(names)) == len(names), f"{trait.id} repeats an {kind}."


@dataclass(frozen=True)
class Trait(_Identifiable):
    """Base class for system traits like platforms and architectures.

    A trait is a distinguishing characteristic of the runtime environment that can
    be detected and identified.

    In addition to the common fields inherited from `_Identifiable`, each trait
    provides:

    - `url`: A link to official documentation or website for the trait.
    - `aliases`: Alternative IDs resolving to the trait.
    - `current`: A boolean indicating if the current environment matches this trait.
    - `info()`: A method returning a dictionary of gathered attributes about the trait.
    - `groups`: A set of {class}`~extra_platforms.Group` objects that include
      this trait as a member.
    """

    url: str = field(repr=False, default="")
    """URL to the trait's official website or documentation."""

    aliases: tuple[str, ...] = field(repr=False, default=())
    """Alternative IDs for this trait.

    Aliases are alternative identifiers that resolve to the same trait. When an
    alias is used, a warning is emitted to encourage using the canonical ID.

    ```{note}
    Aliases do not generate their own symbols, detection functions, or pytest
    decorators. Only the canonical `id` produces these artifacts.
    ```
    """

    def __post_init__(self) -> None:
        """Validate the trait fields.

        - Ensure the URL is not empty and starts with `https://`.
        - Validate aliases are lowercase, unique and distinct from the canonical ID.

        ```{hint}
        The docstring is not built here. For a predefined trait,
        `_LazyDocstring` generates it on the first read of `__doc__`, once
        every module is imported and the groups a trait belongs to are known.
        ```
        """
        super().__post_init__()

        cls_name = type(self).__name__
        assert self.url, f"{cls_name} URL cannot be empty."
        assert self.url.startswith("https://"), (
            f"{cls_name} URL must start with https://."
        )
        _check_alternative_names(self, "alias", self.aliases)

    def _metadata_lines(self) -> list[str]:
        """The metadata list closing the generated docstring of the trait."""
        aliases = ", ".join(f"``{alias}``" for alias in sorted(self.aliases))
        groups = [
            f"{{data}}`~{group.symbol_id}`" + (" ⬥" if group.canonical else "")
            for group in sorted(self.groups, key=attrgetter("id"))
        ]
        return [
            *super()._metadata_lines(),
            f"- **Aliases**: {aliases or '-'}",
            f"- **Reference**: <{self.url}>_",
            *self._reference_lines(),
            f"- **Groups** ({len(groups)}): {', '.join(groups)}",
        ]

    @cached_property
    def groups(self) -> frozenset[Group]:
        """Returns the set of groups this trait belongs to.

        :return: A {class}`frozenset` of {class}`~extra_platforms.Group` objects
            that contain this trait as a member.
        """
        # Avoid circular import.
        from .group_data import ALL_GROUPS

        return frozenset(group for group in ALL_GROUPS if self in group)

    @property
    def current(self) -> bool:
        """Returns whether the current environment matches this trait.

        Calls the detection function named by
        {attr}`~extra_platforms.Trait.detection_func_id`, which caches its own
        result. That function is looked up in the registry of the `detection`
        module, where tests replace it to simulate another environment.

        Raises {exc}`NotImplementedError` if a detection function cannot be found.

        ```{hint}
        This is a property to avoid calling all detection heuristics on
        {class}`~extra_platforms.Trait` object creation, which happens at
        module import time.
        ```
        """
        from .detection import _detection_registry

        try:
            detect = _detection_registry[self.detection_func_id]
        except KeyError:
            raise NotImplementedError(
                f"Detection function {self.detection_func_id}() is not implemented."
            ) from None
        return detect()

    def info(self) -> dict[str, Any]:
        """Returns all trait attributes that can be gathered.

        This default implementation returns the identity metadata common to all
        traits. Subclasses extend it with category-specific fields by merging
        ``super().info()`` into their own result.
        """
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
            "current": self.current,
        }


@dataclass(frozen=True)
class Architecture(Trait):
    """A CPU architecture identifies a [processor instruction set](https://en.wikipedia.org/wiki/Instruction_set_architecture).

    ```{todo}
    Extend our architecture metadata beyond basic ISA detection with
    [`archspec`](https://github.com/archspec/archspec), which provides a rich
    database of CPU microarchitectures (feature flags, compiler compatibility,
    family trees).
    ```
    """

    def info(self) -> dict[str, str | bool | None]:
        """Returns all architecture attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **super().info(),
            "machine": None,
            "processor": None,
        }
        if self.current:
            info["machine"] = platform.machine() or None
            info["processor"] = platform.processor() or None
        return info


@dataclass(frozen=True)
class Platform(Trait):
    """A platform identifies one or more operating systems.

    Distributions or systems that share the same characteristics share a platform.

    See the ``platform_data`` module for the granularity policy deciding when a
    distribution gets a dedicated platform, and when it is folded into an
    existing one.

    ```{todo}
    Detect the init system (systemd, upstart, sysvinit, openrc, runit, ...),
    another dimension of platform characterization. See
    [`python-distro/distro#142`](https://github.com/python-distro/distro/issues/142)
    for prior discussion on init system detection.
    ```
    """

    def info(self) -> dict[str, str | bool | dict[str, str | None] | None]:
        """Returns all platform attributes we can gather."""
        info: dict[str, str | bool | dict[str, str | None] | None] = {
            **super().info(),
            # Extra fields from distro.info().
            "distro_id": None,
            # Product release a version does not carry, like Windows "11".
            "release": None,
            "version": None,
            "version_parts": {"major": None, "minor": None, "build_number": None},
            "like": None,
            "codename": None,
        }
        if self.current:
            # Any platform shipping an os-release file reports it, the BSDs too.
            # Its ID is renamed so it does not clash with the trait's own ID.
            os_release = dict(linux_info())
            os_release["distro_id"] = os_release.pop("id")
            info = _recursive_update(info, _remove_blanks(os_release), strict=True)
            if self.id == "macos":
                info = _recursive_update(info, macos_info(), strict=True)
            elif self.id == "windows":
                info = _recursive_update(info, windows_info(), strict=True)
        return info


@dataclass(frozen=True)
class Shell(Trait):
    """A shell identifies a command-line interpreter.

    ```{seealso}
    Inspired by [UV's cross-platform shell detection](https://github.com/astral-sh/uv/pull/17870).
    ```
    """

    version_env_var: str | None = field(repr=False, default=None)
    """Environment variable set by the shell at startup (like ``BASH_VERSION``).

    A reliable signal that the shell is *currently running*, not just configured
    as the login shell in ``SHELL``. ``None`` for shells that do not set a
    dedicated startup variable (like Dash or Almquist Shell).
    """

    interpreter: str | None = field(repr=False, default=None)
    """Base name of the host interpreter for shells run as an interpreted script.

    Set for shells that are not standalone executables but launcher scripts run
    by an interpreter (like {data}`~extra_platforms.XONSH`, run by ``python``).
    The value is the interpreter's base name (``"python"``); detection tolerates
    a trailing version (``python3``, ``python3.11``). When set, the parent
    process tree is also scanned for an interpreter process whose arguments
    include a launcher file named after this shell's
    {attr}`~extra_platforms.Trait.id`, so the shell is detected even without its
    startup environment variable. ``None`` for standalone shells.
    """

    executables: tuple[str, ...] = field(repr=False, default=())
    """File names the shell's binary goes by, when they differ from its ID.

    Most shells answer to their {attr}`~extra_platforms.Trait.id` alone, so the
    field stays empty. {data}`~extra_platforms.POWERSHELL` ships as ``pwsh`` on
    every platform since ``6.0`` and as ``powershell_ise`` on Windows,
    {data}`~extra_platforms.NUSHELL` as ``nu``, and
    {data}`~extra_platforms.KSH` as ``ksh93`` on Fedora and illumos, where
    ``ksh`` links to it. Detection matches the resolved
    ``SHELL`` path and the parent process tree against
    {attr}`executable_names`, and so does
    {func}`~extra_platforms.shell_from_path`.
    """

    def __post_init__(self) -> None:
        """Validate the executables on top of the trait checks.

        Each executable must be lowercase, unique and distinct from the ID.
        """
        super().__post_init__()
        _check_alternative_names(self, "executable", self.executables)

    @cached_property
    def executable_names(self) -> frozenset[str]:
        """Every file name the shell's binary goes by.

        That is its {attr}`~extra_platforms.Trait.id` and its {attr}`executables`.
        """
        return frozenset((self.id, *self.executables))

    def info(self) -> dict[str, str | bool | None]:
        """Returns all shell attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **super().info(),
            "version": None,
            "path": None,
        }
        if self.current:
            if self.version_env_var:
                info["version"] = environ.get(self.version_env_var)
            # Prefer the actual running binary from the process tree over the
            # configured login shell in SHELL.
            from .detection import _shell_path

            info["path"] = _shell_path(self.executable_names)
        return info


@dataclass(frozen=True)
class Terminal(Trait):
    """A terminal identifies the application rendering the shell's output.

    ```{note}
    Shell and Terminal are orthogonal: any shell can run inside any terminal.
    Unlike shells, multiple terminals can be active simultaneously (like
    tmux inside Kitty).
    ```

    ```{seealso}
    Other tools that detect terminals for adaptation:

    - [`Starship`](https://starship.rs/) adapts prompt rendering based on terminal
    - [`crossterm`](https://github.com/crossterm-rs/crossterm) (Rust)
      negotiates terminal features
    - [`python-prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit)
      adapts to terminal capabilities
    - [`rich`](https://github.com/Textualize/rich) probes terminal
      features for rendering
    - [`termenv`](https://github.com/muesli/termenv) (Go) maintains
      terminal capability database
    ```
    """

    def info(self) -> dict[str, str | bool | None]:
        """Returns all terminal attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **super().info(),
            "version": None,
            "color_support": None,
        }
        if self.current:
            info["version"] = environ.get("TERM_PROGRAM_VERSION")
            info["color_support"] = environ.get("COLORTERM")
        return info


@dataclass(frozen=True)
class CI(Trait, type_name="CI system", all_group="ALL_CI", doc_page="ci.md"):
    """A CI/CD environment identifies a continuous integration platform.

    Its metadata spells the type name out, and keeps the more natural `ALL_CI`
    and `ci.md` instead of the derived `ALL_CIS` and `cis.md`.
    """


@dataclass(frozen=True)
class Agent(Trait):
    """An agent identifies an AI coding agent environment."""
