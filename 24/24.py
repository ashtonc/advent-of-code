import os
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

def getXYIntercept(h1, h2):
	def getPoints(h):
		return ((h[0][0], h[0][1]), (h[0][0] + h[1][0], h[0][1] + h[1][1]))
 
	def getLine(p1, p2):
		A = p1[1] - p2[1]
		B = p2[0] - p1[0]
		C = (p1[0] * p2[1]) - (p2[0] * p1[1])
		return (A, B, -C)

	def getIntersect(l1, l2):
		D  = l1[0] * l2[1] - l1[1] * l2[0]
		if D != 0:
			Dx = l1[2] * l2[1] - l1[1] * l2[2]
			Dy = l1[0] * l2[2] - l1[2] * l2[0]
			return (Dx / D, Dy / D)
		else:
			return None

	return getIntersect(getLine(*getPoints(h1)), getLine(*getPoints(h2)))

def isFuture(h1, h2, intercept):
	x1 = ((intercept[0] - h1[0][0]) * h1[1][0]) >= 0
	x2 = ((intercept[0] - h2[0][0]) * h2[1][0]) >= 0
	y1 = ((intercept[1] - h1[0][1]) * h1[1][1]) >= 0
	y2 = ((intercept[1] - h2[0][1]) * h2[1][1]) >= 0
	return all((x1, x2, y1, y2))

hailstones = []
for h in readFile("input.txt").splitlines():
	hailstones.append(tuple([tuple(map(int, x.split(", "))) for x in h.split(" @ ")]))

areaMin = 200000000000000
areaMax = 400000000000000
checked = set()
insideCount = 0
for h1 in hailstones:
	checked.add(h1)
	for h2 in [h for h in hailstones if h not in checked]:
		intercept = getXYIntercept(h1, h2)
		if (intercept != None and
		    areaMin <= intercept[0] <= areaMax and areaMin <= intercept[1] <= areaMax and
		    isFuture(h1, h2, intercept)):
			insideCount += 1

print("Part 1:", insideCount)

import z3

hail = [[int(i) for i in l.replace('@',',').split(',')]
                for l in open('input.txt')]

rock = z3.RealVector('r', 6)
time = z3.RealVector('t', 3)

s = z3.Solver()
s.add(*[rock[d] + rock[d+3] * t == hail[d] + hail[d+3] * t
        for t, hail in zip(time, hail) for d in range(3)])
s.check()

print("Part 2:", s.model().eval(sum(rock[:3])))

