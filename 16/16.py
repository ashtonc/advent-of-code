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

def isLegal(beam):
    x = beam[0][0]
    y = beam[0][1]
    if beam not in cellCache:
        cellCache.add(beam)
    else:
        return False
    return not (x < 0 or y < 0 or x >= width or y >= height)

def getNextCell(beam):
    x = beam[0][0]
    y = beam[0][1]
    if beam[1] == "N": return (x, y-1)
    if beam[1] == "E": return (x+1, y)
    if beam[1] == "S": return (x, y+1)
    if beam[1] == "W": return (x-1, y)

def getNextState(beam):
    x = beam[0][0]
    y = beam[0][1]
    direction = beam[1]

    if contraption[y][x] == ".":
        return beam, None

    if contraption[y][x] == "/":
        if direction == "N": return ((x, y), "E"), None
        if direction == "E": return ((x, y), "N"), None
        if direction == "S": return ((x, y), "W"), None
        if direction == "W": return ((x, y), "S"), None

    if contraption[y][x] == "\\":
        if direction == "N": return ((x, y), "W"), None
        if direction == "E": return ((x, y), "S"), None
        if direction == "S": return ((x, y), "E"), None
        if direction == "W": return ((x, y), "N"), None

    if contraption[y][x] == "-":
        if direction in ["E", "W"]:
            return beam, None
        else:
            return ((x, y), "E"), ((x, y), "W")

    if contraption[y][x] == "|":
        if direction in ["N", "S"]:
            return beam, None
        else:
            return ((x, y), "N"), ((x, y), "S")

def getEnergizedCount(beams):
    energizedCells = set()
    while len(beams) != 0:
        beam = beams.pop(0)
        nextCell = getNextCell(beam)
        if isLegal(((nextCell), beam[0])):
            energizedCells.add(nextCell)
            beam, beamP = getNextState((nextCell, beam[1]))
            beams.append(beam)
            if beamP != None:
                beams.append(beamP)
    return len(energizedCells)

contraption = readFile("input.txt").splitlines()
height = len(contraption)
width = len(contraption[0])

cellCache = set()
print(f"Part 1: {getEnergizedCount([((-1, 0), 'E')])}")

maxE = 0
for i in range(width):
    cellCache = set()
    count = getEnergizedCount([((i, -1), 'S')])
    if count > maxE: maxE = count

for i in range(height):
    cellCache = set()
    count = getEnergizedCount([((-1, i), 'E')])
    if count > maxE: maxE = count

print(f"Part 2: {maxE}")
