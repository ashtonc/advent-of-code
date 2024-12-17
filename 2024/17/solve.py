from itertools import chain
from pathlib import Path
from re import search


def operate(computer):
    output = []
    pointer = 0
    reg_a, reg_b, reg_c = computer["A"], computer["B"], computer["C"]
    while pointer < len(computer["P"]):
        operand = computer["P"][pointer + 1]
        combo = [0, 1, 2, 3, reg_a, reg_b, reg_c][operand]
        match computer["P"][pointer]:
            case 0:
                reg_a = int(reg_a / (2**combo))
            case 1:
                reg_b = reg_b ^ operand
            case 2:
                reg_b = combo % 8
            case 3:
                if reg_a != 0:
                    pointer = operand
                    continue
            case 4:
                reg_b = reg_b ^ reg_c
            case 5:
                output.append(combo % 8)
            case 6:
                reg_b = int(reg_a / (2**combo))
            case 7:
                reg_c = int(reg_a / (2**combo))
        pointer += 2
    return output


def parse(path):
    with Path(path).open() as f:
        content = f.read()
    return {
        "A": int(search(r"A: (\d+)", content).group(1)),
        "B": int(search(r"B: (\d+)", content).group(1)),
        "C": int(search(r"C: (\d+)", content).group(1)),
        "P": list(map(int, search(r"m: ([\d,]+)", content).group(1).split(","))),
    }


def p1(path):
    return ",".join(map(str, operate(parse(path))))


def find_values(computer, test_a, depth):
    computer["A"] = test_a
    result = operate(computer)
    if result == computer["P"]:
        return [test_a]
    if depth == 0 or result == computer["P"][-depth:]:
        return list(
            chain.from_iterable(
                find_values(computer, 8 * test_a + n, depth + 1) or [] for n in range(8)
            )
        )
    return None


def p2(path):
    return min(find_values(parse(path), 0, 0))


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
