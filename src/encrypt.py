import sys

from src.cyclotomic_matrix_generator import CyclotomicMatrixGenerator
from src.message_matrix_converter import MessageMatrixConverter


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
    mmc = MessageMatrixConverter(l)
    message_matrix = mmc.str_to_matrix(message_str)
    print("Message Matrix:")
    for row in message_matrix:
        for entry in row:
            print(f"{entry:2}", end=" ")
        print()

    # Generate the cyclotomic matrix
    cmg = CyclotomicMatrixGenerator(p, l, generator, k)
    cyclotomic_matrix = cmg.generate_cyclotomic_matrix()
    print("Cyclotomic Matrix:")
    for row in cyclotomic_matrix:
        for entry in row:
            print(f"{entry.n:2}", end=" ")
        print()

if __name__ == "__main__":
    main()
