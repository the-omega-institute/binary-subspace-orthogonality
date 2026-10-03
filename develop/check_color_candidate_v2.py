"""Check the second label candidate and the fourteen-vertex obstruction."""

from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import runpy
import time

from check_color_candidate import coordinate_dot
from check_complement_projection import enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def main():
    started = time.monotonic()
    source = ROOT / 'develop/color_function_candidate_v2.py'
    author = runpy.run_path(str(source))
    certificate = ROOT / 'results/full-15-coloring.json'
    records = json.loads(certificate.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    other_isotropic_space = enumerate_span([5, 18, 40])
    complement = enumerate_span([1, 4, 16])
    products = [[coordinate_dot(first, second) for second in range(64)]
                for first in range(64)]
    assert isotropic_space & other_isotropic_space == frozenset({0, 63})
    assert all(products[first][second] == 0
               for first in other_isotropic_space for second in other_isotropic_space)
    fibers = defaultdict(list)
    outside_clique = []
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
        assert original[0] == kernel and original[1] | {0} == projection
        assert original[2] == values
        omitted_zero += 0 not in original[1]
        available = [generator for generator in [3, 12, 48, 15, 51, 60, 63]
                     if any(products[generator][argument] for argument in projection)]
        assert len(available) >= 4
        expected_generator = available[int(values[0] != 0)]
        label = author['candidate_label_v2'](original)
        assert label == enumerate_span([expected_generator])
        assert author['candidate_label_v2']((kernel, projection, values)) == label
        if not any(products[vector][argument]
                   for vector in label for argument in projection):
            palette_violations += 1
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(products[vector][basis_vector] == 0
                                     for basis_vector in record['basis']))
        entry = (tuple(record['basis']), orthogonal_mask)
        fibers[expected_generator].append(entry)
        if space <= other_isotropic_space:
            outside_clique.append(entry)
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
    assert len(outside_clique) == 14
    for first, second in combinations(outside_clique, 2):
        assert all((first[1] >> vector) & 1 for vector in second[0])
    first_data = author['lift_data'](enumerate_span([2]), isotropic_space, complement)
    second_data = author['lift_data'](enumerate_span([13]), isotropic_space, complement)
    assert first_data == (frozenset({0}), frozenset({1}), (3,))
    assert second_data == (frozenset({0}), frozenset({1}), (12,))
    assert author['candidate_label_v2'](first_data) == enumerate_span([15])
    assert author['candidate_label_v2'](second_data) == enumerate_span([15])
    assert coordinate_dot(2, 13) == 0 and author['are_orthogonal'](first_data, second_data)
    assert author['candidate_label_v2'](author['lift_data'](
        enumerate_span([1]), isotropic_space, complement)) == enumerate_span([3])
    assert sum(len(entries) for entries in fibers.values()) == 2809
    assert palette_violations == 0 and monochromatic_edges == 13945
    assert sorted(len(entries) for entries in fibers.values()) == [35, 70, 394, 575, 1735]
    report = {
        'status': 'diagnostic_passed_candidate_v2_rejected',
        'author_commit': '04d03c6ba8af23b1409f43801e1a8efda12c38b0',
        'vertices_outside_clique': 2809, 'distinct_labels_used': len(fibers),
        'condition_1_violations': palette_violations,
        'same_label_pairs_checked': same_label_pairs,
        'condition_2_violations': monochromatic_edges,
        'label_distribution': per_label,
        'actual_tie_breaker': 'Only zero/nonzero of the first canonical lift value, not its full value.',
        'counterexample': {
            'first_basis': [2], 'second_basis': [13], 'kernel_basis': [],
            'projection_basis': [1], 'first_lift_values': [3], 'second_lift_values': [12],
            'common_label_basis': [15], 'original_coordinate_dot': 0,
            'X': [], 'Y': [], 'Z': [[0]], 'label_projection_pairing': [[1]]
        },
        'previous_span1_span2_counterexample_separated': True,
        'outside_clique_obstruction': {
            'other_isotropic_basis': [5, 18, 40], 'intersection_with_T_basis': [63],
            'vertex_bases': [list(entry[0]) for entry in outside_clique],
            'vertices': 14, 'pairs_checked': 91,
            'proved_lower_bound_on_distinct_labels_required_outside_T': 14
        },
        'zero_missing_from_original_projection_count': omitted_zero,
        'normalizing_projection_zero_changes_no_labels': True,
        'distinct_declared_planes': len(set(author['PLANES_T'])),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - started,
        'scope': 'Independent coordinate checks of all same-label pairs and a written fourteen-clique obstruction. No new coloring, solver, Lean or n7 computation. Author source/certificates unchanged; structural15/n7 open; historical full n6 theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-v2-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
