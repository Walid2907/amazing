"""Configuration parsing and validation for maze generator."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Config:
    """
    Immutable configuration object for the maze generator.

    Attributes:
        width: Width of the maze grid.
        height: Height of the maze grid.
        entry: Entry coordinate (x, y) of the maze.
        exit_: Exit coordinate (x, y) of the maze.
        output_file: Path of the file where the maze will be saved.
        perfect: Whether the maze should be perfect (no loops).
        seed: Optional seed used for deterministic maze generation.
        algorithm: Maze generation algorithm to use.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit_: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algorithm: Optional[str] = "PRIM"


class ConfigError(Exception):
    """Exception raised when configuration parsing or validation fails."""


def set_42_limits(width: int, height: int) -> list[tuple[int, int]]:
    """
    Compute the coordinates that form the '42' pattern inside the maze.

    The pattern is centered relative to the maze dimensions.

    Args:
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        A list of coordinate tuples representing the '42' pattern cells.
    """
    center_r = height // 2
    center_c = width // 2

    coords_fc: list[tuple[int, int]] = [
        (0, -1), (0, -2), (0, -3), (-1, -3),
        (-2, -3), (1, -1), (2, -1), (0, 1),
        (1, 1), (2, 1), (2, 2), (2, 3),
        (0, 2), (0, 3), (-1, 3), (-2, 3),
        (-2, 2), (-2, 1),
    ]

    form_42: list[tuple[int, int]] = []
    for dr, dc in coords_fc:
        target_r = center_r + dr
        target_c = center_c + dc
        form_42.append((target_r, target_c))

    return form_42


def entry_exit_in_42(
    entry: tuple[int, int],
    exit_: tuple[int, int],
    width: int,
    height: int,
) -> bool:
    """
    Check whether the entry or exit position lies within the '42' pattern.

    Args:
        entry: Entry coordinate (x, y).
        exit_: Exit coordinate (x, y).
        width: Maze width.
        height: Maze height.

    Returns:
        True if either the entry or exit coordinate is inside the
        '42' pattern, otherwise False.
    """
    form_42 = set_42_limits(width, height)
    return entry in form_42 or exit_ in form_42


def parse_bool(value: str, key_name: str) -> bool:
    """
    Convert a string value to a boolean.

    Accepted values are "true" or "false" (case-insensitive).

    Args:
        value: The string representation of the boolean.
        key_name: Name of the configuration key for error reporting.

    Returns:
        The parsed boolean value.

    Raises:
        ConfigError: If the value is not a valid boolean string.
    """
    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ConfigError(f"{key_name} must be True or False")


def parse_coord(value: str, key_name: str) -> Tuple[int, int]:
    """
    Parse a coordinate string in the format "x,y".

    Args:
        value: Coordinate string.
        key_name: Configuration key name used for error reporting.

    Returns:
        A tuple containing two integers (x, y).

    Raises:
        ConfigError: If the value cannot be parsed as a valid coordinate.
    """
    try:
        x, y = value.split(",", 1)
        return int(x.strip()), int(y.strip())
    except ValueError:
        raise ConfigError(f"{key_name} must be in format x,y")


def parse_config(file_name: str) -> Config:
    """
    Parse and validate a configuration file for the maze generator.

    The configuration file must contain key-value pairs using the format:
        KEY=value

    Lines beginning with '#' and empty lines are ignored.

    Args:
        file_name: Path to the configuration file.

    Returns:
        A validated Config object.

    Raises:
        ConfigError: If the file cannot be read or if any configuration
        value is missing or invalid.
    """
    confs: dict[str, str] = {}
    required = {
        "width",
        "height",
        "entry",
        "exit",
        "output_file",
        "perfect",
    }

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(
                        f"Line {line_num}: missing '='")
                key, value = line.split("=", 1)
                confs[key.lower().strip()] = value.strip()

    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {file_name}")
    except PermissionError:
        raise ConfigError(f"No permission to open file: {file_name}")
    except OSError:
        raise ConfigError(f"Failed to read config file: {file_name}")

    missing = required - confs.keys()
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ConfigError(f"Missing required keys: {missing_str}")

    try:
        width = int(confs["width"])
        height = int(confs["height"])
    except ValueError:
        raise ConfigError("WIDTH and HEIGHT must be integers")

    if width < 9:
        raise ConfigError("WIDTH must be >= 9")
    if height < 7:
        raise ConfigError("HEIGHT must be >= 7")

    entry = parse_coord(confs["entry"], "ENTRY")
    exit_ = parse_coord(confs["exit"], "EXIT")

    if entry == exit_:
        raise ConfigError(
            "ENTRY and EXIT must be different"
        )

    if entry_exit_in_42(entry, exit_, width, height):
        raise ConfigError("Entry/Exit cannot be inside the '42' pattern")

    for name, (x, y) in {"ENTRY": entry, "EXIT": exit_, }.items():
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} out of bounds")

    perfect = parse_bool(confs["perfect"], "PERFECT")

    output_file = confs["output_file"]
    if not output_file:
        raise ConfigError("OUTPUT_FILE must be non-empty")
    if not output_file.lower().endswith(".txt"):
        raise ConfigError("OUTPUT_FILE must end with .txt")

    seed = None
    if "seed" in confs:
        try:
            seed = int(confs["seed"])
        except ValueError:
            raise ConfigError("SEED must be an integer")

    algorithm = "PRIM"
    if "algorithm" in confs:
        algos = ["PRIM", "DFS"]
        algorithm = confs["algorithm"].upper()
        if algorithm not in algos:
            raise ConfigError("algorithme choice is not valid")
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit_=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algorithm=algorithm
    )
