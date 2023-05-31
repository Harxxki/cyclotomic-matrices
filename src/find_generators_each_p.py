def generators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a ** x) % n)
        if g == s:
            results.append(a)
    return results


for i in range(100):
    gens = generators(i)
    if gens:
        print(f"Z_{i} has generators {gens}")
