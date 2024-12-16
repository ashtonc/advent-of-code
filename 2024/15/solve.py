from pathlib import Path


def ncell(position, move):
    return (position[0] + move[0], position[1] + move[1])


def get_coordinate_sum(grid):
    gps_sum = 0
    for x, y in grid:
        if grid[(x, y)] == "O" or grid[(x, y)] == "[":
            gps_sum += (100 * y) + x
    return gps_sum


def double_grid(grid):
    new_grid = {}
    for x, y in grid:
        if grid[(x, y)] == "O":
            new_grid[(x * 2, y)] = "["
            new_grid[((x * 2) + 1, y)] = "]"
        else:
            new_grid[(x * 2, y)] = grid[(x, y)]
            new_grid[((x * 2) + 1, y)] = grid[(x, y)]
    return new_grid


def parse(path):
    grid = {}
    directions = []
    with Path(path).open() as f:
        for i, line in enumerate(f.read().splitlines()):
            if len(line) > 0 and line[0] == "#":
                for j, char in enumerate(line):
                    grid[(j, i)] = char
                    if char == "@":
                        start = (j, i)
                        grid[(j, i)] = "."
            else:
                for char in line:
                    if char == "v":
                        directions.append((0, 1))
                    if char == "<":
                        directions.append((-1, 0))
                    if char == ">":
                        directions.append((1, 0))
                    if char == "^":
                        directions.append((0, -1))
    return grid, start, directions


def p1(path):
    grid, position, directions = parse(path)
    while len(directions) > 0:
        move = directions.pop(0)
        target = ncell(position, move)
        prop = target
        while grid[prop] not in [".", "#"]:
            prop = ncell(prop, move)
        if grid[prop] == ".":
            position = target
            if prop != target:
                grid[target] = "."
                grid[prop] = "O"
    return get_coordinate_sum(grid)


def get_next_cells(pos, content):
    if content == "[":
        return (pos[0], pos[1]), (pos[0] + 1, pos[1])
    if content == "]":
        return (pos[0] - 1, pos[1]), (pos[0], pos[1])
    return content


def attempt_move(agrid, position, move):
    next_position = ncell(position, move)

    next_content = get_next_cells(next_position, agrid[next_position])
    if next_content == ".":
        return agrid
    if next_content == "#":
        return None

    move_stack = [next_content]
    while len(move_stack) > 0:
        left, right = move_stack.pop()

        left_dest = ncell(left, move)
        right_dest = ncell(right, move)

        left_cont = get_next_cells(left_dest, agrid[left_dest])
        right_cont = get_next_cells(right_dest, agrid[right_dest])

        if left_cont == "#" or right_cont == "#":
            return None

        if left_cont == "." and right_cont == ".":
            agrid[left_dest] = "["
            agrid[right_dest] = "]"
            agrid[left] = "."
            agrid[right] = "."

        else:
            move_stack.append((left, right))
            if left_cont != "." and left_cont not in move_stack:
                move_stack.append(left_cont)
            if right_cont != "." and right_cont not in move_stack:
                move_stack.append(right_cont)

    return agrid


def p2(path):
    grid, position, directions = parse(path)
    position = position[0] * 2, position[1]
    grid = double_grid(grid)

    while len(directions) > 0:
        move = directions.pop(0)

        if move[1] == 0:
            target = ncell(position, move)
            prop = target
            while grid[prop] not in [".", "#"]:
                prop = ncell(prop, move)
            if grid[prop] == ".":
                position = target
                grid[target] = "."
                while prop != target:
                    if move[0] == 1:
                        if grid[prop] == "." or grid[prop[0] + 1, prop[1]] == "[":
                            grid[prop] = "]"
                        else:
                            grid[prop] = "["
                    elif grid[prop] == "." or grid[prop[0] - 1, prop[1]] == "]":
                        grid[prop] = "["
                    else:
                        grid[prop] = "]"
                    prop = ncell(prop, (move[0] * -1, move[1]))
        else:
            attempt = attempt_move(grid.copy(), position, move)
            if attempt is not None:
                position = ncell(position, move)
                grid = attempt

    return get_coordinate_sum(grid)


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
