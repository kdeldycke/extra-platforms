# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Trait base class for architectures, platforms, shells, terminals, CI systems, agents, and more.

A trait represents a distinguishing characteristic of a runtime environment.
Each trait has a unique ID, a human-readable name, an icon, and the ability
to detect if it matches the current environment.

Data associated with traits can be aggressively cached and frozen, as they're only
computed based on environment-dependent values.
"""

from __future__ import annotations

import platform
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from os import environ
from typing import ClassVar

from ._docstrings import get_attribute_docstring
from ._utils import _recursive_update, _remove_blanks
from .platform_info import linux_info, macos_info, windows_info

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True)
class _Identifiable:
    """Base class for identifiable objects with common documentation fields.

    Provides the common fields and initialization logic shared by both
    :class:`~extra_platforms.Trait` and :class:`~extra_platforms.Group`
    classes:

    - ``id``: Unique identifier
    - ``name``: Human-readable name
    - ``icon``: Visual representation
    - ``symbol_id``: Uppercase version of ID for module-level constants
    - ``detection_func_id``: Name of the ``is_<id>()`` detection function

    Subclasses must define the class-level documentation metadata:

    - ``type_id``: Machine-readable type identifier (e.g., "architecture", "ci")
    - ``type_name``: Human-readable type name (e.g., "architecture", "CI system")

    The following are automatically derived from ``type_id`` via ``__init_subclass__``:

    - ``data_module_id``: Module name where instances are defined
    - ``unknown_symbol``: Symbol name for the unknown instance
    - ``all_group``: Symbol name for the group containing all instances
    - ``doc_page``: Documentation page filename
    """

    # Class-level documentation metadata (must be overridden by subclasses).
    type_id: ClassVar[str] = ""
    """Machine-readable type identifier used to derive module and symbol names."""

    type_name: ClassVar[str] = ""
    """Human-readable type name for documentation."""

    # Derived class-level attributes (set by __init_subclass__).
    data_module_id: ClassVar[str] = ""
    """The module name where instances of this type are defined."""

    unknown_symbol: ClassVar[str] = ""
    """The symbol name for the unknown instance of this type."""

    all_group: ClassVar[str] = ""
    """The symbol name for the group containing all instances of this type."""

    doc_page: ClassVar[str] = ""
    """The documentation page filename."""

    id: str
    """Unique ID of the object."""

    symbol_id: str = field(repr=False, init=False)
    """Symbolic identifier.

    This is the variable name under which the instance can be accessed at the
    root of the ``extra_platforms`` module.

    Mainly useful for documentation generation.
    """

    detection_func_id: str = field(repr=False, init=False)
    """ID of the detection function for this object.

    The detection function is expected to be named ``is_<id>()`` and available at the root
    of the ``extra_platforms`` module.
    """

    skip_decorator_id: str = field(repr=False, init=False)
    """ID of the Pytest skip decorator for this object.

    The decorator is expected to be named ``@skip_<id>`` and available from the
    ``extra_platforms.pytest`` module.
    """

    unless_decorator_id: str = field(repr=False, init=False)
    """ID of the Pytest unless decorator for this object.

    The decorator is expected to be named ``@unless_<id>`` and available from the
    ``extra_platforms.pytest`` module.
    """

    name: str
    """User-friendly name of the object."""

    icon: str = field(repr=False, default="❓")
    """Icon of the object."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Compute derived class attributes from class name when subclass is defined.

        Only sets attributes if they haven't been explicitly defined in the subclass.
        """
        super().__init_subclass__(**kwargs)

        # Derive type_id from class name if not explicitly set.
        if "type_id" in cls.__dict__:
            assert cls.type_id, f"{cls.__name__} must define a non-empty type_id."
        else:
            cls.type_id = cls.__name__.lower()

        # Derive type_name from type_id if not explicitly set.
        if "type_name" in cls.__dict__:
            assert cls.type_name, f"{cls.__name__} must define a non-empty type_name."
        else:
            cls.type_name = cls.type_id

        # Only set derived values if not explicitly defined in the subclass itself.
        if "data_module_id" not in cls.__dict__:
            cls.data_module_id = f"{cls.type_id}_data"

        if "unknown_symbol" not in cls.__dict__:
            cls.unknown_symbol = f"UNKNOWN_{cls.type_id.upper()}"

        if "all_group" not in cls.__dict__:
            cls.all_group = f"ALL_{cls.type_id.upper()}S"

        if "doc_page" not in cls.__dict__:
            cls.doc_page = f"{cls.type_id}s.md"

    def __post_init__(self) -> None:
        """Validate and normalize common fields.

        - Ensure the ID, name, and icon are not empty.
        - Set the symbolic ID.
        - Set the detection function ID.
        - Set the Pytest decorator IDs.
        """
        assert self.id, f"{self.__class__.__name__} ID cannot be empty."

        object.__setattr__(self, "symbol_id", self.id.upper())

        object.__setattr__(self, "detection_func_id", f"is_{self.id}")

        object.__setattr__(self, "skip_decorator_id", f"skip_{self.id}")
        object.__setattr__(self, "unless_decorator_id", f"unless_{self.id}")

        assert self.name, f"{self.__class__.__name__} name cannot be empty."

        assert self.icon, f"{self.__class__.__name__} icon cannot be empty."


@dataclass(frozen=True)
class Trait(_Identifiable, ABC):
    """Base class for system traits like platforms and architectures.

    A trait is a distinguishing characteristic of the runtime environment that can
    be detected and identified.

    Additionally of the common fields inherited from ``_Identifiable``, each trait provides:

    - ``url``: A link to official documentation or website for the trait.
    - ``current``: A boolean indicating if the current environment matches this trait.
    - ``info()``: A method returning a dictionary of gathered attributes about the trait.
    - ``groups``: A set of :class:`~extra_platforms.Group` objects that include this trait as a member.
    """

    url: str = field(repr=False, default="")
    """URL to the trait's official website or documentation."""

    aliases: frozenset[str] = field(repr=False, default_factory=frozenset)
    """Alternative IDs for this trait.

    Aliases are alternative identifiers that resolve to the same trait. When an
    alias is used, a warning is emitted to encourage using the canonical ID.

    .. note::
        Aliases do not generate their own symbols, detection functions, or pytest
        decorators. Only the canonical ``id`` produces these artifacts.
    """

    def __post_init__(self) -> None:
        """Validate and normalize trait fields.

        - Ensure the URL is not empty and starts with ``https://``.
        - Validate aliases are lowercase and distinct from the canonical ID.
        - Populate the docstring (deferred until after module initialization).

        .. hint::
            Docstring generation is deferred to avoid circular imports during module
            initialization. See _docstrings._initialize_all_docstrings().
        """
        super().__post_init__()

        assert self.url, f"{self.__class__.__name__} URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        # Validate aliases.
        for alias in self.aliases:
            assert alias, f"{self.__class__.__name__} alias cannot be empty."
            assert alias == alias.lower(), (
                f"Alias '{alias}' must be lowercase for {self.id}."
            )
            assert alias != self.id, f"Alias '{alias}' cannot be the same as ID."

    def generate_docstring(self) -> str:
        """Generate comprehensive docstring for this trait instance.

        Combines the attribute docstring from the source module with various metadata.
        """
        lines = []

        # Fetch attribute docstring from source module.
        source_docstring = get_attribute_docstring(
            f"extra_platforms.{self.data_module_id}", self.symbol_id
        )
        if source_docstring:
            lines.extend(source_docstring.strip().split("\n"))
            lines.append("")

        # Add metadata.
        lines.append(f"- **ID**: ``{self.id}``")
        if self.aliases:
            alias_list = ", ".join(f"``{a}``" for a in sorted(self.aliases))
        else:
            alias_list = "-"
        lines.append(f"- **Aliases**: {alias_list}")
        lines.append(f"- **Name**: {self.name}")
        lines.append(f"- **Icon**: {self.icon}")
        lines.append(f"- **Reference**: <{self.url}>_")
        lines.append(f"- **Detection function**: :func:`~{self.detection_func_id}`")
        lines.append(
            f"- **Pytest decorators**: :deco:`~pytest.{self.skip_decorator_id}` / "
            f":deco:`~pytest.{self.unless_decorator_id}`"
        )

        # Add list of groups this trait belongs to.
        group_links = [
            f":data:`~{group.symbol_id}`" + (" ⬥" if group.canonical else "")
            for group in sorted(self.groups, key=lambda g: g.id)
        ]
        lines.append(f"- **Groups** ({len(group_links)}): {', '.join(group_links)}")

        return "\n".join(lines)

    @cached_property
    def groups(self) -> frozenset:
        """Returns the set of groups this trait belongs to.

        Uses dynamic import to avoid circular dependency with ``group_data`` module.

        Returns:
            A :class:`frozenset` of :class:`~extra_platforms.Group` objects that contain this
            trait as a member.
        """
        # Avoid circular import by importing here.
        from .group_data import ALL_GROUPS

        return frozenset(group for group in ALL_GROUPS if self.id in group.member_ids)

    @cached_property
    def current(self) -> bool:
        """Returns whether the current environment matches this trait.

        The detection function is dynamically looked up based on the trait ID, and is
        expected to be found at the root of the ``extra_platforms`` module.

        Raises :exc:`NotImplementedError` if a detection function cannot be found.

        .. hint::
            This is a property to avoid calling all detection heuristics on
            :class:`~extra_platforms.Trait` object creation, which happens at module import time.
        """
        import extra_platforms

        func = getattr(extra_platforms, self.detection_func_id, None)
        if not func:
            raise NotImplementedError(
                f"Detection function {self.detection_func_id}() is not implemented."
            )
        return func()  # type: ignore[no-any-return]

    @abstractmethod
    def info(self) -> dict:
        """Returns all trait attributes that can be gathered.

        Returns a :class:`dict` of metadata. Subclasses should override this to include
        trait-specific information.
        """
        ...

    def _base_info(self) -> dict[str, str | bool | None]:
        """Returns the base info dictionary common to all traits."""
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
            "current": self.current,
        }


