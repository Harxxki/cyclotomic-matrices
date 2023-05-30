import sys
from collections import namedtuple
from typing import Union

import numpy as np


def power(base: int, exponent: int) -> int:
    return base ** exponent


class CyclotomicMatrix:
    def __init__(self, p: int, l: int, generator: int, k: int):
        self.p = p
        self.l = l
        self.generator = generator
        self.k = k
        self.matrix = self._generate()

    def _generate(self) -> np.ndarray:
        """
        Generates a cyclotomic matrix of order 2l^2 over the field Z_p.
        :param p: A prime number
        :param l: A positive integer
        :param generator: A primitive root of p
        :param k: A positive integer
        :return: A 2l^2 x 2l^2 matrix with entries from the set {0, 1, ..., k-1}^2l^2
        """
        order = 2 * self.l ** 2
        size = order

        Entry = namedtuple('Entry', 'l m n')
        arr = np.empty((size, size), dtype=object)

        for a in range(size):
            for b in range(size):
                arr[a][b] = Entry(l=a, m=b, n=0)

        for a in range(size):
            for b in range(size):
                count = 0
                for s in range(self.k):
                    for t in range(self.k):
                        p1 = 2 * self.l ** 2 * s + arr[a][b].l
                        p2 = 2 * self.l ** 2 * t + arr[a][b].m
                        if (power(self.generator, p1) + 1 - power(self.generator, p2)) % self.p == 0:
                            count += 1
                arr[a][b] = arr[a][b]._replace(n=count)
        return arr

    def _convert_cyclotomic_matrix_to_int_matrix(self) -> np.ndarray:
        if self.matrix is None:
            raise ValueError("Matrix has not been generated yet.")

        size = 2 * self.l ** 2
        arr = np.empty((size, size), dtype=int)

        for a in range(size):
            for b in range(size):
                arr[a][b] = self.matrix[a][b].n

        return arr

    def get(self, only_n=False) -> Union[np.ndarray, int]:
        if only_n:
            return self._convert_cyclotomic_matrix_to_int_matrix()
        return self.matrix


def main():
    if len(sys.argv) < 5:
        print("Please provide the values of p, l, generator, k as command line arguments.")
        return

    p = int(sys.argv[1])
    l = int(sys.argv[2])
    generator = int(sys.argv[3])
    k = int(sys.argv[4])

    cmg = CyclotomicMatrix(p, l, generator, k)
    matrix = cmg.get(only_n=True)
    for row in matrix:
        for entry in row:
            print(f"{entry:2}", end=" ")
        print()


if __name__ == "__main__":
    main()
