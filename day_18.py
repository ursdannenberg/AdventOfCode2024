def _reader(filename):
    with open(filename, "r") as file:
        return tuple(tuple(int(char) for char in line.strip().split(",")) for line in file)

def _bfs(bytes, number, max_x, max_y):
    bytes = set(bytes[:number])
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    queue = [((0, 0), 0)]
    visited = set()
    while queue != []:
        position, steps = queue.pop(0)
        for dir in dirs:
            move = tuple(p + d for p, d in zip(position, dir))
            if move == (max_x, max_y):
                return steps + 1
            if move not in bytes and move not in visited and 0 <= move[0] <= max_x and 0 <= move[1] <= max_y:
                queue.append((move, steps + 1))
                visited.add(move)

def solver(filename):
    bytes = _reader(filename)
    max_x = max_y = 70
    number = 1024
    print(f"Part 1: {_bfs(bytes, number, max_x, max_y)}")
    for num in range(number + 1, len(bytes)):
        if _bfs(bytes, num, max_x, max_y) is None:
            print(f"Part 2: {bytes[num - 1][0]},{bytes[num - 1][1]}")
            break
    