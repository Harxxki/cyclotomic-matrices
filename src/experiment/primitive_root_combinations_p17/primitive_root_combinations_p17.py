"""
primitive_root_combinations_p17.py

このスクリプトは、p=17の原始元の組み合わせを探し、特定の合同算術条件を満たすかどうかを表示する。
与えられた二つの原始元 gamma_prime と gamma_prime_prime、および指数 r に対して、以下の条件を確認する：
1. gamma_prime^r は gamma_prime_prime mod 17 と合同
2. gamma_prime_prime^r は gamma_prime mod 17 と合同 (あるいは合同でない)

結果は、両方の条件を満たす組み合わせと満たさない組み合わせに分けて表示される。
"""


def power_mod(base, exponent, modulus):
    return pow(base, exponent, modulus)


def find_combinations():
    p = 17
    primitive_roots = [3, 5, 6, 7, 10, 11, 12, 14]

    satisfying_combinations = []
    non_satisfying_combinations = []

    for g1 in primitive_roots:
        for g2 in primitive_roots:
            for r in range(1, p):
                if power_mod(g1, r, p) == g2:
                    if power_mod(g2, r, p) == g1:
                        satisfying_combinations.append((g1, g2, r))
                    else:
                        non_satisfying_combinations.append((g1, g2, r))

    print("Satisfying Combinations:")
    for combo in satisfying_combinations:
        print(combo)

    print("\nNon-Satisfying Combinations:")
    for combo in non_satisfying_combinations:
        print(combo)

    # 結果のサマリー
    print("\n--- サマリー ---")
    print(f"条件を満たす組み合わせの数: {len(satisfying_combinations)}")
    print(f"条件を満たさない組み合わせの数: {len(non_satisfying_combinations)}")


find_combinations()
