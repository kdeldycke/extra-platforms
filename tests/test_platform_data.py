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

import sys
from operator import attrgetter
from string import ascii_lowercase, digits

import pytest
import requests

from extra_platforms import ALL_GROUP_IDS, ALL_IDS, ALL_PLATFORM_IDS, ALL_PLATFORMS
from extra_platforms.pytest import unless_linux  # type: ignore[attr-defined]

all_platforms_params = pytest.mark.parametrize(
    "platform", ALL_PLATFORMS.platforms, ids=attrgetter("id")
)


@all_platforms_params
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
    assert platform.id in ALL_PLATFORM_IDS
    assert platform.id not in ALL_GROUP_IDS
    assert platform.id in ALL_IDS

    # Name.
    assert platform.name
    assert platform.name.isascii()
    assert platform.name.isprintable()

    # Icon.
    assert platform.icon
    assert 2 >= len(platform.icon) >= 1

    # URL.
    assert platform.url
    assert platform.url.startswith("https://")

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


# Restrict tests to Linux on Python 3.13 to avoid DOSing websites.
@unless_linux
@pytest.mark.skipif(
    (sys.version_info.major, sys.version_info.minor) == (3, 13),
    reason="DOSing websites",
)
@all_platforms_params
def test_platform_website(platform):
    """Test if platform website is reachable.

    Place this test in a separate function so we can separate it from the platform data
    tests, and allow this test to be skipped while requiring the test above to always
    pass.

    Some websites are known to be flaky, because they block access from GitHub Actions,
    or can't take the load of requests from CI. We skip these platforms.
    """
    flaky_websites = {"hurd", "linuxmint", "midnightbsd", "raspbian"}
    if platform.id in flaky_websites:
        pytest.xfail(f"{platform.url} is known to be flaky and not always responding")
    with requests.get(platform.url) as response:
        assert response.ok, f"{platform.url} is not reachable: {response}"
