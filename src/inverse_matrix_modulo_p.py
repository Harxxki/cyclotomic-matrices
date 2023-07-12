import numpy as np


def multiplicative_inverse(a, p):
    for i in range(1, p):
        if (i * a) % p == 1:
            return i
    return -1


def matrix_inverse_modulo_p(matrix, p):
    n = len(matrix)
    matrix = matrix % p
    augmented_matrix = np.hstack((matrix, np.eye(n)))
    for i in range(n):
        pivot_element = multiplicative_inverse(augmented_matrix[i][i], p)
        if pivot_element == -1:
            return "行列は法pにおいて可逆ではありません"
        augmented_matrix[i] = (augmented_matrix[i] * pivot_element) % p
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j][i]
                augmented_matrix[j] = (augmented_matrix[j] - factor * augmented_matrix[i]) % p
    inverse_matrix = augmented_matrix[:, n:] % p
    return inverse_matrix
