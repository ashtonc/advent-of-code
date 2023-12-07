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

def rankCard(card):
    match card:
        case "A": return 14
        case "K": return 13
        case "Q": return 12
        case "J": return 11
        case "T": return 10
        case _:   return int(card)

def getType(hand):
    hand = list(map(rankCard, [*hand]))
    counts = {}
    for i in range(2,15):
        c = hand.count(i)
        if c > 0:
            counts[i] = c

    if len(counts) == 5: return 0  # High card

    maxV = 0
    for i, (c, v) in enumerate(counts.items()):
        if v == 5:                                    return 6  # Five of a kind
        if v == 4:                                    return 5  # Four of a kind
        if v == 3 and len(counts) == 2:               return 4  # Full house
        if v == 3 and len(counts) == 3:               return 3  # Three of a kind
        if v == 2 and len(counts) == 3 and maxV == 2: return 2  # Two pair
        if v == 2 and len(counts) == 4:               return 1  # One pair
        if v > maxV: maxV = v

def rankHand(hand):
    handScore = (getType(hand)     * 10000000000) \
              + (rankCard(hand[0]) * 100000000) \
              + (rankCard(hand[1]) * 1000000) \
              + (rankCard(hand[2]) * 10000) \
              + (rankCard(hand[3]) * 100) \
              + (rankCard(hand[4]) * 1)
    return handScore


lines = readFile("input.txt").splitlines()

scoredHands = []
for line in lines:
    hand = line.split()[0]
    score = int(line.split()[1])
    scoredHands.append((rankHand(hand), score, hand))

scoredHands = sorted(scoredHands, key=lambda x: x[0])

totalScore = 0
for i, h in enumerate(scoredHands):
    totalScore += ((i + 1) * h[1])

print(f"Total score = {totalScore}")

#############

def rankCardNew(card):
    match card:
        case "A": return 14
        case "K": return 13
        case "Q": return 12
        case "J": return 1
        case "T": return 10
        case _:   return int(card)

def getTypeNew(hand):
    hand = list(map(rankCardNew, [*hand]))
    counts = {}
    for i in range(1,15):
        c = hand.count(i)
        if c > 0:
            counts[i] = c

    if 1 in counts:
        jokerCount = counts[1]
        del counts[1]
    else:
        jokerCount = 0

    if len(counts) == 5: return 0  # High card
    if len(counts) == 0: return 6  # Five of a kind
    if len(counts) == 1: return 6  # Five of a kind

    counts[max(counts, key=counts.get)] += jokerCount

    maxV = 0
    for i, (c, v) in enumerate(counts.items()):
        if v == 5:                                    return 6  # Five of a kind
        if v == 4:                                    return 5  # Four of a kind
        if v == 3 and len(counts) == 2:               return 4  # Full house
        if v == 3 and len(counts) == 3:               return 3  # Three of a kind
        if v == 2 and len(counts) == 3 and maxV == 2: return 2  # Two pair
        if v == 2 and len(counts) == 4:               return 1  # One pair
        if v > maxV: maxV = v

def rankHandNew(hand):
    handScore = (getTypeNew(hand)     * 10000000000) \
              + (rankCardNew(hand[0]) * 100000000) \
              + (rankCardNew(hand[1]) * 1000000) \
              + (rankCardNew(hand[2]) * 10000) \
              + (rankCardNew(hand[3]) * 100) \
              + (rankCardNew(hand[4]) * 1)
    return handScore

scoredHands = []
for line in lines:
    hand = line.split()[0]
    score = int(line.split()[1])
    handRank = rankHandNew(hand)
    scoredHands.append((handRank, score, hand))

scoredHands = sorted(scoredHands, key=lambda x: x[0])

totalScore = 0
for i, h in enumerate(scoredHands):
    totalScore += ((i + 1) * h[1])

print(f"Total score (jokers) = {totalScore}")
