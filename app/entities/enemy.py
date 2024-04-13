# Class public function inherits draw from a Sprite class
# pylint: disable=too-few-public-methods

"""
Class that handles an enemy entity
Enemy moves randomly
Enemy can be killed by a bomb
Entity kills player on collision
"""
import random
from typing import Tuple, Callable, List
import pygame.draw
from app.core.config import Config
from app.core.enums_manager import Movement, GroupClass


class Enemy(pygame.sprite.Sprite):
    """Class that handles an enemy entity"""

    def __init__(self, pos: Tuple[int, int], seed: int):
        """
        :param pos: the initial position of the enemy a grid
        :param seed: random seed to ensure the same movement after reset
        """
        super().__init__()
        # set seed
        random.seed(seed)

        # Create Image and Hitbox for Enemy
        self.pos = (pos[0] * Config.consts['CELL_SIZE'],
                    pos[1] * Config.consts['CELL_SIZE'])
        self.image = Config.load_image_random(Config.consts['ENEMY_IMAGE'],
                                              Config.consts['CELL_SIZE'])
        self.rect = self.image.get_rect(topleft=[self.pos[0] * Config.consts['CELL_SIZE'],
                                                 self.pos[1] * Config.consts['CELL_SIZE']])

        self.direction = self._pick_random(list(Movement))

    def _move(self, new_pos: List[int]) -> None:
        """
        Move entity to the new position
        :param new_pos: tuple of the new position of the enemy
        """
        self.rect.topleft = tuple(new_pos)

    @staticmethod
    def _kill_player(collisions: List) -> bool:
        """
        Check if the enemy collides with the player, if so kill player
        :param collisions: list of entities that collides with the enemy
        :return True if the player was killed, False otherwise
        """
        for entity in collisions:
            # Only player is killable
            if entity.killable:
                entity.kill()
                return True
        return False

    def _can_move(self, new_pos: Tuple[int, int], handle_collision: Callable) -> bool:
        """
        Check if the new position is valid
        :param new_pos: position to move to
        :param handle_collision: Callback from StateManager to return list of collided entities
        :return: True if the position is valid, False otherwise
        """
        self._move(list(new_pos))
        return not bool(handle_collision(self, [GroupClass.WALL], False))

    def _look_around(self, handle_collision: Callable) -> List[Movement]:
        """
        Pick the Directions without obstacles to move to
        :param handle_collision: Callback from StateManager to return list of collided entities
        :return: list of valid directions
        """
        possible_moves = []
        new_pos = list(self.pos)
        movements = list(Movement)

        for movement in movements:
            # Check if enemy can:
            # Move up
            if movement == Movement.MOVE_UP:
                new_pos[1] -= Config.consts['ENEMY_SPEED']
                if self._can_move((new_pos[0], new_pos[1]), handle_collision):
                    possible_moves.append(Movement.MOVE_UP)
                new_pos[1] += Config.consts['ENEMY_SPEED']

            # Move Down
            if movement == Movement.MOVE_DOWN:
                new_pos[1] += Config.consts['ENEMY_SPEED']
                if self._can_move((new_pos[0], new_pos[1]), handle_collision):
                    possible_moves.append(Movement.MOVE_DOWN)
                new_pos[1] -= Config.consts['ENEMY_SPEED']

            # Move Left
            if movement == Movement.MOVE_LEFT:
                new_pos[0] -= Config.consts['ENEMY_SPEED']
                if self._can_move((new_pos[0], new_pos[1]), handle_collision):
                    possible_moves.append(Movement.MOVE_LEFT)
                new_pos[0] += Config.consts['ENEMY_SPEED']

            # Move right
            if movement == Movement.MOVE_RIGHT:
                new_pos[0] += Config.consts['ENEMY_SPEED']
                if self._can_move((new_pos[0], new_pos[1]), handle_collision):
                    possible_moves.append(Movement.MOVE_RIGHT)
                new_pos[0] -= Config.consts['ENEMY_SPEED']

        # Add possible directions
        self._move(list(self.pos))
        return possible_moves

    def update(self, handle_collisions: Callable) -> None:
        """
        Update the internal state of the enemy
        :param handle_collisions: Callback from StateManager to return list of collided entities
        """
        # handle the movement
        new_pos = self._move_in_dir()
        self._move(list(new_pos))

        # Handle Collisions
        collisions = (handle_collisions
                      (self, [GroupClass.WALL, GroupClass.PLAYER, GroupClass.BORDER], False))

        killed = self._kill_player(collisions)
        if killed or not collisions:
            self.pos = new_pos
        else:
            self._move(list(self.pos))
            directions = self._look_around(handle_collisions)
            self.direction = self._pick_random(directions)

        # random direction change
        if random.random() < 0.01:
            directions = self._look_around(handle_collisions)
            self.direction = self._pick_random(directions)

    def _move_in_dir(self) -> Tuple[int, int]:
        """
        Move in a current direction
        :return: the new position and direction
        """
        if self.direction == Movement.MOVE_UP:
            return self.pos[0], self.pos[1] - Config.consts['ENEMY_SPEED']
        if self.direction == Movement.MOVE_DOWN:
            return self.pos[0], self.pos[1] + Config.consts['ENEMY_SPEED']
        if self.direction == Movement.MOVE_LEFT:
            return self.pos[0] - Config.consts['ENEMY_SPEED'], self.pos[1]

        return self.pos[0] + Config.consts['ENEMY_SPEED'], self.pos[1]

    @staticmethod
    def _pick_random(possible_moves: List[Movement]) -> Movement:
        """
        Pick the direction to move to
        :param possible_moves: list of possible directions
        :return: picked direction
        """
        if not possible_moves:
            possible_moves = list(Movement)
        return random.choice(possible_moves)
