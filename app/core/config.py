# pygame constants error
# pylint: disable=no-member
"""This Class is responsible for aggregating the constants"""
import os
import random as rand
import json
from typing import Tuple

import pygame.font
import pygame.image
import pygame.transform


class SpriteHandler:
    """This class is responsible for loading and converting the images"""

    @staticmethod
    def load_image(asset_name: str, scale_factor) -> pygame.image:
        """
        Load in the image
        :param asset_name: path to the asset
        :param scale_factor: scale the image
        :return: pygame image
        """

        if not isinstance(scale_factor, tuple):
            scale_factor = [scale_factor, scale_factor]
        try:
            image_path = os.path.join('app', 'assets', f'{asset_name}')
            image = pygame.image.load(image_path)
        except IOError as e:
            print(f"Error loading image '{asset_name}': {e}")
            image = pygame.Surface((10, 10))
        return pygame.transform.scale(image, scale_factor)

    @staticmethod
    def load_image_random(asset_name: str, scale_factor) -> pygame.image:
        """
        Load image and choose the random alternative
        :param asset_name: path to the asset
        :param scale_factor: scale the image
        :return: pygame image
        """

        image_cnt = {
            'wall_': 6,
            'enemy_': 3,
            'space_': 3
        }

        if asset_name not in image_cnt:
            raise ValueError(f'Unknown asset: {asset_name}')

        if not isinstance(scale_factor, tuple):
            scale_factor = [scale_factor, scale_factor]
        number = rand.randint(0, image_cnt[asset_name] - 1)
        try:
            image_path = os.path.join('app', 'assets', f'{asset_name}{number}.png')
            image = pygame.image.load(image_path)
        except IOError as e:
            print(f"Error loading image '{asset_name}': {e}")
            image = pygame.Surface((10, 10))
        return pygame.transform.scale(image, scale_factor)


