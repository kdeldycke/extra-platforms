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

import io

import pytest

from extra_platforms.platform_info import (
    _parse_os_release_content,
    linux_info,
    os_release_id,
)


class TestParseOsReleaseContent:
    """Tests for ``_parse_os_release_content()``."""

    def test_empty_input(self):
        """Empty input returns empty dict."""
        assert _parse_os_release_content(io.StringIO("")) == {}

    def test_comments_and_blank_lines(self):
        """Comments and blank lines are ignored."""
        content = "# This is a comment\n\nID=fedora\n"
        result = _parse_os_release_content(io.StringIO(content))
        assert result["id"] == "fedora"
        assert len(result) == 1

    def test_typical_ubuntu(self):
        """Parse typical Ubuntu os-release content."""
        content = """\
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
"""
        result = _parse_os_release_content(io.StringIO(content))
        assert result["id"] == "ubuntu"
        assert result["id_like"] == "debian"
        assert result["version_id"] == "22.04"
        assert result["version_codename"] == "jammy"
        assert result["pretty_name"] == "Ubuntu 22.04.3 LTS"

    def test_typical_fedora(self):
        """Parse typical Fedora os-release content."""
        content = """\
NAME="Fedora Linux"
VERSION="39 (Workstation Edition)"
ID=fedora
VERSION_ID=39
PRETTY_NAME="Fedora Linux 39 (Workstation Edition)"
"""
        result = _parse_os_release_content(io.StringIO(content))
        assert result["id"] == "fedora"
        assert result["version_id"] == "39"
        # Codename extracted from VERSION parenthetical.
        assert result["version_codename"] == "Workstation Edition"

    def test_quoted_values(self):
        """Quoted values are properly unquoted."""
        content = 'ID="centos"\nNAME="CentOS Stream"\n'
        result = _parse_os_release_content(io.StringIO(content))
        assert result["id"] == "centos"
        assert result["name"] == "CentOS Stream"

    def test_codename_from_version_comma(self):
        """Codename extracted from VERSION field with comma separator."""
        content = 'VERSION="10, Buster"\nID=debian\n'
        result = _parse_os_release_content(io.StringIO(content))
        assert result["version_codename"] == "Buster"

    def test_version_codename_precedence(self):
        """VERSION_CODENAME takes precedence over VERSION extraction."""
        content = (
            'VERSION="22.04.3 LTS (Jammy Jellyfish)"\n'
            "VERSION_CODENAME=jammy\n"
            "ID=ubuntu\n"
        )
        result = _parse_os_release_content(io.StringIO(content))
        assert result["version_codename"] == "jammy"

    def test_ubuntu_codename_fallback(self):
        """UBUNTU_CODENAME is used as fallback when VERSION_CODENAME is absent."""
        content = "ID=linuxmint\nUBUNTU_CODENAME=focal\n"
        result = _parse_os_release_content(io.StringIO(content))
        assert result["version_codename"] == "focal"

    def test_keys_lowercased(self):
        """All keys are lowercased."""
        content = "ID=test\nPRETTY_NAME=Test\n"
        result = _parse_os_release_content(io.StringIO(content))
        assert "id" in result
        assert "pretty_name" in result


class TestOsReleaseId:
    """Tests for ``os_release_id()`` normalization."""

    @pytest.mark.parametrize(
        ("raw_id", "expected"),
        [
            ("ol", "oracle"),
            ("opensuse-leap", "opensuse"),
            ("opensuse-tumbleweed", "opensuse-tumbleweed"),
            ("Ubuntu", "ubuntu"),
            ("fedora", "fedora"),
        ],
    )
    def test_normalization(self, raw_id, expected, monkeypatch):
        """Test ID normalization rules."""
        monkeypatch.setattr(
            "extra_platforms.platform_info._parse_os_release",
            lambda: {"id": raw_id},
        )
        os_release_id.cache_clear()
        assert os_release_id() == expected
        os_release_id.cache_clear()

    def test_empty_when_no_id(self, monkeypatch):
        """Return empty string when no ID field is present."""
        monkeypatch.setattr(
            "extra_platforms.platform_info._parse_os_release",
            lambda: {},
        )
        os_release_id.cache_clear()
        assert os_release_id() == ""
        os_release_id.cache_clear()


class TestLinuxInfo:
    """Tests for ``linux_info()`` return structure."""

    def test_structure(self, monkeypatch):
        """Return dict has expected keys and version_parts structure."""
        monkeypatch.setattr(
            "extra_platforms.platform_info._parse_os_release",
            lambda: {"id": "ubuntu", "version_id": "22.04.3", "id_like": "debian"},
        )
        os_release_id.cache_clear()
        linux_info.cache_clear()
        info = linux_info()
        assert info["id"] == "ubuntu"
        assert info["version"] == "22.04.3"
        assert info["version_parts"] == {
            "major": "22",
            "minor": "04",
            "build_number": "3",
        }
        assert info["like"] == "debian"
        os_release_id.cache_clear()
        linux_info.cache_clear()

    def test_empty_version(self, monkeypatch):
        """Version parts are empty strings when version_id is absent."""
        monkeypatch.setattr(
            "extra_platforms.platform_info._parse_os_release",
            lambda: {"id": "arch"},
        )
        os_release_id.cache_clear()
        linux_info.cache_clear()
        info = linux_info()
        assert info["version"] == ""
        assert info["version_parts"] == {
            "major": "",
            "minor": "",
            "build_number": "",
        }
        os_release_id.cache_clear()
        linux_info.cache_clear()
