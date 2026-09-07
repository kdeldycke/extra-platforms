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

import re
from collections import Counter
from operator import attrgetter
from pathlib import Path
from string import ascii_lowercase, digits

import pytest

import extra_platforms
from extra_platforms import (
    ALL_GROUP_IDS,
    ALL_GROUPS,
    ALL_IDS,
    ALL_PLATFORM_GROUPS,
    ALL_PLATFORMS,
    ALL_TRAIT_IDS,
    ALL_TRAITS,
    CANONICAL_GROUPS,
    CI,
    LINUX,
    UNKNOWN,
    Agent,
    Architecture,
    Group,
    Platform,
    Shell,
    Terminal,
    Trait,
)
from extra_platforms._docs import generate_traits_mindmap


@pytest.mark.parametrize(
    "klass",
    (Architecture, Platform, Shell, Terminal, CI, Agent),
    ids=attrgetter("__name__"),
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


def test_aliases_do_not_conflict_with_trait_ids():
    """Verify no alias conflicts with a canonical trait ID."""
    for trait in ALL_TRAITS:
        for alias in trait.aliases:
            assert alias not in ALL_TRAIT_IDS, (
                f"Alias '{alias}' for trait '{trait.id}' conflicts with "
                f"an existing canonical trait ID."
            )


def test_aliases_do_not_conflict_with_group_ids():
    """Verify no alias conflicts with a group ID."""
    for trait in ALL_TRAITS:
        for alias in trait.aliases:
            assert alias not in ALL_GROUP_IDS, (
                f"Alias '{alias}' for trait '{trait.id}' conflicts with "
                f"an existing group ID."
            )


def test_aliases_are_unique_across_traits():
    """Verify no alias is defined by multiple traits."""
    seen_aliases: dict[str, str] = {}
    for trait in ALL_TRAITS:
        for alias in trait.aliases:
            assert alias not in seen_aliases, (
                f"Alias '{alias}' is defined multiple times: "
                f"by trait '{seen_aliases[alias]}' and trait '{trait.id}'."
            )
            seen_aliases[alias] = trait.id


def test_shared_icons_belong_to_same_canonical_group():
    """Icons are unique across traits and groups, with two exceptions.

    A canonical group may share its icon with its members, but only when *all*
    of them carry it. Traits may also share an icon between themselves,
    provided no group uses that icon and every sharer belongs to the same
    canonical group (`🎩` is both Fedora and RHEL).
    """
    # Collect every (icon, owner) pair for traits and groups.
    icon_owners: dict[str, list[Trait | Group]] = {}
    for trait in ALL_TRAITS:
        icon_owners.setdefault(trait.icon, []).append(trait)
    for group in ALL_GROUPS:
        icon_owners.setdefault(group.icon, []).append(group)

    # Build a lookup: icon -> canonical group whose members all share that icon.
    allowed_icon: dict[str, Group] = {}
    for group in CANONICAL_GROUPS:
        if all(member.icon == group.icon for member in group):
            allowed_icon[group.icon] = group

    for icon, owners in icon_owners.items():
        if len(owners) < 2:
            continue

        # If a canonical group claims this icon, all owners must be that group
        # or one of its members.
        canonical = allowed_icon.get(icon)
        if canonical is not None:
            for owner in owners:
                assert owner is canonical or (
                    isinstance(owner, Trait) and owner in canonical
                ), (
                    f"Icon {icon!r} is reserved for canonical group "
                    f"{canonical.id!r} and its members, but is also used by "
                    f"{owner.id!r}."
                )
            continue

        # Otherwise, no sharing is allowed: all owners must be in the same
        # canonical group and no group may use this icon.
        traits = [o for o in owners if isinstance(o, Trait)]
        groups = [o for o in owners if isinstance(o, Group)]
        assert not groups, (
            f"Icon {icon!r} is shared between group(s) "
            f"{[g.id for g in groups]} and other owners "
            f"{[o.id for o in owners if o not in groups]}, but the group's "
            f"members do not all share this icon."
        )
        canonical_groups = set()
        for trait in traits:
            for group in CANONICAL_GROUPS:
                if trait in group:
                    canonical_groups.add(group.id)
        trait_ids = [t.id for t in traits]
        assert len(canonical_groups) == 1, (
            f"Traits sharing icon {icon!r} span multiple canonical groups: "
            f"traits={trait_ids}, canonical_groups={canonical_groups}"
        )


_TRAIT_IDS = ALL_TRAITS.member_ids
_GROUP_IDS = frozenset(group.id for group in ALL_GROUPS)

_SYMBOL_REF = re.compile(r"\{data\}`~([A-Z0-9_]+)`")

# Hand-written roster tables of the documentation. Each page maps to the first
# characters of the line opening its table, and to the population its rows cover.
_ROSTERS = {
    "detection.md": ("| Detection function", _TRAIT_IDS | _GROUP_IDS),
    "platforms.md": ("| Icon | Symbol", ALL_PLATFORMS.member_ids),
    "pytest.md": ("| Skip decorator", _TRAIT_IDS | _GROUP_IDS),
    "trait.md": ("| Icon | Symbol", _TRAIT_IDS),
}


def _roster_rows(page: str) -> list[tuple[str, list[str]]]:
    """Return the ID and the cells of each data row of the roster table of `page`.

    The ID is the lower-cased symbol the row points at through its `{data}` link.

    :param page: file name of the page, under `docs/`.
    """
    header, _population = _ROSTERS[page]
    doc = Path(__file__).parent.parent / "docs" / page
    lines = doc.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(header))
    rows = []
    # Step over the header and its alignment row, then read the body until the
    # first line that is not a row.
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        match = _SYMBOL_REF.search(line)
        assert match, f"a row of docs/{page} names no symbol: {line}"
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        rows.append((match.group(1).lower(), cells))
    return rows


