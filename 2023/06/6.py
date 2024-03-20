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

times = list(map(int, re.findall(r"^Time: (.*)$", inputContents[0])[0].split()))
records = list(map(int, re.findall(r"^Distance: (.*)$", inputContents[1])[0].split()))
races = [(pair) for pair in zip(times, records)]

recordMultiple = 1
for race in races:
    time = race[0]
    record = race[1]

    recordCount = 0
    for i in range(1, time):
        distance = i * (time - i)
        if distance > record:
            recordCount += 1

    recordMultiple = recordMultiple * recordCount

print(f"Record multiple: {recordMultiple}")
