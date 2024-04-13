# could not reduce the number of attributes
# pylint: disable=too-many-instance-attributes
"""
State class that handles the main gameplay
Updates internal states of all entities
Implements the game logic
Checks for game over
"""
import random
from datetime import datetime
from typing import List, Dict
import pygame
from app.gui.label import Label
from app.core.config import Config
from app.core.enums_manager import GroupClass
from app.entities.bomb import Bomb
from app.entities.explosion import Explosion
from app.entities.wall import Wall
from app.entities.enemy import Enemy
from app.entities.player import Player
from app.states.base_state import BaseState


class GameInfo:
    """
    Container that stores the game information
    Draw them on the screen as game menu
    """

    def __init__(self):
        self.tries = 0
        self.time = 0
        self.win = None
        self.seed = 0

        self.text_attr = {'color': Config.consts['WHITE'], 'size': 25}
        self.tries_label = Label(f'Tries: {self.tries}', self.text_attr, pos=(0.25, 0.9))
        self.timer_label = Label(f'Time: {self.time}', self.text_attr, pos=(0.75, 0.9))
        space_attr = {'color': Config.consts['WHITE'], 'size': 15}
        self.space_hint_label = (
            Label('(space)',
                  space_attr,
                  pos=(Config.consts['WIDTH'] * 0.44, Config.consts['HEIGHT'] * 0.95)))

    def to_dict(self) -> Dict:
        """
        :return: return the information of the game as dictionary
        """
        return {
            "tries": self.tries,
            "time": self.time,
            "win": self.win,
            "seed": self.seed
        }

    def update(self) -> None:
        """ Update the game information"""
        self.time += 1
        self.tries_label = Label(f'Tries: {self.tries}', self.text_attr,
                                 pos=(Config.consts['WIDTH'] * 0.75, Config.consts['HEIGHT'] * 0.9))
        self.timer_label = Label(f"Time: {self.time // Config.consts['FPS']}", self.text_attr,
                                 pos=(Config.consts['WIDTH'] * 0.10, Config.consts['HEIGHT'] * 0.9))

    def draw(self, screen: pygame.display) -> None:
        """
        Draw the game menu
        :param screen: pygame display
        """
        self.timer_label.draw(screen)
        self.tries_label.draw(screen)
        self.space_hint_label.draw(screen)

    def reset(self) -> None:
        """
        Reset the data in container
        """
        self.tries = 0
        self.win = None
        self.time = 0


