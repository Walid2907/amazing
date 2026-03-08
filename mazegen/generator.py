from .algorithms import prim, dfs, bfs, path_to_cells


class MazeGenerator:
    def __init__(self, width: int,
                 height: int, seed: int = None,
                 perfect: bool = False, algorithm: str = "PRIM"):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.algorithm = algorithm.upper()
        self.maze = None
        self.solution = None

    def generate(self):
        if self.algorithm == "prim":
            self.maze = prim(self.width, self.height, self.seed, self.perfect)
        elif self.algorithm == "DFS":
            self.maze = dfs(self.width, self.height, self.seed, self.perfect)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        return self.maze

    def solve(self, entry: tuple, exit_: tuple):
        if not self.maze:
            raise ValueError("Maze has not been generated yet.")
        self.solution = bfs(self.maze, entry, exit_)
        return path_to_cells(entry, self.solution)
