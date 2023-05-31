import numpy as np
from collections import namedtuple
from src.cyclotomic_matrix import CyclotomicMatrix


def test_cyclotomic_matrix():
    cm = CyclotomicMatrix(p=17, l=2, generator=3, k=2)
    matrix = cm.get(only_n=True)

    expected_output = [
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0]
    ]

    print("\nExpected Output:")
    for row in expected_output:
        print(row)

    print("\nActual Output:")
    for row in matrix:
        print(row)

    for i in range(len(expected_output)):
        for j in range(len(expected_output[0])):
            assert matrix[i][j] == expected_output[i][j]

if __name__ == "__main__":
    test_generate_cyclotomic_matrix()
