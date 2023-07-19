import numpy as np


def multiplicative_inverse(a, modulus):
    for i in range(1, modulus):
        if (i * a) % modulus == 1:
            return i
    return -1


def matrix_inverse_modulo(matrix, modulus):
    n = len(matrix)
    matrix = matrix % modulus
    augmented_matrix = np.hstack((matrix.astype(int), np.eye(n, dtype=int)))
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    break
            else:
                raise ValueError("行列は法pにおいて可逆ではありません (Matrix is not invertible modulo p)")
        pivot_element = multiplicative_inverse(augmented_matrix[i][i], modulus)
        augmented_matrix[i] = (augmented_matrix[i] * pivot_element) % modulus
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j][i]
                augmented_matrix[j, i:] = (
                        (augmented_matrix[j, i:] - factor * augmented_matrix[i,
                                                            i:]) % modulus).astype(
                    int)
    inverse_matrix = augmented_matrix[:, n:] % modulus
    return inverse_matrix
