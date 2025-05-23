"""Test doc using subprocess."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from ansible_navigator.utils.functions import shlex_join
from tests.defaults import BaseScenario
from tests.defaults import id_func


if TYPE_CHECKING:
    from pathlib import Path

    from tests.conftest import TCmdInTty


BUILTINS = (
    "validate_argument_spec",
    "wait_for_connection",
    "yum_repository",
)


@dataclass(frozen=True)
class StdoutCliTest(BaseScenario):
    """Definition of a stdout cli test."""

    comment: str
    """Description of the test"""
    params: tuple[str, ...]
    """Parameters for the subcommand"""
    expected: tuple[str, ...] = BUILTINS
    """Expected output"""
    subcommand: str = "doc"

    def __str__(self) -> str:
        """Provide a test id.

        Returns:
            The test id
        """
        return self.comment

    @property
    def command(self) -> tuple[str, ...]:
        """Provide the constructed command.

        Returns:
            The constructed command
        """
        return ("ansible-navigator", self.subcommand) + self.params


# Intentionally not using parametrize so the behavior can be documented
StdoutCliTests = (
    StdoutCliTest(
        comment="-l",
        params=("-l",),
    ),
    StdoutCliTest(
        comment="--list",
        params=("--list",),
    ),
    StdoutCliTest(
        comment="-F",
        params=("-F",),
    ),
    StdoutCliTest(
        comment="--list_files",
        params=("--list_files",),
    ),
    StdoutCliTest(
        comment="-s",
        params=(
            "debug",
            "-s",
        ),
        expected=(
            "name:",
            "debug:",
            "msg:",
        ),
    ),
    StdoutCliTest(
        comment="--snippet",
        params=(
            "debug",
            "--snippet",
        ),
        expected=(
            "name:",
            "debug:",
            "msg:",
        ),
    ),
    StdoutCliTest(
        comment="--metadata-dump",
        params=("--metadata-dump",),
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=StdoutCliTests, ids=id_func)
@pytest.mark.parametrize(argnames="exec_env", argvalues=(True, False), ids=("ee_true", "ee_false"))
def test(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    data: StdoutCliTest,
    exec_env: bool,
    cmd_in_tty: TCmdInTty,
    skip_if_already_failed: None,
) -> None:
    """Test doc using subcommand.

    Args:
        monkeypatch: The monkeypatch fixture
        tmp_path: The temporary path to use
        data: The test data
        exec_env: Whether to use the exec environment
        cmd_in_tty: The tty command runner
        skip_if_already_failed: Fixture that stops parametrized tests running on first failure.

    Raises:
        AssertionError: When test fails
    """
    log_file = str(tmp_path / "log.txt")
    monkeypatch.setenv("PAGER", "cat")
    monkeypatch.setenv("NO_COLOR", "true")
    command = shlex_join(
        data.command + ("--lf", log_file, "--ee", str(exec_env), "--set-env", "PAGER=cat"),
    )
    stdout, _stderr, _exit_code = cmd_in_tty(cmd=command)

    assert all(d in stdout for d in data.expected)
