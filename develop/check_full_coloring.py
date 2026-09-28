"""Independently check a full coloring against the graph definition, using only stdlib."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def dot(x, y):
    return sum(((x >> i) % 2) * ((y >> i) % 2) for i in range(6)) % 2


def span(basis):
    result = set()
    for bits in product((0, 1), repeat=len(basis)):
        value = 0
        for bit, row in zip(bits, basis):
            if bit:
                value ^= row
        result.add(value)
    return frozenset(result)


def gaussian(n, k):
    if k == 0 or k == n:
        return 1
    return gaussian(n - 1, k) + 2 ** (n - k) * gaussian(n - 1, k - 1)


def check(path):
    data = json.loads(path.read_text())
    assert data['dimension'] == 6
    k = data['colors']
    assert type(k) is int and 1 <= k <= 16
    records = data['subspace_colors']
    spaces = set()
    counts = Counter()
    for record in records:
        basis, c = record['basis'], record['color']
        assert 1 <= len(basis) <= 6 and all(type(x) is int and 1 <= x < 64 for x in basis)
        assert type(c) is int and 0 <= c < k
        U = span(basis)
        assert len(U) == 2 ** len(basis) and U not in spaces
        spaces.add(U)
        counts[len(basis)] += 1
    assert counts == {d: gaussian(6, d) for d in range(1, 7)}
    edge_count = 0
    for r, s in combinations(records, 2):
        orthogonal = all(dot(u, v) == 0 for u in r['basis'] for v in s['basis'])
        if orthogonal:
            edge_count += 1
            assert r['color'] != s['color'], ('monochromatic edge', r, s)
    T = span([3, 12, 48])
    clique = [r for r in records if span(r['basis']) <= T]
    assert len(clique) == 15 and len({r['color'] for r in clique}) == 15
    assert all(dot(x, y) == 0 for x in T for y in T)
    report = {'status': 'passed', 'vertices': len(records), 'all_pairs_checked': len(records)*(len(records)-1)//2,
              'edges_checked': edge_count, 'colors_used': len({r['color'] for r in records}),
              'dimension_counts': dict(sorted(counts.items())), 'clique_lower_bound': 15,
              'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Exact exhaustive integer verification of all graph vertices and edges; not Lean formalized.'}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.certificate)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
