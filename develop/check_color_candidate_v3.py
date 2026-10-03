"""Check the literal v3 rule and a precisely specified inventory repair."""

from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import runpy
import time

from check_color_candidate import coordinate_dot
from check_complement_projection import dimension, enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def evaluate(entries, inventory, products):
    fibers = defaultdict(list)
    availability_failures = 0
    labels_on_fourteen_clique = []
    for entry in entries:
        available = [label for label in inventory
                     if any(products[first][second]
                            for first in label for second in entry['projection'])]
        assert available
        numeric_key = 0
        for value in entry['values']:
            numeric_key = 64 * numeric_key + value
        assert numeric_key < 2 ** 32
        label = available[numeric_key % len(available)]
        if not any(products[first][second]
                   for first in label for second in entry['projection']):
            availability_failures += 1
        fibers[label].append(entry)
        if entry['on_fourteen_clique']:
            labels_on_fourteen_clique.append(label)
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
    assert len(labels_on_fourteen_clique) == 14
    return {
        'inventory_entries': len(inventory), 'distinct_inventory_labels': len(set(inventory)),
        'labels_used': len(fibers), 'condition_1_violations': availability_failures,
        'same_label_pairs_checked': pair_count, 'condition_2_violations': edge_count,
        'label_distribution': per_label,
        'fourteen_clique_distinct_labels': len(set(labels_on_fourteen_clique)),
        'fourteen_clique_monochromatic_edges': sum(
            first == second for first, second in combinations(labels_on_fourteen_clique, 2))
    }


def main():
    started = time.monotonic()
    source = ROOT / 'develop/color_function_candidate_v3'
    author = runpy.run_path(str(source))
    certificate = ROOT / 'results/full-15-coloring.json'
    records = json.loads(certificate.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    other_isotropic_space = enumerate_span([5, 18, 40])
    products = [[coordinate_dot(first, second) for second in range(64)]
                for first in range(64)]
    literal_inventory = author['ALL_SUBSPACES_T']
    corrected_inventory = [enumerate_span([generator])
                           for generator in [3, 12, 48, 15, 51, 60, 63]]
    corrected_inventory += [enumerate_span(basis) for basis in
                            [[3, 12], [3, 48], [12, 48], [3, 60],
                             [12, 51], [48, 63], [15, 51]]]
    corrected_inventory += [isotropic_space]
    complete_inventory = {enumerate_span(generators) for size in range(1, 4)
                          for generators in combinations(sorted(isotropic_space - {0}), size)}
    assert set(corrected_inventory) == complete_inventory and len(complete_inventory) == 15
    assert len(literal_inventory) == 15 and len(set(literal_inventory)) == 13
    entries = []
    omitted_zero = 0
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
        available = [label for label in literal_inventory
                     if any(products[first][second] for first in label for second in projection)]
        numeric_key = 0
        for value in values:
            numeric_key = 64 * numeric_key + value
        expected_label = available[numeric_key % len(available)]
        assert author['candidate_label_v3'](original) == expected_label
        assert author['candidate_label_v3']((kernel, projection, values)) == expected_label
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(products[vector][basis_vector] == 0
                                     for basis_vector in record['basis']))
        entries.append({'basis': tuple(record['basis']), 'projection': projection,
                        'values': values, 'orthogonal_mask': orthogonal_mask,
                        'on_fourteen_clique': space <= other_isotropic_space})
    literal_result = evaluate(entries, literal_inventory, products)
    repaired_result = evaluate(entries, corrected_inventory, products)
    assert len(entries) == 2809
    assert literal_result['labels_used'] == 13
    assert literal_result['condition_1_violations'] == 0
    assert literal_result['condition_2_violations'] == 3507
    first_data = author['lift_data'](enumerate_span([5]), isotropic_space, complement)
    second_data = author['lift_data'](enumerate_span([21]), isotropic_space, complement)
    assert first_data == (frozenset({0}), frozenset({5}), (0,))
    assert second_data == (frozenset({0}), frozenset({21}), (0,))
    assert author['candidate_label_v3'](first_data) == enumerate_span([3])
    assert author['candidate_label_v3'](second_data) == enumerate_span([3])
    assert coordinate_dot(5, 21) == 0 and author['are_orthogonal'](first_data, second_data)
    assert repaired_result['condition_2_violations'] > 0
    report = {
        'status': 'diagnostic_passed_literal_and_inventory_repaired_v3_rejected',
        'author_commit': 'eed4b180f583d3510b9260e581f7b10adb3de094',
        'actual_source_path': 'develop/color_function_candidate_v3',
        'vertices_outside_clique': len(entries), 'literal_candidate': literal_result,
        'specified_inventory_repair': {
            'change': 'Replace plane(3,15) with plane(3,60) and plane(12,60) with plane(15,51), keeping the other ordered entries.',
            'ordered_label_bases': [list(independent_basis(label)) for label in corrected_inventory],
            'result': repaired_result, 'author_source_modified': False,
            'scope': 'Diagnostic of this specific repaired ordering, not all orderings.'
        },
        'counterexample_for_both_inventories': {
            'first_basis': [5], 'second_basis': [21], 'kernel_basis': [],
            'first_projection_basis': [5], 'second_projection_basis': [21],
            'first_lift_values': [0], 'second_lift_values': [0],
            'common_label_basis': [3], 'coordinate_dot': 0,
            'X': [], 'Y': [], 'Z': [[0]]
        },
        'zero_missing_from_original_projection_count': omitted_zero,
        'normalizing_projection_zero_changes_no_labels': True,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'elapsed_seconds': time.monotonic() - started,
        'scope': 'Targeted literal v3 replay and one precisely specified inventory repair. Written zero-lift counterexample; fourteen-clique used as a regression fixture. No solver/Lean/n7 computation; manuscript/certificates/author source unchanged. Structural15/n7 open; historical full n6 theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-candidate-v3-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
