"""Build and peel the n=7 fixed-clique instance; no SAT conclusion is inferred."""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]


def span(rows):
    values = [0]
    for row in rows:
        values += [v ^ row for v in values]
    return values


@lru_cache(None)
def bases(n, max_dimension):
    result = []
    for d in range(1, min(n, max_dimension) + 1):
        for pivots in combinations(range(n), d):
            cells = [(i, j) for i, p in enumerate(pivots)
                     for j in range(p + 1, n) if j not in pivots]
            for assignment in range(1 << len(cells)):
                rows = [1 << p for p in pivots]
                for b, (i, j) in enumerate(cells):
                    if assignment >> b & 1:
                        rows[i] |= 1 << j
                result.append(tuple(rows))
    return tuple(result)


def independent_basis(vectors):
    pivots = {}
    for v in vectors:
        for p, row in sorted(pivots.items(), reverse=True):
            if v >> p & 1:
                v ^= row
        if v:
            pivots[v.bit_length() - 1] = v
    return tuple(pivots.values())


def gaussian(n, k):
    if k in (0, n):
        return 1
    return gaussian(n - 1, k) + 2 ** (n - k) * gaussian(n - 1, k - 1)


def analyze(n):
    start = time.monotonic()
    k = 15 + n % 2
    rows = bases(n, 3)
    spaces = [frozenset(span(b)) for b in rows]
    lookup = {U: i for i, U in enumerate(spaces)}
    assert len(lookup) == sum(gaussian(n, d) for d in range(1, 4))
    T = frozenset(span([3, 12, 48]))
    clique = [i for i, U in enumerate(spaces) if U <= T]
    if n == 7:
        clique.append(lookup[frozenset((0, 64))])
    assert len(set(clique)) == k
    adj = [set() for _ in rows]
    for i, b in enumerate(rows):
        perpendicular = [v for v in range(1 << n)
                         if all((v & r).bit_count() % 2 == 0 for r in b)]
        pb = independent_basis(perpendicular)
        assert len(pb) == n - len(b)
        mapped = [0] * (1 << len(pb))
        for v in range(1, len(mapped)):
            low = v & -v
            mapped[v] = mapped[v ^ low] ^ pb[low.bit_length() - 1]
        for local in bases(len(pb), 3):
            U = frozenset(span([mapped[r] for r in local]))
            j = lookup[U]
            if j < i:
                adj[i].add(j)
                adj[j].add(i)
    assert all(j in adj[i] for i, j in combinations(clique, 2))
    remaining = set(range(len(rows))) - set(clique)
    palettes = {i: set(range(k)) - {c for c, j in enumerate(clique) if j in adj[i]}
                for i in remaining}
    initial_types = Counter((len(rows[i]), len(palettes[i])) for i in remaining)
    degree = {i: len(adj[i] & remaining) for i in remaining}
    queue = deque(i for i in sorted(remaining) if degree[i] < len(palettes[i]))
    removed = []
    while queue:
        i = queue.popleft()
        if i not in remaining:
            continue
        assert len(adj[i] & remaining) < len(palettes[i])
        remaining.remove(i)
        removed.append(i)
        for j in adj[i] & remaining:
            degree[j] -= 1
            if degree[j] < len(palettes[j]):
                queue.append(j)
    edge_clauses = sum(len(palettes[i] & palettes[j]) for i in remaining
                       for j in adj[i] & remaining if j < i)
    vertex_clauses = sum(1 + len(palettes[i]) * (len(palettes[i]) - 1) // 2
                         for i in remaining)
    counts = {d: gaussian(n, d) for d in range(1, n + 1)}
    report = {
        'status': 'reduction_measured_no_solver_run', 'dimension': n, 'target_colors': k,
        'all_subspace_dimension_counts': counts, 'all_vertices': sum(counts.values()),
        'high_dimension_vertices_deleted_by_degree_bound': sum(counts[d] for d in range(4, n + 1)),
        'enumerated_dimensions': [1, 2, 3], 'enumerated_vertices': len(rows),
        'enumerated_edges': sum(map(len, adj)) // 2,
        'additional_low_dimension_deletions': len(removed),
        'core_vertices': len(remaining),
        'core_edges': sum(len(adj[i] & remaining) for i in remaining) // 2,
        'core_dimension_counts': dict(sorted(Counter(len(rows[i]) for i in remaining).items())),
        'initial_palette_types': [{'dimension': d, 'list_size': size, 'vertices': count}
                                  for (d, size), count in sorted(initial_types.items())],
        'pairwise_encoding_variables': sum(len(palettes[i]) for i in remaining),
        'pairwise_encoding_clauses': vertex_clauses + edge_clauses,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - start,
        'scope': 'Exact reduced-instance size. Dimensions at least four can be deleted '
                 'because N(n-d) < target_colors. No new coloring or nonexistence result.'}
    if n == 6:
        assert report['core_vertices'] == 2080 and report['core_edges'] == 39400
        assert report['pairwise_encoding_variables'] == 28600
        assert report['pairwise_encoding_clauses'] == 627510
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = analyze(args.dimension)
    target = args.report or ROOT / f'results/dimension-{args.dimension}-feasibility.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
