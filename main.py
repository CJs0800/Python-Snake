"""Main script entry point for Snake terminal V1."""

from snake_game.app import SnakeApp


def main() -> None:
    """Start the Snake application."""

    SnakeApp().run()


if __name__ == "__main__":
    main()
