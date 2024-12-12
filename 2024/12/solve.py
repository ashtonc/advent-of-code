from itertools import product
from pathlib import Path


def get_neighbors(plot):
    return {(plot[0] + x, plot[1] + y) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]}


def get_regions(garden):
    regions = []
    plot_queue = set(garden.keys())
    while len(plot_queue) > 0:
        plot = plot_queue.pop()
        region = {plot}
        neighbor_queue = get_neighbors(plot)
        while len(neighbor_queue) > 0:
            neighbor = neighbor_queue.pop()
            if neighbor in plot_queue and garden[plot] == garden[neighbor]:
                plot_queue.remove(neighbor)
                region.add(neighbor)
                [neighbor_queue.add(n) for n in get_neighbors(neighbor)]
        regions.append(region)
    return regions


def get_perimeter(region):
    return sum([len([n for n in get_neighbors(p) if n not in region]) for p in region])


def get_sides(region):
    sides = 0
    for x, y in product(
        range(min([p[0] for p in region]), max([p[0] for p in region]) + 2),
        range(min([p[1] for p in region]), max([p[1] for p in region]) + 2),
    ):
        plot, top, left, diag = (x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)
        if not (
            (top in region and plot in region)
            or (top not in region and plot not in region)
            or (top in region and diag in region and left not in region)
            or (plot in region and left in region and diag not in region)
        ):
            sides += 1
        if not (
            (left in region and plot in region)
            or (left not in region and plot not in region)
            or (left in region and diag in region and top not in region)
            or (plot in region and top in region and diag not in region)
        ):
            sides += 1
    return sides


def parse(path):
    garden = {}
    with Path(path).open() as f:
        for y, line in enumerate(f.read().splitlines()):
            for x, plot in enumerate(line):
                garden[(x, y)] = plot
    return garden


def p1(path):
    return sum([len(r) * get_perimeter(r) for r in get_regions(parse(path))])


def p2(path):
    return sum([len(r) * get_sides(r) for r in get_regions(parse(path))])


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