class Config(SpriteHandler):
    """
    This class is responsible for loading and maintaining THE constant values
    """

    consts = {
        "EMPTY": 'space_',
        "BTN_PLAY": 'button_0.png',
        "BTN_EXIT": 'button_1.png',
        "BTN_BACK": 'button_2.png',
        "EXPLOSION_IMAGE": 'explosion_0.png',
        "BOMB_IMAGE": 'bomb_0.png',
        "WALL_IMAGE": 'wall_0.png',
        "PLAYER_IMAGE": 'player_0.png',
        "ENEMY_IMAGE": 'enemy_',
        "CURSOR_IMAGE": 'cursor_0.png',
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
        "ENEMY_SPEED": 3,
        "NUM_OF_ENEMIES": 3,
        "ENEMY_SCALE": 0.8,
        "BOMB_RANGE": 2,
        "BOMB_COUNTDOWN_SEC": 1,
        "BOMB_SCALE": 0.9,
        "BOMB_LIMIT": 3,
        "EXPLOSION_ALIVE_COUNTDOWN": 0.5,
        "EXPLOSION_SPAWN_COUNTDOWN": 0.3,
        "PLAYER_SPEED": 10,
        "PLAYER_SCALE": 0.8,
        "FPS": 60,
        "WIDTH": 1200,
        "HEIGHT": 800,
        "VSYNC": False,
        "TITLE_SIZE": 50,
        "TEXT_SIZE": 30,
        "BACKGROUND_COLOR": (72, 44, 60),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "CELL_SIZE": 50,
        "PROPAGATION_COOLDOWN": 0.1,
    }

    # Asset paths
    FONT = os.path.join('app', 'assets', 'PressStart2P-Regular.ttf')

    # Bomb
    PLANT_BOMB_KEY = pygame.K_SPACE

    # Player
    MOVE_UP = pygame.K_UP
    MOVE_DOWN = pygame.K_DOWN
    MOVE_RIGHT = pygame.K_RIGHT
    MOVE_LEFT = pygame.K_LEFT
    # -----------------------

    # Game
    REMOVE_ENT_EVENT = pygame.USEREVENT + 1
    STATE_END_EVENT = pygame.USEREVENT + 2
    HIDE_CURSOR_EVENT = pygame.USEREVENT + 3

    GRID_HEIGHT = (consts['HEIGHT'] // consts['CELL_SIZE']) - 3
    GRID_WIDTH = consts['WIDTH'] // consts['CELL_SIZE']

    @classmethod
    def _check_range(cls, n: int, f: int, t: int) -> bool:
        """
        Check if the number is valid
        :param cls: tuple to check
        :param n: number to check
        :param f: lower bound
        :param t: upper bound
        :return: True if valid, False otherwise
        """
        if isinstance(n, (int, float)):
            return f < n < t
        return False

    @classmethod
    def _check_tuples(cls, t: Tuple[int, int], length: int) -> bool:
        """
        Check if the tuple is valid
        :param cls: tuple to check
        :param length: needed length
        :return: True if valid, False otherwise
        """
        if not isinstance(t, tuple) or (len(t) != length):
            return False

        for num in t:
            if not isinstance(num, int):
                return False
        return True

    @classmethod
    def _check_data(cls, consts):
        """
        check validity of config file
        :return: True if valid, False otherwise
        """
        if (not cls._check_tuples(consts['UP'], 2) or
                not cls._check_tuples(consts['DOWN'], 2) or
                not cls._check_tuples(consts['LEFT'], 2) or
                not cls._check_tuples(consts['RIGHT'], 2)):
            consts['UP'] = cls.consts['UP']
            consts['DOWN'] = cls.consts['DOWN']
            consts['LEFT'] = cls.consts['LEFT']
            consts['RIGHT'] = cls.consts['RIGHT']

        if not cls._check_range(consts['ENEMY_SPEED'], 0, 10):
            consts['ENEMY_SPEED'] = cls.consts['ENEMY_SPEED']

        if not cls._check_range(consts['NUM_OF_ENEMIES'], 0, 20):
            consts['NUM_OF_ENEMIES'] = cls.consts['NUM_OF_ENEMIES']

        if not cls._check_range(consts['ENEMY_SCALE'], 0, 1):
            consts['ENEMY_SCALE'] = cls.consts['ENEMY_SCALE']

        if not cls._check_range(consts['BOMB_RANGE'], 0, 4):
            consts['BOMB_RANGE'] = cls.consts['BOMB_RANGE']

        if not cls._check_range(consts['BOMB_COUNTDOWN_SEC'], 0, 10):
            consts['BOMB_COUNTDOWN_SEC'] = cls.consts['BOMB_COUNTDOWN_SEC']

        if not cls._check_range(consts['BOMB_SCALE'], 0, 1):
            consts['BOMB_SCALE'] = cls.consts['BOMB_SCALE']

        if not cls._check_range(consts['BOMB_LIMIT'], 0, 1):
            consts['BOMB_LIMIT'] = cls.consts['BOMB_LIMIT']

        if not cls._check_range(consts['EXPLOSION_ALIVE_COUNTDOWN'], 0, 5):
            consts['EXPLOSION_ALIVE_COUNTDOWN'] = cls.consts['EXPLOSION_ALIVE_COUNTDOWN']

        if not cls._check_range(consts['EXPLOSION_SPAWN_COUNTDOWN'], 0, 10):
            consts['EXPLOSION_SPAWN_COUNTDOWN'] = cls.consts['EXPLOSION_SPAWN_COUNTDOWN']

        if not cls._check_range(consts['PLAYER_SPEED'], 0, 10):
            consts['PLAYER_SPEED'] = cls.consts['PLAYER_SPEED']

        if not cls._check_range(consts['PLAYER_SCALE'], 0, 1):
            consts['PLAYER_SCALE'] = cls.consts['PLAYER_SCALE']

        if not cls._check_range(consts['FPS'], 0, 120):
            consts['FPS'] = cls.consts['FPS']

        if not cls._check_range(consts['WIDTH'], 0, 1200):
            consts['WIDTH'] = cls.consts['WIDTH']

        if not cls._check_range(consts['HEIGHT'], 0, 1200):
            consts['HEIGHT'] = cls.consts['HEIGHT']

        if not isinstance(consts['VSYNC'], bool):
            consts['VSYNC'] = cls.consts['VSYNC']

        if not cls._check_range(consts['TITLE_SIZE'], 0, 100):
            consts['TITLE_SIZE'] = cls.consts['TITLE_SIZE']

        if not cls._check_range(consts['TEXT_SIZE'], 0, 100):
            consts['TEXT_SIZE'] = cls.consts['TEXT_SIZE']

        if not cls._check_range(consts['PROPAGATION_COOLDOWN'], 0, 1):
            consts['PROPAGATION_COOLDOWN'] = cls.consts['PROPAGATION_COOLDOWN']

        if not cls._check_range(consts['CELL_SIZE'], 0, 300):
            consts['CELL_SIZE'] = cls.consts['CELL_SIZE']

        if (not cls._check_tuples(consts['WHITE'], 3) or
                not cls._check_tuples(consts['BLACK'], 3) or
                not cls._check_tuples(consts['RED'], 3) or
                not cls._check_tuples(consts['GREEN'], 3) or
                not cls._check_tuples(consts['BLUE'], 3)):
            consts['WHITE'] = cls.consts['WHITE']
            consts['BLACK'] = cls.consts['BLACK']
            consts['RED'] = cls.consts['RED']
            consts['GREEN'] = cls.consts['GREEN']
            consts['BLUE'] = cls.consts['BLUE']

        if not cls._check_tuples(consts['BACKGROUND_COLOR'], 3):
            consts['BACKGROUND_COLOR'] = cls.consts['BACKGROUND_COLOR']

        return consts

    @classmethod
    def get_screen_size(cls) -> tuple:
        """
        return screen size
        :return: tuple
        """
        return cls.consts['WIDTH'], cls.consts['HEIGHT']

    @classmethod
    def get_grid_size(cls) -> tuple:
        """
        return grid size
        :return: tuple
        """
        return cls.GRID_WIDTH, cls.GRID_HEIGHT

    @classmethod
    def export_to_json(cls):
        """
        Export all the variables variables to json
        """
        try:
            json_data = json.dumps(cls.consts, indent=4)
            path = os.path.join('game_settings.json')
            # Save to a JSON file
            with open(path, 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)
        except IOError as error:
            print(f'Error exporting to JSON: {error}')

    @classmethod
    def import_from_json(cls):
        """
        Import all the variables from json
        """
        try:
            path = os.path.join('game_settings.json')
            with open(path, 'r', encoding='utf-8') as json_file:
                consts = json.load(json_file)
                for key in consts.keys():
                    if isinstance(consts[key], list):
                        consts[key] = tuple(consts[key])
                cls.consts = cls._check_data(consts)

        except IOError as error:
            print(f'Error importing from JSON: {error}')


if __name__ == '__main__':
    Config.export_to_json()
