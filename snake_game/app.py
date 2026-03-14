"""Application orchestration for terminal Snake V2."""

from __future__ import annotations

import time

from .config import AppConfig, BoardConfig, DEFAULT_CONFIG
from .input_handler import KeyboardReader
from .logic import GameEngine
from .menu import (
    show_coming_soon_screen,
    show_game_over_screen,
    show_goodbye,
    show_map_size_menu,
    show_main_menu,
)
from .models import Direction, GameStatus
from .renderer import TerminalRenderer

KEY_TO_DIRECTION: dict[str, Direction] = {
    "z": Direction.UP,
    "w": Direction.UP,
    "up": Direction.UP,
    "s": Direction.DOWN,
    "down": Direction.DOWN,
    "q": Direction.LEFT,
    "a": Direction.LEFT,
    "left": Direction.LEFT,
    "d": Direction.RIGHT,
    "right": Direction.RIGHT,
}


class SnakeApp:
    """Drive the menu flow and game sessions."""

    def __init__(self, config: AppConfig = DEFAULT_CONFIG) -> None:
        """Initialize app dependencies for one process execution."""

        self._config = config

    def run(self) -> None:
        """Run the application main loop until the user quits."""

        while True:
            choice = show_main_menu()

            if choice == "1":
                selected_map_size = show_map_size_menu(
                    self._config.map_sizes,
                    self._config.default_map_size_key,
                )
                if selected_map_size is None:
                    continue

                should_quit = self._run_classic_mode(
                    selected_map_size.board,
                    selected_map_size.label,
                )
                if should_quit:
                    show_goodbye()
                    return
                continue

            if choice == "2":
                show_coming_soon_screen()
                continue

            show_goodbye()
            return

    def _run_classic_mode(self, board: BoardConfig, map_label: str) -> bool:
        """Run one classic game session and return True when app should exit."""

        session_config = self._config.with_board(board)
        engine = GameEngine(session_config)
        renderer = TerminalRenderer(session_config)
        state = engine.new_game_state()
        controls_text = (
            f"Map: {map_label} ({board.width}x{board.height}) | "
            "Controles: ZQSD/WASD/Fleches. X: retour menu"
        )

        renderer.render_game(state, controls_text)

        with KeyboardReader() as keyboard:
            while state.status is GameStatus.RUNNING:
                frame_start = time.monotonic()
                pressed_key = keyboard.read_key()

                if pressed_key == "x":
                    return False

                requested_direction = KEY_TO_DIRECTION.get(pressed_key or "")
                if requested_direction is not None:
                    engine.change_direction(state, requested_direction)

                engine.step(state)
                renderer.render_game(state, controls_text)

                elapsed = time.monotonic() - frame_start
                delay = self._config.gameplay.tick_seconds - elapsed
                if delay > 0:
                    time.sleep(delay)

        action = show_game_over_screen(state.score)
        return action == "quit"
