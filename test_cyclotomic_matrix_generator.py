import numpy as np
from collections import namedtuple
from cyclotomic_matrix_generator import CyclotomicMatrixGenerator


def test_generate_cyclotomic_matrix():
    generator = CyclotomicMatrixGenerator(p=17, l=2, generator=3, k=2)
    matrix = generator.generate_cyclotomic_matrix()

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

    print("Expected Output:")
    for row in expected_output:
        print(row)

    print("\nActual Output:")
    for row in matrix:
        print([entry.n for entry in row])

    for i in range(len(expected_output)):
        for j in range(len(expected_output[0])):
            assert matrix[i][j].n == expected_output[i][j]

if __name__ == "__main__":
    test_generate_cyclotomic_matrix()
