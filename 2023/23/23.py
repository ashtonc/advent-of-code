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

maze = readFile("input.txt").splitlines()
height = len(maze)
width = len(maze[0])
start = (0, 1)
end = (height-1, width-2)

def getNeighbors(y, x, p2=False):
	neighbors = []

	if   maze[y][x] == "^" and not p2: neighbors = [(y-1, x)]
	elif maze[y][x] == ">" and not p2: neighbors = [(y,   x+1)]
	elif maze[y][x] == "v" and not p2: neighbors = [(y+1, x)]
	elif maze[y][x] == "<" and not p2: neighbors = [(y,   x-1)]
	else:
		if y > 0:		neighbors.append((y-1, x))
		if x > 0:		neighbors.append((y,   x-1))
		if y < height-1: neighbors.append((y+1, x))
		if x < height-1: neighbors.append((y,   x+1))

	return [n for n in neighbors if maze[n[0]][n[1]] != "#"]

def getPaths(p2=False):
	paths = [[start]]
	complete = []

	while len(paths) != 0:
		path = paths.pop()
		current = path[-1]
		if current != end:
			for neighbor in [n for n in getNeighbors(*current, p2) if n not in path]:
				newPath = path.copy()
				newPath.append(neighbor)
				paths.append(newPath)
		else:
			complete.append(path)

	return complete

def getLongestPath(p2=False):
	nodes = {}
	queue = [start]

	while len(queue) != 0:
		current = queue.pop(0)
		nodes[current] = getNeighbors(*current, p2)
		for neighbor in [n for n in getNeighbors(*current, p2) if n not in nodes]:
			queue.append((neighbor))

	edges = {}
	for node in [n for n in nodes if len(nodes[n]) == 2]:
		n1 = nodes[node][0]
		n2 = nodes[node][1]

		if n1 not in edges: edges[n1] = {}
		if n2 not in edges: edges[n2] = {}

		lDistance = 0
		rDistance = 0
		if node in edges[n1]: lDistance += edges[n1][node]
		if node in edges[n2]: rDistance += edges[n2][node]

		edges[n1][n2] = lDistance + rDistance + 1
		edges[n2][n1] = lDistance + rDistance + 1

		nodes[n1].remove(node); nodes[n1].append(n2)
		nodes[n2].remove(node); nodes[n2].append(n1)

		if node in edges: del edges[node]
		del nodes[node]

	paths = [[start]]
	longest = []
	weight = 0
	while len(paths) != 0:
		path = paths.pop()
		current = path[-1]
		if current != end:
			for neighbor in [n for n in nodes[current] if n not in path]:
				newPath = path.copy()
				newPath.append(neighbor)
				paths.append(newPath)
		else:
			pathSize = 0
			for i, junction in enumerate(path[:-1]):
				pathSize += edges[junction][path[i+1]] + 1
			if pathSize > weight:
				longest = path
				weight = pathSize

	complete = []
	paths = [[start]]
	while len(paths) != 0:
		path = paths.pop()
		current = path[-1]
		if current != end:
			if current in longest:
				target = longest[longest.index(current)+1]
			for neighbor in [n for n in getNeighbors(*current, p2) if n not in path]:
				if neighbor not in longest or neighbor == target:
					newPath = path.copy()
					newPath.append(neighbor)
					paths.append(newPath)
		else:
			complete.append(path)

	return complete[0]

print("Part 1:", max(map(len, getPaths()))-1)
print("Part 2:", len(getLongestPath(p2=True))-1)

