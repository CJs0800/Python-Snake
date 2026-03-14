"""Core business logic for the terminal Snake game."""

from __future__ import annotations

import random
from typing import Callable

from .config import AppConfig
from .models import Direction, GameState, GameStatus, Position

FoodSpawner = Callable[[set[Position], int, int], Position | None]


class GameEngine:
    """Owns game rules and state transitions."""

    def __init__(
        self,
        config: AppConfig,
        rng: random.Random | None = None,
        food_spawner: FoodSpawner | None = None,
    ) -> None:
        """Initialize the engine with configuration and optional deterministic helpers."""

        self.config = config
        self._rng = rng or random.Random()
        self._food_spawner = food_spawner or self._spawn_food_random

    def new_game_state(self) -> GameState:
        """Create and return a fresh game state for classic mode."""

        width = self.config.board.width
        height = self.config.board.height
        initial_length = self.config.gameplay.initial_length
        center_y = height // 2
        head_x = width // 2

        snake = [Position(head_x - offset, center_y) for offset in range(initial_length)]
        foods = self._spawn_initial_foods(
            occupied=set(snake),
            width=width,
            height=height,
        )
        if foods is None:
            raise ValueError("Unable to place initial foods on the board.")

        return GameState(
            snake=snake,
            direction=Direction.RIGHT,
            pending_direction=Direction.RIGHT,
            foods=foods,
        )

    def change_direction(self, state: GameState, requested: Direction) -> None:
        """Register a direction change if it does not reverse the snake instantly."""

        if requested.is_opposite(state.direction):
            return
        state.pending_direction = requested

    def step(self, state: GameState) -> None:
        """Advance the game by one tick."""

        if state.status is not GameStatus.RUNNING:
            return

        if not state.pending_direction.is_opposite(state.direction):
            state.direction = state.pending_direction

        new_head = state.snake[0].moved(state.direction)
        ate_food = new_head in state.foods

        body_to_check = state.snake if ate_food else state.snake[:-1]
        if not self._is_inside_board(new_head) or new_head in body_to_check:
            state.status = GameStatus.GAME_OVER
            return

        state.snake.insert(0, new_head)

        if ate_food:
            state.score += 1
            state.foods.remove(new_head)
            if not self._refill_foods(state):
                state.status = GameStatus.GAME_OVER
                return
        else:
            state.snake.pop()

    def _target_fruit_count(self) -> int:
        """Return the configured target number of simultaneous fruits."""

        return max(1, self.config.gameplay.fruit_count)

    def _spawn_initial_foods(
        self,
        occupied: set[Position],
        width: int,
        height: int,
    ) -> set[Position] | None:
        """Spawn the initial batch of fruits for a new game."""

        foods: set[Position] = set()
        max_attempts = max(width * height * 2, 1)
        attempts = 0

        while len(foods) < self._target_fruit_count():
            if attempts >= max_attempts:
                return None

            candidate = self._food_spawner(occupied | foods, width, height)
            attempts += 1

            if candidate is None:
                return None
            if not self._is_valid_food_position(candidate, occupied, foods, width, height):
                continue

            foods.add(candidate)

        return foods

    def _refill_foods(self, state: GameState) -> bool:
        """Generate fruits until reaching the configured simultaneous target."""

        width = self.config.board.width
        height = self.config.board.height
        occupied = set(state.snake)
        max_attempts = max(width * height * 2, 1)
        attempts = 0

        while len(state.foods) < self._target_fruit_count():
            if attempts >= max_attempts:
                return False

            candidate = self._food_spawner(occupied | state.foods, width, height)
            attempts += 1

            if candidate is None:
                return False
            if not self._is_valid_food_position(
                candidate,
                occupied,
                state.foods,
                width,
                height,
            ):
                continue

            state.foods.add(candidate)

        return True

    def _is_inside_board(self, position: Position) -> bool:
        """Return True when a coordinate is inside map boundaries."""

        return (
            0 <= position.x < self.config.board.width
            and 0 <= position.y < self.config.board.height
        )

    def _spawn_food_random(
        self,
        occupied: set[Position],
        width: int,
        height: int,
    ) -> Position | None:
        """Place one food on a random free cell."""

        free_cells = [
            Position(x, y)
            for y in range(height)
            for x in range(width)
            if Position(x, y) not in occupied
        ]
        if not free_cells:
            return None
        return self._rng.choice(free_cells)

    def _is_valid_food_position(
        self,
        candidate: Position,
        snake_occupied: set[Position],
        existing_foods: set[Position],
        width: int,
        height: int,
    ) -> bool:
        """Return True when a generated fruit position can be safely used."""

        if candidate in snake_occupied or candidate in existing_foods:
            return False
        return 0 <= candidate.x < width and 0 <= candidate.y < height
