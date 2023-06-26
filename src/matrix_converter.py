import numpy as np


class MatrixConverter:
    def __init__(self, l):
        self.l = l

    def char_to_int(self, c):
        return ord(c)

    def int_to_char(self, i):
        return chr(int(i))

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
