"""
Analyze relations among lift values that force different colors in
a 15-coloring of O_6^*.

For each vertex U outside the clique, compute (K, P, f) where
  K = U ∩ T,
  P = π_S(U),
  f: P -> T/K is the lift map defined by f(s) = t + K
  whenever t + s ∈ U.

The script verifies:
  1. The full data (K, P, f on a canonical basis of P) determines
     the color in the fixed certificate.
  2. The orthogonality criterion between two vertices can be tested
     directly from (K, P, f) and (L, Q, g).
  3. The fixed certificate has distinct colors on orthogonal sample pairs.

The sample contains the first 20 non-clique vertices. This diagnostic reads
the existing colors; it does not construct a structural 15-label assignment.
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


def decompose(u, T, S):
    """Decompose u = t + s with t in T and s in S. Return (t, s)."""
    for s in S:
        if (u ^ s) in T:
            return (u ^ s, s)
    raise ValueError(f"Cannot decompose {u} in T ⊕ S")


def lift_data(U, T, S):
    """
    Return (K, P, f_on_basis) where:
      K = U ∩ T,
      P = π_S(U),
      f_on_basis = tuple of canonical representatives of f(s)
                   for s in a canonical basis of P.
    """
    K = U & T
    P_to_f = {}
    for u in U:
        t, s = decompose(u, T, S)
        if s not in P_to_f:
            P_to_f[s] = canonical_representative(t, K)
    if not P_to_f:
        return K, frozenset(), ()
    P = frozenset(P_to_f.keys())
    P_basis = basis_of(P)
    f_values = tuple(P_to_f[s] for s in P_basis)
    return K, P, f_values


def extend_lift(P_basis, f_values, s, K):
    """
    Extend the lift map linearly: given the values f(s_i) on a basis
    of P, compute f(s) for an arbitrary s in P.
    """
    # Express s as a linear combination of P_basis over F_2
    # brute force since P is small
    k = len(P_basis)
    for coeffs in range(2 ** k):
        candidate = 0
        for i in range(k):
            if (coeffs >> i) & 1:
                candidate ^= P_basis[i]
        if candidate == s:
            # f(s) = sum of f(P_basis[i]) for the same coefficients
            result = 0
            for i in range(k):
                if (coeffs >> i) & 1:
                    result ^= f_values[i]
            return canonical_representative(result, K)
    raise ValueError(f"{s} is not in the span of the basis")


def are_orthogonal(data_U, data_W):
    """
    Test orthogonality between two vertices using the criterion:
      U = (K_U, P_U, f_U) and W = (K_W, P_W, f_W) are orthogonal
      iff:
        1. K_U ⊥ P_W and K_W ⊥ P_U;
        2. for all s in P_U, r in P_W:
           dot(s, r) + dot(f_U(s), r) + dot(s, f_W(r)) = 0.
    """
    K_U, P_U, f_U = data_U
    K_W, P_W, f_W = data_W

    # Condition 1
    for k in K_U:
        for q in P_W:
            if dot(k, q):
                return False
    for k in K_W:
        for p in P_U:
            if dot(k, p):
                return False

    # Condition 2
    P_U_basis = basis_of(P_U) if P_U else ()
    P_W_basis = basis_of(P_W) if P_W else ()
    for s in P_U:
        f_s = extend_lift(P_U_basis, f_U, s, K_U)
        for r in P_W:
            f_r = extend_lift(P_W_basis, f_W, r, K_W)
            if (dot(s, r) + dot(f_s, r) + dot(s, f_r)) % 2 != 0:
                return False
    return True


def main():
    cert = json.loads((ROOT / 'results/full-15-coloring.json').read_text())
    records = cert['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    T = span([3, 12, 48])
    S = span([1, 4, 16])

    data = {}
    for r, U in zip(records, spaces):
        if U <= T:
            continue
        K, P, f_values = lift_data(U, T, S)
        data[U] = (r['color'], K, P, f_values)

    # Group by (dim K, dim P, f_values)
    groups = defaultdict(list)
    for U, (color, K, P, f_values) in data.items():
        groups[(dim(K), dim(P), f_values)].append((U, color))

    print(f"Total groups: {len(groups)}")
    multi = {k: v for k, v in groups.items() if len({c for _, c in v}) > 1}
    print(f"Multi-color groups: {len(multi)}")

    # Sanity check: the full data should give 2809 singletons
    full_groups = defaultdict(list)
    for U, (color, K, P, f_values) in data.items():
        full_groups[(frozenset(K), frozenset(P), f_values)].append(
            (U, color))
    multi_full = {k: v for k, v in full_groups.items()
                  if len({c for _, c in v}) > 1}
    print(f"Full-data groups: {len(full_groups)}")
    print(f"Full-data multi-color groups: {len(multi_full)}")

    # Orthogonality test: sample a few pairs
    vertices = list(data.keys())
    sample = vertices[:20]
    count_orth = 0
    for i, U in enumerate(sample):
        for W in sample[i + 1:]:
            if are_orthogonal(data[U][1:], data[W][1:]):
                count_orth += 1
    print(f"Orthogonal pairs in sample: {count_orth}")

    # Verify that orthogonal vertices have different colors
    bad = 0
    for i, U in enumerate(sample):
        for W in sample[i + 1:]:
            if are_orthogonal(data[U][1:], data[W][1:]):
                if data[U][0] == data[W][0]:
                    bad += 1
    print(f"Monochromatic orthogonal pairs in sample: {bad}")
    report = {
        'total_groups': len(groups), 'multi_color_groups': len(multi),
        'full_data_groups': len(full_groups),
        'full_data_multi_color_groups': len(multi_full),
        'sample_vertices': [list(basis_of(space)) for space in sample],
        'sample_pairs': len(sample) * (len(sample) - 1) // 2,
        'orthogonal_pairs_in_sample': count_orth,
        'monochromatic_orthogonal_pairs_in_sample': bad,
        'scope': 'First twenty non-clique vertices only; existing certificate colors, not a structural label construction.'
    }
    (ROOT / 'results/lift-relations.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
