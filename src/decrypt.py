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

    r_0 = args.r_0

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

    print("Encrypt Parameters:")
    print(f"{p=}, {l=}, {k=}, {r_0=}, {encrypt_generator=}, {decrypt_generator=} \n")

    cm = CyclotomicMatrix(p, l, decrypt_generator, k)
    cyclotomic_matrix_b_0 = cm.get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_b_0, "Cyclotomic Matrix B_0")
    cyclotomic_matrix_d = cm.mul(r_0)._calc().get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_d, "Cyclotomic Matrix D (multiplied by r_0 and mod e)")

    inverse_cyclotomic_matrix = cm.inv()
    print_matrix(inverse_cyclotomic_matrix, "Inverse Cyclotomic Matrix (Z or D^*)")

    matrix_converter = MatrixConverter(l)

    print_matrix(cipher_matrix, "Cypher Matrix")

    message_matrix = inverse_cyclotomic_matrix @ cipher_matrix
    print_matrix(message_matrix, "Message Matrix")

    message_str = matrix_converter.matrix_to_str(message_matrix)
    print(f"Decrypted Message: {message_str}")


if __name__ == "__main__":
    print("------ Decrypt ------\n")
    main()
