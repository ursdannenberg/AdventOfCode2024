def _reader(filename: str) -> tuple[list[int], ...]:
    left, right = [], [] 
    with open(filename, "r") as file:
        for line in file:
            le, ri = line.strip().split()
            left.append(int(le))
            right.append(int(ri))
    return left, right
    
def solver(filename: str):
    left, right = _reader(filename)
    
    sum = 0
    for le, ri in zip(sorted(left), sorted(right)):
        sum += abs(ri - le)
    print(f"Part 1: {sum}")
    
    sum = 0
    for le in left:
        sum += le * right.count(le)
    print(f"Part 2: {sum}")
    
    
    