from pathlib import Path


def in_bounds(antinode, height, width):
    x, y = antinode
    return x >= 0 and y >= 0 and x < width and y < height


def parse(path):
    antennas = {}
    with Path(path).open() as f:
        antennamap = f.read().splitlines()
        for i, line in enumerate(antennamap):
            for j, frequency in enumerate(line):
                if frequency != ".":
                    if frequency in antennas:
                        antennas[frequency].append((j, i))
                    else:
                        antennas[frequency] = [(j, i)]
        return antennas.values(), len(antennamap), len(antennamap[0])


def p1(path):
    antennas, h, w = parse(path)
    antinodes = set()
    for locations in antennas:
        for l_index, location in enumerate(locations):
            i = l_index
            while i < len(locations) - 1:
                i += 1
                distance_x = location[0] - locations[i][0]
                distance_y = location[1] - locations[i][1]

                [
                    antinodes.add(antinode)
                    for antinode in [
                        (location[0] + distance_x, location[1] + distance_y),
                        (locations[i][0] - distance_x, locations[i][1] - distance_y),
                    ]
                    if in_bounds(antinode, h, w)
                ]
    return len(antinodes)


def p2(path):
    antennas, h, w = parse(path)
    antinodes = set()
    for locations in antennas:
        for l_index, location in enumerate(locations):
            i = l_index
            while i < len(locations) - 1:
                i += 1
                distance_x = location[0] - locations[i][0]
                distance_y = location[1] - locations[i][1]

                antinode = location
                while in_bounds(antinode, h, w):
                    antinodes.add(antinode)
                    antinode = (antinode[0] + distance_x, antinode[1] + distance_y)

                antinode = locations[i]
                while in_bounds(antinode, h, w):
                    antinodes.add(antinode)
                    antinode = (antinode[0] - distance_x, antinode[1] - distance_y)
    return len(antinodes)


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
