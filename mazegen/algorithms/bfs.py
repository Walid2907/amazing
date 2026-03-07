from collections import deque
from typing import Optional


# Wall bit masks
NORTH = 1  # bit 0
EAST = 2  # bit 1
SOUTH = 4  # bit 2
WEST = 8  # bit 3

# Direction vectors: (dr, dc, wall bit to check in current cell)
DIRECTIONS = {
    'N': (-1, 0, NORTH),
    'E': (0, 1, EAST),
    'S': (1, 0, SOUTH),
    'W': (0, -1, WEST),
}


def bfs(
    grid: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int]
) -> Optional[list[str]]:
    """
    BFS shortest path on a maze grid encoded with 4-bit wall values.

    Args:
        grid: 2D list of ints; each cell is a 4-bit mask where
              1=North wall closed, 2=East, 4=South, 8=West.
        start: (row, col) of the entry cell.
        end: (row, col) of the exit cell.

    Returns:
        List of direction letters ['N','E','S','W'] representing the
        shortest path, or None if no path exists.
    """
    # swap x,y into y,x because i used the algo this way row, coll
    t = start
    start = (t[1], t[0])
    t = end
    end = (t[1], t[0])

    rows = len(grid)
    cols = len(grid[0])

    queue: deque[tuple[int, int, list[str]]] = deque()
    queue.append((start[0], start[1], []))
    visited: set[tuple[int, int]] = {start}

    while queue:
        r, c, path = queue.popleft()

        if (r, c) == end:
            return path

        for letter, (dr, dc, wall_bit) in DIRECTIONS.items():
            # Can we go this direction? Wall must be OPEN (bit = 0)
            if grid[r][c] & wall_bit:
                continue  # wall is closed

            nr, nc = r + dr, c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if (nr, nc) in visited:
                continue

            visited.add((nr, nc))
            queue.append((nr, nc, path + [letter]))

    return None  # no path found


def path_to_cells(start: tuple[int, int],
                  solution: list[str]) -> list[tuple[int, int]]:
    """
    Convert a start position and list of direction letters to a list of cells.

    Args:
        start:      (row, col) starting cell.
        solution: List of 'N', 'E', 'S', 'W' moves.

    Returns:
        Ordered list of (row, col) cells including start and end.
    """
    cords = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    cells: list[tuple[int, int]] = [start]
    r, c = start
    for d in solution:
        dr, dc = cords[d]
        r, c = r + dr, c + dc
        cells.append((r, c))
    return cells
