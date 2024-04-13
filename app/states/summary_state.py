"""
Class that handles the summary of played game
State is responsible for displaying the data about past game
    - how long the game was played
    - how many times the player have died
returns to the main menu
"""

from typing import Dict
import pygame
from app.gui.label import Label
from app.gui.button import Button
from app.states.base_state import BaseState
from app.core.config import Config


class SummaryState(BaseState):
    """Class that handles the summary of played game"""

    def __init__(self):
        super().__init__()
        self.time = 0
        self.tries = 0
        self.text = 'You have Escaped!'
        self.continue_btn = None

    def _init_state(self) -> None:
        """
        The state is almost completely static
        :return:
        """

    def retrieve_information(self, information: Dict) -> None:
        """
        Get information about the game status from previous state
        :param information: dictionary
        {
            times: how long have till win
            tires: number of deaths
        }
        """
        self.time = information['time']
        self.tries = information['tries']
        self._create_menu()

    def draw(self, screen: pygame.display) -> None:
        """
        Draw the entities on the screen
        :param screen: pygame display
        """
        pygame.display.set_caption('Game Over')
        screen.fill(Config.consts['BACKGROUND_COLOR'])

        for entity in self._entities:
            entity.draw(screen)
        self.continue_btn.draw(screen)

    def update(self, events: pygame.event) -> None:
        """
        Update the internal summary state
        :param events: pygame events feed
        """
        if self.continue_btn.update():
            self.active = False

    def _create_menu(self) -> None:
        """
        Create the layout of the summary screen
        """
        self._entities += [
            Label(self.text, {'color': Config.consts['WHITE'], 'size': 30},
                  pos=(Config.consts['WIDTH'] * 0.30, Config.consts['HEIGHT'] * 0.1)),

            Label(f'You have died {self.tries} x',
                  {'color': Config.consts['WHITE'], 'size': 20},
                  pos=(Config.consts['WIDTH'] * 0.35, Config.consts['HEIGHT'] * 0.3)),

            Label(f'You have finished the level after {self.time // 60} seconds',
                  {'color': Config.consts['WHITE'], 'size': 20},
                  pos=(Config.consts['WIDTH'] * 0.15, Config.consts['HEIGHT'] * 0.5))
        ]

        self.continue_btn = Button(Config.consts['BTN_BACK'],
                                   pos=(Config.consts['WIDTH'] * 0.33,
                                        Config.consts['HEIGHT'] * 0.7))
