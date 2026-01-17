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

import re
from operator import attrgetter
from pathlib import Path
from string import ascii_lowercase, digits

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUP_IDS,
    ALL_IDS,
    ALL_TRAIT_IDS,
    ALL_TRAITS,
    CI,
    UNKNOWN,
    Architecture,
    Platform,
    Trait,
)


@pytest.mark.parametrize(
    "klass", (Architecture, Platform, CI), ids=attrgetter("__name__")
)
def test_trait_class_metadata(klass):
    class_id = klass.__name__.lower()

    assert klass.type_name
    assert klass.type_name.isascii()
    assert klass.type_name.isprintable()

    assert hasattr(extra_platforms, f"current_{class_id}")

    assert klass.data_module_id == f"{class_id}_data"
    assert hasattr(extra_platforms, klass.data_module_id)

    assert klass.unknown_symbol == f"UNKNOWN_{class_id.upper()}"
    assert (
        klass.unknown_symbol == getattr(extra_platforms, klass.unknown_symbol).symbol_id
    )

    assert re.fullmatch(rf"ALL_{class_id.upper()}S?", klass.all_group)
    assert klass.all_group == getattr(extra_platforms, klass.all_group).symbol_id

    assert klass.doc_page.startswith(class_id)
    assert klass.doc_page.endswith(".md")
    # Verify that the doc_page actually exists in the docs directory.
    doc_file = Path(__file__).parent.parent / "docs" / klass.doc_page
    assert doc_file.exists(), f"Documentation file not found: {doc_file}"
    assert doc_file.is_file(), f"Expected a file but got directory: {doc_file}"
    # Verify that the file starts with a proper markdown title.
    assert re.fullmatch(
        rf"# \{{octicon}}`\S+` {klass.type_name[0].upper()}{klass.type_name[1:]}s",
        doc_file.read_text(encoding="utf-8").splitlines()[0],
    )


@pytest.mark.parametrize("trait", tuple(ALL_TRAITS | UNKNOWN), ids=attrgetter("id"))
def test_all_traits_generated_constants(trait):
    assert trait

    assert trait.id
    assert trait.id.isascii()
    assert trait.id[0] in ascii_lowercase
    assert trait.id[-1] in ascii_lowercase + digits
    assert set(trait.id).issubset(ascii_lowercase + digits + "_")
    assert trait.id.islower()
    assert trait.id not in ALL_GROUP_IDS

    if "unknown" in trait.id:
        assert trait in UNKNOWN
        assert trait.id not in ALL_TRAIT_IDS
        assert trait.id not in ALL_IDS
        assert trait.id == f"unknown_{trait.__class__.__name__.lower()}"
        assert (
            trait.name.lower()
            == "unknown " + trait.__class__.__name__.replace("_", " ").lower()
        )
        assert trait.icon == "❓"
    else:
        assert trait.id in ALL_TRAIT_IDS
        assert trait.id in ALL_IDS
        assert trait not in UNKNOWN

    # Some special words can only be used as part of a compound word, never as
    # standalone tokens.
    for special_word in ("all", "any", "is", "skip", "unless", "without", "not"):
        assert not trait.id.startswith(special_word)
        assert special_word not in trait.id.split("_")

    # Name.
    assert trait.name
    assert trait.name.isascii()
    assert trait.name.isprintable()

    # Icon.
    assert trait.icon
    assert 2 >= len(trait.icon) >= 1

    # URL.
    assert trait.url
    assert trait.url.startswith("https://")

    # Symbol ID.
    assert trait.symbol_id
    assert trait.symbol_id == trait.id.upper()
    assert hasattr(extra_platforms, trait.symbol_id)

    # Detection function.
    assert trait.detection_func_id
    assert hasattr(extra_platforms, trait.detection_func_id)
    assert trait.current in (True, False)

    # Info.
    assert trait.info()
    for k, v in trait.info().items():
        assert set(k).issubset(ascii_lowercase + "_")
        if v is not None:
            assert isinstance(v, (str, bool, dict))
            if isinstance(v, str):
                assert v
            elif isinstance(v, dict):
                assert v
                for k1, v1 in v.items():
                    assert set(k1).issubset(ascii_lowercase + "_")
                    if v1 is not None:
                        assert v1
    assert trait.info()["id"] == trait.id


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
