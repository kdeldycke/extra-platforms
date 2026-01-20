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
from textwrap import dedent
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
    Platform,
    current_platform,
    current_traits,
    traits_from_ids,
)
from ._utils import _recursive_update, _remove_blanks


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


def _make_deprecated_proxy(target, name: str, replacement: str, docstring: str = ""):
    """Convenience factory returning a deprecated proxy for ``target``.

    Keeps call-sites concise and avoids repeating the proxy class.

    Args:
        target: The object to proxy to.
        name: Deprecated name.
        replacement: Suggested replacement.
        docstring: Documentation string for the proxy.
    """
    proxy = _DeprecatedProxy(target, name, replacement)
    if docstring:
        proxy.__doc__ = docstring
    return proxy


def _make_deprecated_callable(
    name: str, replacement: str, func: Callable[..., Any] | str, docstring: str = ""
) -> Callable[..., Any]:
    """Return a function wrapping ``func`` that emits a deprecation warning.

    The returned callable preserves the wrapped function metadata.

    ``func`` can be either a callable or a string. If it's a string, it's treated
    as the name of a function to look up lazily in ``extra_platforms`` module.
    This allows wrapping dynamically generated functions that don't exist yet at
    module load time.

    Args:
        name: Deprecated name.
        replacement: Suggested replacement.
        func: The callable to wrap or string name to look up.
        docstring: Documentation string for the wrapper.
    """

    @wraps(func) if callable(func) else (lambda f: f)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        _warn_deprecated(name, replacement)
        target = func if callable(func) else getattr(_ep, func)
        return target(*args, **kwargs)

    if docstring:
        _wrapper.__doc__ = docstring

    return _wrapper


