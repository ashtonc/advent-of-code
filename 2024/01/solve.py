from pathlib import Path


def parse(path):
    with Path(path).open() as f:
        uinput = f.read()

    left = []
    right = []
    for row in uinput.splitlines():
        left.append(int(row.split()[0]))
        right.append(int(row.split()[1]))

    return (sorted(left), sorted(right))


def p1(path):
    left, right = parse(path)

    diff = 0
    for i in range(len(left)):
        diff += abs(left[i] - right[i])

    return diff


def p2(path):
    left, right = parse(path)

    similarity = 0
    for i in set(left):
        similarity += i * left.count(i) * right.count(i)

    return similarity


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
