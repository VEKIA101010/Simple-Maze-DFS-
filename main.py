import random
import time
import os

WIDTH, HEIGHT = 50, 50

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy//2][x + dx//2] = 0
                carve(nx, ny)

    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    maze[start_y][start_x] = 0
    carve(start_x, start_y)
    return maze, (start_x, start_y)

def print_maze(maze, path=set(), stack_top=None, start=None, end=None):
    for y, row in enumerate(maze):
        line = ''
        for x, cell in enumerate(row):
            pos = (x, y)
            if pos == start:
                line += 'S '
            elif pos == end:
                line += 'E '
            elif pos == stack_top:
                line += '? '
            elif pos in path:
                line += '* '
            elif cell == 1:
                line += '█ '
            else:
                line += '. '
        print(line)
    print()

def neighbors(pos, maze):
    x, y = pos
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] == 0:
                yield (nx, ny)

def dfs(maze, start, end, delay=0.02):
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        clear_console()
        print_maze(maze, set(path), stack_top=current, start=start, end=end)
        time.sleep(delay)

        if current == end:
            return path

        if current in visited:
            continue
        visited.add(current)

        for nxt in neighbors(current, maze):
            if nxt not in visited:
                stack.append((nxt, path + [nxt]))

    return None

if __name__ == "__main__":
    maze, start = generate_maze(WIDTH, HEIGHT)
    free_cells = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 0 and (x, y) != start]
    end = random.choice(free_cells)

    print("Maze generated. Start:", start, "End:", end)
    time.sleep(1)

    path = dfs(maze, start, end)
    if path:
        clear_console()
        print_maze(maze, set(path), start=start, end=end)
        print("Path found! Length:", len(path))
    else:
        print("No path found.")
