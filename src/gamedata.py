"""Game data management module for maze, entities, and game state."""

from src.ghost import Ghost
from src.pacman import Pacman
from src.super_pacgums import SuperPacgum
from src.regular_pacgums import RegularPacgum
from src.enums_helper import Direction, Mode, Color

from mazegenerator import MazeGenerator
from typing import Dict, Tuple, List


class GameData:
    """Manages all game state including maze, ghosts, pacman, and pacgums."""

    def __init__(self, config: Dict) -> None:
        """Initialize the game with maze, entities, and scoring from config.

        Args:
            config: Dictionary of game configuration values.
        """
        self.config = config

        # set the maze
        self.size_maze = (15, 15)
        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), 42)
        self.grid = self.maze.maze

        self.nb_level = 1
        self.__original_time = config.get('level_max_time', 90)
        self.time_count = self.__original_time

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

        self.__regular_pacgums = RegularPacgum(
            config, self.__pacman.current_position,
            self.__super_pacgums.positions, self.grid,
            self.nb_level)

    @property
    def ghost_red(self) -> Ghost:
        """Return the red ghost instance."""
        return self.__ghost_red

    @property
    def ghost_blue(self) -> Ghost:
        """Return the blue ghost instance."""
        return self.__ghost_blue

    @property
    def ghost_green(self) -> Ghost:
        """Return the green ghost instance."""
        return self.__ghost_green

    @property
    def ghost_yellow(self) -> Ghost:
        """Return the yellow ghost instance."""
        return self.__ghost_yellow

    @property
    def pacman(self) -> Pacman:
        """Return the Pac-Man instance."""
        return self.__pacman

    @property
    def regular_pacgums(self) -> RegularPacgum:
        """Return the regular pacgums instance."""
        return self.__regular_pacgums

    @property
    def super_pacgums(self) -> SuperPacgum:
        """Return the super pacgums instance."""
        return self.__super_pacgums

    def __set_the_ghosts(self) -> None:
        """Create and position all four ghosts on the maze."""
        # initialize red ghost and his start location
        self.__ghost_red = Ghost(Color.RED)
        self.__ghost_red.grid = self.grid
        self.__ghost_red.size_maze = self.size_maze
        self.__ghost_red.set_start_position()

        # initialize blue ghost and his start location
        self.__ghost_blue = Ghost(Color.BLUE)
        self.__ghost_blue.grid = self.grid
        self.__ghost_blue.size_maze = self.size_maze
        self.__ghost_blue.set_start_position()

        # initialize green ghost and his start location
        self.__ghost_green = Ghost(Color.GREEN)
        self.__ghost_green.grid = self.grid
        self.__ghost_green.size_maze = self.size_maze
        self.__ghost_green.set_start_position()

        # initialize yellow ghost and his start location
        self.__ghost_yellow = Ghost(Color.YELLOW)
        self.__ghost_yellow.grid = self.grid
        self.__ghost_yellow.size_maze = self.size_maze
        self.__ghost_yellow.set_start_position()

    def __set_pacman(self, lives: int) -> None:
        """Create and position Pac-Man on the maze.

        Args:
            lives: Number of lives for Pac-Man.
        """
        self.__pacman = Pacman(lives)
        self.__pacman.grid = self.grid
        self.__pacman.size_maze = self.size_maze
        self.__pacman.start_position()

    def __can_move(self, current_position: Tuple, direction: Direction,
                   grid: List[List]) -> bool:
        """Check if movement in the given direction is valid.

        Args:
            current_position: Current (x, y) position.
            direction: Direction to move.
            grid: The maze grid.

        Returns:
            True if no wall blocks the movement.
        """
        x, y = current_position

        if direction.value & grid[y][x] > 0:
            return False

        return True

    def __add_score_to_pacman(self, current_position: Tuple,
                              grid_pacgums: List[List]) -> None:
        """Add score to Pac-Man when eating pacgums or super pacgums.

        Args:
            current_position: Pac-Man's current (x, y) position.
            grid_pacgums: The pacgum grid to check and update.
        """
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
        """Generate the next maze level and reset all entities."""

        self.nb_level += 1
        if self.nb_level > 10:
            self.pacman.mode = Mode.WIN
            return

        # set the maze
        self.maze = MazeGenerator(self.size_maze, False,
                                  (0, 0), (-1, -1), 0)

        self.grid.clear()
        self.grid.extend(self.maze.maze)

        self.__pacman.start_position()
        self.__pacman.mode = Mode.FLEE

        # initialize super pacgums
        temp_super = SuperPacgum(self.size_maze)
        old_super_positions = self.__super_pacgums.positions
        old_super_positions.clear()
        old_super_positions.extend(temp_super.positions)
        self.__super_pacgums.positions = old_super_positions

        self.__ghost_blue.set_start_position()
        self.__ghost_blue.previous_position = self.ghost_blue.current_position
        self.__ghost_blue.mode = Mode.ATTACK

        self.__ghost_green.set_start_position()
        self.__ghost_green.previous_position = (
            self.__ghost_green.current_position)
        self.__ghost_green.mode = Mode.ATTACK

        self.__ghost_yellow.set_start_position()
        self.__ghost_yellow.previous_position = (
            self.__ghost_yellow.current_position)
        self.__ghost_yellow.mode = Mode.ATTACK

        self.__ghost_red.set_start_position()
        self.__ghost_red.previous_position = self.__ghost_red.current_position
        self.__ghost_red.mode = Mode.ATTACK

        self.time_count = self.__original_time
        old_pacgums_grid = self.__regular_pacgums.pacgums_grid
        self.__regular_pacgums = RegularPacgum(
            self.config, self.__pacman.current_position,
            self.__super_pacgums.positions, self.grid,
            self.nb_level)

        old_pacgums_grid.clear()
        old_pacgums_grid.extend(self.__regular_pacgums.pacgums_grid)
        self.__regular_pacgums.pacgums_grid = old_pacgums_grid

    def change_mode_player_ghosts(self, pacman_mode: Mode,
                                  ghost_mode: Mode) -> None:
        """Change the mode of Pac-Man and all ghosts.

        Args:
            pacman_mode: New mode for Pac-Man.
            ghost_mode: New mode for all ghosts.
        """
        # change the mode of the player
        self.pacman.mode = pacman_mode

        # change the mode of the ghosts
        self.ghost_red.mode = ghost_mode
        self.ghost_yellow.mode = ghost_mode
        self.ghost_green.mode = ghost_mode
        self.ghost_blue.mode = ghost_mode

    def update_pos_by_dirc(self, current_position: Tuple,
                           direction: Direction) -> Tuple:
        """Move Pac-Man in the given direction if valid.

        Args:
            current_position: Current (x, y) position.
            direction: Direction to move.

        Returns:
            Updated (x, y) position, or original if blocked.
        """
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
