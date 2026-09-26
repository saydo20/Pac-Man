from typing import Tuple
from enums_helper import Mode


class Pacman:
    def __init__(self, lives: int = 3):
        self.current_position: Tuple
        self.lives = lives
        self.score: int = 0
        self.grid = []
        self.size_maze: Tuple = (0, 0)
        self.mode = Mode.FLEE

    def start_position(self) -> None:
        width, height = self.size_maze
        x = width // 2
        y = height // 2

        while self.grid[y][x] == 15:
            y -= 1
        self.current_position = (x, y)
