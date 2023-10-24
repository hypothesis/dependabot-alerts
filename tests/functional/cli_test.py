from subprocess import run


def test_help():
    """Test the dependabot-alerts --help command."""
    run(["dependabot-alerts", "--help"], check=True)


def test_version():
    """Test the dependabot-alerts --version command."""
    run(["dependabot-alerts", "--version"], check=True)
