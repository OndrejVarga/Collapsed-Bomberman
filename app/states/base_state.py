# pylint disable=too-few-public-methods
"""
Abstract base class for all states
State is the elementary block of game
"""

from typing import List, Dict
from abc import ABC, abstractmethod
import pygame.display


class BaseState(ABC):
    """Base class for the states"""

    def __init__(self):
        self._entities = []
        self.information = None
        self.active = True
        self.cursor = True

    @abstractmethod
    def _init_state(self) -> None:
        """
        Set up the scene
        """

    @abstractmethod
    def draw(self, screen: pygame.display) -> None:
        """
        Draw all the entities every tick
        :param screen: screen to draw on
        """

    @abstractmethod
    def update(self, events: List):
        """
        Update the state of this state and its entities every tick
        :param events: pygame event feed
        """

    def change_state(self) -> bool:
        """
        Check if the state should be changed
        :return: true if the state should be changed
        """
        return not self.active

    def retrieve_information(self, information: Dict) -> None:
        """Set information
        :params information:
        """
        self.information = information
