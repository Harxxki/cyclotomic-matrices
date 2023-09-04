from typing import List, Tuple

from src.find_generators import find_generators


def find_combinations(p: int) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """指定されたpに対して条件を満たす/満たさない組み合わせを返す"""
    generators = find_generators(p)
    satisfying_combinations = []
    non_satisfying_combinations = []

    for g1 in generators:
        for g2 in generators:
            for r in range(1, p):
                if pow(g1, r, p) == g2:
                    if pow(g2, r, p) == g1:
                        satisfying_combinations.append((g1, g2, r))
                    else:
                        non_satisfying_combinations.append((g1, g2, r))

    return satisfying_combinations, non_satisfying_combinations


def main(p1: int = 10, p2: int = 100):
    if p1 >= p2:
        raise ValueError("p1 should be less than p2.")

    summary = []
    equal_cases = []
    more_satisfying_cases = []

    for p in range(p1, p2 + 1):
        if p < 2:
            continue
        satisfying, non_satisfying = find_combinations(p)
        summary.append((p, len(satisfying), len(non_satisfying)))
        if len(satisfying) == len(non_satisfying):
            equal_cases.append(p)
        elif len(satisfying) > len(non_satisfying):
            more_satisfying_cases.append(p)

    # サマリーの出力
    print("p\t条件を満たす組み合わせ\t条件を満たさない組み合わせ")
    for p, s, ns in summary:
        print(f"{p}\t{s}\t{ns}")

    # 追加: サマリーの拡張部分
    print("\n条件を満たす組み合わせと条件を満たさない組み合わせの数が等しいp:")
    print(", ".join(map(str, equal_cases)))

    print("\n条件を満たす組み合わせの数が条件を満たさない組み合わせよりも多いp:")
    print(", ".join(map(str, more_satisfying_cases)))

    # サマリーの出力 (KaTeX形式)
    table_header = "\\begin{array}{|c|c|c|} \n\hline \n p & \text{条件を満たす組み合わせ} & \text{条件を満たさない組み合わせ} \\\\ \n\hline"
    table_footer = "\hline \n\end{array}"
    table_rows = []

    for p, s, ns in summary:
        table_rows.append(f" {p} & {s} & {ns} \\\\ \hline")

    table_content = "\n".join(table_rows)
    katex_table = f"{table_header} \n {table_content} \n {table_footer}"
    print(katex_table)


if __name__ == "__main__":
    main()
