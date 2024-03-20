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

cardList = readFile("input.txt").splitlines()
cardNumRegex = re.compile(r"^Card +([0-9]+): .*")
winningNumRegex = re.compile(r"^Card +[0-9]+:([0-9 ]+) | .*$")
chosenNumRegex = re.compile(r"^Card +[0-9]+:[0-9 ]+ | ([0-9 ]+)$")

pointTotal = 0
for card in cardList:
    cardNumber = re.findall(cardNumRegex, card)[0]
    winningNums = list(filter(None, re.findall(winningNumRegex, card)[0].strip().split(" ")))
    chosenNums = list(filter(None, re.findall(chosenNumRegex, card)[1].strip().split(" ")))
    intersectionCount = len(list(set(winningNums) & set(chosenNums)))
    points = 2**(intersectionCount-1) if intersectionCount > 0 else 0
    pointTotal += points
print(f"Point total = {pointTotal}")

cardTotal = 0
cardCounts = {}
for card in cardList:
    cardNumber = int(re.findall(cardNumRegex, card)[0])
    cardCount = cardCounts[cardNumber] if cardNumber in cardCounts else 1
    cardTotal += cardCount

    winningNums = list(filter(None, re.findall(winningNumRegex, card)[0].strip().split(" ")))
    chosenNums = list(filter(None, re.findall(chosenNumRegex, card)[1].strip().split(" ")))
    intersectionCount = len(list(set(winningNums) & set(chosenNums)))

    for i in range(cardNumber+1, cardNumber+intersectionCount+1):
        iCount = cardCounts[i] if i in cardCounts else 1
        cardCounts[i] = iCount + cardCount
print(f"Card total = {cardTotal}")
