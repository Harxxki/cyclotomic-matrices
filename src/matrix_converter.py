import numpy as np
import string


class MatrixConverter:
    def __init__(self, l, p):
        if p > 62:
            raise ValueError("p cannot exceed 62.")
        self.l = l
        self.p = p
        self.char_list = list(string.ascii_lowercase[:p]) + list(
            string.digits[:max(0, p - 26)]) + list(string.ascii_uppercase[:max(0, p - 36)])

    def char_to_int(self, c):
        try:
            return self.char_list.index(c)
        except ValueError:
            raise ValueError(f"Character {c} not in char_list.")

    def int_to_char(self, i):
        try:
            return self.char_list[i]
        except IndexError:
            raise ValueError(f"Index {i} out of range for char_list.")

    def str_to_matrix(self, s):
        matrix_size = 2 * self.l ** 2
        if len(s) > matrix_size ** 2:
            raise ValueError("The input string is too large for the specified matrix size.")
        matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        for idx, char in enumerate(s):
            row = idx // matrix_size
            col = idx % matrix_size
            matrix[row][col] = self.char_to_int(char)
        return matrix

    def matrix_to_str(self, matrix):
        flat_list = matrix.flatten().tolist()
        return ''.join(self.int_to_char(i) for i in flat_list)
