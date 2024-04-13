# In my opinion the number of instance-attributes is valid
# regarding the algorithm it is implementing
# pylint: disable = too-many-instance-attributes


"""
This class implements an implementation of Simple Tile Wave Function Collapse algorithm
This class creates an empty grid with the cells in "superposition"
On each iteration (update call) a cell collapses propagating the change throughout the grid
The class also implements a simple rules generation based on input

My Implementation was inspired by:
https://github.com/mxgmn/WaveFunctionCollapse
https://github.com/robert/wavefunction-collapse
"""
import random
from typing import List, Dict, Tuple
import pygame
import scipy
from app.core.config import Config
from app.entities.empty import Empty
from app.entities.wall import Wall


class WaveFunctionCollapse:
    """Class implements simple Tile Wave Function Collapse algorithm"""

    def __init__(self, width: int, height: int) -> None:
        """
        :param width: width of the output grid
        :param height:  height of the output grid
        """
        # Tiles are mapped to a number/character
        self.tiles = {}

        # boolean matrix of cells' state
        self.grid_collapsed = []

        # pointers to placeholder sprites
        self.grid_placeholder_sprites = []

        # set tuples of generated rules
        # (A, B, UP) means B can be place above A
        self.rules = {}

        # Counts of tiles
        self.weights = {}

        self.grid = []

        # Size of output grid
        self.width = width
        self.height = height

        # Sprites groups for algorithm visualisation
        self._walls_group = pygame.sprite.Group()
        self._empty_group = pygame.sprite.Group()
        self._non_collapsed_group = pygame.sprite.Group()

        # Keep track of positions of walls to use in game-state
        self._walls_pos = []

        # All cells are collapsed
        self.collapsed = False

    def get_maps(self) -> Tuple:
        """
        Return the outputs of the algorithm
        :return: walls_group, empty_group, walls_pos
        """
        return self._walls_group, self._empty_group, self._walls_pos

    def update(self) -> None:
        """
        Execute 1 iteration of the WaveFunctionCollapse algorithm
        """

        # all cells have been collapsed
        if self.collapsed:
            return

        # get the position of the cell with the smallest entropy
        tile_to_collapse = self.get_pos_min_entropy()

        # if there is no such cell end the algorithm
        if self.collapsed:
            self._collapse_rest()
            return

        # collapse the found cell
        self.collapse(tile_to_collapse)

        # propagate the change throughout the grid
        self.propagate(tile_to_collapse)

    def _collapse_rest(self) -> None:
        """
        Collapse all the tiles in the with only one possible state
        Although in this implementation, the cells with 1 possible state are collapsed implicitly
        the information about cell collapsing won't be
        recorded in containers for game_state (_wall_group, _emtpy_group)
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.grid_collapsed[i][j]:
                    continue
                self.collapse((i, j))

    def entropy(self, tiles: List) -> float:
        """
        Calculate the shanon entropy of a tile from weights of possible states
        :param tiles: list of possible tiles for give cell
        :return tiles entropy
        """
        return scipy.stats.entropy([self.weights[tile] for tile in tiles])

    def get_pos_min_entropy(self) -> tuple[None, None] | tuple[int, int]:
        """
        Retrieve the position of the un-collapsed cell with the lowest entropy
        :return: the position of the cell or None, None if all cells are collapsed
        """
        min_entropy = None
        argmin = None

        # Iterate through grid
        for i in range(self.height):
            for j in range(self.width):
                # Calculate entropy for each cell
                entropy = self.entropy(self.grid[i][j])
                # update the entropy if is the smallest
                if not self.grid_collapsed[i][j] and (min_entropy is None or entropy < min_entropy):
                    min_entropy = entropy
                    argmin = (i, j)

        # Check if the grid is collapsed
        if min_entropy is None:
            self.collapsed = True
            return None, None

        return argmin

    def _create_entity(self, tile: int | str, pos: Tuple[int, int]):
        """
        Transform the collapsed cell into game entity
        :param tile: collapsed value of a cell
        :param pos: position of a cell
        """
        entity = self.tiles[tile][0]
        wall = self.tiles[tile[0]][1]
        pos = pos[1], pos[0]

        if wall:
            self._walls_group.add(Wall(pos, entity))
            self._walls_pos.append(pos)
            return
        self._empty_group.add(Empty(pos, entity))

    def collapse(self, pos: Tuple[int, int]) -> None:
        """
        Collapse the cell with the lowest entropy
        Pick the state randomly using weights of tiles
        :param pos: position of tile to collapse
        """
        # get the possible states and their respective weights for the cell
        possible_tiles = list(self.grid[pos[0]][pos[1]])
        possible_weights = [self.weights[tile] for tile in possible_tiles]

        # pick a random state
        random_pick = random.choices(possible_tiles, weights=possible_weights)[0]
        self.grid[pos[0]][pos[1]] = set(list(random_pick))

        # Update the internal containers
        self.grid_collapsed[pos[0]][pos[1]] = True

        # Transform the collapsed cell into game entity
        self._create_entity(list(self.grid[pos[0]][pos[1]])[0], pos)

        # remove from collapsed
        self.grid_placeholder_sprites[pos[0]][pos[1]].kill()

    def draw(self, screen: pygame.display) -> None:
        """
        Render the placeholders and collapsed cells
        :param screen: pygame display
        """
        self._walls_group.draw(screen)
        self._empty_group.draw(screen)
        self._non_collapsed_group.draw(screen)

    def propagate(self, tile_to_collapse: Tuple[int, int]) -> None:
        """
        Propagate the change after collapsing throughout the grid
        Using BFS iterate through the grid and decrease possible states for the cells
        :param tile_to_collapse:
        """
        # Inspired by https://github.com/robert/wavefunction-collapse
        # I decided to use similar approach of using
        # BFS instead of iterating throughout the entire grid
        # The propagation will be stopped if the list of possible states have not changed
        to_visit = [tile_to_collapse]
        visited = set()

        # Iterate through the cells which superposition was changed
        while to_visit:
            curr_tile_pos = to_visit.pop()
            visited.add(curr_tile_pos)
            curr_tile = self.grid[curr_tile_pos[0]][curr_tile_pos[1]]

            directions = [Config.consts['UP'],
                          Config.consts['DOWN'],
                          Config.consts['LEFT'],
                          Config.consts['RIGHT']]
            # Because of the simple Tiled approach we check only adjacent cells
            for curr_direction in directions:
                valid, pos = self._is_pos_valid(curr_tile_pos,
                                                curr_direction,
                                                self.width,
                                                self.height)
                # The current cell is at the boundary of grid
                if not valid:
                    continue

                # Iterate through all possible states of the neighbour cell
                for neighbor_tile in self.grid[pos[0]][pos[1]].copy():
                    is_ok = False
                    # Iterate through all possible states of current cell in bfs
                    for curr_tile_opt in curr_tile:
                        # Check if the state in the current cell is compatible with
                        # at least one state from neighbour states
                        if (curr_tile_opt, neighbor_tile, curr_direction) in self.rules:
                            is_ok = True
                            break
                    # If the neighbour state  is not compatible with any states from current tile
                    # remove the neighbour state
                    # we change the state of neighbour because we start bfs from collapsed cell
                    if not is_ok:
                        self.grid[pos[0]][pos[1]].remove(neighbor_tile)
                        if pos not in visited:
                            to_visit.append(pos)

    def init_wave_function_collapse(self, example_scene: List, tiles: Dict) -> None:
        """
        Prepare for generating a level
        :param: example_scene: List representation of example scene
                list is used to derive the ruleset for WFC
        :tiles: mapping of game tiles to symbols in the example scene
                {symbol: [filename of the asset, is the entity wall]}
        """
        # Create ruleset from the example scene
        self.rules, self.weights = self.__create_ruleset(example_scene)
        self.tiles = tiles

        # Create a grid of cells in the superposition
        self.grid, self.grid_collapsed, self.grid_placeholder_sprites = self._create_grid()

        # Add non_collapsed cells to group for rendering
        for row in self.grid_placeholder_sprites:
            for empty in row:
                self._non_collapsed_group.add(empty)

    def _create_grid(self) -> Tuple:
        """
        Create an empty Grid with a cells.
        The possible states of each cell are all available tiles
        :return: grid of cells,
                boolean grid of cell state,
                pointers to placeholder sprites for un-collapsed cells
        """
        grid = []
        grid_collapsed = []
        grid_placeholder = []
        for i in range(self.height):
            # get all possible states
            tiles = self.weights.keys()

            # populate containers
            grid.append([set(tiles) for _ in range(self.width)])
            grid_collapsed.append([False for _ in range(self.width)])
            grid_placeholder.append([Empty((j, i), 'explosion_0.png') for j in range(self.width)])
        return grid, grid_collapsed, grid_placeholder

    @staticmethod
    def _is_pos_valid(pos: Tuple[int, int], direction: Tuple[int, int], width: int, height: int) \
            -> Tuple[bool, Tuple[int, int]] | Tuple[bool, None]:
        """
        Check if the move in direction is valid
        :param pos: current position
        :param direction: direction to check
        :return: True, new_pos if valid, False,None if not
        """
        new_pos = pos[0] + direction[0], pos[1] + direction[1]

        # Outside the boundaries
        if (new_pos[0] < 0 or
                new_pos[0] >= height or
                new_pos[1] < 0 or
                new_pos[1] >= width):
            return False, None

        return True, new_pos

    def __create_ruleset(self, example: List) -> tuple:
        """
        Create a set of rules from the example list that will be used for WFC
        The list should contain identifiers for tiles
        :param example: Example scene
        :return: Ruleset and weights tiles
        """
        ruleset = set()
        weights = {}

        # iterate through the example list
        for i, row in enumerate(example):
            for j in range(len(row)):
                # increase the tile weight
                tile = row[j]
                weights[tile] = 1 if tile not in weights else weights[tile] + 1
                directions = [Config.consts['UP'],
                              Config.consts['DOWN'],
                              Config.consts['LEFT'],
                              Config.consts['RIGHT']]
                # check adjacent tiles and create rules from their position
                for curr_direction in directions:
                    valid, new_pos = self._is_pos_valid((i, j),
                                                        curr_direction,
                                                        len(row),
                                                        len(example))
                    if valid:
                        ruleset.add((tile,
                                     example[new_pos[0]][new_pos[1]],
                                     curr_direction))
        return ruleset, weights
