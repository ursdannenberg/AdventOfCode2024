from itertools import pairwise, product

#+---+---+---+
#| 7 | 8 | 9 |
#+---+---+---+
#| 4 | 5 | 6 |
#+---+---+---+
#| 1 | 2 | 3 |
#+---+---+---+
#    | 0 | A |
#    +---+---+
NUM_PAD = {"7": (0, 0), "8": (1, 0), "9": (2, 0), "4": (0, 1), "5": (1, 1), "6": (2, 1), "1": (0, 2), "2": (1, 2), "3": (2, 2), "0": (1, 3), "A": (2, 3)}

#    +---+---+
#    | ^ | A |
#+---+---+---+
#| < | v | > |
#+---+---+---+
DIR_PAD = {(0, -1): (1, 0), "A": (2, 0), (-1, 0): (0, 1), (0, 1): (1, 1), (1, 0): (2, 1)}

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
CACHE = {}

def _reader(filename):
    with open(filename, "r") as file:
        return tuple(doorcode.strip() for doorcode in file.readlines())

def _bfs(start, end, pad):
    queue = [(start, [])]
    visited = {start}
    paths = []
    while queue != []:
        position, path = queue.pop(0)
        if paths != [] and len(path) + 1 > len(paths[0]):
            break
        for dir in DIRS:
            move = tuple(p + d for p, d in zip(position, dir))
            if move == end:
                paths.append(path + [dir])
            if move in pad.values() and move not in path:
                queue.append((move, path + [dir]))
                visited.add(move)
    return paths

def _navigate_pad(code, pad):
    codes = []
    for first_key, second_key in pairwise(code):
        if first_key != second_key:
            first_key = pad[first_key]
            second_key = pad[second_key]
            if (first_key, second_key) not in CACHE:
                # Press "A" to push the button
                 CACHE[(first_key, second_key)] = [code + ["A"] for code in _bfs(first_key, second_key, pad)]
            codes = CACHE[(first_key, second_key)] if codes == [] else [co + ca for co, ca in product(codes, CACHE[(first_key, second_key)])]
        else:
            # Press "A" to push the button
            codes = [code + ["A"] for code in codes] 
    return codes
        
def solver(filename):
    doorcodes = _reader(filename)
    # Takes too long!
    for num_dir_pads in (2, 25):
        sum = 0
        for doorcode in doorcodes:
            # All robots initially aim at "A"
            more_codes = _navigate_pad("A" + doorcode, NUM_PAD)
            for i in range(num_dir_pads):
                codes = []
                for code in more_codes:
                    codes.extend(_navigate_pad(["A"] + code, DIR_PAD))
                min_length = min(len(code) for code in codes)
                more_codes = [code for code in codes if len(code) == min_length]
            sum += min(len(code) for code in more_codes) * int(doorcode.strip("A"))
        print(f"Part 1: {sum}" if num_dir_pads == 2 else f"Part 2: {sum}")