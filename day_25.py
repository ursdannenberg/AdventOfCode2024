from itertools import product
def _parse_object(object):
    heights = [0] * 5
    if object.startswith("#####"):
        lines = object.split("\n")
    else:
        lines = object.split("\n")[::-1]
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                heights[i] = j
    return heights         

def _reader(filename):
    with open(filename, "r") as file:
        objects = file.read().split("\n\n")
    keys = ()
    locks = ()
    for object in objects:
        if object.startswith("#####"):
            locks = locks + (_parse_object(object),)
        else:
            keys = keys + (_parse_object(object),)
    return keys, locks

def solver(filename):
    keys, locks = _reader(filename)
    print(f"Part 1: {sum(all(k + l <= 5 for k, l in zip(key, lock)) for key, lock in product(keys, locks))}")