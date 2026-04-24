# {octicon}`terminal` CLI

```{py:currentmodule} extra_platforms
```

The `extra-platforms` command-line tool detects and reports the architecture, platform, shell, terminal, CI system, and agent of the current environment.

## Invocation

`````{tab-set}

````{tab-item} uvx (no install)
```{code-block} shell-session
$ uvx extra-platforms
```
````

````{tab-item} Installed package
```{code-block} shell-session
$ extra-platforms
```
````

````{tab-item} Python module
```{code-block} shell-session
$ python -m extra_platforms
```
````

````{tab-item} uv run (development)
```{code-block} shell-session
$ uv run extra-platforms
```
````
`````

## Options

`--help`
: Show usage information and exit.

`--version`
: Print the package version and exit.

`--json`
: Output results as JSON instead of the default human-readable format. Useful for scripting and piping into tools like `jq`.

## Default output

The default output prints each detected trait with its metadata, followed by summary tables of all detected traits and groups:

```{code-block} shell-session
$ extra-platforms
extra-platforms 11.2.0

── Architecture ── 📱 ARM64 (AArch64) ──[AARCH64]────────────
            id: aarch64
       aliases: arm64
          name: ARM64 (AArch64)
          icon: 📱
           url: https://en.wikipedia.org/wiki/AArch64
       current: True
       machine: arm64
        symbol: AARCH64
     detection: is_aarch64()
        pytest: @skip_aarch64, @unless_aarch64
        groups: ALL_ARCHITECTURES, ALL_ARM, ARCH_64_BIT, LITTLE_ENDIAN

── Platform ── 🍎 macOS ──[MACOS]────────────────────────────
            id: macos
          (...)
```

## JSON output

The `--json` flag produces a single JSON object with all detected traits and groups:

```{code-block} shell-session
$ extra-platforms --json
```

```{code-block} json
{
  "version": "11.2.0",
  "architecture": {
    "id": "aarch64",
    "name": "ARM64 (AArch64)",
    "icon": "📱",
    "url": "https://en.wikipedia.org/wiki/AArch64",
    "current": true,
    "machine": "arm64",
    "processor": null,
    "aliases": ["arm64"],
    "symbol": "AARCH64",
    "detection": "is_aarch64",
    "groups": ["ALL_ARCHITECTURES", "ALL_ARM", "ARCH_64_BIT", "LITTLE_ENDIAN"]
  },
  "platform": { "..." : "..." },
  "shell": { "..." : "..." },
  "terminal": { "..." : "..." },
  "ci": { "..." : "..." },
  "agent": { "..." : "..." },
  "groups": [
    {
      "id": "all_arm",
      "name": "ARM architectures",
      "icon": "📱",
      "symbol": "ALL_ARM",
      "detection": "is_any_arm",
      "canonical": true
    }
  ]
}
```

Each trait section contains:

| Field | Description |
| ----- | ----------- |
| {attr}`id <Trait.id>` | Unique trait identifier |
| {attr}`name <Trait.name>` | Human-readable name |
| {attr}`icon <Trait.icon>` | Single-glyph icon |
| {attr}`url <Trait.url>` | Reference URL |
| {attr}`current <Trait.current>` | Whether this trait matches the current environment |
| {attr}`aliases <Trait.aliases>` | Alternative IDs for this trait |
| {attr}`symbol <Trait.symbol_id>` | Uppercase symbol for Python imports (`from extra_platforms import AARCH64`) |
| {attr}`detection <Trait.detection_func_id>` | Detection function name (`from extra_platforms import is_aarch64`) |
| {attr}`groups <Trait.groups>` | Groups this trait belongs to |

Trait-specific fields (like `machine`, `version`, `codename`) are included when available.

### Scripting examples

Extract the current platform ID:

```{code-block} shell-session
$ extra-platforms --json | jq --raw-output .platform.id
macos
```

List all detected group names:

```{code-block} shell-session
$ extra-platforms --json | jq --raw-output '.groups[].name'
ARM architectures
All BSD
All Unix
(...)
```

Check if running in CI:

```{code-block} shell-session
$ extra-platforms --json | jq '.ci.id != "unknown_ci"'
false
```
