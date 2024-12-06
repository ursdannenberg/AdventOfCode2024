from itertools import cycle

def _reader(filename: str) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    with open(filename, "r") as file:
        lines = file.readlines()
    obstacles = [(i, j) for j, line in enumerate(lines) for i, char in enumerate(line) if char == "#"]
    guard = [(i, j) for j, line in enumerate(lines) for i, char in enumerate(line) if char == "^"][0]
    max_x = max([x for x, _ in obstacles])
    max_y = max([y for _, y in obstacles])
    return obstacles, guard, max_x, max_y

def _mover(obstacles : list[tuple[int, int]], guard: tuple[int, int], max_x: int, max_y: int) -> set:
    visited = ()
    directions = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])
    direction = next(directions)
    while 0 <= guard[0] <= max_x and 0 <= guard[1] <= max_y:
        if (guard, direction) in visited:
            return set()
        else:
            visited += ((guard, direction),)
        new_guard = tuple(g + d for g, d in zip(guard, direction))
        if new_guard in obstacles:
            direction = next(directions)
        else:
            guard = new_guard
    return set(guard for guard, _ in visited)
        

def solver(filename: str) -> None:
    obstacles, guard, max_x, max_y = _reader(filename)
    visited = _mover(obstacles, guard, max_x, max_y)
    print(f"Part 1: {len(visited)}") 
    # Slow!
    sum = 0
    for obstacle in (obstacle for obstacle in visited if obstacle != guard):
        if _mover(obstacles + [obstacle], guard, max_x, max_y) == set():
            sum += 1
    print(f"Part 2: {sum}")