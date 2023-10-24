from subprocess import run


def test_help():
    """Test the dependabot-alerts --help command."""
    run(["dependabot-alerts", "--help"], check=True)
