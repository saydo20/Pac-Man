"""Super pacgum management module."""

from typing import List, Tuple


class SuperPacgum:
    """Manages super pacgum positions and score values."""

    def __init__(self, size_maze: Tuple):
        """Initialize super pacgums at the four maze corners.

        Args:
            size_maze: Tuple of (width, height) of the maze.
        """
        self.__super_pacgum_score: int = 0
        self.__size_maze = size_maze
        self.positions: List[Tuple] = self.get_super_pacgums_positions()

    def set_super_pacgum_score(self, super_pacgum_score: int) -> None:
        """Set the score value for eating a super pacgum.

        Args:
            super_pacgum_score: Points awarded per super pacgum.
        """
        self.__super_pacgum_score = super_pacgum_score

    def get_super_pacgums_positions(self) -> List[Tuple]:
        """Calculate super pacgum positions at the four maze corners.

        Returns:
            List of (x, y) tuples for each corner position.
        """
        x, y = self.__size_maze

        positions = [
            ((x - x), (y - y)),
            ((x - 1), (y - y)),
            ((x - x), (y - 1)),
            ((x - 1), (y - 1))
        ]
        return positions

    def get_super_pacgum_score(self) -> int:
        """Return the score value for a super pacgum.

        Returns:
            Points awarded for eating a super pacgum.
        """
        return self.__super_pacgum_score
