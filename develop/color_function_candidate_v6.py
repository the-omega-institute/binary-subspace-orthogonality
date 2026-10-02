"""
Sixth candidate for a color function c(K, P, f) for the 15-coloring of O_6^*.

Lesson from v5: the image of f is not enough. Proposition 5.5 shows
that no coloring depending on (K, P, rank, image, kernel) can separate
U = span(13,6) from W = span(9,14).

v6 retains the full matrix M of f : P -> T/K in canonical bases.
M is not invariant under Stab(T), so v6 escapes the orbit obstruction
that rules out every Stab(T)-invariant coloring.
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
    raise ValueError(f"Cannot decompose {u}")


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
    frozenset({0, 3}), frozenset({0, 12}), frozenset({0, 48}),
    frozenset({0, 15}), frozenset({0, 51}), frozenset({0, 60}),
    frozenset({0, 63}),
]
PLANES_T = [
    frozenset(span([3, 12])), frozenset(span([3, 48])),
    frozenset(span([3, 60])), frozenset(span([12, 48])),
    frozenset(span([12, 51])), frozenset(span([48, 15])),
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


def express(v, basis):
    n = len(basis)
    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if (mask >> i) & 1:
                s ^= basis[i]
        if s == v:
            return tuple((mask >> i) & 1 for i in range(n))
    raise ValueError(f"{v} not in span {basis}")


def matrix_hash(M):
    h = 0
    for row in M:
        for bit in row:
            h = (h << 1) | bit
    return h


def candidate_label_v6(U_data):
    K, P, f_values = U_data
    if not P:
        return T

    P_basis = basis_of(P)
    t_values = [canonical_representative(f_values[i], K)
                for i in range(len(P_basis))]

    A_0 = span(list(K) + t_values)
    R_basis = basis_of(A_0) if A_0 != frozenset({0}) else ()

    if not R_basis:
        p_min = min(P - {0})
        available = sorted(
            [A for A in ALL_SUBSPACES_T if availability_score(A, P) > 0],
            key=lambda A: (len(A), sorted(A)))
        return available[p_min % len(available)]

    M = tuple(express(t_values[i], R_basis)
              for i in range(len(P_basis)))
    h = matrix_hash(M)

    candidates = sorted(
        [A for A in ALL_SUBSPACES_T
         if A_0 <= A and availability_score(A, P) > 0],
        key=lambda A: (len(A), sorted(A)))
    if not candidates:
        candidates = sorted(
            [A for A in ALL_SUBSPACES_T if availability_score(A, P) > 0],
            key=lambda A: (len(A), sorted(A)))
    return candidates[h % len(candidates)]


def are_orthogonal(u1, u2):
    K_U, P_U, f_U = u1
    K_W, P_W, g_W = u2
    for k in basis_of(K_U):
        for q in basis_of(P_W):
            if dot(k, q):
                return False
    for l in basis_of(K_W):
        for p in basis_of(P_U):
            if dot(l, p):
                return False
    P_basis = basis_of(P_U)
    Q_basis = basis_of(P_W)
    for i, p in enumerate(P_basis):
        t_i = canonical_representative(f_U[i], K_U)
        for j, q in enumerate(Q_basis):
            u_j = canonical_representative(g_W[j], K_W)
            val = (dot(p, q) + dot(t_i, q) + dot(p, u_j)) % 2
            if val != 0:
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
            'U': U, 'K': K, 'P': P, 'f_values': f_values,
            'in_T_prime': U <= T_prime,
        })

    print(f"Vertices outside the clique: {len(data)}")

    labels = {}
    for d in data:
        labels[d['U']] = candidate_label_v6(
            (d['K'], d['P'], d['f_values']))

    # --- Screen 1: pair separation ---
    U_test = span([13, 6])
    W_test = span([9, 14])
    lU = labels.get(U_test)
    lW = labels.get(W_test)
    print(f"\n=== Screen 1: pair separation ===")
    print(f"  label(span(13,6)) = {sorted(lU) if lU else None}")
    print(f"  label(span(9,14)) = {sorted(lW) if lW else None}")
    print(f"  SEPARATED: {lU != lW and lU is not None and lW is not None}")

    # --- Screen 2: 14-clique ---
    fourteen_labels = set()
    for d in data:
        if d['in_T_prime']:
            fourteen_labels.add(labels[d['U']])
    print(f"\n=== Screen 2: 14-clique ===")
    print(f"  distinct labels on 14-clique: {len(fourteen_labels)}")

    # --- Full check ---
    distinct = set(labels.values())
    print(f"\n=== Full certificate ===")
    print(f"  distinct labels used: {len(distinct)}")

    bad_avail = sum(1 for d in data
                    if availability_score(labels[d['U']], d['P']) == 0)
    print(f"  availability violations: {bad_avail}")

    by_label = defaultdict(list)
    for d in data:
        by_label[labels[d['U']]].append(d)

    bad_orth = 0
    for A, group in by_label.items():
        for i, d1 in enumerate(group):
            for d2 in group[i + 1:]:
                u1 = (d1['K'], d1['P'], d1['f_values'])
                u2 = (d2['K'], d2['P'], d2['f_values'])
                if are_orthogonal(u1, u2):
                    bad_orth += 1
    print(f"  orthogonality violations (same label, adjacent): {bad_orth}")


if __name__ == '__main__':
    main()
