import sys
import os
from config import parse_config, ConfigError
from mazegen.utils import set_42_limits
from mazegen import MazeGenerator, bfs
from display import print_ascii_maze, ADDI, animate_path_walk


def organize_output_file(
    grid: list[list[int]],
    output_file: str,
    path: str,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> bool:
    """Write the maze and metadata to the output file.

    Args:
        grid: Generated maze grid.
        output_file: Path of the file where the maze will be written.
        path: Path from entry to exit encoded as a string.
        entry: Entry coordinate.
        exit_: Exit coordinate.

    Returns:
        True if the file was successfully written, False otherwise.
    """
    if os.path.exists(output_file):
        while True:
            print("1. to overwrite the content of the file")
            print("2. to cancel the process")
            try:
                choice = input(f"The file '{output_file}' already exists. "
                               f"Choose an option: ").strip()
            except BaseException:
                print("\nDetected Key Interruption Exiting gracefully...")
                return False
            if choice == '1':
                break
            elif choice == '2':
                print("Operation cancelled. The file was not modified.")
                return False
            else:
                print("Invalid input. Please enter 1, 2, or q.")

    content = ""

    for row in grid:
        for column in row:
            content += format(column, "X")
        content += "\n"

    try:
        with open(output_file, "w") as file:
            file.write(content)
            file.write(f"\n{entry[0]},{entry[1]}\n")
            file.write(f"{exit_[0]},{exit_[1]}\n")
            file.write(path)
            file.write("\n")

    except PermissionError:
        print(f"You don't have permission to write to {output_file}")
        return False
    except IsADirectoryError:
        print(f"{output_file} is a directory.")
        return False
    except OSError as e:
        print(f"An unexpected operating system error occurred "
              f"while writing to {output_file}: {e}")
        return False
    return True


def main() -> None:
    """Main entry point of the maze generator program."""
    # check if the arguments are right
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit()
        file_name = sys.argv[1]
        if not file_name.lower().endswith(".txt"):
            raise ConfigError("file_name must end with .txt")
        # get the configs from the config file
        config = parse_config(file_name)
        width = config.width
        height = config.height
        entry = config.entry
        exit_ = config.exit_
        perfect = config.perfect
        seed = config.seed
        output_file = config.output_file
        algo = config.algorithm if config.algorithm is not None else "PRIM"
        # assign the needed additional vars
        add_vars = ADDI(False, False, False, False)
        safe = set_42_limits(width, height)
        # call the MazeGenerator
        generator = MazeGenerator(width, height, seed, perfect, algo)
        # generate the maze and solve it
        maze = generator.generate()
        path_out_list = bfs(maze, entry, exit_)
        if path_out_list is None:
            print("no path found")
            sys.exit()
        path = generator.solve(entry, exit_)
        # write to output file
        if organize_output_file(maze, output_file, "".join(path_out_list),
                                entry, exit_) is False:
            sys.exit()
        # print the maze
        print_ascii_maze(maze, safe, add_vars, config, path)
        # the menu
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
                print("\nDetected Key Interruption Exiting gracefully...")
                sys.exit()

            if choice == "1":
                print("Maze re-generation started...")
                # give the seed NOne so it generate new random one
                generator.seed = None
                maze = generator.generate()
                path = generator.solve(entry, exit_)
                print_ascii_maze(maze, safe, add_vars, config, path)
            elif choice == "2":
                add_vars.path_check = not add_vars.path_check
                print_ascii_maze(maze, safe, add_vars, config, path)
            elif choice == "3":
                add_vars.animation_check = not add_vars.animation_check
                print_ascii_maze(maze, safe, add_vars, config, path)
            elif choice == "4":
                add_vars.path_check = False
                animate_path_walk(maze, safe, add_vars,
                                  config, path, delay=0.3)
            elif choice == "5":
                add_vars.color_check = True
                add_vars.color_42_check = True
                add_vars.animation_check = True
                print_ascii_maze(maze, safe, add_vars, config, path)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
    except BaseException as e:
        print(e)


if __name__ == "__main__":
    main()
