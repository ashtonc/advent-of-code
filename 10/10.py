import os
import re
import sys
import math

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputMap = (readFile("input.txt").replace("L", "└")
                                 .replace("J", "┘")
                                 .replace("7", "┐")
                                 .replace("F", "┌")
                                 .replace("|", "│")
                                 .replace("-", "─")
                                 .replace(".", "·")).splitlines()

mapHeight = len(inputMap)
mapWidth = len(inputMap[0])

startChar = "S"
startPosition = None
for i, line in enumerate(inputMap):
    if startChar in line:
        startPosition = i, line.index(startChar)
        break

def getCoordinateChar(c):
    return inputMap[c[0]][c[1]]

def getAdjacentCoordinates(c):
    adjacentCoordinates = []
    if c[0]-1 >= 0 and getCoordinateChar(c) in ["S", "│", "└", "┘"]:        adjacentCoordinates.append((c[0]-1, c[1])) # North
    if c[1]+1 < mapWidth and getCoordinateChar(c) in ["S", "─", "└", "┌"]:  adjacentCoordinates.append((c[0], c[1]+1)) # East
    if c[0]+1 < mapHeight and getCoordinateChar(c) in ["S", "│", "┐", "┌"]: adjacentCoordinates.append((c[0]+1, c[1])) # South
    if c[1]-1 >= 0 and getCoordinateChar(c) in ["S", "─", "┐", "┘"]:        adjacentCoordinates.append((c[0], c[1]-1)) # West
    return adjacentCoordinates

def getNextPosition(origin, c):
    for n in getAdjacentCoordinates(c):
        if n[0] < c[0] and getCoordinateChar(n) in ["│", "┐", "┌"] and n != origin: return n # North
        if n[1] > c[1] and getCoordinateChar(n) in ["─", "┐", "┘"] and n != origin: return n # East
        if n[0] > c[0] and getCoordinateChar(n) in ["│", "└", "┘"] and n != origin: return n # South
        if n[1] < c[1] and getCoordinateChar(n) in ["─", "└", "┌"] and n != origin: return n # West
    return startPosition

def getAdjacentPathCoordinates(c):
    index = path.index(c)
    adjacentPathCoordinates = []

    if index == 0:
        adjacentPathCoordinates.append(path[-1])
    else:
        adjacentPathCoordinates.append(path[index-1])
    
    if index == len(path)-1:
        adjacentPathCoordinates.append(path[0])
    else:
        adjacentPathCoordinates.append(path[index+1])
    
    return adjacentPathCoordinates

pathStarts = []
for c in getAdjacentCoordinates(startPosition):
    if c[0] < startPosition[0] and getCoordinateChar(c) in ["│", "┐", "┌"]: pathStarts.append(c) # North
    if c[1] > startPosition[1] and getCoordinateChar(c) in ["─", "┐", "┘"]: pathStarts.append(c) # East
    if c[0] > startPosition[0] and getCoordinateChar(c) in ["│", "└", "┘"]: pathStarts.append(c) # South
    if c[1] < startPosition[1] and getCoordinateChar(c) in ["─", "└", "┌"]: pathStarts.append(c) # West

path = [startPosition, pathStarts[0]]
currentPosition = pathStarts[0]
nextPosition = None
while nextPosition != startPosition:
    nextPosition = getNextPosition(path[-2], path[-1])
    if nextPosition != startPosition: path.append(nextPosition)

pathMap = []
for y in range(0, mapHeight):
    newLine = []
    for x in range(0, mapWidth):
        if (y, x) not in path:
            newLine.append("·")
        else:
            newLine.append(inputMap[y][x])
    pathMap.append("".join(newLine))

for line in pathMap: print(line)
print()

enclosedCount = 0
for y in range(0, mapHeight):
    edges = [c for c in path if c[0] == y]
    edgeHits = 0
    edgeStartChar = None
    for x in range(0, mapWidth):
        char = getCoordinateChar((y, x))
        if (y, x) in edges and char == "│":
            # print("█", end="")
            edgeHits += 1
        elif (y, x) in edges and char in ["└", "┌"]:
            # print("▒", end="")
            edgeStartChar = char
        elif (y, x) in edges and char in ["┘", "┐", startChar]: # Manual fix for "S"
            if (edgeStartChar == "└" and char == "┘") or (edgeStartChar == "┌" and char == "┐"):
                # print("▒", end="")
                pass
            else:
                # print("█", end="")
                edgeHits += 1
            edgeStartChar = None
        elif (y, x) in edges and char == "─":
            # print("▒", end="")
            pass
        elif edgeHits % 2 == 1:
            # print("╳", end="")
            enclosedCount += 1
        else:
            # print("·", end="")
            pass
    # print(" ", enclosedCount)

print(f"Max distance = {int(math.ceil((len(path))/2))}")
print(f"Enclosed count = {enclosedCount}")
