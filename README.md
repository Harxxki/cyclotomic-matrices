# Cyclotomic Matrices

An implementation of the algorithm described in the
paper [A Public Key Cryptosystem Using Cyclotomic Matrices](https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices).

## Using `encrypt.py`

The `encrypt.py` script is a command-line utility that allows you to encrypt a message. The script requires various
parameters that can be either provided as command line arguments.

### Required Arguments

- `message`: The message you want to encrypt.
- `order`: Prime number, Order of \(F^*_p\).
- `l`: The parameter \(l\).
- `k`: The parameter \(k\).

### Optional Arguments

- `-g`, `--private_generator`: The private generator. If not specified, a random generator will be chosen.

### Usage Examples

1. **Providing all arguments:**

```bash
python encrypt.py "Your Message Here" 41 2 5 -g 2
```

In this example, the message "Your Message Here" will be encrypted using `order`=41, `l`=2, `k`=5,
and `private_generator`=2.

2. **Providing only the required arguments:**

```bash
python encrypt.py "Your Message Here" 41 2 5
```

In this example, the message "Your Message Here" will be encrypted using `order`=41, `l`=2, and `k`=5. A
random `private_generator` will be chosen.

The `encrypt.py` script will display the encrypted message, the cipher matrix, and other relevant parameters. It will
also save these parameters to a file for later use in decryption.

## Using `decrypt.py`

The `decrypt.py` script is a command-line utility that allows you to decrypt a message that was encrypted using
the `encrypt.py` script. The script requires various parameters that can be either provided as command line arguments or
retrieved from a previous run of the `encrypt.py` script, stored in a pickle dump file.

### Required Arguments

- `mode`: The mode of decryption. It can be either "dump" (using a dump file) or "manual" (providing all the necessary
  parameters manually).

### Optional Arguments

- `-p`: Public value, order of \(F^*_p\).
- `-l`: Public parameter \(l\).
- `-k`: Public parameter \(k\).
- `--public_generator`: Public generator (gamma prime).
- `-d`, `--datetime`: The datetime string in format `%Y%m%d_%H%M%S` used for the filename. This is used to specify a
  particular pickle dump file from which to load parameters.
- `-c`, `--cipher_str`: The encrypted message string.
- `--private_generator`: Secret generator (gamma double prime).
- `-r_0`: Secret value \(r_0\).

### Usage Examples

1. **Using dump mode:**

```bash
python decrypt.py dump
```

In this example, the script will automatically load the necessary parameters from the latest available pickle dump file
and proceed with the decryption.

2. **Using dump mode with a specific datetime:**

```bash
python decrypt.py dump -d 20230530_124512
```

In this example, the script will load the necessary parameters from the specified pickle dump file and proceed with the
decryption.

3. **Using manual mode:**

```bash
python decrypt.py manual -p 41 -l 2 -k 5 --public_generator 17 -c "encrypted string" --private_generator 30 -r_0 31
```

In this example, all the necessary parameters are provided manually, and the script will proceed with the decryption
using these specific parameters.

The `decrypt.py` script will display the decrypted message, the decrypted matrix, and other relevant matrices.

## Author

- Haruki MORI ([@Harxxki](https://github.com/Harxxki))
