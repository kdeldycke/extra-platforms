# {octicon}`git-pull-request` Contribution guide

To add a new Linux distribution, you can get inspiration from these pull requests:

- [#156](https://github.com/kdeldycke/extra-platforms/pull/156)
- [#94](https://github.com/kdeldycke/extra-platforms/pull/94)

## Documentation build

`docs/conf.py` holds three build hooks for bugs of Sphinx and sphinxext-opengraph. A comment above each hook links its upstream fix.

```{todo}
Delete the `anchor_viewcode_backlinks`, `sort_todos` and `strip_title_icon_gap` hooks of `docs/conf.py`, with the `OCTICON_TITLE_GAP` pattern, once a click-extra release registers them in `click_extra.sphinx`. In the same change, raise the `click-extra[sphinx]` floor of the `docs` group to that release.
```

## `AGENTS.md` file

```{include} ../AGENTS.md
:start-line: 2
```
