import os
import sys

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputContents = readFile("input.txt").split("\n\n")

def findReflectionRow(group, vertical=False, ignore=(0,0,"V")):
    for i in range(len(group)-1):
        c = i
        m = True
        for a in range(i, -1, -1):
            c += 1
            if c >= len(group):
                break
            if group[a] != group[c]:
                m = False
                break
        if m:
            r = (len(group)-i-1, len(group)-i, "V") if vertical else (i+1, i+2, "H")
            if r != ignore:
                return r
    if not vertical:
        return findReflectionRow(list(''.join(list(x)) for x in zip(*group))[::-1], vertical=True, ignore=ignore)

part1sum = 0
for group in inputContents:
    reflection = findReflectionRow(group.splitlines())
    if reflection[2] == "V": part1sum += reflection[0]
    if reflection[2] == "H": part1sum += reflection[0] * 100

print(f"Part 1: {part1sum}")

part2sum = 0
for group in inputContents:
    g = group.splitlines()
    reflection = findReflectionRow(g)

    for i in range(len(g)):
        for y in range(len(g[i])):
            if g[i][y] == "#":
                reflectionP = findReflectionRow(g[0:i] + [g[i][0:y] + "." + g[i][y+1:]] + g[i+1:], ignore=reflection)
            elif g[i][y] == ".":
                reflectionP = findReflectionRow(g[0:i] + [g[i][0:y] + "#" + g[i][y+1:]] + g[i+1:], ignore=reflection)
            if reflectionP != reflection and reflectionP != None:
                break
        else:
            continue
        break

    if reflectionP[2] == "V": part2sum += reflectionP[0]
    if reflectionP[2] == "H": part2sum += reflectionP[0] * 100

print(f"Part 2: {part2sum}")
