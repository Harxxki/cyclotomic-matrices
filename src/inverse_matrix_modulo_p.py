import numpy as np


def multiplicative_inverse(a, p):
    for i in range(1, p):
        if (i * a) % p == 1:
            return i
    return -1


def matrix_inverse_modulo_p(matrix, p):
    n = len(matrix)
    matrix = matrix % p
    augmented_matrix = np.hstack((matrix.astype(int), np.eye(n, dtype=int)))
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    break
            else:
                return "行列は法pにおいて可逆ではありません"
        pivot_element = multiplicative_inverse(augmented_matrix[i][i], p)
        augmented_matrix[i] = (augmented_matrix[i] * pivot_element) % p
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j][i]
                augmented_matrix[j, i:] = (
                        (augmented_matrix[j, i:] - factor * augmented_matrix[i, i:]) % p).astype(
                    int)
    inverse_matrix = augmented_matrix[:, n:] % p
    return inverse_matrix
