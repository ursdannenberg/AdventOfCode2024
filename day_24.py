def _reader(filename):
    with open(filename, "r") as file:
        wire_list, gate_list = file.read().split("\n\n")
    wires = {}
    for wire in wire_list.split("\n"):
        first, second = wire.split(": ")
        wires[first] = int(second)
    gates = {}
    for gate in gate_list.split("\n"):
        gate, result = gate.split(" -> ")
        first, operator, second = gate.split(" ")
        gates[result] = (first, second, operator)
    return wires, gates

def _compute_gates(wires, gates):
    gate_list = list(gates.keys())
    while gate_list != []:
        for gate in gate_list:
            if any(wire not in wires for wire in gates[gate][0:2]):
                continue
            match gates[gate][2]:
                case "AND":
                    wires[gate] = wires[gates[gate][0]] & wires[gates[gate][1]]
                case "OR":
                    wires[gate] = wires[gates[gate][0]] | wires[gates[gate][1]]
                case "XOR":
                    wires[gate] = wires[gates[gate][0]] ^ wires[gates[gate][1]]
                case _:
                    continue
            gate_list.remove(gate)
    return wires

def solver(filename):
    wires, gates = _reader(filename)
    wires = _compute_gates(wires, gates)
    print([key for key in wires.keys() if key.startswith("z")])
    print("Part 1: " + str(int("".join([str(wires[key]) for key in sorted(wires.keys(), reverse=True) if key.startswith("z")]), 2)))
        
    
    