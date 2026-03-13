"""Keyboard input helpers for terminal gameplay."""

from __future__ import annotations

import os
import select
import sys
from types import TracebackType

if os.name != "nt":
    import termios
    import tty
else:
    import msvcrt


class KeyboardReader:
    """Read keyboard keys without blocking the game loop."""

    def __init__(self) -> None:
        """Create a keyboard reader instance."""

        self._fd: int | None = None
        self._old_settings: list[int] | None = None

    def __enter__(self) -> "KeyboardReader":
        """Enter raw-like terminal mode on Unix systems."""

        if os.name != "nt" and sys.stdin.isatty():
            self._fd = sys.stdin.fileno()
            self._old_settings = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Restore terminal settings on Unix systems."""

        if (
            os.name != "nt"
            and self._fd is not None
            and self._old_settings is not None
        ):
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

    def read_key(self) -> str | None:
        """Return the latest available key or None when no key was pressed."""

        if os.name == "nt":
            return self._read_windows_key()
        return self._read_unix_key()

    def _read_windows_key(self) -> str | None:
        """Read one key on Windows terminals."""

        if not msvcrt.kbhit():
            return None

        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            arrow = msvcrt.getwch()
            return {
                "H": "up",
                "P": "down",
                "K": "left",
                "M": "right",
            }.get(arrow)

        return key.lower()

    def _read_unix_key(self) -> str | None:
        """Read one key on Unix-like terminals."""

        if not sys.stdin.isatty():
            return None

        ready, _, _ = select.select([sys.stdin], [], [], 0)
        if not ready:
            return None

        key = sys.stdin.read(1)
        if key == "\x1b":
            return self._read_unix_escape_sequence()

        return key.lower()

    def _read_unix_escape_sequence(self) -> str | None:
        """Parse ANSI escape sequences to support arrow keys."""

        sequence = ""
        for _ in range(2):
            ready, _, _ = select.select([sys.stdin], [], [], 0)
            if not ready:
                break
            sequence += sys.stdin.read(1)

        return {
            "[A": "up",
            "[B": "down",
            "[D": "left",
            "[C": "right",
        }.get(sequence)