@dataclass(frozen=True)
class Architecture(Trait):
    """A CPU architecture identifies a `processor instruction set
    <https://en.wikipedia.org/wiki/Instruction_set_architecture>`_.
    """

    def info(self) -> dict[str, str | bool | None]:
        """Returns all architecture attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **self._base_info(),
            "machine": None,
            "processor": None,
        }
        if self.current:
            info["machine"] = platform.machine() or None
            info["processor"] = platform.processor() or None

        return info


@dataclass(frozen=True)
class Platform(Trait):
    """A platform can identify multiple distributions or OSes with the same
    characteristics.
    """

    def info(self) -> dict[str, str | bool | None | dict[str, str | None]]:
        """Returns all platform attributes we can gather."""
        info: dict[str, str | bool | None | dict[str, str | None]] = {
            **self._base_info(),
            # Extra fields from distro.info().
            "distro_id": None,
            "version": None,
            "version_parts": {"major": None, "minor": None, "build_number": None},
            "like": None,
            "codename": None,
        }
        if self.current:
            # Get Linux distribution info from os-release.
            distro_info = dict(linux_info())
            # Rename distro ID to avoid conflict with our own ID.
            distro_info["distro_id"] = distro_info.pop("id")
            info = _recursive_update(info, _remove_blanks(distro_info), strict=True)

            # Add extra macOS infos.
            if self.id == "macos":
                info = _recursive_update(info, macos_info(), strict=True)
            # Add extra Windows infos.
            elif self.id == "windows":
                info = _recursive_update(info, windows_info(), strict=True)

        return info


@dataclass(frozen=True)
class Shell(Trait):
    """A shell identifies a command-line interpreter.

    .. seealso::
        Inspired by `UV's cross-platform shell detection
        <https://github.com/astral-sh/uv/pull/17870>`_.
    """

    def info(self) -> dict[str, str | bool | None]:
        """Returns all shell attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **self._base_info(),
            "version": None,
            "path": None,
        }
        if self.current:
            info["version"] = self._detect_version()
            info["path"] = environ.get("SHELL")
        return info

    def _detect_version(self) -> str | None:
        """Return the shell version from environment if available."""
        version_vars = {
            "bash": "BASH_VERSION",
            "zsh": "ZSH_VERSION",
            "fish": "FISH_VERSION",
            "ksh": "KSH_VERSION",
            "nushell": "NU_VERSION",
            "xonsh": "XONSH_VERSION",
        }
        env_var = version_vars.get(self.id)
        if env_var:
            return environ.get(env_var)
        return None


