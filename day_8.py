def _reader(filename: str) -> tuple[dict[int, list[tuple[int, int]]], int]:
    map = {}
    max_xy = 0
    with open(filename, "r") as file:
        for j, line in enumerate(file):
            max_xy += 1
            for i, char in enumerate(line):
                if char.isalnum():
                    if char in map:
                        map[char].append((i, j))
                    else:
                        map[char] = [(i, j)] 
    return map, max_xy - 1

def _antinode_locator(first: tuple[int, int], second: tuple[int, int], max_xy: int, part: int) -> set[tuple[int, int]]:
    if part == 1:
        antinodes = set(tuple(f + (f - s) for f, s in zip(fir, sec)) for fir, sec in ((first, second), (second, first)))
    else: 
        antinodes = set()
        for fir, sec in ((first, second), (second, first)):
            antinodes = antinodes | set(tuple(f + i * (f - s) for f, s in zip(fir, sec)) for i in range(max_xy))
    return set((x, y) for x, y in antinodes if 0 <= x <= max_xy and 0 <= y <= max_xy)

def solver(filename: str):
    map, max_xy = _reader(filename)
    antinodes = set()
    for part in (1, 2):
        for _, antennas in map.items():
            for i, first in enumerate(antennas):
                for second in antennas[i + 1:]:
                    antinodes = antinodes | _antinode_locator(first, second, max_xy, part)
        print(f"Part {part}: {len(antinodes)}")