def _make_deprecated_module(
    module_name: str,
    version: str,
    replacement: str,
    symbols: dict[str, Any],
) -> ModuleType:
    """Create a deprecated module shim that warns on attribute access.

    This factory generates a fake module that can be injected into ``sys.modules``
    to provide backward-compatible imports while issuing deprecation warnings.

    Args:
        module_name: Full module path (e.g., "extra_platforms.platform").
        version: Version when the module was deprecated (e.g., "7.0.0").
        replacement: Suggested replacement module (e.g., "extra_platforms.trait").
        symbols: Dictionary mapping symbol names to their values or import paths.
            Values can be:
            - Direct objects (e.g., ``Platform`` class)
            - Tuples of ``(module_path, symbol_name)`` for lazy imports

    Returns:
        A :class:`~types.ModuleType` subclass instance that warns on attribute access.
    """

    class _DeprecatedModule(ModuleType):
        def __init__(self):
            super().__init__(module_name)
            self.__doc__ = (
                "Backward-compatible module for deprecated imports.\n\n"
                f".. deprecated:: {version}\n"
                f"    This module is deprecated. Import from ``{replacement}`` instead."
            )
            self.__file__ = __file__
            self.__all__ = list(symbols.keys())
            # Store symbols without triggering __setattr__ warning.
            object.__setattr__(self, "_symbols", symbols)

        def __getattr__(self, name: str):
            # Block private attributes unless explicitly listed in symbols.
            if name.startswith("_") and name not in self._symbols:
                raise AttributeError(
                    f"module {module_name!r} has no attribute {name!r}"
                )
            if name in self._symbols:
                warnings.warn(
                    f"The {module_name!r} module is deprecated. "
                    f"Import from {replacement!r} instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                value = self._symbols[name]
                # Handle lazy imports specified as (module_path, symbol_name) tuples.
                if isinstance(value, tuple) and len(value) == 2:
                    mod_path, sym_name = value
                    import importlib

                    mod = importlib.import_module(mod_path, package="extra_platforms")
                    return getattr(mod, sym_name)
                return value
            raise AttributeError(f"module {module_name!r} has no attribute {name!r}")

    return _DeprecatedModule()


# ================================================================
# Data aliases
# ================================================================


ALL_PLATFORM_IDS = _make_deprecated_proxy(
    ALL_TRAIT_IDS,
    "ALL_PLATFORM_IDS",
    "ALL_TRAIT_IDS",
    dedent("""\
        Alias ``ALL_PLATFORM_IDS`` → :data:`~ALL_TRAIT_IDS`.

        .. deprecated:: 6.0.0
           Use :data:`~ALL_TRAIT_IDS` instead.
        """),
)


ALL_PLATFORMS_WITHOUT_CI = _make_deprecated_proxy(
    ALL_PLATFORMS,
    "ALL_PLATFORMS_WITHOUT_CI",
    "ALL_PLATFORMS",
    dedent("""\
        Alias ``ALL_PLATFORMS_WITHOUT_CI`` → :data:`~ALL_PLATFORMS`.

        .. deprecated:: 6.0.0
           Use :data:`~ALL_PLATFORMS` instead.
        """),
)


UNKNOWN_LINUX = _make_deprecated_proxy(
    UNKNOWN_PLATFORM,
    "UNKNOWN_LINUX",
    "UNKNOWN_PLATFORM",
    dedent("""\
        Alias ``UNKNOWN_LINUX`` → :data:`~UNKNOWN_PLATFORM`.

        .. deprecated:: 7.0.0
           Use :data:`~UNKNOWN_PLATFORM` instead.
        """),
)


# ================================================================
# Platform and trait detection functions
# ================================================================


current_os = _make_deprecated_callable(
    "current_os()",
    "current_platform()",
    current_platform,  # type: ignore[has-type]
    dedent(
        """Alias ``current_os()`` → :func:`~current_platform`.

        .. deprecated:: 6.0.0
           Use :func:`~current_platform` instead.
        """
    ),
)


def _current_platforms_impl() -> tuple[Platform, ...]:
    return tuple(t for t in current_traits() if isinstance(t, Platform))


current_platforms = _make_deprecated_callable(
    "current_platforms()",
    "current_traits()",
    _current_platforms_impl,
    dedent(
        """Alias ``current_platforms()`` → :func:`~current_traits`.

        .. deprecated:: 6.0.0
           Use :func:`~current_traits` instead.
        """
    ),
)


is_unknown_linux = _make_deprecated_callable(
    "is_unknown_linux()",
    "is_unknown_platform()",
    "is_unknown_platform",
)
"""Alias ``is_unknown_linux()`` → :func:`~is_unknown_platform`.

.. deprecated:: 7.0.0
   Use :func:`~is_unknown_platform` instead.
"""


# ================================================================
# Group membership check functions
# ================================================================


is_all_platforms_without_ci = _make_deprecated_callable(
    "is_all_platforms_without_ci()",
    "is_any_platform()",
    "is_any_platform",
)
"""Alias ``is_all_platforms_without_ci()`` → :func:`~is_any_platform`.

.. deprecated:: 6.0.0
   Use :func:`~is_any_platform` instead.
"""


is_ci = _make_deprecated_callable("is_ci()", "is_any_ci()", "is_any_ci")
"""Alias ``is_ci()`` → :func:`~is_any_ci`.

.. deprecated:: 6.0.0
    Use :func:`~is_any_ci` instead.
"""


is_all_architectures = _make_deprecated_callable(
    "is_all_architectures()", "is_any_architecture()", "is_any_architecture"
)
"""Alias ``is_all_architectures()`` → :func:`~is_any_architecture`.

.. deprecated:: 7.0.0
   Use :func:`~is_any_architecture` instead.
"""


is_all_platforms = _make_deprecated_callable(
    "is_all_platforms()", "is_any_platform()", "is_any_platform"
)
"""Alias ``is_all_platforms()`` → :func:`~is_any_platform`.

.. deprecated:: 7.0.0
   Use :func:`~is_any_platform` instead.
"""


is_all_ci = _make_deprecated_callable("is_all_ci()", "is_any_ci()", "is_any_ci")
"""Alias ``is_all_ci()`` → :func:`~is_any_ci`.

.. deprecated:: 7.0.0
    Use :func:`~is_any_ci` instead.
"""


is_all_traits = _make_deprecated_callable(
    "is_all_traits()", "is_any_trait()", "is_any_trait"
)
"""Alias ``is_all_traits()`` → :func:`~is_any_trait`.

.. deprecated:: 7.0.0
   Use :func:`~is_any_trait` instead.
"""


is_other_unix = _make_deprecated_callable(
    "is_other_unix()", "is_other_posix()", "is_other_posix"
)
"""Alias ``is_other_unix()`` → :func:`~is_other_posix`.

.. deprecated:: 7.0.0
   Use :func:`~is_other_posix` instead.
"""


is_bsd_without_macos = _make_deprecated_callable(
    "is_bsd_without_macos()", "is_bsd_not_macos()", "is_bsd_not_macos"
)
"""Alias ``is_bsd_without_macos()`` → :func:`~is_bsd_not_macos`.

.. deprecated:: 7.0.0
   Use :func:`~is_bsd_not_macos` instead.
"""


is_unix_without_macos = _make_deprecated_callable(
    "is_unix_without_macos()", "is_unix_not_macos()", "is_unix_not_macos"
)
"""Alias ``is_unix_without_macos()`` → :func:`~is_unix_not_macos`.

.. deprecated:: 7.0.0
   Use :func:`~is_unix_not_macos` instead.
"""


# ================================================================
# Deprecated group symbols
# ================================================================


ANY_ARM = _make_deprecated_proxy(
    ALL_ARM,
    "ANY_ARM",
    "ALL_ARM",
    dedent("""\
        Alias ``ANY_ARM`` → :data:`~ALL_ARM`.

        .. deprecated:: 7.0.0
           Use :data:`~ALL_ARM` instead.
        """),
)


ANY_MIPS = _make_deprecated_proxy(
    ALL_MIPS,
    "ANY_MIPS",
    "ALL_MIPS",
    dedent("""\
        Alias ``ANY_MIPS`` → :data:`~ALL_MIPS`.

        .. deprecated:: 7.0.0
           Use :data:`~ALL_MIPS` instead.
        """),
)


ANY_SPARC = _make_deprecated_proxy(
    ALL_SPARC,
    "ANY_SPARC",
    "ALL_SPARC",
    dedent("""\
        Alias ``ANY_SPARC`` → :data:`~ALL_SPARC`.

        .. deprecated:: 7.0.0
           Use :data:`~ALL_SPARC` instead.
        """),
)


ANY_WINDOWS = _make_deprecated_proxy(
    ALL_WINDOWS,
    "ANY_WINDOWS",
    "ALL_WINDOWS",
    dedent("""\
        Alias ``ANY_WINDOWS`` → :data:`~ALL_WINDOWS`.

        .. deprecated:: 7.0.0
           Use :data:`~ALL_WINDOWS` instead.
        """),
)


OTHER_UNIX = _make_deprecated_proxy(
    OTHER_POSIX,
    "OTHER_UNIX",
    "OTHER_POSIX",
    dedent("""\
        Alias ``OTHER_UNIX`` → :data:`~OTHER_POSIX`.

        .. deprecated:: 7.0.0
           Use :data:`~OTHER_POSIX` instead.
        """),
)


# ================================================================
# Trait utilities
# ================================================================


platforms_from_ids = _make_deprecated_callable(
    "platforms_from_ids",
    "traits_from_ids",
    traits_from_ids,
    dedent(
        """Alias ``platforms_from_ids`` → :func:`~traits_from_ids`.

        .. deprecated:: 6.0.0
           Use :func:`~traits_from_ids` instead.
        """
    ),
)


# ================================================================
# Deprecated modules
# ================================================================


sys.modules["extra_platforms.platform"] = _make_deprecated_module(
    module_name="extra_platforms.platform",
    version="7.0.0",
    replacement="extra_platforms.trait",
    symbols={
        "Platform": Platform,
        "_recursive_update": _recursive_update,
        "_remove_blanks": _remove_blanks,
    },
)


sys.modules["extra_platforms.operations"] = _make_deprecated_module(
    module_name="extra_platforms.operations",
    version="8.0.0",
    replacement="extra_platforms",
    symbols={
        "ALL_GROUP_IDS": (".group_data", "ALL_GROUP_IDS"),
        "ALL_IDS": (".group_data", "ALL_IDS"),
        "ALL_TRAIT_IDS": (".group_data", "ALL_TRAIT_IDS"),
        "groups_from_ids": (".group", "groups_from_ids"),
        "reduce": (".group", "reduce"),
        "traits_from_ids": (".group", "traits_from_ids"),
    },
)
