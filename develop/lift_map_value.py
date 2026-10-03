"""
Test whether the exact value pattern of the lift map f: P -> T/K on a
canonical basis of P separates the multi-color profiles of the fixed
15-coloring.

This is the next step after Proposition 5.5, which ruled out the
matrix features (rank, image, kernel) alone.
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


def basis_of(U):
    """Return a canonical basis of a subspace U (list of ints)."""
    basis = []
    for v in sorted(U, reverse=True):
        x = v
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return tuple(basis)


def canonical_representative(t, K):
    """Return the minimal representative of the coset t + K."""
    return min(t ^ k for k in K)


def lift_map_pattern(U, T, S):
    """
    Return the pattern of f on a canonical basis of P = pi_S(U).
    The pattern is (dim K, dim P, tuple of f-values on the basis).
    """
    K = U & T
    P_to_f = {}
    for u in U:
        for s in S:
            if (u ^ s) in T:
                t = u ^ s
                if s not in P_to_f:
                    P_to_f[s] = canonical_representative(t, K)
                break
    if not P_to_f:
        return (0, 0, ())
    P = frozenset(P_to_f.keys())
    P_basis = basis_of(P)
    f_values = tuple(P_to_f[s] for s in P_basis)
    return (dim(K), dim(P), f_values)


def analyze(certificate_path):
    data = json.loads(certificate_path.read_text())
    records = data['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    T = span([3, 12, 48])
    S = span([1, 4, 16])

    refined = defaultdict(set)
    for r, U in zip(records, spaces):
        if U <= T:
            continue
        pattern = lift_map_pattern(U, T, S)
        refined[pattern].add(r['color'])

    multi = {inv: cs for inv, cs in refined.items() if len(cs) > 1}
    single = {inv: cs for inv, cs in refined.items() if len(cs) == 1}

    return {
        'total_profiles': len(refined),
        'single_color_profiles': len(single),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_K': inv[0], 'dim_P': inv[1], 'f_values': list(inv[2]),
             'colors': sorted(cs)}
            for inv, cs in list(multi.items())[:10]
        ],
    }


if __name__ == '__main__':
    result = analyze(ROOT / 'results/full-15-coloring.json')
    out = ROOT / 'results/lift-map-values.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
