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
This repository includes `pyproject.toml` and the `mazegen` package so that a wheel/sdist can be built using standard Python b*This project has been created as part of the 42 curriculum by wkerdad, achahi.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator and solver. Given a configuration file, it generates a maze (perfect or imperfect), writes it to an output file using a hexadecimal wall-encoding scheme, and displays it interactively in the terminal.

The project is split into two main parts:
- **`mazegen`** — a reusable Python package that handles maze generation and solving.
- **`a_maze_ing.py`** — the entry point that ties together config parsing, maze generation, solving, and display.

### Config Parsing

The program opens `config.txt` as its first step. The parser skips any line beginning with `#` (comments), then reads each remaining line expecting the format `KEY=VALUE`. All mandatory and optional keys are collected and returned as a dictionary. If a key name is unrecognized, a value is malformed, or a required key is missing, the parser raises a custom `ConfigError` exception with a descriptive message.

### Maze Generation — Prim's Algorithm

The maze starts as a fully closed grid. Each cell is represented by a single hexadecimal integer (`0xF` = 15), where each bit encodes one wall:

| Direction | Bit | Delta (row, col) |
|-----------|-----|-----------------|
| North     | `0001` | `(-1,  0)` |
| East      | `0010` | `( 0, +1)` |
| South     | `0100` | `(+1,  0)` |
| West      | `1000` | `( 0, -1)` |

The algorithm picks a random starting cell, adds its four neighboring walls to a *frontier* list, and marks the cell as visited. At each step it picks a random frontier entry, verifies that the target cell is in-bounds, unvisited, and not part of the embedded "42" pattern, then carves through the shared wall (clearing the corresponding bit in both cells using bitwise masking). This continues until every cell has been visited and the frontier is empty, producing a **perfect maze** (exactly one path between any two cells). To generate an **imperfect maze**, the algorithm then randomly removes additional walls, creating multiple routes to the exit.

### Maze Generation — DFS Algorithm

As an alternative, the generator supports a randomized depth-first search. Starting from the entry cell, it builds a list of unvisited neighbors, shuffles them randomly, and recurses into each one. Before moving into a neighbor, it clears the wall bit in the current cell **and** the opposite wall bit in the neighbor cell — using a direction-to-opposite dictionary — so both sides of the passage are always consistent. Cells belonging to the "42" logo are added to the visited set by default so the pattern is preserved.

### BFS Path Solving

The solver uses a `deque`-based breadth-first search. It starts by pushing the entry cell onto the deque. At each step it pops the leftmost element (current cell + path string that led to it), checks each of the four directions by testing the corresponding wall bit, and — if the wall is open — pushes the neighboring cell along with the extended path string onto the deque. Each visited cell is recorded to avoid revisiting. This continues until the exit cell is dequeued, at which point the accumulated path string (a sequence of direction characters) is returned as the solution.

### Terminal Display

The display engine maps the maze onto a character buffer using two separate coordinate systems: one for **corners** (grid intersections) and one for **cells** (interior positions). For each corner it inspects the wall bits of all adjacent cells to decide whether to draw a horizontal bar, a vertical bar, or a blank. The buffer is filled in three passes: the top row of horizontal walls, the middle rows (alternating horizontal walls and vertical walls), and the bottom row. Color and display style can be toggled via boolean flags passed from the main entry point.

---

## Instructions

### Requirements

- Python >= 3.10

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

### Lint

```sh
make lint
# or
make lint-strict
```

---

## Configuration File Format

One `KEY=VALUE` per line. Lines starting with `#` are ignored.

**Mandatory keys:**

| Key | Type | Description |
|-----|------|-------------|
| `WIDTH` | `int` | Number of columns |
| `HEIGHT` | `int` | Number of rows |
| `ENTRY` | `x,y` | Entry cell coordinates |
| `EXIT` | `x,y` | Exit cell coordinates |
| `OUTPUT_FILE` | `filename.txt` | Path to write the generated maze |
| `PERFECT` | `True\|False` | Whether to generate a perfect maze |

**Optional keys:**

| Key | Type | Description |
|-----|------|-------------|
| `SEED` | `int` | Random seed for reproducibility |
| `ALGORITHM` | `PRIM\|DFS` | Generation algorithm (default: PRIM) |

**Example:**

```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=PRIM
```

---

## Maze Generation Algorithms

Two algorithms are implemented:

- **Prim's Algorithm** — starts from a random cell, grows the maze by repeatedly picking a random wall from a frontier list, and carves through it if the target cell is unvisited. Tends to produce mazes with many short dead-ends and a uniform texture.
- **DFS (Depth-First Search)** — starts from a random cell and recursively carves into random unvisited neighbors, backtracking when stuck. Tends to produce mazes with long winding corridors.

Both naturally produce **perfect mazes** (a spanning tree of all cells with no loops and no isolated regions), and both are reproducible by seeding Python's `random` module.

---

## Maze Constraints & Rules Enforced

- **Reproducibility** — passing `SEED` guarantees the same maze every run.
- **Wall coherence** — if a cell's east wall is closed, the western wall of its eastern neighbor is also closed (enforced via bitmasking on both cells simultaneously).
- **No large open areas** — the generator avoids any 3×3 fully open region.
- **"42" pattern** — when the maze is large enough, a visible "42" logo made of fully closed cells is embedded. If the maze is too small to fit the pattern, the program prints an informative error and generates without it.

---

## Reusable Code — `mazegen` Module

The `mazegen` package is fully self-contained and can be imported into any project:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True, algorithm="PRIM")
grid = gen.generate()          # returns the wall-encoded 2-D grid
path = gen.solve(entry, exit_) # returns the solution path string
```

| Symbol | Description |
|--------|-------------|
| `MazeGenerator(width, height, seed, perfect, algorithm)` | Constructor |
| `.generate()` | Generates and returns the hex-encoded wall grid |
| `.solve(entry, exit_)` | BFS solver; returns direction string from entry to exit |

---

## Resources

- [Randomized Prim's Algorithm — Maze generation (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm)
- [Depth-First Search maze generation (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Python `collections.deque` (BFS)](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python `typing` module docs](https://docs.python.org/3/library/typing.html)
- [mypy — optional static typing for Python](https://mypy.readthedocs.io/)
- [flake8 — Python style guide enforcement](https://flake8.pycqa.org/)

---

## Team and Project Management

| Wkerdad                             | Achahi                                 |
| ----------------------------------- | -------------------------------------- |
| Config Parsing                      | Maze Generation Using Prim's Algorithm |
| Maze Generation Using DFS algorithm | Path Solving using BFS algorithm       |
| Maze Terminal Print                 | Makefile And final organization        |
uild tooling.

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