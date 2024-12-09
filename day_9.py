def _reader(filename: str) -> tuple[list[int], tuple[int, ...]]:
    with open(filename, "r") as file:
        input = file.readline().strip()
    files = [i for i, char in enumerate(input[::2]) for _ in range(int(char))]
    spaces = tuple(int(char) for char in input[1::2])
    return files, spaces

def _remover(files: list[int], number: int):
    while number in files:
        files.remove(number)
    return files 

def _space_filler_1(compacted : list[int], uncompacted: list[int], space: int): 
    compacted.extend(uncompacted[-space:][::-1])
    del uncompacted[-space:]
    return compacted, uncompacted

def _space_filler_2(compacted : list[int], uncompacted: list[int], space: int):
    last = uncompacted[-1]
    while space > 0 and last >= min(uncompacted):
        files = [last] * uncompacted.count(last)
        if len(files) <= space:
            compacted.extend(files)
            uncompacted = _remover(uncompacted, last)
            space -= len(files)
        last -= 1
    compacted.extend([0] * space)
    return compacted, uncompacted

def _compacter(uncompacted: list[int], spaces: tuple[int, ...], part: int) -> list[int]:
    compacted = [0] * uncompacted.count(0)
    uncompacted = _remover(uncompacted, 0)
    for i, space in enumerate(spaces):
        if space > 0:
            if part == 1:
                compacted, uncompacted = _space_filler_1(compacted, uncompacted, space)
            elif part == 2:
                compacted, uncompacted = _space_filler_2(compacted, uncompacted, space)
        if i + 1 in uncompacted:
            compacted.extend([i + 1] * uncompacted.count(i + 1))
            uncompacted = _remover(uncompacted, i + 1)
        else:
            compacted.extend([0] * compacted.count(i + 1))
        if uncompacted == []:
            return compacted   

def solver(filename: str):
    for part in (1, 2):
        files, spaces = _reader(filename)
        print(f"Part {part}: {sum(i * file for i, file in enumerate(_compacter(files, spaces, part)))}")
    