from typing import Tuple, List
from enums_helper import Mode, Color
from bfs import BFS


class Ghost:
    def __init__(self, size_maze: Tuple, color: Color, grid: List[List]):
        self.current_position: Tuple = (0, 0)
        self.color = color
        self.__grid = grid
        self.__size_maze: Tuple = size_maze
        self.mode = Mode.ATTACK

    def __get_right_position(self, x: int, y: int) -> Tuple:
        match self.color:
            case Color.RED | Color.BLUE:
                # Move down but stop before falling off the bottom edge
                while self.__grid[y][x] == 15 and y < self.__size_maze[1] - 1:
                    y += 1
                return (x, y)

            case Color.GREEN | Color.YELLOW:
                # Move up but stop before hitting a negative number
                while self.__grid[y][x] == 15 and y > 0:
                    y -= 1
                return (x, y)

    def set_start_position(self) -> None:
        x, y = self.__size_maze

        match self.color:
            case Color.RED:
                self.current_position = self.__get_right_position(1, 0)
            case Color.BLUE:
                self.current_position = self.__get_right_position(x - 1, 1)
            case Color.GREEN:
                self.current_position = self.__get_right_position(1, y - 1)
            case Color.YELLOW:
                self.current_position = self.__get_right_position(x - 1, y - 2)

    def move_ghost(self, pacman_position: Tuple) -> Tuple:
        self.current_position = BFS.shortest_path(self.__grid,
                                                  self.current_position,
                                                  pacman_position)
