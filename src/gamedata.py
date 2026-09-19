import ghost
import pacman
import super_pacgums
import regular_pacgums

from mazegenerator import MazeGenerator

from typing import Dict


class GameData:
    def __init__(self, config: Dict) -> None:
        self.levels = config['levels']
        self.size_maze = (self.levels[1]['width'],
                          self.levels[1]['height'])

        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), config['seed'])

        self.grid = self.maze.maze

        # initialize the 4 ghosts
        self.__set_the_ghosts()

        # initialize pacman and set his start location
        self.__set_pacman(config['lives'])

        # initialize regular pacgums
        self.__regular_pacgums = regular_pacgums.RegularPacgum()

        # initialize super pacgums
        self.__super_pacgums = super_pacgums.SuperPacgum(self.size_maze)
        self.super_pacgums.set_super_pacgum_score(
            config['points_per_super_pacgum'])

    @property
    def ghost_red(self) -> ghost.Ghost:
        return self.__ghost_red

    @property
    def ghost_blue(self) -> ghost.Ghost:
        return self.__ghost_blue

    @property
    def ghost_green(self) -> ghost.Ghost:
        return self.__ghost_green

    @property
    def ghost_yellow(self) -> ghost.Ghost:
        return self.__ghost_yellow

    @property
    def pacman(self) -> pacman.Pacman:
        return self.__pacman

    @property
    def regular_pacgums(self) -> regular_pacgums.RegularPacgum:
        return self.__regular_pacgums

    @property
    def super_pacgums(self) -> super_pacgums.SuperPacgum:
        return self.__super_pacgums

    def __set_the_ghosts(self) -> None:
        # initialize red ghost and his start location
        self.__ghost_red = ghost.Ghost(self.size_maze, ghost.Color.RED,
                                       self.grid)
        self.__ghost_red.set_start_position()

        # initialize blue ghost and his start location
        self.__ghost_blue = ghost.Ghost(self.size_maze, ghost.Color.BLUE,
                                        self.grid)
        self.__ghost_blue.set_start_position()

        # initialize green ghost and his start location
        self.__ghost_green = ghost.Ghost(self.size_maze, ghost.Color.GREEN,
                                         self.grid)
        self.__ghost_green.set_start_position()

        # initialize yellow ghost and his start location
        self.__ghost_yellow = ghost.Ghost(self.size_maze, ghost.Color.YELLOW,
                                          self.grid)
        self.__ghost_yellow.set_start_position()

    def __set_pacman(self, lives: int) -> None:
        self.__pacman = pacman.Pacman(self.size_maze, self.grid, lives)
        self.__pacman.start_position()
