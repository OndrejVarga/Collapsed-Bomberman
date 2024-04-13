# Pygame Constant errors
# pylint: disable=no-member
# Class inherits draw public method from Sprite class
# pylint: disable=too-few-public-methods

""""
Class with the user controllable player
Every level has one and only one player
Entity can place bombs
Entity can be killed by collision with explosion or enemies
"""
from typing import Tuple, Callable, List
import pygame.draw
from app.core.config import Config
from app.core.enums_manager import GroupClass
from app.entities.bomb import Bomb


class Player(pygame.sprite.Sprite):
    """Class with the user controllable player"""

    def __init__(self, pos: Tuple[int, int]):
        """
        :param pos: the starting GRID position of the player
        """
        super().__init__()

        # Create Image and Hitbox for the player
        self.image = Config.load_image(Config.consts['PLAYER_IMAGE'],
                                       Config.consts['CELL_SIZE'] * Config.consts['PLAYER_SCALE'])
        self.pos = pos[0] * Config.consts['CELL_SIZE'], pos[1] * Config.consts['CELL_SIZE']
        self.rect = self.image.get_rect(topleft=self.pos)

        self.killable = True
        self.destroyable = False

    def update(self, events: List, handle_collisions: Callable, spawn_entity: Callable) -> None:
        """
        Update the internal player state
        :param events: event feed from pygame
        :param handle_collisions: Callback from StateManager to return list of collided entities
        :param spawn_entity: Callback from StateManager to spawn bomb entity
        """
        # Handle Movement
        self.pos = self._handle_movement(handle_collisions)

        for event in events:
            # Spawn a bomb
            if event.type == pygame.KEYDOWN:
                self._plant_bomb(event, spawn_entity)

    def _plant_bomb(self, event: pygame.event, spawn_entity: Callable) -> bool:
        """
        Plant a bomb at the current position
        :param event: event feed from pygame
        :param spawn_entity: Callback from StateManager to spawn bomb entity
        :return: True if the bomb has been planted, False otherwise
        """
        if event.key == Config.PLANT_BOMB_KEY:
            spawn_entity(Bomb(self.pos))
            return True
        return False

    def _can_move(self, new_pos: List[int], handle_collision: Callable) -> bool:
        """
        Test if the player can move to a new position
        :param new_pos: the position to move to
        :param handle_collision: Callback from StateManager to return list of collided entities
        :return: True if the player can move to a new position, False otherwise
        """
        self._move(new_pos)
        collisions = handle_collision(self, [GroupClass.WALL, GroupClass.BORDER], False)
        return not bool(collisions)

    def _move(self, new_pos: List[int]) -> None:
        """
        Move the player to a new position
        :param new_pos:
        """
        self.rect.topleft = tuple(new_pos)

    def _handle_movement(self, handle_collision: Callable) -> Tuple:
        """
        Try to move to a new position and check if a collision occurs
        :param handle_collision: Callback from StateManager to return list of
            collided entities
        :return: -> new position without collision
        """
        key_pressed = pygame.key.get_pressed()
        new_pos = list(self.pos)

        # Move Up
        if key_pressed[Config.MOVE_UP]:
            new_pos[1] -= Config.consts['PLAYER_SPEED']
            if not self._can_move(new_pos, handle_collision):
                new_pos[1] += Config.consts['PLAYER_SPEED']
                self._move(new_pos)

        # Move Down
        if key_pressed[Config.MOVE_DOWN]:
            new_pos[1] += Config.consts['PLAYER_SPEED']
            if not self._can_move(new_pos, handle_collision):
                new_pos[1] -= Config.consts['PLAYER_SPEED']
                self._move(new_pos)

        # Move Left
        if key_pressed[Config.MOVE_LEFT]:
            new_pos[0] -= Config.consts['PLAYER_SPEED']
            if not self._can_move(new_pos, handle_collision):
                new_pos[0] += Config.consts['PLAYER_SPEED']
                self._move(new_pos)

        # Move Right
        if key_pressed[Config.MOVE_RIGHT]:
            new_pos[0] += Config.consts['PLAYER_SPEED']
            if not self._can_move(new_pos, handle_collision):
                new_pos[0] -= Config.consts['PLAYER_SPEED']
                self._move(new_pos)

        return tuple(new_pos)
