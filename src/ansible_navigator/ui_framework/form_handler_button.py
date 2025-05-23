"""Get one line of text input."""

from __future__ import annotations

import curses

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_window import CursesWindow


if TYPE_CHECKING:
    from ansible_navigator.action_runner import Window
    from ansible_navigator.ui_framework.ui_config import UIConfig

    from .field_button import FieldButton


class FormHandlerButton(CursesWindow):
    """Handle form button."""

    def __init__(self, screen: Window, ui_config: UIConfig) -> None:
        """Initialize the handler for a form button.

        Args:
            screen: A curses window
            ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._form_field: FieldButton | None = None
        self._form_fields: list[FieldButton] | None = None
        self._screen = screen

    def populate(self) -> None:
        """Populate the window with the button.

        Raises:
            RuntimeError: if there is a runtime error
        """
        if not self._form_field:
            msg = "_form_field not initialized"
            raise RuntimeError(msg)
        color = 8 if self._form_field.disabled is True else self._form_field.color

        if self._ui_config.color is False:
            text = f"[{self._form_field.text.upper()}]"
        else:
            text = self._form_field.text

        clp_button = CursesLinePart(0, text, color, curses.A_STANDOUT)
        self._add_line(self.win, 0, CursesLine((clp_button,)))

    def handle(self, idx: int, form_fields: list[FieldButton]) -> tuple[FieldButton, int]:
        """Handle the check box field.

        Args:
            form_fields: List of fields
            idx: Index to retrieve specific field

        Returns:
            Field and input from said field
        """
        self._form_fields = form_fields
        self._form_field = form_fields[idx]
        self.populate()

        while True:
            char = self.win.getch()

            if char in [curses.KEY_RESIZE, curses_ascii.TAB]:
                break

            if char in [curses_ascii.NL, curses_ascii.CR]:
                if not self._form_field.disabled:
                    self._form_field.pressed = True
                break
        return self._form_field, char
