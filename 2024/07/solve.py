from pathlib import Path


def is_valid(value, numbers, total, *, concat=False):
    if total > value:
        return False

    if len(numbers) == 0:
        return value == total

    add_result = is_valid(value, numbers[1:], total + numbers[0], concat=concat)
    mul_result = is_valid(value, numbers[1:], total * numbers[0], concat=concat)
    con_result = (
        is_valid(value, numbers[1:], int(str(total) + str(numbers[0])), concat=concat)
        if concat
        else False
    )

    return add_result or mul_result or con_result


def parse(path):
    with Path(path).open() as f:
        equations = []
        for line in f.read().splitlines():
            value, numbers = line.split(": ")
            equations.append((int(value), list(map(int, numbers.split()))))
        return equations


def p1(path):
    calibration_result = 0
    for value, numbers in parse(path):
        if is_valid(value, numbers[1:], numbers[0], concat=False):
            calibration_result += value
    return calibration_result


def p2(path):
    calibration_result = 0
    for value, numbers in parse(path):
        if is_valid(value, numbers[1:], numbers[0], concat=True):
            calibration_result += value
    return calibration_result


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
