from importlib.metadata import version

import pytest

from dependabot_alerts.cli import cli


def test_it(GitHub, github, subprocess, capsys, format_text):
    cli(["test-organization"])

    GitHub.assert_called_once_with(subprocess.run)
    github.alerts.assert_called_once_with("test-organization", ignore=[])
    format_text.assert_called_once_with(github.alerts.return_value, "test-organization")
    captured = capsys.readouterr()
    assert captured.out == f"{format_text.return_value}\n"
    assert not captured.err


def test_format_slack(capsys, github, format_slack):
    cli(["--format", "slack", "test-organization"])

    format_slack.assert_called_once_with(
        github.alerts.return_value, "test-organization"
    )
    captured = capsys.readouterr()
    assert captured.out == f"{format_slack.return_value}\n"


def test_it_ignores_repositories(GitHub, github, subprocess):
    cli(
        [
            "--ignore-repo",
            "org/repo1",
            "--ignore-repo",
            "org/repo2",
            "test-organization",
        ]
    )

    GitHub.assert_called_once_with(subprocess.run)
    github.alerts.assert_called_once_with(
        "test-organization", ignore=["org/repo1", "org/repo2"]
    )


def test_it_prints_nothing_if_there_are_no_alerts(capsys, format_text):
    format_text.return_value = None

    cli(["test-organization"])

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err


def test_it_crashes_if_no_organization_argument_is_given(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli([])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert not captured.out
    assert "error: the following arguments are required: organization" in captured.err


def test_it_crashes_if_an_invalid_format_is_given(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli(["--format", "foo", "organization"])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert not captured.out
    assert "error: argument --format: invalid choice: 'foo'" in captured.err


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


def test_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli(["--version"])

    assert capsys.readouterr().out.strip() == version("dependabot-alerts")
    assert not exc_info.value.code


@pytest.fixture(autouse=True)
def GitHub(mocker):
    return mocker.patch("dependabot_alerts.cli.GitHub")


@pytest.fixture
def github(GitHub):
    return GitHub.return_value


@pytest.fixture(autouse=True)
def format_slack(mocker):
    return mocker.patch("dependabot_alerts.cli.format_slack")


@pytest.fixture(autouse=True)
def format_text(mocker):
    return mocker.patch("dependabot_alerts.cli.format_text")


@pytest.fixture(autouse=True)
def subprocess(mocker):
    return mocker.patch("dependabot_alerts.cli.subprocess")
