"""Application orchestration for terminal Snake V3."""

from __future__ import annotations

import time

from .config import AppConfig, BoardConfig, DEFAULT_CONFIG, SpeedConfig
from .input_handler import KeyboardReader
from .logic import GameEngine
from .menu import (
    show_coming_soon_screen,
    show_game_over_screen,
    show_goodbye,
    show_map_size_menu,
    show_main_menu,
    show_speed_menu,
)
from .models import Direction, GameState, GameStatus
from .renderer import TerminalRenderer
from .timing import FramePacer

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
                classic_options = self._select_classic_options()
                if classic_options is None:
                    continue

                board, map_label, speed = classic_options
                should_quit = self._run_classic_mode(
                    board,
                    map_label,
                    speed,
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

    def _select_classic_options(self) -> tuple[BoardConfig, str, SpeedConfig] | None:
        """Collect map and speed choices before starting a classic session."""

        while True:
            selected_map_size = show_map_size_menu(
                self._config.map_sizes,
                self._config.default_map_size_key,
            )
            if selected_map_size is None:
                return None

            selected_speed = show_speed_menu(
                self._config.speed_presets,
                self._config.default_speed_key,
            )
            if selected_speed is None:
                continue

            return selected_map_size.board, selected_map_size.label, selected_speed

    def _run_classic_mode(
        self,
        board: BoardConfig,
        map_label: str,
        speed: SpeedConfig,
    ) -> bool:
        """Run one classic game session and return True when app should exit."""

        session_config = self._config.with_board(board)
        engine = GameEngine(session_config)
        renderer = TerminalRenderer(session_config)
        pacer = FramePacer(speed.tick_seconds)
        state = engine.new_game_state()
        controls_text = (
            f"Map: {map_label} ({board.width}x{board.height}) | "
            f"Vitesse: {speed.label} ({speed.tick_seconds:.2f}s/tick) | "
            "Mode: Classique | "
            "Controles: ZQSD/WASD/Fleches. X: retour menu"
        )

        renderer.render_game(state, controls_text)
        should_return_to_menu = self._run_game_loop(
            engine=engine,
            renderer=renderer,
            state=state,
            controls_text=controls_text,
            pacer=pacer,
        )
        if should_return_to_menu:
            return False

        action = show_game_over_screen(state.score)
        return action == "quit"

    def _run_game_loop(
        self,
        engine: GameEngine,
        renderer: TerminalRenderer,
        state: GameState,
        controls_text: str,
        pacer: FramePacer,
    ) -> bool:
        """Run the interactive game loop and return True when user exits to menu."""

        with KeyboardReader() as keyboard:
            while state.status is GameStatus.RUNNING:
                frame_start = time.monotonic()
                pressed_key = keyboard.read_key()

                if pressed_key == "x":
                    return True

                requested_direction = KEY_TO_DIRECTION.get(pressed_key or "")
                if requested_direction is not None:
                    engine.change_direction(state, requested_direction)

                engine.step(state)
                renderer.render_game(state, controls_text)
                pacer.sleep_remaining(frame_start)

        return False
