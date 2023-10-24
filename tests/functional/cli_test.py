from subprocess import run

import pytest


def test_help():
    """Test the dependabot-alerts --help command."""
    run(["dependabot-alerts", "--help"], check=True)


@pytest.mark.xfail
def test_version():
    """Test the dependabot-alerts --version command."""
    run(["dependabot-alerts", "--version"], check=True)
