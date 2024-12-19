from functools import cache

def _reader(filename):
    with open(filename, "r") as file:
        towels, patterns = file.read().split("\n\n")
    return (
        tuple(t for t in towels.strip().split(", ")),
        tuple(p.strip() for p in patterns.splitlines())
    )

@cache
def _knapsack(pattern, towels):
    if pattern == "":
        return (1, 1)
    if any(pattern.startswith(towel) for towel in towels):
        return (
            max(_knapsack(pattern[len(towel):], towels)[0] for towel in towels if pattern.startswith(towel)),
            sum(_knapsack(pattern[len(towel):], towels)[1] for towel in towels if pattern.startswith(towel))
        )
    else:
        return (0, 0) 
    
def solver(filename):
    towels, patterns = _reader(filename)
    print(f"Part 1, 2: {tuple(sum(_knapsack(pattern, towels)[i] for pattern in patterns) for i in range(2))}")
    