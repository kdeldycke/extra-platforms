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
"""Backward-compatible deprecated aliases."""

from __future__ import annotations

import warnings
from functools import wraps
from typing import TYPE_CHECKING, cast

from . import (
    ALL_PLATFORMS,
    ALL_TRAIT_IDS,
    UNKNOWN_PLATFORM,
    current_platform,
    current_traits,
    is_unknown_platform,
    traits_from_ids,
)
from .trait import _recursive_update as _trait_recursive_update
from .trait import _remove_blanks as _trait_remove_blanks

if TYPE_CHECKING:
    from .platform import Platform


def _get_dynamic_functions():
    """Lazy import of dynamically-generated group membership functions.

    These functions are generated at module initialization time, so we need
    to import them after the module is fully loaded.
    """
    from . import is_all_ci as _is_all_ci
    from . import is_all_platforms as _is_all_platforms

    return _is_all_ci, _is_all_platforms


def _warn_deprecated(name: str, replacement: str) -> None:
    """Issue a deprecation warning for a name pointing to a replacement.

    Args:
        name: Deprecated name.
        replacement: Suggested replacement.
    """
    warnings.warn(
        f"{name} is deprecated, use {replacement} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class _DeprecatedProxy:
    """Generic deprecated proxy that delegates to a target and warns on use.

    This proxy attempts to be transparent: attribute access, iteration,
    membership, length, item access and call are delegated to the underlying
    target after emitting a deprecation warning.
    """

    def __init__(self, target, name: str, replacement: str):
        self._target = target
        self._name = name
        self._replacement = replacement

    def _warn(self) -> None:
        _warn_deprecated(self._name, self._replacement)

    def __getattr__(self, attr):
        self._warn()
        return getattr(self._target, attr)

    def __iter__(self):
        self._warn()
        return iter(self._target)

    def __len__(self):
        self._warn()
        return len(self._target)

    def __contains__(self, item):
        self._warn()
        return item in self._target

    def __call__(self, *args, **kwargs):
        self._warn()
        return self._target(*args, **kwargs)

    def __getitem__(self, item):
        self._warn()
        return self._target[item]

    def __repr__(self):
        return repr(self._target)


def _make_deprecated_proxy(target, name: str, replacement: str):
    """Convenience factory returning a deprecated proxy for `target`.

    Keeps call-sites concise and avoids repeating the proxy class.
    """
    return _DeprecatedProxy(target, name, replacement)


def _make_deprecated_callable(name: str, replacement: str, func):
    """Return a function wrapping `func` that emits a deprecation warning.

    The returned callable preserves the wrapped function metadata.
    """

    @wraps(func)
    def _wrapper(*args, **kwargs):
        _warn_deprecated(name, replacement)
        return func(*args, **kwargs)

    return _wrapper


# ================================================================
# Data aliases
# ================================================================


ALL_PLATFORM_IDS = _make_deprecated_proxy(
    ALL_TRAIT_IDS, "ALL_PLATFORM_IDS", "ALL_TRAIT_IDS"
)
"""
Alias `ALL_PLATFORM_IDS` → `ALL_TRAIT_IDS`.

.. deprecated:: 6.0.0
   Use `ALL_TRAIT_IDS` instead.
"""


ALL_PLATFORMS_WITHOUT_CI = _make_deprecated_proxy(
    ALL_PLATFORMS, "ALL_PLATFORMS_WITHOUT_CI", "ALL_PLATFORMS"
)
"""
Alias `ALL_PLATFORMS_WITHOUT_CI` → `ALL_PLATFORMS`.

.. deprecated:: 6.0.0
   Use `ALL_PLATFORMS` instead.
"""


UNKNOWN_LINUX = _make_deprecated_proxy(
    UNKNOWN_PLATFORM, "UNKNOWN_LINUX", "UNKNOWN_PLATFORM"
)
"""
Alias `UNKNOWN_LINUX` → `UNKNOWN_PLATFORM`.

.. deprecated:: 7.0.0
   Use `UNKNOWN_PLATFORM` instead.
"""


# ================================================================
# Platform and trait detection functions
# ================================================================


current_os = _make_deprecated_callable(
    "current_os()",
    "current_platform()",
    current_platform,  # type: ignore[has-type]
)
"""
Alias `current_os()` → `current_platform()`.

.. deprecated:: 6.0.0
   Use `current_platform()` instead.
"""


def _current_platforms_impl() -> tuple[Platform, ...]:
    # Import lazily to avoid circular import when this module is imported
    # from the package top-level `__init__.py`.
    from .platform import Platform

    return tuple(t for t in current_traits() if isinstance(t, Platform))


current_platforms = _make_deprecated_callable(
    "current_platforms()", "current_traits()", _current_platforms_impl
)
"""
Alias `current_platforms()` → `current_traits()`.

.. deprecated:: 6.0.0
   Use `current_traits()` instead.
"""


is_unknown_linux = _make_deprecated_callable(
    "is_unknown_linux()", "is_unknown_platform()", is_unknown_platform
)
"""
Alias `is_unknown_linux()` → `is_unknown_platform()`.

.. deprecated:: 7.0.0
   Use `is_unknown_platform()` instead.
"""


# ================================================================
# Group membership check functions
# ================================================================


def _is_all_platforms_without_ci_impl() -> bool:
    _, is_all_platforms_func = _get_dynamic_functions()
    return cast(bool, is_all_platforms_func())


is_all_platforms_without_ci = _make_deprecated_callable(
    "is_all_platforms_without_ci()",
    "is_all_platforms()",
    _is_all_platforms_without_ci_impl,
)
"""
Alias `is_all_platforms_without_ci()` → `is_all_platforms()`.

.. deprecated:: 6.0.0
   Use `is_all_platforms()` instead.
"""


def _is_ci_impl() -> bool:
    is_all_ci_func, _ = _get_dynamic_functions()
    return cast(bool, is_all_ci_func())


is_ci = _make_deprecated_callable("is_ci()", "is_all_ci()", _is_ci_impl)
"""
Alias `is_ci()` → `is_all_ci()`.

.. deprecated:: 6.0.0
   Use `is_all_ci()` instead.
"""


# ================================================================
# Trait utilities
# ================================================================


platforms_from_ids = _make_deprecated_callable(
    "platforms_from_ids", "traits_from_ids", traits_from_ids
)
"""
Alias `platforms_from_ids` → `traits_from_ids`.

.. deprecated:: 6.0.0
   Use `traits_from_ids` instead.
"""


# ================================================================
# Internal utility aliases (for backward compatibility)
# ================================================================


_recursive_update = _make_deprecated_callable(
    "_recursive_update",
    "extra_platforms.trait._recursive_update",
    _trait_recursive_update,
)
"""
Alias for backward compatibility.

.. deprecated:: 7.0.0
   Use ``extra_platforms.trait._recursive_update`` instead.
"""


_remove_blanks = _make_deprecated_callable(
    "_remove_blanks",
    "extra_platforms.trait._remove_blanks",
    _trait_remove_blanks,
)
"""
Alias for backward compatibility.

.. deprecated:: 7.0.0
   Use ``extra_platforms.trait._remove_blanks`` instead.
"""
