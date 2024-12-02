from pathlib import Path


def parse(path):
    with Path(path).open() as f:
        uinput = f.read()

    return [list(map(int, report.split())) for report in uinput.splitlines()]


def p1(path):
    reports = parse(path)

    safe = 0
    for report in reports:
        direction = "asc" if report[0] < report[1] else "desc"
        for i in range(len(report)):
            if i == len(report) - 1:
                safe += 1
            else:
                if direction == "asc" and report[i] >= report[i + 1]:
                    break
                if direction == "desc" and report[i] <= report[i + 1]:
                    break
                if abs(report[i] - report[i + 1]) not in range(1, 3 + 1):
                    break

    return safe


def p2(path):
    reports = parse(path)

    safe = 0
    for report in reports:
        results = []
        for i in range(len(report)):
            if i == len(report) - 1:
                break
            if report[i] < report[i + 1]:
                results.append("asc")
            elif report[i] > report[i + 1]:
                results.append("desc")
            else:
                results.append("even")
        print(results)

    return safe


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
# print(f"  Part 2: {p2('input.txt')}")
