import numpy as np
from src.find_generators import find_generators


def print_matrix(matrix: np.ndarray, name: str) -> None:
    """Print a named matrix in a pretty format."""
    print(f"{name}:")
    for row in matrix:
        for entry in row:
            print(f"{entry:2}", end=" ")
        print()
    print()  # Add an extra newline for readability.


def secret_key_expansion(p: int, l: int, r_0: int, generator: int):
    """
    Algorithm 4. Secret key expansion. (Wrapper of Algorithm 2 & 3)
    :param p: A prime number
    :param l: A positive integer
    :param r_0: A positive integer
    :param generator: A primitive root of p
    :return: generators: list of
    """
    # TODO implementation Algorithm 1
    generators = find_generators(p)
    return generators
