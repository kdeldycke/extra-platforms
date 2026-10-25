# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import pytest

from extra_platforms._utils import _recursive_update, _remove_blanks


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    (
        pytest.param(
            {"apple": "red", "citrus": {"lemon": "green"}},
            {"citrus": {"lemon": "yellow"}},
            {"apple": "red", "citrus": {"lemon": "yellow"}},
            id="nested_value",
        ),
        pytest.param(
            {"fruit": {"citrus": {"lemon": {"color": "green", "taste": "sour"}}}},
            {"fruit": {"citrus": {"lemon": {"color": "yellow"}}}},
            {"fruit": {"citrus": {"lemon": {"color": "yellow", "taste": "sour"}}}},
            id="deep_nesting",
        ),
        pytest.param(
            {"apple": "red"},
            {"apple": "green", "pear": "yellow"},
            {"apple": "green"},
            id="unknown_key_ignored",
        ),
        pytest.param(
            {"citrus": {"lemon": "green"}},
            {"citrus": "none"},
            {"citrus": "none"},
            id="dict_replaced_by_value",
        ),
        pytest.param(
            {"citrus": "none"},
            {"citrus": {"lemon": "green"}},
            {"citrus": {"lemon": "green"}},
            id="value_replaced_by_dict",
        ),
    ),
)
def test_recursive_update(a, b, expected):
    """The second dict updates the first one in place, at every depth."""
    result = _recursive_update(a, b)
    assert result is a
    assert result == expected


@pytest.mark.parametrize(
    ("b", "key"),
    (
        pytest.param({"pear": "yellow"}, "pear", id="top_level"),
        pytest.param({"citrus": {"lime": "green"}}, "lime", id="nested"),
    ),
)
def test_recursive_update_strict_rejects_unknown_key(b, key):
    """In strict mode, a key the first dict lacks raises, at any depth."""
    a = {"apple": "red", "citrus": {"lemon": "green"}}
    with pytest.raises(ValueError, match=f"Parameter '{key}' found in second dict"):
        _recursive_update(a, b, strict=True)


@pytest.mark.parametrize(
    ("tree", "options", "expected"),
    (
        pytest.param(
            {"apple": "red", "pear": None, "citrus": {"lemon": None, "lime": "green"}},
            {},
            {"apple": "red", "citrus": {"lime": "green"}},
            id="none_removed",
        ),
        pytest.param(
            {"apple": "red", "pear": None, "citrus": {"lemon": None}},
            {"remove_none": False},
            {"apple": "red", "pear": None, "citrus": {"lemon": None}},
            id="none_kept",
        ),
        pytest.param(
            {"apple": "red", "pear": "", "citrus": {"lemon": "", "lime": "green"}},
            {},
            {"apple": "red", "citrus": {"lime": "green"}},
            id="empty_string_removed",
        ),
        pytest.param(
            {"apple": "red", "pear": "", "citrus": {"lemon": ""}},
            {"remove_str": False},
            {"apple": "red", "pear": "", "citrus": {"lemon": ""}},
            id="empty_string_kept",
        ),
        pytest.param(
            {"apple": "red", "pear": {}, "citrus": {"lemon": {}, "lime": "green"}},
            {},
            {"apple": "red", "citrus": {"lime": "green"}},
            id="empty_dict_removed",
        ),
        pytest.param(
            {"apple": "red", "pear": {}, "citrus": {"lemon": {}}},
            {"remove_dicts": False},
            {"apple": "red", "pear": {}, "citrus": {"lemon": {}}},
            id="empty_dict_kept",
        ),
        pytest.param(
            {"fruit": {"citrus": {"lemon": None}}},
            {},
            {},
            id="emptied_dicts_removed",
        ),
        pytest.param(
            {
                "apple": "red",
                "pear": None,
                "plum": "",
                "fig": {},
                "citrus": {"lime": "green", "lemon": None, "yuzu": "", "kumquat": {}},
            },
            {},
            {"apple": "red", "citrus": {"lime": "green"}},
            id="mixed_blanks_removed",
        ),
        pytest.param(
            {"apple": None, "pear": "", "plum": {}},
            {"remove_none": False, "remove_str": False, "remove_dicts": False},
            {"apple": None, "pear": "", "plum": {}},
            id="nothing_removed",
        ),
        pytest.param(
            {"count": 0, "ripe": False, "seeds": [1, 2], "citrus": {"lime": "green"}},
            {},
            {"count": 0, "ripe": False, "seeds": [1, 2], "citrus": {"lime": "green"}},
            id="falsy_values_kept",
        ),
    ),
)
def test_remove_blanks(tree, options, expected):
    """Blank values go at every depth, unless the option for their kind is off."""
    assert _remove_blanks(tree, **options) == expected
