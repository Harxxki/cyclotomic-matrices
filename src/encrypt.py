import sys
import pickle
import datetime

from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from utils import print_matrix


def encrypt_message(p, l, generator, k, message_str):
    # Convert the message string to a message matrix
    mc = MatrixConverter(l)
    message_matrix = mc.str_to_matrix(message_str)

    # Generate the cyclotomic matrix
    cm = CyclotomicMatrix(p, l, generator, k)
    cyclotomic_matrix = cm.get(only_n=True)

    # Encrypt the message
    cipher_matrix = cyclotomic_matrix @ message_matrix

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

    print_matrix(cipher_matrix, "Cypher Matrix")
    print(f"Ciphertext: {cipher_str}")

    save_variables_to_file(p, l, k, generator, cipher_matrix, cipher_str)


if __name__ == "__main__":
    main()
