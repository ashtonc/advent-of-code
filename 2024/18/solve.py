from collections import defaultdict
from pathlib import Path
from re import findall


def get_neighbors(x, y, size):
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx <= size and 0 <= ny <= size]


def get_path(memory, size, limit):
    visited = set()
    current = (0, 0)
    scores = {current: 0}
    pqueue = defaultdict(set)
    pqueue[0].add(current)
    while pqueue:
        bucket = min(pqueue)
        current = pqueue[bucket].pop()
        if not pqueue[bucket]:
            del pqueue[bucket]
        if current == (size, size):
            return scores[(size, size)]
        visited.add(current)
        for neighbor in get_neighbors(*current, size):
            if neighbor in memory and memory[neighbor] < limit:
                continue
            score = scores[current] + 1
            if neighbor not in scores or score < scores[neighbor]:
                scores[neighbor] = score
                if neighbor not in visited:
                    pqueue[score].add(neighbor)
    return None


def parse(path):
    memory = {}
    with Path(path).open() as f:
        for i, line in enumerate(f.read().splitlines()):
            x, y = map(int, findall(r"\d+", line))
            memory[(x, y)] = i
    return memory


def p1(path, size, limit):
    return get_path(parse(path), size, limit)


def p2(path, size):
    memory = parse(path)
    min_i, max_i = 0, len(memory)
    while min_i < max_i:
        mid = (min_i + max_i) // 2
        if get_path(memory, size, mid):
            min_i = mid + 1
        else:
            max_i = mid
    return next(f"{k[0]},{k[1]}" for k, v in memory.items() if v == mid)


print("Example")
print(f"  Part 1: {p1('example.txt', 6, 12)}")
print(f"  Part 2: {p2('example.txt', 6)}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt', 70, 1024)}")
print(f"  Part 2: {p2('input.txt', 70)}")
