from typing import List, Dict, Tuple
import random


class RegularPacgum:

    def __init__(self, config: Dict, grid: List[List],
                 pacman_position: Tuple,
                 super_pacgums_position: List[Tuple],
                 ghosts_position: List[Tuple]) -> None:

        # get the position of ghosts, super_pacgums, pacman
        self.__pacman_position = pacman_position
        self.__super_pacgums_position = super_pacgums_position
        self.__ghosts_position = ghosts_position

        # initialize empty list to hold positions of pacgums
        self.pacgums_grid: List[List] = [[0 for _ in row] for row in grid]

        # get data from config file, and get the available cells for dots
        self.score_pacgum = config.get('points_per_pacgum', 10)
        self.nb_available_cells = self.__get_nb_available_cells(grid)
        self.__pacgums = config.get('pacgum', self.nb_available_cells)

        # get the number of pacgums
        if self.__pacgums <= self.nb_available_cells:
            self.nb_pacgums = self.__pacgums
        else:
            self.nb_pacgums = self.nb_available_cells

    def __is_position_has_superpacgums(self, y: int, x: int) -> bool:
        for ps in self.__super_pacgums_position:
            if (x, y) == ps:
                return True
        return False

    def __get_nb_available_cells(self, grid: List[List]) -> int:
        nb_available_cells = 0

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 15:
                    self.pacgums_grid[y][x] = 0
                elif (x, y) == self.__pacman_position:
                    self.pacgums_grid[y][x] = 0
                elif self.__is_position_has_superpacgums(y, x):
                    self.pacgums_grid[y][x] = 0
                else:
                    self.pacgums_grid[y][x] = 1
                    nb_available_cells += 1

        return nb_available_cells
