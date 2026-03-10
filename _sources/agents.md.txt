# {octicon}`dependabot` Agents

```{py:currentmodule} extra_platforms
```

Each agent represents an AI coding agent environment, and is associated with:

- a unique agent ID
- a human-readable name
- an icon (emoji / unicode character)
- a [detection function](detection.md)
- various metadata in its `info()` method

## Agent usage

Each agent is materialized by a {class}`~Agent` object, from which you can access various metadata:

```pycon
>>> from extra_platforms import CLAUDE_CODE
>>> CLAUDE_CODE
Agent(id='claude_code', name='Claude Code')
>>> CLAUDE_CODE.id
'claude_code'
>>> CLAUDE_CODE.current
False
>>> CLAUDE_CODE.info()
{'id': 'claude_code', 'name': 'Claude Code', 'icon': '✴️', 'url': 'https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview', 'current': False}
```

To check if the current environment is running in a specific agent, use the corresponding [detection function](detection.md):

```pycon
>>> from extra_platforms import is_claude_code
>>> is_claude_code()
False
```

The current agent can be obtained via the `current_agent()` function:

```pycon
>>> from extra_platforms import current_agent
>>> current_agent()
Agent(id='unknown_agent', name='Unknown agent')
```

## Recognized agents

<!-- agent-table-start -->

| Icon | Symbol                | Name       | Detection function       |
| :--: | :-------------------- | :--------- | :----------------------- |
|  ✴️  | {data}`~CLAUDE_CODE`  | Claude Code | {func}`~is_claude_code` |
|  👾  | {data}`~CLINE`        | Cline      | {func}`~is_cline`       |
|  ➤  | {data}`~CURSOR`       | Cursor     | {func}`~is_cursor`      |

```{hint}
The {data}`~UNKNOWN_AGENT` trait represents an unrecognized
agent. It is not included in the {data}`~ALL_AGENTS` group,
and will be returned by {func}`~current_agent` if the current
agent is not recognized.
```

<!-- agent-table-end -->

## Groups of agents

There is only one group defined for agents: `ALL_AGENTS`, which includes all recognized agents.

<!-- agent-groups-table-start -->

| Icon | Symbol              | Description | [Detection](detection.md) | {attr}`Canonical <Group.canonical>` |
| :--: | :------------------ | :---------- | :------------------------ | :---------------------------------: |
|  🧠  | {data}`~ALL_AGENTS` | Agents      | {func}`~is_any_agent`     |                  ⬥                  |

<!-- agent-groups-table-end -->

<!-- agent-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 400}}
---
sankey-beta

ALL_AGENTS,CLAUDE_CODE,1
ALL_AGENTS,CLINE,1
ALL_AGENTS,CURSOR,1
```

<!-- agent-sankey-end -->

<!-- agent-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((🧠 ALL_AGENTS))
        (✴️ CLAUDE_CODE)
        (👾 CLINE)
        (➤ CURSOR)
```

<!-- agent-mindmap-end -->

## Predefined agents

```{eval-rst}
.. autoclasstree:: extra_platforms.agent_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.agent_data
   :no-index:
```

<!-- agent-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.CLAUDE_CODE
.. autodata:: extra_platforms.CLINE
.. autodata:: extra_platforms.CURSOR
.. autodata:: extra_platforms.UNKNOWN_AGENT
```

<!-- agent-data-autodata-end -->
