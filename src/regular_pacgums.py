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
        self.pacgums_positions: List[Tuple] = []

        # get data from config file, and get the available cells for dots
        self.score_pacgum = config.get('points_per_pacgum', 10)
        self.nb_available_cells = self.__get_nb_available_cells(grid)
        self.__pacgums = config.get('pacgum', self.nb_available_cells)

        # get the number of pacgums
        if self.__pacgums <= self.nb_available_cells:
            self.nb_pacgums = self.__pacgums
        else:
            self.nb_pacgums = self.nb_available_cells

        # get randomly the postions of dots
        self.pacgums_positions = random.sample(self.pacgums_positions,
                                               self.nb_pacgums)

    def __is_position_has_superpacgums(self, y: int, x: int) -> bool:
        for ps in self.__super_pacgums_position:
            if (x, y) == ps:
                return True
        return False

    def __is_position_has_ghost(self, y: int, x: int) -> bool:
        return (x, y) in self.__ghosts_position

    def __get_nb_available_cells(self, grid: List[List]) -> int:
        nb_available_cells = 0

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 15:
                    continue
                elif (x, y) == self.__pacman_position:
                    continue
                elif self.__is_position_has_superpacgums(y, x):
                    continue
                elif self.__is_position_has_ghost(y, x):
                    continue
                else:
                    self.pacgums_positions.append((x, y))
                    nb_available_cells += 1

        return nb_available_cells
