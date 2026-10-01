"""
Analyze the lift map f: P -> T/K as a linear map over F_2, and test
whether its matrix features (rank, image, kernel) separate the
multi-color profiles of the fixed 15-coloring.

Setup:
  V_6 = T ⊕ S, with T = span(3, 12, 48) and S = span(1, 4, 16).
  For U outside the clique, K = U ∩ T and P = π_S(U).
  The lift map f: P -> T/K is defined by f(s) = t + K
  whenever t + s belongs to U.
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


def coset(t, K):
    """Representative of the coset t + K in T/K."""
    return frozenset(t ^ k for k in K)


def lift_map_features(U, T, S):
    """
    Compute features of the lift map f: P -> T/K.

    Returns a tuple (dim_K, dim_P, rank_f, image, kernel).
    """
    K = U & T

    # Collect (s, coset of f(s)) pairs
    P_to_f = {}
    for u in U:
        for s in S:
            if (u ^ s) in T:
                t = u ^ s
                if s not in P_to_f:
                    P_to_f[s] = coset(t, K)
                break

    P = frozenset(P_to_f.keys())
    image = frozenset(P_to_f.values())
    kernel = U & S

    return (
        dim(K),
        dim(P) if P else 0,
        dim(image) if image else 0,
        image,
        kernel,
    )


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
        dim_K, dim_P, rank_f, image, kernel = lift_map_features(U, T, S)
        inv = (dim_K, dim_P, rank_f, image, kernel)
        refined[inv].add(r['color'])

    multi = {inv: cs for inv, cs in refined.items() if len(cs) > 1}
    single = {inv: cs for inv, cs in refined.items() if len(cs) == 1}

    return {
        'total_profiles': len(refined),
        'single_color_profiles': len(single),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_K': inv[0], 'dim_P': inv[1], 'rank_f': inv[2],
             'image': sorted(sorted(coset_vectors) for coset_vectors in inv[3]),
             'kernel': sorted(inv[4]),
             'colors': sorted(cs)}
            for inv, cs in list(multi.items())[:10]
        ],
    }


if __name__ == '__main__':
    result = analyze(ROOT / 'results/full-15-coloring.json')
    out = ROOT / 'results/lift-map-matrix.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