@pytest.mark.parametrize("page", tuple(_ROSTERS))
def test_doc_roster_covers_its_population(page):
    """Each roster table of the documentation names its whole population.

    These tables are written by hand, and nothing reads them back, so a trait
    added without touching them leaves a hole no build reports: the page just
    lists one platform fewer. The reverse direction matters as much, a row
    outliving its trait pointing at a symbol that no longer resolves.
    """
    _header, population = _ROSTERS[page]
    listed = [row_id for row_id, _cells in _roster_rows(page)]

    repeated = sorted(row_id for row_id, count in Counter(listed).items() if count > 1)
    assert not repeated, f"docs/{page} lists {repeated} more than once"

    assert set(listed) == population, (
        f"docs/{page} disagrees with the code: "
        f"missing {sorted(population - set(listed))}, "
        f"stale {sorted(set(listed) - population)}"
    )


@pytest.mark.parametrize("page", ("platforms.md", "trait.md"))
def test_doc_roster_repeats_icon_and_name(page):
    """The rosters carrying an Icon and a Name column repeat what the code says.

    Copying either into a table forks it, so a renamed trait or a swapped icon
    would otherwise leave the page stating the old value for good.
    """
    by_id = {trait.id: trait for trait in ALL_TRAITS}

    for row_id, cells in _roster_rows(page):
        icon, _symbol, name = cells[:3]
        owner = by_id[row_id]
        assert icon == owner.icon, (
            f"docs/{page} shows icon {icon!r} for {owner.id!r}, which declares "
            f"{owner.icon!r}"
        )
        assert name == owner.name, (
            f"docs/{page} shows name {name!r} for {owner.id!r}, which declares "
            f"{owner.name!r}"
        )


# Roster regions of the readme. The pages above expose Markdown tables, but these
# are console transcripts and a diagram, so each region needs its own extractor.
_README = Path(__file__).parent.parent / "readme.md"


def _readme_block(pattern: str, region: str) -> str:
    """Return the single capture of `pattern` in the readme.

    Failing here keeps a readme restructure from quietly reducing a roster to an
    empty set, which would then be reported as every platform going missing.

    :param pattern: regular expression carrying exactly one capturing group.
    :param region: name of the region, used in the failure message.
    """
    text = _README.read_text(encoding="UTF-8")
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        pytest.fail(f"readme.md no longer holds the {region} block")
    return match.group(1)


