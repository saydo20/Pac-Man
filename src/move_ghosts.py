"""Ghost movement algorithms module."""

from typing import Tuple, List
from collections import deque
import random

from src.enums_helper import Direction


class MoveGhost:
    """Provides static methods for ghost movement strategies."""

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    @staticmethod
    def __is_wall_not_exist(current_position: Tuple,
                            dx: int, dy: int,
                            grid: List[List]) -> bool:
        """Check if no wall blocks movement in the given direction.

        Args:
            current_position: Current (x, y) position.
            dx: Horizontal direction offset.
            dy: Vertical direction offset.
            grid: The maze grid.

        Returns:
            True if movement is not blocked by a wall.
        """
        x, y = current_position
        if (dx, dy) == (0, -1):
            direction = Direction.UP
        elif (dx, dy) == (0, 1):
            direction = Direction.DOWN
        elif (dx, dy) == (-1, 0):
            direction = Direction.LEFT
        elif (dx, dy) == (1, 0):
            direction = Direction.RIGHT

        if grid[y][x] & direction.value > 0:
            return False

        return True

    @staticmethod
    def ghosts_run_away(grid: List[List], start_position: Tuple,
                        previous_position: Tuple,
                        pacman_position: Tuple) -> Tuple:
        """Move ghost away from Pac-Man using Manhattan distance.

        Args:
            grid: The maze grid.
            start_position: Ghost's current position.
            previous_position: Ghost's previous position.
            pacman_position: Pac-Man's current position.

        Returns:
            The next position that maximizes distance from Pac-Man.
        """
        valid_moves = []
        x, y = start_position
        max_y = len(grid)
        max_x = len(grid[0])
        px, py = pacman_position

        for dx, dy in MoveGhost.directions:
            next_x, next_y = dx + x, dy + y
            neighbor = (next_x, next_y)

            if 0 <= next_x < max_x and 0 <= next_y < max_y:
                if MoveGhost.__is_wall_not_exist(start_position, dx, dy, grid):
                    valid_moves.append(neighbor)

        if len(valid_moves) > 1 and previous_position in valid_moves:
            valid_moves.remove(previous_position)

        best_move = start_position
        max_distance = -1

        for move in valid_moves:
            mx, my = move
            distance = abs(px - mx) + abs(py - my)

            if distance > max_distance:
                max_distance = distance
                best_move = move

        return best_move

    @staticmethod
    def move_ghost_random(grid: List[List], start_position: Tuple,
                          previous_position: Tuple) -> Tuple:
        """Move ghost to a random valid neighbor, avoiding backtracking.

        Args:
            grid: The maze grid.
            start_position: Ghost's current position.
            previous_position: Ghost's previous position.

        Returns:
            A randomly chosen valid neighbor position.
        """
        valid_moves = []
        x, y = start_position
        max_y = len(grid)
        max_x = len(grid[0])

        for dx, dy in MoveGhost.directions:
            next_x, next_y = dx + x, dy + y
            neighbor = (next_x, next_y)

            if 0 <= next_x < max_x and 0 <= next_y < max_y:
                if MoveGhost.__is_wall_not_exist(start_position, dx, dy, grid):
                    valid_moves.append(neighbor)

        if len(valid_moves) > 1 and previous_position in valid_moves:
            valid_moves.remove(previous_position)

        if valid_moves:
            return random.choice(valid_moves)

        return start_position

    @staticmethod
    def Move_ghost_with_bfs(grid: List[List], start_position: Tuple,
                            target_position: Tuple) -> Tuple:
        """Find the next step toward a target using BFS pathfinding.

        Args:
            grid: The maze grid.
            start_position: Ghost's current position.
            target_position: The target position to reach.

        Returns:
            The next position along the shortest path to the target.
        """
        queue = deque([start_position])
        visited = set()
        parents: dict = {}
        path = []
        visited.add(start_position)

        len_cols = len(grid[0])
        len_rows = len(grid)

        while queue:
            current = queue.popleft()
            x, y = current

            if current == target_position:
                path.append(current)
                while current != start_position:
                    path.append(parents[current])
                    current = parents[current]
                path.reverse()
                if len(path) > 1:
                    return path[1]
                else:
                    return start_position

            for dx, dy in MoveGhost.directions:
                next_x, next_y = dx + x, dy + y
                neighbor = (next_x, next_y)

                if 0 <= next_x < len_cols and 0 <= next_y < len_rows:
                    if (MoveGhost.__is_wall_not_exist(current, dx, dy, grid)
                            and neighbor not in visited):
                        visited.add(neighbor)
                        queue.append(neighbor)
                        parents[neighbor] = current

        return start_position
