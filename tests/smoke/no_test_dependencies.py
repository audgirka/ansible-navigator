"""Tests ensuring only requirements.txt are needed."""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest  # pylint: disable=preferred-module
import uuid

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner import CommandRunner


def _get_venv_prefix() -> str:
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path is None:
        return ""
    venv = Path(venv_path, "bin", "activate")
    return f". {venv} && "


@dataclass
class NavigatorCommand(Command):
    """Data structure for a full command."""

    ee_tests: tuple[bool, bool] = (True, False)
    find: str = ""
    set_env: str = "--senv PAGER=cat"

    def __post_init__(self) -> None:
        """Post the init."""
        self.identity = self.command
        venv = _get_venv_prefix()
        self.command = f"{venv}ansible-navigator {self.command} {self.set_env}"


@dataclass
class PartialCommand:
    """The unique parts of one command."""

    params: str
    find: str
    ee_support: tuple[bool, ...] = (True, False)


PartialCommands = (
    PartialCommand(params="--help", find="Start at the welcome page"),
    PartialCommand(params="settings --help", find="Options (settings subcommand)"),
    PartialCommand(params="builder --help-builder", find="Print ansible-builder version"),
    PartialCommand(params="config list --mode stdout", find="Valid YAML extensions"),
    PartialCommand(params="doc debug --mode stdout", find="ansible.builtin.debug"),
    PartialCommand(params="exec whoami", find="root", ee_support=(True,)),
    PartialCommand(params="run --help-playbook", find="--become"),
)


def _generate_commands(tmp_dir: Path) -> list[Command]:
    """Produce the commands.

    Args:
        tmp_dir: Path to a temporary directory

    Returns:
        All the commands
    """
    commands: list[Command] = []
    for partial_command in PartialCommands:
        for ee_value in partial_command.ee_support:
            random_name = uuid.uuid4()
            artifact_file = tmp_dir / f"{random_name}.json"
            log_file = tmp_dir / f"{random_name}.txt"
            append = f"--lf {log_file} --pas {artifact_file!s} --ee {ee_value!s}"
            nav_cmd = NavigatorCommand(
                find=partial_command.find,
                identity=partial_command.params,
                command=f"{partial_command.params} {append}",
                post_process=_post_process,
            )
            commands.append(nav_cmd)
    return commands


def _post_process(*_args: Any, **_kwargs: Any) -> None:
    """Do nothing command post processor.

    Args:
        *_args: The arguments
        **_kwargs: The keyword arguments
    """


class Test(unittest.TestCase):
    """The smoke tests."""

    def setUp(self) -> None:
        """Create a temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        """Remove the directory after the test."""
        shutil.rmtree(self.test_dir)

    def test(self) -> None:
        """Execute the smoke tests."""
        tmp_dir = self.test_dir
        commands = _generate_commands(tmp_dir)
        command_results = CommandRunner().run_multi_process(commands)
        for command in command_results:
            assert isinstance(command, NavigatorCommand)
            with self.subTest():
                print(command.command)
                assert command.find in command.stdout, (
                    f"command: {command.command}, "
                    f"stdout: {command.stdout}, "
                    f"stderr: {command.stderr}"
                )


if __name__ == "__main__":
    unittest.main()
