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

from extra_platforms import ALL_TRAITS, UNKNOWN
from extra_platforms.trait import Trait


def test_all_traits_have_detection_function():
    for trait in ALL_TRAITS | {UNKNOWN}:
        assert trait.detection_func_id
        assert trait.current in (True, False)


def test_detection_function_missing(caplog):

    class DummyTrait(Trait):
        id = "dummy_trait"

        def info(self) -> dict:
            return {}

    trait = DummyTrait(
        id="dummy_trait", name="Dummy Trait", icon="❓", url="https://example.com"
    )

    assert trait.detection_func_id == "is_dummy_trait"
    with pytest.raises(
        NotImplementedError,
        match=r"Detection function is_dummy_trait\(\) is not implemented\.",
    ):
        _ = trait.current
