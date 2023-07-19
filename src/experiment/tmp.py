import numpy as np
import pandas as pd

from src.cyclotomic_matrix import CyclotomicMatrix
from src.encrypt import encrypt_message
from src.utils import print_matrix


def decrypt_with_mod(_p, _l, _k, _r_0, _generator, _cipher_matrix, _modulo=-1):
    encrypt_generator = _generator
    decrypt_generator = pow(encrypt_generator, _r_0, _p)

    print("Encrypt Parameters:")
    print(f"{_p=}, {_l=}, {_k=}, {_r_0=}, {encrypt_generator=}, {decrypt_generator=} \n")

    cm = CyclotomicMatrix(_p, _l, decrypt_generator, _k)
    cyclotomic_matrix_b_0 = cm.get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_b_0, "Cyclotomic Matrix B_0")
    cyclotomic_matrix_d = cm.mul(_r_0)._calc().get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_d, "Cyclotomic Matrix D (multiplied by r_0 and mod e)")

    inverse_cyclotomic_matrix = cm.inv()
    if _modulo != -1:
        inverse_cyclotomic_matrix_mod_p = np.mod(inverse_cyclotomic_matrix, _modulo)
        print_matrix(inverse_cyclotomic_matrix_mod_p,
                     "Modulered Inverse Cyclotomic Matrix (Z or D^*)")
        inverse_cyclotomic_matrix = inverse_cyclotomic_matrix_mod_p.astype(int)
        print_matrix(inverse_cyclotomic_matrix, "Int version of it")
    else:
        print_matrix(inverse_cyclotomic_matrix, "Inverse Cyclotomic Matrix (Z or D^*)")
        inverse_cyclotomic_matrix = inverse_cyclotomic_matrix.astype(int)
        print_matrix(inverse_cyclotomic_matrix, "Int version of it")

    print_matrix(_cipher_matrix, "Cypher Matrix")

    decrypted_message_matrix = inverse_cyclotomic_matrix @ _cipher_matrix
    print_matrix(decrypted_message_matrix, "Message Matrix")

    return decrypted_message_matrix


p = 17
e = 8
rand = 3

l = 2
generator = 11
k = 2
r_0 = 7

message_matrix = np.array([
    [2, 3, 5, 9, 8, 0, 2, 1],
    [1, 5, 9, 2, 9, 3, 0, 5],
    [2, 1, 3, 2, 5, 6, 8, 7],
    [5, 3, 0, 7, 8, 7, 3, 1],
    [4, 2, 3, 1, 9, 8, 7, 3],
    [0, 9, 2, 3, 5, 6, 8, 9],
    [1, 0, 2, 9, 6, 7, 9, 8],
    [9, 1, 3, 2, 4, 4, 5, 6]
])

cipher_matrix, _ = encrypt_message(p, l, generator, k, message_matrix)
cyclotomic_matrix = CyclotomicMatrix(p, l, generator, k).get(matrix_format="calculated")
# 正当
Expected = decrypt_with_mod(p, l, k, r_0, generator, cipher_matrix)
# 行列A (Zをmod pしてそのままMessage Matrixを計算)
A = decrypt_with_mod(p, l, k, r_0, generator, cipher_matrix, p)
# 行列B (Zをmod eしてそのままMessage Matrixを計算)
B = decrypt_with_mod(p, l, k, r_0, generator, cipher_matrix, e)
# 行列Rand (Zをmod rand=3してそのままMessage Matrixを計算)
Rand = decrypt_with_mod(p, l, k, r_0, generator, cipher_matrix, rand)

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
