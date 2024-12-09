from pathlib import Path


def get_checksum(disk):
    checksum = 0
    for i, content in enumerate(disk):
        if content is None:
            continue
        checksum += i * content
    return checksum


def parse(path):
    with Path(path).open() as f:
        disk_map = map(int, f.read())
    ids = {}
    frees = set()
    disk_position = 0
    block_id = 0
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            for _ in range(c):
                ids[block_id] = {"start": disk_position, "length": c}
            disk_position += c
            block_id += 1
        else:
            for _ in range(c):
                frees.add(disk_position)
                disk_position += 1
    return ids, frees, disk_position


def p1(path):
    ids, frees, disk_size = parse(path)

    disk = []
    block_id = 0
    block_id_rev = max(ids.keys())

    disk_position = 0
    while disk_position < disk_size:
        if disk_position in frees:
            if block_id_rev <= 0:
                disk.append(None)
            else:
                if ids[block_id_rev]["length"] == 0:
                    block_id_rev -= 1
                if ids[block_id_rev]["length"] > 0:
                    disk.append(block_id_rev)
                    frees.add(ids[block_id_rev]["start"] + ids[block_id_rev]["length"])
                    ids[block_id_rev]["length"] += -1
            disk_position += 1
        elif block_id in ids:
            for _ in range(ids[block_id]["length"]):
                disk.append(block_id)
                disk_position += 1
            ids[block_id]["length"] = 0
            block_id += 1
        else:
            disk.append(None)
            disk_position += 1

    return get_checksum(disk)


def p2(path):
    ids, frees_arr, disk_size = parse(path)

    start = 0
    frees = {}
    for free in frees_arr:
        if start in frees and start + frees[start] == free:
            frees[start] += 1
        else:
            start = free
            frees[free] = 1

    for block_id in range(max(ids.keys()), -1, -1):
        for free_block in sorted(frees.keys()):
            if (
                frees[free_block] >= ids[block_id]["length"]
                and free_block < ids[block_id]["start"]
            ):
                ids[block_id]["start"] = free_block
                remaining_space = frees[free_block] - ids[block_id]["length"]
                if remaining_space > 0:
                    frees[free_block + ids[block_id]["length"]] = remaining_space
                del frees[free_block]
                break

    disk = [None] * disk_size
    for block_id in ids:
        for i in range(ids[block_id]["length"]):
            disk[ids[block_id]["start"] + i] = block_id

    return get_checksum(disk)


print("Example")
print(f"  Part 1: {p1('example.txt')}")
print(f"  Part 2: {p2('example.txt')}")

print("\nPuzzle Input")
print(f"  Part 1: {p1('input.txt')}")
print(f"  Part 2: {p2('input.txt')}")
