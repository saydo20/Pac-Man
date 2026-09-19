from typing import Tuple, List


class Pacman:
    def __init__(self, size_maze: Tuple, grid: List[List], lives: int = 3):
        self.current_position: Tuple
        self.lives = lives
        self.__grid = grid
        self.__size_maze: Tuple = size_maze

    def start_position(self) -> None:
        width, height = self.__size_maze
        x = width // 2
        y = height // 2

        while self.__grid[y][x] == 15:
            y -= 1
        self.current_position = (x, y)
