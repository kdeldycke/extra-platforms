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
"""Helpers shared by multiple test modules."""

from __future__ import annotations

import functools
import json
import os


@functools.cache
def github_runner_os() -> str | None:
    """Returns the OS name as defined in the GitHub Actions matrix context.

    .. caution::
        This only works when running inside a GitHub Actions job that uses a ``matrix``
        strategy with an ``os`` variant. Which is the case for the ``extra-platforms``
        workflows.
    """
    matrix_context_str = os.environ.get("EXTRA_PLATFORMS_TEST_MATRIX", "{}")
    matrix_context = json.loads(matrix_context_str)
    os_value = matrix_context.get("os")
    if isinstance(os_value, str):
        return os_value
    return None
