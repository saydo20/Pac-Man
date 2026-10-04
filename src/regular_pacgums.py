import random
from typing import List, Dict, Tuple


class RegularPacgum:

    def __init__(self, config: Dict,
                 pacman_position: Tuple,
                 super_pacgums_position: List[Tuple],
                 grid: List[List], nb_level: int) -> None:

        self.__pacman_position = pacman_position
        self.__super_pacgums_position = super_pacgums_position
        self.__grid = grid

        self.pacgums_grid: List[List] = [[0 for _ in row] for
                                         row in self.__grid]

        self.score_pacgum = config.get('points_per_pacgum', 10)

        self.available_coords = self.__get_available_coords(self.__grid)

        self.nb_available_cells = len(self.available_coords)

        calculated_pacgums = (self.nb_available_cells * (nb_level + 2)) // 12
        self.nb_pacgums = min(calculated_pacgums, self.nb_available_cells)

        chosen_cells = random.sample(self.available_coords, self.nb_pacgums)

        for y, x in chosen_cells:
            self.pacgums_grid[y][x] = 1

    def __is_position_has_superpacgums(self, y: int, x: int) -> bool:
        for ps in self.__super_pacgums_position:
            if (x, y) == ps:
                return True
        return False

    def __get_available_coords(self, grid: List[List]) -> List[Tuple]:
        available_cells = []

        for y in range(len(grid)):
            for x in range(len(grid[y])):

                if grid[y][x] == 15:
                    pass
                elif (x, y) == self.__pacman_position:
                    pass
                elif self.__is_position_has_superpacgums(y, x):
                    pass
                else:
                    available_cells.append((y, x))

        return available_cells
