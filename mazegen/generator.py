from .algorithms import prim, dfs, bfs, path_to_cells
from typing import Optional


class MazeGenerator:
    """Generate and solve mazes using different algorithms.

    This class provides a unified interface for creating a maze using
    different generation algorithms and solving it using BFS.

    Attributes:
        width: Width of the maze.
        height: Height of the maze.
        seed: Optional random seed for deterministic generation.
        perfect: Whether the maze should contain no loops.
        algorithm: Generation algorithm to use ("PRIM" or "DFS").
        maze: Generated maze grid.
        solution: Path solution returned by the solver.
    """
    def __init__(self, width: int,
                 height: int, seed: int | None = None,
                 perfect: bool = False, algorithm: str = "PRIM"):
        """Initialize the maze generator.

        Args:
            width: Width of the maze grid.
            height: Height of the maze grid.
            seed: Optional random seed.
            perfect: Whether the maze must be perfect (no loops).
            algorithm: Maze generation algorithm ("PRIM" or "DFS").
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.algorithm = algorithm.upper()
        self.maze: Optional[list[list[int]]] = None
        self.solution: Optional[list[str]] = None

    def generate(self) -> list[list[int]]:
        """Generate a maze using the selected algorithm.

        Returns:
            The generated maze as a 2D grid.

        Raises:
            ValueError: If the selected algorithm is unsupported.
        """
        if self.algorithm == "PRIM":
            self.maze = prim(self.width, self.height, self.seed, self.perfect)
        elif self.algorithm == "DFS":
            self.maze = dfs(self.width, self.height, self.seed, self.perfect)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        return self.maze

    def solve(self, entry: tuple[int, int],
              exit_: tuple[int, int]) -> list[tuple[int, int]]:
        """Solve the maze using BFS.

        Args:
            entry: Entry coordinate.
            exit_: Exit coordinate.

        Returns:
            A list of cell coordinates representing the path
            from entry to exit.

        Raises:
            ValueError: If the maze has not been generated yet
                or if no path exists.
        """
        if not self.maze:
            raise ValueError("Maze has not been generated yet.")
        self.solution = bfs(self.maze, entry, exit_)
        if self.solution is None:
            raise ValueError("No path found between entry and exit.")
        return path_to_cells(entry, self.solution)
