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
"""CPU architectures.

Everything here can be aggressively cached and frozen, as it's only compute
architecture-dependent values.
"""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from functools import cached_property

from . import detection


@dataclass(frozen=True)
class Architecture:
    """A CPU architecture identifies a `processor instruction set
    <https://en.wikipedia.org/wiki/Instruction_set_architecture>`_.

    It has a unique ID, a human-readable name, and boolean to flag current architecture.
    """

    id: str
    """Unique ID of the architecture."""

    name: str
    """User-friendly name of the architecture."""

    icon: str = field(repr=False, default="▣")
    """Icon of the architecture."""

    url: str = field(repr=False, default="")
    """URL to the architecture's documentation or Wikipedia page."""

    def __post_init__(self):
        """Validate and normalize architecture fields:

        - Ensure the architecture ID, name, icon and URL are not empty.
        - Ensure the URL starts with ``https://``.
        - Populate the docstring.
        """
        assert self.id, "Architecture ID cannot be empty."
        assert self.name, "Architecture name cannot be empty."
        assert self.icon, "Architecture icon cannot be empty."
        assert self.url, "Architecture URL cannot be empty."
        assert self.url.startswith("https://"), "URL must start with https://."

        object.__setattr__(self, "__doc__", f"Identify {self.name} architecture.")

    @cached_property
    def short_desc(self) -> str:
        """Returns a short description of the architecture.

        Mainly used to produce docstrings for function dynamically generated for each
        group.
        """
        return self.name

    @cached_property
    def current(self) -> bool:
        """Returns whether the current architecture is this one.

        This is a property to avoid calling all architecture detection heuristics on
        ``Architecture`` objects creation, which happens at module import time.
        """
        return getattr(detection, f"is_{self.id}")()  # type: ignore[no-any-return]

    def info(self) -> dict[str, str | bool | None]:
        """Returns all architecture attributes we can gather."""
        info: dict[str, str | bool | None] = {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
            "current": self.current,
            "machine": None,
            "processor": None,
        }
        if self.current:
            info["machine"] = platform.machine() or None
            info["processor"] = platform.processor() or None

        return info
