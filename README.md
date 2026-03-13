*This project has been created as part of the 42 curriculum by Walid2907, wkerdad, achahi.*

## Description
**A-Maze-ing** is a Python maze generator. It reads a configuration file, generates a maze (perfect or not), writes it to a file using a hexadecimal wall representation, and provides a terminal visual representation with interactive controls (regenerate, show/hide shortest path, change colors, animations).

## Instructions

### Requirements
- Python **3.10+**
- Dependencies are listed in `requirements.txt`

### Install
```sh
make install
```

### Run
```sh
python3 a_maze_ing.py config.txt
# or
make run
```

### Debug
```sh
make debug
```

### Clean
```sh
make clean
```

### Lint
```sh
make lint
# optional
make lint-strict
```

## Configuration file format
The configuration file is plain text and must contain one `KEY=VALUE` pair per line.
Lines starting with `#` are comments and are ignored.

### Mandatory keys
- `WIDTH` (maze width in number of cells)
- `HEIGHT` (maze height in number of cells)
- `ENTRY` (x,y)
- `EXIT` (x,y)
- `OUTPUT_FILE` (output filename)
- `PERFECT` (`True` or `False`)

### Optional keys implemented in this repo
- `SEED` (integer seed for reproducibility)
- `ALGORITHM` (`PRIM` or `DFS`)

### Example (default file in repo)
See `config.txt` at the root of the repository.

## Maze generation algorithm
This repository supports 2 algorithms (set using `ALGORITHM=` in the config file):

- **PRIM**: randomized Prim-style generation using a frontier of walls
- **DFS**: randomized depth-first search (recursive backtracker style, implemented with a stack)

### Why these algorithms
Both Prim and DFS naturally generate **perfect mazes** (spanning trees) when no extra random openings are carved:
- full connectivity (no isolated cells),
- consistent wall representation (neighbor walls match),
- and, in perfect mode, a unique path between entry and exit.

## Output file format
The maze is written to `OUTPUT_FILE` using **one hexadecimal digit per cell**.
Each digit encodes closed walls using 4 bits:

- bit 0 (1): North
- bit 1 (2): East
- bit 2 (4): South
- bit 3 (8): West

Cells are written **row by row**, one row per line, each line ending with `\n`.

After an empty line, the file contains 3 lines:
1) entry coordinates: `x,y`
2) exit coordinates: `x,y`
3) a shortest valid path using letters `N`, `E`, `S`, `W`

## Visual representation (terminal)
This repo implements a terminal renderer in `display/terminal.py`.

Displayed elements:
- walls (box drawing characters),
- entry cell (green),
- exit cell (red),
- optional shortest path overlay,
- optional color changes and animations.

### Interactions (menu in `a_maze_ing.py`)
At minimum, the program supports:
- Re-generate a new maze
- Show/Hide a valid shortest path
- Change maze wall colours

Extra interactions included:
- Animate maze rendering
- Animate path walk

## Code reusability requirements
Maze generation logic is reusable via the `mazegen` module:
- `mazegen/generator.py` provides the `MazeGenerator` class
- `mazegen/algorithms/` contains the algorithms and BFS solver

### Example usage
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True, algorithm="PRIM")
maze = gen.generate()
solution_cells = gen.solve((0, 0), (19, 14))
```

### Accessing generated structure
- `MazeGenerator.generate()` returns a `list[list[int]]` grid (hex-wall encoding per cell).
- `MazeGenerator.solve(entry, exit_)` returns a list of `(row, col)` cells representing a valid shortest path.

## Packaging
This repository includes `pyproject.toml` and the `mazegen` package so that a wheel/sdist can be built using standard Python build tooling.

## Resources
- Maze generation algorithms: randomized Prim, DFS backtracker
- Python typing: `typing` + `mypy`
- flake8 documentation for style checking

### How AI was used
AI was used as a productivity tool for:
- generating requirement checklists against the subject,
- identifying missing requirements (README, constraints),
- suggesting refactors and validation strategies.
All final code and explanations were reviewed and adapted by the team.

## Team and project management
### Roles
- wkerdad: (fill in)
- achahi: (fill in)

### Planning
- Initial plan: implement config parsing + generator + output writer + display
- Adjustments: add interactions, add second algorithm, improve error handling

### What worked well / what could be improved
- Worked well: deterministic generation with seed, modular organization (`mazegen`, `display`, config parser)
- Could be improved: more automated tests (pytest), stricter validation for extra maze constraints

### Tools used
- Git / GitHub
- flake8, mypy
- Python build tooling (`build`)