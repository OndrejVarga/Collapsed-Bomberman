# the maze example scene triggers this error, but this way is the matrix more readable
# pylint: disable=line-too-long

"""
State class that handles the creation of Level
"""

from typing import List
import pygame
from app.core.config import Config
from app.core.wave_function_collapse import WaveFunctionCollapse
from app.states.base_state import BaseState


class WaveFunctionCollapseState(BaseState):
    """State class that handles the creation of Level"""

    def __init__(self):
        super().__init__()
        # Generate one seed
        self.cursor = False
        self._init_state()

    def _init_state(self) -> None:
        """
        Initializes the WFC state
        """

        # Create example scene
        tiles = {
            'L': ('wall_3.png', True),
            'S': ('space_6.png', False),
            'C': ('space_5.png', False),
        }

        labyrinth = [
            ['L', 'S', 'L', 'S'],
            ['S', 'L', 'L', 'L'],
            ['L', 'S', 'S', 'S'],
            ['S', 'S', 'C', 'S'],
            ['L', 'S', 'C', 'S'],
            ['S', 'S', 'S', 'S'],
            ['L', 'S', 'S', 'S'],
        ]

        # Initialize wfc
        self.wfc = WaveFunctionCollapse(Config.GRID_WIDTH, Config.GRID_HEIGHT)
        self.wfc.init_wave_function_collapse(labyrinth, tiles)

    def draw(self, screen: pygame.display) -> None:
        """
        Render the groups
        :param screen: screen to draw to
        """

        pygame.display.set_caption('Map Creation')
        screen.fill(Config.consts['BACKGROUND_COLOR'])
        self.wfc.draw(screen)

    def update(self, events: List) -> None:
        """
        Update the internal state of the entities
        :param events: pygame logic feed
        """
        self.wfc.update()
        # The level was created
        if self.wfc.collapsed:
            maps = self.wfc.get_maps()
            self.information = {'walls': maps[0], 'empty': maps[1], 'walls_pos': maps[2]}
            self.active = False
