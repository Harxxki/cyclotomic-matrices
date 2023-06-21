import sys
import math
import argparse
import random
import numpy as np
import os
import glob
import pickle
from find_generators import find_generators
from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from utils import print_matrix


def load_cipher_data(filename):
    with open(filename, "rb") as f:
        p, l, k, generator, cipher_matrix, cipher_str = pickle.load(f)
    return p, l, k, generator, cipher_matrix, cipher_str


def main():
    parser = argparse.ArgumentParser(description='Decrypt a message.')
    parser.add_argument('r_0', type=int, help='Random value.')
    parser.add_argument('-p', type=int, help='The prime number.')
    parser.add_argument('-l', type=int, help='The parameter l.')
    parser.add_argument('-k', type=int, help='The parameter k.')
    parser.add_argument('-g', '--generator', type=int, help='The generator.')
    parser.add_argument('-d', '--datetime', help='The datetime string in format %Y%m%d_%H%M%S.')
    parser.add_argument('-s', '--cipher_str', help='The cipher string.')

    args = parser.parse_args()

    if args.datetime:
        filename = f"dist/{args.datetime}_cipher_data.pkl"
        if not os.path.exists(filename):
            print(f"Error: No such file '{filename}'")
            sys.exit(1)
        p, l, k, generator, cipher_matrix, cipher_str = load_cipher_data(filename)
    else:
        files = glob.glob("dist/*_cipher_data.pkl")
        if not files:
            print("Error: No cipher data files found in 'dist/' directory.")
            sys.exit(1)
        filename = max(files, key=os.path.getctime)
        p, l, k, generator, cipher_matrix, cipher_str = load_cipher_data(filename)

    if args.r_0:
        r_0 = args.r_0
    else:
        r_0 = random.randint(1, p-1)
        print(f"r_0 is now determined randomly.: {r_0}")
    if args.p:
        p = args.p
    if args.l:
        l = args.l
    if args.k:
        k = args.k
    if args.generator:
        generator = args.generator
    if args.cipher_str:
        cipher_str = args.cipher_str

    encrypt_generator = generator
    decrypt_generator = pow(encrypt_generator, r_0, p)
    cm = CyclotomicMatrix(p, l, decrypt_generator, k).mul(args.r_0)._calc()
    cyclotomic_matrix = cm.get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix, "Cyclotomic Matrix")

    mc = MatrixConverter(l)
    # Check if the matrix is invertible
    if np.linalg.det(cyclotomic_matrix) == 0:
        print("cyclotomic matrix is not invertible.")
    else:
        print("cyclotomic matrix is invertible.")

    # # 行列の各要素に対してF_p上での逆元を求める ("逆行列"ではない)
    # inverse_cyclotomic_matrix = np.empty_like(cyclotomic_matrix)
    # for i in range(cyclotomic_matrix.shape[0]):
    #     for j in range(cyclotomic_matrix.shape[1]):
    #         element = int(cyclotomic_matrix[i, j])
    #         if math.gcd(element, p) == 1:  # Ensure that the element has an inverse modulo p
    #             inverse_cyclotomic_matrix[i, j] = pow(element, -1, p)
    #         else:
    #             print(f"Element {element} at ({i}, {j}) does not have an inverse modulo {p}")

    inverse_cyclotomic_matrix = np.linalg.inv(cyclotomic_matrix)
    print_matrix(inverse_cyclotomic_matrix, "Inverse Cyclotomic Matrix (Z)")

    if args.cipher_str:
        cypher_matrix = mc.str_to_matrix(args.cipher_str)
    print_matrix(cypher_matrix, "Cypher Matrix")

    message_matrix = inverse_cyclotomic_matrix @ cypher_matrix
    print_matrix(message_matrix, "Message Matrix")

    message_str = mc.matrix_to_str(message_matrix)
    print(f"Decrypted Message: {message_str}")


if __name__ == "__main__":
    main()
