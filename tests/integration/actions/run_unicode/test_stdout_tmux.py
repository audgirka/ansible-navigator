"""Tests for run from CLI, stdout, with unicode."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices

from .base import BaseClass
from .base import inventory_path
from .base import playbook_path


class StdoutCommand(Command):
    """A command to run in the terminal."""

    subcommand = "run"
    preclear = True


class ShellCommand(UiTestStep):
    """A test step, specifically in mode stdout."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="run playbook with ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["航海家", "ok=2", "failed=0"],
    ),
    ShellCommand(
        comment="run playbook without ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["航海家", "ok=2", "failed=0"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value: ShellCommand) -> str:
    """Return a test id for the test step object.

    Args:
        value: The data to generate the id from

    Returns:
        The test id
    """
    return f"{value.step_index}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for run from CLI, stdout."""

    UPDATE_FIXTURES = False
