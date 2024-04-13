# Testing private functions
# pylint: disable = protected-access
# Pygame constants error
# pylint: disable = no-member


"""This module aggregates the tests for this project."""
from typing import List, Tuple
import numpy as np
import pytest
import pygame
from app.core.wave_function_collapse import WaveFunctionCollapse
from app.core.enums_manager import Movement
from app.entities.enemy import Enemy
from app.entities.explosion import Explosion
from app.entities.bomb import Bomb
from app.entities.wall import Wall
from app.entities.player import Player
from app.core.config import Config
from app.gui.button import Button
from app.states.game_state import GameState


class TestExplosionClass:
    """
    Test Explosion entity class
    """

    @pytest.mark.parametrize("remaining_children, direction, synced_timer,pos", [
        (4, Movement.MOVE_UP, 40, (0, -1)),
        (3, Movement.MOVE_DOWN, 30, (0, 1)),
        (2, Movement.MOVE_LEFT, 20, (-1, 0)),
        (1, Movement.MOVE_RIGHT, 10, (1, 0)),
    ])
    def test_can_create_explosion(self,
                                  remaining_children: int,
                                  direction: Movement,
                                  synced_timer: int,
                                  pos: Tuple[int, int]):
        """
        Test if the explosion can spawn children in right directions
        :param remaining_children:
        :param direction:
        :param synced_timer:
        :param pos:
        """

        def same(a: Explosion, b: Explosion) -> bool:
            """
            cmp function
            """
            return (a.pos == b.pos
                    and a.range == b.range
                    and a.direction == b.direction
                    and a.synced_timer == b.synced_timer)

        explosion = Explosion((0, 0), remaining_children, direction, synced_timer)
        child = explosion._create_children()
        assert same(child, Explosion(pos, remaining_children - 1, direction, synced_timer))

    @pytest.mark.parametrize("remaining_children, direction, lifespan, expected_value", [
        (4, Movement.MOVE_UP, 0, (0, -1), True),
        (0, Movement.MOVE_DOWN, 30, (0, 1), False),
        (-1, Movement.MOVE_LEFT, 20, (-1, 0), False),
        (5, Movement.MOVE_RIGHT, 10, (1, 0), True),
        (1, Movement.MOVE_RIGHT, 10, (1, 0), True),
        (0, Movement.MOVE_RIGHT, 0, (1, 0), False),

    ])
    def spawn_explosion(self, remaining_children: int, direction: Movement, lifespan: int,
                        expected_value: Tuple[int, int]):
        """
        Test if the explosion won't/will spawn children
        """
        explosion = Explosion((0, 0), remaining_children, direction, lifespan)
        assert explosion._spawn_explosion(lambda x: x) == expected_value


class TestBombClass:
    """
    Test the Bomb class methods
    """

    @pytest.mark.parametrize("bomb_pos, expected_result", [
        ((0, 0), (0, 0)),
        ((0.1, 0.1), (0, 0)),
        ((5, 5), (5, 5)),
        ((0.1, 0.2), (0, 0)),
        ((5.5, 6.6), (6, 7)),
        ((10.0, 10.8), (10, 11)),
        ((15.3, 15.7), (15, 16)),
        ((0.5, 0.8), (0, 1)),
        ((20.9, 20.2), (21, 20)),
    ])
    def test_center_pos(self, bomb_pos: Tuple[int, int], expected_result: Tuple[int, int]) -> None:
        """
        Test the bombs' center_pos method
        :param bomb_pos: position of the bomb
        :param expected_result:
        """
        bomb = Bomb((0, 0))
        result = bomb._center_pos(
            (bomb_pos[0] * Config.consts['CELL_SIZE'],
             bomb_pos[1] * Config.consts['CELL_SIZE']))
        assert result == expected_result

    def test_create_bombs(self) -> None:
        """
        Test the create_explosion method
        """
        bomb = Bomb((0, 0))
        result = bomb._create_explosion()
        assert len(result) == 5
        for obj in result:
            assert isinstance(obj, Explosion)

    def test_explosion(self) -> None:
        """
        Test the "explode" method
        """
        bomb = Bomb((0, 0))

        def mock_spawn_bomb(_):
            """
            Mock spawn_bomb function
            """

        for _ in range(Config.consts['BOMB_COUNTDOWN_SEC'] * Config.consts['FPS'] - 1):
            bomb.update(mock_spawn_bomb)
            assert bomb.countdown > 0
        bomb.update(mock_spawn_bomb)
        assert bomb.countdown <= 0


