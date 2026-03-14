"""Menu screens for the terminal Snake application."""

from .config import MapSizeConfig, SpeedConfig
from .renderer import clear_screen


def show_main_menu() -> str:
    """Display the welcome menu and return the selected option."""

    while True:
        clear_screen()
        print("=== Snake Terminal ===")
        print("1. Commencer une partie (Mode Classique)")
        print("2. Modes et evolutions a venir")
        print("3. Quitter")
        choice = input("Votre choix: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        input("Choix invalide. Appuyez sur Entree pour recommencer...")


def show_coming_soon_screen() -> None:
    """Display V4+ features planned for future versions."""

    clear_screen()
    print("=== A venir ===")
    print("- Plusieurs fruits simultanes")
    print("- Modes de jeu supplementaires")
    input("\nAppuyez sur Entree pour revenir au menu...")


def show_map_size_menu(
    map_sizes: tuple[MapSizeConfig, ...],
    default_key: str,
) -> MapSizeConfig | None:
    """Display map size options and return the selected preset."""

    choices_by_index = {str(index + 1): map_size for index, map_size in enumerate(map_sizes)}
    default_index = next(
        (
            str(index + 1)
            for index, map_size in enumerate(map_sizes)
            if map_size.key == default_key
        ),
        "1",
    )

    while True:
        clear_screen()
        print("=== Choix de la map (Mode Classique) ===")
        for index, map_size in enumerate(map_sizes, start=1):
            suffix = " (par defaut)" if str(index) == default_index else ""
            print(
                f"{index}. {map_size.label} ({map_size.board.width}x{map_size.board.height}){suffix}"
            )
        print("b. Retour au menu")

        choice = input("Votre choix: ").strip().lower()
        if choice == "b":
            return None
        if choice in choices_by_index:
            return choices_by_index[choice]

        input("Choix invalide. Appuyez sur Entree pour recommencer...")


def show_speed_menu(
    speed_presets: tuple[SpeedConfig, ...],
    default_key: str,
) -> SpeedConfig | None:
    """Display speed options and return the selected preset."""

    choices_by_index = {str(index + 1): speed for index, speed in enumerate(speed_presets)}
    default_index = next(
        (
            str(index + 1)
            for index, speed in enumerate(speed_presets)
            if speed.key == default_key
        ),
        "1",
    )

    while True:
        clear_screen()
        print("=== Choix de la vitesse (Mode Classique) ===")
        for index, speed in enumerate(speed_presets, start=1):
            suffix = " (par defaut)" if str(index) == default_index else ""
            print(f"{index}. {speed.label} ({speed.tick_seconds:.2f}s / tick){suffix}")
        print("b. Retour au menu map")

        choice = input("Votre choix: ").strip().lower()
        if choice == "b":
            return None
        if choice in choices_by_index:
            return choices_by_index[choice]

        input("Choix invalide. Appuyez sur Entree pour recommencer...")


def show_game_over_screen(score: int) -> str:
    """Display final score and ask where to go next."""

    print("\nPartie terminee.")
    print(f"Score final: {score}")
    choice = input("Appuyez sur Entree pour revenir au menu, ou tapez q pour quitter: ")
    if choice.strip().lower() == "q":
        return "quit"
    return "menu"


def show_goodbye() -> None:
    """Display a short exit message."""

    clear_screen()
    print("Merci d'avoir joue a Snake. A bientot.")
