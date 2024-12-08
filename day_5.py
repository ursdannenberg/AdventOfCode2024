def _reader(filename: str) -> tuple[dict[int, list[int]], list[list[int]]]:
    inverted_rules = {}
    updates = []
    with open(filename, "r") as file:
        for line in file:
            if "|" in line:
                first, second = [int(page) for page in line.strip().split("|")]
                if second in inverted_rules:
                    inverted_rules[second].append(first)
                else:
                    inverted_rules[second] = [first]    
            elif "," in line:
                updates.append([int(page) for page in line.strip().split(",")])             
    return inverted_rules, updates

def _permuter(update: list[int], inverted_rules: dict[int, list[int]]) -> list[int]:
    for i, first in enumerate(update[:-1]):
        if first in inverted_rules:
            for second in update[i + 1:][::-1]:
                if second in inverted_rules[first]:
                    j = update.index(second)
                    return update[:i] + update[i + 1:j + 1] + [first] + update[j + 1:] 
    
def solver(filename: str):
    inverted_rules, updates = _reader(filename)
    sum_1 = 0
    sum_2 = 0
    for update in updates:
        if not any ([[p for p in update[i + 1:] if p in inverted_rules[page]] for i, page in enumerate(update[:-1]) if page in inverted_rules]):
            sum_1 += update[len(update)//2]
        else:
            while any ([[p for p in update[i + 1:] if p in inverted_rules[page]] for i, page in enumerate(update[:-1]) if page in inverted_rules]):
                update = _permuter(update, inverted_rules)
            sum_2 += update[len(update)//2]      
    print(f"Part 1: {sum_1}")
    print(f"Part 2: {sum_2}")
    