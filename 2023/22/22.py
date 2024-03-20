import os
import sys
from functools import cache

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

def init():
    return [tuple([tuple(map(int, c.split(","))) for c in b.split("~")]) for b in readFile("input.txt").splitlines()]

def settle(bricks):
    unsettled = sorted(bricks.copy(), key=lambda x: (min(x[0][2], x[1][2]), min(x[0][0], x[1][0]), min(x[0][1], x[1][1])))

    minX = min([min(b[0][0], b[1][0]) for b in unsettled])
    maxX = max([max(b[0][0], b[1][0]) for b in unsettled])
    minY = min([min(b[0][1], b[1][1]) for b in unsettled])
    maxY = max([max(b[0][1], b[1][1]) for b in unsettled])

    settled = []
    while len(unsettled) != 0:
        current = unsettled.pop(0)

        while len(getAdjacent(current, tuple(settled), "down")) == 0:
            currentZ = getZ(current)
            current = makeBrick(getXY(current), (currentZ[0]-1, currentZ[1]-1))
        settled.append(current)

    return settled

def getXY(brick):
    cornerA = (min(brick[0][0], brick[1][0]), min(brick[0][1], brick[1][1]))
    cornerB = (max(brick[0][0], brick[1][0]), max(brick[0][1], brick[1][1]))
    return cornerA, cornerB

def getZ(brick):
    return (min(brick[0][2], brick[1][2]), max(brick[0][2], brick[1][2]))

def isOverlapXY(b1, b2):
    xOverlap = b1[0][0] <= b2[1][0] and b1[1][0] >= b2[0][0]
    yOverlap = b1[0][1] <= b2[1][1] and b1[1][1] >= b2[0][1]
    return xOverlap and yOverlap

@cache
def getAdjacent(brick, bricks, direction="down"):
    if direction == "down":
        minZ = getZ(brick)[0]
        if minZ-1 == 0: return ["ground"]
        adjacent = [b for b in [b for b in bricks if max(b[0][2], b[1][2]) == minZ-1] if isOverlapXY(getXY(brick), getXY(b))]
    elif direction == "up":
        maxZ = getZ(brick)[1]
        adjacent = [b for b in [b for b in bricks if min(b[0][2], b[1][2]) == maxZ+1] if isOverlapXY(getXY(brick), getXY(b))]
    return adjacent

def makeBrick(xy, z):
    return((xy[0][0], xy[0][1], z[0]), (xy[1][0], xy[1][1], z[1]))

def getRemoveable(bricks):
    removeable = []
    for brick in bricks:
        safe = True
        for b in getAdjacent(brick, bricks, "up"):
            if len(getAdjacent(b, bricks, "down")) <= 1:
                safe = False
        if safe:
            removeable.append(brick)
    return removeable

def getChainCount(brick, bricks, removed):
    chainCount = 0
    removed.add(brick)
    for b in getAdjacent(brick, bricks, "up"):
        if removed.issuperset(getAdjacent(b, bricks, "down")):
            removed.add(b)
            chainCount += getChainCount(b, bricks, removed) + 1
    return chainCount

print("Settling bricks...", end="", flush=True); settledBricks = tuple(settle(init())); print(" done.")
print("Part 1:", len(getRemoveable(settledBricks)))
print("Part 2:", sum([getChainCount(b, settledBricks, set()) for b in settledBricks]))
