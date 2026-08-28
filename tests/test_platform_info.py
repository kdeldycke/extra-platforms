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
import os
import shutil
import subprocess

import pytest

from extra_platforms.platform_info import (
    _hostnamectl_os_release,
    _parse_cpe_name,
    _parse_hostnamectl_content,
    _parse_os_release,
    _parse_os_release_content,
    invalidate_os_release_cache,
    linux_info,
    os_release_id,
)

HOSTNAMECTL_CLOUDLINUX = """\
   Static hostname: web.illinois.edu
         Icon name: computer-vm
           Chassis: vm
           Boot ID: 5b5b8c522ccd4974808f192aea001491
    Virtualization: kvm
  Operating System: CloudLinux 7.6 (Vladimir Lyakhov)
       CPE OS Name: cpe:/o:cloudlinux:cloudlinux:7.6:GA:server
            Kernel: Linux 3.10.0-962.3.2.lve1.5.24.9.el7.x86_64
      Architecture: x86-64
"""
"""Status output of the CloudLinux VM reported in
[`python-distro/distro#240`](https://github.com/python-distro/distro/issues/240),
where no os-release file is readable.
"""


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


@pytest.fixture
def fresh_hostnamectl_caches():
    """Clear the caches a `hostnamectl`-driving test fills.

    ``_parse_os_release()`` memoizes whatever the fallback answered, so it is
    cleared next to ``_hostnamectl_os_release()``. Both are cleared on entry and
    exit, which ``fresh_os_release_caches`` cannot do for
    ``_parse_os_release()``: no test using this fixture replaces either
    function, so the real ``cache_clear()`` stays reachable on both sides.
    """
    _hostnamectl_os_release.cache_clear()
    _parse_os_release.cache_clear()
    yield
    _hostnamectl_os_release.cache_clear()
    _parse_os_release.cache_clear()


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


@pytest.mark.parametrize(
    ("cpe_name", "distro_id"),
    (
        ("cpe:/o:almalinux:almalinux:10::baseos", "almalinux"),
        ("cpe:/o:alt:server:10.1", "altlinux"),
        ("cpe:/o:amazon:linux:2016.03:ga", "amzn"),
        ("cpe:2.3:o:amazon:amazon_linux:2023", "amzn"),
        ("cpe:/o:centos:centos:7", "centos"),
        ("cpe:/o:cloudlinux:cloudlinux:7.3:GA:server", "cloudlinux"),
        ("cpe:/o:fedoraproject:fedora:19", "fedora"),
        ("cpe:/o:ibm:kvmibm:1.1.1", "kvmibm"),
        ("cpe:/o:opensuse:leap:15.2", "opensuse-leap"),
        ("cpe:/o:opensuse:opensuse:42.1", "opensuse"),
        ("cpe:/o:oracle:linux:7:5:server", "ol"),
        ("cpe:/o:redhat:enterprise_linux:9::baseos", "rhel"),
        ("cpe:/o:rocky:rocky:8.4:GA", "rocky"),
        ("cpe:/o:scientificlinux:scientificlinux:7.2:GA", "rhel"),
        ("cpe:/o:slackware:slackware_linux:14.1", "slackware"),
        ("cpe:/o:suse:sles:12:sp1", "sles"),
    ),
)
def test_parse_cpe_name_matches_os_release_id(cpe_name, distro_id):
    """A CPE name derives the `ID` the same system declares in its os-release.

    Both fields of each case are read from one real os-release file, as
    collected in
    [python-distro's test resources](https://github.com/python-distro/distro/tree/master/tests/resources/distros).
    That covers every ``vendor:product`` pair those fixtures carry, so a new
    entry in ``CPE_ID_OVERRIDES`` that contradicts a released distribution fails
    here.
    """
    assert _parse_cpe_name(cpe_name)["id"] == distro_id


@pytest.mark.parametrize(
    ("cpe_name", "expected"),
    (
        pytest.param(
            "cpe:/o:cloudlinux:cloudlinux:7.6:GA:server",
            {
                "cpe_name": "cpe:/o:cloudlinux:cloudlinux:7.6:GA:server",
                "id": "cloudlinux",
                "version_id": "7.6",
            },
            id="uri_binding_drops_trailing_components",
        ),
        pytest.param(
            "cpe:2.3:o:amazon:amazon_linux:2023",
            {
                "cpe_name": "cpe:2.3:o:amazon:amazon_linux:2023",
                "id": "amzn",
                "version_id": "2023",
            },
            id="formatted_string_binding",
        ),
        pytest.param(
            "cpe:/o:vendor:product",
            {"cpe_name": "cpe:/o:vendor:product", "id": "product"},
            id="no_version",
        ),
        pytest.param(
            "cpe:/o:vendor:product:*",
            {"cpe_name": "cpe:/o:vendor:product:*", "id": "product"},
            id="any_version_placeholder",
        ),
        pytest.param(
            "cpe:/o:vendor:-:1.0",
            {"cpe_name": "cpe:/o:vendor:-:1.0", "version_id": "1.0"},
            id="not_applicable_product_placeholder",
        ),
        pytest.param("cpe:/a:vendor:product:1.0", {}, id="application_not_os"),
        pytest.param("cpe:/h:vendor:product:1.0", {}, id="hardware_not_os"),
        pytest.param("", {}, id="empty_input"),
        pytest.param("CloudLinux 7.6", {}, id="not_a_cpe_name"),
    ),
)
def test_parse_cpe_name(cpe_name, expected):
    """Parsing a CPE name produces the exact expected mapping."""
    assert _parse_cpe_name(cpe_name) == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    (
        pytest.param("", {}, id="empty_input"),
        pytest.param(
            HOSTNAMECTL_CLOUDLINUX,
            {
                "cpe_name": "cpe:/o:cloudlinux:cloudlinux:7.6:GA:server",
                "id": "cloudlinux",
                "version_id": "7.6",
                "pretty_name": "CloudLinux 7.6 (Vladimir Lyakhov)",
                # Codename extracted from the pretty name parenthetical.
                "version_codename": "Vladimir Lyakhov",
            },
            id="cloudlinux_vm",
        ),
        pytest.param(
            "  Operating System: Ubuntu 22.04.3 LTS\n"
            "            Kernel: Linux 6.5.0-14-generic\n",
            {"pretty_name": "Ubuntu 22.04.3 LTS"},
            id="no_cpe_line",
        ),
        pytest.param(
            "       CPE OS Name: cpe:/o:fedoraproject:fedora:39\n",
            {
                "cpe_name": "cpe:/o:fedoraproject:fedora:39",
                "id": "fedora",
                "version_id": "39",
            },
            id="no_pretty_name_line",
        ),
        pytest.param(
            "   Static hostname: fridge\n"
            "           Chassis: container\n"
            "            Kernel: Linux 6.5.0-14-generic\n",
            {},
            id="host_lines_only",
        ),
        pytest.param(
            "Failed to query system properties: Connection refused\n",
            {},
            id="bus_error_message",
        ),
    ),
)
def test_parse_hostnamectl_content(content, expected):
    """Parsing hostnamectl output produces the exact expected mapping."""
    assert _parse_hostnamectl_content(content.splitlines()) == expected


