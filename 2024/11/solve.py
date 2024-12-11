from collections import defaultdict
from functools import cache
from pathlib import Path


@cache
def next_stone(stone):
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        half = len(str(stone)) // 2
        return [int(str(stone)[half:]), int(str(stone)[:half])]
    return [stone * 2024]


def blink(stones, count):
    for _ in range(count):
        new_stones = defaultdict(int)
        for stone, count in stones.items():
            for n in next_stone(stone):
                new_stones[n] += count
        stones = new_stones
    return stones


def parse(path):
    with Path(path).open() as f:
        stones = defaultdict(int)
        for stone in map(int, f.read().split()):
            stones[stone] += 1
        return stones


def p1(path):
    return sum(blink(parse(path), 25).values())


def p2(path):
    return sum(blink(parse(path), 75).values())


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
