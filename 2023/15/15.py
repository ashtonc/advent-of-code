import os
import sys
import re
from functools import cache

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputContents = readFile("input.txt")

def getHash(sequence):
    a = 0
    for c in sequence:
        a = ((a + ord(c)) * 17) % 256
    return a

print(f"Part 1: {sum(map(getHash, inputContents.split(',')))}")

boxes = {}
for sequence in inputContents.split(','):
    if "=" in sequence:
        label = sequence.split("=")[0]
        box = getHash(label)
        focalLength = sequence.split("=")[1]

        if box not in boxes:
            boxes[box] = []

        if label not in [b[0] for b in boxes[box]]:
            boxes[box].append((label, focalLength))
        else:
            boxes[box][[b[0] for b in boxes[box]].index(label)] = (label, focalLength)

    elif "-" in sequence:
        label = sequence.split("-")[0]
        box = getHash(label)
        if box in boxes:
            remove = [b for b in boxes[box] if label == b[0]]
            for i in range(len(remove)):
                boxes[box].remove(remove[i])

tfp = 0
for box in boxes:
    for i, lens in enumerate(boxes[box]):
        focusPower = (box+1) * (i+1) * int(lens[1])
        tfp += focusPower

print(f"Part 2: {tfp}")
