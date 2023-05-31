# 円分行列を用いた暗号方式

[A Public Key Cryptosystem Using Cyclotomic Matrices](https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices)[^1] の実装.

[^1]:
    Md. Helal Ahmed, Jagmohan Tanti, and Sumant Pushp,
    A Public Key Cryptosystem Using Cyclotomic Matrices,
    Coding Theory - Recent Advances, New Perspectives and Applications,
    June 2019.
    Also available at https://www.researchgate.net/publication/356720825_A_Public_Key_Cryptosystem_Using_Cyclotomic_Matrices.

## `decrypt.py` の使い方

`decrypt.py`スクリプトは、`encrypt.py`スクリプトで暗号化されたメッセージを復号するためのコマンドラインユーティリティです。このスクリプトは、コマンドライン引数として提供するか、pickleダンプファイルから読み込むことで必要なパラメータを取得します。

### 必須引数

- `r_0`: 復号処理の乗算操作に使用される数値で、必須の引数です。

### オプション引数

- `p`, `l`, `k`, `generator`: これらは暗号化処理で使用されたオプションのパラメータです。指定しなかった場合、最新のpickleダンプファイルから読み込まれます。

- `datetime`: パラメータを読み込む特定のpickleダンプファイルを指定するために使用します。日時は "YYYYMMDD_HHMMSS" の形式であるべきです。このオプションを使用しない場合、パラメータは最新のpickleダンプファイルから読み込まれます。

- `cipher_str`: 暗号化されたメッセージ文字列です。指定しなかった場合、文字列は他のパラメータと同じpickleダンプファイルから読み込まれます。

### 使用例

1. **すべての引数を指定する:**
```bash
python decrypt.py 10 -p 3 -l 2 -k 1 -g 2 -d 20230530_124512 -s "暗号化された文字列"
```
この例では、`r_0`は10、`p`=3、`l`=2、`k`=1、`generator`=2、`datetime`="20230530_124512"、`cipher_str`="暗号化された文字列"が引数として指定されています。これらの特定のパラメータを使用して復号処理が行われます。

2. **一部の引数を指定する:**
```bash
python decrypt.py 10 -p 3 -l 2
```
この例では、`r_0`は10、`p`=3、`l`=2が引数として指定されています。`k`、`generator`、`datetime`、`cipher_str`は最新の利用可能なpickleダンプファイルから読み込まれます。

3. **必須引数のみを指定する:**
```bash
python decrypt.py 10
```
この例では、`r_0`のみが指定されています。他のすべてのパラメータ（`p`、`l`、`k`、`generator`、`

datetime`、`cipher_str`）は最新の利用可能なpickleダンプファイルから読み込まれます。

`decrypt.py`スクリプトは、パラメータの組み合わせを柔軟に扱うことができ、特定の使用ケースに基づいた復号操作を可能にします。


## 作成者

- Haruki MORI ([@Harxxki](https://github.com/Harxxki))
