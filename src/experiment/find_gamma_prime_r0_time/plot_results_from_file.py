import matplotlib.pyplot as plt
import pickle
import sys


def plot_results_from_file(filename):
    """Plot the average execution time of both algorithms from a pickle file."""
    with open(filename, 'rb') as f:
        p_values, times_current, times_proposed = pickle.load(f)

    plt.figure(figsize=(10, 5))
    plt.plot(p_values, times_current, marker='o', label='Current algorithm')
    plt.plot(p_values, times_proposed, marker='o', label='Proposed algorithm')
    plt.title('Average time required to solve DLP vs. p')
    plt.xlabel('p')
    plt.ylabel('Average time (seconds)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the filename as a command line argument.")
        sys.exit(1)
    filename = sys.argv[1]
    plot_results_from_file(filename)
