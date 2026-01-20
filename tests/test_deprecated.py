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

from __future__ import annotations

import warnings

import pytest

from extra_platforms import (
    ALL_ARM,
    ALL_MIPS,
    ALL_PLATFORMS,
    ALL_SPARC,
    ALL_TRAIT_IDS,
    ALL_WINDOWS,
    LINUX,
    UNKNOWN_PLATFORM,
    Group,
    current_platform,
    current_traits,
    extract_members,
    is_unknown_platform,
    traits_from_ids,
)
from extra_platforms._deprecated import (
    ALL_PLATFORM_IDS,
    ALL_PLATFORMS_WITHOUT_CI,
    ANY_ARM,
    ANY_MIPS,
    ANY_SPARC,
    ANY_WINDOWS,
    UNKNOWN_LINUX,
    _DeprecatedProxy,
    _make_deprecated_callable,
    _make_deprecated_proxy,
    current_os,
    current_platforms,
    is_all_architectures,
    is_all_ci,
    is_all_platforms,
    is_all_platforms_without_ci,
    is_all_traits,
    is_ci,
    is_other_unix,
    is_unknown_linux,
    platforms_from_ids,
)


@pytest.mark.parametrize(
    "operation,target,old_name,new_name,operation_func,expected,expects_warning",
    [
        # Test attribute access (getattr).
        (
            "getattr",
            {"key": "value"},
            "old_name",
            "new_name",
            lambda p: p.keys(),
            lambda r: r is not None,
            True,
        ),
        # Test iteration.
        (
            "iter",
            [1, 2, 3],
            "old_list",
            "new_list",
            lambda p: list(p),
            lambda r: r == [1, 2, 3],
            True,
        ),
        # Test len().
        (
            "len",
            [1, 2, 3, 4],
            "old_list",
            "new_list",
            lambda p: len(p),
            lambda r: r == 4,
            True,
        ),
        # Test 'in' operator (contains).
        (
            "contains",
            {1, 2, 3},
            "old_set",
            "new_set",
            lambda p: 2 in p,
            lambda r: r is True,
            True,
        ),
        # Test function call.
        (
            "call",
            lambda x, y: x + y,
            "old_func()",
            "new_func()",
            lambda p: p(3, 5),
            lambda r: r == 8,
            True,
        ),
        # Test item access (getitem).
        (
            "getitem",
            {"a": 1, "b": 2},
            "old_dict",
            "new_dict",
            lambda p: p["a"],
            lambda r: r == 1,
            True,
        ),
        # Test repr() - should not trigger warning.
        (
            "repr",
            [1, 2, 3],
            "old_list",
            "new_list",
            lambda p: repr(p),
            lambda r: r == "[1, 2, 3]",
            False,
        ),
    ],
)
def test_deprecated_proxy_operations(
    operation, target, old_name, new_name, operation_func, expected, expects_warning
):
    """Test that _DeprecatedProxy delegates various operations."""
    proxy = _DeprecatedProxy(target, old_name, new_name)

    if expects_warning:
        with pytest.warns(
            DeprecationWarning, match=f"{old_name}.*deprecated.*{new_name}"
        ):
            result = operation_func(proxy)
        assert expected(result)
    else:
        # repr() should not trigger a warning, it's just for display.
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = operation_func(proxy)
        assert expected(result)


def test_make_deprecated_proxy():
    """Test the _make_deprecated_proxy factory function."""
    target = {"test": "value"}
    proxy = _make_deprecated_proxy(target, "old_name", "new_name")

    assert isinstance(proxy, _DeprecatedProxy)
    with pytest.warns(DeprecationWarning):
        _ = proxy["test"]


def test_make_deprecated_callable_with_function():
    """Test _make_deprecated_callable with a real function."""

    def real_func(x):
        return x * 2

    wrapped = _make_deprecated_callable("old_func()", "new_func()", real_func)

    with pytest.warns(DeprecationWarning, match="old_func.*deprecated.*new_func"):
        result = wrapped(5)
    assert result == 10


def test_make_deprecated_callable_with_string():
    """Test _make_deprecated_callable with a string (lazy lookup)."""
    # Use a known function that exists in extra_platforms.
    wrapped = _make_deprecated_callable(
        "old_is_unknown()", "is_unknown_platform()", "is_unknown_platform"
    )

    with pytest.warns(
        DeprecationWarning, match="old_is_unknown.*deprecated.*is_unknown_platform"
    ):
        result = wrapped()
    assert isinstance(result, bool)


def test_all_platform_ids_alias():
    """Test ALL_PLATFORM_IDS → ALL_TRAIT_IDS alias."""
    with pytest.warns(DeprecationWarning, match="ALL_PLATFORM_IDS.*ALL_TRAIT_IDS"):
        result = list(ALL_PLATFORM_IDS)
    assert set(result) == ALL_TRAIT_IDS


