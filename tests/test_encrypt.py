import numpy as np
from src.encrypt import encrypt_message


def test_encrypt_message():
    p = 17
    l = 2
    generator = 11
    k = 2
    message_matrix = np.array([
        [2, 3, 5, 9, 8, 0, 2, 1],
        [1, 5, 9, 2, 9, 3, 0, 5],
        [2, 1, 3, 2, 5, 6, 8, 7],
        [5, 3, 0, 7, 8, 7, 3, 1],
        [4, 2, 3, 1, 9, 8, 7, 3],
        [0, 9, 2, 3, 5, 6, 8, 9],
        [1, 0, 2, 9, 6, 7, 9, 8],
        [9, 1, 3, 2, 4, 4, 5, 6]
    ])

    expected_cipher_matrix = np.array([
        [2, 1, 3, 2, 5, 6, 8, 7],
        [5, 12, 2, 10, 13, 13, 11, 10],
        [11, 4, 8, 11, 12, 4, 7, 7],
        [5, 7, 12, 3, 18, 11, 7, 8],
        [14, 4, 3, 9, 12, 11, 8, 7],
        [2, 5, 11, 11, 15, 10, 9, 13],
        [1, 9, 4, 12, 11, 13, 17, 17],
        [6, 3, 6, 3, 14, 14, 15, 10]
    ])

    cipher_matrix, _ = encrypt_message(p, l, generator, k, message_matrix)

    np.testing.assert_array_equal(cipher_matrix, expected_cipher_matrix)
