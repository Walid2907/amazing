import sys
import random
from config import parse_config, ConfigError, set_42_limits
from algorithms.prim import generate_maze
from display.terminal import print_ascii_maze, ADDI, animate_path_walk
from algorithms.bfs import bfs, path_to_cells


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit(1)
        file_name = sys.argv[1]
        if not file_name.lower().endswith(".txt"):
            raise ConfigError("file_name must end with .txt")
        # get main vars
        config = parse_config(file_name)
        WIDTH = config.width
        HEIGHT = config.height
        ENTRY = config.entry
        EXIT = config.exit_
        PERFECT = config.perfect
        SEED = config.seed
        output_file = config.output_file
        # assign additional vars
        add_vars = ADDI(False, False, False, False)
        maze = generate_maze(WIDTH, HEIGHT, SEED, PERFECT)
        safe = set_42_limits(WIDTH, HEIGHT)
        solution = bfs(maze, ENTRY, EXIT)
        # convert the solution from string to cords
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
                choice = input("Enter your choice (1-6): ").strip()
            except BaseException:
                print("\nDetected Key Enterruption Exiting gracefully...")
                exit(0)

            if choice == "1":
                print("Maze re-generation started...")
                maze = generate_maze(WIDTH, HEIGHT, None, PERFECT)  # I changed the random seed to just non because prim handle non seed
                solution = bfs(maze, ENTRY, EXIT)
                path = path_to_cells(ENTRY, solution)   # why you removed the generator of the output file idiot
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "2":
                add_vars.path_check = not add_vars.path_check
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "3":
                add_vars.animation_check = not add_vars.animation_check
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "4":
                add_vars.path_check = False
                animate_path_walk(maze, safe, add_vars, path, delay=0.1)
            elif choice == "5":
                add_vars.color_check = True
                add_vars.color_42_check = True
                print_ascii_maze(maze, safe, add_vars, path)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        print(e)
