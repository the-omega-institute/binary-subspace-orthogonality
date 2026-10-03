"""Replay v4 and verify its palette-residue counterexample independently."""

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
    source = ROOT / 'develop/color_function_candidate_v4'
    author = runpy.run_path(str(source))
    certificate = ROOT / 'results/full-15-coloring.json'
    records = json.loads(certificate.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    other_isotropic_space = enumerate_span([5, 18, 40])
    products = [[coordinate_dot(first, second) for second in range(64)]
                for first in range(64)]
    complete_inventory = {enumerate_span(generators) for size in range(1, 4)
                          for generators in combinations(sorted(isotropic_space - {0}), size)}
    inventory = author['ALL_SUBSPACES_T']
    assert len(inventory) == 15 and set(inventory) == complete_inventory
    fibers = defaultdict(list)
    by_basis = {}
    fixture = []
    omitted_zero = 0
    palette_violations = 0
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        exact, features, mapping = independent_features(space, isotropic_space)
        kernel, projection = exact
        values = tuple(min(mapping[vector]) for vector in independent_basis(projection))
        original = author['lift_data'](space, isotropic_space, complement)
        assert original[0] == kernel and original[1] | {0} == projection
        assert original[2] == values
        omitted_zero += 0 not in original[1]
        available = [label for label in inventory
                     if any(products[first][second] for first in label for second in projection)]
        assert len(available) in (11, 14, 15)
        numeric_key = min(projection - {0})
        for value in values:
            numeric_key = 64 * numeric_key + value
        assert numeric_key < 2 ** 32
        expected_label = available[numeric_key % len(available)]
        assert author['candidate_label_v4'](original) == expected_label
        assert author['candidate_label_v4']((kernel, projection, values)) == expected_label
        if not any(products[first][second] for first in expected_label for second in projection):
            palette_violations += 1
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(products[vector][basis_vector] == 0
                                     for basis_vector in record['basis']))
        entry = {'basis': tuple(record['basis']), 'label': expected_label,
                 'key': numeric_key, 'available': available, 'data': original,
                 'orthogonal_mask': orthogonal_mask}
        fibers[expected_label].append(entry)
        by_basis[tuple(record['basis'])] = entry
        if space <= other_isotropic_space:
            fixture.append(entry)
    pair_count = 0
    edge_count = 0
    per_label = []
    for label, members in sorted(fibers.items(),
                                 key=lambda item: (len(item[0]), independent_basis(item[0]))):
        label_edges = 0
        for first, second in combinations(members, 2):
            pair_count += 1
            if all((first['orthogonal_mask'] >> vector) & 1 for vector in second['basis']):
                label_edges += 1
        edge_count += label_edges
        per_label.append({'label_basis': list(independent_basis(label)),
                          'vertices': len(members),
                          'same_label_pairs': len(members) * (len(members) - 1) // 2,
                          'monochromatic_edges': label_edges})
    assert len(fixture) == 14
    for first, second in combinations(fixture, 2):
        assert all((first['orthogonal_mask'] >> vector) & 1 for vector in second['basis'])
    fixture_labels = len({entry['label'] for entry in fixture})
    fixture_edges = sum(first['label'] == second['label']
                        for first, second in combinations(fixture, 2))
    first = by_basis[(11,)]
    second = by_basis[(52,)]
    assert first['data'] == (frozenset({0}), frozenset({4}), (15,))
    assert second['data'] == (frozenset({0}), frozenset({4}), (48,))
    assert first['available'] == second['available'] and len(first['available']) == 11
    assert first['key'] == 271 and second['key'] == 304
    assert first['key'] % 11 == second['key'] % 11 == 7
    assert first['label'] == second['label'] == enumerate_span([12, 51])
    assert coordinate_dot(11, 52) == 0 and author['are_orthogonal'](first['data'], second['data'])
    assert by_basis[(5,)]['label'] == enumerate_span([12])
    assert by_basis[(21,)]['label'] == enumerate_span([48])
    assert len(by_basis) == 2809 and len(fibers) == 15
    assert palette_violations == 0 and edge_count == 2873 and fixture_labels == 8
    report = {
        'status': 'diagnostic_passed_candidate_v4_rejected',
        'author_commit': '22aee3de1c2e7460ae00a5c5fbe26be5e3d3dfcc',
        'actual_source_path': 'develop/color_function_candidate_v4',
        'vertices_outside_clique': len(by_basis), 'distinct_inventory_labels': 15,
        'labels_used': len(fibers), 'condition_1_violations': palette_violations,
        'same_label_pairs_checked': pair_count, 'condition_2_violations': edge_count,
        'label_distribution': per_label,
        'fourteen_clique': {'vertices': 14, 'pairs_checked': 91,
                            'distinct_labels': fixture_labels, 'monochromatic_edges': fixture_edges,
                            'vertex_labels': [{'basis': list(entry['basis']),
                                               'label_basis': list(independent_basis(entry['label']))}
                                              for entry in fixture]},
        'previous_zero_lift_pair': {'first_basis': [5], 'first_label_basis': [12],
                                    'second_basis': [21], 'second_label_basis': [48], 'separated': True},
        'residue_counterexample': {
            'first_basis': [11], 'second_basis': [52], 'kernel_basis': [],
            'projection_basis': [4], 'first_lift_values': [15], 'second_lift_values': [48],
            'available_label_count': 11, 'first_key': 271, 'second_key': 304, 'common_index': 7,
            'common_label_basis': [12, 51], 'coordinate_dot': 0,
            'X': [], 'Y': [], 'Z': [[0]], 'lift_value_difference': 33,
            'obstruction_scope': 'Every fixed common-palette ordering with index (integer_multiplier*t + common_K_P_offset) modulo11 identifies these two values. Does not exclude nonlinear or f-dependent geometric selection.'
        },
        'zero_missing_from_original_projection_count': omitted_zero,
        'normalizing_projection_zero_changes_no_labels': True,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - started,
        'scope': 'Independent original-coordinate checks of this requested candidate and written affine-residue obstruction. No solver/Lean/n7 computation; author source/manuscript/certificates unchanged. Structural15/n7 open; historical full n6 theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-v4-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
