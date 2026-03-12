*This project has been created as part of the 42 curriculum by Walid2907.*

## Description
A-Maze-ing is a Python maze generator. It reads a configuration file, generates a maze (perfect or not), writes it to a file using a hexadecimal wall encoding, and displays it in the terminal with interactive controls.

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

## Configuration file format
One `KEY=VALUE` per line. Lines starting with `#` are ignored.

Mandatory keys:
- `WIDTH=<int>`
- `HEIGHT=<int>`
- `ENTRY=x,y`
- `EXIT=x,y`
- `OUTPUT_FILE=<filename.txt>`
- `PERFECT=True|False`

Optional keys:
- `SEED=<int>`
- `ALGORITHM=PRIM|DFS`

Example:
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

## Maze generation algorithm
Implemented algorithms:
- Prim
- DFS

Why:
- Both generate perfect mazes naturally.
- Easy to make reproducible with a seed.

## Maze constraints / rules enforced
- Reproducibility with `SEED`
- Walls are coherent between neighbors (if east wall is closed in a cell, west wall is closed in the neighbor)
- The maze avoids any 3x3 open area (no large open rooms)
- The maze contains a visible “42” made of fully closed cells **when the maze is large enough**. If too small, the program prints an error and generates without the pattern.

## Reusable code (mazegen module)
The reusable generator is in the `mazegen` package and exposes:
- `MazeGenerator(width, height, seed, perfect, algorithm)`
- `.generate()` -> returns the wall-encoded grid
- `.solve(entry, exit_)` -> returns solution cells

## Resources
- Maze generation: randomized Prim / DFS spanning-tree maze generation
- Python typing: typing + mypy docs
- flake8 docs

### How AI was used
(Describe honestly what you used AI for: refactoring, checklisting requirements, generating README skeleton, etc.)

## Team and project management
- Roles: (fill)
- Planning: (fill)
- What worked / improvements: (fill)
- Tools used: (fill)