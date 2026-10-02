"""Check v5 in original coordinates and apply the projection obstruction."""

from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import runpy
import time

from check_color_candidate import coordinate_dot
from check_complement_projection import enumerate_span, project_vector
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def main():
    started = time.monotonic()
    source = ROOT / 'color_function_candidate_v5.py'
    author = runpy.run_path(str(source))
    certificate = ROOT / 'results/full-15-coloring.json'
    records = json.loads(certificate.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    other_isotropic_space = enumerate_span([5, 18, 40])
    products = [[coordinate_dot(first, second) for second in range(64)]
                for first in range(64)]
    inventory = author['ALL_SUBSPACES_T']
    complete_inventory = {enumerate_span(generators) for size in range(1, 4)
                          for generators in combinations(sorted(isotropic_space - {0}), size)}
    assert len(inventory) == 15 and set(inventory) == complete_inventory
    fibers = defaultdict(list)
    by_space = {}
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
        image_projection = frozenset(vector ^ project_vector(vector) for vector in space)
        assert image_projection == enumerate_span(list(kernel) + list(values))
        available = [label for label in inventory
                     if any(products[first][second] for first in label for second in projection)]
        if image_projection != frozenset({0}) and image_projection in available:
            expected_label = image_projection
        else:
            containers = [label for label in available if image_projection <= label]
            if image_projection != frozenset({0}) and containers:
                expected_label = min(containers, key=lambda label: (len(label), sorted(label)))
            else:
                expected_label = available[min(projection - {0}) % len(available)]
        assert author['candidate_label_v5'](original) == expected_label
        assert author['candidate_label_v5']((kernel, projection, values)) == expected_label
        palette_violations += expected_label not in available
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(products[vector][basis_vector] == 0
                                     for basis_vector in record['basis']))
        entry = {'basis': tuple(record['basis']), 'label': expected_label,
                 'projection': projection, 'T_projection': image_projection,
                 'kernel': kernel, 'values': values, 'data': original,
                 'orthogonal_mask': orthogonal_mask}
        fibers[expected_label].append(entry)
        by_space[space] = entry
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
                          'vertices': len(members), 'monochromatic_edges': label_edges})
    assert len(fixture) == 14
    for first, second in combinations(fixture, 2):
        assert all((first['orthogonal_mask'] >> vector) & 1 for vector in second['basis'])
    fixture_labels = len({entry['label'] for entry in fixture})
    fixture_edges = sum(first['label'] == second['label']
                        for first, second in combinations(fixture, 2))
    first = by_space[enumerate_span([13, 6])]
    second = by_space[enumerate_span([9, 14])]
    assert first['kernel'] == second['kernel'] == frozenset({0})
    assert first['projection'] == second['projection'] == enumerate_span([1, 4])
    assert first['T_projection'] == second['T_projection'] == enumerate_span([3, 12])
    assert first['label'] == second['label'] == enumerate_span([3, 12])
    cross_gram = [[products[vector][other] for other in [9, 14]] for vector in [13, 6]]
    assert cross_gram == [[0, 0], [0, 0]]
    assert author['are_orthogonal'](first['data'], second['data'])
    requested_labels = [{'basis': [vector],
                         'label_vectors': sorted(by_space[enumerate_span([vector])]['label']),
                         'label_basis': list(independent_basis(by_space[enumerate_span([vector])]['label']))}
                        for vector in [11, 52, 5, 21]]
    assert requested_labels[0]['label_vectors'] == [0, 15]
    assert requested_labels[1]['label_vectors'] == [0, 12, 48, 60]
    assert len(by_space) == 2809 and len(fibers) == 15
    assert palette_violations == 0 and edge_count == 2636 and fixture_labels == 7
    report = {
        'status': 'diagnostic_passed_candidate_v5_rejected',
        'author_commit': '3e9f649dcf8107fe86f2d330b1553b558300c8c7',
        'actual_source_path': 'color_function_candidate_v5.py',
        'source_repair': 'ROOT changed from parents[1] to parent because author committed file at repository root. Mathematical selection unchanged.',
        'vertices_outside_clique': len(by_space), 'distinct_inventory_labels': 15,
        'labels_used': len(fibers), 'condition_1_violations': palette_violations,
        'same_label_pairs_checked': pair_count, 'condition_2_violations': edge_count,
        'label_distribution': per_label, 'requested_line_labels': requested_labels,
        'fourteen_clique': {'vertices': 14, 'pairs_checked': 91,
                            'distinct_labels': fixture_labels, 'monochromatic_edges': fixture_edges,
                            'vertex_labels': [{'basis': list(entry['basis']),
                                               'label_basis': list(independent_basis(entry['label']))}
                                              for entry in fixture]},
        'projection_obstruction': {
            'first_basis': [13, 6], 'second_basis': [9, 14], 'kernel_basis': [],
            'S_projection_basis': [1, 4], 'T_projection_basis': [3, 12],
            'first_lifts_on_1_4': [12, 15], 'second_lifts_on_1_4': [15, 3],
            'common_label_basis': [3, 12], 'cross_gram': cross_gram,
            'scope': 'Application of manuscript Proposition5.5: no coloring based solely on the two coordinate projections P,R is proper. A0=R for every vertex; changing a tie order or fallback cannot separate this pair.'},
        'A0_equals_T_projection_checked_vertices': len(by_space),
        'zero_missing_from_original_projection_count': omitted_zero,
        'normalizing_projection_zero_changes_no_labels': True,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - started,
        'scope': 'Requested finite v5 diagnostic and written projection obstruction; no solver, Lean or n7 computation. TeX/PDF/certificates unchanged. Structural15/n7 open; historical full n6 Lean theorem retains three standard plus four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-v5-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