def _fake_run(stdout):
    """Build a `subprocess.run` stand-in returning ``stdout``."""

    def run(*args, **kwargs):
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

    return run


def test_hostnamectl_os_release(monkeypatch, fresh_hostnamectl_caches):
    """A reachable systemd bus rebuilds the os-release fields."""
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/hostnamectl")
    monkeypatch.setattr(subprocess, "run", _fake_run(HOSTNAMECTL_CLOUDLINUX))
    assert _hostnamectl_os_release() == {
        "cpe_name": "cpe:/o:cloudlinux:cloudlinux:7.6:GA:server",
        "id": "cloudlinux",
        "version_id": "7.6",
        "pretty_name": "CloudLinux 7.6 (Vladimir Lyakhov)",
        "version_codename": "Vladimir Lyakhov",
    }


def test_hostnamectl_os_release_skips_missing_binary(
    monkeypatch, fresh_hostnamectl_caches
):
    """No subprocess is spawned on a system shipping no `hostnamectl`."""

    def forbidden_run(*args, **kwargs):
        raise AssertionError("hostnamectl must not be spawned when absent")

    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(subprocess, "run", forbidden_run)
    assert _hostnamectl_os_release() == {}


@pytest.mark.parametrize(
    "error",
    (
        pytest.param(FileNotFoundError("hostnamectl"), id="binary_missing"),
        pytest.param(PermissionError("hostnamectl"), id="not_executable"),
        pytest.param(
            subprocess.CalledProcessError(1, "hostnamectl"), id="non_zero_exit"
        ),
        pytest.param(
            subprocess.TimeoutExpired("hostnamectl", 2), id="unresponsive_bus"
        ),
    ),
)
def test_hostnamectl_os_release_degrades(error, monkeypatch, fresh_hostnamectl_caches):
    """Every failure to reach the bus degrades to an empty result."""

    def failing_run(*args, **kwargs):
        raise error

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/hostnamectl")
    monkeypatch.setattr(subprocess, "run", failing_run)
    assert _hostnamectl_os_release() == {}


def test_parse_os_release_falls_back_to_hostnamectl(
    monkeypatch, fresh_hostnamectl_caches, fresh_os_release_caches
):
    """A system hiding both os-release files is identified through the bus."""
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/hostnamectl")
    monkeypatch.setattr(subprocess, "run", _fake_run(HOSTNAMECTL_CLOUDLINUX))
    assert _parse_os_release()["id"] == "cloudlinux"
    assert os_release_id() == "cloudlinux"
    assert linux_info() == {
        "id": "cloudlinux",
        "version": "7.6",
        "version_parts": {"major": "7", "minor": "6", "build_number": None},
        "like": None,
        "codename": "Vladimir Lyakhov",
    }


def test_parse_os_release_prefers_files_over_hostnamectl(
    monkeypatch, fresh_hostnamectl_caches, fresh_os_release_caches
):
    """A readable os-release file is never second-guessed through the bus."""

    def forbidden_run(*args, **kwargs):
        raise AssertionError("hostnamectl must not be spawned when a file is readable")

    monkeypatch.setattr(os.path, "isfile", lambda path: path == "/etc/os-release")
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/hostnamectl")
    monkeypatch.setattr(subprocess, "run", forbidden_run)
    monkeypatch.setattr(
        "extra_platforms.platform_info.open",
        lambda *args, **kwargs: io.StringIO("ID=ubuntu\n"),
        raising=False,
    )
    assert _parse_os_release() == {"id": "ubuntu"}


def test_invalidate_os_release_cache_clears_hostnamectl(
    monkeypatch, fresh_hostnamectl_caches
):
    """The hostnamectl result is re-read after a cache invalidation."""
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/hostnamectl")
    monkeypatch.setattr(subprocess, "run", _fake_run(HOSTNAMECTL_CLOUDLINUX))
    assert _hostnamectl_os_release()["id"] == "cloudlinux"

    monkeypatch.setattr(
        subprocess,
        "run",
        _fake_run("  Operating System: Fedora Linux 39\n"),
    )
    # The cached CloudLinux answer is still served before invalidation.
    assert _hostnamectl_os_release()["id"] == "cloudlinux"

    invalidate_os_release_cache()
    assert _hostnamectl_os_release() == {"pretty_name": "Fedora Linux 39"}
