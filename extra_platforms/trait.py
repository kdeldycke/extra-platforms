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
"""Trait base class for platforms, architectures, and CI systems.

A trait represents a distinguishing characteristic of a runtime environment.
Each trait has a unique ID, a human-readable name, an icon, and the ability
to detect if it matches the current environment.

Everything here can be aggressively cached and frozen, as traits only compute
environment-dependent values.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property

from . import detection


@dataclass(frozen=True)
class Trait(ABC):
    """Base class for system traits like platforms and architectures.

    A trait is a distinguishing characteristic of the runtime environment that can
    be detected and identified. Examples include:

    - Operating systems (macOS, Linux, Windows)
    - CPU architectures (x86_64, ARM64)
    - CI/CD environments (GitHub Actions, GitLab CI)

    Each trait has:

    - A unique ID for programmatic use
    - A human-readable name
    - An icon for visual representation
    - A URL to official documentation
    - A ``current`` property that detects if this trait matches the runtime
    """

    id: str
    """Unique ID of the trait."""

    name: str
    """User-friendly name of the trait."""

    icon: str = field(repr=False, default="❓")
    """Icon of the trait."""

    url: str = field(repr=False, default="")
    """URL to the trait's official website or documentation."""

    def __post_init__(self) -> None:
        """Validate and normalize trait fields.

        - Ensure the trait ID, name, icon and URL are not empty.
        - Ensure the URL starts with ``https://``.
        - Populate the docstring.
        """
        assert self.id, f"{self.__class__.__name__} ID cannot be empty."
        assert self.name, f"{self.__class__.__name__} name cannot be empty."
        assert self.icon, f"{self.__class__.__name__} icon cannot be empty."
        assert self.url, f"{self.__class__.__name__} URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        object.__setattr__(self, "__doc__", f"Identify {self.name}.")

    @cached_property
    def short_desc(self) -> str:
        """Returns a short description of the trait.

        Mainly used to produce docstrings for functions dynamically generated for each
        group.
        """
        return self.name

    @cached_property
    def current(self) -> bool:
        """Returns whether the current environment matches this trait.

        This is a property to avoid calling all detection heuristics on
        ``Trait`` objects creation, which happens at module import time.
        """
        return getattr(detection, f"is_{self.id}")()  # type: ignore[no-any-return]

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