def test_all_platforms_without_ci_alias():
    """Test ALL_PLATFORMS_WITHOUT_CI → ALL_PLATFORMS alias."""
    with pytest.warns(
        DeprecationWarning, match="ALL_PLATFORMS_WITHOUT_CI.*ALL_PLATFORMS"
    ):
        result = set(ALL_PLATFORMS_WITHOUT_CI)
    # Should be the same as ALL_PLATFORMS members.
    assert result == set(ALL_PLATFORMS)


def test_unknown_linux_alias():
    """Test UNKNOWN_LINUX → UNKNOWN_PLATFORM alias."""
    # Accessing an attribute triggers the deprecation warning.
    with pytest.warns(DeprecationWarning, match="UNKNOWN_LINUX.*UNKNOWN_PLATFORM"):
        result = UNKNOWN_LINUX.id
    assert result == UNKNOWN_PLATFORM.id


def test_any_arm_alias():
    """Test ANY_ARM → ALL_ARM alias."""
    with pytest.warns(DeprecationWarning, match="ANY_ARM.*ALL_ARM"):
        result = set(ANY_ARM)
    assert result == set(ALL_ARM)


def test_any_mips_alias():
    """Test ANY_MIPS → ALL_MIPS alias."""
    with pytest.warns(DeprecationWarning, match="ANY_MIPS.*ALL_MIPS"):
        result = set(ANY_MIPS)
    assert result == set(ALL_MIPS)


def test_any_sparc_alias():
    """Test ANY_SPARC → ALL_SPARC alias."""
    with pytest.warns(DeprecationWarning, match="ANY_SPARC.*ALL_SPARC"):
        result = set(ANY_SPARC)
    assert result == set(ALL_SPARC)


def test_any_windows_alias():
    """Test ANY_WINDOWS → ALL_WINDOWS alias."""
    with pytest.warns(DeprecationWarning, match="ANY_WINDOWS.*ALL_WINDOWS"):
        result = set(ANY_WINDOWS)
    assert result == set(ALL_WINDOWS)


def test_current_os_alias():
    """Test current_os() → current_platform() alias."""
    with pytest.warns(DeprecationWarning, match="current_os.*current_platform"):
        result = current_os()
    assert result == current_platform()


def test_current_platforms_alias():
    """Test current_platforms() → current_traits() alias."""
    from extra_platforms import Platform

    with pytest.warns(DeprecationWarning, match="current_platforms.*current_traits"):
        result = current_platforms()
    # current_platforms returns only Platform instances from current_traits.
    expected = {t for t in current_traits() if isinstance(t, Platform)}
    assert set(result) == expected


def test_is_unknown_linux_alias():
    """Test is_unknown_linux() → is_unknown_platform() alias."""
    with pytest.warns(
        DeprecationWarning, match="is_unknown_linux.*is_unknown_platform"
    ):
        result = is_unknown_linux()
    assert result == is_unknown_platform()


def test_group_extract_platforms_deprecated():
    """Test Group._extract_platforms() deprecated method."""
    with pytest.warns(DeprecationWarning, match="_extract_platforms.*extract_members"):
        result = list(Group._extract_platforms(LINUX))
    expected = list(extract_members(LINUX))
    assert result == expected


def test_deprecated_is_all_functions():
    """Test is_all_* deprecated functions."""
    # Each should trigger a warning and return a boolean.
    with pytest.warns(DeprecationWarning):
        result = is_all_architectures()
    assert isinstance(result, bool)

    with pytest.warns(DeprecationWarning):
        result = is_all_ci()
    assert isinstance(result, bool)

    with pytest.warns(DeprecationWarning):
        result = is_all_platforms()
    assert isinstance(result, bool)

    with pytest.warns(DeprecationWarning):
        result = is_all_platforms_without_ci()
    assert isinstance(result, bool)

    with pytest.warns(DeprecationWarning):
        result = is_all_traits()
    assert isinstance(result, bool)


def test_deprecated_is_ci_function():
    """Test is_ci() deprecated function."""
    with pytest.warns(DeprecationWarning, match="is_ci.*is_any_ci"):
        result = is_ci()
    assert isinstance(result, bool)


def test_deprecated_is_other_unix_function():
    """Test is_other_unix() deprecated function."""
    with pytest.warns(DeprecationWarning, match="is_other_unix.*is_other_posix"):
        result = is_other_unix()
    assert isinstance(result, bool)


def test_deprecated_platforms_from_ids():
    """Test platforms_from_ids() → traits_from_ids() alias."""
    with pytest.warns(DeprecationWarning, match="platforms_from_ids.*traits_from_ids"):
        result = platforms_from_ids("linux")
    # Should work the same as traits_from_ids.
    expected = traits_from_ids("linux")
    assert set(result) == set(expected)
