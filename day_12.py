def _reader(filename: str) -> dict[str, list[tuple[int, int]]]:
    garden = {}
    with open(filename, "r") as file:
        for j, row in enumerate(file):
            for i, plant in enumerate(row.strip()):
                if plant in garden:
                    garden[plant].append((i, j))
                else:
                    garden[plant] = [(i, j)]
    return garden
            
def _bfs(start: tuple[int, int], plants: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], int, int]:
    # Breadth-first search to find neighbouring plants that form a region 
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    perimeter = 0
    adjacent = set()
    region = [start]
    plants.remove(start)
    queue = [start]
    for plant in queue:
        pm = 4
        for dir in dirs:
            neighbour = tuple(p + d for p, d in zip(plant, dir))
            if neighbour in plants:
                region.append(neighbour)
                plants.remove(neighbour)
                queue.append(neighbour)
                pm -= 1
            elif neighbour in region:
                pm -= 1
            else:
                adjacent.add((neighbour, dir))
        perimeter += pm
    
    # Exclude neighbours in same direction from plants adjacent to region
    # The number of remaining adjacent plants is equal to the number of sides of the region
    sides = 0
    checked = set()
    for plant, direction in adjacent:
        if (plant, direction) in checked:
            continue
        sides += 1
        checked.add((plant, direction))
        queue = [plant]
        for plant in queue:
            for dir in dirs:
                neighbour = tuple(p + d for p, d in zip(plant, dir))
                if (neighbour, direction) in adjacent and (neighbour, direction) not in checked:
                    checked.add((neighbour, direction))
                    queue.append(neighbour)
    return region, len(region) * perimeter, len(region) * sides
    
def _filter(unfiltered: dict[str, list[tuple[int, int]]]) -> tuple[int, int]:
    # Split up areas that share a letter but are not connected.
    filtered = ()
    price_without_discount = 0
    price_with_discount = 0
    for _, plants in unfiltered.items():
        while plants != []:
            region, pwod, pwd = _bfs(plants[0], plants)
            filtered += (region,)
            price_without_discount += pwod
            price_with_discount += pwd
    return price_without_discount, price_with_discount

def solver(filename: str):
    garden = _reader(filename)
    price_without_discount, price_with_discount = _filter(garden)
    print(f"Part 1: {price_without_discount}")
    print(f"Part 2: {price_with_discount}")
    