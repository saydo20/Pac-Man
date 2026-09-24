from ghost import Ghost
from pacman import Pacman
from super_pacgums import SuperPacgum
from regular_pacgums import RegularPacgum
from enums_helper import Direction, Mode, Color

from mazegenerator import MazeGenerator
from typing import Dict, Tuple, List


class GameData:

    def __init__(self, config: Dict) -> None:
        self.config = config

        # set the maze
        self.size_maze = (15, 15)
        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), 42)
        self.grid = self.maze.maze

        # initialize the 4 ghosts
        self.__set_the_ghosts()
        self.score_per_ghost = config.get('points_per_ghost', 200)

        # get the score of each pacgum
        self.score_per_pacgum: int = config.get('points_per_pacgum', 10)

        # initialize pacman and set his start location
        self.__set_pacman(config.get('lives', 3))

        # initialize super pacgums
        self.__super_pacgums = SuperPacgum(self.size_maze)
        self.__super_pacgums.set_super_pacgum_score(
            config.get('points_per_super_pacgum', 50))

        # initialize regular pacgums
        self.__ghosts_position = [
            self.__ghost_red.current_position,
            self.__ghost_yellow.current_position,
            self.__ghost_green.current_position,
            self.__ghost_blue.current_position,
        ]
        self.__regular_pacgums = RegularPacgum(
            config, self.grid, self.__pacman.current_position,
            self.__super_pacgums.positions,
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

    def __can_move(self, current_position: Tuple, direction: Direction,
                   grid: List[List]) -> bool:
        x, y = current_position

        match direction:
            case Direction.UP:
                if grid[y][x] & Direction.UP.value > 0:
                    return False
            case Direction.RIGHT:
                if grid[y][x] & Direction.RIGHT.value > 0:
                    return False
            case Direction.DOWN:
                if grid[y][x] & Direction.DOWN.value > 0:
                    return False
            case Direction.LEFT:
                if grid[y][x] & Direction.LEFT.value > 0:
                    return False
        return True

    def __add_score_to_pacman(self, current_position: Tuple,
                              grid_pacgums: List[List]) -> None:
        x, y = current_position

        # check if the pacman eat super_pacgum
        if current_position in self.super_pacgums.positions:
            self.pacman.score += self.super_pacgums.get_super_pacgum_score()
            self.change_mode_player_ghosts(Mode.ATTACK, Mode.FLEE)
            self.super_pacgums.positions.remove(current_position)

        # check if pacman eat regular_pacgum
        if grid_pacgums[y][x] == 1:
            grid_pacgums[y][x] = 0
            self.pacman.score += self.score_per_pacgum

    def generate_next_level(self) -> None:
        # set the maze
        self.size_maze = (15, 15)
        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), 0)

        self.__pacman.start_position()
        self.__pacman.mode = Mode.FLEE

        # initialize super pacgums
        self.__super_pacgums.get_super_pacgums_positions()

        self.__ghost_blue.set_start_position()
        self.__ghost_blue.mode = Mode.ATTACK

        self.__ghost_green.set_start_position()
        self.__ghost_green.mode = Mode.ATTACK

        self.__ghost_yellow.set_start_position()
        self.__ghost_yellow.mode = Mode.ATTACK

        self.__ghost_red.set_start_position()
        self.__ghost_red.mode = Mode.ATTACK

        # initialize regular pacgums
        self.__ghosts_position = [
            self.__ghost_red.current_position,
            self.__ghost_yellow.current_position,
            self.__ghost_green.current_position,
            self.__ghost_blue.current_position,
        ]
        self.__regular_pacgums = RegularPacgum(
            self.config, self.grid, self.__pacman.current_position,
            self.__super_pacgums.positions,
            self.__ghosts_position)

    def change_mode_player_ghosts(self, pacman_mode: Mode,
                                  ghost_mode: Mode) -> None:
        # change the mode of the player
        self.pacman.mode = pacman_mode

        # change the mode of the ghosts
        self.ghost_red.mode = ghost_mode
        self.ghost_yellow.mode = ghost_mode
        self.ghost_green.mode = ghost_mode
        self.ghost_blue.mode = ghost_mode

    def update_position_by_direction(self, current_position: Tuple,
                                     direction: Direction) -> Tuple:
        x, y = current_position
        grid_maze = self.grid
        grid_pacgums = self.regular_pacgums.pacgums_grid

        match direction:
            case Direction.UP:
                if self.__can_move(current_position, Direction.UP,
                                   grid_maze):
                    current_position = (x, y - 1)
                    self.__add_score_to_pacman(current_position, grid_pacgums)
                    return current_position
            case Direction.DOWN:
                if self.__can_move(current_position, Direction.DOWN,
                                   grid_maze):
                    current_position = (x, y + 1)
                    self.__add_score_to_pacman(current_position, grid_pacgums)
                    return current_position
            case Direction.RIGHT:
                if self.__can_move(current_position, Direction.RIGHT,
                                   grid_maze):
                    current_position = (x + 1, y)
                    self.__add_score_to_pacman(current_position, grid_pacgums)
                    return current_position
            case Direction.LEFT:
                if self.__can_move(current_position, Direction.LEFT,
                                   grid_maze):
                    current_position = (x - 1, y)
                    self.__add_score_to_pacman(current_position, grid_pacgums)
                    return current_position

        return current_position
