"""
Test a candidate color function c(K, P, f) for the 15-coloring of O_6^*.

The candidate is based on the pairing between P and the lines of T.

The criterion for a proper label assignment is (Zhang-Ma):
  1. For a non-clique vertex U = (K, P, f), the chosen label A must
     satisfy dot(A, P) != 0.
  2. For two non-clique vertices U = (K, P, f) and W = (L, Q, g)
     with the same label, at least one of the three matrices X, Y, Z
     must be nonzero:
       X[a, j] = dot(k_a, q_j)
       Y[i, b] = dot(p_i, l_b)
       Z[i, j] = dot(p_i, q_j) + dot(t_i, q_j) + dot(p_i, u_j).
"""
import json
from collections import defaultdict
from itertools import product
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
    return min(t ^ k for k in K)


def decompose(u, T, S):
    for s in S:
        if (u ^ s) in T:
            return (u ^ s, s)
    raise ValueError(f"Cannot decompose {u} in T ⊕ S")


def lift_data(U, T, S):
    K = U & T
    P_to_f = {}
    for u in U:
        if u == 0:
            continue
        t, s = decompose(u, T, S)
        if s not in P_to_f:
            P_to_f[s] = canonical_representative(t, K)
    if not P_to_f:
        return K, frozenset(), ()
    P = frozenset(P_to_f.keys())
    P_basis = basis_of(P)
    f_values = tuple(P_to_f[s] for s in P_basis)
    return K, P, f_values


def nonzero_matrix_X(K, Q):
    """X[a, j] = dot(k_a, q_j)."""
    K_basis = basis_of(K)
    Q_basis = basis_of(Q)
    for k in K_basis:
        for q in Q_basis:
            if dot(k, q):
                return True
    return False


def nonzero_matrix_Y(L, P):
    """Y[i, b] = dot(p_i, l_b)."""
    P_basis = basis_of(P)
    L_basis = basis_of(L)
    for p in P_basis:
        for l in L_basis:
            if dot(p, l):
                return True
    return False


def nonzero_matrix_Z(P, Q, f_values, g_values, K, L):
    """
    Z[i, j] = dot(p_i, q_j) + dot(t_i, q_j) + dot(p_i, u_j).
    Here t_i = canonical_representative(f(p_i), K), and
    u_j = canonical_representative(g(q_j), L).
    We use the basis values directly and compute the matrix
    for basis vectors of P and Q.
    """
    P_basis = basis_of(P)
    Q_basis = basis_of(Q)
    for i, p in enumerate(P_basis):
        t_i = canonical_representative(f_values[i], K)
        for j, q in enumerate(Q_basis):
            u_j = canonical_representative(g_values[j], L)
            val = (dot(p, q) + dot(t_i, q) + dot(p, u_j)) % 2
            if val != 0:
                return True
    return False


def are_orthogonal(U_data, W_data):
    """
    The full orthogonality test: U and W are orthogonal iff
    all of X, Y, Z vanish.
    """
    K_U, P_U, f_U = U_data
    K_W, P_W, g_W = W_data
    if nonzero_matrix_X(K_U, P_W):
        return False
    if nonzero_matrix_Y(K_W, P_U):
        return False
    if nonzero_matrix_Z(P_U, P_W, f_U, g_W, K_U, K_W):
        return False
    return True


def candidate_label(U_data, T):
    """
    Candidate label function.

    Idea: use the set of lines of T that are NOT orthogonal to P.
    If this set is nonempty, choose the first such line.
    If P = 0 (so all lines are orthogonal to P), fall back to
    a line contained in K (which gives a nonzero A-P? no,
    but A must have dot(A, P) != 0, so if P = 0 we cannot
    satisfy condition 1 with a line; we use T itself instead).

    This is a first attempt; it may not satisfy the three-block
    condition.
    """
    K, P, f = U_data
    lines_T = [
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 4}),
        frozenset({0, 8}),
        frozenset({0, 16}),
        frozenset({0, 32}),
        frozenset({0, 63}),
    ]
    # In T = span{3, 12, 48}, the seven lines are:
    # {0,3}, {0,12}, {0,48}, {0,15}, {0,51}, {0,60}, {0,63}
    lines_T = [
        frozenset({0, 3}),
        frozenset({0, 12}),
        frozenset({0, 48}),
        frozenset({0, 15}),
        frozenset({0, 51}),
        frozenset({0, 60}),
        frozenset({0, 63}),
    ]
    planes_T = [
        frozenset(span([3, 12])),
        frozenset(span([3, 48])),
        frozenset(span([3, 15])),
        frozenset(span([12, 48])),
        frozenset(span([12, 51])),
        frozenset(span([12, 60])),
        frozenset(span([48, 63])),
    ]
    all_nonzero = lines_T + planes_T + [T]

    # Condition 1: dot(A, P) != 0
    for A in all_nonzero:
        A_basis = basis_of(A)
        P_basis = basis_of(P) if P else ()
        ok = False
        for a in A_basis:
            for p in P_basis:
                if dot(a, p):
                    ok = True
                    break
            if ok:
                break
        if ok:
            return A

    # Fallback: if P = 0, use T
    return T


def main():
    cert = json.loads((ROOT / 'results/full-15-coloring.json').read_text())
    records = cert['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    T = span([3, 12, 48])
    S = span([1, 4, 16])

    # Collect data
    data = []
    for r, U in zip(records, spaces):
        if U <= T:
            continue
        K, P, f_values = lift_data(U, T, S)
        data.append({
            'U': U,
            'K': K,
            'P': P,
            'f_values': f_values,
            'color': r['color'],
        })

    print(f"Vertices outside the clique: {len(data)}")

    # Candidate label assignment
    labels = {}
    for d in data:
        labels[d['U']] = candidate_label((d['K'], d['P'], d['f_values']), T)

    # Count distinct labels
    distinct_labels = set(labels.values())
    print(f"Distinct labels used: {len(distinct_labels)}")

    # Verify condition 1
    bad1 = 0
    for d in data:
        A = labels[d['U']]
        P = d['P']
        P_basis = basis_of(P) if P else ()
        A_basis = basis_of(A)
        ok = False
        for a in A_basis:
            for p in P_basis:
                if dot(a, p):
                    ok = True
                    break
            if ok:
                break
        if not ok:
            bad1 += 1
    print(f"Condition 1 violations: {bad1}")

    # Verify condition 2
    by_label = defaultdict(list)
    for d in data:
        by_label[labels[d['U']]].append(d)

    bad2 = 0
    for A, group in by_label.items():
        for i, d1 in enumerate(group):
            for d2 in group[i + 1:]:
                u1 = (d1['K'], d1['P'], d1['f_values'])
                u2 = (d2['K'], d2['P'], d2['f_values'])
                if are_orthogonal(u1, u2):
                    bad2 += 1
    print(f"Condition 2 violations: {bad2}")

    # Report
    print()
    print("Label distribution:")
    for A, group in sorted(by_label.items(), key=lambda x: -len(x[1])):
        print(f"  Label size {len(A):2d}: {len(group)} vertices")


if __name__ == '__main__':
    main()
