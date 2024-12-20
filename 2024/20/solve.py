from heapq import heappop, heappush
from pathlib import Path


def neighbors(x, y, width, height, d=1):
    return {
        (nx, ny)
        for dx in range(-d, d + 1)
        for ny in (y + (d - abs(dx)), y - (d - abs(dx)))
        for nx in [x + dx]
        if 0 <= nx < width and 0 <= ny < height
    }


def get_scores(track, start, width, height):
    scores = {start: 0}
    pqueue = [(0, start)]
    while pqueue:
        score, current = heappop(pqueue)
        for neighbor in neighbors(*current, width, height):
            if track[neighbor] != "#":
                new_score = score + 1
                if neighbor not in scores or new_score < scores[neighbor]:
                    scores[neighbor] = new_score
                    heappush(pqueue, (new_score, neighbor))
    return scores


def parse(path):
    with Path(path).open() as f:
        grid = f.read().splitlines()
    height, width = len(grid), len(grid[0])
    track = {(x, y): char for y, row in enumerate(grid) for x, char in enumerate(row)}
    start = next(pos for pos, char in track.items() if char == "S")
    end = next(pos for pos, char in track.items() if char == "E")
    return track, width, height, start, end


def p1(path, threshold):
    track, width, height, start, end = parse(path)
    sscores = get_scores(track, start, width, height)
    escores = get_scores(track, end, width, height)
    return sum(
        1
        for pos, char in track.items()
        if char != "#"
        for neighbor in neighbors(*pos, width, height, 2)
        if neighbor in escores
        and sscores[pos] + escores[neighbor] + 2 <= sscores[end] - threshold
    )


def p2(path, threshold):
    track, width, height, start, end = parse(path)
    sscores = get_scores(track, start, width, height)
    escores = get_scores(track, end, width, height)
    return sum(
        1
        for pos, char in track.items()
        if char != "#"
        for cheat in range(21)
        for neighbor in neighbors(*pos, width, height, cheat)
        if neighbor in escores
        and sscores[pos] + escores[neighbor] + cheat <= sscores[end] - threshold
    )


print("Example")
print(f"  Part 1: {p1('example.txt', threshold=1)}")
print(f"  Part 2: {p2('example.txt', threshold=50)}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt', threshold=100)}")
print(f"  Part 2: {p2('input.txt', threshold=100)}")
