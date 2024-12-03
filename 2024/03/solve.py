import re
from pathlib import Path


def parse(path):
    with Path(path).open() as f:
        uinput = f.read()

    return uinput.splitlines()


def p1(path):
    mul_sum = 0
    for line in parse(path):
        for i in re.findall(r"mul\(([0-9]+),([0-9]+)\)", line):
            mul_sum += int(i[0]) * int(i[1])
    return mul_sum


def p2(path):
    enabled = True
    mul_sum = 0
    for line in parse(path):
        for i in re.findall(r"(?:mul\(([0-9]+),([0-9]+)\))|(do\(\))|(don't\(\))", line):
            if len(i[2]) > 0:
                enabled = True
            elif len(i[3]) > 0:
                enabled = False
            elif enabled:
                mul_sum += int(i[0]) * int(i[1])
    return mul_sum


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
