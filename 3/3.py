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

engineSchematic = readFile("input.txt").splitlines()
partRegex = re.compile(r"[0-9]+")
symbolRegex = re.compile(r"[^\.0-9]")
gearRegex = re.compile(r"[*]")

partSum = 0
for i, line in enumerate(engineSchematic):
    for match in re.finditer(partRegex, line):
        partNumber = int(match.group(0))
        for r in range(max(0, i-1), min(len(engineSchematic), i+2)):
            for c in range(max(0, match.span()[0]-1), min(len(line), match.span()[1]+1)):
                if re.search(symbolRegex, engineSchematic[r][c]) is not None:
                    partSum += partNumber
                    break
        else:
            continue
        break
print(f"Part sum = {partSum}")

gearRatioSum = 0
for i, line in enumerate(engineSchematic):
    for gear in re.finditer(gearRegex, line):
        associatedParts = []
        overlapRange = range(max(0, gear.span()[0]-1), min(len(line), gear.span()[1]+1))
        for r in range(max(0, i-1), min(len(engineSchematic), i+2)):
            for part in re.finditer(partRegex, engineSchematic[r]):
                partNumber = int(part.group(0))
                partRange = range(max(0, part.span()[0]), min(len(line), part.span()[1]))
                if len(list(range(max(overlapRange[0], partRange[0]), min(overlapRange[-1], partRange[-1])+1))) > 0:
                    associatedParts += [partNumber]
        if len(associatedParts) == 2:
            gearRatioSum += associatedParts[0] * associatedParts[1]
print(f"Gear ratio sum = {gearRatioSum}")
