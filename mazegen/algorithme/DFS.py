from random import shuffle, randrange


def make_maze(width=16, height=8):
    visited = [[False] * width for _ in range(height)]

    # Each cell keeps track of which walls exist
    walls = [[{'N': True, 'S': True, 'E': True, 'W': True}
              for _ in range(width)] for _ in range(height)]

    def walk(x, y):
        visited[y][x] = True
        directions = [('N', 0, -1), ('S', 0, 1), ('W', -1, 0), ('E', 1, 0)]
        shuffle(directions)

        for d, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                walls[y][x][d] = False
                walls[ny][nx][{'N':'S','S':'N','E':'W','W':'E'}[d]] = False
                walk(nx, ny)

    walk(randrange(width), randrange(height))
    return draw_maze(walls, width, height)


def draw_maze(walls, width, height):
    maze = []

    # Top border
    maze.append('┌' + '───' * width + '┐')

    # Each row
    for y in range(height):
        # Cell row
        mid = '│'
        for x in range(width):
            mid += '   '
            if x < width - 1:
                mid += '│' if walls[y][x]['E'] else ' '
        mid += '│'  # Right border
        maze.append(mid)

        # Horizontal walls row (unless it's the last row)
        if y < height - 1:
            bottom = '│'
            for x in range(width):
                bottom += '───' if walls[y][x]['S'] else '   '
                if x < width - 1:
                    # Check if there's a vertical wall between current and next cell
                    bottom += '│' if (walls[y][x]['E'] or walls[y+1][x]['E']) else ' '
            bottom += '│'  # Right border
            maze.append(bottom)

    # Bottom border
    maze.append('└' + '───' * width + '┘')

    return '\n'.join(maze)


if __name__ == '__main__':
    print(make_maze(19, 9))