class TestPlayerClass:
    """
    Test the PlayerClass methods
    """

    @pytest.mark.parametrize("starting_pos, new_pos, collision_result, expected_result", [
        ((0, 0), (1, 1), [], True),
        ((0, 0), (1, 1), ['obj1', 'obj2'], False),
        ((0, 0), (1, 1), ['obj1', 'obj2', 'obj3'], False),
        ((0, 0), (1, 1), ['single_object'], False),
    ])
    def test_can_move(self, starting_pos: Tuple[int, int],
                      new_pos: Tuple[int, int], collision_result: List, expected_result: bool):
        """
        Check if the player can move on general input
        :param starting_pos:
        :param new_pos: position to move to
        :param collision_result: return value of callback
        :param expected_result:
        """

        def handle_collision_mock(_, __, ___):
            return collision_result

        player = Player(starting_pos)
        result = player._can_move(list(new_pos), handle_collision_mock)
        assert result == expected_result

    @pytest.mark.parametrize("starting_pos, new_pos, expected_result", [
        ((0, 0), (0, 0), False),
        ((0, 1), (0, 1), False),
        ((0, 2), (0, 2), False),
        ((1, 0), (1, 0), False),
        ((1, 1), (1, 1), False),
        ((1, 2), (1, 2), False),
        ((2, 0), (2, 0), False),
        ((2, 1), (2, 1), False),
        ((2, 2), (2, 2), False),
        ((1, 1), (1, 2), True),
        ((1, 2), (0, 1), True),
        ((2, 0), (2, 2), True),
    ])
    def test_can_move_wall(self, starting_pos: Tuple[int, int],
                           new_pos: Tuple[int, int], expected_result: bool):
        """
        Check if player can move to the wall
        :param starting_pos:
        :param new_pos:
        :param expected_result:
        """
        player = Player((Config.consts['CELL_SIZE'], Config.consts['CELL_SIZE']))
        wall = Wall(starting_pos)

        def handle_collision_mock(_, __, ___):
            return [] if expected_result else [wall]

        result = player._can_move(
            list((Config.consts['CELL_SIZE'] * new_pos[0],
                  Config.consts['CELL_SIZE'] * new_pos[1])),
            handle_collision_mock)
        assert result == expected_result

    @pytest.mark.parametrize("starting_pos, new_pos, expected_result", [
        ((0, 0), (0, 0), True),
        ((0, 1), (0, 1), True),
        ((0, 2), (0, 2), True),
        ((1, 0), (1, 0), True),
        ((1, 1), (1, 2), True),
        ((1, 2), (0, 1), True),
        ((2, 0), (2, 2), True),

    ])
    def test_can_move_bomb(self,
                           starting_pos: Tuple[int, int],
                           new_pos: Tuple[int, int],
                           expected_result: bool):
        """
        Test if player can stand on the bomb
        :param starting_pos:
        :param new_pos:
        :param expected_result:
        """
        player = Player((Config.consts['CELL_SIZE'], Config.consts['CELL_SIZE']))
        bomb = Bomb(starting_pos)

        def handle_collision_mock(_, __, ___):
            return [] if expected_result else [bomb]

        result = player._can_move(
            list((Config.consts['CELL_SIZE'] * new_pos[0],
                  Config.consts['CELL_SIZE'] * new_pos[1])),
            handle_collision_mock)
        assert result == expected_result

    def test_move(self):
        """
        Check if the player was moved correctly
        :return:
        """
        player = Player((Config.consts['CELL_SIZE'], Config.consts['CELL_SIZE']))
        new_pos = [33, 8]
        player._move(new_pos)
        assert player.rect.topleft[0] == new_pos[0]
        assert player.rect.topleft[1] == new_pos[1]


