
# creating a that connect 2cells
# !!!!!! add a methode to protect it
class _Wall:
    def __init__(self):
        self.is_closed = True
        self.is_protected = False
        self.id = _Wall.id
        _Wall.id += 1
_Wall.id = 0

# initilise a cell
class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.north: _Wall | None = None
        self.south: _Wall | None = None
        self.east: _Wall | None = None
        self.west: _Wall | None = None
        self.visited = False


class Maze:
    def __init__(self, width: int, height: int, entry: int, exit_: int):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self._create_walls()

    def _create_walls(self):
        # Initialize walls and share between cells
        pass

    def generate_dfs(self, start_x=0, start_y=0):
        # DFS maze generation
        pass
