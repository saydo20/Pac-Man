"""Enum definitions for directions, game modes, and ghost colors."""

from enum import Enum


class Direction(Enum):
    """Represents movement directions using bitmask values."""

    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Mode(Enum):
    """Represents game entity modes."""

    ATTACK = 1
    FLEE = 2
    DEAD = 3
    WIN = 4


class Color(Enum):
    """Represents ghost color identifiers."""

    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
