"""Unit tests for static configuration presets."""

import unittest

from snake_game.config import (
    DEFAULT_CONFIG,
    GAME_MODE_BY_KEY,
    GAME_MODE_PRESETS,
    MAP_SIZE_BY_KEY,
    MAP_SIZE_PRESETS,
    SPEED_BY_KEY,
    SPEED_PRESETS,
)


class ConfigPresetTests(unittest.TestCase):
    """Validate map and speed preset definitions."""

    def test_speed_presets_have_expected_keys(self) -> None:
        """Speed presets should expose the three expected names."""

        self.assertEqual(len(SPEED_PRESETS), 3)
        keys = {speed.key for speed in SPEED_PRESETS}
        self.assertEqual(keys, {"lent", "normal", "rapide"})

    def test_speed_tick_order_is_consistent(self) -> None:
        """Lent should be slower than normal, and normal slower than rapide."""

        self.assertGreater(SPEED_BY_KEY["lent"].tick_seconds, SPEED_BY_KEY["normal"].tick_seconds)
        self.assertGreater(
            SPEED_BY_KEY["normal"].tick_seconds,
            SPEED_BY_KEY["rapide"].tick_seconds,
        )

    def test_default_keys_exist_in_presets(self) -> None:
        """Default map and speed keys should point to existing presets."""

        self.assertIn(DEFAULT_CONFIG.default_map_size_key, MAP_SIZE_BY_KEY)
        self.assertIn(DEFAULT_CONFIG.default_speed_key, SPEED_BY_KEY)
        self.assertIn(DEFAULT_CONFIG.default_mode_key, GAME_MODE_BY_KEY)
        self.assertGreaterEqual(len(MAP_SIZE_PRESETS), 5)

    def test_default_fruit_count_supports_multi_fruit(self) -> None:
        """Default gameplay should enable multiple simultaneous fruits."""

        self.assertEqual(DEFAULT_CONFIG.gameplay.fruit_count, 1)

    def test_game_modes_have_expected_fruit_counts(self) -> None:
        """Classique and MultiFruit modes should expose expected fruit counts."""

        self.assertEqual(len(GAME_MODE_PRESETS), 2)
        self.assertEqual(GAME_MODE_BY_KEY["classique"].fruit_count, 1)
        self.assertGreaterEqual(GAME_MODE_BY_KEY["multifruit"].fruit_count, 2)


if __name__ == "__main__":
    unittest.main()
