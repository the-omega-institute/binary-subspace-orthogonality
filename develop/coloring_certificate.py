"""Construct explicit colorings; optimality is not inferred from greedy search."""
from itertools import combinations
from pathlib import Path
import json


def dsatur(adj, dimensions):
    left = set(range(len(adj)))
    colors = [-1] * len(adj)
    saturation = [set() for _ in adj]
    while left:
        v = max(left, key=lambda x: (len(saturation[x]), len(adj[x]), -dimensions[x], x))
        c = next(k for k in range(len(adj)) if k not in saturation[v])
        colors[v] = c
        left.remove(v)
        for w in adj[v]:
            saturation[w].add(c)
    return colors


def build():
    n = 6
    spaces = []
    for k in range(1, n + 1):
        for pivots in combinations(range(n), k):
            cells = [(i, j) for i, p in enumerate(pivots)
                     for j in range(p + 1, n) if j not in pivots]
            for assignment in range(1 << len(cells)):
                rows = [1 << p for p in pivots]
                for b, (i, j) in enumerate(cells):
                    if assignment >> b & 1:
                        rows[i] |= 1 << j
                span = [0]
                for row in rows:
                    span += [x ^ row for x in span]
                mask = sum(1 << x for x in span)
                perp = sum(1 << x for x in range(1 << n)
                           if all((x & r).bit_count() % 2 == 0 for r in rows))
                spaces.append((mask, perp, rows))
    adj = [set() for _ in spaces]
    for i, (_, perp, _) in enumerate(spaces):
        for j in range(i):
            if spaces[j][0] & ~perp == 0:
                adj[i].add(j)
                adj[j].add(i)
    colors = dsatur(adj, [len(s[2]) for s in spaces])
    lines = list(range(1, 64))
    line_adj = [{j for j, y in enumerate(lines)
                 if x != y and (x & y).bit_count() % 2 == 0} for x in lines]
    line_colors = dsatur(line_adj, [1] * 63)
    return {
        'dimension': n,
        'encoding': 'Vector x has coordinate i equal to bit i of its integer label.',
        'line_classes': [[x for x, c in zip(lines, line_colors) if c == k]
                         for k in range(max(line_colors) + 1)],
        'subspace_colors': [{'basis': s[2], 'color': c}
                            for s, c in zip(spaces, colors)],
        'full_graph_edges': sum(map(len, adj)) // 2,
        'claims': {'line_upper_bound': max(line_colors) + 1,
                   'full_upper_bound': max(colors) + 1,
                   'full_lower_bound': 15},
    }


if __name__ == '__main__':
    output = Path(__file__).with_name('coloring-certificate.json')
    certificate = build()
    output.write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'claims': certificate['claims'],
                      'subspaces': len(certificate['subspace_colors']),
                      'edges': certificate['full_graph_edges']}))
