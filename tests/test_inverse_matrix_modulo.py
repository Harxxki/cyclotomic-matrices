import re

import numpy as np
import pytest

from src.inverse_matrix_modulo import matrix_inverse_modulo


# 逆行列が存在する場合のテストケース
@pytest.mark.parametrize("matrix, modulus", [
    (np.array([[2, 1], [5, 3]]), 7),
    (np.array([[1, 2], [3, 4]]), 5),
    (np.array([[3, 3], [2, 5]]), 7),
    (np.array([[2, 5], [1, 6]]), 11),
    (np.array([[4, 7], [2, 6]]), 11),
    (np.array([[6, 2], [1, 8]]), 13),
    (np.array([[7, 4], [5, 2]]), 13),
    (np.array([[8, 3], [4, 7]]), 17),
    (np.array([[9, 6], [3, 8]]), 19),
    (np.array([[10, 7], [5, 9]]), 23),
    # 10x10 matrix with values from 1 to 100, modulus is a prime number
    # 常に可逆とは限らないので修正した方がいいかも
    (np.random.randint(1, 100, (10, 10)), 97),
])
def test_matrix_inverse_modulo(matrix, modulus):
    inverse_matrix = matrix_inverse_modulo(matrix, modulus)
    identity_matrix = np.eye(len(matrix), dtype=int)
    assert np.array_equal((np.dot(matrix, inverse_matrix) % modulus), identity_matrix)


# 逆行列が存在しない場合のテストケース
@pytest.mark.parametrize("matrix, modulus", [
    (np.array([[2, 4], [1, 2]]), 7),
    (np.array([[3, 6], [1, 2]]), 5),
    (np.array([[4, 8], [2, 4]]), 7),
    (np.array([[5, 10], [2, 4]]), 11),
    (np.array([[6, 12], [3, 6]]), 11),
    (np.array([[7, 14], [2, 4]]), 13),
    (np.array([[8, 16], [4, 8]]), 13),
    (np.array([[9, 18], [3, 6]]), 17),
    (np.array([[10, 20], [5, 10]]), 19),
    (np.array([[11, 22], [2, 4]]), 23),
    (np.ones((10, 10), dtype=int), 97),  # 10x10 matrix with all values 1, modulus is a prime number
])
def test_matrix_inverse_modulo_error(matrix, modulus):
    with pytest.raises(ValueError,
                       match=re.escape(
                           "行列は法pにおいて可逆ではありません (Matrix is not invertible modulo p)")):
        matrix_inverse_modulo(matrix, modulus)
