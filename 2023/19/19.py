import os
import re
import sys
from time import sleep

def readFile(path):
    if not os.path.exists(path):
        sys.exit(f"ERROR: '{path}' not found")
    with open(path, "r", encoding="utf-8") as file:
        try:
            return file.read()
        except:
            sys.exit(f"ERROR: could not read '{path}'")

inputContents = readFile("input.txt").split("\n\n")
workflowInput = inputContents[0].splitlines()
partInput = inputContents[1].splitlines()

workflows = {}
for workflow in workflowInput:
    parsedWorkflow = re.findall(r"([a-z]+)\{([^\}]+)\}", workflow)
    workflows[parsedWorkflow[0][0]] = parsedWorkflow[0][1].split(",")

parts = []
for part in partInput:
    newPart = {}
    for value in part[1:-1].split(","):
        newPart[value[0]] = int(value[2:])
    parts.append(newPart)

def applyWorkflows(part):
    wf = "in"
    while 1:
        for rule in workflows[wf]:
            if ":" not in rule:
                wf = rule
            else:
                condition = rule.split(":")[0]
                if eval(f"{part[rule[0]]}{condition[1]}{condition[2:]}"):
                    wf = rule.split(":")[1]
                    break
        if wf in ["A", "R"]:
            return wf == "A"

def getRatingSum(part):
    if applyWorkflows(part): return sum(part.values())
    return 0

def getDistinctCombinations(minrating=1, maxrating=4000):
    acceptedCombos = []
    stack = [{"xmin": minrating, "xmax": maxrating
             ,"mmin": minrating, "mmax": maxrating
             ,"amin": minrating, "amax": maxrating
             ,"smin": minrating, "smax": maxrating}]
    while len(stack) != 0:
        wf = "in"
        comboSet = stack.pop()
        while 1:
            for rule in workflows[wf]:
                if ":" not in rule:
                    wf = rule
                else:
                    condition = rule.split(":")[0]
                    value = int(condition[2:])

                    testMin = eval(f"{comboSet[rule[0] + 'min']}{condition[1]}{value}")
                    testMax = eval(f"{comboSet[rule[0] + 'max']}{condition[1]}{value}")

                    if testMin and testMax:
                        wf = rule.split(":")[1]
                        break
                    elif not testMin and not testMax:
                        pass
                    else:
                        comboSetP = comboSet.copy()
                        if testMin:
                            comboSet[rule[0] + "max"] = value - 1
                            comboSetP[rule[0] + "min"] = value
                        elif testMax:
                            comboSet[rule[0] + "min"] = value + 1
                            comboSetP[rule[0] + "max"] = value
                        stack.append(comboSetP)
                        wf = rule.split(":")[1]
                        break

            if wf == "A": acceptedCombos.append(comboSet)
            if wf in ["A", "R"]: break

    return acceptedCombos

def getCombinationSum(combination):
    combinationSum = 1
    for c in ["x", "m", "a", "s"]:
        combinationSum *= combination[c+"max"] - combination[c+"min"] + 1
    return combinationSum

print(f"Part 1: {sum(map(getRatingSum, parts))}")
print(f"Part 2: {sum(map(getCombinationSum, getDistinctCombinations()))}")
