"""Terminal rendering utilities for Snake."""

from __future__ import annotations

from .config import AppConfig
from .models import GameState


def clear_screen() -> None:
    """Clear the terminal and move the cursor to the top-left corner."""

    print("\033[2J\033[H", end="")


class TerminalRenderer:
    """Render menu and game frames using plain terminal output."""

    def __init__(self, config: AppConfig) -> None:
        """Store rendering and board configuration."""

        self._config = config

    def render_game(self, state: GameState, controls_text: str) -> None:
        """Draw the current game frame."""

        clear_screen()

        width = self._config.board.width
        height = self._config.board.height

        board = [
            [self._config.render.empty_cell for _ in range(width)] for _ in range(height)
        ]

        for segment in state.snake[1:]:
            board[segment.y][segment.x] = self._config.render.body_cell

        head = state.snake[0]
        board[head.y][head.x] = self._config.render.head_cell
        board[state.food.y][state.food.x] = self._config.render.food_cell

        border = (
            self._config.render.corner
            + self._config.render.horizontal_border * width
            + self._config.render.corner
        )

        print("Snake Terminal - Mode Classique (V1)")
        print(f"Score: {state.score}")
        print(controls_text)
        print(border)
        for row in board:
            print(
                self._config.render.vertical_border
                + "".join(row)
                + self._config.render.vertical_border
            )
        print(border)
