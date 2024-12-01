from pathlib import Path


def parse(path):
    with Path(path).open() as f:
        uinput = f.read()

    return uinput.splitlines()


def p1(path):
    return None


def p2(path):
    return None


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
