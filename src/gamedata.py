from ghost import Ghost, Color
from pacman import Pacman
from super_pacgums import SuperPacgum
from regular_pacgums import RegularPacgum

from mazegenerator import MazeGenerator
from typing import Dict


class GameData:
    static_grid = []

    def __init__(self, config: Dict) -> None:
        # set the maze
        self.size_maze = (15, 15)
        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), 42)
        self.grid = self.maze.maze
        GameData.static_grid = self.grid
        # initialize the 4 ghosts
        self.__set_the_ghosts()
        self.score_per_ghost = config.get('points_per_ghost', 200)

        # initialize pacman and set his start location
        self.__set_pacman(config.get('lives', 3))

        # initialize super pacgums
        self.__super_pacgums = SuperPacgum(self.size_maze)
        self.super_pacgums.set_super_pacgum_score(
            config.get('points_per_super_pacgum', 50))

        # initialize regular pacgums
        self.__ghosts_position = [
            self.ghost_red.current_position,
            self.ghost_yellow.current_position,
            self.ghost_green.current_position,
            self.ghost_blue.current_position,
        ]
        self.__regular_pacgums = RegularPacgum(
            config, self.grid, self.pacman.current_position,
            self.super_pacgums.get_super_pacgums_positions(),
            self.__ghosts_position)

    @property
    def ghost_red(self) -> Ghost:
        return self.__ghost_red

    @property
    def ghost_blue(self) -> Ghost:
        return self.__ghost_blue

    @property
    def ghost_green(self) -> Ghost:
        return self.__ghost_green

    @property
    def ghost_yellow(self) -> Ghost:
        return self.__ghost_yellow

    @property
    def pacman(self) -> Pacman:
        return self.__pacman

    @property
    def regular_pacgums(self) -> RegularPacgum:
        return self.__regular_pacgums

    @property
    def super_pacgums(self) -> SuperPacgum:
        return self.__super_pacgums

    def __set_the_ghosts(self) -> None:
        # initialize red ghost and his start location
        self.__ghost_red = Ghost(self.size_maze, Color.RED,
                                 self.grid)
        self.__ghost_red.set_start_position()

        # initialize blue ghost and his start location
        self.__ghost_blue = Ghost(self.size_maze, Color.BLUE,
                                  self.grid)
        self.__ghost_blue.set_start_position()

        # initialize green ghost and his start location
        self.__ghost_green = Ghost(self.size_maze, Color.GREEN,
                                   self.grid)
        self.__ghost_green.set_start_position()

        # initialize yellow ghost and his start location
        self.__ghost_yellow = Ghost(self.size_maze, Color.YELLOW,
                                    self.grid)
        self.__ghost_yellow.set_start_position()

    def __set_pacman(self, lives: int) -> None:
        self.__pacman = Pacman(self.size_maze, self.grid, lives)
        self.__pacman.start_position()
