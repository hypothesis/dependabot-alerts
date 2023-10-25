import subprocess
from argparse import ArgumentParser
from importlib.metadata import version

from dependabot_alerts.core import GitHub
from dependabot_alerts.format import format_slack, format_text


def cli(argv=None):
    parser = ArgumentParser()
    parser.add_argument(
        "-v", "--version", action="version", version=version("dependabot-alerts")
    )
    parser.add_argument(
        "--format", choices=["text", "slack"], default="text", help="output format"
    )
    parser.add_argument("organization", help="GitHub organization")
    args = parser.parse_args(argv)

    alerts = GitHub(subprocess.run).alerts(args.organization)

    formatters = {
        "text": format_text,
        "slack": format_slack,
    }

    formatter = formatters[args.format]

    output = formatter(alerts, args.organization)

    if output:
        print(output)
