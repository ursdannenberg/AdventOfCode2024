import re
def _reader(filename: str) -> str:
    with open(filename, "r") as file:
        return "".join(file.readlines())

def _sum_multiplications(memory: str) -> int:
    sum = 0
    multiplications = re.findall("mul\(\d+,\d+\)", memory) 
    for multiplication in multiplications:
        first, second = multiplication.strip("mul()").split(",")
        sum += int(first) * int(second)
    return sum

def solver(filename: str) -> None:
    memory = _reader(filename)    
    
    print(f"Part 1: {_sum_multiplications(memory)}")
    
    sum = 0
    while "don't()" in memory:
        sum += _sum_multiplications(memory.split("don't()", 1)[0])
        memory = memory.split("don't()", 1)[1]
        memory = "" if "do()" not in memory else memory.split("do()", 1)[1]
    sum += _sum_multiplications(memory)
    print(f"Part 2: {sum}")