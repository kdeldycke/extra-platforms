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

import ast
import inspect
from operator import attrgetter
from pathlib import Path
from string import ascii_lowercase, digits

import pytest

from extra_platforms import ALL_ARCHITECTURES, ALL_GROUP_IDS, ALL_IDS, ALL_MEMBER_IDS
from extra_platforms import architecture_data as architecture_data_module

all_architectures_params = pytest.mark.parametrize(
    "architecture", ALL_ARCHITECTURES.platforms, ids=attrgetter("id")
)


def test_architecture_data_sorting():
    """Architecture instances must be sorted alphabetically."""
    architecture_instance_ids = []
    tree = ast.parse(Path(inspect.getfile(architecture_data_module)).read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and node.value.func.id == "Architecture"
        ):
            assert len(node.targets) == 1
            instance_id = node.targets[0].id
            assert instance_id.isupper()
            architecture_instance_ids.append(instance_id)

    assert architecture_instance_ids == sorted(architecture_instance_ids)


@all_architectures_params
def test_architecture_definitions(architecture):
    assert architecture

    # ID.
    assert architecture.id
    assert architecture.id.isascii()
    assert architecture.id[0] in ascii_lowercase
    assert architecture.id[-1] in ascii_lowercase + digits
    assert set(architecture.id).issubset(ascii_lowercase + digits + "_")
    assert architecture.id.islower()
    # Platforms are not allowed to starts with all_ or any_, which is reserved
    # for groups. Use unknown_ prefix instead.
    assert not architecture.id.startswith(("all_", "any_"))
    assert architecture.id in ALL_MEMBER_IDS
    assert architecture.id not in ALL_GROUP_IDS
    assert architecture.id in ALL_IDS

    # Name.
    assert architecture.name
    assert architecture.name.isascii()
    assert architecture.name.isprintable()

    # Icon.
    assert architecture.icon
    assert 2 >= len(architecture.icon) >= 1

    # URL.
    assert architecture.url
    assert architecture.url.startswith("https://")

    # Info.
    assert architecture.info()
    for k, v in architecture.info().items():
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
    assert architecture.info()["id"] == architecture.id
