"""Configuration parsing and validation for maze generator."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Config:
    """Parsed configuration values."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit_: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algorithm: Optional[str] = "PRIM"


class ConfigError(Exception):
    """Configuration parsing or validation error."""


def set_42_limits(width: int, height: int) -> list[tuple[int, int]]:
    """Return coordinates forming the 42 pattern in the maze."""
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
    """Return True if entry or exit is in the 42 pattern."""
    form_42 = set_42_limits(width, height)
    return entry in form_42 or exit_ in form_42


def parse_bool(value: str, key_name: str) -> bool:
    """Parse a boolean string value."""
    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ConfigError(f"{key_name} must be True or False")


def parse_coord(value: str, key_name: str) -> Tuple[int, int]:
    """Parse a coordinate in the format x,y."""
    try:
        x, y = value.split(",", 1)
        return int(x.strip()), int(y.strip())
    except ValueError:
        raise ConfigError(f"{key_name} must be in format x,y")


def parse_config(file_name: str) -> Config:
    """Parse the config file and return a Config object."""
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
