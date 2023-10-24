from argparse import ArgumentParser
from importlib.metadata import version
from typing import List

from dependabot_alerts.core import GitHubClient, Vulnerability, fetch_alerts


def cli(_argv=None):  # pragma: no cover
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("organization", help="GitHub user or organization")

    args = parser.parse_args(_argv)

    if args.version:
        print(version("dependabot-alerts"))
        return 0

    gh_client = GitHubClient.init()
    vulns = fetch_alerts(gh_client, args.organization)
    print(format_slack_message(args.organization, vulns))

    return 0


def format_slack_message(
    organization: str, vulns: List[Vulnerability]
) -> str:  # pragma: no cover
    """
    Format a Slack status report from a list of vulnerabilities.

    Returns a message using Slack's "mrkdwn" format. See
    https://api.slack.com/reference/surfaces/formatting.
    """
    if not vulns:
        return "Found no open vulnerabilities."

    n_repos = len(set(vuln.repo for vuln in vulns))

    msg_parts = []
    msg_parts.append(f"*Found {len(vulns)} vulnerabilities in {n_repos} repositories.*")

    for vuln in vulns:
        vuln_msg = []
        vuln_msg.append(
            f"{organization}/{vuln.repo}: <{vuln.url}|{vuln.package_name} {vuln.severity} - {vuln.title}>"
        )
        if vuln.pr:
            vuln_msg.append(f"  Resolved by {vuln.pr}")
        msg_parts.append("\n".join(vuln_msg))

    return "\n\n".join(msg_parts)
