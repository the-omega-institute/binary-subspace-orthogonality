"""Check clique-induced color lists and a reversible list-coloring reduction.

This is a finite preprocessing certificate, not a coloring or noncolorability
claim. It uses the already supplied subspace enumeration; no Lean job runs.
"""
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def span(rows):
    values = {0}
    for row in rows:
        values |= {x ^ row for x in values}
    return values


def main():
    source = ROOT / 'coloring-certificate.json'
    rows = [record['basis'] for record in json.loads(source.read_text())['subspace_colors']]
    spaces = [span(basis) for basis in rows]
    assert len({frozenset(s) for s in spaces}) == 2824
    assert Counter(len(s) for s in spaces) == {2: 63, 4: 651, 8: 1395, 16: 651, 32: 63, 64: 1}
    masks = [sum(1 << x for x in s) for s in spaces]
    perps = [sum(1 << x for x in range(64) if all((x & r).bit_count() % 2 == 0 for r in b)) for b in rows]
    adj = [set() for _ in rows]
    for i, j in combinations(range(len(rows)), 2):
        if masks[j] & ~perps[i] == 0:
            assert masks[i] & ~perps[j] == 0
            adj[i].add(j)
            adj[j].add(i)
    T = span([3, 12, 48])
    assert {x for x in range(64) if all((x & t).bit_count() % 2 == 0 for t in T)} == T
    clique = [i for i, s in enumerate(spaces) if s <= T]
    assert len(clique) == 15 and all(j in adj[i] for i, j in combinations(clique, 2))
    remaining = set(range(len(rows))) - set(clique)
    palettes = {}
    types = Counter()
    for i in sorted(remaining):
        H = {x for x in T if perps[i] >> x & 1}
        h = len(H).bit_length() - 1
        assert h in (0, 1, 2)
        forbidden = {color for color, j in enumerate(clique) if spaces[j] <= H}
        assert forbidden == {color for color, j in enumerate(clique) if j in adj[i]}
        assert len(forbidden) == (0, 1, 4)[h]
        palettes[i] = set(range(15)) - forbidden
        types[h, len(palettes[i])] += 1
    degree = {i: len(adj[i] & remaining) for i in remaining}
    queue = deque(i for i in sorted(remaining) if degree[i] < len(palettes[i]))
    removed = []
    while queue:
        i = queue.popleft()
        if i not in remaining:
            continue
        assert degree[i] < len(palettes[i])
        remaining.remove(i)
        removed.append({'vertex': i, 'remaining_degree': degree[i], 'list_size': len(palettes[i])})
        for j in adj[i] & remaining:
            degree[j] -= 1
            if degree[j] < len(palettes[j]):
                queue.append(j)
    # Replay from the original graph, independently recomputing each degree.
    replay = set(range(len(rows))) - set(clique)
    for step in removed:
        i = step['vertex']
        assert len(adj[i] & replay) == step['remaining_degree'] < len(palettes[i])
        replay.remove(i)
    assert replay == remaining
    assert all(len(adj[i] & remaining) >= len(palettes[i]) for i in remaining)
    report = {'status': 'preprocessing_verified', 'dimension': 6, 'vertices': len(rows),
              'edges': sum(map(len, adj)) // 2, 'clique_indices': clique,
              'palette_types': [{'intersection_dimension': h, 'list_size': k, 'vertices': count}
                                for (h, k), count in sorted(types.items())],
              'deleted_vertices': len(removed), 'core_vertices': len(remaining),
              'core_edges': sum(len(adj[i] & remaining) for i in remaining) // 2,
              'core_dimension_counts': dict(sorted(Counter(len(rows[i]) for i in remaining).items())),
              'core_indices': sorted(remaining), 'deletion_certificate': removed,
              'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Equivalent residual list-coloring instance; no SAT/UNSAT or Lean claim.'}
    (ROOT / 'precoloring-reduction.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('clique_indices', 'core_indices', 'deletion_certificate')}, indent=2))


if __name__ == '__main__':
    main()
