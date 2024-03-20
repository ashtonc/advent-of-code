import os
import re
import sys

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

def getDugSet(plans, useHex=False):
    dug = set()
    current = (0,0)
    dug.add(current)

    for plan in plans:
        plan = re.findall(planRegex, plan)

        direction = plan[0][0]
        count = int(plan[0][1])

        if useHex:
            direction = ["R", "D", "L", "U"][int(plan[0][2][-1])]
            count = int(plan[0][2][:5], 16)

        for i in range(count):
            if direction == "U": current = (current[0]-1, current[1])
            if direction == "R": current = (current[0],   current[1]+1)
            if direction == "D": current = (current[0]+1, current[1])
            if direction == "L": current = (current[0],   current[1]-1)
            dug.add(current)

    return dug

def getDugPath(plans, useHex=False):
    path = [(0, 0)]
    for plan in plans:
        plan = re.findall(planRegex, plan)

        direction = plan[0][0]
        count = int(plan[0][1])

        if useHex:
            direction = ["R", "D", "L", "U"][int(plan[0][2][-1])]
            count = int(plan[0][2][:5], 16)

        current = path[-1]
        if direction == "U": current = (current[0]-count, current[1])
        if direction == "R": current = (current[0],       current[1]+count)
        if direction == "D": current = (current[0]+count, current[1])
        if direction == "L": current = (current[0],       current[1]-count)

        path.append(current)
    return path

def getFilledSetCount(dug):
    minheight = min(x[0] for x in dug)
    minwidth = min(x[1] for x in dug)
    height = max(x[0] for x in dug)
    width = max(x[1] for x in dug)

    # for h in range(minheight, height+1):
        # for w in range(minwidth, width+1):
            # if (h, w) == (0, 0):
                # print("╳", end="")
            # elif (h, w) in dug:
                # print("#", end="")
            # else:
                # print("-", end="")
        # print()

    flooded = set()
    test = [(1,1)]

    while test != []:
        current = test.pop(0)
        for adj in [(current[0]-1, current[1]), (current[0], current[1]+1), (current[0]+1, current[1]), (current[0], current[1]-1)]:
            if adj not in dug and adj not in flooded:
                flooded.add(adj)
                test.append(adj)

    return len(flooded) + len(dug)

def getFilledPathCount(path):
    perimiter = 0
    area = 0.0
    for i in range(len(path)):
        j = (i + 1) % len(path)
        area += path[i][0] * path[j][1]
        area -= path[j][0] * path[i][1]
        perimiter += abs(path[i][0] - path[j][0] + path[i][1] - path[j][1])
    return abs(int(0.5 * area)) + int((perimiter / 2) + 1)

plans = readFile("input.txt").splitlines()
planRegex = re.compile(r"([RDLU]) ([0-9]+) \(#(......)\)")

print(f"Part 1: {getFilledSetCount(getDugSet(plans))}")
print(f"Part 2: {getFilledPathCount(getDugPath(plans, True))}")
