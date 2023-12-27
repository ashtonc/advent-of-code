import os
import sys
import random

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

def getSetSize(start):
    visited = set()
    queue = [start]
    while len(queue) != 0:
        current = queue.pop(0)
        visited.add(current)
        for neighbor in components[current]:
            if neighbor not in visited:
                queue.append(neighbor)
    return len(visited)

def getSetSizeTest(toDelete):
    goal = getSetSize([c for c in components][0])
    for connection in toDelete:
        components[connection[0]].remove(connection[1])
        components[connection[1]].remove(connection[0])

    sideAsize = getSetSize(toDelete[0][0])
    sideBsize = getSetSize(toDelete[0][1])

    for connection in toDelete:
        components[connection[0]].add(connection[1])
        components[connection[1]].add(connection[0])

    return goal, sideAsize, sideBsize

def getShortestPath(start, end):
    distance = 0
    current = start

    visited = set()
    distances = {}

    while current != end:
        visited.add(current)
        distances[current] = distance

        for neighbor in components[current]:
            if neighbor not in visited:
                distances[neighbor] = distance + 1
            else:
                distances[neighbor] = min(distances[neighbor], distance + 1)

        distance = min([distances[n] for n in distances if n not in visited])
        nextNodes = [n for n, v in distances.items() if n not in visited if v == distance]
        
        if end in nextNodes:
            current = end
        else:
            current = nextNodes[0]

    path = [end]
    distance = distances[end]
    while distance > 0:
        current = path[-1]
        distance = distance - 1
        path.append([n for n in components[current] if n in distances and distances[n] == distance][0])

    connections = []
    for i in range(len(path)-1):
        connections.append(tuple(sorted((path[i], path[i+1]))))

    return connections

components = {}
for component in readFile("input.txt").splitlines():
    name = component.split(": ")[0]
    connections = set(component.split(": ")[1].split())
    if name not in components:
        components[name] = connections
    else:
        for connection in connections:
            components[name].add(connection)
    for connection in connections:
        if connection not in components:
            components[connection] = set([name])
        else:
            components[connection].add(name)

connectionCount = {}
checked = set()
todo = []
for c1 in components:
    checked.add(c1)
    for c2 in [c for c in components if c not in checked]:
        todo.append(tuple(sorted((c1, c2))))

random.shuffle(todo)
for i, connection in enumerate(todo):
    for c in getShortestPath(*connection):
        if c not in connectionCount:
            connectionCount[c] = 1
        else:
            connectionCount[c] += 1

    if i > 1 and i % 50 == 0:
        sizes = getSetSizeTest(sorted(connectionCount, key=connectionCount.get, reverse=True)[0:3])
        if sizes[1] + sizes[2] == sizes[0]:
            print("Part 1:", sizes[1]*sizes[2])
            break
