from collections import defaultdict
from math import prod
from pathlib import Path
from re import search
from statistics import variance


def get_position(px, py, vx, vy, time, width, height):
    return (px + (time * vx)) % width, (py + (time * vy)) % height


def parse(path):
    with Path(path).open() as f:
        return [
            list(map(int, search(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line).groups()))
            for line in f.read().splitlines()
        ]


def p1(path):
    width = 101
    height = 103
    safety_factor = defaultdict(int)
    for x, y in [get_position(*r, 100, width, height) for r in parse(path)]:
        if x < (width / 2) - 1 and y < (height / 2) - 1:
            safety_factor[0] += 1
        elif x > width / 2 and y < (height / 2) - 1:
            safety_factor[1] += 1
        elif x < (width / 2) - 1 and y > height / 2:
            safety_factor[2] += 1
        elif x > width / 2 and y > height / 2:
            safety_factor[3] += 1
    return prod(safety_factor.values())


def p2(path):
    width = 101
    height = 103
    robots = parse(path)
    x_variance = None
    y_variance = None
    for i in range(max(width, height)):
        x_vals, y_vals = [], []
        for x, y in [get_position(*r, i, width, height) for r in robots]:
            x_vals.append(x)
            y_vals.append(y)
        if x_variance is None or variance(x_vals) < x_variance[0]:
            x_variance = (variance(x_vals), i)
        if y_variance is None or variance(y_vals) < y_variance[0]:
            y_variance = (variance(y_vals), i)
    for i in range(width * height, 0, -1):
        if i % width == x_variance[1] and i % height == y_variance[1]:
            return i
    return None


print("Puzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
