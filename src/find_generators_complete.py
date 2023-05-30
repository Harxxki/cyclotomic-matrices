import sys


# gが原始元かどうかをチェックする関数
def is_primitive_root(g, p):
    seen = set()
    for i in range(1, p):
        val = pow(g, i, p)
        seen.add(val)
    return len(seen) == p - 1

# pの原始元を求める関数
def find_primitive_roots(p):
    primitive_roots = [g for g in range(1, p) if is_primitive_root(g, p)]
    return primitive_roots

# コマンドライン引数から素数pを取得
if len(sys.argv) > 1:
    p = int(sys.argv[1])
    print(find_primitive_roots(p))
else:
    print("Please provide a prime number as an argument.")
