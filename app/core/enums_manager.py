"""
This module aggregates the enums used in this project
"""
from enum import Enum


class Movement(Enum):
    """
    Directions
    """
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3


class GroupClass(Enum):
    """
    Entity Class types
    """
    BORDER = 5
    PLAYER = 0
    BOMB = 1
    WALL = 2
    EXPLOSION = 3
    ENEMY = 4