class TestGameState:
    """
    Test the Game state class
    """

    def test_uniqueness(self):
        """
        Test if the _generate_unique_tuples picks all possible combinations
        """
        pygame.init()
        g = GameState()
        all_possible_tuples = [(i, j) for i in range(1, Config.GRID_WIDTH)
                               for j in range(1, Config.GRID_HEIGHT)]

        control = all_possible_tuples.copy()
        test = []
        for i in range(len(all_possible_tuples)):
            to_add = g._generate_unique_tuples(1, all_possible_tuples)
            test.append(to_add[0])
            all_possible_tuples.remove(to_add[0])

        assert len(test) == len(control)

    @pytest.mark.parametrize("num_of_enemies, all_possible_tuples", [
        (10000, [(1, 2), (3, 4), (5, 6), (7, 8)]),
        (0, [(1, 2), (3, 4), (5, 6), (7, 8)]),
        (2, [(1, 2), (3, 4), (5, 6), (7, 8)]),
    ])
    def test_spawn_enemies(self, num_of_enemies: int, all_possible_tuples: List):
        """
        Test the _spawn_enemies method
        """
        Config.NUM_OF_ENEMIES = num_of_enemies
        g = GameState()
        enemies = g._spawn_enemies(all_possible_tuples)
        assert len(enemies) == len(all_possible_tuples)

    def test_check_win(self):
        """
        Check if the game ends
        """
        g = GameState()
        g._enemy_group = pygame.sprite.Group()
        g.check_end_game()
        assert not g.active

    def test_check_lose(self):
        """
        Check if the game restarts
        """
        g = GameState()
        g._player_group = pygame.sprite.Group()
        g.check_end_game()
        assert bool(g._player_group)


