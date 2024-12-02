from pathlib import Path


def is_valid_report(report):
    for i in range(len(report)):
        if i == len(report) - 1:
            return True
        if report[0] < report[1] and report[i] >= report[i + 1]:
            break
        if report[0] > report[1] and report[i] <= report[i + 1]:
            break
        if abs(report[i] - report[i + 1]) not in range(1, 3 + 1):
            break
    return False


def parse(path):
    with Path(path).open() as f:
        return [list(map(int, report.split())) for report in f.read().splitlines()]


def p1(path):
    return sum(map(int, map(is_valid_report, parse(path))))


def p2(path):
    safe = 0
    for report in parse(path):
        if is_valid_report(report):
            safe += 1
            continue

        for i in range(len(report)):
            if is_valid_report(report[:i] + report[i + 1 :]):
                safe += 1
                break

    return safe


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
