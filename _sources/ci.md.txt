# {octicon}`container` CI systems

Each CI system represents a continuous integration/delivery platform, and is associated with:

- a unique CI ID
- a human-readable name
- an icon (emoji / unicode character)
- a [detection function](detection.md)
- various metadata in its `info()` method

Each CI system is materialized by a [`CI` object](#extra_platforms.ci.CI), from which you can access various metadata:

```pycon
>>> from extra_platforms import GITHUB_CI
>>> GITHUB_CI
CI(id='github_ci', name='GitHub Actions runner')
>>> GITHUB_CI.id
'github_ci'
>>> GITHUB_CI.current
False
>>> GITHUB_CI.info()
{'id': 'github_ci', 'name': 'GitHub Actions runner', 'icon': '🐙', 'url': 'https://docs.github.com/en/actions', 'current': False}
```

To check if the current environment is running in a specific CI system, use the corresponding [detection function](detection.md):

```pycon
>>> from extra_platforms import is_github_ci
>>> is_github_ci()
False
```

The current CI system can be obtained via the `current_ci()` function:

```pycon
>>> from extra_platforms import current_ci
>>> current_ci()
CI(id='unknown_ci', name='Unknown CI')
```

## Recognized CI

<!-- ci-table-start -->

|  Icon  | Symbol                                                        | Name                  | Detection function                                                                  |
| :--: | :------------------------------------------------------------ | :-------------------- | :---------------------------------------------------------------------------------- |
|   ═    | [`AZURE_PIPELINES`](#extra_platforms.ci_data.AZURE_PIPELINES) | Azure Pipelines       | [`is_azure_pipelines()`](detection.md#extra_platforms.detection.is_azure_pipelines) |
|   ⟲    | [`BAMBOO`](#extra_platforms.ci_data.BAMBOO)                   | Bamboo                | [`is_bamboo()`](detection.md#extra_platforms.detection.is_bamboo)                   |
|   🪁   | [`BUILDKITE`](#extra_platforms.ci_data.BUILDKITE)             | Buildkite             | [`is_buildkite()`](detection.md#extra_platforms.detection.is_buildkite)             |
|   ⪾    | [`CIRCLE_CI`](#extra_platforms.ci_data.CIRCLE_CI)             | Circle CI             | [`is_circle_ci()`](detection.md#extra_platforms.detection.is_circle_ci)             |
|   ≋    | [`CIRRUS_CI`](#extra_platforms.ci_data.CIRRUS_CI)             | Cirrus CI             | [`is_cirrus_ci()`](detection.md#extra_platforms.detection.is_cirrus_ci)             |
|   ᚙ    | [`CODEBUILD`](#extra_platforms.ci_data.CODEBUILD)             | CodeBuild             | [`is_codebuild()`](detection.md#extra_platforms.detection.is_codebuild)             |
|   🐙   | [`GITHUB_CI`](#extra_platforms.ci_data.GITHUB_CI)             | GitHub Actions runner | [`is_github_ci()`](detection.md#extra_platforms.detection.is_github_ci)             |
|   🦊   | [`GITLAB_CI`](#extra_platforms.ci_data.GITLAB_CI)             | GitLab CI             | [`is_gitlab_ci()`](detection.md#extra_platforms.detection.is_gitlab_ci)             |
|   ⥁    | [`HEROKU_CI`](#extra_platforms.ci_data.HEROKU_CI)             | Heroku CI             | [`is_heroku_ci()`](detection.md#extra_platforms.detection.is_heroku_ci)             |
|   🏙️   | [`TEAMCITY`](#extra_platforms.ci_data.TEAMCITY)               | TeamCity              | [`is_teamcity()`](detection.md#extra_platforms.detection.is_teamcity)               |
|   👷   | [`TRAVIS_CI`](#extra_platforms.ci_data.TRAVIS_CI)             | Travis CI             | [`is_travis_ci()`](detection.md#extra_platforms.detection.is_travis_ci)             |

```{hint}
The [`UNKNOWN_CI`](#extra_platforms.ci_data.UNKNOWN_CI) trait represents an unrecognized CI system. It is not included in the [`ALL_CI`](groups.md#extra_platforms.group_data.ALL_CI) group, and will be returned by `current_ci()` if the current CI system is not recognized.
```

<!-- ci-table-end -->

## Groups of CI

There is only one group defined for CI systems: `ALL_CI`, which includes all recognized CI systems.

<!-- ci-sankey-start -->

```mermaid
---
config: {"sankey": {"showValues": false, "width": 800, "height": 800}}
---
sankey-beta

ALL_CI,AZURE_PIPELINES,1
ALL_CI,BAMBOO,1
ALL_CI,BUILDKITE,1
ALL_CI,CIRCLE_CI,1
ALL_CI,CIRRUS_CI,1
ALL_CI,CODEBUILD,1
ALL_CI,GITHUB_CI,1
ALL_CI,GITLAB_CI,1
ALL_CI,HEROKU_CI,1
ALL_CI,TEAMCITY,1
ALL_CI,TRAVIS_CI,1
```

<!-- ci-sankey-end -->

<!-- ci-mindmap-start -->

```mermaid
---
config: {"mindmap": {"padding": 5}}
---
mindmap
    ((♺ ALL_CI))
        (═ AZURE_PIPELINES)
        (⟲ BAMBOO)
        (🪁 BUILDKITE)
        (⪾ CIRCLE_CI)
        (≋ CIRRUS_CI)
        (ᚙ CODEBUILD)
        (🐙 GITHUB_CI)
        (🦊 GITLAB_CI)
        (⥁ HEROKU_CI)
        (🏙️ TEAMCITY)
        (👷 TRAVIS_CI)
```

<!-- ci-mindmap-end -->

## `extra_platforms.ci_data` API

```{eval-rst}
.. autoclasstree:: extra_platforms.ci_data
   :strict:
```

```{eval-rst}
.. automodule:: extra_platforms.ci_data
```

<!-- ci-data-autodata-start -->

```{eval-rst}
.. autodata:: extra_platforms.ci_data.AZURE_PIPELINES
.. autodata:: extra_platforms.ci_data.BAMBOO
.. autodata:: extra_platforms.ci_data.BUILDKITE
.. autodata:: extra_platforms.ci_data.CIRCLE_CI
.. autodata:: extra_platforms.ci_data.CIRRUS_CI
.. autodata:: extra_platforms.ci_data.CODEBUILD
.. autodata:: extra_platforms.ci_data.GITHUB_CI
.. autodata:: extra_platforms.ci_data.GITLAB_CI
.. autodata:: extra_platforms.ci_data.HEROKU_CI
.. autodata:: extra_platforms.ci_data.TEAMCITY
.. autodata:: extra_platforms.ci_data.TRAVIS_CI
.. autodata:: extra_platforms.ci_data.UNKNOWN_CI
```

<!-- ci-data-autodata-end -->
