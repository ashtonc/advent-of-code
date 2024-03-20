import os
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

def init(inFile):
	modules = {}
	for module in readFile("input.txt").splitlines():
		m = module.split(" -> ")
		mType = m[0][0]
		mName = m[0][1:] if mType in ["%", "&"] else m[0]
		mDestinations = m[1].split(", ")

		modules[mName] = {"type": mType, "destinations": mDestinations}
		if mType == "%": modules[mName]["on"] = False
		if mType == "&": modules[mName]["received"] = {}

	rxInput = ""
	for module in modules:
		for d in modules[module]["destinations"]:
			if d in modules and modules[d]["type"] == "&":
					modules[d]["received"][module] = 0
			if d == "rx":
				rxInput = module

	for module in modules:
		for d in modules[module]["destinations"]:
			if d == rxInput:
				rxInputs[module] = 0

	return modules

def pressButton(count=1):
	high = 0
	low = 0
	for i in range(count):
		global presses
		presses += 1

		pulseQueue = []
		pulseQueue.append(("broadcaster", 0, "button")) # destination, low = 0 high = 1, source
		while pulseQueue != []:
			pulse = pulseQueue.pop(0)
			# print(pulse[2], "to", pulse[0], "[low]" if pulse[1] == 0 else "[high]")

			if pulse[1] == 0: low += 1
			elif pulse[1] == 1: high += 1

			if pulse[0] not in modules:
				pass
			elif modules[pulse[0]]["type"] == "b":
				for d in modules[pulse[0]]["destinations"]:
					pulseQueue.append((d, pulse[1], pulse[0]))
				pass
			elif modules[pulse[0]]["type"] == "%":
				if not pulse[1]:
					if modules[pulse[0]]["on"]:
						for d in modules[pulse[0]]["destinations"]: pulseQueue.append((d, 0, pulse[0]))
					else:
						for d in modules[pulse[0]]["destinations"]: pulseQueue.append((d, 1, pulse[0]))
					modules[pulse[0]]["on"] = not modules[pulse[0]]["on"]
			elif modules[pulse[0]]["type"] == "&":
				modules[pulse[0]]["received"][pulse[2]] = pulse[1]
				if all(x==1 for x in modules[pulse[0]]["received"].values()):
					for d in modules[pulse[0]]["destinations"]: pulseQueue.append((d, 0, pulse[0]))
				else:
					for d in modules[pulse[0]]["destinations"]: pulseQueue.append((d, 1, pulse[0]))

			if pulse[0] in rxInputs and pulse[1] == 0:
				if rxInputs[pulse[0]] == 0:
					rxInputs[pulse[0]] = presses

	return low, high

presses = 0
rxInputs = {}
modules = init("input.txt")

print(f"Part 1: {(lambda x: x[0]*x[1])(pressButton(1000))}")

while any(x==0 for x in rxInputs.values()): pressButton()
print(f"Part 2: {lcm(*tuple(rxInputs.values()))} (found after {presses} clicks)")

