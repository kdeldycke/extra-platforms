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
"""CI/CD environments.

Everything here can be aggressively cached and frozen, as it's only compute
CI-dependent values.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .trait import Trait


@dataclass(frozen=True)
class CI(Trait):
    """A CI/CD environment identifies a continuous integration platform.

    It has a unique ID, a human-readable name, and boolean to flag current CI.
    """

    icon: str = field(repr=False, default="♲")
    """Icon of the CI environment."""

    def __post_init__(self) -> None:
        """Validate and normalize CI fields."""
        super().__post_init__()
        # Customize the docstring for CI environments.
        object.__setattr__(self, "__doc__", f"Identify {self.name} CI environment.")

    def info(self) -> dict[str, str | bool | None]:
        """Returns all CI attributes we can gather."""
        return {
            **self._base_info(),
        }
