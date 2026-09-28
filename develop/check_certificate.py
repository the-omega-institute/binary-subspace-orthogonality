"""Independently check the explicit certificates, without importing the search."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def dot(x, y, n=6):
    return sum(((x >> i) % 2) * ((y >> i) % 2) for i in range(n)) % 2


def span(rows):
    result = set()
    for coefficients in product((0, 1), repeat=len(rows)):
        x = 0
        for bit, row in zip(coefficients, rows):
            if bit:
                x ^= row
        result.add(x)
    return frozenset(result)


def gaussian(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return gaussian(n - 1, k) + 2 ** (n - k) * gaussian(n - 1, k - 1)


def check(path):
    data = json.loads(path.read_text())
    assert data['dimension'] == 6
    classes = data['line_classes']
    assert len(classes) == 14
    assert sorted(x for c in classes for x in c) == list(range(1, 64))
    line_pairs = 0
    for c in classes:
        for u, v in combinations(c, 2):
            assert dot(u, v) == 1
            line_pairs += 1
    records = data['subspace_colors']
    counts = [0] * 7
    unique = set()
    for record in records:
        rows = record['basis']
        assert 1 <= len(rows) <= 6 and all(1 <= x < 64 for x in rows)
        assert isinstance(record['color'], int) and 0 <= record['color'] < 16
        U = span(rows)
        assert len(U) == 2 ** len(rows)
        assert U not in unique
        unique.add(U)
        counts[len(rows)] += 1
    assert counts[1:] == [gaussian(6, k) for k in range(1, 7)]
    assert len(records) == 2824 and set(r['color'] for r in records) == set(range(16))
    subspace_pairs = 0
    for color in range(16):
        group = [r['basis'] for r in records if r['color'] == color]
        for U, W in combinations(group, 2):
            assert any(dot(u, w) == 1 for u in U for w in W)
            subspace_pairs += 1
    # All nonzero subspaces of the isotropic span of 3,12,48 give the lower bound.
    T = span([3, 12, 48])
    assert len(T) == 8 and all(dot(x, y) == 0 for x in T for y in T)
    clique = [U for U in unique if U <= T]
    assert len(clique) == 15
    for U, W in combinations(clique, 2):
        assert U != W and all(dot(x, y) == 0 for x in U for y in W)
    return {'status': 'passed', 'dimension_counts': counts[1:],
            'line_vertices': 63, 'line_colors': 14, 'line_pairs_checked': line_pairs,
            'subspace_vertices': len(records), 'subspace_colors': 16,
            'same_color_subspace_pairs_checked': subspace_pairs,
            'clique_size': 15, 'clique_pairs_checked': 105,
            'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'formalization': 'Exact finite certificate check; not Lean formalized.'}


if __name__ == '__main__':
    result = check(Path(__file__).with_name('coloring-certificate.json'))
    Path(__file__).with_name('certificate-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
