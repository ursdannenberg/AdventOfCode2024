
def _report_analyser(levels: list[int]) -> bool:
    if sorted(levels) != levels and sorted(levels, reverse=True) != levels:
        return False
    for first, second in zip(levels[:-1], levels[1:]):
        if abs(first - second) < 1 or abs(first - second) > 3:
            return False
    return True

def _reader(filename: str) -> int:
    sum_1 = 0
    sum_2 = 0
    with open(filename, "r") as file:
        for line in file:
            levels = [int(element) for element in line.strip().split()]
            if _report_analyser(levels):
                sum_1 += 1
                sum_2 += 1
                continue
            for i in range(len(levels)):
                if _report_analyser(levels[:i] + levels[i + 1:]):
                    sum_2 += 1
                    break 
    return sum_1, sum_2
            
def solver(filename: str) -> None:
    sum_1, sum_2 = _reader(filename)
    print(f"Part 1: {sum_1}")
    print(f"Part 2: {sum_2}")