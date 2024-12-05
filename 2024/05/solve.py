from pathlib import Path


def is_correct_order(rules, update):
    correct_order = True
    for rule in [r for r in rules if r[0] in update and r[1] in update]:
        correct_order = update.index(rule[0]) < update.index(rule[1])
        if not correct_order:
            return False
    return True


def parse(path):
    rules = []
    updates = []
    with Path(path).open() as f:
        for line in f.read().splitlines():
            if "|" in line:
                rules.append(list(map(int, line.split("|"))))
            if "," in line:
                updates.append(list(map(int, line.split(","))))
    return rules, updates


def p1(path):
    rules, updates = parse(path)
    return sum([u[int(len(u) / 2)] for u in updates if is_correct_order(rules, u)])


def p2(path):
    rules, updates = parse(path)
    middle_sum = 0
    for update in [u for u in updates if not is_correct_order(rules, u)]:
        correct_order = False
        while not correct_order:
            for rule in [r for r in rules if r[0] in update and r[1] in update]:
                l_index = update.index(rule[0])
                r_index = update.index(rule[1])
                if l_index < r_index:
                    continue
                update[l_index], update[r_index] = rule[1], rule[0]
            correct_order = is_correct_order(rules, update)
        middle_sum += update[int(len(update) / 2)]
    return middle_sum


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
