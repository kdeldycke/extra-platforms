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

import sys
import warnings
from collections.abc import Callable
from functools import wraps
from types import ModuleType
from typing import Any

# Dynamically generated detection functions are imported lazily to avoid
# circular imports during module initialization.
import extra_platforms as _ep

from . import (
    ALL_ARM,
    ALL_MIPS,
    ALL_PLATFORMS,
    ALL_SPARC,
    ALL_TRAIT_IDS,
    ALL_WINDOWS,
    OTHER_POSIX,
    UNKNOWN_PLATFORM,
    current_platform,
    current_traits,
    traits_from_ids,
)
from ._utils import _recursive_update, _remove_blanks
from .trait import Platform


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
    """Convenience factory returning a deprecated proxy for ``target``.

    Keeps call-sites concise and avoids repeating the proxy class.
    """
    return _DeprecatedProxy(target, name, replacement)


def _make_deprecated_callable(
    name: str, replacement: str, func: Callable[..., Any] | str
) -> Callable[..., Any]:
    """Return a function wrapping ``func`` that emits a deprecation warning.

    The returned callable preserves the wrapped function metadata.

    ``func`` can be either a callable or a string. If it's a string, it's treated
    as the name of a function to look up lazily in ``extra_platforms`` module.
    This allows wrapping dynamically generated functions that don't exist yet at
    module load time.
    """

    @wraps(func) if callable(func) else (lambda f: f)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        _warn_deprecated(name, replacement)
        target = func if callable(func) else getattr(_ep, func)
        return target(*args, **kwargs)

    return _wrapper


# ================================================================
# Data aliases
# ================================================================


ALL_PLATFORM_IDS = _make_deprecated_proxy(
    ALL_TRAIT_IDS, "ALL_PLATFORM_IDS", "ALL_TRAIT_IDS"
)
"""
Alias `ALL_PLATFORM_IDS` → :data:`~extra_platforms.ALL_TRAIT_IDS`.

.. deprecated:: 6.0.0
   Use :data:`~extra_platforms.ALL_TRAIT_IDS` instead.
"""


ALL_PLATFORMS_WITHOUT_CI = _make_deprecated_proxy(
    ALL_PLATFORMS, "ALL_PLATFORMS_WITHOUT_CI", "ALL_PLATFORMS"
)
"""
Alias `ALL_PLATFORMS_WITHOUT_CI` → :data:`~extra_platforms.ALL_PLATFORMS`.

.. deprecated:: 6.0.0
   Use :data:`~extra_platforms.ALL_PLATFORMS` instead.
"""


UNKNOWN_LINUX = _make_deprecated_proxy(
    UNKNOWN_PLATFORM, "UNKNOWN_LINUX", "UNKNOWN_PLATFORM"
)
"""
Alias `UNKNOWN_LINUX` → :data:`~extra_platforms.UNKNOWN_PLATFORM`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.UNKNOWN_PLATFORM` instead.
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
Alias `current_os()` → :func:`~extra_platforms.current_platform`.

.. deprecated:: 6.0.0
   Use :func:`~extra_platforms.current_platform` instead.
"""


def _current_platforms_impl() -> tuple[Platform, ...]:
    return tuple(t for t in current_traits() if isinstance(t, Platform))


current_platforms = _make_deprecated_callable(
    "current_platforms()", "current_traits()", _current_platforms_impl
)
"""
Alias `current_platforms()` → :func:`~extra_platforms.current_traits`.

.. deprecated:: 6.0.0
   Use :func:`~extra_platforms.current_traits` instead.
"""


is_unknown_linux = _make_deprecated_callable(
    "is_unknown_linux()",
    "is_unknown_platform()",
    "is_unknown_platform",
)
"""
Alias `is_unknown_linux()` → :func:`~extra_platforms.is_unknown_platform`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_unknown_platform` instead.
"""


# ================================================================
# Group membership check functions
# ================================================================


is_all_platforms_without_ci = _make_deprecated_callable(
    "is_all_platforms_without_ci()",
    "is_any_platform()",
    "is_any_platform",
)
"""
Alias `is_all_platforms_without_ci()` → :func:`~extra_platforms.is_any_platform`.

.. deprecated:: 6.0.0
   Use :func:`~extra_platforms.is_any_platform` instead.
"""


is_ci = _make_deprecated_callable("is_ci()", "is_any_ci()", "is_any_ci")
"""
Alias `is_ci()` → :func:`~extra_platforms.is_any_ci`.

.. deprecated:: 6.0.0
   Use :func:`~extra_platforms.is_any_ci` instead.
"""


is_all_architectures = _make_deprecated_callable(
    "is_all_architectures()", "is_any_architecture()", "is_any_architecture"
)
"""
Alias `is_all_architectures()` → :func:`~extra_platforms.is_any_architecture`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_any_architecture` instead.
"""


is_all_platforms = _make_deprecated_callable(
    "is_all_platforms()", "is_any_platform()", "is_any_platform"
)
"""
Alias `is_all_platforms()` → :func:`~extra_platforms.is_any_platform`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_any_platform` instead.
"""


