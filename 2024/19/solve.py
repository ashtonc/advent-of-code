from functools import cache
from pathlib import Path


@cache
def combos(design, patterns):
    if not design:
        return 1
    return sum(
        combos(design[len(pattern) :], patterns)
        for pattern in patterns
        if design.startswith(pattern)
    )


def parse(path):
    with Path(path).open() as f:
        content = f.read().splitlines()
    return tuple(content[0].split(", ")), content[2:]


def p1(path):
    patterns, designs = parse(path)
    return sum(combos(design, patterns) > 0 for design in designs)


def p2(path):
    patterns, designs = parse(path)
    return sum(combos(design, patterns) for design in designs)


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
