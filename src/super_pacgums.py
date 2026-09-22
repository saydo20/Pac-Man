from typing import List, Tuple


class SuperPacgum:
    def __init__(self, size_maze: Tuple):
        self.__super_pacgum_score: int = 0
        self.__size_maze = size_maze
        self.positions: List[Tuple] = self.__super_pacgums_positions()

    def set_super_pacgum_score(self, super_pacgum_score: int) -> None:
        self.__super_pacgum_score = super_pacgum_score

    def __super_pacgums_positions(self) -> List[Tuple]:
        x, y = self.__size_maze

        self.__positions = [
            ((x - x), (y - y)),
            ((x - 1), (y - y)),
            ((x - x), (y - 1)),
            ((x - 1), (y - 1))
        ]

        return self.__positions

    def get_super_pacgum_score(self) -> int:
        return self.__super_pacgum_score
