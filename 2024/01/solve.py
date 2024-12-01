from pathlib import Path


def parse(uinput):
    left = []
    right = []
    for row in uinput.splitlines():
        left.append(int(row.split()[0]))
        right.append(int(row.split()[1]))

    return (sorted(left), sorted(right))


def p1(uinput):
    left, right = parse(uinput)

    diff = 0
    for i in range(len(left)):
        diff += abs(left[i] - right[i])

    return diff


def p2(uinput):
    left, right = parse(uinput)

    similarity = 0
    for i in set(left):
        similarity += i * left.count(i) * right.count(i)

    return similarity


with Path("example.txt").open() as f:
    example_input = f.read()

with Path("input.txt").open() as f:
    puzzle_input = f.read()

print("Example")
print(f"  Part 1: {p1(example_input)}")
print(f"  Part 2: {p2(example_input)}")

print("\nPuzzle Input")
print(f"  Part 1: {p1(puzzle_input)}")
print(f"  Part 2: {p2(puzzle_input)}")
