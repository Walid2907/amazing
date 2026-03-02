from mlx import Mlx

def draw_maze(maze, cell_size=40):
    rows = len(maze)
    cols = len(maze[0])
    width = cols * cell_size
    height = rows * cell_size

    m = Mlx()
    mlx_ptr = m.mlx_init()
    win = m.mlx_new_window(mlx_ptr, width, height, "Maze")

    WHITE = 0xFFFFFF
    BLACK = 0x000000

    def draw_line(x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            m.mlx_pixel_put(mlx_ptr, win, x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def render(param):
        # Fill background
        for y in range(height):
            for x in range(width):
                m.mlx_pixel_put(mlx_ptr, win, x, y, WHITE)

        for row in range(rows):
            for col in range(cols):
                cell = maze[row][col]
                x = col * cell_size
                y = row * cell_size

                if not (cell & (1 << 0)):  # North
                    draw_line(x, y, x + cell_size, y, BLACK)
                if not (cell & (1 << 1)):  # East
                    draw_line(x + cell_size, y, x + cell_size, y + cell_size, BLACK)
                if not (cell & (1 << 2)):  # South
                    draw_line(x, y + cell_size, x + cell_size, y + cell_size, BLACK)
                if not (cell & (1 << 3)):  # West
                    draw_line(x, y, x, y + cell_size, BLACK)

    m.mlx_loop_hook(mlx_ptr, render, None)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    example_maze = [
        [0b0110, 0b1100, 0b0101],
        [0b0011, 0b1010, 0b1001],
        [0b0110, 0b0101, 0b1100],
    ]
    draw_maze(example_maze, cell_size=60)