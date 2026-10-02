"""
Fifth candidate for a color function c(K, P, f) for the 15-coloring
of O_6^*.

Key lessons from v1-v4:
  1. The full fifteen-subspace inventory of T is required.
  2. The numeric key must use the geometry of P, not just f.
  3. The modulo operation loses information: two orthogonal vertices
     can share a residue class (span(11) and span(52) in v4).

This candidate uses a structural approach:
  - Compute A_0 = K + span(t_s), where t_s is a canonical
    representative of f(s) in T/K, for s in a basis of P.
  - If A_0 is available (dot(A_0, P) != 0), return A_0.
  - Otherwise, return the smallest available subspace of T
    containing A_0.
  - If A_0 = 0, fall back to min(P).
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
    raise ValueError(f"Cannot decompose {u} in T + S")


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


T = span([3, 12, 48])

LINES_T = [
    frozenset({0, 3}),
    frozenset({0, 12}),
    frozenset({0, 48}),
    frozenset({0, 15}),
    frozenset({0, 51}),
    frozenset({0, 60}),
    frozenset({0, 63}),
]

PLANES_T = [
    frozenset(span([3, 12])),
    frozenset(span([3, 48])),
    frozenset(span([3, 60])),
    frozenset(span([12, 48])),
    frozenset(span([12, 51])),
    frozenset(span([48, 15])),
    frozenset(span([15, 51])),
]

ALL_SUBSPACES_T = LINES_T + PLANES_T + [T]


def availability_score(A, P):
    A_basis = basis_of(A)
    P_basis = basis_of(P) if P else ()
    count = 0
    for a in A_basis:
        for p in P_basis:
            if dot(a, p):
                count += 1
    return count


def candidate_label_v5(U_data):
    """
    Choose a label A from the full fifteen-subspace inventory of T,
    using a structural selection based on the image of f.
    """
    K, P, f = U_data
    if not P:
        return T

    P_basis = basis_of(P)
    t_values = [canonical_representative(f[i], K)
                for i in range(len(P_basis))]

    A_0 = span(list(K) + t_values)

    if A_0 != frozenset({0}):
        if availability_score(A_0, P) > 0:
            return A_0
        candidates = [A for A in ALL_SUBSPACES_T
                      if A_0 <= A and availability_score(A, P) > 0]
        if candidates:
            return min(candidates,
                       key=lambda A: (len(A), sorted(A)))

    p_min = min(P - {0})
    available = [A for A in ALL_SUBSPACES_T
                 if availability_score(A, P) > 0]
    return available[p_min % len(available)]


def nonzero_matrix_X(K, Q):
    for k in basis_of(K):
        for q in basis_of(Q):
            if dot(k, q):
                return True
    return False


def nonzero_matrix_Y(L, P):
    for p in basis_of(P):
        for l in basis_of(L):
            if dot(p, l):
                return True
    return False


def nonzero_matrix_Z(P, Q, f_values, g_values, K, L):
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


def are_orthogonal(u1, u2):
    K_U, P_U, f_U = u1
    K_W, P_W, g_W = u2
    if nonzero_matrix_X(K_U, P_W):
        return False
    if nonzero_matrix_Y(K_W, P_U):
        return False
    if nonzero_matrix_Z(P_U, P_W, f_U, g_W, K_U, K_W):
        return False
    return True


def main():
    cert = json.loads(
        (ROOT / 'results/full-15-coloring.json').read_text())
    records = cert['subspace_colors']
    spaces = [span(r['basis']) for r in records]
    S = span([1, 4, 16])
    T_prime = span([5, 18, 40])

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
            'in_T_prime': U <= T_prime,
        })

    print(f"Vertices outside the clique: {len(data)}")

    labels = {}
    for d in data:
        labels[d['U']] = candidate_label_v5(
            (d['K'], d['P'], d['f_values']))

    distinct = set(labels.values())
    print(f"Distinct labels used: {len(distinct)}")

    bad1 = 0
    for d in data:
        A = labels[d['U']]
        if availability_score(A, d['P']) == 0:
            bad1 += 1
    print(f"Condition 1 violations: {bad1}")

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

    fourteen_labels = set()
    for d in data:
        if d['in_T_prime']:
            fourteen_labels.add(labels[d['U']])
    print(
        f"Distinct labels on the fourteen-clique: "
        f"{len(fourteen_labels)}")

    for target in [[11], [52], [5], [21]]:
        target_space = span(target)
        for d in data:
            if d['U'] == target_space:
                print(
                    f"Label of span{target}: "
                    f"{sorted(labels[d['U']])}")
                break

    print()
    print("Label distribution:")
    for A, group in sorted(by_label.items(),
                           key=lambda x: -len(x[1])):
        print(f"  Label size {len(A):2d}: "
              f"{len(group)} vertices")


if __name__ == '__main__':
    main()
