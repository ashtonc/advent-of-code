from collections import defaultdict
from pathlib import Path


def neighbors_score(node):
    x, y, dx, dy = *node[0], *node[1]
    if dx == 0:
        turn1 = (x, y), (1, 0)
        turn2 = (x, y), (-1, 0)
    else:
        turn1 = (x, y), (0, 1)
        turn2 = (x, y), (0, -1)
    return [(((x + dx, y + dy), (dx, dy)), 1), (turn1, 1000), (turn2, 1000)]


def get_path(maze, start, end, direction=(1, 0)):
    visited = set()
    current = start, direction
    scores = {current: 0}
    pqueue = defaultdict(set)
    pqueue[0].add(current)
    bucket = 0
    while current[0] != end:
        if len(pqueue[bucket]) == 0:
            bucket += 1
            continue
        current = pqueue[bucket].pop()
        visited.add(current)
        for neighbor, score in neighbors_score(current):
            if maze[neighbor[0]] != "#":
                nscore = scores[current] + score
                if neighbor not in scores or nscore < scores[neighbor]:
                    scores[neighbor] = nscore
                if neighbor not in visited:
                    pqueue[scores[neighbor]].add(neighbor)
    return scores[current], scores


def parse(path):
    maze = {}
    with Path(path).open() as f:
        for i, line in enumerate(f.read().splitlines()):
            for j, char in enumerate(line):
                maze[(j, i)] = char
                if char == "S":
                    start = (j, i)
                if char == "E":
                    end = (j, i)
    return maze, start, end


def p1(path):
    return get_path(*parse(path))[0]


def p2(path):
    maze, start, end = parse(path)
    total, scores = get_path(maze, start, end)
    escores = get_path(maze, end, start)[1]

    best_nodes = set()
    for node in scores:
        xy, dx, dy = node[0], *node[1]
        rnode = xy, (dx * -1, dy * -1)
        if (
            node in scores
            and rnode in escores
            and scores[node] + escores[rnode] in [total, total + 1000, total + 2000]
        ):
            best_nodes.add(node[0])
    return len(best_nodes)


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
