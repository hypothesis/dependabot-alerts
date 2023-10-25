import json
import os
from dataclasses import dataclass
from typing import Optional

import requests


class GitHubClient:  # pragma: no cover
    """
    Client for GitHub's GraphQL API.

    See https://docs.github.com/en/graphql.
    """

    def __init__(self, token):
        self.token = token
        self.endpoint = "https://api.github.com/graphql"

    def query(self, query, variables=None):
        data = {"query": query, "variables": variables if variables is not None else {}}
        result = requests.post(
            url=self.endpoint,
            headers={"Authorization": f"Bearer {self.token}"},
            data=json.dumps(data),
            timeout=(30, 30),
        )
        body = result.json()
        result.raise_for_status()
        if "errors" in body:
            errors = body["errors"]
            raise RuntimeError(f"Query failed: {json.dumps(errors)}")
        return body["data"]

    @classmethod
    def init(cls):
        """
        Initialize an authenticated GitHubClient.

        This will read from the `GITHUB_TOKEN` env var if set, or prompt for
        a token otherwise.
        """
        access_token = os.environ["GITHUB_TOKEN"]
        return GitHubClient(access_token)


@dataclass
class Vulnerability:  # pylint:disable=too-many-instance-attributes
    repo: str
    """Repository where this vulnerability was reported."""

    created_at: str
    """ISO date when this alert was created."""

    package_name: str
    """Name of the vulnerable package."""

    ecosystem: str
    """Package ecosytem (eg. npm) that the package comes from."""

    severity: str
    """Vulnerability severity level."""

    version_range: str
    """Version ranges of package affected by vulnerability."""

    number: str
    """Number of this vulnerability report."""

    url: str
    """Link to the vulernability report on GitHub."""

    pr: Optional[str]
    """Link to the Dependabot update PR that resolves this vulnerability."""

    title: str
    """Summary of what the vulnerability is."""


def fetch_alerts(
    gh: GitHubClient, organization: str
) -> list[Vulnerability]:  # pragma: no cover
    """
    Fetch details of all open vulnerability alerts in `organization`.

    To reduce the volume of noise, especially for repositories which include the
    same dependency in multiple lockfiles, only one vulnerability is reported
    per package per repository.

    Vulnerabilities are not reported from archived repositories.
    """
    # pylint:disable=too-many-locals

    query = """
query($organization: String!, $cursor: String) {
  organization(login: $organization) {
    repositories(first: 100, after: $cursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        name
        vulnerabilityAlerts(first: 100, states:OPEN) {
          nodes {
            number
            createdAt
            dependabotUpdate {
              pullRequest {
                url
              }
            }
            securityAdvisory {
              summary
            }
            securityVulnerability {
              package {
                name
                ecosystem
              }
              severity
              vulnerableVersionRange
            }
          }
        }
      }
    }
  }
}
"""

    vulns = []
    cursor = None
    has_next_page = True

    while has_next_page:
        result = gh.query(
            query=query, variables={"organization": organization, "cursor": cursor}
        )
        page_info = result["organization"]["repositories"]["pageInfo"]
        cursor = page_info["endCursor"]
        has_next_page = page_info["hasNextPage"]

        for repo in result["organization"]["repositories"]["nodes"]:
            alerts = repo["vulnerabilityAlerts"]["nodes"]

            if alerts:
                repo_name = repo["name"]
                vulnerable_packages = set()

                for alert in alerts:
                    sa = alert["securityAdvisory"]
                    sv = alert["securityVulnerability"]
                    number = alert["number"]
                    package_name = sv["package"]["name"]

                    if package_name in vulnerable_packages:
                        continue
                    vulnerable_packages.add(package_name)

                    pr = None

                    dep_update = alert["dependabotUpdate"]
                    if dep_update and dep_update["pullRequest"]:
                        pr = dep_update["pullRequest"]["url"]

                    vuln = Vulnerability(
                        repo=repo_name,
                        created_at=alert["createdAt"],
                        ecosystem=sv["package"]["ecosystem"],
                        number=number,
                        package_name=sv["package"]["name"],
                        pr=pr,
                        severity=sv["severity"],
                        title=sa["summary"],
                        url=f"https://github.com/{organization}/{repo_name}/security/dependabot/{number}",
                        version_range=sv["vulnerableVersionRange"],
                    )
                    vulns.append(vuln)

    return vulns
