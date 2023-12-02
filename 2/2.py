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

gamesRecord = readFile("input.txt")
gamesRegex = re.compile(r"^Game ([0-9]+): (.*)")

idSum = 0
powerSum = 0

for game in gamesRecord.splitlines():
    gameParts = re.findall(gamesRegex, game)
    gameID = int(gameParts[0][0])
    gameList = gameParts[0][1].split("; ")

    minRed = 0
    minGreen = 0
    minBlue = 0

    for record in gameList:
        redMatch = re.findall(r"([0-9]+) red", record)
        greenMatch = re.findall(r"([0-9]+) green", record)
        blueMatch = re.findall(r"([0-9]+) blue", record)

        redCount = int(redMatch[0]) if len(redMatch) == 1 else 0
        greenCount = int(greenMatch[0]) if len(greenMatch) == 1 else 0
        blueCount = int(blueMatch[0]) if len(blueMatch) == 1 else 0

        if redCount > minRed: minRed = redCount
        if greenCount > minGreen: minGreen = greenCount
        if blueCount > minBlue: minBlue = blueCount

    print(f"{gameID} = Red: {minRed}, Green: {minGreen}, Blue: {minBlue}") 

    if minRed <= 12 and minGreen <= 13 and minBlue <= 14:
        idSum += gameID

    powerSum += (minRed * minGreen * minBlue)

print(f"Sum = {idSum}")
print(f"Power = {powerSum}")