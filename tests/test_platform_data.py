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

from string import ascii_lowercase, digits

from extra_platforms import ALL_OS_LABELS, ALL_PLATFORMS

import pytest
import requests


@pytest.mark.parametrize("platform", ALL_PLATFORMS.platforms)
def test_platform_definitions(platform):
    assert platform

    # ID.
    assert platform.id
    assert platform.id.isascii()
    assert platform.id[0] in ascii_lowercase
    assert platform.id[-1] in ascii_lowercase + digits
    assert set(platform.id).issubset(ascii_lowercase + digits + "_")
    assert platform.id.islower()
    # Platforms are not allowed to starts with all_ or any_, which is reserved
    # for groups. Use unknown_ prefix instead.
    assert not platform.id.startswith(("all_", "any_"))

    # Name.
    assert platform.name
    assert platform.name.isascii()
    assert platform.name.isprintable()
    assert platform.name in ALL_OS_LABELS

    # Icon.
    assert platform.icon
    assert 2 >= len(platform.icon) >= 1

    # URL.
    assert platform.url
    assert platform.url.startswith("https://")
    if platform.id == "raspbian":
        pytest.xfail("raspberrypi.com is blocking access from GitHub Actions")
    with requests.get(platform.url) as response:
        assert response.ok, f"{platform.url} is not reachable: {response}"

    # Info.
    assert platform.info()
    for k, v in platform.info().items():
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
    assert platform.info()["id"] == platform.id


def test_os_labels():
    assert len(ALL_OS_LABELS) == len(ALL_PLATFORMS)
