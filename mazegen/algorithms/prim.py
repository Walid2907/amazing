"""
Prim's algorithm maze generator used in the A-Maze-ing project.

This module generates a maze using a randomized version of Prim's
algorithm and optionally introduces loops when the maze is not
required to be perfect.
"""

import random
from typing import Optional
from ..utils import set_42_limits

# --- Direction constants ---
NORTH = 0  # bit 0 → value 1
EAST = 1  # bit 1 → value 2
SOUTH = 2  # bit 2 → value 4
WEST = 3  # bit 3 → value 8

WALL_BITS = {NORTH: 1, EAST: 2, SOUTH: 4, WEST: 8}

# Opposite direction
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

# Row/column changes for each direction
CHANGES = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}


def prim(
    width: int,
    height: int,
    seed: Optional[int] = None,
    perfect: bool = True,
) -> list[list[int]]:
    """
    Generate a maze using Prim's algorithm.

    The algorithm starts with a random cell, then repeatedly removes
    walls between visited and unvisited cells until all reachable
    cells are connected.

    Args:
        width: Maze width.
        height: Maze height.
        seed: Optional random seed for deterministic generation.
        perfect: If True, generate a perfect maze (no loops).

    Returns:
        A 2D grid representing the maze. Each cell contains bit flags
        describing which walls remain.
    """
    form_42 = set_42_limits(width, height)
    rng = random.Random(seed)

    # Start: every cell fully walled (0xF = all 4 walls closed)
    grid: list[list[int]] = [[0xF] * width for _ in range(height)]
    visited: list[list[bool]] = [[False] * width for _ in range(height)]

    def in_bounds(r: int, c: int) -> bool:
        """
        Args:
            r: row coordinate
            c: coll coordinate
        Return True if the cell (r, c) is inside the maze grid.
        """
        return 0 <= r < height and 0 <= c < width

    def remove_wall(r1: int, c1: int, direction: int) -> None:
        """
        Remove the wall between a cell and its neighbor.

        Args:
            r1: Row of the source cell.
            c1: Column of the source cell.
            direction: Direction of the neighbor cell.
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
                if (in_bounds(nr, nc) and not visited[nr][nc]
                        and (nr, nc) not in form_42):
                    frontier.append((r2, c2, new_direction))
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
    Randomly remove additional walls to create loops.

    After random carving, the function restores the "42" pattern
    to ensure it remains completely sealed.

    Args:
        grid: Maze grid.
        width: Maze width.
        height: Maze height.
        rng: Random generator instance.
        form_42: Coordinates representing the 42 pattern.
        carve_chance: Probability of removing a wall.
    """

    def enforce_42(grid_: list[list[int]],
                   form_42_: list[tuple[int, int]],
                   width: int, height: int) -> None:
        """
        Ensures that the pattern cells remain sealed and
        neighboring cells cannot open passages into it.
        Restore the walls of the 42 pattern if carved by accedents
        Args:
            grid_ : the grid (Generated Maze)
            form_42_ : The 42 pattern cells coordinates
            width_ : Width of the maze
            height_: height of the maze

        """
        for rw, coll in form_42_:
            grid_[rw][coll] |= 0xF

        for row, coll in form_42_:
            neighbors = [
                (row - 1, coll, NORTH),
                (row, coll + 1, EAST),
                (row + 1, coll, SOUTH),
                (row, coll - 1, WEST),
            ]
            for nr, nc, direction in neighbors:
                if not (0 <= nr < height and 0 <= nc < width):
                    continue
                if (nr, nc) in form_42_:
                    continue
                grid_[nr][nc] |= WALL_BITS[OPPOSITE[direction]]

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