def _linux_members_dict() -> frozenset[str]:
    """IDs of the `LINUX.members` mapping the readme prints."""
    block = _readme_block(
        r"^>>> LINUX\.members\nmappingproxy\(\{\n(.*?)^\}\)$", "LINUX.members"
    )
    return frozenset(re.findall(r"^ +'([^']+)': Platform\(", block, re.MULTILINE))


def _linux_member_ids() -> frozenset[str]:
    """IDs of the `LINUX.member_ids` frozenset the readme prints.

    A frozenset repr is hash-ordered, so only its contents carry meaning.
    """
    block = _readme_block(
        r"^>>> LINUX\.member_ids\nfrozenset\(\{(.*?)\}\)$", "LINUX.member_ids"
    )
    return frozenset(re.findall(r"'([^']+)'", block))


def _linux_names() -> frozenset[str]:
    """Platform names the readme prints for the LINUX group."""
    block = _readme_block(
        r'^>>> print\("\\n"\.join\(\[p\.name for p in LINUX\]\)\)\n(.*?)^```$',
        "LINUX names",
    )
    return frozenset(block.strip("\n").split("\n"))


def _all_platforms_mermaid() -> str:
    """Return the mermaid block of the readme holding the platform mindmap.

    The readme carries one mindmap per trait category, so the root node is what
    tells the platform one apart.
    """
    text = _README.read_text(encoding="UTF-8")
    blocks: list[str] = re.findall(
        r"^```mermaid\n.*?^```$", text, re.MULTILINE | re.DOTALL
    )
    for block in blocks:
        if re.search(r"^ +\(\(\S+ ALL_PLATFORMS\)\)$", block, re.MULTILINE):
            return block
    pytest.fail("readme.md no longer holds the ALL_PLATFORMS mindmap")


def _all_platforms_mindmap() -> frozenset[str]:
    """Trait symbols the platform mindmap of the readme names.

    Groups render as `)icon SYMBOL(` and traits as `(icon SYMBOL)`, so only the
    latter are collected.
    """
    return frozenset(
        re.findall(r"^ +\(\S+ ([A-Z0-9_]+)\)$", _all_platforms_mermaid(), re.MULTILINE)
    )


_README_ROSTERS = {
    "LINUX.members dict": (_linux_members_dict, LINUX.member_ids),
    "LINUX.member_ids frozenset": (_linux_member_ids, LINUX.member_ids),
    "LINUX names list": (
        _linux_names,
        frozenset(platform.name for platform in LINUX),
    ),
    "ALL_PLATFORMS mindmap": (
        _all_platforms_mindmap,
        frozenset(platform.symbol_id for platform in ALL_PLATFORMS),
    ),
}


@pytest.mark.parametrize("region", tuple(_README_ROSTERS))
def test_readme_roster_covers_its_population(region):
    """Each roster region of the readme names its whole population.

    These regions are pasted by hand and nothing reads them back, so a trait
    added without touching the readme leaves a hole no build reports. The
    reverse direction matters as much, an entry outliving the trait it names.
    """
    extract, population = _README_ROSTERS[region]
    listed = extract()

    assert listed == population, (
        f"readme.md {region} disagrees with the code: "
        f"missing {sorted(population - listed)}, "
        f"stale {sorted(listed - population)}"
    )


def test_readme_mindmap_matches_its_generator():
    """The platform mindmap of the readme still matches what produces it.

    The readme pastes the output of `generate_traits_mindmap()` under a
    `mirror-src` comment holding the call that produced it. Comparing the block
    against a fresh call catches what a roster check cannot: a swapped icon, a
    renamed group, or a trait that moved between groups.
    """
    expected = generate_traits_mindmap(
        list(CANONICAL_GROUPS & ALL_PLATFORM_GROUPS) + [ALL_PLATFORMS]
    )
    assert _all_platforms_mermaid() == expected
