# サイクロトミック行列

[A Public Key Cryptosystem Using Cyclotomic Matrices](https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices)
の実装。

## `encrypt.py`の使用方法

`encrypt.py`スクリプトは、メッセージを暗号化するためのコマンドラインユーティリティです。このスクリプトは、コマンドライン引数として提供することができるいくつかのパラメータを必要とします。

### 必須の引数

- `message`: 暗号化したいメッセージ。
- `order`: 素数、\(F^*_p\)のオーダー。
- `l`: パラメータ\(l\)。
- `k`: パラメータ\(k\)。

### オプションの引数

- `-g`, `--private_generator`: プライベートジェネレータ。指定されていない場合、ランダムなジェネレータが選ばれます。

### 使用例

1. **すべての引数を提供する場合:**

```bash
python encrypt.py "Your Message Here" 41 2 5 -g 2
```

この例では、メッセージ "Your Message Here" が `order`=41、`l`=2、`k`=5、および `private_generator`=2 を使用して暗号化されます。

2. **必須の引数のみを提供する場合:**

```bash
python encrypt.py "Your Message Here" 41 2 5
```

この例では、メッセージ "Your Message Here" が `order`=41、`l`=2、および `k`=5 を使用して暗号化されます。ランダムな `private_generator` が選ばれます。

`encrypt.py`スクリプトは、暗号化されたメッセージ、暗号行列、およびその他の関連するパラメータを表示します。これらのパラメータは、後で復号化で使用するためにファイルに保存されます。

## `decrypt.py`の使用方法

`decrypt.py`スクリプトは、`encrypt.py`
スクリプトを使用して暗号化されたメッセージを復号化するためのコマンドラインユーティリティです。このスクリプトは、コマンドライン引数として提供するか、`encrypt.py`
スクリプトの前回の実行から保存されたpickleダンプファイルから取得することができるいくつかのパラメータを必要とします。

### 必須の引数

- `mode`: 復号化のモード。"dump"（ダンプファイルを使用）または "manual"（必要なすべてのパラメータを手動で提供）のいずれかです。

### オプションの引数

- `-p`: 公開値、\(F^*_p\)のオーダー。
- `-l`: 公開パラメータ\(l\)。
- `-k`: 公開パラメータ\(k\)。
- `--public_generator`: 公開ジェネレータ（ガンマプライム）。
- `-d`, `--datetime`: ファイル名に使用される日時文字列の形式 `%Y%m%d_%H%M%S`。これは、特定のpickleダンプファイルからパラメータをロードするために使用されます。
- `-c`, `--cipher_str`: 暗号化されたメッセージ文字列。
- `--private_generator`: 秘密のジェネレータ（ガンマダブルプライム）。
- `-r_0`: 秘密の値 \(r_0\)。

### 使用例

1. **dumpモードを使用する場合:**

```bash
python decrypt.py dump
```

この例では、スクリプトは自動的に最新の利用可能なpickleダンプファイルから必要なパラメータをロードし、復号化を進めます。

2. **特定の日時でdumpモードを使用する場合:**

```bash
python decrypt.py dump -d 20230530_124512
```

この例では、スクリプトは指定されたpickleダンプファイルから必要なパラメータをロードし、復号化を進めます。

3. **manualモードを使用する場合:**

```bash
python decrypt.py manual -p 41 -l 2 -k 5 --public_generator 17 -c "encrypted string" --private_generator 30 -r_0 31
```

この例では、すべての必要なパラメータが手動で提供され、スクリプトはこれらの特定のパラメータを使用して復号化を進めます。

`decrypt.py`スクリプトは、復号化されたメッセージ、復号化された行列、およびその他の関連する行列を表示します。

## Author

Haruki Mori ([@Harxxki](https://github.com/Harxxki))
