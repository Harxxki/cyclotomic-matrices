import numpy as np
import sys
from collections import namedtuple


def power(base, exponent):
    return base ** exponent


class CyclotomicMatrixGenerator:
    def __init__(self, p, l, generator, k):
        self.p = p
        self.l = l
        self.generator = generator
        self.k = k

    def generate_cyclotomic_matrix(self):
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


def main():
    if len(sys.argv) < 5:
        print("Please provide the values of p, l, γ, k as command line arguments.")
        return

    p = int(sys.argv[1])
    l = int(sys.argv[2])
    γ = int(sys.argv[3])
    k = int(sys.argv[4])

    generator = CyclotomicMatrixGenerator(p, l, γ, k)
    matrix = generator.generate_cyclotomic_matrix()
    for row in matrix:
        for entry in row:
            print(f"{entry.n:2}", end=" ")
        print()


if __name__ == "__main__":
    main()
