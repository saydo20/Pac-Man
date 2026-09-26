from typing import Tuple
from enums_helper import Mode, Color
from move_ghosts import MoveGhost


class Ghost:
    def __init__(self, color: Color):
        self.current_position: Tuple = (0, 0)
        self.previous_position = self.current_position
        self.color = color
        self.grid = []
        self.size_maze: Tuple = (0, 0)
        self.mode = Mode.ATTACK

    def __get_right_position(self, x: int, y: int) -> Tuple:
        match self.color:
            case Color.RED | Color.BLUE:
                # Move down but stop before falling off the bottom edge
                while self.grid[y][x] == 15 and y < self.size_maze[1] - 1:
                    y += 1
                return (x, y)

            case Color.GREEN | Color.YELLOW:
                # Move up but stop before hitting a negative number
                while self.grid[y][x] == 15 and y > 0:
                    y -= 1
                return (x, y)

    def set_start_position(self) -> None:
        x, y = self.size_maze

        match self.color:
            case Color.RED:
                self.current_position = self.__get_right_position(0, 0)
            case Color.BLUE:
                self.current_position = self.__get_right_position(x - 1, 0)
            case Color.GREEN:
                self.current_position = self.__get_right_position(0, y - 1)
            case Color.YELLOW:
                self.current_position = self.__get_right_position(x - 1, y - 1)

    def move_ghost(self, pacman_position: Tuple) -> None:
        # make the ghost run from pacman when they are in FLEE mode
        if self.mode == Mode.FLEE:
            next_step = MoveGhost.ghosts_run_away(
                self.grid, self.current_position, self.previous_position,
                pacman_position
            )

            self.previous_position = self.current_position
            self.current_position = next_step

        elif self.mode == Mode.ATTACK:
            # make the red ghost go direct to pacman
            if self.color == Color.RED:
                self.current_position = MoveGhost.Move_ghost_with_bfs(
                    self.grid, self.current_position, pacman_position)

            # Target a tile near Pacman rather than his exact location
            # to prevent the ghosts from stacking.
            elif self.color == Color.YELLOW:
                pac_x, pac_y = pacman_position
                target_position = (pac_x, pac_y + 1)

                next_step = MoveGhost.Move_ghost_with_bfs(
                    self.grid, self.current_position, target_position)

                if next_step == self.current_position:
                    next_step = MoveGhost.Move_ghost_with_bfs(
                        self.grid, self.current_position, pacman_position)

                self.current_position = next_step

            elif self.color in (Color.GREEN, Color.BLUE):
                next_step = MoveGhost.move_ghost_random(
                    self.grid, self.current_position, self.previous_position)

                self.previous_position = self.current_position
                self.current_position = next_step
