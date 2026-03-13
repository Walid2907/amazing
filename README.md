*This project has been created as part of the 42 curriculum by wkerdad, achahi.*

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

maze = MazeGenerator(width=20, height=15, seed=42, perfect=True, algorithm="PRIM")
grid = maze.generate()          # returns the wall encoded 2D grid
path = mzae.solve(entry, exit_) # returns the solution path string
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
| Maze Generation Using DFS algorithm | Maze Generation Using Prim's Algorithm |
| Maze Terminal Print                 | Path Solving using BFS algorithm       |
| Config Parsing                      | Makefile And final organization        |

### Planning and Evolution
---
Initial Plan: Our original roadmap was strictly linear:

1- Parse the configuration file.

2-Implement a basic maze generator (Prim's algorithm).

3-Write the output to a file.

4-Add a simple terminal print as a starting point.

**How it Evolved**: As we progressed, we realized the subject's requirements for reusability and packaging were more complex.

Pivot 1: We decided to separate the core logic into a standalone package (mazegen) early on, rather than keeping everything in one script. This required significant refactoring of our imports.
Pivot 2: We added the DFS algorithm as a second option to test our architecture's flexibility.
Pivot 3: The "42" pattern requirement introduced edge cases (e.g., small mazes), forcing us to add specific validation logic in config.py and utils.py.
