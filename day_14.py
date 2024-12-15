from math import log, exp
import matplotlib.pyplot as plt

def _reader(filename: str) -> tuple[tuple[tuple[int, int], ...], ...]:
    robots = ()
    with open(filename, "r") as file:
        for robot in file:
            position = tuple(int(pos) for pos in robot.strip().split(" ")[0].strip("p= ").split(","))
            velocity = tuple(int(vel) for vel in robot.strip().split(" ")[1].strip("v= ").split(","))
            robots += ((position, velocity),)
    return robots

def _mover(robot: tuple[tuple[int, int], ...], steps: int, x_max: int, y_max: int) -> tuple[int, int]:
    position, velocity = robot
    return tuple((pos + vel * steps) % xy_max for pos, vel, xy_max in zip(position, velocity, (x_max, y_max)))

def _quadrant_locator(positions, x_max: int, y_max: int):
    quadrants = [0, 0, 0, 0]
    for position in positions:
        if position[0] <= x_max // 2 - 1 and position[1] <= y_max // 2 - 1:
            quadrants[0] += 1
        elif position[0] >= x_max // 2 + 1 and position[1] <= y_max // 2 - 1:
            quadrants[1] += 1
        elif position[0] <= x_max // 2 - 1 and position[1] >= y_max // 2 + 1:
            quadrants[2] += 1
        elif position[0] >= x_max // 2 + 1 and position[1] >= y_max // 2 + 1:
            quadrants[3] += 1
    # Work-around since there is no prod()
    return int(round(exp(sum(log(quadrant) for quadrant in quadrants))))

def solver(filename : str) -> None:
    x_max, y_max = (101, 103)
    robots = _reader(filename)
    for i in range(10001):
        positions = ()
        for robot in robots:
            positions += (_mover(robot, i, x_max, y_max),)
        print(f"Part 1: {_quadrant_locator(positions, x_max, y_max)}")
        plt.plot([x for x, _ in positions], [y for _, y in positions], "kx")
        plt.savefig(f"day_14/{i}.png")
        plt.clf()