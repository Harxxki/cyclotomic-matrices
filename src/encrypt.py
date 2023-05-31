import sys

from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter
from utils import print_matrix


def main():
    if len(sys.argv) < 6:
        print("Please provide the values of p, l, generator, k, message as command line arguments.")
        return

    p = int(sys.argv[1])
    l = int(sys.argv[2])
    generator = int(sys.argv[3])
    k = int(sys.argv[4])
    message_str = sys.argv[5]

    # Convert the message string to a message matrix
    mc = MatrixConverter(l)
    message_matrix = mc.str_to_matrix(message_str)
    print_matrix(message_matrix, "Message Matrix")

    # Generate the cyclotomic matrix
    cm = CyclotomicMatrix(p, l, generator, k)
    cyclotomic_matrix = cm.get(only_n=True)
    print_matrix(cyclotomic_matrix, "Cyclotomic Matrix")

    # Encrypt the message
    encrypted_matrix = cyclotomic_matrix @ message_matrix
    print_matrix(encrypted_matrix, "Encrypted Matrix")

    # Convert the encrypted matrix to a string
    encrypted_message = mc.matrix_to_str(encrypted_matrix)
    print(f"Encrypted Message: {encrypted_message}")


if __name__ == "__main__":
    main()
