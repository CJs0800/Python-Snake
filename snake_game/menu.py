"""Menu screens for the terminal Snake application."""

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
    """Display V2+ features planned for future versions."""

    clear_screen()
    print("=== A venir ===")
    print("- Choix de la taille de map")
    print("- Choix de la vitesse")
    print("- Plusieurs fruits simultanes")
    print("- Modes de jeu supplementaires")
    input("\nAppuyez sur Entree pour revenir au menu...")


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