class TestWaveFunctionCollapse:
    """Test the WaveFunctionCollapse class"""

    def test_create_rules(self):
        """
        Test the create_rules method
        :return: 
        """
        wfc = WaveFunctionCollapse(10, 10)
        wfc.init_wave_function_collapse([
            ['Y', 'Y', 'Y', 'Q'],
            ['P', 'Y', 'Y', 'Q'],
            ['Q', 'Q', 'Q', 'Q'],
            ['Q', 'Y', 'Y', 'Q'],
            ['Y', 'P', 'P', 'Y'],
            ['Y', 'P', 'Y', 'P'],
            ['P', 'P', 'P', 'P'],
        ],
            tiles={'Q': [0, 0], 'Y': [0, 0], 'P': [0, 0]})
        rules, weights = wfc.rules, wfc.weights
        assert weights == {'Y': 11, 'Q': 8, 'P': 9}
        assert rules == {('P', 'P', (0, 1)), ('Q', 'Y', (-1, 0)), ('Y', 'Q', (0, 1)),
                         ('Y', 'P', (0, 1)), ('Q', 'Y', (0, -1)), ('Q', 'P', (-1, 0)),
                         ('Q', 'Y', (1, 0)), ('P', 'Y', (-1, 0)), ('Q', 'Q', (-1, 0)),
                         ('P', 'Y', (0, -1)), ('Q', 'Q', (0, -1)), ('Y', 'Y', (-1, 0)),
                         ('Q', 'Q', (1, 0)), ('P', 'Y', (1, 0)), ('Y', 'Y', (0, -1)),
                         ('P', 'P', (-1, 0)), ('Y', 'Y', (1, 0)), ('P', 'Q', (1, 0)),
                         ('P', 'P', (0, -1)), ('Q', 'Y', (0, 1)), ('P', 'P', (1, 0)),
                         ('Y', 'P', (-1, 0)), ('Y', 'Q', (-1, 0)), ('P', 'Y', (0, 1)),
                         ('Q', 'Q', (0, 1)), ('Y', 'P', (0, -1)), ('Y', 'Q', (1, 0)),
                         ('Y', 'P', (1, 0)), ('Y', 'Q', (0, -1)), ('Y', 'Y', (0, 1))}

    def test_create_map(self):
        """
        test the create_map method of
        """
        wfc = WaveFunctionCollapse(2, 2)
        wfc.init_wave_function_collapse([
            ['Q', 'Q', 'Q', 'Q'],
            ['Q', 'Q', 'Q', 'Q'],
            ['Q', 'Q', 'Q', 'Q'],
            ['Q', 'Y', 'Y', 'Q'],
            ['Y', 'P', 'P', 'Y'],
            ['P', 'P', 'P', 'Y'],
            ['P', 'P', 'P', 'P'],
        ], tiles={'Q': [0, 0], 'Y': [0, 0], 'P': [0, 0]})

        expected_result = np.array([
            [{'Y', 'Q', 'P'}, {'Y', 'Q', 'P'}],
            [{'Y', 'Q', 'P'}, {'Y', 'Q', 'P'}]
        ])
        assert np.array_equal(wfc.grid, expected_result)

    @pytest.mark.parametrize("tile, pos, expected_value", [
        ('Y', (0, 0), (1, 0)),
        ('Q', (9, 9), (0, 1)),
        ('Y', (5, 5), (1, 0)),
    ])
    def test_create_entity(self, tile: str, pos: Tuple[int, int], expected_value: Tuple[int, int]):
        """
        Test the create_entity method
        """
        wfc = WaveFunctionCollapse(10, 10)
        wfc.init_wave_function_collapse([
            ['Q', 'Y', 'Q', 'Q'],
            ['Q', 'Q', 'Y', 'Q'],
        ], {'Q': ['wall_0.png', True], 'Y': ['space_0.png', False]})
        wfc._create_entity(tile, pos)
        assert len(wfc._walls_group) == expected_value[1]
        assert len(wfc._empty_group) == expected_value[0]

    @pytest.mark.parametrize("pos", [
        ([1, 0]),
        ([0, 1]),
        ([1, 0]),
    ])
    def test_collapse(self, pos: Tuple[int, int]):
        """
        Test teh collapse method
        :param pos:
        :return:
        """
        wfc = WaveFunctionCollapse(10, 10)
        pos = tuple(pos)
        wfc.init_wave_function_collapse([
            ['Q', 'Y', 'Q', 'Q'],
            ['Q', 'Q', 'Y', 'Q'],
        ], {'Q': ['wall_0.png', True], 'Y': ['space_0.png', False]})
        before = len(wfc._non_collapsed_group)
        wfc.collapse(pos)
        assert wfc.grid_collapsed[pos[0]][pos[1]]
        assert len(wfc._non_collapsed_group) == before - 1
        assert len(wfc.grid[pos[0]][pos[1]]) == 1

    @pytest.mark.parametrize("pos, direction, size, expected_value", [
        ((0, 0), (1, 0), (5, 5), (True, (1, 0))),
        ((2, 2), (0, 1), (4, 4), (True, (2, 3))),
        ((3, 2), (0, 1), (4, 4), (True, (3, 3))),
        ((4, 4), (1, 0), (5, 5), (False, None)),
        ((2, 2), (1, 0), (3, 3), (False, None)),
    ])
    def test_is_pos_valid(self, pos: Tuple[int, int],
                          direction: Tuple[int, int],
                          size: Tuple[int, int],
                          expected_value: Tuple):
        """
        Test the pos_is_valid method
        """
        assert WaveFunctionCollapse._is_pos_valid(pos,
                                                  direction,
                                                  size[0],
                                                  size[1]) == expected_value


