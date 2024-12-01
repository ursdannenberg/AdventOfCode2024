def _reader(filename: str) -> tuple[list[int], ...]:
    left, right = [], [] 
    with open(filename, "r") as file:
        for line in file:
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
    return left, right
    
def solver(filename: str):
    left, right = _reader(filename)
    
    sum = 0
    for l, r in zip(sorted(left), sorted(right)):
        sum += abs(r - l)
    print(f"Part 1: {sum}")
    
    sum = 0
    for l in left:
        sum += l * right.count(l)
    print(f"Part 2: {sum}")
    
    
    