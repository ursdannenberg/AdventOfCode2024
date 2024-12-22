from itertools import pairwise

def _reader(filename):
    with open(filename, "r") as file:
        return tuple(int(number.strip()) for number in file.readlines())

def _number_evolver(number):
    number = (number ^ (number * 64)) % 16777216
    number = (number ^ int(number / 32)) % 16777216
    return (number ^ (number * 2048)) % 16777216

def _cacher(number, sequences, cache):
    cache.append(number)
    if len(cache) <= 4:
        return sequences, cache
    if len(cache) >= 6:
        del cache[0]
    sequence = tuple(second - first for first, second in pairwise(cache))
    if sequence not in sequences:
        sequences[sequence] = number
    return sequences, cache

def solver(filename):
    numbers = _reader(filename)
    buyers = ()
    all_sequences = set()
    total = 0
    for number in numbers:
        sequences = {}
        cache = []
        for _ in range(2000):
            number = _number_evolver(number)
            sequences, cache = _cacher(int(str(number)[-1]), sequences, cache)
        buyers += (sequences,)
        all_sequences.update(sequences.keys())
        total += number
    print(f"Part 1: {total}")
    print(f"Part 2: {max(sum(0 if sequence not in buyer else buyer[sequence] for buyer in buyers) for sequence in all_sequences)}")