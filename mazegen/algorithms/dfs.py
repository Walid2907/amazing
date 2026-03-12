import random
from typing import Optional
from config import set_42_limits

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

WALL_BITS = {
    NORTH: 1,
    EAST: 2,
    SOUTH: 4,
    WEST: 8,
}
OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}
CHANGES = {
    NORTH: (-1, 0),
    EAST:  (0, 1),
    SOUTH: (1, 0),
    WEST:  (0, -1),
}


def random_opens(grid: list[list[int]], width: int,
                 height: int, rng: random.Random,
                 form_42: list[tuple[int, int]],
                 carve_chance: float = 0.1) -> None:

    def enforce_42(grid_: list[list[int]],
                   form_42_: list[tuple[int, int]],
                   width_: int, height_: int) -> None:
        for rw, cw in form_42_:
            grid_[rw][cw] |= 0xF
        for row, col in form_42_:
            neighbors_of_42 = [
                (row - 1, col, SOUTH),
                (row, col + 1, WEST),
                (row + 1, col, NORTH),
                (row, col - 1, EAST)
            ]
            for nr, nc, direction_toward_42 in neighbors_of_42:
                if not (0 <= nr < height_ and 0 <= nc < width_):
                    continue
                if (nr, nc) in form_42_:
                    continue
                grid_[nr][nc] |= WALL_BITS[direction_toward_42]

    for r in range(height):
        for c in range(width):
            if c < width - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[EAST]:
                    grid[r][c] &= ~WALL_BITS[EAST]
                    grid[r][c + 1] &= ~WALL_BITS[WEST]
            if r < height - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[SOUTH]:
                    grid[r][c] &= ~WALL_BITS[SOUTH]
                    grid[r + 1][c] &= ~WALL_BITS[NORTH]

    enforce_42(grid, form_42, width, height)


def dfs(width: int, height: int, seed: Optional[int] = None,
        perfect: bool = True) -> list[list[int]]:

    form_42 = set_42_limits(width, height)
    form_42_set = set(form_42)
    rng = random.Random(seed)

    grid: list[list[int]] = [[0xF] * width for _ in range(height)]
    visited: list[list[bool]] = [[False] * width for _ in range(height)]

    for (r42, c42) in form_42_set:
        if 0 <= r42 < height and 0 <= c42 < width:
            visited[r42][c42] = True

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < height and 0 <= c < width

    def remove_wall(r1: int, c1: int, direction: int) -> None:
        dr, dc = CHANGES[direction]
        r2, c2 = r1 + dr, c1 + dc
        if (r1, c1) in form_42_set or (r2, c2) in form_42_set:
            return
        grid[r1][c1] &= ~WALL_BITS[direction]
        grid[r2][c2] &= ~WALL_BITS[OPPOSITE[direction]]

    def dfs_helper(start_r: int, start_c: int) -> None:
        stack = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            curr_r, curr_c = stack[-1]
            directions = [NORTH, EAST, SOUTH, WEST]
            rng.shuffle(directions)
            moved = False
            for direction in directions:
                dr, dc = CHANGES[direction]
                neighbor_r = curr_r + dr
                neighbor_c = curr_c + dc
                if (in_bounds(neighbor_r, neighbor_c) and
                        not visited[neighbor_r][neighbor_c]):
                    remove_wall(curr_r, curr_c, direction)
                    visited[neighbor_r][neighbor_c] = True
                    stack.append((neighbor_r, neighbor_c))
                    moved = True
                    break
            if not moved:
                stack.pop()

    while True:
        start_r = rng.randint(0, height - 1)
        start_c = 0
        if (start_r, start_c) not in form_42_set:
            break

    dfs_helper(start_r, start_c)

    if not perfect:
        random_opens(grid, width, height, rng, form_42)

    return grid
