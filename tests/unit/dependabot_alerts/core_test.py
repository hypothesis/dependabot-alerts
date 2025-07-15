import json
import subprocess
from unittest.mock import Mock, create_autospec

import pytest

from dependabot_alerts.core import GitHub


class TestGitHub:
    def test_alerts(self, github, run, alert_factory, alert_dict_factory):
        run.return_value = Mock(
            stdout=json.dumps(
                [
                    *alert_dict_factory.create_batch(
                        size=2,
                        organization="hypothesis",
                        repo="foo",
                        ghsa_id="GHSA-1",
                    ),
                    alert_dict_factory(
                        organization="hypothesis",
                        repo="foo",
                        ghsa_id="GHSA-2",
                    ),
                    alert_dict_factory(
                        organization="hypothesis",
                        repo="bar",
                        ghsa_id="GHSA-1",
                    ),
                ]
            )
        )

        repos = github.alerts("hypothesis")

        run.assert_called_once_with(
            [
                "gh",
                "api",
                "--paginate",
                "/orgs/hypothesis/dependabot/alerts?state=open",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        assert repos == [
            alert_factory(
                organization="hypothesis",
                repo="foo",
                ghsa_id="GHSA-1",
                duplicates=1,
            ),
            alert_factory(
                organization="hypothesis",
                repo="foo",
                ghsa_id="GHSA-2",
            ),
            alert_factory(
                organization="hypothesis",
                repo="bar",
                ghsa_id="GHSA-1",
            ),
        ]

    def test_alerts_returns_an_empty_dict_if_there_are_no_alerts(self, github, run):
        run.return_value = Mock(stdout=json.dumps([]))
        assert github.alerts("hypothesis") == []

    def test_alerts_filters_ignored_repositories(
        self, github, run, alert_factory, alert_dict_factory
    ):
        run.return_value = Mock(
            stdout=json.dumps(
                [
                    alert_dict_factory(
                        organization="hypothesis",
                        repo="foo",
                        ghsa_id="GHSA-1",
                    ),
                    alert_dict_factory(
                        organization="hypothesis",
                        repo="ignored-repo",
                        ghsa_id="GHSA-2",
                    ),
                    alert_dict_factory(
                        organization="hypothesis",
                        repo="bar",
                        ghsa_id="GHSA-3",
                    ),
                ]
            )
        )

        repos = github.alerts("hypothesis", ignore=["hypothesis/ignored-repo"])

        assert repos == [
            alert_factory(
                organization="hypothesis",
                repo="foo",
                ghsa_id="GHSA-1",
            ),
            alert_factory(
                organization="hypothesis",
                repo="bar",
                ghsa_id="GHSA-3",
            ),
        ]

    @pytest.fixture
    def run(self):
        return create_autospec(subprocess.run)

    @pytest.fixture
    def github(self, run):
        return GitHub(run)
