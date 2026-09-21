from enum import Enum
from typing import Tuple
from gamedata import GameData


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Movement:

    @staticmethod
    def __can_move(current_position: Tuple, direction: Direction) -> bool:
        grid = GameData.static_grid
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

    @staticmethod
    def update_position_by_direction(current_position: Tuple,
                                     direction: Direction) -> Tuple:
        x, y = current_position

        match direction:
            case Direction.UP:
                if Movement.__can_move(current_position, Direction.UP):
                    return (x, y - 1)
            case Direction.DOWN:
                if Movement.__can_move(current_position, Direction.DOWN):
                    return (x, y + 1)
            case Direction.RIGHT:
                if Movement.__can_move(current_position, Direction.RIGHT):
                    return (x + 1, y)
            case Direction.LEFT:
                if Movement.__can_move(current_position, Direction.LEFT):
                    return (x - 1, y)

        return current_position
