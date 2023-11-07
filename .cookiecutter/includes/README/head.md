`dependabot-alerts` lists Dependabot security alerts for all repos of a GitHub
organization. You can run it from the command line:

```terminal
$ dependabot-alerts <your_github_organization>
```

You'll need to have [GitHub CLI](https://cli.github.com/) installed and logged in.

There's also a [GitHub Actions workflow](.github/workflows/alert.yml) that runs
automatically on a schedule and notifies us in Slack of any Dependabot alerts
in the `hypothesis` GitHub organization.
