import sys
import pickle
import datetime

import numpy as np

from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from src.utils import print_matrix
from typing import Tuple, Union


def encrypt_message(p: int, l: int, generator: int, k: int,
                    message_input: Union[str, np.ndarray]) -> Tuple[np.ndarray, str]:
    """
    Encrypt a message using the cyclotomic matrix.
    :param p:
    :param l:
    :param generator:
    :param k:
    :param message_input: plaintext or message matrix
    :return:
    """
    # Convert the message input to a message matrix
    mc = MatrixConverter(l)
    if isinstance(message_input, str):
        message_matrix = mc.str_to_matrix(message_input)
    elif isinstance(message_input, np.ndarray):
        message_matrix = message_input
    else:
        raise TypeError("message_input must be either a string or a numpy ndarray")

    print_matrix(message_matrix, "Message Matrix")

    # Generate the cyclotomic matrix
    cm = CyclotomicMatrix(p, l, generator, k)
    cyclotomic_matrix = cm.get(only_n=True)
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


def save_variables_to_file(p, l, k, generator, cipher_matrix, cipher_str):
    # Save the variables to a file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"dist/{timestamp}_cipher_data.pkl", "wb") as f:
        pickle.dump((p, l, k, generator, cipher_matrix, cipher_str), f)


def main():
    if len(sys.argv) < 6:
        print("Please provide the values of p, l, generator, k, message as command line arguments.")
        return

    p = int(sys.argv[1])
    l = int(sys.argv[2])
    generator = int(sys.argv[3])
    k = int(sys.argv[4])
    message_str = sys.argv[5]

    cipher_matrix, cipher_str = encrypt_message(p, l, generator, k, message_str)

    print_matrix(cipher_matrix, "Cipher Matrix")
    print(f"Ciphertext: {cipher_str}")

    save_variables_to_file(p, l, k, generator, cipher_matrix, cipher_str)


if __name__ == "__main__":
    main()
