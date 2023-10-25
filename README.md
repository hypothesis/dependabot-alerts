<a href="https://github.com/hypothesis/dependabot-alerts/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/dependabot-alerts/ci.yml?branch=main"></a>
<a><img src="https://img.shields.io/badge/python-3.12 | 3.11-success"></a>
<a href="https://github.com/hypothesis/dependabot-alerts/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# Dependabot Alerts

Notifications of Dependabot alerts across a GitHub organization.

`dependabot-alerts` lists Dependabot security alerts for all repos of a GitHub
organization. You can run it from the command line:

```terminal
$ dependabot-alerts <your_github_organization>
```

You'll need to have [GitHub CLI](https://cli.github.com/) installed and logged in.

There's also a [GitHub Actions workflow](.github/workflows/alert.yml) that runs
automatically on a schedule and notifies us in Slack of any Dependabot alerts
in the `hypothesis` GitHub organization.

## Installing

We recommend using [pipx](https://pypa.github.io/pipx/) to install
Dependabot Alerts.
First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

```terminal
pipx install git+https://github.com/hypothesis/dependabot-alerts.git
```

You now have Dependabot Alerts installed! For some help run:

```
dependabot-alerts --help
```

## Upgrading

To upgrade to the latest version run:

```terminal
pipx upgrade dependabot-alerts
```

To see what version you have run:

```terminal
dependabot-alerts --version
```

## Uninstalling

To uninstall run:

```
pipx uninstall dependabot-alerts
```

## Setting up Your Dependabot Alerts Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/dependabot-alerts.git
cd dependabot-alerts
make help
```

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request
