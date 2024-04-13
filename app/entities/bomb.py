# bomb inherits public draw wo it satisfies the 2 public methods
# pylint: disable=too-few-public-methods

"""
Class for the Bomb entity.
A bomb can be placed only by the player
The range of the bomb can be changed in config file
Class crates explosion entities
"""
from typing import Tuple, List, Callable
import pygame.draw
from app.entities.explosion import Explosion
from app.core.config import Config
from app.core.enums_manager import Movement


class Bomb(pygame.sprite.Sprite):
    """Class for the Bomb entity."""

    def __init__(self, pos: Tuple[int, int]):
        """
        :param pos: The initial position of the bomb
        """
        super().__init__()
        # Create Image and Hitbox of a bomb
        self.image = Config.load_image(Config.consts['BOMB_IMAGE'], Config.consts['CELL_SIZE'])

        # Calculate the position on the grid
        self.pos = self._center_pos(pos)
        self.rect = self.image.get_rect(topleft=(self.pos[0] * Config.consts['CELL_SIZE'],
                                                 self.pos[1] * Config.consts['CELL_SIZE']))
        # Lifespan of entity
        self.countdown = Config.consts['BOMB_COUNTDOWN_SEC'] * Config.consts['FPS']

    @staticmethod
    def _center_pos(pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Place the bomb at the center of the closest cell
        :param pos: (x,y) raw position (not the grid indices)
        :return: (x,y) new position in grid
        """
        return (round(pos[0] / Config.consts['CELL_SIZE']),
                round(pos[1] / Config.consts['CELL_SIZE']))

    def _create_explosion(self) -> List[Explosion]:
        """
        Create Explosion entities in all directions around the bomb
        :return: a list of Explosion entities
        """
        return [
            # Center Explosion
            Explosion((self.pos[0], self.pos[1]), 0, Movement.MOVE_RIGHT),

            Explosion((self.pos[0] + 1, self.pos[1]),
                      Config.consts['BOMB_RANGE'] - 1,
                      Movement.MOVE_RIGHT),
            Explosion((self.pos[0] - 1, self.pos[1]),
                      Config.consts['BOMB_RANGE'] - 1,
                      Movement.MOVE_LEFT),
            Explosion((self.pos[0], self.pos[1] + 1),
                      Config.consts['BOMB_RANGE'] - 1,
                      Movement.MOVE_DOWN),
            Explosion((self.pos[0], self.pos[1] - 1),
                      Config.consts['BOMB_RANGE'] - 1,
                      Movement.MOVE_UP), ]

    def update(self, spawn_entity: Callable) -> None:
        """
        Reduce the lifespan and handle a bomb explosion
        :param spawn_entity: callback from StateManager that creates new explosion
        """
        self.countdown -= 1
        self._spawn_explosions(spawn_entity)

    def _spawn_explosions(self, spawn_entity: Callable) -> None:
        """
        Spawn explosions at the end of the lifespan
        :param spawn_entity:
        """
        if self.countdown > 0:
            return

        expl = self._create_explosion()
        for entity in expl:
            spawn_entity(entity)
        # Remove bomb
        self.kill()
