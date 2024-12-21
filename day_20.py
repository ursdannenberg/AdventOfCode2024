DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))

def _reader(filename):
    walls = set()
    with open(filename, "r") as file:
        for j, line in enumerate(file):
            for i, char in enumerate(line.strip()):
                match char:
                    case "#":
                        walls.add((i, j))
                    case "S":
                        start = (i, j)
                    case "E":
                        end = (i, j)
    return start, end, walls
        
def _bfs_wo_cheat(start, end, walls):
    queue = [(start, {start: 0})]
    visited = {start}
    while queue != []:
        position, path = queue.pop(0)
        for dir in DIRS:
            move = tuple(p + d for p, d in zip(position, dir))
            if move == end:
                for key in path:
                    path[key] = path[position] + 1 - path[key]
                return path
            if move not in walls and move not in visited:
                path_move = path.copy()
                path_move[move] = path[position] + 1
                queue.append((move, path_move))
                visited.add(move)

def _bfs_w_cheat(start, end, time_cheat, path_wo_cheat, max_x, max_y):
    cheats = 0
    queue = [(start, 0)]
    while queue != []:
        position, steps = queue.pop(0)
        for dir in DIRS:
            move = tuple(p + d for p, d in zip(position, dir))
            if move == end:
                if steps + 1 <= path_wo_cheat[start] - 100:
                    cheats += 1
            else:
                if time_cheat - steps == 0:
                    if move in path_wo_cheat:
                        if steps + 1 + path_wo_cheat[move] <= path_wo_cheat[start] - 100:
                            cheats += 1
                else:
                    if 0 < move[0] < max_x and 0 < move[1] < max_y:
                        queue.append((move, steps + 1))
    return cheats
    

def solver(filename):
    start, end, walls = _reader(filename)
    path_wo_cheat = _bfs_wo_cheat(start, end, walls)
    max_x = max(x for x, _ in walls)
    max_y = max(y for _, y in walls)
    # Takes too long!
    for time_cheat in (1, 20):
        cheats = 0
        for i, position in enumerate(path_wo_cheat):
            print(i / len(path_wo_cheat))
            cheats += _bfs_w_cheat(position, end, time_cheat, path_wo_cheat, max_x, max_y)
        print(f"Part 1: {cheats}") if time_cheat == 1 else print(f"Part 2: {cheats}")