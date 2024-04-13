# pygame constants missing errors
# pylint: disable=no-member
# The main function of this class is to combine all code parts together
# that is why it has too few public methods
# pylint: disable=too-few-public-methods
"""
Class Game contains the main state-loop
Throughout the runtime,
    - one only one state is active
    - one state must be always active
Game class handles the active states' draw-update loop,
starts the tick clock and handles the pygame event feed
"""
import json
from typing import List
import pygame
from app.core.config import Config
from app.states.game_state import GameState
from app.states.menu_state import Menu
from app.states.summary_state import SummaryState
from app.states.wfc_state import WaveFunctionCollapseState


class StateManager:
    """Class Game handles the main update-draw loop"""

    def __init__(self):
        pygame.init()

        # Load config data
        try:
            Config.import_from_json()
        except FileNotFoundError as e:
            print(f"Error: JSON file not found - {e}")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON - {e}")
        except ValueError as e:
            print(f"An unexpected error occurred: {e}")

        self.run = False
        self.screen = pygame.display.set_mode(vsync=Config.consts['VSYNC'],
                                              size=Config.get_screen_size(),
                                              flags=pygame.SCALED)
        self.states = [Menu(), WaveFunctionCollapseState(), GameState(), SummaryState()]
        self.current_state = 0

        self.cursor_image = Config.load_image(Config.consts['CURSOR_IMAGE'], 80)
        self.cursor_rect = self.cursor_image.get_rect()

        # Set the custom cursor
        pygame.mouse.set_visible(False)

    def _handle_events(self, events: List) -> None:
        """
        Call update method for active state
        :param events: pygame events
        """
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.states[self.current_state].update(events)
        # Exit window
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False

    def _handle_draw(self) -> None:
        """
        Call draw method for active state and update the screen
        """
        self.screen.fill(Config.consts['WHITE'])
        self.states[self.current_state].draw(self.screen)
        if self.states[self.current_state].cursor:
            self.screen.blit(self.cursor_image, self.cursor_rect)
        pygame.display.flip()

    def _handle_state(self) -> None:
        """
        Check if the state is still active
        If not, pass the information between states and update the active state
        """
        if not self.states[self.current_state].change_state():
            return

        information = self.states[self.current_state].information
        self.current_state = (self.current_state + 1) % len(self.states)
        # New init
        self.states = [Menu(), WaveFunctionCollapseState(), GameState(), SummaryState()]
        self.states[self.current_state].retrieve_information(information)

    def game_loop(self) -> None:
        """The main game-loop of game"""
        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(Config.consts['FPS'])
            events = pygame.event.get()
            self._handle_events(events)
            self._handle_draw()
            self._handle_state()
        # Exit application

        pygame.display.quit()
        pygame.quit()
