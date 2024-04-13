# pygame errors
# pylint: disable=no-member

"""This state allows player to start a new game or exit application"""
import pygame
from app.gui.label import Label
from app.gui.button import Button
from app.core.config import Config
from app.states.base_state import BaseState


class Menu(BaseState):
    """This state allows player to start a new game or exit application"""

    def __init__(self):
        super().__init__()
        self.active = True
        self.entities = []
        self._create_menu()

    def _init_state(self):
        """
        The state is static
        """

    def draw(self, screen: pygame.display) -> None:
        """
        Draw the game on the screen
        :param screen: pygame display
        """
        pygame.display.set_caption('Collapsed Bomberman')
        screen.fill(Config.consts['BACKGROUND_COLOR'])
        for entity in self.entities:
            entity.draw(screen)

    def update(self, events: pygame.event) -> None:
        """
        Update the internal menu state
        :param events: pygame events feed
        """
        if self.play.update():
            self.active = False
        if self.exit.update():
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _create_menu(self) -> None:
        """Create the layout of the menu"""
        self.entities.append(Label("Collapsed Bomberman",
                                   {'color': Config.consts['WHITE'], 'size': 30},
                                   pos=(Config.consts['WIDTH'] * 0.25,
                                        Config.consts['HEIGHT'] * 0.2)))

        self.play = Button(Config.consts['BTN_PLAY'],
                           (Config.consts['WIDTH'] * 0.32, Config.consts['HEIGHT'] * 0.5))
        self.exit = Button(Config.consts['BTN_EXIT'],
                           (Config.consts['WIDTH'] * 0.32, Config.consts['HEIGHT'] * 0.7))
        self.entities += [self.play, self.exit]
