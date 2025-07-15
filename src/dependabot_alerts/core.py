from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from subprocess import CalledProcessError


@dataclass(frozen=True)
class Alert:  # pylint:disable=too-many-instance-attributes
    repo_full_name: str | None
    ghsa_id: str | None
    html_url: str | None = field(compare=False)
    package: str | None = field(compare=False)
    manifest_path: str | None = field(compare=False)
    summary: str | None = field(compare=False)
    severity: str | None = field(compare=False)
    duplicates: list[Alert] = field(compare=False, default_factory=list)

    @classmethod
    def make(cls, alert_dict):
        return cls(
            repo_full_name=alert_dict["repository"]["full_name"],
            ghsa_id=alert_dict["security_advisory"]["ghsa_id"],
            html_url=alert_dict["html_url"],
            package=alert_dict["dependency"]["package"]["name"],
            manifest_path=alert_dict["dependency"]["manifest_path"],
            summary=alert_dict["security_advisory"]["summary"],
            severity=alert_dict["security_advisory"]["severity"],
        )


class GitHub:
    def __init__(self, run):
        self._run = run

    def alerts(self, organization, ignore=None) -> list[Alert]:
        try:
            result = self._run(
                [
                    "gh",
                    "api",
                    "--paginate",
                    f"/orgs/{organization}/dependabot/alerts?state=open",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except CalledProcessError as err:  # pragma: no cover
            for line in err.stdout.splitlines():
                print(f"GitHub CLI stdout> {line}")
            for line in err.stderr.splitlines():
                print(f"GitHub CLI stderr> {line}", file=sys.stderr)
            raise

        alert_dicts = json.loads(result.stdout)

        alerts: dict[Alert, Alert] = {}
        ignore = ignore or []

        for alert_dict in alert_dicts:
            alert = Alert.make(alert_dict)

            # Skip alerts from ignored repositories
            if alert.repo_full_name in ignore:
                continue

            if alert in alerts:
                alerts[alert].duplicates.append(alert)
            else:
                alerts[alert] = alert

        return list(alerts.values())
