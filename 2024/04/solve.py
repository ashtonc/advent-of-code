from pathlib import Path


def parse(path):
    with Path(path).open() as f:
        return f.read().splitlines()


def p1(path):
    array = parse(path)
    height = len(array)
    width = len(array[0])

    xmas_count = 0
    for i, line in enumerate(array):
        for j, letter in enumerate(line):
            if letter == "X":
                for h in [-1, 0, 1]:
                    for v in [-1, 0, 1]:
                        location = (i, j)
                        for c in ["M", "A", "S"]:
                            location = (location[0] + h, location[1] + v)
                            if (
                                location[0] >= 0
                                and location[0] < height
                                and location[1] >= 0
                                and location[1] < width
                            ):
                                if array[location[0]][location[1]] != c:
                                    break
                                if c == "S":
                                    xmas_count += 1
    return xmas_count


def p2(path):
    array = parse(path)
    height = len(array)
    width = len(array[0])

    xmas_count = 0
    for i, line in enumerate(array):
        for j, letter in enumerate(line):
            if letter == "A":
                corners = ""
                for h in [-1, 1]:
                    for v in [-1, 1]:
                        location = (i + h, j + v)
                        if (
                            location[0] >= 0
                            and location[0] < height
                            and location[1] >= 0
                            and location[1] < width
                        ):
                            corners = corners + array[location[0]][location[1]]
                if corners in ["SSMM", "MMSS", "MSMS", "SMSM"]:
                    xmas_count += 1
    return xmas_count


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
