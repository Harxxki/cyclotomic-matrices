from collections import namedtuple

import numpy as np

from src.cyclo_matrix_inverse import cyclo_matrix_inverse
from src.utils import print_matrix
from src.cyclotomic_matrix import CyclotomicMatrix

from pprint import pprint


def pretty_print_nparray(arr):
    """Pretty print a numpy array with namedtuple elements."""
    for row in arr:
        print(' '.join(f"({item.l}, {item.m}, {item.n})" for item in row))


def test_cyclo_matrix_inverse():
    # TODO: expectedをactualと書き、actualを名前なしで書いてしまっているので修正する
    # Public values
    l = 2
    p = 17
    gamma_prime = 11

    # Secret values
    gamma_prime_prime = 3
    r_0 = 7

    # --- TEST: B0 ---
    cm_b_0 = CyclotomicMatrix(p=p, l=l, generator=gamma_prime_prime, k=2)
    B_0 = cm_b_0.get(matrix_format="calculated")
    actual_B_0 = np.array([
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
    print_matrix(B_0, 'B_0')
    print_matrix(actual_B_0, 'actual_B_0')
    np.testing.assert_array_equal(x=B_0, y=actual_B_0, err_msg="B_0 is not correct.")

    # --- TEST: D ---
    cm_actual_d = CyclotomicMatrix(p=p, l=l, generator=gamma_prime_prime, k=2)
    Entry = namedtuple('Entry', 'l m n')
    actual_d_values = np.array([
        [(0, 0), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)],
        [(0, 7), (0, 1), (1, 2), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2)],
        [(0, 6), (1, 2), (0, 2), (1, 3), (2, 4), (2, 5), (2, 4), (1, 6)],
        [(0, 5), (1, 6), (1, 3), (0, 3), (1, 4), (2, 5), (2, 5), (1, 5)],
        [(0, 4), (1, 5), (2, 4), (1, 4), (0, 4), (1, 5), (2, 4), (1, 4)],
        [(0, 3), (1, 4), (2, 5), (2, 5), (1, 5), (0, 5), (1, 6), (1, 3)],
        [(0, 2), (1, 3), (2, 4), (2, 5), (2, 4), (1, 6), (0, 6), (1, 2)],
        [(0, 1), (1, 2), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (0, 7)]
    ])
    for i in range(cm_actual_d.size):
        for j in range(cm_actual_d.size):
            l, m = actual_d_values[i][j]
            cm_actual_d.matrix[i][j] = Entry(l=l, m=m, n=0)

    # cm-b_0 が簡略化されてないのでテストに失敗する
    cm_d = cm_b_0.mul(r_0)._calc()
    D = cm_d.get(matrix_format="all")
    actual_D = cm_actual_d._calc().get(matrix_format="all")
    # print_matrix(D, 'D')
    print('\nD:\n')
    pretty_print_nparray(D)
    # print_matrix(actual_D, 'actual_D')
    print('\nactual_D:\n')
    pretty_print_nparray(actual_D)
    np.testing.assert_array_equal(x=D, y=actual_D, err_msg="D is not correct.")

    # --- TEST: inverse of D ---
    D_inversed_pairs = cyclo_matrix_inverse(cm_d.get(matrix_format="pair"), p)
    actual_D_inversed = np.array([
        [-1, 1, 1, -1, -1, 1, -1, 1],
        [1, 0, 0, 1, 0, 0, 0, -1],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [-1, 1, 0, -1, 0, 1, -1, 1],
        [-1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, -1, 1, -1],
        [-1, 0, 0, -1, 0, 1, 0, 1],
        [1, -1, 0, 1, 1, -1, 1, -1]
    ])
    cm_d_inversed = CyclotomicMatrix(p=p, l=l, generator=gamma_prime_prime, k=2)
    Entry = namedtuple('Entry', 'l m n')
    for i in range(cm_d_inversed.size):
        for j in range(cm_d_inversed.size):
            l, m = D_inversed_pairs[i][j]
            cm_d_inversed.matrix[i][j] = Entry(l=l, m=m, n=0)

    D_inversed = cm_d_inversed._calc().get(matrix_format="calculated")
    np.testing.assert_array_equal(D_inversed, actual_D_inversed)


if __name__ == "__main__":
    test_cyclo_matrix_inverse()
