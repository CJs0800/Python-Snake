"""Data models for game state and directions."""

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Cardinal direction used by the snake."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def delta(self) -> tuple[int, int]:
        """Return horizontal and vertical movement increments."""

        return self.value

    def is_opposite(self, other: "Direction") -> bool:
        """Return True when two directions point in opposite ways."""

        dx, dy = self.delta
        ox, oy = other.delta
        return dx == -ox and dy == -oy


@dataclass(frozen=True, slots=True)
class Position:
    """Coordinate on the game board."""

    x: int
    y: int

    def moved(self, direction: Direction) -> "Position":
        """Return a new position moved by one cell in the given direction."""

        dx, dy = direction.delta
        return Position(self.x + dx, self.y + dy)


class GameStatus(Enum):
    """Current lifecycle status of a game session."""

    RUNNING = "running"
    GAME_OVER = "game_over"


@dataclass(slots=True)
class GameState:
    """Mutable state for one running game."""

    snake: list[Position]
    direction: Direction
    pending_direction: Direction
    food: Position
    score: int = 0
    status: GameStatus = GameStatus.RUNNING
