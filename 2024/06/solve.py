from pathlib import Path


def get_visited(grid, position, obstacle=(-1, -1)):
    direction = (0, -1)
    visited_directions = set()
    visited_positions = set()
    success = False
    while not success and (position, direction) not in visited_directions:
        visited_directions.add((position, direction))
        visited_positions.add(position)
        next_x = position[0] + direction[0]
        next_y = position[1] + direction[1]
        if next_x < 0 or next_y < 0 or next_x >= len(grid[0]) or next_y >= len(grid):
            success = True
        elif grid[next_y][next_x] == "#" or (next_x, next_y) == obstacle:
            if direction == (0, 1):
                direction = (-1, 0)
            elif direction == (-1, 0):
                direction = (0, -1)
            elif direction == (0, -1):
                direction = (1, 0)
            else:
                direction = (0, 1)
        else:
            position = (next_x, next_y)
    if not success:
        return None
    return visited_positions


def parse(path):
    with Path(path).open() as f:
        grid = f.read().splitlines()
        for i, line in enumerate(grid):
            if "^" in line:
                return grid, (line.index("^"), i)
    return None


def p1(path):
    grid, start = parse(path)
    return len(get_visited(grid, start))


def p2(path):
    grid, start = parse(path)
    loop_count = 0
    for x, y in get_visited(grid, start) - {start}:
        if get_visited(grid, start, (x, y)) is None:
            loop_count += 1
    return loop_count


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
