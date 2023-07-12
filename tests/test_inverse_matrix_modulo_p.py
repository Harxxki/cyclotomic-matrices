import numpy as np
from src.inverse_matrix_modulo_p import matrix_inverse_modulo_p


def test_matrix_inverse_modulo_p():
    matrix = np.array([[2, 1], [5, 3]])
    print("Original matrix:")
    print(matrix)
    p = 7
    expected_inverse = np.array([[6, 1], [2, 2]])
    calculated_inverse = matrix_inverse_modulo_p(matrix, p)
    print("Calculated inverse:")
    print(calculated_inverse)
    print("int version of calculated inverse:")
    print(calculated_inverse.astype(int))
    print("Expected inverse:")
    print(expected_inverse)
    assert np.array_equal(calculated_inverse, expected_inverse), "Test failed!"
    print("Test passed!")


if __name__ == "__main__":
    test_matrix_inverse_modulo_p()
