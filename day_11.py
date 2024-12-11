from functools import cache
def _reader(filename: str) -> list[int]:
    with open(filename, "r") as file:
        return {int(stone): 1 for stone in file.readline().strip().split(" ")}

@cache
def _blink(stone: int) -> tuple[int]:
    if stone == 0:
        return (1,)
    elif len(str(stone)) % 2 == 0:
        engraving = str(stone)
        return (int(engraving[:len(engraving)//2]), int(engraving[len(engraving)//2:]))
    else:
        return (stone * 2024,)

def solver(filename: str):
    stones = _reader(filename)
    for i in range(75):
        changes = {}
        for stone, number in stones.items():
            for change in _blink(stone):
                if change in changes:
                    changes[change] += number
                else:
                    changes[change] = number
        stones = changes
        if i == 24:
            print(f"Part 1: {sum(number for _, number in stones.items())}")
    print(f"Part 2: {sum(number for _, number in stones.items())}")
    