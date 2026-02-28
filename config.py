"""Configuration parsing and validation for maze generator."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Config:
    """Parsed configuration values."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


class ConfigError(Exception):
    """Configuration parsing or validation error."""


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
    required = {"width", "height", "entry", "exit", "output_file", "perfect"}

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Line {line_num}: missing '='")
                cleanline, trash = line.split(" ", 1)
                key, value = cleanline.split("=", 1)
                confs[key.lower().strip()] = value.strip()
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {file_name}")
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

    if width <= 1 or height <= 1:
        raise ConfigError("WIDTH and HEIGHT must be > 1")

    entry = parse_coord(confs["entry"], "ENTRY")
    ex_it = parse_coord(confs["exit"], "EXIT")

    if entry == ex_it:
        raise ConfigError("ENTRY and EXIT must be different")

    perfect = parse_bool(confs["perfect"], "PERFECT")

    output_file = confs["output_file"]
    if not output_file:
        raise ConfigError("OUTPUT_FILE must be non-empty")

    seed: Optional[int] = None
    if "seed" in confs:
        try:
            seed = int(confs["seed"])
        except ValueError:
            raise ConfigError("SEED must be an integer")

    for name, (x, y) in {"ENTRY": entry, "EXIT": ex_it}.items():
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} out of bounds")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=ex_it,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
