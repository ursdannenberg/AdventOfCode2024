from math import gcd
import mip

def _reader(filename: str) -> tuple[tuple[tuple[int, int], ...], ...]:
    machines = ()
    with open(filename, "r") as file:
        for machine in file.read().split("\n\n"):
            a, b, prize = machine.splitlines() 
            a = tuple(int(xy) for xy in a.strip("Button A: X+").split(", Y+"))
            b = tuple(int(xy) for xy in b.strip("Button A: X+").split(", Y+"))
            prize = tuple(int(xy) for xy in prize.strip("Prize: X=").split(", Y="))
            machines += ((a, b, prize),)
    return machines

def _brute_force(machine: tuple[tuple[int, int], ...]) -> int:
    a, b, prize = machine
    # c can be expressed as a linear combination of a and b if and only if it is a multiple of gcd(a, b)
    if any(p_xy % gcd(a_xy, b_xy) != 0 for a_xy, b_xy, p_xy in zip(a, b, prize)):
        return 0
    tokens = 400
    for i in range(101):
        if any(a_xy * i > p_xy for a_xy, p_xy in zip(a, prize)):
            break
        for j in range(101):
            if any(b_xy * j > p_xy for b_xy, p_xy in zip(b, prize)):
                break 
            if all(a_xy * i + b_xy * j == p_xy for a_xy, b_xy, p_xy in zip(a, b, prize)):
                tokens = min(tokens, i * 3 + j)
    return tokens if tokens < 400 else 0

def _mip(machine: tuple[tuple[int, int], ...]) -> int:
    a, b, prize = machine
    if any(p_xy % gcd(a_xy, b_xy) != 0 for a_xy, b_xy, p_xy in zip(a, b, prize)):
        return 0
    model = mip.Model(mip.MINIMIZE)
    num_a = model.add_var(var_type=mip.INTEGER, lb=0)
    num_b = model.add_var(var_type=mip.INTEGER, lb=0)
    
    model += num_a * a[0] + num_b * b[0] == prize[0]
    model += num_a * a[1] + num_b * b[1] == prize[1]
    
    model.objective = mip.xsum([num_a * 3 + num_b])
    model.optimize()
    return int(model.objective_value) if model.objective_value is not None else 0

def solver(filename: str) -> None:
    machines = _reader(filename)
    tokens = 0
    for machine in machines:
        tokens += _brute_force(machine)
    print(f"Part 1: {tokens}")
    tokens = 0
    for machine in machines:
        prize = tuple(xy + 10000000000000 for xy in machine[2])
        tokens += _mip((machine[0], machine[1], prize))
    print(f"Part 2: {tokens}")