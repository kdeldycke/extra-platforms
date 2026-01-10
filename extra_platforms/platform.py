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
"""Backward-compatible module for deprecated imports.

.. deprecated:: 6.0.0
   This module is deprecated. Import from ``extra_platforms.trait`` instead.
"""

from __future__ import annotations

# Re-export deprecated utility functions.
# These are wrapped with deprecation warnings in _deprecated.py.
from ._deprecated import _recursive_update, _remove_blanks

# Re-export Platform class from trait module for backward compatibility.
from .trait import Platform

__all__ = [
    "Platform",
    "_recursive_update",
    "_remove_blanks",
]
