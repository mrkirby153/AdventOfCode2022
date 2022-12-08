def to_2d_matrix(raw_input, mapper=None):
    """
    Reads the raw input into a 2d matrix
    """
    return [[y if mapper is None else mapper(y) for y in x] for x in raw_input]

def print_2d_matrix(matrix, print_func=print, mapper=None, pad=False):
    """
    Prints out a 2d matrix
    """
    max_width = 0
    if pad:
        raw = [y if mapper is None else mapper(y) for x in matrix for y in x]
        max_width = max([len(str(y)) for y in raw])
    for row in matrix:
        for col in row:
            value = str(col if mapper is None else mapper(col))
            while len(value) < max_width:
                value = f" {value}"
            print_func(value, end=' ')
        print_func()