# Class represents a static widget that is the reason for few public methods
# pylint: disable=too-few-public-methods
"""
Class that is responsible for Label Widget
Entity is not intractable and displays static text on the screen
"""
from typing import Dict, Tuple

from pygame import font
from pygame import display
from app.core.config import Config


class Label:
    """ Class that is responsible for Label Widget"""

    def __init__(self, text: str, text_desc: Dict, pos: Tuple[float, float]):
        """
        Create a new label entity
        :param text: display text
        :param text_desc: Attributes of text,
            {
                'color': tuple = color of the text as rgb tuple
                'size': int = font size
            }
        :param pos: location of the label
        """
        self.text = text
        self.text_size = text_desc['size']
        self.color = text_desc['color']
        self.font = font.Font(Config.FONT, text_desc['size'])
        self.widget = self.font.render(text, True, text_desc['color'])
        self.pos = int(pos[0]), int(pos[1])

    def draw(self, screen: display) -> None:
        """
        Draw the text on the screen
        :param screen: pygame display
        """
        screen.blit(self.widget, self.pos)
