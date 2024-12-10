def _reader(filename: str) -> tuple[dict[tuple[int, int], int], tuple[int, ...], int, int]:
    with open(filename, "r") as file:
        lines = file.readlines()
    max_y = len(lines) - 1
    max_x = len(lines[0].strip()) - 1
    map = {(i, j): int(char) for j, line in enumerate(lines) for i, char in enumerate(line.strip())}
    starts = tuple(key for key, value in map.items() if value == 0)
    return map, starts, max_x, max_y

def _path_finder(heights: dict[tuple[int, int], int], starts: tuple[int, ...], max_x: int, max_y: int, dirs: tuple[tuple[int, int], ...]) -> int:
    ends = ()
    for start in starts:
        tops = ()
        positions = ((start, 0),)
        while positions != ():
            new_positions = ()
            for position, height in positions:
                for dir in dirs:
                    new = tuple(p + d for p, d in zip(position, dir))
                    if not 0 <= new[0] <= max_x or not 0 <= new[1] <= max_y:
                        continue
                    if heights[new] == height + 1:
                        if height + 1 == 9:
                            tops += (new,)
                        else:
                            new_positions += ((new, height + 1),)
            positions = new_positions
        ends += (tops,)
    return ends

def solver(filename : str) -> None:
    heights, starts, max_x, max_y = _reader(filename)
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    ends = _path_finder(heights, starts, max_x, max_y, dirs)
    print(f"Part 1: {sum(len(set(tops)) for tops in ends)}")
    print(f"Part 2: {sum(len(tops) for tops in ends)}")