"""Independently diagnose the first subspace-label candidate."""

from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import runpy
import time

from check_complement_projection import enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def coordinate_dot(first, second):
    return sum(((first >> coordinate) % 2) * ((second >> coordinate) % 2)
               for coordinate in range(6)) % 2


def main():
    started = time.monotonic()
    source = ROOT / 'develop/color_function_candidate.py'
    author = runpy.run_path(str(source))
    certificate = ROOT / 'results/full-15-coloring.json'
    records = json.loads(certificate.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    products = [[coordinate_dot(first, second) for second in range(64)]
                for first in range(64)]
    fibers = defaultdict(list)
    omitted_zero = 0
    palette_violations = 0
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        exact, features, mapping = independent_features(space, isotropic_space)
        kernel, projection = exact
        projection_basis = independent_basis(projection)
        values = tuple(min(mapping[vector]) for vector in projection_basis)
        original = author['lift_data'](space, isotropic_space, complement)
        assert original[0] == kernel
        assert original[1] | {0} == projection
        assert original[2] == values
        omitted_zero += 0 not in original[1]
        assert projection != frozenset({0})
        label = author['candidate_label'](original, isotropic_space)
        expected_generator = next(vector for vector in [3, 12, 48]
                                  if any(products[vector][argument]
                                         for argument in projection))
        assert label == enumerate_span([expected_generator])
        assert author['candidate_label']((kernel, projection, values), isotropic_space) == label
        if not any(products[vector][argument]
                   for vector in label for argument in projection):
            palette_violations += 1
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(products[vector][basis_vector] == 0
                                     for basis_vector in record['basis']))
        fibers[expected_generator].append((tuple(record['basis']), orthogonal_mask))
    same_label_pairs = 0
    monochromatic_edges = 0
    per_label = []
    for generator, entries in sorted(fibers.items()):
        edge_count = 0
        for first, second in combinations(entries, 2):
            same_label_pairs += 1
            if all((first[1] >> vector) & 1 for vector in second[0]):
                edge_count += 1
        monochromatic_edges += edge_count
        per_label.append({'label_basis': [generator], 'vertices': len(entries),
                          'same_label_pairs': len(entries) * (len(entries) - 1) // 2,
                          'monochromatic_edges': edge_count})
    first_space = enumerate_span([1])
    second_space = enumerate_span([2])
    first_data = author['lift_data'](first_space, isotropic_space, complement)
    second_data = author['lift_data'](second_space, isotropic_space, complement)
    first_label = author['candidate_label'](first_data, isotropic_space)
    second_label = author['candidate_label'](second_data, isotropic_space)
    assert first_label == second_label == enumerate_span([3])
    assert coordinate_dot(1, 2) == 0
    assert first_data == (frozenset({0}), frozenset({1}), (0,))
    assert second_data == (frozenset({0}), frozenset({1}), (3,))
    assert author['are_orthogonal'](first_data, second_data)
    declared_planes = [enumerate_span(basis) for basis in
                       [[3, 12], [3, 48], [3, 15], [12, 48],
                        [12, 51], [12, 60], [48, 63]]]
    assert len(set(declared_planes)) == 5
    assert sum(len(entries) for entries in fibers.values()) == 2809
    assert palette_violations == 0 and monochromatic_edges == 25496
    assert {generator: len(entries) for generator, entries in fibers.items()} == {
        3: 2451, 12: 307, 48: 51}
    report = {
        'status': 'diagnostic_passed_candidate_rejected',
        'author_commit': '53428f67566d1cf305a90bd91dc873c645126b19',
        'vertices_outside_clique': 2809,
        'distinct_labels_used': len(fibers),
        'condition_1_violations': palette_violations,
        'same_label_pairs_checked': same_label_pairs,
        'condition_2_violations': monochromatic_edges,
        'label_distribution': per_label,
        'counterexample': {
            'first_basis': [1], 'second_basis': [2],
            'kernel_basis': [], 'projection_basis': [1],
            'first_lift_values': [0], 'second_lift_values': [3],
            'common_label_basis': [3], 'original_coordinate_dot': 0,
            'X': [], 'Y': [], 'Z': [[0]],
            'label_projection_pairing': [[1]]
        },
        'zero_missing_from_original_projection_count': omitted_zero,
        'normalizing_projection_zero_changes_no_labels': True,
        'declared_plane_entries': 7, 'distinct_declared_planes': 5,
        'distinct_declared_labels': 13,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - started,
        'scope': 'Independent coordinate adjacency checks for all same-label pairs of this candidate, not a new coloring or a solver/Lean run. Author source and existing certificates are unchanged. Structural15 and n7 remain open; historical full-subspace n6 theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
