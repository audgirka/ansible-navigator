"""Check migration output."""

import filecmp
import os
import shutil

from pathlib import Path

import pytest

from tests.integration._tmux_session import TmuxSession


files = [
    "ansible-navigator_all.yml",
    "ansible-navigator_some.yml",
    "ansible-navigator_1.1.yaml",
    "ansible-navigator_1.1.json",
]


@pytest.mark.parametrize("file", files)
def test_version(
    file: str,
    request: pytest.FixtureRequest,
    test_dir_fixture_dir: Path,
    tmp_path: Path,
) -> None:
    """Test migration with a file of all changes.

    Args:
        file: The file to test
        request: The pytest fixture request
        test_dir_fixture_dir: Path to the test directory
        tmp_path: The pytest tmp_path fixture
    """
    file_path = Path(file)
    file_stem = file_path.stem
    file_suffix = file_path.suffix

    source = test_dir_fixture_dir / file
    destination = tmp_path / ("ansible-navigator" + file_suffix)
    backup = tmp_path / "ansible-navigator.v1"
    corrected = test_dir_fixture_dir / (file_stem + "_corrected" + file_suffix)
    shutil.copy(source, destination)

    with TmuxSession(
        request=request,
        config_path=destination,
        cwd=tmp_path,
    ) as session:
        session.interaction(
            value="ansible-navigator --version",
            search_within_response="Do you want to run them all?",
            send_clear=False,
        )
        session.interaction(
            value="y\n",
            search_within_response="Press Enter to continue:",
            send_clear=False,
        )
        result = session.interaction(
            value="\n",
            search_within_response="ansible-navigator",
            send_clear=False,
        )

    if os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true":
        shutil.copy(destination, corrected)

    assert any("ansible-navigator 25." in line for line in result), (
        "(Note: requires recent tags, `git fetch --all`)"
    )
    assert filecmp.cmp(destination, corrected)
    assert filecmp.cmp(source, backup)
