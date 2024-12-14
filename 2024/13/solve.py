from pathlib import Path
from re import search


def get_score(x, y, ax, ay, bx, by):
    a = int((x * by - y * bx) / (ax * by - ay * bx))
    b = int((ax * y - ay * x) / (ax * by - ay * bx))
    if (a * ax) + (b * bx) == x and (a * ay) + (b * by) == y:
        return (a * 3) + b
    return 0


def parse(path):
    with Path(path).open() as f:
        return [
            {
                "a": map(int, search(r"A: X.(\d+), Y.(\d+)", m).groups()),
                "b": map(int, search(r"B: X.(\d+), Y.(\d+)", m).groups()),
                "prize": map(int, search(r"Prize: X=(\d+), Y=(\d+)", m).groups()),
            }
            for m in f.read().split("\n\n")
        ]


def p1(path):
    score_sum = 0
    for machine in parse(path):
        x, y = machine["prize"]
        ax, ay = machine["a"]
        bx, by = machine["b"]
        score_sum += get_score(x, y, ax, ay, bx, by)
    return score_sum


def p2(path):
    score_sum = 0
    for machine in parse(path):
        x, y = machine["prize"]
        ax, ay = machine["a"]
        bx, by = machine["b"]
        score_sum += get_score(x + 10000000000000, y + 10000000000000, ax, ay, bx, by)
    return score_sum


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
