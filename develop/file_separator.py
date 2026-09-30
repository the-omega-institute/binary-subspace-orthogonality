"""
Find a geometric invariant that distinguishes the two adjacent lines
span(e1) and span(e2) in the fixed 15-coloring.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dot(u, v):
    return (u & v).bit_count() % 2


def span(rows):
    result = {0}
    for r in rows:
        result |= {x ^ r for x in list(result)}
    return frozenset(result)


def dim(U):
    return len(U).bit_length() - 1


def analyze(certificate_path):
    data = json.loads(certificate_path.read_text())
    records = data['subspace_colors']
    spaces = [span(r['basis']) for r in records]

    # Find the two lines span(e1) and span(e2) in binary coordinates
    e1 = 1  # 000001
    e2 = 2  # 000010
    record_e1 = None
    record_e2 = None
    for r in records:
        if sorted(r['basis']) == [e1]:
            record_e1 = r
        if sorted(r['basis']) == [e2]:
            record_e2 = r

    print("Color of span(e1):", record_e1['color'] if record_e1 else "not found")
    print("Color of span(e2):", record_e2['color'] if record_e2 else "not found")
    print()

    # Compute several candidate invariants for both lines
    T = span([3, 12, 48])
    e1_set = frozenset({0, e1})
    e2_set = frozenset({0, e2})

    for name, U in [("span(e1)", e1_set), ("span(e2)", e2_set)]:
        H = frozenset(t for t in T if all(dot(t, u) == 0 for u in U))
        K = U & T
        UH = U & H
        # Position of U relative to T^perp (= T)
        # Some candidate invariants:
        # 1. Which vectors of T are orthogonal to U?
        print(f"--- {name} ---")
        print("  dim U:", dim(U))
        print("  H =", sorted(H))
        print("  K =", sorted(K))
        print("  U ∩ H =", sorted(UH))
        # 2. Which vectors of the complement of T are orthogonal to U?
        #    (This could distinguish the two lines if the complement is rich.)
        # Compute the "orthogonal complement of U inside the whole space"
        U_perp = frozenset(x for x in range(64) if all(dot(x, u) == 0 for u in U))
        print("  |U^perp|:", len(U_perp))
        # 3. The color of the line in the clique that is NOT orthogonal to U?
        #    (i.e., the color that U is adjacent to but the other line is not)
        # Count clique colors adjacent to U
        labels = {r['color']: U2 for r, U2 in zip(records, spaces) if U2 <= T}
        adj_colors = sorted(c for c, W in labels.items() if W <= H)
        print("  Clique colors adjacent to U:", adj_colors)


if __name__ == '__main__':
    analyze(ROOT / 'results/full-15-coloring.json')
