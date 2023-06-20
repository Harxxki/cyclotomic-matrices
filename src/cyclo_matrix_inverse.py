import numpy as np


def cyclo_add(pair1, pair2, p):
    i, j = pair1
    k, l = pair2
    return (i + k) % p, (j + l) % p


def cyclo_sub(pair1, pair2, p):
    i, j = pair1
    k, l = pair2
    return (i - k) % p, (j - l) % p


def cyclo_scalar_mul(scalar, pair, p):
    i, j = pair
    return (scalar * i) % p, (scalar * j) % p


def find_multiplicative_inverse(a, p):
    """a mod pの乗法逆元を探す.
    注意: aとpが互いに素である必要がある.
    """
    for i in range(1, p):
        if (i * a) % p == 1:
            return i
    raise ValueError(f"No multiplicative inverse for {a} mod {p}")


def cyclo_matrix_inverse(matrix, p):
    """ガウス-ジョルダンの消去法を使用してサイクロトミック行列の逆行列を計算する.

    Parameters:
    matrix: A 2D numpy array of pairs (i, j)
    p: The prime number
    """
    n = len(matrix)
    inverse_matrix = np.empty_like(matrix)

    # 単位行列の生成
    for i in range(n):
        for j in range(n):
            inverse_matrix[i][j] = (1, 0) if i == j else (0, 0)

    # ガウス-ジョルダンの消去法
    for i in range(n):
        # 対角要素が"0"の場合は, 対角要素が"0"でない行と入れ替える
        if matrix[i][i] == (0, 0):
            for j in range(i + 1, n):
                if matrix[j][i] != (0, 0):
                    matrix[[i, j]] = matrix[[j, i]]
                    inverse_matrix[[i, j]] = inverse_matrix[[j, i]]
                    break

        # 非ゼロの行を交換できない場合で, 対角要素が依然としてゼロの場合は逆行列が存在しない
        if matrix[i][i] == (0, 0):
            raise ValueError("Matrix is singular.")

        # 対角要素を(1, 0)にするために現在の行をスケーリング
        inv_diagonal = find_multiplicative_inverse(matrix[i][i][0], p)
        for j in range(n):
            matrix[i][j] = cyclo_scalar_mul(inv_diagonal, matrix[i][j], p)
            inverse_matrix[i][j] = cyclo_scalar_mul(inv_diagonal, inverse_matrix[i][j], p)

        # 対角要素の上と下を"0"にする
        for j in range(n):
            if j != i:
                ratio = matrix[j][i]
                for k in range(n):
                    matrix[j][k] = cyclo_sub(matrix[j][k],
                                             cyclo_scalar_mul(ratio[0], matrix[i][k], p), p)
                    inverse_matrix[j][k] = cyclo_sub(inverse_matrix[j][k],
                                                     cyclo_scalar_mul(ratio[0],
                                                                      inverse_matrix[i][k], p), p)

    return inverse_matrix