class GameState(BaseState):
    """State class that handles the main gameplay"""

    def __init__(self):

        # Base entity groups from WFC
        self.walls_pos = []
        self._walls_group = pygame.sprite.Group()
        self._empty_group = pygame.sprite.Group()

        super().__init__()

        self._game_info = GameInfo()
        self._enemies_alive = 0

        # Generate a unique seed
        self.rand = random.Random()
        self._seed = datetime.now().microsecond
        self.rand.seed(self._seed)
        self._game_info.seed = self._seed

        self.cursor = False
        self._init_state()

    def _init_state(self) -> None:
        """
        Initializes the game state
        use to restart the game
        """

        # Set existing seed
        self.rand.seed(self._seed)

        # Entity Groups
        self._player_group = pygame.sprite.Group()
        self._bomb_group = pygame.sprite.Group()
        self._explosion_group = pygame.sprite.Group()
        self._enemy_group = pygame.sprite.Group()
        self._map_border_group = pygame.sprite.Group()

        # Config data
        self._enemies_alive = Config.consts['NUM_OF_ENEMIES']

        # UI bomb counter
        self._bomb_counter_group = [
            Bomb(((Config.GRID_WIDTH * 0.5) * Config.consts['CELL_SIZE'],
                  (Config.GRID_HEIGHT + 1) * Config.consts['CELL_SIZE'])),
            Bomb(((Config.GRID_WIDTH * 0.45) * Config.consts['CELL_SIZE'],
                  (Config.GRID_HEIGHT + 1) * Config.consts['CELL_SIZE'])),
            Bomb(((Config.GRID_WIDTH * 0.4) * Config.consts['CELL_SIZE'],
                  (Config.GRID_HEIGHT + 1) * Config.consts['CELL_SIZE']))]

        # Choose starting enemy positions
        all_possible_tuples = [(i, j) for i in range(1, Config.GRID_WIDTH)
                               for j in range(1, Config.GRID_HEIGHT)]

        # Create Level
        all_possible_tuples = self._create_grid(all_possible_tuples)
        all_possible_tuples = self._spawn_enemies(all_possible_tuples)
        self._player_group.add(Player((all_possible_tuples[0])))

    def spawn_bomb(self, new_entity: Bomb) -> bool:
        """
        Callback to add a bomb to the sprite group
        :param new_entity: Bomb to add to the game
        :return: True if the bomb was created, False otherwise
        """

        if len(self._bomb_group) >= Config.consts['BOMB_LIMIT']:
            return False

        self._bomb_group.add(new_entity)
        return True

    def spawn_explosion(self, new_entity: Explosion) -> None:
        """
        Callback to add an explostion to the sprite group
        :param new_entity: Explosion to add to the game
        """
        self._explosion_group.add(new_entity)

    def handle_collision(self, entity: pygame.sprite, groups: List, dokill: bool) -> List:
        """
        Callback to check for collision
        :param groups: list of groups to check collision with
        :param dokill: kill all collided entities
        :param entity: entity to check collision with
        :return: list of state_entities that has collided with entity
        """
        check_collision = []

        # Add Groups to Check
        if GroupClass.PLAYER in groups:
            check_collision.append(self._player_group)
        if GroupClass.BOMB in groups:
            check_collision.append(self._bomb_group)
        if GroupClass.WALL in groups:
            check_collision.append(self._walls_group)
        if GroupClass.ENEMY in groups:
            check_collision.append(self._enemy_group)
        if GroupClass.BORDER in groups:
            check_collision.append(self._map_border_group)

        collisions = []
        # Get collisions
        for group in check_collision:
            collisions += pygame.sprite.spritecollide(entity, group, dokill)
        return collisions

    def draw(self, screen: pygame.display) -> None:
        """
        Render the groups on the screen
        :param screen: a screen to draw to
        """

        pygame.display.set_caption('Collapsed Bomberman')
        screen.fill(Config.consts['BACKGROUND_COLOR'])

        self._empty_group.draw(screen)
        self._walls_group.draw(screen)
        self._bomb_group.draw(screen)
        self._enemy_group.draw(screen)
        self._explosion_group.draw(screen)
        self._game_info.draw(screen)
        self._player_group.draw(screen)

        # Bombs UI
        for i in range(3 - len(self._bomb_group)):
            screen.blit(self._bomb_counter_group[i].image, self._bomb_counter_group[i].rect)

    def check_end_game(self) -> None:
        """
        Check and handle the game after the player or all enemies are dead
        """

        # All enemies were destroyed
        if not self._enemy_group:
            self._game_info.win = True

            # Notify state manager to change the scenes
            pygame.event.post(pygame.event.Event(Config.STATE_END_EVENT))
            self.information = self._game_info.to_dict()
            self.active = False

        # Player was killed
        if not self._player_group:
            self._init_state()
            self._game_info.tries += 1

    def retrieve_information(self, information: Dict) -> None:
        """
        Get information about the game status
        :param information:
        """
        self._walls_group = information['walls']
        self._empty_group = information['empty']
        self.walls_pos = information['walls_pos']
        self._init_state()

    def update(self, events: List) -> None:
        """
        Update the internal state of the entities
        handle the game logic
        :param events: pygame logic feed
        """
        if not self.active:
            return

        self.check_end_game()
        self._game_info.time += 1
        self._walls_group.update()
        self._player_group.update(events, self.handle_collision, self.spawn_bomb)
        self._bomb_group.update(self.spawn_explosion)
        self._explosion_group.update(self.handle_collision, self.spawn_explosion)
        self._enemy_group.update(self.handle_collision)
        self._game_info.update()

    def _create_grid(self, all_possible_tuples: List) -> List:
        """
        Create an indestructible border with walls
        :param: all_possible_tuples: list of empty locations
        """
        all_possible_tuples = list(set(all_possible_tuples).difference(set(self.walls_pos)))

        # Create border
        top_border = [(i, -1) for i in range(Config.GRID_WIDTH)]
        bottom_border = [(i, Config.GRID_HEIGHT) for i in range(Config.GRID_WIDTH)]
        right_border = [(Config.GRID_WIDTH, i) for i in range(Config.GRID_HEIGHT)]
        left_border = [(-1, i) for i in range(Config.GRID_HEIGHT)]

        for pos in left_border + right_border + top_border + bottom_border:
            self._map_border_group.add(Wall(pos))

        return all_possible_tuples

    def _spawn_enemies(self, all_possible_tuples: List) -> List:
        """
        Add initial enemies to the level
        :param: all_possible_tuples: list of possible locations
        :returns: list of possible locations after the creation of  enemies
        """
        # -1 because player needs empty space
        self._enemies_alive = min(len(all_possible_tuples) - 1, self._enemies_alive)
        enemy_pos = self._generate_unique_tuples(self._enemies_alive, all_possible_tuples)

        for pos in enemy_pos:
            self._enemy_group.add(Enemy(pos, self._seed))
            all_possible_tuples.remove(pos)
        return all_possible_tuples

    def _generate_unique_tuples(self, number_of_indexes, all_possible_tuples):
        """
        Given a list of tuples, retrieve randomly selected positions
        :param number_of_indexes:
        :param all_possible_tuples:
        :return: list of unique tuples
        """
        unique_tuples = self.rand.sample(all_possible_tuples, number_of_indexes)
        return unique_tuples
