"""Configuration objects for the terminal Snake application."""

from dataclasses import dataclass, field, replace


@dataclass(frozen=True, slots=True)
class BoardConfig:
    """Static board dimensions for the classic game mode."""

    width: int = 20
    height: int = 12


@dataclass(frozen=True, slots=True)
class MapSizeConfig:
    """Named map size preset."""

    key: str
    label: str
    board: BoardConfig


@dataclass(frozen=True, slots=True)
class SpeedConfig:
    """Named speed preset for frame pacing."""

    key: str
    label: str
    tick_seconds: float


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
    """Gameplay defaults for the current version."""

    initial_length: int = 3


def _default_map_sizes() -> tuple[MapSizeConfig, ...]:
    """Provide default map presets for application configuration."""

    return MAP_SIZE_PRESETS


def _default_speeds() -> tuple[SpeedConfig, ...]:
    """Provide default speed presets for application configuration."""

    return SPEED_PRESETS


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Aggregate application configuration."""

    board: BoardConfig = field(default_factory=BoardConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    gameplay: GameplayConfig = field(default_factory=GameplayConfig)
    map_sizes: tuple[MapSizeConfig, ...] = field(default_factory=_default_map_sizes, repr=False)
    speed_presets: tuple[SpeedConfig, ...] = field(default_factory=_default_speeds, repr=False)
    default_map_size_key: str = "moyenne"
    default_speed_key: str = "normal"

    def with_board(self, board: BoardConfig) -> "AppConfig":
        """Return a copy configured for a specific board size."""

        return replace(self, board=board)


MAP_SIZE_PRESETS: tuple[MapSizeConfig, ...] = (
    MapSizeConfig(
        key="tres_petite",
        label="Tres-petite",
        board=BoardConfig(width=12, height=8),
    ),
    MapSizeConfig(
        key="petite",
        label="Petite",
        board=BoardConfig(width=16, height=10),
    ),
    MapSizeConfig(
        key="moyenne",
        label="Moyenne",
        board=BoardConfig(width=20, height=12),
    ),
    MapSizeConfig(
        key="grande",
        label="Grande",
        board=BoardConfig(width=28, height=16),
    ),
    MapSizeConfig(
        key="tres_grande",
        label="Tres grande",
        board=BoardConfig(width=36, height=20),
    ),
)

MAP_SIZE_BY_KEY: dict[str, MapSizeConfig] = {
    map_size.key: map_size for map_size in MAP_SIZE_PRESETS
}

SPEED_PRESETS: tuple[SpeedConfig, ...] = (
    SpeedConfig(
        key="lent",
        label="Lent",
        tick_seconds=0.28,
    ),
    SpeedConfig(
        key="normal",
        label="Normal",
        tick_seconds=0.18,
    ),
    SpeedConfig(
        key="rapide",
        label="Rapide",
        tick_seconds=0.11,
    ),
)

SPEED_BY_KEY: dict[str, SpeedConfig] = {
    speed.key: speed for speed in SPEED_PRESETS
}


DEFAULT_CONFIG = AppConfig(
    board=MAP_SIZE_BY_KEY["moyenne"].board,
    map_sizes=MAP_SIZE_PRESETS,
    speed_presets=SPEED_PRESETS,
)
