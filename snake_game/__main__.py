"""Module execution entry point for `python -m snake_game`."""

from .app import SnakeApp


def main() -> None:
    """Run the Snake terminal application."""

    SnakeApp().run()


if __name__ == "__main__":
    main()
