import pytest

from dependabot_alerts.cli import cli


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code
