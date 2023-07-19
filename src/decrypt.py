import argparse
import glob
import os
import pickle
import sys
from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from utils import print_matrix


def load_cipher_data(filename):
    with open(filename, "rb") as f:
        p, l, k, generator, cipher_matrix, cipher_str = pickle.load(f)
    return p, l, k, generator, cipher_matrix, cipher_str


def get_cipher_data(filename=None):
    if filename:
        if not os.path.exists(filename):
            print(f"Error: No such file '{filename}'")
            sys.exit(1)
    else:
        files = glob.glob("dist/*_cipher_data.pkl")
        if not files:
            print("Error: No cipher data files found in 'dist/' directory.")
            sys.exit(1)
        filename = max(files, key=os.path.getctime)
    return load_cipher_data(filename)


def decrypt(p, l, k, r_0, generator, cipher_matrix):
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
    inverse_cyclotomic_matrix = inverse_cyclotomic_matrix.astype(int)
    print_matrix(inverse_cyclotomic_matrix, "Int version of it")

    matrix_converter = MatrixConverter(l, p)

    print_matrix(cipher_matrix, "Cypher Matrix")

    decrypted_message_matrix = inverse_cyclotomic_matrix @ cipher_matrix
    print_matrix(decrypted_message_matrix, "Message Matrix")

    # decrypted_message_str = matrix_converter.matrix_to_str(decrypted_message_matrix)
    decrypted_message_str = 'hoge'
    print(f"Decrypted Message: {decrypted_message_str}")

    return decrypted_message_matrix, decrypted_message_str


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
    else:
        filename = None

    p, l, k, generator, cipher_matrix, cipher_str = get_cipher_data(filename)

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

    decrypt(p, l, k, r_0, generator, cipher_matrix)


if __name__ == "__main__":
    print("------ Decrypt ------\n")
    main()
