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

totalEndValueSum = 0
totalStartValueSum = 0
for line in inputContents:
    values = list(map(int, line.split()))

    endValues = []
    endValues.append(values[-1])

    startValues = []
    startValues.append(values[0])

    endValues.append(values[-1])
    remaining = 1
    while remaining != 0:
        newValues = []
        for i, value in enumerate(values[:-1]):
            newValues.append(values[i+1]-value)
        
        remaining = len([n for n in newValues if n != 0])
        endValues.append(newValues[-1])
        startValues.append(newValues[0])

        values = newValues

    firstEndValue = sum(endValues)
    totalEndValueSum += firstEndValue

    firstStartValue = startValues[-1]
    for sValue in reversed(startValues[:-1]):
        firstStartValue = sValue - firstStartValue

    totalStartValueSum += firstStartValue

print("End value total =", totalEndValueSum)
print("Start value total =", totalStartValueSum)