@dataclass(frozen=True)
class Terminal(Trait):
    """A terminal identifies the application rendering the shell's output.

    .. note::
        Shell and Terminal are orthogonal: any shell can run inside any terminal.
        Unlike shells, multiple terminals can be active simultaneously (e.g.,
        tmux inside Kitty).

    .. seealso::
        Other tools that detect terminals for adaptation:

        - `Starship <https://starship.rs/>`_ adapts prompt rendering based on terminal
        - `crossterm <https://github.com/crossterm-rs/crossterm>`_ (Rust) negotiates terminal features
        - `python-prompt-toolkit <https://github.com/prompt-toolkit/python-prompt-toolkit>`_ adapts to terminal capabilities
        - `rich <https://github.com/Textualize/rich>`_ probes terminal features for rendering
        - `termenv <https://github.com/muesli/termenv>`_ (Go) maintains terminal capability database
    """

    def info(self) -> dict[str, str | bool | None]:
        """Returns all terminal attributes we can gather."""
        info: dict[str, str | bool | None] = {
            **self._base_info(),
            "version": None,
            "color_support": None,
        }
        if self.current:
            info["version"] = environ.get("TERM_PROGRAM_VERSION")
            info["color_support"] = environ.get("COLORTERM")
        return info


@dataclass(frozen=True)
class CI(Trait):
    """A CI/CD environment identifies a continuous integration platform."""

    type_name = "CI system"
    """Override the default ``ci`` type name."""

    all_group = "ALL_CI"
    """Override the default ``ALL_CIS`` name with a more natural ``ALL_CI``."""

    doc_page = "ci.md"
    """Override the default ``cis.md`` filename."""

    def __post_init__(self) -> None:
        """Tweak CI docstring."""
        super().__post_init__()
        object.__setattr__(self, "__doc__", f"Identify {self.name} environment.")

    def info(self) -> dict[str, str | bool | None]:
        """Returns all CI attributes we can gather."""
        return {**self._base_info()}


@dataclass(frozen=True)
class Agent(Trait):
    """An agent identifies an AI coding agent environment."""

    type_name = "agent"

    all_group = "ALL_AGENTS"

    def __post_init__(self) -> None:
        """Tweak agent docstring."""
        super().__post_init__()
        object.__setattr__(self, "__doc__", f"Identify {self.name} environment.")

    def info(self) -> dict[str, str | bool | None]:
        """Returns all agent attributes we can gather."""
        return {**self._base_info()}


@lru_cache(maxsize=128)
def _resolve_alias(id_: str) -> str:
    """Resolve an alias to its canonical ID, emitting a warning if an alias is used.

    Results are cached, so the warning is only emitted once per alias.

    Args:
        id_: The ID to resolve (already lowercased).

    Returns:
        The canonical ID if ``id_`` is an alias, otherwise ``id_`` unchanged.
    """
    # Avoid circular import.
    from .group_data import ALL_TRAITS

    for trait in ALL_TRAITS:
        if id_ in trait.aliases:
            warnings.warn(
                f"'{id_}' is an alias for '{trait.id}'. "
                f"Use the canonical ID '{trait.id}' instead.",
                UserWarning,
                stacklevel=4,
            )
            return trait.id
    return id_
