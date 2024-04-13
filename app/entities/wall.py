# The class inherits from Sprite hence the small number of public
# methods(it inherits draw function from Sprite class)
# pylint: disable=too-few-public-methods

"""
Class for the Wall entity
The wall functions as obstacle for player and enemies
Every wall can be destroyed by bombs
"""
from typing import Tuple
import pygame.draw
from app.core.config import Config


class Wall(pygame.sprite.Sprite):
    """Class for the destroyable wall"""

    def __init__(self, pos: Tuple[int, int], asset: str = Config.consts['WALL_IMAGE']):
        """
        :param pos: initial position of the wall in the grid.
        :para asset: filename of image to render
        """
        super().__init__()

        # create image and hitbox of the Wall
        self.image = Config.load_image(asset, Config.consts['CELL_SIZE'])
        self.pos = (pos[0] * Config.consts['CELL_SIZE'], pos[1] * Config.consts['CELL_SIZE'])
        self.rect = self.image.get_rect(topleft=self.pos)

        self.destroyable = True
        self.killable = False
