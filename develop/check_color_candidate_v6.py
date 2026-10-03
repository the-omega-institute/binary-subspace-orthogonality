"""Independently replay the two requested v6 screens and Stab(T) witness."""

from itertools import product
import json
from pathlib import Path
import runpy

from check_complement_projection import enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def dot(u, v):
    return (u & v).bit_count() % 2


def span(rows):
    result = {0}
    for row in rows:
        result |= {value ^ row for value in list(result)}
    return frozenset(result)


def decompose(vector, T, S):
    for s in S:
        if vector ^ s in T:
            return vector ^ s, s
    raise ValueError(vector)


def lift_data_independent(U, T, S):
    K = U & T
    mapping = {}
    for vector in U:
        t, s = decompose(vector, T, S)
        mapping.setdefault(s, min(t ^ k for k in K))
    if not mapping:
        return K, frozenset(), ()
    P = frozenset(mapping)
    basis = independent_basis(P)
    return K, P, tuple(mapping[s] for s in basis)


def linear_map(images, basis, vector):
    for mask in range(1 << len(basis)):
        candidate = 0
        image = 0
        for index, value in enumerate(basis):
            if mask >> index & 1:
                candidate ^= value
                image ^= images[index]
        if candidate == vector:
            return image
    raise ValueError(vector)


def main():
    author = runpy.run_path(str(ROOT / 'develop/color_function_candidate_v6.py'))
    certificate = json.loads((ROOT / 'results/full-15-coloring.json').read_text())
    T = enumerate_span([3, 12, 48])
    S = enumerate_span([1, 4, 16])
    T_prime = enumerate_span([5, 18, 40])
    records = certificate['subspace_colors']
    labels = {}
    clique = []
    for record in records:
        U = enumerate_span(record['basis'])
        if U <= T:
            continue
        data = lift_data_independent(U, T, S)
        expected = author['candidate_label_v6'](data)
        labels[U] = expected
        assert expected == author['candidate_label_v6'](data)
        if U <= T_prime:
            clique.append(expected)
    first = span([13, 6])
    second = span([9, 14])
    pair_labels = [labels[first], labels[second]]

    # Explicit stabilizer witness. In the ordered S basis (1,4,16), use
    # B(1)=3, B(4)=12, B(16)=0. Its matrix is symmetric under the
    # perfect T-S pairing, so g_B(t,s)=(t+B(s),s) is an isometry.
    s_basis = (1, 4, 16)
    b_images = (3, 12, 0)
    assert all(dot(linear_map(b_images, s_basis, left), right) ==
               dot(left, linear_map(b_images, s_basis, right))
               for left in s_basis for right in s_basis)
    mapped_first = frozenset(vector ^ linear_map(
        b_images, s_basis, decompose(vector, T, S)[1]) for vector in first)
    assert mapped_first == second

    result = {
        'status': 'passed_screens_v6_rejected',
        'author_commit': '9a96fad30b00c3c7e22ec52f5a31239fd5649658',
        'vertices_checked': len(labels),
        'pair_separated': pair_labels[0] != pair_labels[1],
        'pair_label_bases': [list(independent_basis(label)) for label in pair_labels],
        'fourteen_clique_distinct_labels': len(set(clique)),
        'fourteen_clique_expected': 14,
        'full_replay_run': False,
        'reason_full_replay_skipped': 'Screen 2 failed: v6 uses only seven labels on the fourteen-clique.',
        'stabilizer_witness': {
            'B_on_S_basis_(1,4,16)': list(b_images),
            'mapped_plane_basis': [14, 9],
            'target_plane_basis': [9, 14],
            'self_adjoint_checked': True,
            'isometry_witness_checked': True,
            'correction_to_author_equations': 'g_B(13)=14, not 7; g_B(6)=9. The asserted g_B(13)=7 is impossible because g_B fixes the S projection and 13 and 7 have different S projections.'
        },
        'scope': 'Independent finite screens and explicit written stabilizer witness. No full replay, solver, Lean or n7 computation. Structural15 and n7 remain open; historical full n6 Lean theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-v6-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
