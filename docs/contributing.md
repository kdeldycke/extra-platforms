# {octicon}`git-pull-request` Contribution guide

To add a new Linux distribution, you can get inspiration from these pull requests:

- [#156](https://github.com/kdeldycke/extra-platforms/pull/156)
- [#94](https://github.com/kdeldycke/extra-platforms/pull/94)

## Documentation build

`docs/conf.py` holds an `anchor_viewcode_backlinks` build hook for a bug of Sphinx's `viewcode`. `click_extra.sphinx` registers the same hook since `10.4.0`, and `docs/conf.py` connects it a second time. Without that second pass, one parallel build in five logged `click_extra.dead_link` warnings for the `[source]` anchors of `is_webos`, `is_omarchy`, `machine_architecture` and `webos_info`.

```{todo}
Delete the `anchor_viewcode_backlinks` hook of `docs/conf.py` once [sphinx-doc/sphinx#14815](https://github.com/sphinx-doc/sphinx/pull/14815) ships, or once the `click_extra.dead_link` warnings of a parallel build without it are explained and fixed in click-extra.
```

## `AGENTS.md` file

```{include} ../AGENTS.md
:start-line: 2
```
