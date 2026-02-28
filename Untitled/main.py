"""
Prim's Algorithm - Maze Generator for A-Maze-ing (42 project)
==============================================================
"""
from tools import print_ascii_maze
import random
from typing import Optional

# --- Direction constants ---
NORTH = 0  # bit 0 → value 1
EAST  = 1  # bit 1 → value 2
SOUTH = 2  # bit 2 → value 4
WEST  = 3  # bit 3 → value 8

WALL_BITS = {NORTH: 1, EAST: 2, SOUTH: 4, WEST: 8}

# Opposite direction
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

# derived for each direction
CHANGES = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}





# Set 42 limits
def set_42_limits(width, height):
    center_r = int(height / 2)
    center_c = int(width / 2)

    # The cells that can build together a 42 pattern
    coords_fc : list[tuple[int, int]] = [
        (0, -1), (0, -2), (0, -3), (-1, -3),
        (-2, -3), (1, -1), (2, -1), (0, 1),
        (1, 1), (2, 1), (2, 2),(2, 3), (0, 2),
        (0, 3), (-1, 3), (-2, 3), (-2, 2), (-2, 1)
    ]

    form_42:list[tuple[int, int]] = []

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
    generate the maze using prim's algorithm
    picking one cell add there walls excluding the borders
    pick random wall and remove it and go the next cell
    and do the same process again and until no wall still in frontiers
    """
    form_42 = set_42_limits(width, height)
    rng = random.Random(seed)

    # Start: every cell fully walled (0xF = all 4 walls closed)
    grid: list[list[int]] = [[0xF] * width for _ in range(height)]

    # visited[r][c] = True once the cell is part of the maze
    visited: list[list[bool]] = [[False] * width for _ in range(height)]

    def in_bounds(r: int, c: int) -> bool:
        """Return True if (r, c) is inside the grid."""
        return 0 <= r < height and 0 <= c < width

    def remove_wall(r1: int, c1: int, direction: int) -> None:
        """
        Remove the wall between cell (r1, c1) and its neighbour in `direction`.
        Updates both cells to keep wall data coherent (subject rule).
        """
        dr, dc = CHANGES[direction]    #Delta direction used to navigate in the maze [go to obsidian l10]
        r2, c2 = r1 + dr, c1 + dc    # Define the opposite cell coordinates

        # Open wall on cell 1 side
        grid[r1][c1] &= ~WALL_BITS[direction]
        # Open wall on cell 2 side (opposite direction)
        grid[r2][c2] &= ~WALL_BITS[OPPOSITE[direction]]

    # --- Prim's Algorithm ---
    # 1. Pick a random starting cell
    start_r = rng.randint(0, height - 1)
    start_c = rng.randint(0, width - 1)
    visited[start_r][start_c] = True

    # 2. Add all walls of the starting cell to the frontier
    # frontier = list of (from_row, from_col, direction_to_unvisited_neighbour)
    frontier: list[tuple[int, int, int]] = []
    for direction, (dr, dc) in CHANGES.items():
        nr, nc = start_r + dr, start_c + dc
        if in_bounds(nr, nc):
            frontier.append((start_r, start_c, direction))

    # 3. While there are walls in the frontier and remove it
    while frontier:
        # Pick a random wall from the frontier
        idx = rng.randint(0, len(frontier) - 1)
        r1, c1, direction = frontier[idx]
        frontier.pop(idx)

        #Define the opposite cell
        dr, dc = CHANGES[direction]
        r2, c2 = r1 + dr, c1 + dc

        # If the cell on the other side is NOT yet visited →  remove a wall
        # and add it to visited list
        if in_bounds(r2, c2) and not visited[r2][c2] and (r2, c2) not in form_42 :
            remove_wall(r1, c1, direction)
            visited[r2][c2] = True

            # Add new frontier walls from the newly visited cell
            # just if the opposite cell not visited and not out of bounds
            for new_direction, (ddr, ddc) in CHANGES.items():
                nr, nc = r2 + ddr, c2 + ddc
                if in_bounds(nr, nc) and not visited[nr][nc]:
                    frontier.append((r2, c2, new_direction))

    # If perfect=False, we optionally carve extra passages to create loops
    if not perfect:
        random_opens(grid, width, height, rng, form_42)

    # Enforce external border walls (subject rule: borders must always be closed)
    # _enforce_borders(grid, width, height)

    return grid







def random_opens(
    grid: list[list[int]],
    width: int,
    height: int,
    rng: random.Random,
    form_42,
    carve_chance: float = 0.3
) -> None:
    """
    Open more random wall using a random generator, and reclose the
    42 pattern after the random opens
    """
    def enforce_42 (grid, form_42):

        for rw, coll in form_42:
            grid[rw][coll] |= 15

        for row, coll in form_42:
            north_r, north_c = row-1, coll
            east_r, east_c = row, coll + 1
            south_r, south_c = row + 1 , coll
            west_r, west_c = row , coll - 1
            neighbors = [
                (north_r, north_c, NORTH),
                (east_r, east_c, EAST),
                (south_r, south_c, SOUTH),
                (west_r, west_c, WEST),
            ]
            for row, coll, direction in neighbors:
                grid[row][coll] |= WALL_BITS[OPPOSITE[direction]]


    for r in range(height):  #loop over height and width to visite all cells
        for c in range(width):
            # Try removing East wall (avoid right border)
            if c < width - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[EAST]:  # wall exists
                    grid[r][c] &= ~WALL_BITS[EAST]
                    grid[r][c + 1] &= ~WALL_BITS[WEST]
            # Try removing South wall (avoid bottom border)
            if r < height - 1 and rng.random() < carve_chance:
                if grid[r][c] & WALL_BITS[SOUTH]:  # wall exists
                    grid[r][c] &= ~WALL_BITS[SOUTH]
                    grid[r + 1][c] &= ~WALL_BITS[NORTH]

    enforce_42(grid, form_42)

def maze_to_hex_string(grid: list[list[int]]) -> str:
    """
    Convert the maze grid to the output file format.
    One hex digit per cell, one row per line.

    Returns:
        A string where each line is one row of the maze (uppercase hex digits).
    """
    lines = []
    for row in grid:
        lines.append("".join(format(cell, 'X') for cell in row))
    return "\n".join(lines)


def create_entry_exit(grid, height , width):
    grid[0][0] &= ~1
    grid[height-1][width-1] &= ~4


if __name__ == "__main__":
    WIDTH, HEIGHT, SEED = 32, 14, 23

    if WIDTH < 9 or HEIGHT < 7:
        print("The width or the height not enough")
        exit(0)
    print(f"Generating {WIDTH}x{HEIGHT} perfect maze (seed={SEED})...\n")
    maze = generate_maze(WIDTH, HEIGHT, seed=SEED, perfect=True)
    create_entry_exit(maze, HEIGHT, WIDTH)

    print("=== ASCII view ===")
    print_ascii_maze(maze)

    print("\n=== Hex output (one row per line) ===")
    print(maze_to_hex_string(maze))

    print("\n=== Cell values (for understanding) ===")
    for row in maze:
        print(" ".join(f"0x{v:X}" for v in row))

