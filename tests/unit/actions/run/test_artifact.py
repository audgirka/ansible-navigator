"""Unit tests for artifact creation. in the run action."""

from __future__ import annotations

import logging
import os
import pathlib
import re

from copy import deepcopy
from dataclasses import dataclass
from re import Pattern
from typing import TYPE_CHECKING
from typing import Any

import pytest

from ansible_navigator.utils.functions import expand_path


if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from ansible_navigator.actions.run import Action as action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.initialization import parse_and_update
from tests.defaults import BaseScenario


def make_dirs(*_args: Any, **_kwargs: dict[str, Any]) -> bool:
    """Mock make_dirs.

    Args:
        *_args: The positional arguments
        **_kwargs: The keyword arguments

    Returns:
        Indication of directory creation success
    """
    return True


def get_status(*_args: Any, **_kwargs: dict[str, Any]) -> tuple[str, int]:
    """Mock run.get_status.

    Args:
        *_args: The positional arguments
        **_kwargs: The keyword arguments

    Returns:
        The runner status
    """
    return ("successful", 0)


@dataclass
class Scenario(BaseScenario):
    """The artifact files test data object."""

    # pylint: disable=too-many-instance-attributes

    name: str
    filename: str | None
    playbook: str
    starts_with: str | None = None
    re_match: Pattern[str] | None = None
    help_playbook: bool = False
    enable_prompts: bool = False
    playbook_artifact_enable: bool = True
    time_zone: str = "UTC"

    def __post_init__(self) -> None:
        """Ensure one match is set.

        Raises:
            ValueError: When neither is set
        """
        if not (self.re_match or self.starts_with):
            msg = "re_match or starts_with required"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Provide the test id.

        Returns:
            The test id
        """
        return self.name


test_data = [
    pytest.param(
        Scenario(
            name="Filename absolute",
            filename="/tmp/artifact.json",
            playbook="site.yml",
            starts_with="/tmp/artifact.json",
        ),
    ),
    pytest.param(
        Scenario(
            name="Filename with .",
            filename="./artifact.json",
            playbook="site.yml",
            starts_with=f"{expand_path('.')}/artifact.json",
        ),
    ),
    pytest.param(
        Scenario(
            name="Filename with ..",
            filename="../artifact.json",
            playbook="site.yml",
            starts_with=f"{expand_path('..')}/artifact.json",
        ),
    ),
    pytest.param(
        Scenario(
            name="Filename with ~",
            filename="~/artifact.json",
            playbook="/tmp/site.yaml",
            starts_with="/home/test_user/artifact.json",
        ),
    ),
    pytest.param(
        Scenario(
            name="Playbook absolute",
            filename=None,
            playbook="/tmp/site.yaml",
            starts_with="/tmp/site-artifact",
        ),
    ),
    pytest.param(
        Scenario(
            name="Playbook with .",
            filename=None,
            playbook="./site.yaml",
            starts_with=f"{expand_path('.')}/site-artifact",
        ),
    ),
    pytest.param(
        Scenario(
            name="Playbook with ..",
            filename=None,
            playbook="../site.yaml",
            starts_with=f"{expand_path('..')}/site-artifact",
        ),
    ),
    pytest.param(
        Scenario(
            name="Playbook with ~",
            filename=None,
            playbook="~/site.yaml",
            starts_with="/home/test_user/site-artifact",
        ),
    ),
    pytest.param(
        Scenario(
            name="help_playbook enabled",
            filename=None,
            playbook="~/site.yaml",
            starts_with="/home/test_user/site-artifact",
            help_playbook=True,
            playbook_artifact_enable=False,
        ),
    ),
    pytest.param(
        Scenario(
            name="Check with enable_prompts",
            filename=None,
            playbook="~/site.yaml",
            starts_with="/home/test_user/site-artifact",
            enable_prompts=True,
            playbook_artifact_enable=False,
        ),
    ),
    pytest.param(
        Scenario(
            name="Filename timezone",
            filename="/tmp/{time_stamp}.json",
            playbook="site.yml",
            time_zone="America/Los_Angeles",
            re_match=re.compile("^/tmp/.*-0[7,8]:00"),
        ),
    ),
    pytest.param(
        Scenario(
            name="With status",
            playbook="site.yml",
            filename="/tmp/{playbook_status}/{playbook_name}.json",
            starts_with="/tmp/successful/site.json",
        ),
    ),
]


@pytest.mark.parametrize("data", test_data)
def test_artifact_path(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
    data: Scenario,
) -> None:
    """Test the building of the artifact filename given a filename or playbook.

    Args:
        monkeypatch: The monkeypatch fixture
        mocker: The mocker fixture
        caplog: The log capture fixture
        data: The test data
    """
    caplog.set_level(logging.DEBUG)
    monkeypatch.setenv("HOME", "/home/test_user")
    monkeypatch.setattr(pathlib.Path, "mkdir", make_dirs)
    monkeypatch.setattr(action, "_get_status", get_status)
    mocked_write = mocker.patch(
        "ansible_navigator.actions.run.serialize_write_file",
        return_value=None,
    )

    args = deepcopy(NavigatorConfiguration)
    args.entry("playbook").value.current = data.playbook
    args.entry("help_playbook").value.current = data.help_playbook
    args.entry("time_zone").value.current = data.time_zone
    args.entry("playbook_artifact_enable").value.current = data.playbook_artifact_enable

    save_as = args.entry("playbook_artifact_save_as")

    if data.filename:
        save_as.value.current = data.filename
    else:
        save_as.value.current = save_as.value.default

    assert args.post_processor
    args.post_processor.playbook(
        entry=args.entry("playbook"),
        config=args,
    )
    args.post_processor.playbook_artifact_save_as(
        entry=save_as,
        config=args,
    )

    run_action = action(args=args)
    run_action.write_artifact(filename=data.filename)

    if data.playbook_artifact_enable is True:
        opened_filename = str(mocked_write.call_args[1]["file"])
        if data.starts_with is not None:
            assert opened_filename.startswith(data.starts_with), caplog.text
        if data.re_match is not None:
            assert data.re_match.match(opened_filename), caplog.text
    else:
        mocked_write.assert_not_called()


def test_artifact_contents(monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    """Test the artifact contents for settings information.

    Args:
        monkeypatch: The monkeypatch fixture
        mocker: The mocker fixture
    """
    monkeypatch.setattr(os, "makedirs", make_dirs)
    monkeypatch.setattr(action, "_get_status", get_status)
    mocked_write = mocker.patch(
        "ansible_navigator.actions.run.serialize_write_file",
        return_value=None,
    )

    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True
    _messages, exit_messages = parse_and_update(params=["run", "site.yaml"], args=settings)
    assert not exit_messages

    run_action = action(args=settings)
    run_action.write_artifact(filename="artifact.json")

    settings_entries = mocked_write.call_args[1]["content"]["settings_entries"]
    assert settings_entries["ansible-navigator"]["app"] == "run"

    settings_sources = mocked_write.call_args[1]["content"]["settings_sources"]
    assert settings_sources["ansible-navigator.app"] == Constants.USER_CLI.value
