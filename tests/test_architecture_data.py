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
from pathlib import Path

from extra_platforms import architecture_data as architecture_data_module


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
