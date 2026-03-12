from typing import Optional
from dataclasses import dataclass
import random
import os
import time
from config import Config


# an additional data class
# to hold more vars needed
@dataclass
class ADDI:
    path_check: bool
    color_check: bool
    color_42_check: bool
    animation_check: bool


# each bit position
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
# dict of each direction actual bit value
WALL_BITS = {NORTH: 1, EAST: 2, SOUTH: 4, WEST: 8}

# colors codes and a list
# for the color random
RESET_CODE = "\033[0m"
RED_CODE = "\033[91m"
GREEN_CODE = "\033[32m"
BLUE_CODE = "\033[34m"
YELLOW_CODE = "\033[33m"
WHITE_CODE = "\033[37m"
MAGENTA_CODE = "\033[35m"
CYAN_CODE = "\033[36m"

colors = [RED_CODE, GREEN_CODE, BLUE_CODE,
          YELLOW_CODE, WHITE_CODE, MAGENTA_CODE, CYAN_CODE]


def possible_corners(n: bool, e: bool, s: bool, w: bool) -> str:
    # return the right corner from the possible combination of corners
    if n and e and s and w:
        return "╋"
    if n and e and w:
        return "┻"
    if s and e and w:
        return "┳"
    if s and n and w:
        return "┫"
    if s and n and e:
        return "┣"
    if w and s:
        return "┓"
    if s and e:
        return "┏"
    if e and n:
        return "┗"
    if n and w:
        return "┛"
    if n or s:
        return "┃"
    if w or e:
        return "━"
    return " "


def hor_wall(grid: list[list[int]], r: int, c: int, direction: int) -> bool:
    # function to check the horizontal walls north and south
    height = len(grid)
    width = len(grid[0])
    if r < 0 or r >= height or c < 0 or c >= width:
        # Check opposite wall of adjacent cell
        # if out of bounds
        if r == height and direction == NORTH:
            return bool(grid[r-1][c] & WALL_BITS[SOUTH])
        if r == -1 and direction == SOUTH:
            return bool(grid[0][c] & WALL_BITS[NORTH])
        return False
    return bool(grid[r][c] & WALL_BITS[direction])


