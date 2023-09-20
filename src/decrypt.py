import sys
import argparse
from typing import NamedTuple, Optional, Tuple

import numpy as np
import os
import glob
import pickle
from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from src.utils import print_matrix


class SecretKey(NamedTuple):
    p: int
    l: int
    private_generator: int
    r_0: int


class DecryptParameters:
    def __init__(self, p, l, k, public_generator, secret_key, cipher_matrix=None, cipher_str=None):
        self.p = p
        self.l = l
        self.k = k
        self.public_generator = public_generator
        self.secret_key = secret_key
        self.cipher_matrix = cipher_matrix
        self.cipher_str = cipher_str

        if self.cipher_matrix is None and self.cipher_str is None:
            raise ValueError("Either cipher_matrix or cipher_str must be provided.")
        elif self.cipher_matrix is None and self.cipher_str is not None:
            mc = MatrixConverter(self.l, self.p)
            self.cipher_matrix = mc.str_to_matrix(self.cipher_str)


def decrypt_message(params: DecryptParameters) -> Tuple[np.ndarray, str]:
    """
    Decrypt a message using the cyclotomic matrix.
    :param params: DecryptParameters
    :return: decrypted_matrix, decrypted_message
    """
    cm = CyclotomicMatrix(params.p, params.l, params.secret_key.private_generator, params.k)

    cyclotomic_matrix_b_0 = cm.get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_b_0, "Cyclotomic Matrix B_0")
    cyclotomic_matrix_d = cm.mul(params.secret_key.r_0)._calc().get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix_d, "Cyclotomic Matrix D (multiplied by r_0 and mod e)")

    inverse_cyclotomic_matrix = cm.inv()
    print_matrix(inverse_cyclotomic_matrix, "Inverse Cyclotomic Matrix (Z or D^*)")
    inverse_cyclotomic_matrix = inverse_cyclotomic_matrix.astype(int)
    print_matrix(inverse_cyclotomic_matrix, "Int version of it")

    matrix_converter = MatrixConverter(params.l, params.p)

    decrypted_matrix = inverse_cyclotomic_matrix @ params.cipher_matrix
    print_matrix(decrypted_matrix, "Decrypted Message Matrix")

    print_matrix(np.mod(decrypted_matrix, params.p), "Message Matrix (Modulused by p)")
    decrypted_message = matrix_converter.matrix_to_str(decrypted_matrix)

    return decrypted_matrix, decrypted_message


def load_cipher_data(filename):
    with open(filename, "rb") as f:
        p, l, k, public_generator, private_generator, r_0, cipher_matrix, cipher_str = pickle.load(
            f)
    return p, l, k, public_generator, private_generator, r_0, cipher_matrix, cipher_str


def validate_args(args):
    if args.mode == "dump":
        # "dump"の場合、--datetime以外の引数はすべてNoneであることを期待
        if any([args.p, args.l, args.k, args.public_generator, args.cipher_str,
                args.private_generator, args.r_0]):
            raise ValueError('In "dump" mode, other arguments should not be provided.')
    elif args.mode == "manual":
        # "manual"の場合、--datetime以外の引数はすべてNoneでないことを期待
        if not all([args.p, args.l, args.k, args.public_generator, args.cipher_str,
                    args.private_generator, args.r_0]):
            raise ValueError('In "manual" mode, all arguments must be provided.')
    else:
        raise ValueError('Invalid mode specified. Please use "dump" or "manual".')


def main():
    parser = argparse.ArgumentParser(description='Decrypt a message.')
    parser.add_argument('mode', type=str,
                        help='The mode of the decrypt. "dump": using dump, "manual": using manual input (including secret values).')
    parser.add_argument('-p', type=int, help='Public value, order of F^*_p.')
    parser.add_argument('-l', type=int, help='Public parameter l.')
    parser.add_argument('-k', type=int, help='Public parameter k.')
    parser.add_argument('--public_generator', type=int, help='Public generator (gamma prime).')
    parser.add_argument('-d', '--datetime',
                        help='The datetime string in format %Y%m%d_%H%M%S using for the filename.')
    parser.add_argument('-c', '--cipher_str', type=str, help='The cipher string.')
    parser.add_argument('--private_generator', type=int,
                        help='Secret generator (gamma double prime).')
    parser.add_argument('-r_0', type=int, help='Secret value r_0.')

    args = parser.parse_args()
    validate_args(args)

    if args.mode == "dump":
        if args.datetime:
            filename = f"dist/{args.datetime}_cipher_data.pkl"
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Error: No such file '{filename}'")
            p, l, k, public_generator, private_generator, r_0, cipher_matrix, cipher_str = load_cipher_data(
                filename)
        else:  # datetimeが指定されていない場合、最新のファイルを読み込む
            files = glob.glob("dist/*_cipher_data.pkl")
            if not files:
                print("Error: No cipher data files found in 'dist/' directory.")
                sys.exit(1)
            filename = max(files, key=os.path.getctime)
            p, l, k, public_generator, private_generator, r_0, cipher_matrix, cipher_str = load_cipher_data(
                filename)
        secret_key = SecretKey(p, l, private_generator, r_0)
        params = DecryptParameters(p, l, k, public_generator, secret_key, cipher_matrix, cipher_str)
    else:  # args.mode == "manual"
        secret_key = SecretKey(args.p, args.l, args.private_generator, args.r_0)
        params = DecryptParameters(args.p, args.l, args.k, args.public_generator, secret_key, None,
                                   args.cipher_str)

    print(f"[Decrypt] Decrypt Parameters: {params}")

    decrypted_matrix, decrypted_message = decrypt_message(params)
    print(f"[Decrypt] Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    print("------ Decrypt ------\n")
    main()
