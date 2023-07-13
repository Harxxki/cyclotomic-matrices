import numpy as np
import pandas as pd

p = 17
e = 8
rand = 3

# 行列A (Zをmod pしてそのままMessage Matrixを計算)
A = np.array([
    [2039, 1750, 1871, 1833, 32, 77, 101, 115],
    [115, 97, 103, 101, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1955, 1649, 1751, 1717, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1955, 1649, 1751, 1717, 0, 0, 0, 0],
    [1955, 1649, 1751, 1717, 0, 0, 0, 0],
    [1955, 1649, 1751, 1717, 0, 0, 0, 0]
])

# 行列B (Zをmod eしてそのままMessage Matrixを計算)
B = np.array([
    [1004, 877, 944, 924, 32, 77, 101, 115],
    [115, 97, 103, 101, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [920, 776, 824, 808, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [920, 776, 824, 808, 0, 0, 0, 0],
    [920, 776, 824, 808, 0, 0, 0, 0],
    [920, 776, 824, 808, 0, 0, 0, 0]
])

# 行列Rand (Zをmod rand=3してそのままMessage Matrixを計算)
Rand = np.array([
    [42, 34, 54, 43, 25, 3, 14, 67],
    [6, 6, 31, 33, 10, 1, 9, 50],
    [2, 0, 10, 11, 1, 0, 3, 14],
    [17, 23, 40, 35, 24, 3, 9, 66],
    [6, 0, 30, 33, 3, 0, 9, 42],
    [6, 18, 33, 33, 24, 3, 9, 66],
    [6, 18, 33, 33, 24, 3, 9, 66],
    [39, 33, 54, 39, 24, 3, 9, 66],
])

# 正当
Expected = np.array([
    [84, 101, 120, 116, 32, 77, 101, 115],
    [115, 97, 103, 101, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

# mod p or eを計算
A_mod_p = np.mod(A, p)
A_mod_e = np.mod(A, e)
A_mod_rand = np.mod(A, rand)
B_mod_p = np.mod(B, p)
B_mod_e = np.mod(B, e)
B_mod_rand = np.mod(B, rand)
Rand_mod_p = np.mod(Rand, p)
Rand_mod_e = np.mod(Rand, e)
Rand_mod_rand = np.mod(Rand, rand)
Expected_mod_p = np.mod(Expected, p)
Expected_mod_e = np.mod(Expected, e)
Expected_mod_rand = np.mod(Expected, rand)

# print("A mod p:")
# print(A_mod_p)
# print("\nExpected mod p:")
# print(Expected_mod_p)
# print("\nB mod e:")
# print(B_mod_e)
# print("\nExpected mod e:")
# print(Expected_mod_e)
# print("\nA mod rand:")
# print(A_mod_rand)
# print("\nB mod rand:")
# print(B_mod_rand)
print("\nRand mod rand:")
print(Rand_mod_rand)
print("\nExpected mod rand:")
print(Expected_mod_rand)

# 行列が一致したかどうかを比較
# 行列のリストを作成
matrix_list = [('A_mod_p', A_mod_p), ('A_mod_e', A_mod_e), ('A_mod_rand', A_mod_rand),
               ('B_mod_p', B_mod_p), ('B_mod_e', B_mod_e), ('B_mod_rand', B_mod_rand),
               ('Rand_mod_p', Rand_mod_p), ('Rand_mod_e', Rand_mod_e),
               ('Rand_mod_rand', Rand_mod_rand)
               ]
expected_list = [('Expected_mod_p', Expected_mod_p), ('Expected_mod_e', Expected_mod_e),
                 ('Expected_mod_rand', Expected_mod_rand)]

# 結果を格納するための空のDataFrameを作成
results = pd.DataFrame(columns=[' '] + [exp[0] for exp in expected_list])

# 各行列の組み合わせについて比較を行う
for matrix in matrix_list:
    row = {}
    row[' '] = matrix[0]
    for expected in expected_list:
        row[expected[0]] = np.array_equal(matrix[1], expected[1])
    results = results.append(row, ignore_index=True)

# 結果を出力
# print(results.to_string(index=False, justify='center', col_space=10))
print(results)

latex_output = results.to_latex(index=False)
print(latex_output)