is_all_ci = _make_deprecated_callable("is_all_ci()", "is_any_ci()", "is_any_ci")
"""
Alias `is_all_ci()` → :func:`~extra_platforms.is_any_ci`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_any_ci` instead.
"""


is_all_traits = _make_deprecated_callable(
    "is_all_traits()", "is_any_trait()", "is_any_trait"
)
"""
Alias `is_all_traits()` → :func:`~extra_platforms.is_any_trait`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_any_trait` instead.
"""


is_other_unix = _make_deprecated_callable(
    "is_other_unix()", "is_other_posix()", "is_other_posix"
)
"""
Alias `is_other_unix()` → :func:`~extra_platforms.is_other_posix`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_other_posix` instead.
"""


is_bsd_without_macos = _make_deprecated_callable(
    "is_bsd_without_macos()", "is_bsd_not_macos()", "is_bsd_not_macos"
)
"""
Alias `is_bsd_without_macos()` → :func:`~extra_platforms.is_bsd_not_macos`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_bsd_not_macos` instead.
"""


is_unix_without_macos = _make_deprecated_callable(
    "is_unix_without_macos()", "is_unix_not_macos()", "is_unix_not_macos"
)
"""
Alias `is_unix_without_macos()` → :func:`~extra_platforms.is_unix_not_macos`.

.. deprecated:: 7.0.0
   Use :func:`~extra_platforms.is_unix_not_macos` instead.
"""


# ================================================================
# Deprecated group symbols
# ================================================================


ANY_ARM = _make_deprecated_proxy(ALL_ARM, "ANY_ARM", "ALL_ARM")
"""
Alias `ANY_ARM` → :data:`~extra_platforms.ALL_ARM`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.ALL_ARM` instead.
"""


ANY_MIPS = _make_deprecated_proxy(ALL_MIPS, "ANY_MIPS", "ALL_MIPS")
"""
Alias `ANY_MIPS` → :data:`~extra_platforms.ALL_MIPS`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.ALL_MIPS` instead.
"""


ANY_SPARC = _make_deprecated_proxy(ALL_SPARC, "ANY_SPARC", "ALL_SPARC")
"""
Alias `ANY_SPARC` → :data:`~extra_platforms.ALL_SPARC`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.ALL_SPARC` instead.
"""


ANY_WINDOWS = _make_deprecated_proxy(ALL_WINDOWS, "ANY_WINDOWS", "ALL_WINDOWS")
"""
Alias `ANY_WINDOWS` → :data:`~extra_platforms.ALL_WINDOWS`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.ALL_WINDOWS` instead.
"""


OTHER_UNIX = _make_deprecated_proxy(OTHER_POSIX, "OTHER_UNIX", "OTHER_POSIX")
"""
Alias `OTHER_UNIX` → :data:`~extra_platforms.OTHER_POSIX`.

.. deprecated:: 7.0.0
   Use :data:`~extra_platforms.OTHER_POSIX` instead.
"""


# ================================================================
# Trait utilities
# ================================================================


platforms_from_ids = _make_deprecated_callable(
    "platforms_from_ids", "traits_from_ids", traits_from_ids
)
"""
Alias `platforms_from_ids` → :func:`~extra_platforms.traits_from_ids`.

.. deprecated:: 6.0.0
   Use :func:`~extra_platforms.traits_from_ids` instead.
"""


# ================================================================
# Deprecated module: extra_platforms.platform
# ================================================================

# Simulate the deprecated `extra_platforms.platform` module by injecting a fake
# module into sys.modules. This allows `from extra_platforms.platform import Platform`
# to work while issuing a deprecation warning, without needing a separate file.


class _DeprecatedPlatformModule(ModuleType):
    """A fake module that warns on attribute access.

    .. deprecated:: 7.0.0
       The ``extra_platforms.platform`` module is deprecated.
       Import from ``extra_platforms.trait`` instead.
    """

    def __init__(self):
        super().__init__("extra_platforms.platform")
        self.__doc__ = (
            "Backward-compatible module for deprecated imports.\n\n"
            ".. deprecated:: 7.0.0\n"
            "    This module is deprecated. Import from ``extra_platforms.trait``"
            " instead."
        )
        self.__file__ = __file__
        self.__all__ = ["Platform", "_recursive_update", "_remove_blanks"]
        # Store actual values without triggering __setattr__ warning.
        object.__setattr__(self, "_Platform", Platform)
        object.__setattr__(self, "_recursive_update", _recursive_update)
        object.__setattr__(self, "_remove_blanks", _remove_blanks)

    def __getattr__(self, name: str):
        warnings.warn(
            "The 'extra_platforms.platform' module is deprecated. "
            "Import from 'extra_platforms.trait' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if name == "Platform":
            return self._Platform
        if name == "_recursive_update":
            return self._recursive_update
        if name == "_remove_blanks":
            return self._remove_blanks
        raise AttributeError(
            f"module 'extra_platforms.platform' has no attribute {name!r}"
        )


# Register the fake module in sys.modules.
sys.modules["extra_platforms.platform"] = _DeprecatedPlatformModule()
