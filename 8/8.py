import os
import re
import sys
from math import lcm

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputContents = readFile("input.txt").splitlines()

instructions = inputContents[0]
instructions = list([*instructions])

network = {}
for node in inputContents[2:]:
    node = re.findall(r"^([^\s]+) = \(([^\s]+), ([^\s]+)\)$", node)[0]
    network[node[0]] = (node[1], node[2])

#########

instructionNumber = 0
position = "AAA"
stepCount = 0
while position != "ZZZ":
    if instructions[instructionNumber] == "L":
        position = network[position][0]
    else:
        position = network[position][1]

    if instructionNumber == len(instructions) - 1:
        instructionNumber = 0
    else:
        instructionNumber += 1

    stepCount += 1

print(f"Step count = {stepCount}")

#########

ghostNodes = [n for n in network.keys() if n[-1] == "A"]
instructionNumber = 0
ghostSteps = []

for node in ghostNodes:
    instructionNumber = 0
    position = node
    stepCount = 0
    while position[-1] != "Z":
        if instructions[instructionNumber] == "L":
            position = network[position][0]
        else:
            position = network[position][1]

        if instructionNumber == len(instructions) - 1:
            instructionNumber = 0
        else:
            instructionNumber += 1

        stepCount += 1
    ghostSteps.append(stepCount)

print(f"Ghost step count = {lcm(*ghostSteps)}")
