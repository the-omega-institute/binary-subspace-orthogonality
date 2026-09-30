"""
Test whether the pair (U ∩ T, projection of U to S) determines the
color in the fixed 15-coloring, for the chosen complement
S = span(e1, e3, e5).

The projection is along T, using the direct-sum decomposition
V_6 = T ⊕ S.
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


def projection_to_S(U, T, S):
    """
    Project U onto S along T.

    Since V_6 = T ⊕ S, each vector u in U decomposes uniquely as
    u = t + s with t in T and s in S. We compute the S-component
    by brute force over the (small) subspace S.
    """
    proj = set()
    for u in U:
        if u == 0:
            proj.add(0)
            continue
        for s in S:
            if (u ^ s) in T:
                proj.add(s)
                break
    return frozenset(proj)


def analyze(certificate_path):
    data = json.loads(certificate_path.read_text())
    records = data['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    T = span([3, 12, 48])
    S = span([1, 4, 16])

    # Verify that T + S = V_6 (as sets of 64 vectors)
    assert len(T ^ S) == 64 or len(set(x ^ y for x in T for y in S)) == 64, \
        "T and S are not complementary"

    refined = defaultdict(set)
    for r, U in zip(records, spaces):
        if U <= T:
            continue
        UT = U & T
        US = projection_to_S(U, T, S)
        inv = (dim(U), UT, US)
        refined[inv].add(r['color'])

    multi = {inv: cs for inv, cs in refined.items() if len(cs) > 1}
    single = {inv: cs for inv, cs in refined.items() if len(cs) == 1}

    return {
        'total_profiles': len(refined),
        'single_color_profiles': len(single),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_U': inv[0],
             'U_intersect_T': sorted(inv[1]),
             'projection_to_S': sorted(inv[2]),
             'colors': sorted(cs)}
            for inv, cs in list(multi.items())[:10]
        ],
    }


if __name__ == '__main__':
    result = analyze(ROOT / 'results/full-15-coloring.json')
    out = ROOT / 'results/complement-projection.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
