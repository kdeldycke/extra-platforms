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
"""Trait base class for architectures, platforms, CI systems, and more.

A trait represents a distinguishing characteristic of a runtime environment.
Each trait has a unique ID, a human-readable name, an icon, and the ability
to detect if it matches the current environment.

Data associated with traits can be aggressively cached and frozen, as they're only
computed based on environment-dependent values.
"""

from __future__ import annotations

import platform
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar

import distro

import extra_platforms
from extra_platforms._utils import _recursive_update, _remove_blanks

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True)
class _Identifiable:
    """Base class for identifiable objects with common documentation fields.

    Provides the common fields and initialization logic shared by both ``Trait``
    and ``Group`` classes:

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
    - ``groups``: A set of ``Group`` objects that include this trait as a member.
    """

    url: str = field(repr=False, default="")
    """URL to the trait's official website or documentation."""

    def __post_init__(self) -> None:
        """Validate and normalize trait fields.

        - Ensure the URL is not empty and starts with ``https://``.
        - Populate the docstring.
        """
        super().__post_init__()

        assert self.url, f"{self.__class__.__name__} URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        # Generate docstring using type_name for context (e.g., "Predefined ARM64
        # architecture.").
        object.__setattr__(self, "__doc__", f"Predefined {self.name} {self.type_name}.")

    @cached_property
    def groups(self) -> frozenset:
        """Returns the set of groups this trait belongs to.

        Uses dynamic import to avoid circular dependency with group_data module.

        Returns:
            A frozenset of Group objects that contain this trait as a member.
        """
        # Avoid circular import by importing here.
        from .group_data import ALL_GROUPS

        return frozenset(group for group in ALL_GROUPS if self.id in group.member_ids)

    @cached_property
    def current(self) -> bool:
        """Returns whether the current environment matches this trait.

        The detection function is dynamically looked up based on the trait ID, and is
        expected to be found at the root of the ``extra_platforms`` module.

        Raises ``NotImplementedError`` if a detection function cannot be found.

        .. hint::
            This is a property to avoid calling all detection heuristics on
            ``Trait`` objects creation, which happens at module import time.
        """
        func = getattr(extra_platforms, self.detection_func_id, None)
        if not func:
            raise NotImplementedError(
                f"Detection function {self.detection_func_id}() is not implemented."
            )
        return func()  # type: ignore[no-any-return]

    @abstractmethod
    def info(self) -> dict:
        """Returns all trait attributes that can be gathered.

        Subclasses should override this to include trait-specific information.
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
            # Get extra Linux distribution info from distro.
            distro_info = dict(distro.info())
            # Rename distro ID to avoid conflict with our own ID.
            distro_info["distro_id"] = distro_info.pop("id")
            info = _recursive_update(info, _remove_blanks(distro_info), strict=True)

            # Add extra macOS infos.
            if self.id == "macos":
                info = _recursive_update(info, self._macos_infos(), strict=True)
            # Add extra Windows infos.
            elif self.id == "windows":
                info = _recursive_update(info, self._windows_infos(), strict=True)

        return info

    _MACOS_CODENAMES = {
        ("10", "0"): "Cheetah",
        ("10", "1"): "Puma",
        ("10", "2"): "Jaguar",
        ("10", "3"): "Panther",
        ("10", "4"): "Tiger",
        ("10", "5"): "Leopard",
        ("10", "6"): "Snow Leopard",
        ("10", "7"): "Lion",
        ("10", "8"): "Mountain Lion",
        ("10", "9"): "Mavericks",
        ("10", "10"): "Yosemite",
        ("10", "11"): "El Capitan",
        ("10", "12"): "Sierra",
        ("10", "13"): "High Sierra",
        ("10", "14"): "Mojave",
        ("10", "15"): "Catalina",
        ("11", None): "Big Sur",
        ("12", None): "Monterey",
        ("13", None): "Ventura",
        ("14", None): "Sonoma",
        ("15", None): "Sequoia",
        ("26", None): "Tahoe",
    }
    """Maps macOS ``(major, minor)`` version parts to release code name.

    See:

    - https://en.wikipedia.org/wiki/Template:MacOS_versions
    - https://docs.python.org/3/library/platform.html#platform.mac_ver
    """

    @classmethod
    def _get_macos_codename(
        cls, major: str | None = None, minor: str | None = None
    ) -> str:
        matches = set()
        for (major_key, minor_key), codename in cls._MACOS_CODENAMES.items():
            if minor_key is not None and minor_key != minor:
                continue
            if major_key == major:
                matches.add(codename)
        if not matches:
            raise ValueError(f"No macOS codename match version ({major!r}, {minor!r})")
        if len(matches) != 1:
            raise ValueError(
                f"Version {major}.{minor} match multiple codenames: {matches!r}"
            )
        return matches.pop()

    @classmethod
    def _macos_infos(cls) -> dict[str, Any]:
        """Fetch extra macOS infos.

        Returns the same dict structure as ``distro.info()``.
        """
        release, _versioninfo, _machine = platform.mac_ver()
        parts = dict(zip(("major", "minor", "build_number"), release.split(".", 2)))
        major = parts.get("major")
        minor = parts.get("minor")
        build_number = parts.get("build_number")
        return {
            "version": release,
            "version_parts": {
                "major": major,
                "minor": minor,
                "build_number": build_number,
            },
            "codename": cls._get_macos_codename(major, minor),
        }

    @classmethod
    def _windows_infos(cls) -> dict[str, Any]:
        """Fetch extra Windows infos.

        Returns the same dict structure as ``distro.info()``.

        .. todo:
            Get even more details for windows version? See inspirations from:
            https://github.com/saltstack/salt/blob/246d066/salt/grains/core.py#L1432-L1488
        """
        release, _version, _csd, _ptype = platform.win32_ver()
        parts = dict(zip(("major", "minor", "build_number"), release.split(".", 2)))
        major = parts.get("major")
        minor = parts.get("minor")
        build_number = parts.get("build_number")
        return {
            "version": release,
            "version_parts": {
                "major": major,
                "minor": minor,
                "build_number": build_number,
            },
            "codename": " ".join((release, platform.win32_edition())),
        }


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
