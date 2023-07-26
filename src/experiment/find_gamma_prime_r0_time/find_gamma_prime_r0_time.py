import pickle

import sympy
import random
import time

import os
from datetime import datetime

from src.experiment.find_gamma_prime_r0_time.plot_results_from_file import plot_results_from_file


def is_generator_optimized(g, p):
    """Check if g is a generator of F_p using optimized algorithm."""
    for f in sympy.factorint(p - 1):
        if pow(g, (p - 1) // f, p) == 1:
            return False
    return True


def find_generator(p):
    """Find a generator of F_p."""
    for g in range(1, p):
        if is_generator_optimized(g, p):
            return g


def find_r_gamma_current(p, gamma_prime):
    """Find r_0 and gamma_prime_prime using the current algorithm."""
    while True:
        r_0 = random.randint(1, p - 1)
        gamma_prime_prime = random.randint(1, p - 1)
        if is_generator_optimized(gamma_prime_prime, p) and pow(gamma_prime_prime, r_0,
                                                                p) == gamma_prime:
            return r_0, gamma_prime_prime


def find_r_gamma_proposed(p, gamma_prime):
    """Find r_0 and gamma_prime_prime using the proposed algorithm."""
    while True:
        gamma_prime_prime = random.randint(1, p - 1)
        if is_generator_optimized(gamma_prime_prime, p):
            for r_0 in range(1, p):
                if pow(gamma_prime_prime, r_0, p) == gamma_prime:
                    return r_0, gamma_prime_prime


def average_time_over_trials(algorithm, trials, p, gamma_prime):
    """Average the execution time of an algorithm over multiple trials."""
    total_time = 0
    for _ in range(trials):
        start_time = time.time()
        algorithm(p, gamma_prime)
        total_time += time.time() - start_time
    return total_time / trials


def save_results(p_values, trials):
    """Calculate and save the average execution time of both algorithms."""
    times_current = []
    times_proposed = []

    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('dump', f'results_{now_str}.pkl')

    for p in p_values:
        print(f"p = {p}: start")
        gamma_prime = find_generator(p)  # Finding gamma_prime for each p
        times_current.append(average_time_over_trials(find_r_gamma_current, trials, p, gamma_prime))
        times_proposed.append(
            average_time_over_trials(find_r_gamma_proposed, trials, p, gamma_prime))
        # Save intermediate results
        with open(filename, 'wb') as f:
            pickle.dump((p_values[:len(times_current)], times_current, times_proposed), f)

    return filename


p_values = list(sympy.primerange(2 ** 0,
                                 2 ** 32))  # Adjust the range of primes depending on your computational power.
trials = 10
filename = save_results(p_values, trials)
plot_results_from_file(filename)
