import sys

from src.cyclotomic_matrix import CyclotomicMatrix
from src.matrix_converter import MatrixConverter


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
    print("Message Matrix:")
    for row in message_matrix:
        for entry in row:
            print(f"{entry:2}", end=" ")
        print()

    # Generate the cyclotomic matrix
    cm = CyclotomicMatrix(p, l, generator, k)
    cyclotomic_matrix = cm.get(only_n=True)
    print("Cyclotomic Matrix:")
    for row in cyclotomic_matrix:
        for entry in row:
            print(f"{entry:2}", end=" ")
        print()


if __name__ == "__main__":
    main()
