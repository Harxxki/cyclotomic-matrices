import argparse

import numpy as np
import pytest
from src.decrypt import (
    SecretKey,
    DecryptParameters,
    decrypt_message,
    load_cipher_data,
    validate_args,
    main
)
import pickle


def test_secret_key_class():
    secret_key = SecretKey(p=1, l=2, private_generator=3, r_0=4)
    assert secret_key.p == 1
    assert secret_key.l == 2
    assert secret_key.private_generator == 3
    assert secret_key.r_0 == 4


def test_decrypt_parameters_class():
    # Both cipher_matrix and cipher_str are None
    with pytest.raises(ValueError):
        DecryptParameters(p=41, l=2, k=5, public_generator=None, secret_key=SecretKey(1, 2, 3, 4),
                          cipher_matrix=None, cipher_str=None)

    # Only cipher_str is given
    params = DecryptParameters(p=41, l=2, k=5, public_generator=None,
                               secret_key=SecretKey(p=41, l=2, private_generator=34, r_0=17),
                               cipher_matrix=None,
                               cipher_str="ttnbl. n.diif,atndoo. fma, b, c,kcok, alkcok, alceimg,fuae,bf,cg")
    expected_cipher_matrix = np.array([[22, 22, 16, 4, 14, 2, 0, 16],
                                       [2, 6, 11, 11, 8, 1, 3, 22],
                                       [16, 6, 17, 17, 2, 0, 8, 15],
                                       [3, 1, 0, 4, 1, 0, 5, 1],
                                       [13, 5, 17, 13, 1, 0, 3, 14],
                                       [13, 5, 17, 13, 1, 0, 3, 14],
                                       [5, 7, 11, 15, 9, 1, 8, 23],
                                       [3, 7, 1, 4, 8, 1, 5, 9]])
    assert np.array_equal(params.cipher_matrix, expected_cipher_matrix)


def test_decrypt_message():
    params = DecryptParameters(p=41, l=2, k=5, public_generator=17,
                               secret_key=SecretKey(p=41, l=2, private_generator=30, r_0=31),
                               cipher_matrix=None,
                               cipher_str="vtxmm.a1c,hm. fmndoo. fmice.    .diif,atndoo. fmae,bf,cg d, e, f")
    matrix, message = decrypt_message(params)
    assert matrix is not None
    assert message.strip() == "a, b, c, d, e, f. hi, alice."


def test_load_cipher_data(tmp_path):
    data = (1, 1, 1, 1, 1, 1, None, "test")
    file_path = tmp_path / "test.pkl"

    with open(file_path, "wb") as f:
        pickle.dump(data, f)

    loaded_data = load_cipher_data(file_path)
    assert loaded_data == data


def test_validate_args():
    # "dump" mode test
    args = argparse.Namespace(
        mode="dump",
        p=None, l=None, k=None,
        public_generator=None, datetime=None,
        cipher_str=None, private_generator=None, r_0=None
    )
    validate_args(args)  # Should not raise an exception

    # "manual" mode test
    args = argparse.Namespace(
        mode="manual",
        p=1, l=1, k=1,
        public_generator=1, datetime=1,
        cipher_str="test", private_generator=1, r_0=1
    )
    validate_args(args)  # Should not raise an exception

    # Invalid mode test
    args = argparse.Namespace(mode="invalid")
    with pytest.raises(ValueError):
        validate_args(args)


def test_main_dump_mode(tmp_path, mocker, capsys):
    data = (1, 1, 1, 1, 1, 1, None, "test")
    file_path = tmp_path / "test_cipher_data.pkl"

    with open(file_path, "wb") as f:
        pickle.dump(data, f)

    mocker.patch('sys.argv', ['script_name', 'dump', '--datetime', 'test'])
    main()
    captured = capsys.readouterr()

    assert "Decrypted Message:" in captured.out


def test_main_manual_mode(mocker, capsys):
    # Mock command line arguments for manual mode
    mocker.patch('sys.argv', ['script_name', 'manual', '-p', '1', '-l', '2', '-k', '3',
                              '--public_generator', '4', '-d', 'test', '-c', 'test_cipher',
                              '--private_generator', '5', '-r_0', '6'])
    main()
    captured = capsys.readouterr()

    assert "Decrypted Message:" in captured.out
    # replace with the actual expected message
