"""Timing utilities for the game loop."""

from __future__ import annotations

import time


class FramePacer:
    """Maintain a target frame interval for the game loop."""

    def __init__(self, tick_seconds: float) -> None:
        """Store the expected duration of one game tick."""

        self._tick_seconds = tick_seconds

    def sleep_remaining(self, frame_started_at: float) -> None:
        """Sleep only for the remaining frame time when needed."""

        elapsed = time.monotonic() - frame_started_at
        delay = self._tick_seconds - elapsed
        if delay > 0:
            time.sleep(delay)
