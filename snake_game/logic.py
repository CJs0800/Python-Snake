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
        food = self._food_spawner(set(snake), width, height)
        if food is None:
            raise ValueError("Unable to place initial food on the board.")

        return GameState(
            snake=snake,
            direction=Direction.RIGHT,
            pending_direction=Direction.RIGHT,
            food=food,
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
        ate_food = new_head == state.food

        body_to_check = state.snake if ate_food else state.snake[:-1]
        if not self._is_inside_board(new_head) or new_head in body_to_check:
            state.status = GameStatus.GAME_OVER
            return

        state.snake.insert(0, new_head)

        if ate_food:
            state.score += 1
            next_food = self._food_spawner(
                set(state.snake),
                self.config.board.width,
                self.config.board.height,
            )
            if next_food is None:
                state.status = GameStatus.GAME_OVER
                return
            state.food = next_food
        else:
            state.snake.pop()

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
