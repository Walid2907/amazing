import sys
from config import parse_config, ConfigError, set_42_limits
from mazegen import MazeGenerator
from display import print_ascii_maze, ADDI, animate_path_walk


def main() -> None:
    # check if the arguments are right
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit(1)
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
        # !! don't forget the output file brother
        output_file = config.output_file
        algo = config.algorithm
        # assign the needed additional vars
        add_vars = ADDI(False, False, False, False)
        safe = set_42_limits(width, height)
        # call the MazeGenerator
        generator = MazeGenerator(width, height, seed, perfect, algo)
        # generate the maze and solve it
        maze = generator.generate()
        path = generator.solve(entry, exit_)
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
                sys.exit(0)

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
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
