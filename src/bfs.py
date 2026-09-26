from typing import Tuple, List
from collections import deque


class BFS:
    @staticmethod
    def shortest_path(grid: List[List], start_position: Tuple,
                      target_position: Tuple) -> Tuple:
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        queue = deque([start_position])
        visited = set()
        parents = {}
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

            for dx, dy in directions:
                next_x, next_y = dx + x, dy + y
                neighbor = (next_x, next_y)
                if 0 <= next_x < len_cols and 0 <= next_y < len_rows:
                    if grid[next_y][next_x] != 15 and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        parents[neighbor] = current

        return start_position
