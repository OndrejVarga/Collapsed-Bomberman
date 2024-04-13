"""This module is responsible for starting the application."""
from app.core.state_manager import StateManager


def run_game() -> None:
    """
    Run the main game
    """
    game = StateManager()
    game.game_loop()


if __name__ == '__main__':
    run_game()
