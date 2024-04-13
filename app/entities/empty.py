# The class inherits from Sprite hence the small number of public methods (it inherits draw method)
# pylint: disable=too-few-public-methods

"""
Class for the Empty space
The Empty entity is non-collidable and non-interactive
Used only to render the tile
"""
from typing import Tuple
import pygame.draw
from app.core.config import Config


class Empty(pygame.sprite.Sprite):
    """Class for the Empty space"""

    def __init__(self, pos: Tuple[int, int], asset: str):
        """
        :param pos: initial position of the entity in the grid.
        :param asset: the filename of an image
        """
        super().__init__()
        self.image = Config.load_image(asset, Config.consts['CELL_SIZE'])

        self.pos = (pos[0] * Config.consts['CELL_SIZE'], pos[1] * Config.consts['CELL_SIZE'])
        self.rect = self.image.get_rect(topleft=self.pos)
