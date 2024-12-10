from pathlib import Path


def get_directions(x, y, height):
    return [
        (x + 1, y, height + 1),
        (x, y + 1, height + 1),
        (x - 1, y, height + 1),
        (x, y - 1, height + 1),
    ]


def get_trails(guide):
    max_height = 9
    trails = {}
    for y, row in guide.items():
        for x, height in row.items():
            if height == 0:
                trails[(x, y)] = []
                dir_stack = get_directions(x, y, height)
                while len(dir_stack) > 0:
                    t_x, t_y, t_height = dir_stack.pop()
                    if t_x in row and t_y in guide and guide[t_y][t_x] == t_height:
                        if t_height == max_height:
                            trails[(x, y)].append((t_x, t_y))
                        else:
                            dir_stack.extend(get_directions(t_x, t_y, t_height))
    return trails.values()


def parse(path):
    guide = {}
    with Path(path).open() as f:
        for i, line in enumerate(f.read().splitlines()):
            guide[i] = {j: int(height) for j, height in enumerate(line)}
        return guide


def p1(path):
    return sum(len(set(t)) for t in get_trails(parse(path)))


def p2(path):
    return sum(len(t) for t in get_trails(parse(path)))


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
