import numpy as np
import sympy

from src.find_generators import find_generators
import random


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


def is_generator(generator: int, p: int) -> bool:
    """Check if g is a generator of F_p."""
    for f in sympy.factorint(p - 1):
        if pow(generator, (p - 1) // f, p) == 1:
            return False
    return True


def find_public_generator(private_generator: int, p: int) -> tuple:
    """Find r_0 and gamma_prime (public)"""
    r_0s = list(range(1, p))
    random.shuffle(r_0s)
    for r_0 in r_0s:
        public_generator = pow(private_generator, r_0, p)
        if is_generator(public_generator, p):
            return public_generator, r_0
