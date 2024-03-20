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

inputContent = readFile("input.txt").splitlines()
inputHeight = len(inputContent)
inputWidth = len(inputContent[0])

emptyRows = []
for i, line in enumerate(inputContent):
    # print(line)
    galaxyCount = len([g for g in line if g == "#"])
    if galaxyCount == 0:
        emptyRows.append(i)

galaxyList = []
emptyColumns = []
for x in range(0, inputWidth):
    empty = True
    for y in range(0, inputHeight):
        if inputContent[y][x] == "#":
            empty = False
            galaxyList.append((y, x))
    if empty:
        emptyColumns.append(x)

expandedGalaxyList = []
for galaxy in galaxyList:
    extraRows = len([c for c in emptyRows if c < galaxy[0]])
    extraColumns = len([c for c in emptyColumns if c < galaxy[1]])
    expandedGalaxyList.append((galaxy[0]+extraRows, galaxy[1]+extraColumns))

shortestPathSum = 0
for galaxy in expandedGalaxyList:
    for galaxyP in expandedGalaxyList:
        shortestPathLength = abs(galaxyP[0] - galaxy[0]) + abs(galaxyP[1] - galaxy[1])
        shortestPathSum += shortestPathLength

print(f"Shortest path sum = {int(shortestPathSum / 2)}")

oldGalaxyList = []
for galaxy in galaxyList:
    extraRows = len([c for c in emptyRows if c < galaxy[0]]) * 999999
    extraColumns = len([c for c in emptyColumns if c < galaxy[1]]) * 999999
    oldGalaxyList.append((galaxy[0]+extraRows, galaxy[1]+extraColumns))

shortestPathSum = 0
for galaxy in oldGalaxyList:
    for galaxyP in oldGalaxyList:
        shortestPathLength = abs(galaxyP[0] - galaxy[0]) + abs(galaxyP[1] - galaxy[1])
        shortestPathSum += shortestPathLength

print(f"Shortest path sum (old) = {int(shortestPathSum / 2)}")

