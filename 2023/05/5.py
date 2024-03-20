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

def findCorrespondingNum(number, refMap):
    output = None
    for ref in refMap:
        srcStart = ref[0]
        desStart = ref[1]
        rngLength = ref[2]
        if number >= desStart and number < desStart+rngLength:
            output = number + srcStart - desStart
    if not output:
        output = number
    return output

inputContents = readFile("input.txt").splitlines()
seedRegex = re.compile(r"^seeds: (.*)$")
mapRegex = re.compile(r"^(.*)-to-(.*) map:$")
numsRegex = re.compile(r"^([0-9]+) ([0-9]+) ([0-9]+)$")

seeds = list(map(int, re.findall(seedRegex, inputContents[0])[0].split()))
resultSum = 0
maps = {}
currentMap = ""

for line in inputContents[2:]:
    mapName = re.search(mapRegex, line)
    nums = re.search(numsRegex, line)
    if mapName is not None:
        currentMap = f"{mapName.group(1)}-{mapName.group(2)}"
        maps[currentMap] = []
    elif nums is not None:
        numList = list(map(int, nums.group().split()))
        maps[currentMap] += [numList]

minLocation = None
for seed in seeds:
    soil = findCorrespondingNum(seed, maps["seed-soil"])
    fertilizer = findCorrespondingNum(soil, maps["soil-fertilizer"])
    water = findCorrespondingNum(fertilizer, maps["fertilizer-water"])
    light = findCorrespondingNum(water, maps["water-light"])
    temperature = findCorrespondingNum(light, maps["light-temperature"])
    humidity = findCorrespondingNum(temperature, maps["temperature-humidity"])
    location = findCorrespondingNum(humidity, maps["humidity-location"])
    # print(f"Seed {seed}: {soil}, {fertilizer}, {water}, {light}, {temperature}, {humidity}, {location}")
    if not minLocation:
        minLocation = location
    else:
        if location < minLocation:
            minLocation = location

print(f"Min location = {minLocation}\n")

def getRangeIntersect(range1, range2):
    return range(max(range1[0], range2[0]), min(range1[-1], range2[-1])+1)

def findCorrespondingRanges(seedRanges, refMap):
    newRanges = []
    for seedRange in seedRanges:
        coveredRanges = []
        for ref in refMap:
            refRange = range(ref[1], ref[1]+ref[2])
            coveredRanges.append(refRange)
            if seedRange.start <= refRange.stop and refRange.start <= seedRange.stop:
                overlap = getRangeIntersect(seedRange, refRange)
                newRange = range(overlap.start + ref[0] - ref[1], overlap.stop + ref[0] - ref[1])
                newRanges.append(newRange)
        newRanges = mergeRanges(newRanges)
        coveredRanges = mergeRanges(coveredRanges)

        uncoveredRanges = []
        uncoveredRanges.append(seedRange)
        for coveredRange in coveredRanges:
            newUncoveredRanges = []
            for uncoveredRange in uncoveredRanges:
                if uncoveredRange.start >= coveredRange.start and uncoveredRange.stop <= coveredRange.stop:
                    pass
                elif uncoveredRange.start >= coveredRange.start and uncoveredRange.stop > coveredRange.stop:
                    newUncoveredRanges.append(range(max(uncoveredRange.start, coveredRange.stop), uncoveredRange.stop))
                elif uncoveredRange.start < coveredRange.start and uncoveredRange.stop <= coveredRange.stop:
                    newUncoveredRanges.append(range(uncoveredRange.start, min(coveredRange.start, uncoveredRange.stop)))
                elif uncoveredRange.start < coveredRange.start and uncoveredRange.stop > coveredRange.stop:
                    newUncoveredRanges.append(range(uncoveredRange.start, coveredRange.start))
                    newUncoveredRanges.append(range(coveredRange.stop, uncoveredRange.stop))
            uncoveredRanges = mergeRanges(newUncoveredRanges.copy())

        for uncoveredRange in uncoveredRanges:
            newRanges.append(uncoveredRange)

    return mergeRanges(newRanges)

def mergeRanges(rangeList):
    ranges_copy = sorted(rangeList.copy(), key=lambda x: x.stop)
    ranges_copy = sorted(ranges_copy, key=lambda x: x.start)
    merged_ranges = []

    while ranges_copy:
        range1 = ranges_copy[0]
        del ranges_copy[0]

        merges = []

        for i, range2 in enumerate(ranges_copy):
            if range1.start <= range2.stop and range2.start <= range1.stop:
                range1 = range(min([range1.start, range2.start]), max([range1.stop, range2.stop]))
                merges.append(i)

        merged_ranges.append(range1)
        for i in reversed(merges):
            del ranges_copy[i]

    return merged_ranges

seedPairs = [list(pair) for pair in zip(seeds[::2], seeds[1::2])]
seedRanges = []
for seedPair in seedPairs:
    seedRanges.append(range(seedPair[0], seedPair[0]+seedPair[1]))
seedRanges = mergeRanges(sorted(seedRanges, key=lambda r: r.start))

soilRanges = findCorrespondingRanges(seedRanges, maps["seed-soil"])
fertilizerRanges = findCorrespondingRanges(soilRanges, maps["soil-fertilizer"])
waterRanges = findCorrespondingRanges(fertilizerRanges, maps["fertilizer-water"])
lightRanges = findCorrespondingRanges(waterRanges, maps["water-light"])
temperatureRanges = findCorrespondingRanges(lightRanges, maps["light-temperature"])
humidityRanges = findCorrespondingRanges(temperatureRanges, maps["temperature-humidity"])
locationRanges = findCorrespondingRanges(humidityRanges, maps["humidity-location"])

print(f"Min location (seed ranges) = {locationRanges[0].start}")
