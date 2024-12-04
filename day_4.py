import re
def _reader(filename: str) -> str:
    with open(filename, "r") as file:
        return file.readlines()

def _counter(string: str) -> int:
    return len(re.findall("XMAS", string)) + len(re.findall("SAMX", string))

def _diagonal_constructor(word_search: list[str], num_rows: int, num_columns: int) -> list[str]:
    forward_diagonals = ["" for _ in range((num_rows + num_columns - 1))]
    backward_diagonals = ["" for _ in range((num_rows + num_columns - 1))]
    for j in range(num_columns):
        for i in range(num_rows):
            forward_diagonals[i - j + num_rows - 1] += word_search[j][i]
            backward_diagonals[i + j] += word_search[j][i]
    return forward_diagonals + backward_diagonals

def _mas_finder(word_search: list[str], num_rows: int, num_columns: int) -> int:
    sum = 0
    mas = [("M", "M", "A", "S", "S"), 
        ("M", "S", "A", "M", "S"),
        ("S", "M", "A", "S", "M"),
        ("S", "S", "A", "M", "M")]
    for j in range(num_columns - 2):
        for i in range(num_rows - 2):
            if (word_search[j][i], word_search[j + 2][i], word_search[j + 1][i + 1], word_search[j][i + 2], word_search[j + 2][i + 2]) in mas:
                sum += 1
    return sum

def solver(filename: str) -> None:
    word_search = _reader(filename)    
    
    sum = 0
    num_rows = len(word_search)
    num_columns = len(word_search[0].strip())
    # horizontal
    for row in word_search:
        sum += _counter(row)
    # vertical
    for column in ["".join(row[i] for row in word_search) for i in range(num_columns)]:
         sum += _counter(column)
    # diagonal
    for diagonal in _diagonal_constructor(word_search, num_rows, num_columns):
        sum += _counter(diagonal)
    print(f"Part 1: {sum}")
    
    print(f"Part 2: {_mas_finder(word_search, num_rows, num_columns)}")
    
