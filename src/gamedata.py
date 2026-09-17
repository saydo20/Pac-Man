import ghost, pacman, regular_pacgums, super_pacgums
from mazegenerator import MazeGenerator

from typing import Dict


class GameData:
    def __init__(self, config: Dict) -> None:
        self.__ghosts = ghost.Ghost()
        self.__pacman = pacman.Pacman()
        self.__regular_pacgums = regular_pacgums.RegularPacgum()
        self.__super_pacgums = super_pacgums.SuperPacgum()

        self.levels = config['levels']
        self.size_maze = (self.levels[1]['width'],
                          self.levels[1]['height'])
        self.seed = config['seed']
        self.__mazegen = MazeGenerator(self.size_maze, False,
                                       (0, 0), (-1, -1), self.seed)

    @property
    def ghosts(self) -> ghost.Ghost:
        return self.__ghosts

    @property
    def pacman(self) -> pacman.Pacman:
        return self.__pacman

    @property
    def regular_pacgums(self) -> regular_pacgums.RegularPacgum:
        return self.__regular_pacgums

    @property
    def maze(self) -> MazeGenerator:
        return self.__mazegen

    @property
    def super_pacgums(self) -> super_pacgums.SuperPacgum:
        return self.__super_pacgums
