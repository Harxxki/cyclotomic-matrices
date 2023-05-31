import math
import sys


# p-1の全ての素因数を求める
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


# gが生成元かどうかをチェックする
def is_generator(g, p, factors):
    for q in factors:
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True


def find_generators(p):
    """
    Algorithm 2: Determination of generators of F_p
    :param p:
    :return:
    """
    factors = prime_factors(p - 1)
    generators = [g for g in range(1, p) if is_generator(g, p, factors)]
    return generators


if __name__ == '__main__':
    # コマンドライン引数から素数pを取得
    if len(sys.argv) > 1:
        p = int(sys.argv[1])
        print(find_generators(p))
    else:
        print("Please provide a prime number as an argument.")
