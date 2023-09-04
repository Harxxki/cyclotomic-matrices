import time
import random

import sympy
import matplotlib.pyplot as plt


def is_generator_optimized(g, p):
    for f in sympy.factorint(p - 1):
        if pow(g, (p - 1) // f, p) == 1:
            return False
    return True


def find_generator(p):
    """Find a generator of F_p."""
    for _ in range(1, p):
        g = random.randint(1, p)
        if is_generator_optimized(g, p):
            print(f"{g=}")
            return int(g)


def naive_dlp(a, b, p):
    """Solve the discrete logarithm problem using a naive method."""
    for x in range(1, p):
        if pow(a, x, p) == b:
            return x
    return None


def find_r_gamma_fixed(p, gamma_prime):
    """Find r_0 and gamma_prime_prime using the fixed gamma_prime_prime method."""
    gamma_prime_prime = find_generator(p)
    for r_0 in range(1, p):
        if pow(gamma_prime_prime, r_0, p) == gamma_prime:
            print(f"{r_0=} {gamma_prime_prime=}")
            return r_0, gamma_prime_prime


def average_execution_time_over_trials(algorithm, trials, *args):
    """Average the execution time of an algorithm over multiple trials."""
    total_time = 0
    for _ in range(trials):
        start_time = time.time()
        algorithm(*args)
        total_time += time.time() - start_time
    return total_time / trials


def compare_execution_time(p_values, trials):
    """Compare the execution time of the DLP and the current problem."""
    times_dlp = []
    times_current = []

    for p in p_values:
        print(f"p = {p}: start")
        gamma_prime = find_generator(p)
        a = find_generator(p)

        times_dlp.append(average_execution_time_over_trials(naive_dlp, trials, a, gamma_prime, p))
        times_current.append(
            average_execution_time_over_trials(find_r_gamma_fixed, trials, p, gamma_prime))

    return times_dlp, times_current


def plot_execution_time(p_values, times_dlp, times_current):
    """Plot the execution time of the DLP and the current problem."""
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, times_dlp, label='DLP')
    plt.plot(p_values, times_current, label='Current Problem')
    plt.xlabel('Size of p')
    plt.ylabel('Execution Time (s)')
    plt.legend()
    plt.grid(True)
    plt.title('Comparison of Execution Time')
    plt.show()


p_values = list(sympy.primerange(2 ** 0,
                                 2 ** 16))  # Adjust the range of primes depending on your computational power.
trials = 10
times_dlp, times_current = compare_execution_time(p_values, trials)
plot_execution_time(p_values, times_dlp, times_current)
