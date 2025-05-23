"""Tests for ``settings`` from CLI, stdout."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices

from .base import BaseClass


class StdoutCommand(Command):
    """Stdout command."""

    subcommand = "settings"
    preclear = True


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="print settings to stdout with ee",
        user_input=StdoutCommand(
            cmdline="",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["workdir"],
    ),
    ShellCommand(
        comment="print settings to stdout with no ee",
        user_input=StdoutCommand(
            cmdline="",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["workdir"],
    ),
    ShellCommand(
        comment="print json schema to stdout, default json, mode auto",
        user_input=StdoutCommand(
            cmdline="--schema",
            execution_environment=False,
        ).join(),
        present=["ansible-navigator settings"],
    ),
    ShellCommand(
        comment="print json schema to stdout, specify json, mode auto",
        user_input=StdoutCommand(
            cmdline="--schema json",
            execution_environment=False,
        ).join(),
        present=["ansible-navigator settings"],
    ),
    ShellCommand(
        comment="print a settings sample to stdout, mode auto",
        user_input=StdoutCommand(
            cmdline="--sample",
            execution_environment=False,
        ).join(),
        present=["#   time-zone: UTC"],
    ),
    ShellCommand(
        comment="print effective settings to stdout, mode auto",
        user_input=StdoutCommand(
            cmdline="--effective --ll debug",
            execution_environment=False,
        ).join(),
        present=["effective: true"],
    ),
    ShellCommand(
        comment="print settings sources to stdout,, mode auto",
        user_input=StdoutCommand(
            cmdline="--sources --ll debug",
            execution_environment=False,
        ).join(),
        present=["ansible-navigator.settings.sources: Command line"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value: ShellCommand) -> str:
    """Return the test id from the test step object.

    Args:
        value: If relevant, values for test id

    Returns:
        String with step_id information
    """
    return f"{value.step_index}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``settings`` from CLI, mode stdout."""

    PANE_HEIGHT = 1000
    UPDATE_FIXTURES = False
