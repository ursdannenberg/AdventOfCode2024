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
        
def _bfs_1(start, direction, end, walls):
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    queue = [(0, start, direction)]
    parents = {}
    visited = {}
    while queue != []:
        queue = sorted(queue)
        score, position, direction = queue.pop(0)
        if position == end:
            return score
        if (position, direction) not in visited:
            visited[(position, direction)] = score
            parents[(position, direction)] = ()
            move = tuple(p + d for p, d in zip(position, dirs[direction]))
            if move not in walls:
                queue.append((score + 1, move, direction))
            right = 0 if direction + 1 == 4 else direction + 1
            queue.append((score + 1000, position, right))
            left = 3 if direction - 1 == -1 else direction - 1
            queue.append((score + 1000, position, left))
            
def _update_visited_parents_queue(daughter, parent, score, visited, parents, queue):
    if daughter not in visited or score < visited[daughter]:
        visited[daughter] = score
        parents[daughter] = [parent]
        queue.append((score, daughter[0], daughter[1]))
    elif score == visited[daughter]:
        parents[daughter].append(parent)
    return visited, parents, queue
    
def _path_finder(end, start, parents):
    tiles = {end[0]}
    queue = [end]
    while queue != []:
        position = queue.pop(0)
        if position == start:
            continue
        for parent in parents[position]:
            queue.append(parent)
            if parent[0] not in tiles:
                tiles.add(parent[0])
    return len(tiles)

def _bfs_2(start, direction, end, walls, low_score):
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    queue = [(0, start, direction)]
    parents = {}
    visited = {}
    while queue != []:
        queue = sorted(queue)
        score, position, direction = queue.pop(0)
        if position == end:
            continue
        if score + 1000 <= low_score:
            right = 0 if direction + 1 == 4 else direction + 1
            left = 3 if direction - 1 == -1 else direction - 1
            for dir in (right, left):
                visited, parents, queue = _update_visited_parents_queue((position, dir), (position, direction), score + 1000, visited, parents, queue)
        if score + 1 <= low_score:
            move = tuple(p + d for p, d in zip(position, dirs[direction]))
            if move not in walls:
                visited, parents, queue = _update_visited_parents_queue((move, direction), (position, direction), score + 1, visited, parents, queue)
    return _path_finder((end, direction), (start, 0), parents)
    
def solver(filename):
    start, end, walls = _reader(filename)
    score = _bfs_1(start, 0, end, walls)
    print(f"Part 1: {score}")
    print(f"Part 2: {_bfs_2(start, 0, end, walls, score)}")
    