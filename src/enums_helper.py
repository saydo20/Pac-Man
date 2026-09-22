from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Mode(Enum):
    ATTACK = 1
    FLEE = 2


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
