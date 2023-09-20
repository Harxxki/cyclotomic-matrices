import sys
import pickle
import datetime

import numpy as np

from src.cyclotomic_matrix import CyclotomicMatrix
from src.find_generators import find_generators
from src.matrix_converter import MatrixConverter
from src.utils import find_public_generator, is_generator, is_prime, print_matrix
from typing import Tuple, Union
import argparse
import random


def encrypt_message(p: int, l: int, public_generator: int, k: int,
                    message_input: Union[str, np.ndarray]) -> Tuple[np.ndarray, str]:
    """
    Encrypt a message using the cyclotomic matrix.
    :rtype: object
    :param p:
    :param l:
    :param public_generator:
    :param k:
    :param message_input: plaintext or message matrix
    :return:
    """
    # Convert the message input to a message matrix
    mc = MatrixConverter(l, p)
    if isinstance(message_input, str):
        message_matrix = mc.str_to_matrix(message_input)
    elif isinstance(message_input, np.ndarray):
        message_matrix = message_input
    else:
        raise TypeError("message_input must be either a string or a numpy ndarray")

    print_matrix(message_matrix, "Message Matrix")

    # Generate the cyclotomic matrix
    cm = CyclotomicMatrix(p, l, public_generator, k)
    cyclotomic_matrix = cm.get(matrix_format="calculated")
    print_matrix(cyclotomic_matrix, "Cyclotomic Matrix")
    # Check if the matrix is invertible
    if np.linalg.det(cyclotomic_matrix) == 0:
        print("Error: The cyclotomic matrix is not invertible.")
        sys.exit(1)

    # Encrypt the message
    cipher_matrix = cyclotomic_matrix @ message_matrix
    print_matrix(cipher_matrix, "Cipher Matrix")

    # Convert the encrypted matrix to a string
    cipher_str = mc.matrix_to_str(cipher_matrix)

    return cipher_matrix, cipher_str


def save_variables_to_file(p: int, l: int, k: int, public_generator: int, private_generator: int,
                           r_0: int, cipher_matrix, cipher_str):
    # Save the variables to a file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"dist/{timestamp}_cipher_data.pkl", "wb") as f:
        pickle.dump((p, l, k, public_generator, private_generator, r_0, cipher_matrix, cipher_str),
                    f)


def main():
    parser = argparse.ArgumentParser(description='Encrypt a message.')
    parser.add_argument('message', type=str, help='The message to encrypt.')
    parser.add_argument('order', type=int, help='Prime number, Order of F^*_p.')
    parser.add_argument('l', type=int, help='The parameter l.')
    parser.add_argument('k', type=int, help='The parameter k.')
    parser.add_argument('-g', '--private_generator', type=int, help='The private generator.')
    if len(sys.argv) < 4:
        print(
            "[Encrypt] Please provide the values of message, p, l, k as command line arguments.")
        return

    args = parser.parse_args()

    if not is_prime(args.order):
        raise ValueError("[Encrypt] Order should be prime number.")

    message = args.message
    p = args.order
    l = args.l
    k = args.k
    if args.private_generator:
        if not is_generator(args.private_generator, p):
            raise ValueError("[Encrypt] Provided private generator is not a generator of F_p.")
        private_generator = args.private_generator
        print(
            f"[Encrypt] Using given private generator (gamma double prime) = {args.private_generator}")
    else:
        private_generator = random.choice(find_generators(p))
        print(
            f"[Encrypt] Using random private generator (gamma double prime) = {private_generator}")

    public_generator, r_0 = find_public_generator(private_generator, p)
    print(f"[Encrypt] Generated public generator (gamma prime) = {public_generator}")
    print(f"[Encrypt] Generated r_0 = {r_0}")
    print(
        f"[Encrypt] All params: {p=}, {l=}, {k=}, {private_generator=}, {public_generator=}, {r_0=}")

    cipher_matrix, cipher_str = encrypt_message(p, l, public_generator, k, message)

    print_matrix(cipher_matrix, "Cipher Matrix")
    print(f"[Encrypt] Ciphertext: {cipher_str}")

    save_variables_to_file(p=p, l=l, k=k, public_generator=public_generator,
                           private_generator=private_generator, r_0=r_0,
                           cipher_matrix=cipher_matrix, cipher_str=cipher_str)


if __name__ == "__main__":
    print("------ Encrypt ------\n")
    main()
