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
"""Test os-release parsing and platform information gathering."""

from __future__ import annotations

import io

import pytest

from extra_platforms.platform_info import (
    _parse_os_release_content,
    linux_info,
    os_release_id,
)


@pytest.fixture
def fresh_os_release_caches():
    """Clear derived os-release caches around a test patching
    ``_parse_os_release``.

    Only the caches of ``os_release_id()`` and ``linux_info()`` are cleared:
    ``_parse_os_release()`` itself is replaced by ``monkeypatch``, whose
    teardown runs after this fixture's, so the patched stand-in (a plain
    lambda) has no cache to clear.
    """
    os_release_id.cache_clear()
    linux_info.cache_clear()
    yield
    os_release_id.cache_clear()
    linux_info.cache_clear()


@pytest.mark.parametrize(
    ("content", "expected"),
    (
        pytest.param("", {}, id="empty_input"),
        pytest.param(
            "# This is a comment\n\nID=fedora\n",
            {"id": "fedora"},
            id="comments_and_blank_lines",
        ),
        pytest.param(
            'PRETTY_NAME="Ubuntu 22.04.3 LTS"\n'
            'NAME="Ubuntu"\n'
            'VERSION_ID="22.04"\n'
            'VERSION="22.04.3 LTS (Jammy Jellyfish)"\n'
            "VERSION_CODENAME=jammy\n"
            "ID=ubuntu\n"
            "ID_LIKE=debian\n",
            {
                "pretty_name": "Ubuntu 22.04.3 LTS",
                "name": "Ubuntu",
                "version_id": "22.04",
                "version": "22.04.3 LTS (Jammy Jellyfish)",
                "version_codename": "jammy",
                "id": "ubuntu",
                "id_like": "debian",
            },
            id="typical_ubuntu",
        ),
        pytest.param(
            'NAME="Fedora Linux"\n'
            'VERSION="39 (Workstation Edition)"\n'
            "ID=fedora\n"
            "VERSION_ID=39\n"
            'PRETTY_NAME="Fedora Linux 39 (Workstation Edition)"\n',
            {
                "name": "Fedora Linux",
                "version": "39 (Workstation Edition)",
                "id": "fedora",
                "version_id": "39",
                "pretty_name": "Fedora Linux 39 (Workstation Edition)",
                # Codename extracted from the VERSION parenthetical.
                "version_codename": "Workstation Edition",
            },
            id="typical_fedora",
        ),
        pytest.param(
            'ID="centos"\nNAME="CentOS Stream"\n',
            {"id": "centos", "name": "CentOS Stream"},
            id="quoted_values",
        ),
        pytest.param(
            'VERSION="10, Buster"\nID=debian\n',
            {
                "version": "10, Buster",
                "id": "debian",
                # Codename extracted from the VERSION comma separator.
                "version_codename": "Buster",
            },
            id="codename_from_version_comma",
        ),
        pytest.param(
            'VERSION="22.04.3 LTS (Jammy Jellyfish)"\n'
            "VERSION_CODENAME=jammy\n"
            "ID=ubuntu\n",
            {
                "version": "22.04.3 LTS (Jammy Jellyfish)",
                # VERSION_CODENAME takes precedence over VERSION extraction.
                "version_codename": "jammy",
                "id": "ubuntu",
            },
            id="version_codename_precedence",
        ),
        pytest.param(
            "ID=linuxmint\nUBUNTU_CODENAME=focal\n",
            {
                "id": "linuxmint",
                "ubuntu_codename": "focal",
                # UBUNTU_CODENAME is a fallback for VERSION_CODENAME.
                "version_codename": "focal",
            },
            id="ubuntu_codename_fallback",
        ),
        pytest.param(
            "ID=test\nPRETTY_NAME=Test\n",
            {"id": "test", "pretty_name": "Test"},
            id="keys_lowercased",
        ),
    ),
)
def test_parse_os_release_content(content, expected):
    """Parsing os-release content produces the exact expected mapping."""
    assert _parse_os_release_content(io.StringIO(content)) == expected


@pytest.mark.parametrize(
    ("raw_id", "expected"),
    (
        ("ol", "ol"),
        ("opensuse-leap", "opensuse-leap"),
        ("opensuse-slowroll", "opensuse-slowroll"),
        ("opensuse-tumbleweed", "opensuse-tumbleweed"),
        ("Ubuntu", "ubuntu"),
        ("fedora", "fedora"),
    ),
)
def test_os_release_id_sanitization(
    raw_id, expected, monkeypatch, fresh_os_release_caches
):
    """IDs are lowercased but otherwise preserved, sub-variants included."""
    monkeypatch.setattr(
        "extra_platforms.platform_info._parse_os_release",
        lambda: {"id": raw_id},
    )
    assert os_release_id() == expected


def test_os_release_id_empty(monkeypatch, fresh_os_release_caches):
    """Return empty string when no ID field is present."""
    monkeypatch.setattr(
        "extra_platforms.platform_info._parse_os_release",
        dict,
    )
    assert os_release_id() == ""


def test_linux_info_structure(monkeypatch, fresh_os_release_caches):
    """Return dict has expected keys and version_parts structure."""
    monkeypatch.setattr(
        "extra_platforms.platform_info._parse_os_release",
        lambda: {"id": "ubuntu", "version_id": "22.04.3", "id_like": "debian"},
    )
    info = linux_info()
    assert info["id"] == "ubuntu"
    assert info["version"] == "22.04.3"
    assert info["version_parts"] == {
        "major": "22",
        "minor": "04",
        "build_number": "3",
    }
    assert info["like"] == "debian"


def test_linux_info_empty_version(monkeypatch, fresh_os_release_caches):
    """Version parts are None when version_id is absent."""
    monkeypatch.setattr(
        "extra_platforms.platform_info._parse_os_release",
        lambda: {"id": "arch"},
    )
    info = linux_info()
    assert info["version"] is None
    assert info["version_parts"] == {
        "major": None,
        "minor": None,
        "build_number": None,
    }
    assert info["like"] is None
    assert info["codename"] is None
