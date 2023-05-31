# Cyclotomic Matrices

An implementation of the algorithm described in the paper [A Public Key Cryptosystem Using Cyclotomic Matrices](https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices)[^1].

[^1]:
    Md. Helal Ahmed, Jagmohan Tanti, and Sumant Pushp,
    A Public Key Cryptosystem Using Cyclotomic Matrices,
    Coding Theory - Recent Advances, New Perspectives and Applications,
    June 2019.
    Also available at https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices.



## Using `decrypt.py`

The `decrypt.py` script is a command-line utility that allows you to decrypt a message that was encrypted using the `encrypt.py` script. The script requires various parameters that can be either provided as command line arguments or retrieved from a previous run of the `encrypt.py` script, stored in a pickle dump file.

### Required Arguments

- `r_0`: This is a required argument for decryption. It is a number used during the multiplication operation in the decryption process.

### Optional Arguments

- `p`, `l`, `k`, `generator`: These are optional parameters that were used during the encryption process. If not specified, they will be loaded from the latest pickle dump file available.

- `datetime`: This option can be used to specify a particular pickle dump file from which to load parameters. The date and time should be in the format "YYYYMMDD_HHMMSS". If this option is not used, parameters will be loaded from the latest pickle dump file.

- `cipher_str`: The encrypted message string. If not specified, the string will be loaded from the same pickle dump file the other parameters are loaded from.

### Usage Examples

1. **Providing all arguments:**
```bash
python decrypt.py 10 -p 3 -l 2 -k 1 -g 2 -d 20230530_124512 -s "encrypted string"
```
In this example, `r_0` is 10 and `p`=3, `l`=2, `k`=1, `generator`=2, `datetime`="20230530_124512", `cipher_str`="encrypted string" are provided as arguments. Decryption will proceed using these specific parameters.

2. **Providing some arguments:**
```bash
python decrypt.py 10 -p 3 -l 2
```
In this example, `r_0` is 10 and `p`=3, `l`=2 are provided as arguments. `k`, `generator`, `datetime`, and `cipher_str` will be loaded from the latest available pickle dump file.

3. **Providing only the required argument:**
```bash
python decrypt.py 10
```
In this example, only `r_0` is provided. All other parameters (`p`, `l`, `k`, `generator`, `datetime`, `cipher_str`) will be loaded from the latest available pickle dump file.

The `decrypt.py` script allows for flexible combination of parameters, enabling decryption operations based on the specific requirements of your use case.


## Author

- Haruki MORI ([@Harxxki](https://github.com/Harxxki))
