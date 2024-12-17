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

def _execute_programme(registers, programme):
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

def solver(filename):
    registers, programme = _reader(filename)
    output = _execute_programme(registers, programme)
    print(f"Part 1: {output}")
