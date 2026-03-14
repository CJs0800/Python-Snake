"""Unit tests for Snake core business logic."""

import unittest

from snake_game.config import (
    MAP_SIZE_PRESETS,
    AppConfig,
    BoardConfig,
    GameplayConfig,
    RenderConfig,
)
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
            gameplay=GameplayConfig(initial_length=3, fruit_count=3),
            render=RenderConfig(),
        )
        self.engine = GameEngine(self.config, food_spawner=first_available_food)

    def _assert_position_in_bounds(self, position: Position, board: BoardConfig) -> None:
        """Check that a position is inside board boundaries."""

        self.assertGreaterEqual(position.x, 0)
        self.assertLess(position.x, board.width)
        self.assertGreaterEqual(position.y, 0)
        self.assertLess(position.y, board.height)

    def test_new_game_state_is_valid_for_each_map_size(self) -> None:
        """Initial snake and fruits placement should be valid for every map preset."""

        for map_size in MAP_SIZE_PRESETS:
            with self.subTest(map_size=map_size.key):
                config = AppConfig(
                    board=map_size.board,
                    gameplay=GameplayConfig(initial_length=3, fruit_count=3),
                    render=RenderConfig(),
                )
                engine = GameEngine(config, food_spawner=first_available_food)
                state = engine.new_game_state()

                self.assertEqual(len(state.snake), config.gameplay.initial_length)
                self.assertEqual(len(set(state.snake)), len(state.snake))
                for segment in state.snake:
                    self._assert_position_in_bounds(segment, map_size.board)

                self.assertEqual(len(state.foods), config.gameplay.fruit_count)
                for food in state.foods:
                    self._assert_position_in_bounds(food, map_size.board)
                    self.assertNotIn(food, state.snake)

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

    def test_snake_grows_scores_and_refills_when_eating_fruit(self) -> None:
        """Eating one fruit should increase snake length, score and refill fruits."""

        state = self.engine.new_game_state()
        length_before = len(state.snake)
        state.foods = {
            Position(state.snake[0].x + 1, state.snake[0].y),
            Position(0, 0),
            Position(0, 1),
        }

        self.engine.step(state)

        self.assertEqual(len(state.snake), length_before + 1)
        self.assertEqual(state.score, 1)
        self.assertEqual(state.status, GameStatus.RUNNING)
        self.assertEqual(len(state.foods), self.config.gameplay.fruit_count)
        self.assertNotIn(state.snake[0], state.foods)

    def test_collision_with_wall_ends_game(self) -> None:
        """Crossing board boundaries should end the game."""

        state = self.engine.new_game_state()
        state.snake = [Position(9, 4), Position(8, 4), Position(7, 4)]
        state.direction = Direction.RIGHT
        state.pending_direction = Direction.RIGHT
        state.foods = {Position(0, 0), Position(0, 1), Position(0, 2)}

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
        state.foods = {Position(0, 0), Position(0, 1), Position(0, 2)}

        self.engine.step(state)

        self.assertEqual(state.status, GameStatus.GAME_OVER)

    def test_fruits_stay_unique_after_multiple_consumptions(self) -> None:
        """Fruit collection should remain unique after repeated consumptions."""

        state = self.engine.new_game_state()

        for _ in range(3):
            state.foods = {
                Position(state.snake[0].x + 1, state.snake[0].y),
                Position(0, 0),
                Position(0, 1),
            }
            self.engine.step(state)
            self.assertEqual(len(state.foods), len(set(state.foods)))
            for food in state.foods:
                self.assertNotIn(food, state.snake)


if __name__ == "__main__":
    unittest.main()
