import numpy as np


class MessageMatrixConverter:
    def __init__(self, l):
        self.l = l

    def str_to_int(self, s):
        try:
            return int.from_bytes(s.encode(), 'little')
        except UnicodeEncodeError:
            raise ValueError("The input string contains non-ASCII characters.")

    def int_to_str(self, i):
        return i.to_bytes((i.bit_length() + 7) // 8, 'little').decode()

    def int_to_matrix(self, i):
        matrix_size = 2 * self.l**2
        matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        binary = bin(i)[2:]
        binary = binary.zfill(matrix_size**2)
        for idx, bit in enumerate(binary):
            row = idx // matrix_size
            col = idx % matrix_size
            matrix[row][col] = int(bit)
        return matrix

    def matrix_to_int(self, matrix):
        flat_list = matrix.flatten().tolist()
        binary = ''.join(map(str, flat_list))
        return int(binary, 2)

    def str_to_matrix(self, s):
        matrix_size = 2 * self.l**2
        i = self.str_to_int(s)
        if i.bit_length() > matrix_size**2:
            raise ValueError("The input string is too large for the specified matrix size.")
        return self.int_to_matrix(i)

    def matrix_to_str(self, matrix):
        i = self.matrix_to_int(matrix)
        return self.int_to_str(i)
