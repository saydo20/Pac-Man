from enum import Enum
from typing import Tuple


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Movement:
    @staticmethod
    def update_position_by_direction(current_position: Tuple,
                                     direction: Direction) -> Tuple:
        x, y = current_position

        match direction:
            case Direction.UP:
                current_position = (x, y - 1)
            case Direction.DOWN:
                current_position = (x, y + 1)
            case Direction.RIGHT:
                current_position = (x + 1, y)
            case Direction.LEFT:
                current_position = (x - 1, y)
            case _:
                return current_position

        return current_position
