import numpy as np
from src.utils import print_matrix
from src.cyclotomic_matrix import CyclotomicMatrix


def test_cyclotomic_matrix():
    """
    Test the cyclotomic matrix.
    :return:
    """
    cm = CyclotomicMatrix(p=17, l=2, generator=3, k=2)
    matrix = cm.get(matrix_format="calculated")

    expected_output = np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0]
    ])

    print('\n')
    print_matrix(expected_output, 'Expected Output')
    print_matrix(matrix, 'Actual Output')

    np.testing.assert_array_equal(matrix, expected_output)


if __name__ == "__main__":
    test_cyclotomic_matrix()
