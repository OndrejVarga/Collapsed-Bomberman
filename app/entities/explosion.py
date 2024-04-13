# The Class inherits from Sprite public method draw
# pylint: disable=too-few-public-methods

# I couldn't find a way to decrease the number of attributes
# pylint: disable=too-many-instance-attributes

"""
Class that handles the explosion after a bomb detonation
Explosion can be created only by a bomb or by another explosion
It can only travel in one direction and only if the range is > 0
On a collision it kills a player/enemy and destroys walls
"""
from typing import Tuple, Callable
import pygame.draw
from app.core.config import Config
from app.core.enums_manager import GroupClass, Movement


class Explosion(pygame.sprite.Sprite):
    """Class that handles the explosion after a bomb detonation"""

    def __init__(self,
                 pos: Tuple[int, int],
                 remaining_range: int,
                 direction: Movement,
                 timer: int = None):
        """
        :param pos: initial position of the explosion in the grid
        :param remaining_range: number of children explosions that will be created
        :param direction: direction of the explosion
        :param timer: synced timers to stop all explosions at the same time
        """
        super().__init__()
        self.pos = pos

        # Create image and hitbox for the explosion
        self.image = Config.load_image(Config.consts['EXPLOSION_IMAGE'], Config.consts['CELL_SIZE'])
        self.rect = self.image.get_rect(topleft=[self.pos[0] * Config.consts['CELL_SIZE'],
                                                 self.pos[1] * Config.consts['CELL_SIZE']])
        # direction to create children explosions
        self.direction = direction
        # number of explosions in range
        self.range = remaining_range
        # if entity is killed stop the spreading
        self.create_children = True

        self.lifespan = 0
        self.synced_timer = timer

        # Initial explosion
        if self.synced_timer is None:
            self.synced_timer = (
                    self.range * Config.consts['FPS'] * Config.consts['EXPLOSION_ALIVE_COUNTDOWN'])

    def _create_children(self) -> 'Explosion':
        """
        Create the consecutive explosions
        :return: a new explosion entity moved in the direction of the explosion
        """
        new_pos = list(self.pos)
        if self.direction == Movement.MOVE_UP:
            new_pos[1] -= 1
        elif self.direction == Movement.MOVE_DOWN:
            new_pos[1] += 1
        elif self.direction == Movement.MOVE_LEFT:
            new_pos[0] -= 1
        else:
            new_pos[0] += 1
        return Explosion(
            (new_pos[0], new_pos[1]), self.range - 1, self.direction, self.synced_timer)

    def update(self, handle_collisions: Callable, spawn_entity: Callable) -> None:
        """
        Update the internal explosion state"
        :param handle_collisions: Callback from StateManager to return list of collided entities
        :param spawn_entity: Callback from StateManager to spawn explosion entity
        """""
        # Kill collided entities
        self._handle_collisions(handle_collisions)

        # Update internal state
        self.lifespan += 1
        self.synced_timer -= 1
        self._spawn_explosion(spawn_entity)

        # Destroy
        if self.synced_timer <= 0:
            self.kill()

    def _spawn_explosion(self, spawn_entity: Callable) -> bool:
        """
        Spawn the child explosion entity
        :param spawn_entity: Callback from StateManager to spawn explosion entity
        """
        if (self.lifespan >= (Config.consts['EXPLOSION_SPAWN_COUNTDOWN'] * Config.consts['FPS'])
                and self.create_children
                and self.range != 0):
            spawn_entity(self._create_children())
            return True
        return False

    def _handle_collisions(self, handle_collisions: Callable) -> None:
        """
        Remove an entity on a collision
        :param handle_collisions: Callback from StateManager to return list of collided entities
        """
        entities = handle_collisions(self,
                                     [GroupClass.WALL,
                                      GroupClass.PLAYER,
                                      GroupClass.BOMB,
                                      GroupClass.ENEMY], False)
        # Kill Collided entities and disable ability to spawning child
        for entity in entities:
            self.create_children = False
            entity.kill()
