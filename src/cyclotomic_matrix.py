import sys
from collections import namedtuple
from typing import Union

import numpy as np


def power(base: int, exponent: int) -> int:
    return base ** exponent


class CyclotomicMatrix:
    def __init__(self, p: int, l: int, generator: int, k: int):
        """
        :param p: A prime number
        :param l: A positive integer
        :param generator: A primitive root of p
        :param k: A positive integer
        """
        self.p = p
        self.l = l
        self.generator = generator
        self.k = k
        self.order = 2 * self.l ** 2
        self.size = self.order
        self.matrix = self._generate()
        self._calc()

    def _generate(self) -> np.ndarray:
        """
        Generates a cyclotomic matrix of order 2l^2 over the field Z_p.
        """
        Entry = namedtuple('Entry', 'l m n')
        arr = np.empty((self.size, self.size), dtype=object)

        for a in range(self.size):
            for b in range(self.size):
                arr[a][b] = Entry(l=a, m=b, n=0)

        return arr

    def _calc(self):
        """
        Calculates the entries of the cyclotomic matrix.
        基本的には初期化のタイミングのみで呼び出すが, 主に復号において (l, m) の値を変更した場合に再度計算をかける必要があるので, その際には外部から呼び出す.
        """
        for a in range(self.size):
            for b in range(self.size):
                count = 0
                for s in range(self.k):
                    for t in range(self.k):
                        p1 = 2 * self.l ** 2 * s + self.matrix[a][b].l
                        p2 = 2 * self.l ** 2 * t + self.matrix[a][b].m
                        is_zero = (power(self.generator, p1) + 1 - power(self.generator, p2)) % self.p == 0
                        count += np.sum(is_zero)
                self.matrix[a][b] = self.matrix[a][b]._replace(n=count)
        return self

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

    def mul(self, r_0):
        size = 2 * self.l ** 2
        Entry = namedtuple('Entry', 'l m n')  # Re-introduce the namedtuple here
        for a in range(size):
            for b in range(size):
                l, m, n = self.matrix[a][b]
                l_new = (l * r_0) % self.p
                m_new = (m * r_0) % self.p
                self.matrix[a][b] = Entry(l_new, m_new, n)  # Use Entry namedtuple here
        return self


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
