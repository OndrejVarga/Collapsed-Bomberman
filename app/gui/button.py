"""
Class that is responsible for Button Widget
Entity is able to notice on click event
"""
from typing import Tuple

import pygame.sprite
from app.core.config import Config


class Button:
    """Class that is responsible for Button Widget"""

    def __init__(self, asset: str, pos: Tuple[float, float]):
        """
        Create a new button
        :param asset: filename of image
        :param pos: position of the button
        """
        super().__init__()
        # Hardcoded size
        self.size = (Config.consts['CELL_SIZE'] * 8, Config.consts['CELL_SIZE'] * 2)
        self.image = Config.load_image(asset, self.size)

        self.pos = int(pos[0]), int(pos[1])
        self.rect = self.image.get_rect(topleft=self.pos)

        self.pressed = False

    def draw(self, screen: pygame.display) -> None:
        """
        Render the button
        :param screen: to render on
        """
        screen.blit(self.image, self.pos)

    @staticmethod
    def _normalize_position(pos: Tuple[float, float]) -> Tuple[int, int]:
        """
        Return normalized position
        :param pos: the position to normalize
        :return: Tuple with the normalized position
        """
        x_norm = round(pos[0] * Config.consts['WIDTH'])
        y_norm = round(pos[1] * Config.consts['HEIGHT'])
        return x_norm, y_norm

    def _handle_collision(self) -> bool:
        """
        Check for mouse collision
        :return: True if the button is clicked, False otherwise
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):

            # Notify the button on the click release
            if pygame.mouse.get_pressed()[0] == 0:
                if self.pressed:
                    self.pressed = False
                    return True

            # Button is clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed is False:
                self.pressed = True
        return False

    def update(self) -> bool:
        """
        Update the internal state of the button
        :return: True if the button is clicked, False otherwise
        """
        return self._handle_collision()
