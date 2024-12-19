import sys

def _reader(filename):
    registers = {}
    with open(filename, "r") as file:
        regs, programme = file.read().split("\n\n")
    for reg in regs.splitlines():
        letter, value = reg.strip("Register ").split(": ")
        registers[letter] = int(value)
    return registers, programme.strip("Program: ")

def _get_operand(operand, registers):
    operands = {"0": 0, "1": 1, "2": 2, "3": 3, "4": registers["A"], "5": registers["B"], "6": registers["C"], "7": None}
    return operands[operand], int(operand)

def _execute_programme(registers, programme, once = False):
    ip = 0
    output = ""
    while ip <= len(programme) - 2:
        combo_operand, literal_operand = _get_operand(programme[ip+2], registers)
        instruction = programme[ip]
        match instruction:
            case "0":
                registers["A"] = int(registers["A"] / 2. ** combo_operand)
            case "1":
                registers["B"] ^= literal_operand
            case "2":
                registers["B"] = combo_operand % 8
            case "3":
                if once:
                    return output
                if registers["A"] != 0:
                    ip = literal_operand * 2
            case "4":
                registers["B"] ^= registers["C"]
            case "5":
                output += f"{combo_operand % 8}" if output == "" else f",{combo_operand % 8}"
            case "6":
                registers["B"] = int(registers["A"] / 2. ** combo_operand)
            case "7":
                registers["C"] = int(registers["A"] / 2. ** combo_operand)
            case _:
                continue
        if instruction != "3" or registers["A"] == 0:
            ip += 4
    return output

def _find_nema(values, programme, a, ind):
    val = values[ind]
    for i in range(0, 8):
        registers = {"A": a + i, "B": 0, "C": 0}
        output = _execute_programme(registers, programme, once = True)
        if int(output[0]) == val:
            if abs(ind) == len(values):
                print(f"Part 2: {a + i}")
                sys.exit()
            elif abs(ind) < len(values):
                _find_nema(values, programme, (a + i) * 8, ind - 1)

def solver(filename):
    registers, programme = _reader(filename)
    print(f"Part 1: {_execute_programme(registers, programme)[0]}")
    values = tuple(int(value) for value in programme.split(","))
    _find_nema(values, programme, 0, -1)
