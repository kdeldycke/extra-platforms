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
"""CI definitions and metadata."""

from __future__ import annotations

from .trait import CI

AZURE_PIPELINES = CI(
    "azure_pipelines",
    "Azure Pipelines",
    "═",
    "https://azure.microsoft.com/en-us/products/devops/pipelines/",
)

BAMBOO = CI("bamboo", "Bamboo", "⟲", "https://www.atlassian.com/software/bamboo")

BUILDKITE = CI("buildkite", "Buildkite", "🪁", "https://buildkite.com")

CIRCLE_CI = CI("circle_ci", "Circle CI", "⪾", "https://circleci.com")

CIRRUS_CI = CI("cirrus_ci", "Cirrus CI", "≋", "https://cirrus-ci.org")

CODEBUILD = CI("codebuild", "CodeBuild", "ᚙ", "https://aws.amazon.com/codebuild/")

GITHUB_CI = CI(
    "github_ci", "GitHub Actions runner", "🐙", "https://docs.github.com/en/actions"
)

GITLAB_CI = CI(
    "gitlab_ci",
    "GitLab CI",
    "🦊",
    "https://docs.gitlab.com/topics/build_your_application/",
)

GUIX_BUILD = CI(
    "guix_build",
    "Guix Build",
    "🐂",
    "https://guix.gnu.org/manual/en/html_node/Invoking-guix-build.html",
)

HEROKU_CI = CI(
    "heroku_ci", "Heroku CI", "⥁", "https://www.heroku.com/continuous-integration/"
)

TEAMCITY = CI("teamcity", "TeamCity", "🏙️", "https://www.jetbrains.com/teamcity/")

TRAVIS_CI = CI("travis_ci", "Travis CI", "👷", "https://www.travis-ci.com")

UNKNOWN_CI = CI(
    "unknown_ci",
    "Unknown CI",
    "❓",
    "https://en.wikipedia.org/wiki/Continuous_integration",
)
