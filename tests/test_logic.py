"""Unit tests for Snake core business logic."""

import unittest

from snake_game.config import AppConfig, BoardConfig, GameplayConfig, RenderConfig
from snake_game.logic import GameEngine
from snake_game.models import Direction, GameStatus, Position


def first_available_food(
    occupied: set[Position],
    width: int,
    height: int,
) -> Position | None:
    """Return the first free cell scanning rows from top-left."""

    for y in range(height):
        for x in range(width):
            candidate = Position(x, y)
            if candidate not in occupied:
                return candidate
    return None


class GameEngineTests(unittest.TestCase):
    """Validate movement, growth and collision rules."""

    def setUp(self) -> None:
        """Create a deterministic engine and config for each test."""

        self.config = AppConfig(
            board=BoardConfig(width=10, height=8),
            gameplay=GameplayConfig(tick_seconds=0.1, initial_length=3),
            render=RenderConfig(),
        )
        self.engine = GameEngine(self.config, food_spawner=first_available_food)

    def test_snake_moves_forward_when_no_input_change(self) -> None:
        """Snake head should move one cell to the right on each step initially."""

        state = self.engine.new_game_state()
        initial_head = state.snake[0]

        self.engine.step(state)

        self.assertEqual(state.snake[0], Position(initial_head.x + 1, initial_head.y))
        self.assertEqual(state.status, GameStatus.RUNNING)

    def test_reverse_direction_is_ignored(self) -> None:
        """Instant reverse should not be accepted."""

        state = self.engine.new_game_state()

        self.engine.change_direction(state, Direction.LEFT)
        self.engine.step(state)

        self.assertEqual(state.direction, Direction.RIGHT)

    def test_snake_grows_and_scores_when_eating_food(self) -> None:
        """Eating one food should increase snake length and score."""

        state = self.engine.new_game_state()
        length_before = len(state.snake)
        state.food = Position(state.snake[0].x + 1, state.snake[0].y)

        self.engine.step(state)

        self.assertEqual(len(state.snake), length_before + 1)
        self.assertEqual(state.score, 1)
        self.assertEqual(state.status, GameStatus.RUNNING)

    def test_collision_with_wall_ends_game(self) -> None:
        """Crossing board boundaries should end the game."""

        state = self.engine.new_game_state()
        state.snake = [Position(9, 4), Position(8, 4), Position(7, 4)]
        state.direction = Direction.RIGHT
        state.pending_direction = Direction.RIGHT

        self.engine.step(state)

        self.assertEqual(state.status, GameStatus.GAME_OVER)

    def test_collision_with_body_ends_game(self) -> None:
        """Moving into the snake body should end the game."""

        state = self.engine.new_game_state()
        state.snake = [
            Position(3, 2),
            Position(3, 3),
            Position(2, 3),
            Position(2, 2),
            Position(2, 1),
            Position(3, 1),
        ]
        state.direction = Direction.LEFT
        state.pending_direction = Direction.LEFT
        state.food = Position(0, 0)

        self.engine.step(state)

        self.assertEqual(state.status, GameStatus.GAME_OVER)


if __name__ == "__main__":
    unittest.main()
