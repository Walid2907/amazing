"""
Prim's Algorithm - Maze Generator for A-Maze-ing (42 project)
==============================================================
"""
import random
from typing import Optional

# --- Direction constants ---
NORTH = 0  # bit 0 → value 1
EAST = 1  # bit 1 → value 2
SOUTH = 2  # bit 2 → value 4
WEST = 3  # bit 3 → value 8

WALL_BITS = {NORTH: 1, EAST: 2, SOUTH: 4, WEST: 8}

# Opposite direction
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

# Derived for each direction
CHANGES = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}


# Set 42 limits
def set_42_limits(width: int, height: int) -> list[tuple[int, int]]:
    """Return coordinates forming the 42 pattern in the maze."""
    center_r = int(height / 2)
    center_c = int(width / 2)

    # The cells that can build together a 42 pattern
    coords_fc: list[tuple[int, int]] = [
        (0, -1), (0, -2), (0, -3), (-1, -3),
        (-2, -3), (1, -1), (2, -1), (0, 1),
        (1, 1), (2, 1), (2, 2), (2, 3),
        (0, 2), (0, 3), (-1, 3), (-2, 3),
        (-2, 2), (-2, 1)
    ]

    form_42: list[tuple[int, int]] = []

    for dr, dc in coords_fc:
        target_r, target_c = center_r + dr, center_c + dc
        form_42.append((target_r, target_c))

    return form_42


def generate_maze(
    width: int,
    height: int,
    seed: Optional[int] = None,
    perfect: bool = True,
) -> list[list[int]]:
    """
    Generate the maze using Prim's algorithm:
    - Start with one random cell fully walled
    - Pick random walls and remove them to connect to unvisited cells
    - Continue until no walls remain in the frontier
    """
    form_42 = set_42_limits(width, height)
    rng = random.Random(seed)

    # Start: every cell fully walled (0xF = all 4 walls closed)
    grid: list[list[int]] = [[0xF] * width for _ in range(height)]
    visited: list[list[bool]] = [[False] * width for _ in range(height)]

    def in_bounds(r: int, c: int) -> bool:
        """Return True if (r, c) is inside the grid."""
        return 0 <= r < height and 0 <= c < width

    def remove_wall(r1: int, c1: int, direction: int) -> None:
        """
        Remove the wall between cell (r1, c1) and its neighbor in `direction`.
        Updates both cells to keep wall data coherent (subject rule).
        """
        dr, dc = CHANGES[direction]
        r2, c2 = r1 + dr, c1 + dc

        if (r2, c2) in form_42 or (r1, c2) in form_42:
            return

        grid[r1][c1] &= ~WALL_BITS[direction]
        grid[r2][c2] &= ~WALL_BITS[OPPOSITE[direction]]

    # --- Prim's Algorithm ---
    start_r = rng.randint(0, height - 1)
    start_c = 0
    visited[start_r][start_c] = True

    # Add all walls of the starting cell to the frontier
    frontier: list[tuple[int, int, int]] = []
    for direction, (dr, dc) in CHANGES.items():
        nr, nc = start_r + dr, start_c + dc
        if in_bounds(nr, nc) and (nr, nc) not in form_42:
            frontier.append((start_r, start_c, direction))

    # Process frontier walls
    while frontier:
        idx = rng.randint(0, len(frontier) - 1)
        r1, c1, direction = frontier.pop(idx)
        dr, dc = CHANGES[direction]
        r2, c2 = r1 + dr, c1 + dc

        if (in_bounds(r2, c2) and not visited[r2][c2]
                and (r2, c2) not in form_42):
            remove_wall(r1, c1, direction)
            visited[r2][c2] = True

            for new_direction, (ddr, ddc) in CHANGES.items():
                nr, nc = r2 + ddr, c2 + ddc
                if in_bounds(nr, nc) and not visited[nr][nc] and (nr, nc) not in form_42:
                    frontier.append((r2, c2, new_direction))

    # Optionally carve extra passages to create loops
    if not perfect:
        random_opens(grid, width, height, rng, form_42)

    # Return the final maze grid
    return grid


def random_opens(
    grid: list[list[int]],
    width: int,
    height: int,
    rng: random.Random,
    form_42: list[tuple[int, int]],
    carve_chance: float = 0.1
) -> None:
    """
    Open more random walls using a random generator,
    and reclose the 42 pattern after the random opens.
    """

    def enforce_42 (grid_: list[list[int]],
                    form_42_: list[tuple[int, int]],
                    width: int,
                    height: int) -> None:
        """Restore walls for the 42 pattern and seal neighbors facing into it."""

        # Step 1: fully wall every 42 cell
        for rw, coll in form_42_:
            grid_[rw][coll] |= 0xF

        # Step 2: close the wall on each neighbor that faces a 42 cell
        for row, coll in form_42_:
            neighbors = [
                (row - 1, coll, NORTH),  # neighbor to the north looks SOUTH into 42
                (row, coll + 1, EAST),  # neighbor to the east  looks WEST  into 42
                (row + 1, coll, SOUTH),  # neighbor to the south looks NORTH into 42
                (row, coll - 1, WEST),  # neighbor to the west  looks EAST  into 42
            ]
            for nr, nc, direction in neighbors:
                # bounds check: skip if neighbor is outside the grid
                if not (0 <= nr < height and 0 <= nc < width):
                    continue
                # skip if the neighbor is itself a 42 cell (already handled above)
                if (nr, nc) in form_42_:
                    continue
                # close the wall on the neighbor's side that faces the 42 cell
                grid_[nr][nc] |= WALL_BITS[OPPOSITE[direction]]

    for r in range(height):
        for c in range(width):
            # Try removing East wall (avoid right border)
            if c < width - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[EAST]:
                    grid[r][c] &= ~WALL_BITS[EAST]
                    grid[r][c + 1] &= ~WALL_BITS[WEST]

            # Try removing South wall (avoid bottom border)
            if r < height - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[SOUTH]:
                    grid[r][c] &= ~WALL_BITS[SOUTH]
                    grid[r + 1][c] &= ~WALL_BITS[NORTH]

    enforce_42(grid, form_42, width, height)