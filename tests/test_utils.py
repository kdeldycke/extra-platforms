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

import pytest

from extra_platforms._utils import _recursive_update, _remove_blanks


def test_recursive_update_basic():
    """Test basic recursive update."""
    a = {"key1": "value1", "key2": {"nested": "old"}}
    b = {"key2": {"nested": "new"}}

    result = _recursive_update(a, b)

    assert result["key1"] == "value1"
    assert result["key2"]["nested"] == "new"


def test_recursive_update_adds_new_keys():
    """Test that recursive update ignores keys not in first dict."""
    a = {"existing": "value"}
    b = {"existing": "updated", "new_key": "new_value"}

    result = _recursive_update(a, b)

    assert result["existing"] == "updated"
    assert "new_key" not in result


def test_recursive_update_strict_mode():
    """Test strict mode raises ValueError for unregistered keys."""
    a = {"existing": "value"}
    b = {"existing": "updated", "unregistered": "value"}

    with pytest.raises(
        ValueError, match="Parameter 'unregistered' found in second dict"
    ):
        _recursive_update(a, b, strict=True)


def test_recursive_update_deep_nesting():
    """Test recursive update with deep nesting (3+ levels)."""
    a = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": "old_value",
                    "keep": "this",
                },
            },
        },
    }
    b = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": "new_value",
                },
            },
        },
    }

    result = _recursive_update(a, b)

    assert result["level1"]["level2"]["level3"]["level4"] == "new_value"
    assert result["level1"]["level2"]["level3"]["keep"] == "this"


def test_recursive_update_overwrites_non_dict():
    """Test that non-dict values are overwritten, not merged."""
    a = {"key": "old_value"}
    b = {"key": "new_value"}

    result = _recursive_update(a, b)

    assert result["key"] == "new_value"


def test_recursive_update_preserves_original():
    """Test that original dict is modified in place."""
    a = {"key": "value"}
    b = {"key": "updated"}

    result = _recursive_update(a, b)

    # The function returns a, so result is the same object.
    assert result is a
    assert a["key"] == "updated"


@pytest.mark.parametrize(
    "blank_type,tree,remove_kwargs,should_remove",
    [
        # Test removing None values
        (
            "none",
            {
                "key1": "value",
                "key2": None,
                "key3": {"nested": None, "other": "keep"},
            },
            {"remove_none": True},
            True,
        ),
        # Test keeping None values
        (
            "none",
            {"key1": "value", "key2": None},
            {"remove_none": False},
            False,
        ),
        # Test removing empty strings
        (
            "empty_string",
            {
                "key1": "value",
                "key2": "",
                "key3": {"nested": "", "other": "keep"},
            },
            {"remove_str": True},
            True,
        ),
        # Test keeping empty strings
        (
            "empty_string",
            {"key1": "value", "key2": ""},
            {"remove_str": False},
            False,
        ),
        # Test removing empty dicts
        (
            "empty_dict",
            {
                "key1": "value",
                "key2": {},
                "key3": {"nested": {}, "other": "keep"},
            },
            {"remove_dicts": True},
            True,
        ),
        # Test keeping empty dicts
        (
            "empty_dict",
            {"key1": "value", "key2": {}},
            {"remove_dicts": False},
            False,
        ),
    ],
)
def test_remove_blanks_options(blank_type, tree, remove_kwargs, should_remove):
    """Test removing or keeping different types of blank values."""
    result = _remove_blanks(tree, **remove_kwargs)

    assert "key1" in result

    if should_remove:
        # When removing, blank values should be gone
        assert "key2" not in result
        if "key3" in tree:
            assert "nested" not in result["key3"]
            assert result["key3"]["other"] == "keep"
    else:
        # When keeping, blank values should remain
        assert "key2" in result
        if blank_type == "none":
            assert result["key2"] is None
        elif blank_type == "empty_string":
            assert result["key2"] == ""
        elif blank_type == "empty_dict":
            assert result["key2"] == {}


def test_remove_blanks_mixed_scenario():
    """Test removing all blank types in a mixed scenario."""
    tree = {
        "keep_value": "value",
        "remove_none": None,
        "remove_empty_str": "",
        "remove_empty_dict": {},
        "nested": {
            "keep": "this",
            "remove_none": None,
            "remove_empty": "",
            "deeply_nested": {
                "remove_all": None,
            },
        },
    }

    result = _remove_blanks(tree, remove_none=True, remove_str=True, remove_dicts=True)

    assert result == {
        "keep_value": "value",
        "nested": {
            "keep": "this",
        },
    }


def test_remove_blanks_all_options_disabled():
    """Test that nothing is removed when all options are disabled."""
    tree = {
        "key1": "value",
        "key2": None,
        "key3": "",
        "key4": {},
    }

    result = _remove_blanks(
        tree, remove_none=False, remove_str=False, remove_dicts=False
    )

    assert result == tree


def test_remove_blanks_recursive_cleanup():
    """Test that nested dicts are cleaned recursively."""
    tree = {
        "level1": {
            "level2": {
                "level3": {
                    "remove": None,
                },
            },
        },
    }

    result = _remove_blanks(tree, remove_none=True, remove_dicts=True)

    # All nested empty dicts should be removed.
    assert result == {}


def test_remove_blanks_preserves_non_blank_values():
    """Test that non-blank values of all types are preserved."""
    tree = {
        "string": "text",
        "number": 42,
        "zero": 0,
        "false": False,
        "list": [1, 2, 3],
        "dict": {"key": "value"},
    }

    result = _remove_blanks(tree)

    assert result == tree
