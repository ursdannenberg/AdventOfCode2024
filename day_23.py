from collections import defaultdict

def _reader(filename):
    connections = defaultdict(list)
    with open(filename, "r") as file:
        for line in file:
            first, second = line.strip().split("-")
            connections[first].append(second)
            connections[second].append(first)
    return connections

def _set_finder(connections):
    sets = set()
    for computer in connections.keys():
        new_sets = {frozenset((computer,))}
        for sett in sets:
            if all(c in connections[computer] for c in sett):
                new_sets.add(frozenset(sett | {computer,}))
            new_sets.add(frozenset(sett,))
        sets = new_sets
    return sets
    
def solver(filename):
    connections = _reader(filename)
    sets = _set_finder(connections)
    print(f"Part 1: {sum(1 if len(sett) == 3 and any(c.startswith('t') for c in sett) else 0 for sett in sets)}")
    max_length = 0 
    for sett in sets:
        if len(sett) > max_length:
            max_length = len(sett)
            longest_set = ",".join(sorted(list(sett)))
    print(f"Part 2: {longest_set}")