class TestEnemyClass:
    """Test enemy class"""

    @pytest.mark.parametrize("starting_pos, new_pos, collision_result, expected_result", [
        ((0, 0), (1, 1), [], True),
        ((0, 0), (1, 1), [Wall((0, 0)), Wall((0, 0))], False),
        ((0, 0), (1, 1), [Wall((0, 0)), Wall((2, 1)), Player((0, 0))], False),
        ((1, 1), (4, 4), [Player((1, 1)), Wall((2, 1)), Wall((2, 2)), Wall((2, 3))], False),
        ((0, 0), (3, 3), [Wall((3, 2)), Player((0, 0))],
         False),
        ((0, 0), (2, 2), [Player((0, 0))],
         False),
    ])
    def test_can_move(self, starting_pos: Tuple[int, int], new_pos: Tuple[int, int],
                      collision_result: List, expected_result: bool):
        """
        Test If the enemy can move to the position
        """

        def handle_collision_mock(_, __, ___):
            """
            Mock handle collision callback
            """
            return collision_result

        enemy = Enemy(starting_pos, 1)
        result = enemy._can_move(new_pos, handle_collision_mock)
        assert result == expected_result

    @pytest.mark.parametrize("starting_pos, new_pos, expected_result", [
        ((0, 0), (0, 1), False),
        ((0, 1), (0, 1), False),
        ((0, 2), (0, 2), False),
        ((1, 0), (1, 0), False),
        ((1, 1), (1, 1), False),
        ((1, 2), (1, 2), False),
        ((2, 0), (2, 0), False),
        ((2, 1), (2, 1), False),
        ((2, 2), (2, 2), False),
        ((1, 1), (1, 2), True),
        ((1, 2), (0, 1), True),
        ((2, 0), (2, 2), True),

    ])
    def test_can_move_wall(self,
                           starting_pos: Tuple[int, int],
                           new_pos: Tuple[int, int],
                           expected_result: bool):
        """
        Check if the enemy can move to the wall
        :param starting_pos:
        :param new_pos:
        :param expected_result:
        """
        enemy = Enemy((Config.consts['CELL_SIZE'], Config.consts['CELL_SIZE']), 1)
        wall = Wall(starting_pos)

        def handle_collision_mock(_, __, ___):
            return [] if expected_result else [wall]

        result = enemy._can_move((Config.consts['CELL_SIZE'] * new_pos[0],
                                  Config.consts['CELL_SIZE'] * new_pos[1]),
                                 handle_collision_mock)
        assert result == expected_result

    @pytest.mark.parametrize("direction, expected_position", [
        (Movement.MOVE_UP, (0, -Config.consts['ENEMY_SPEED'])),
        (Movement.MOVE_DOWN, (0, Config.consts['ENEMY_SPEED'])),
        (Movement.MOVE_LEFT, (-Config.consts['ENEMY_SPEED'], 0)),
        (Movement.MOVE_RIGHT, (Config.consts['ENEMY_SPEED'], 0)),
    ])
    def test_move_in_dir(self, direction: Movement, expected_position: Tuple[int, int]):
        """
        Test moving in direction function
        :param direction:
        :param expected_position:
        """
        n = Enemy((0, 0), 0)
        n.direction = direction
        assert n._move_in_dir() == (expected_position[0], expected_position[1])


@pytest.mark.parametrize("input_pos, expected_result", [
    ((0.5, 0.5), (Config.consts['WIDTH'] // 2, Config.consts['HEIGHT'] // 2)),
    ((0.25, 0.75), (Config.consts['WIDTH'] // 4, 3 * Config.consts['HEIGHT'] // 4)),
    ((1.0, 0.0), (Config.consts['WIDTH'], 0)),
    ((0.0, 1.0), (0, Config.consts['HEIGHT'])),
    ((0.123, 0.456), (round(0.123 * Config.consts['WIDTH']),
                      round(0.456 * Config.consts['HEIGHT']))),
])
def test_normalize_position(input_pos: Tuple[int, int], expected_result: Tuple[int, int]):
    """
    Test normalize position function
    :param input_pos:
    :param expected_result:
    """
    result = Button._normalize_position(input_pos)
    assert result == expected_result

    if __name__ == '__main__':
        pytest.main()
