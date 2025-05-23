"""Base class for ``config`` interactive/stdout tests."""

import difflib
import os

from collections.abc import Generator

import pytest

from tests.defaults import FIXTURES_DIR
from tests.integration._common import retrieve_fixture_for_step
from tests.integration._common import update_fixtures
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._tmux_session import TmuxSession


TEST_FIXTURE_DIR = FIXTURES_DIR / "integration" / "actions" / "config"
CONFIG_FIXTURE = TEST_FIXTURE_DIR / "ansible.cfg"


base_steps = (
    UiTestStep(user_input=":f Cache plugin timeout", comment="filter for cache plugin timeout"),
    UiTestStep(user_input=":0", comment="cache plugin details", present=["current_config_file:"]),
    UiTestStep(user_input=":back", comment="return to filtered list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Action warnings", "Callbacks enabled"],
        mask=True,
    ),
    UiTestStep(user_input=":f Yaml filename extensions", comment="filter off screen value"),
    UiTestStep(
        user_input=":0",
        comment="Yaml filename extensions details",
        present=["Yaml filename extensions (current/default: ['.yml', '.yaml', '.json'])"],
    ),
    UiTestStep(user_input=":back", comment="return to filtered list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Action warnings", "Callbacks enabled"],
        mask=True,
    ),
)


class BaseClass:
    """Base class for interactive/stdout ``config`` tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 25
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(
        self,
        request: pytest.FixtureRequest,
    ) -> Generator[TmuxSession, None, None]:
        """Generate a tmux fixture for this module.

        Args:
            request: A fixture providing details about the test caller

        Yields:
            A tmux session
        """
        with TmuxSession(
            setup_commands=["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42", "export PAGER=cat"],
            request=request,
            pane_height=self.PANE_HEIGHT,
            pane_width=self.PANE_WIDTH,
        ) as tmux_session:
            yield tmux_session

    def test(
        self,
        request: pytest.FixtureRequest,
        tmux_session: TmuxSession,
        step: UiTestStep,
        skip_if_already_failed: None,
    ) -> None:
        # pylint: disable=too-many-locals
        """Run the tests for ``config``, mode and ``ee`` set in child class.

        Args:
            request: A fixture providing details about the test caller
            tmux_session: The tmux session to use
            step: The commands to issue and content to look for
            skip_if_already_failed: Fixture that stops parametrized tests running on first failure.

        Raises:
            ValueError: When the test mode is not set
        """
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "Warning"
        else:
            msg = "test mode not set"
            raise ValueError(msg)

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        if step.mask:
            # mask out some configuration that is subject to change each run
            maskables = [
                "Become plugin path",
                "Cache plugin connection",
                "Collections paths",
                "Default callback plugin path",
                "Default local tmp",
            ]
            # Determine if a menu is showing
            mask_column_name = "Current"
            column_start = received_output[0].find(mask_column_name)
            column_exists = column_start != -1
            if column_exists:
                mask = len(mask_column_name) * "X"
                for idx, line in enumerate(received_output):
                    if any(f"│{m}" in line for m in maskables):
                        received_output[idx] = received_output[idx][0:column_start] + mask

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        if fixtures_update_requested:
            update_fixtures(
                request,
                step.step_index,
                received_output,
                step.comment,
                additional_information={
                    "present": step.present,
                    "absent": step.absent,
                    "compared_fixture": not any((step.present, step.absent)),
                },
            )

        page = " ".join(received_output)

        if step.present:
            assert all(present in page for present in step.present)

        if step.absent:
            assert not any(look_not in page for look_not in step.absent)

        if not any((step.present, step.absent)):
            expected_output = retrieve_fixture_for_step(request, step.step_index)
            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received"),
            )
