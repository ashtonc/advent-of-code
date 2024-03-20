import os
import sys
import re
from functools import cache

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputContents = readFile("input.txt")

@cache
def rotate90(p):
    return tuple(list(zip(*p[::-1])))

@cache
def tiltEast(p):
    r = []
    for line in p:
        l = "".join(line)
        while "O." in l:
            l = l.replace("O.", ".O")
        r.append(l)
    return tuple(r)

@cache
def getLoadNorth(p):
    height = len(p)
    a = 0
    for i in range(height, 0, -1):
        a += p[height-i].count("O") * i
    return a

platform = tuple(inputContents.splitlines())
print(f"P1 load: {getLoadNorth(rotate90(rotate90(rotate90((tiltEast(rotate90(platform)))))))}")

rotateCount = 1000000000
platformC = platform
states = set()
loopCount = 0
loopStart = 0
for i in range(rotateCount):
    platformC = tiltEast(rotate90(tiltEast(rotate90(tiltEast(rotate90(tiltEast(rotate90(platformC))))))))
    if platformC not in states:
        if loopCount > 0:
            loopCount += 1
        states.add(platformC)
    else:
        if loopCount == 0:
            states = set()
            loopStart = i+1
            loopCount += 1
            states.add(platformC)
        else:
            break

platformP = platform
for i in range(loopStart + ((rotateCount - loopCount - loopStart) % loopCount)):
    platformP = tiltEast(rotate90(tiltEast(rotate90(tiltEast(rotate90(tiltEast(rotate90(platformP))))))))

print(f"P2 load: {getLoadNorth(platformP)} (cycle start = {loopStart}, length = {loopCount})")