def vert_wall(grid: list[list[int]], r: int,
              c: int, direction: int) -> bool:
    """Helper to safely check for a vertical wall."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    if r < 0 or r >= height or c < 0 or c >= width:
        if c == width and direction == WEST:
            return bool(grid[r][c-1] & WALL_BITS[EAST])
        if c == -1 and direction == EAST:
            return bool(grid[r][0] & WALL_BITS[WEST])
        return False
    return bool(grid[r][c] & WALL_BITS[direction])


def get_corner(grid: list[list[int]], r: int, c: int) -> str:
    """
    Determine the four wall and creat the corner to get the right
    corner from the possibilities
    """
    n = vert_wall(grid, r - 1, c, WEST)  # vertical wall above
    s = vert_wall(grid, r, c, WEST)      # vertical wall below
    e = hor_wall(grid, r, c, NORTH)     # horizontal wall right
    w = hor_wall(grid, r, c - 1, NORTH)  # horizontal wall left
    return possible_corners(n, e, s, w)


def get_bottom_corner(grid: list[list[int]], r: int, c: int) -> str:
    """Corner for the very bottom edge of the grid."""
    n = vert_wall(grid, r, c, WEST)      # vertical wall above
    s = False                            # no wall below bottom edge
    e = hor_wall(grid, r, c, SOUTH)     # horizontal wall right
    w = hor_wall(grid, r, c - 1, SOUTH)  # horizontal wall left
    return possible_corners(n, e, s, w)


def print_ascii_maze(grid: list[list[int]], safe: list[tuple[int, int]],
                     add_vars: ADDI,
                     config: Config,
                     path: Optional[list[tuple[int, int]]] = None) -> None:
    """
    Print an ASCII representation of the maze to the terminal.
    """
    height = config.height
    width = config.width
    path_set = set(path) if path else set()

    color = random.choice(colors) if add_vars.color_check else WHITE_CODE
    color_42 = random.choice(colors) if add_vars.color_42_check else WHITE_CODE
    os.system('cls' if os.name == 'nt' else 'clear')
    try:

        for r in range(height):
            # Top edge of row
            top = ""
            for c in range(width):
                top += get_corner(grid, r, c)
                top += "━━" if hor_wall(grid, r, c, NORTH) else "  "

            # Top-rightmost corner of the row
            n = vert_wall(grid, r - 1, width - 1, EAST)
            s = vert_wall(grid, r, width - 1, EAST)
            w = hor_wall(grid, r, width - 1, NORTH)
            top += possible_corners(n, False, s, w)

            print(color + top)
            if add_vars.animation_check:
                time.sleep(0.05)
            # Middle of row
            mid = ""
            for c in range(width):
                mid += "┃" if vert_wall(grid, r, c, WEST) else " "
                if (r, c) in path_set and add_vars.path_check:
                    mid += "🕷️ "       # path marker, 2 chars wide
                elif (c, r) == config.entry:
                    mid += GREEN_CODE + "██" + color
                elif (c, r) == config.exit_:
                    mid += RED_CODE + "██" + color
                elif (r, c) in safe:
                    mid += color_42 + "██" + color  # safe zone, 2 chars wide
                else:
                    mid += "  "       # empty cell, 2 chars wide

            mid += "┃" if vert_wall(grid, r, width - 1, EAST) else " "
            print(mid)
            if add_vars.animation_check:
                time.sleep(0.05)
        # Bottom edge of the maze
        bottom = ""
        for c in range(width):
            bottom += get_bottom_corner(grid, height - 1, c)
            bottom += "━━" if hor_wall(grid, height - 1, c, SOUTH) else "  "
        # Bottom-rightmost corner
        n = vert_wall(grid, height - 1, width - 1, EAST)
        w = hor_wall(grid, height - 1, width - 1, SOUTH)
        bottom += possible_corners(n, False, False, w)
        print(bottom + RESET_CODE)
    except KeyboardInterrupt:
        print(RESET_CODE)  # Reset the colors
        print("\nAnimation interrupted.")


def animate_path_walk(
    grid: list[list[int]],
    safe: list[tuple[int, int]],
    add_vars: ADDI,
    conf: Config,
    path: list[tuple[int, int]],
    delay: float = 0.1
) -> None:
    """
    Animate a spider walking the path.
    the spider will moves cell by cell,
    leaving 🕸️ on visited cells.
    !! remembre takes 2 space
    """
    height = len(grid)
    total_lines = height * 2 + 1

    # Draw the initial maze (no path)
    add_vars.path_check = False
    print_ascii_maze(grid, safe, add_vars, conf, [])
    # ANSI helpers
    # special characters that help move the cursor in the terminal
    # without printing anything

    def move_up(n: int) -> None:
        # move the cursor up n lines
        print(f"\033[{n}A", end="")

    def move_to_col(n: int) -> None:
        print(f"\033[{n}G", end="")

    def overwrite_cell(r: int, c: int, symbol: str,
                       color: str = WHITE_CODE) -> None:
        """
        Jump to the exact terminal position of cell (r,c)
        and overwrite its content.
        Each cell occupies columns: corner(1) + 2 chars per cell.
        The 'middle' line of row r is at line offset:
        r*2 + 1 (0-indexed from maze top).
        """
        # Move cursor up from current bottom position to the cell's mid-line
        line_from_bottom = total_lines - (r * 2 + 1)
        move_up(line_from_bottom)

        # Column: each cell is 3 chars wide (1 wall + 2 content),
        # 1-indexed for ANSI
        col_pos = c * 3 + 2  # +1 for ANSI 1-index, +1 to skip the wall char
        move_to_col(col_pos)

        print(color + symbol + RESET_CODE, end="", flush=True)

        # Move back down to bottom
        print(f"\033[{line_from_bottom}B", end="", flush=True)
        move_to_col(1)

    footprint = "🕸️ "
    spider = "🕷️ "
    try:
        for i, cell in enumerate(path):
            if i > 0:
                overwrite_cell(path[i - 1][0],
                               path[i - 1][1], footprint, CYAN_CODE)
            overwrite_cell(cell[0], cell[1], spider)
            time.sleep(delay)
    except KeyboardInterrupt:
        print(RESET_CODE)  # Reset the colors
        print("\nAnimation interrupted.")
