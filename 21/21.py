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

def init(start=None):
    if start == None:
        for i in range(height):
            for j in range(width):
                if garden[i][j] == "S":
                    start = (i, j) # y, x
    return {start: {"even": 0}} # minimum even/odd steps

def getNeighbors(y, x, garden):
    neighbors = []
    if y > 0: neighbors.append((y-1, x))
    if x > 0: neighbors.append((y, x-1))
    if y < height-1: neighbors.append((y+1, x))
    if x < height-1: neighbors.append((y, x+1))
    return [n for n in neighbors if garden[n[0]%height][n[1]%width] != "#"]

def explore(steps, count):
    for i in range(count):
        isEven = i % 2 == 0
        checkPlots = steps.copy().keys()
        for plot in checkPlots:
            for neighbor in getNeighbors(*plot, garden):
                if neighbor not in steps:
                    steps[neighbor] = {}
                if not isEven and "odd" in steps[plot] and "even" not in steps[neighbor]:
                    steps[neighbor]["even"] = i+1
                if isEven and "even" in steps[plot] and "odd" not in steps[neighbor]:
                    steps[neighbor]["odd"] = i+1
        for plot in checkPlots:
            for neighbor in getNeighbors(*plot, garden):
                if "even" not in steps[plot] and "odd" in steps[neighbor]:
                    steps[plot]["even"] = steps[neighbor]["odd"]+1
                if "odd" not in steps[plot] and "even" in steps[neighbor]:
                    steps[plot]["odd"] = steps[neighbor]["even"]+1
    return

def getReachablePlots(garden, count=1, start=None):
    steps = init(start)
    explore(steps, min(height, count)) # not generally applicable

    if count > ((height-1)/2):
        assert width == height # assumed
        plots = (count - ((width-1)/2)) / width; assert plots % 1 == 0 # assumed

        evenCorners = (plots + (plots % 2))
        oddCorners = (plots + ((plots + 1) % 2))
        evenPlots = evenCorners ** 2
        oddPlots = oddCorners ** 2

        reachableCornerEven = len([p for p in steps.values() if "even" in p and p["even"]>((height-1)/2)])
        reachableCornerOdd = len([p for p in steps.values() if "odd" in p and p["odd"]>((height-1)/2)])
        reachableFullEven = len([p for p in steps.values() if "even" in p])
        reachableFullOdd = len([p for p in steps.values() if "odd" in p])

        return int(sum([(evenPlots * reachableFullEven),
                        (oddPlots * reachableFullOdd),
                        (evenCorners * reachableCornerEven * (1 if plots % 2 == 0 else -1)),
                        (oddCorners * reachableCornerOdd * (1 if plots % 2 == 1 else -1))]))

    minY = max(0, min([k[0] for k in steps.keys()]))
    minX = max(0, min([k[1] for k in steps.keys()]))
    maxY = min(height-1, max([k[0] for k in steps.keys()]))
    maxX = min(width-1, max([k[1] for k in steps.keys()]))

    reachable = 0
    for i in range(minY, maxY+1):
        for j in range(minX, maxX+1):
            cell = (i, j)
            if cell in steps and ("even" if count % 2 == 0 else "odd") in steps[cell]:
                if p: print("O", end="")
                reachable += 1
            else:
                if p: print(garden[i%height][j%width], end="")
        if p: print()
    return reachable

garden = readFile("input.txt").splitlines()
height = len(garden)
width = len(garden[0])
p = False # print reachable steps

print(f"Part 1: {getReachablePlots(garden, 64)}")
print(f"Part 2: {getReachablePlots(garden, 26501365)}")
