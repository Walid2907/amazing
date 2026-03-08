from .algorithms import prim, dfs, bfs, path_to_cells
from typing import Optional


class MazeGenerator:
    def __init__(self, width: int,
                 height: int, seed: int | None = None,
                 perfect: bool = False, algorithm: str = "PRIM"):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.algorithm = algorithm.upper()
        self.maze: Optional[list[list[int]]] = None
        self.solution: Optional[list[str]] = None

    def generate(self) -> list[list[int]]:
        if self.algorithm == "PRIM":
            self.maze = prim(self.width, self.height, self.seed, self.perfect)
        elif self.algorithm == "DFS":
            self.maze = dfs(self.width, self.height, self.seed, self.perfect)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        return self.maze

    def solve(self, entry: tuple[int, int],
              exit_: tuple[int, int]) -> list[tuple[int, int]]:
        if not self.maze:
            raise ValueError("Maze has not been generated yet.")
        self.solution = bfs(self.maze, entry, exit_)
        if self.solution is None:
            raise ValueError("No path found between entry and exit.")
        return path_to_cells(entry, self.solution)
