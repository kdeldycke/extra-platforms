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
