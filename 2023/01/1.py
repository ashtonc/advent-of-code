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

calibrationValues = readFile("input.txt")
calibrationSum = 0
calibrationRegex = re.compile(r"[0-9]")

for line in calibrationValues.splitlines():
    line = (line.replace("one", "one1one")
                .replace("two", "two2two")
                .replace("three", "three3three")
                .replace("four", "four4four")
                .replace("five", "five5five")
                .replace("six", "six6six")
                .replace("seven", "seven7seven")
                .replace("eight", "eight8eight")
                .replace("nine", "nine9nine"))

    numbers = re.findall(calibrationRegex, line)

    if len(numbers) < 1:
        sys.exit(f"ERROR: no numbers found in line '{line}'")
    else:
        calibrationValue = int(f"{numbers[0]}{numbers[-1]}")
        calibrationSum += calibrationValue

print(calibrationSum)
