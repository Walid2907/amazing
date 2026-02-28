
# --- Direction constants ---

NORTH = 0  # bit 0 → value 1
EAST  = 1  # bit 1 → value 2
SOUTH = 2  # bit 2 → value 4
WEST  = 3  # bit 3 → value 8

WALL_BITS = {NORTH: 1, EAST: 2, SOUTH: 4, WEST: 8}

def print_ascii_maze(grid: list[list[int]]) -> None:
    """
    Print a simple ASCII representation of the maze to the terminal.
    Uses '+', '-', '|' and spaces.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    for r in range(height):
        # Top edge of row
        top = ""
        for c in range(width):
            top += "+"
            top += "--" if (grid[r][c] & WALL_BITS[NORTH]) else "  "
        top += "+"
        print(top)

        # Middle of row
        mid = ""
        for c in range(width):
            mid += "|" if (grid[r][c] & WALL_BITS[WEST]) else " "
            mid += "  "
        mid += "|" if (grid[r][width - 1] & WALL_BITS[EAST]) else " "
        print(mid)

    # Bottom edge
    bottom = ""
    for c in range(width):
        bottom += "+"
        bottom += "--" if (grid[height - 1][c] & WALL_BITS[SOUTH]) else "  "
    bottom += "+"
    print(bottom)