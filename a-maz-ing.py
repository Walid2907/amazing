import sys
import config


def write_to_file(output: str) -> None:
    """
    Write the maze output to the configured output file.

    Args:
        output (str): The maze data to write.

    Note:
        Exits the program with code 1 if the file cannot be written.
    """
    try:
        with open(output_path, 'w') as file:
            file.write(output)
    except OSError as e:
        print(f"Error: '{output_path}' {e.strerror}")
        exit(1)

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <config_file>")
    sys.exit(1)
try:
    config_file = sys.argv[1]
    options = config.parse_config(config_file)
    width = options.width
    height = options.height
    entry = options.entry
    exit_ = options.ex_it
    output_path = options.output_file
    perfect = options.perfect
    seed = options.seed
except Exception as e:
    print("Error:", e)
    exit(1)
