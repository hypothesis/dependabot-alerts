from importlib.metadata import version

import pytest

from dependabot_alerts.cli import cli


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


@pytest.mark.xfail
def test_version(capsys):  # pragma: no cover
    exit_code = cli(["--version"])

    assert capsys.readouterr().out.strip() == version("dependabot-alerts")
    assert not exit_code
