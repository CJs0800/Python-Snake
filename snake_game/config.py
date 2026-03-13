"""Configuration objects for the terminal Snake application."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class BoardConfig:
    """Static board dimensions for the classic game mode."""

    width: int = 20
    height: int = 12


@dataclass(frozen=True, slots=True)
class RenderConfig:
    """ASCII symbols used to draw the game board in the terminal."""

    empty_cell: str = " "
    head_cell: str = "@"
    body_cell: str = "o"
    food_cell: str = "*"
    horizontal_border: str = "-"
    vertical_border: str = "|"
    corner: str = "+"


@dataclass(frozen=True, slots=True)
class GameplayConfig:
    """Timing and gameplay defaults for V1."""

    tick_seconds: float = 0.18
    initial_length: int = 3


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Aggregate application configuration."""

    board: BoardConfig = field(default_factory=BoardConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    gameplay: GameplayConfig = field(default_factory=GameplayConfig)


DEFAULT_CONFIG = AppConfig()
