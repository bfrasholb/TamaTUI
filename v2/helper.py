def add_tuple(pair_one: tuple, pair_two: tuple) -> tuple:
    return (pair_one[0] + pair_two[0], pair_one[1] + pair_two[1])

def add_tuple_wrap(pair_one: tuple, pair_two: tuple, bounds: tuple) -> tuple:
    return ((pair_one[0] + pair_two[0]) % (bounds[0] - 1), (pair_one[1] + pair_two[1]) % bounds[1])
