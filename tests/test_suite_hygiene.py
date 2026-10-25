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
"""Checks on the test suite itself, rather than on the package."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _collect(hash_seed: str) -> list[str]:
    """Collect the whole suite in a fresh interpreter, with pytest-randomly off."""
    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "--quiet",
            "-p",
            "no:randomly",
            "-p",
            "no:cacheprovider",
            str(Path(__file__).parent),
        ),
        capture_output=True,
        text=True,
        encoding="UTF-8",
        env={**os.environ, "PYTHONHASHSEED": hash_seed},
        check=True,
    )
    return [line for line in result.stdout.splitlines() if "::" in line]


def test_collection_order_ignores_hash_seed():
    """Every xdist worker must collect the same tests in the same order.

    Each worker is a fresh interpreter with its own hash seed. A parametrize source
    that iterates a `set` or a `frozenset` then yields its cases in a different order
    on each worker, and xdist aborts the session with `Different tests were
    collected`. pytest-randomly hides the problem, because it re-sorts the collected
    items: a packager build that disables it does not.
    """
    first, second = _collect("1"), _collect("2")
    assert sorted(first) == sorted(second)
    unstable = sorted({a.split("[")[0] for a, b in zip(first, second) if a != b})
    assert not unstable, f"Collection order follows the hash seed in: {unstable}"
