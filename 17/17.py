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

def getNeighbors(cell, direction, streak, minstraight, maxstraight):
    y = cell[0]
    x = cell[1]

    options = ["N", "E", "S", "W"]

    if   direction == "N": options.remove("S")
    elif direction == "E": options.remove("W")
    elif direction == "S": options.remove("N")
    elif direction == "W": options.remove("E")

    if streak >= maxstraight:
        options.remove(direction)

    if streak < minstraight and streak != 0:
        options = [direction]

    neighbors = []
    for d in options:
        if   d == "N": c = (y-1, x)
        elif d == "E": c = (y,   x+1)
        elif d == "S": c = (y+1, x)
        elif d == "W": c = (y,   x-1)

        if c[0] >= 0 and c[1] >= 0 and c[0] < height and c[1] < width:
            neighbors.append((c[0], c[1], d, streak+1 if direction == d else 1))

    return neighbors

def getShortestPath(start, end, city, minstraight, maxstraight):
    queue = {}
    visited = set()

    distance = 0
    current = (start[0], start[1], None, distance)

    while not (((current[0], current[1]) == end) and current[3] >= minstraight):
        visited.add(current)
        for neighbor in getNeighbors((current[0], current[1]), current[2], current[3], minstraight, maxstraight):
            if neighbor not in visited:
                distanceN = distance + int(city[neighbor[0]][neighbor[1]])
                if distanceN not in queue: queue[distanceN] = set()
                queue[distanceN].add(neighbor)

        for i in range(distance, distance+10):
            if i in queue and len(queue[i]) > 0:
                distance = i
                current = queue[i].pop()
                break

    return distance

city = readFile("input.txt").splitlines()
height = len(city)
width = len(city[0])
endNode = (height-1, width-1)

print(f"Part 1: {getShortestPath((0, 0), endNode, city, 1, 3)}")
print(f"Part 2: {getShortestPath((0, 0), endNode, city, 4, 10)}")
