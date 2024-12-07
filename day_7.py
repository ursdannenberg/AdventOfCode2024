def _reader(filename: str) -> dict[int, tuple[int]]:
    equations = {}
    with open(filename, "r") as file:
       for line in file:
           left, right = line.strip().split(": ")
           equations[int(left)] = tuple(int(number) for number in right.split(" "))
    return equations

def _calculator(solutions: set[int], number: int, part: int) -> set[int]:
    if part == 1:
        return set(solution + number for solution in solutions) | set(solution * number for solution in solutions)
    elif part == 2:
        return _calculator(solutions, number, 1) | set(int(str(solution)+str(number)) for solution in solutions)

def solver(filename: str) -> None:
    equations = _reader(filename)
    for part in (1, 2):
        sum = 0
        for solution, numbers in equations.items():
            solutions = {numbers[0]}
            for number in numbers[1:]:
                solutions = _calculator(solutions, number, part)
            if solution in solutions:
                sum += solution
        print(f"Part {part}: {sum}")         