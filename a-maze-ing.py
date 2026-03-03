import sys
import random
from dataclasses import dataclass
from config import parse_config, ConfigError, set_42_limits
from algorithms.prim import generate_maze
from display.terminal import print_ascii_maze, additional
from algorithms.bfs import bfs


def path_to_cells(start: tuple[int, int],solution: list[str]
) -> list[tuple[int, int]]:
    """
    Convert a start position and list of direction letters to a list of cells.

    Args:
        start:      (row, col) starting cell.
        solution: List of 'N', 'E', 'S', 'W' moves.

    Returns:
        Ordered list of (row, col) cells including start and end.
    """
    delta = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    cells: list[tuple[int, int]] = [start]
    r, c = start
    for d in solution:
        dr, dc = delta[d]
        r, c = r + dr, c + dc
        cells.append((r, c))
    return cells


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit(1)
        file_name = sys.argv[1]
        if not file_name.lower().endswith(".txt"):
            raise ConfigError("file_name must end with .txt")
        config = parse_config(file_name)
        WIDTH = config.width
        HEIGHT = config.height
        ENTRY = config.entry
        EXIT = config.exit_
        PERFECT = config.perfect
        SEED = config.seed
        output_file = config.output_file
        add_vars = additional(False, False, False, False)
        maze = generate_maze(WIDTH, HEIGHT, SEED, PERFECT)
        safe = set_42_limits(WIDTH, HEIGHT)
        solution = bfs(maze, ENTRY, EXIT)
        path = path_to_cells(ENTRY, solution)
        print_ascii_maze(maze, safe, add_vars, path)
        while True:
            print("\n=== Main Menu ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. animate the maze")
            print("4. animate path")
            print("5. Change maze color")
            print("6. Quit")

            try:
                choice = input("Enter your choice (1-3): ").strip()
            except BaseException :
                print("\nDetected Key Enterruption Exiting gracefully...")
                exit(0)

            if choice == "1":
                SEED = random.randrange(2**32)
                print("Maze re-generation started...")
                maze = generate_maze(WIDTH, HEIGHT, SEED, PERFECT)
                solution = bfs(maze, ENTRY, EXIT)
                path = path_to_cells(ENTRY, solution)
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "2":
                add_vars.path_check = not add_vars.path_check
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "3":
                add_vars.animation_check = not add_vars.animation_check
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "4":
                add_vars.color_check = True
                add_vars.color_42_check = True
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "5":
                print("Goodbye!") # let me do this.
                break
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        print(e)