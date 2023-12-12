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

inputContents = readFile("input.txt").splitlines()

springArray = []
springArray2 = []
for line in inputContents:
    inputs = line.split()
    springArray.append((inputs[0]+".", [int(x) for x in inputs[1].split(",")]))
    springArray2.append(("?".join([inputs[0]]*5)+".", [int(x) for x in inputs[1].split(",")]*5))

def testMatch(spring):
    regex = r"\.*"
    for i, group in enumerate(spring[1]):
        regex += r"#" * group
        if i < len(spring[1]) - 1:
            regex += r"\.+"
        else:
            regex += r"\.*"
    return re.match(regex, spring[0]) != None

mcache = {}
def solveSpring(condition, groups, currentGroupSize=0):
    if (condition, tuple(groups), currentGroupSize) in mcache:
        return mcache[(condition, tuple(groups), currentGroupSize)]

    if len(condition) == 0:
        if len(groups) == 0 and currentGroupSize == 0:
            return 1
        else:
            return 0

    if condition[0] == "#":
        testChars = ["#"]
    elif condition[0] == ".":
        testChars = ["."]
    else:
        testChars = ["#", "."]

    arrangementCount = 0
    for c in testChars:
        if c == "#":
            arrangementCount += solveSpring(condition[1:], groups, currentGroupSize + 1)
        else:
            if currentGroupSize > 0:
                if len(groups) > 0 and currentGroupSize == groups[0]:
                    arrangementCount += solveSpring(condition[1:], groups[1:], 0)
                else:
                    arrangementCount += 0
            else:
                arrangementCount += solveSpring(condition[1:], groups, 0)

    mcache[(condition, tuple(groups), currentGroupSize)] = arrangementCount
    return arrangementCount

def countArrangements(springArray):
    totalArrangementCount = 0
    for spring in springArray:
        # print(spring[0], "-", spring[1], "-", solveSpring(spring[0], spring[1]))
        totalArrangementCount += solveSpring(spring[0], spring[1])
    return totalArrangementCount

print(f"Total arrangements: {countArrangements(springArray)}")
print(f"Total arrangements (unfolded): {countArrangements(springArray2)}")
