"""Audit ordered normal forms and full marked groups for (4,5,6;6,1,8)."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, vector_sum
from check_dimension_seven_three_six_charge import linear_values
from check_dimension_seven_four_five_five_charge import inherited_bindings
from check_dimension_seven_four_five_six_charge import cover_binding


def image_block(block, mapping):
    return tuple(sorted(mapping[point] for point in block))


def orbit_data(objects, group, action):
    remaining = set(objects)
    sizes = Counter()
    stabilizers = Counter()
    while remaining:
        representative = min(remaining)
        orbit = {action(representative, mapping) for mapping in group}
        assert orbit <= remaining
        stabilizer = sum(action(representative, mapping) == representative for mapping in group)
        assert len(orbit) * stabilizer == len(group)
        sizes[len(orbit)] += 1
        stabilizers[stabilizer] += 1
        remaining -= orbit
    assert sum(size * count for size, count in sizes.items()) == len(objects)
    return {'objects': len(objects), 'orbits': sum(sizes.values()),
            'orbit_size_counts': dict(sorted(sizes.items())),
            'stabilizer_order_counts': dict(sorted(stabilizers.items()))}


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    holes = set(decoded[:8]) - {0}
    even = [point for point in range(1, 128) if not dot(point, 127)]
    forms = [(eta, charge) for eta in (0, 1) for charge in (15, 51, 60, 63)]
    completions = {0: (71, 120), 1: (89, 102)}
    expected = set()
    for even_sum, charge, odd_projection, mixed_odd in permutations(sorted(holes), 4):
        for completion in even:
            other = completion ^ even_sum ^ odd_projection ^ mixed_odd
            if dot(completion, odd_projection) and dot(completion, even_sum) == dot(completion, mixed_odd) and dot(completion, other):
                assert completion not in holes and other not in holes
                expected.add((even_sum, charge, odd_projection, mixed_odd, completion))
    assert len(expected) == 10752
    matrices = [linear_values(columns) for columns in permutations(range(1, 8), 3)
                if len(set(linear_values(columns))) == 8]
    symmetric = []
    for bits in range(64):
        first, second, third, first_second, first_third, second_third = [(bits >> index) & 1 for index in range(6)]
        symmetric.append(linear_values((first | first_second << 1 | first_third << 2,
                                       first_second | second << 1 | second_third << 2,
                                       first_third | second_third << 1 | third << 2)))
    assert len(matrices) == 168 and len(set(symmetric)) == 64
    controls = {form: Counter() for form in forms}
    groups = {eta: [] for eta in (0, 1)}
    gram_controls = 0
    for matrix in matrices:
        dual = tuple(next(destination for destination in range(8)
                          if all(dot(matrix[1 << index], destination) == ((source >> index) & 1)
                                 for index in range(3))) for source in range(8))
        for shear in symmetric:
            images = tuple(decoded[matrix[bits & 7] ^ shear[dual[(bits >> 3) & 7]]
                                   | dual[(bits >> 3) & 7] << 3 | bits & 64] for bits in range(128))
            mapping = tuple(images[encoded[point]] for point in range(128))
            assert len(set(mapping)) == 128 and mapping[127] == 127
            assert all(dot(first, second) == dot(mapping[first], mapping[second]) for first in basis for second in basis)
            gram_controls += 49
            for eta, charge in forms:
                completion, other = completions[eta]
                key = (mapping[3], mapping[charge], mapping[12], mapping[48], mapping[completion])
                assert key in expected
                assert mapping[other] == mapping[completion] ^ mapping[3] ^ mapping[12] ^ mapping[48]
                assert dot(mapping[completion], mapping[3]) == eta
                controls[(eta, charge)][key] += 1
            if all(mapping[point] == point for point in (3, 12, 48)):
                for eta, (completion, other) in completions.items():
                    if mapping[completion] == completion:
                        assert mapping[other] == other
                        groups[eta].append(mapping)
    assert gram_controls == 526848
    assert all(len(group) == 8 and len(set(group)) == 8 for group in groups.values())
    assert all(len(counter) == 1344 and set(counter.values()) == {8} for counter in controls.values())
    assert sum(len(counter) for counter in controls.values()) == len(expected)
    assert set().union(*(set(counter) for counter in controls.values())) == expected
    for first, second in combinations(forms, 2):
        assert not set(controls[first]) & set(controls[second])
    dot_controls = 0
    closure_controls = 0
    for group in groups.values():
        assert tuple(range(128)) in group
        for mapping in group:
            assert all(mapping[hole] == hole for hole in holes)
            assert all(dot(first, second) == dot(mapping[first], mapping[second])
                       for first in range(128) for second in range(128))
            dot_controls += 128**2
        for first in group:
            for second in group:
                assert tuple(first[second[point]] for point in range(128)) in group
                closure_controls += 128
    catalogs = {size: bit_cliques(even, size) for size in (4, 5, 6, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    anchored = [block for block in catalogs[7] if set(block) & holes]
    assert len(catalogs[7]) == 288 and len(anchored) == 224
    rows = []
    actual_hole_transports = 0
    catalog_actions = 0
    for eta, charge in forms:
        completion, other = completions[eta]
        group = groups[eta]
        components = {
            'D0': [block for block in catalogs[4] if vector_sum(block) == 3
                   and all(dot(point, 3) and dot(point, charge) for point in block)
                   and completion not in block and other not in block],
            'D1': [block for block in catalogs[5] if all(dot(point, 12) for point in block)
                   and vector_sum(block) == completion ^ 12 and other not in block],
            'P': [block for block in catalogs[6] if vector_sum(block) == other
                  and set(block) & holes and completion not in block],
            'Hq': [block for block in anchored if other in block and completion not in block],
            'Ht': [block for block in anchored if completion in block and other not in block],
            'J_pure_source': [block for block in catalogs[6] if vector_sum(block) == 48
                              and completion not in block and other not in block]}
        if eta:
            components['J_mixed_source'] = [block for block in catalogs[6] if vector_sum(block) == 48
                                            and completion in block and other not in block]
        assert len(components['D0']) == (8 if eta == 1 and charge == 63 else 16)
        assert len(components['D1']) == 4
        assert all(len(components[name]) == 18 for name in ('P', 'Hq', 'Ht'))
        assert len(components['J_pure_source']) == (22 if eta else 32)
        if eta:
            assert len(components['J_mixed_source']) == 4
        odd_roles = {'D0': (3, charge), 'D1': (12,), 'J_pure_source': (48,), 'J_mixed_source': (48,)}
        for name, blocks in components.items():
            for block in blocks:
                original = block + tuple(127 ^ odd for odd in odd_roles.get(name, ()))
                assert len(set(original)) == len(original)
                assert all(dot(first, second) for first, second in combinations(original, 2))
                if name in ('P', 'Hq', 'Ht'):
                    assert len(set(block) & holes) == 1
                else:
                    assert not set(block) & holes
            for mapping in group:
                assert {image_block(block, mapping) for block in blocks} == set(blocks)
                catalog_actions += len(blocks)
                if name in ('P', 'Hq', 'Ht'):
                    for block in blocks:
                        hole, = set(block) & holes
                        mapped_hole, = set(image_block(block, mapping)) & holes
                        assert mapped_hole == mapping[hole] == hole
                        actual_hole_transports += 1
        pure_source_pairs = [(first, second) for first in components['P'] for second in components['Hq']
                             if not set(first) & set(second)]
        assert pure_source_pairs == [(first, second) for first in components['P'] for second in components['Hq']
                                     if all(point not in second for point in first)]
        assert len(pure_source_pairs) == 144
        hole_counts = Counter((next(iter(set(first) & holes)), next(iter(set(second) & holes)))
                              for first, second in pure_source_pairs)
        assert len(hole_counts) == 12 and set(hole_counts.values()) == {12}
        assert all(first != second and dot(first, completion) and dot(second, completion)
                   for first, second in hole_counts)
        pair_action = lambda pair, mapping: (image_block(pair[0], mapping), image_block(pair[1], mapping))
        pair_orbits = orbit_data(pure_source_pairs, group, pair_action)
        assert pair_orbits['orbits'] == 48 and pair_orbits['orbit_size_counts'] == {2: 24, 4: 24}
        for mapping in group:
            assert {pair_action(pair, mapping) for pair in pure_source_pairs} == set(pure_source_pairs)
        component_orbits = {name: orbit_data(blocks, group, image_block) for name, blocks in components.items()}
        rows.append({'eta': eta, 'a': 3, 'b': charge, 'c': 12, 'd': 48, 't': completion, 'q': other,
                     'characteristic_projections': sorted(holes - {3, charge, 12, 48}),
                     'characteristic_charge': charge ^ 63,
                     'ordered_markings_in_orbit': 1344, 'full_ordered_marked_stabilizer_order': 8,
                     'all_M_points_fixed': True, 'role_exchange_symmetries': 0,
                     'completion_source_cases': ['pure'] + (['mixed'] if eta else []),
                     'component_catalogs_and_orbits': component_orbits,
                     'disjoint_P_Hq_pair_orbits': pair_orbits,
                     'ordered_actual_P_Hq_hole_allocations': [{'holes': pair, 'pairs': count} for pair, count in sorted(hole_counts.items())],
                     'complete_joint_roots_constructed': False})
    previous_name = 'results/dimension-7-four-five-six-charge.json'
    previous = json.loads((root / previous_name).read_text())
    assert previous['checker_sha256'] == digest(root / 'develop/check_dimension_seven_four_five_six_charge.py')
    assert previous['proof_note_sha256'] == digest(root / 'notes/dimension-seven-four-five-six-charge.md')
    for name, checksum in previous['dependency_sha256'].items():
        assert digest(root / name) == checksum, name
    inherited = inherited_bindings(root)
    inherited.update(cover_binding(root, stem) for stem in ('three-six-cover', 'four-six-six-cover'))
    assert inherited == previous['inherited_theorem_report_sha256']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py', 'develop/check_dimension_seven_three_six_charge.py',
                    'develop/check_dimension_seven_four_five_six_charge.py', 'notes/dimension-seven-four-five-six-charge.md',
                    previous_name, 'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'eight_exhaustive_ordered_marked_forms_and_full_groups', 'dimension': 7,
            'profile': [4, 5, 6, 6, 1, 8], 'written_exhaustive_normalization': True,
            'full_ordered_marked_groups_proved': True, 'source_case_branches': 12,
            'recoloring_role_exchange_is_not_an_ordered_marked_isometry': True,
            'forms': rows, 'fixed_M_ordered_markings': len(expected),
            'normalizing_image_controls': sum(sum(counter.values()) for counter in controls.values()),
            'normalizing_images_per_ordered_marking': 8, 'source_Gram_entries_checked': gram_controls,
            'stabilizer_dot_product_pairs_checked': dot_controls,
            'stabilizer_composition_points_checked': closure_controls,
            'component_catalog_actions_checked': catalog_actions,
            'actual_hole_transports_checked': actual_hole_transports,
            'necessary_cover_specification': {
                'pure_t_source': {'fixed_even_component_sizes': [4, 5, 6, 6, 7, 7],
                                  'remaining_points': 28, 'remaining_holes': 4, 'remaining_pure_heptads': 4},
                'mixed_t_source': {'fixed_even_component_sizes': [4, 5, 6, 6, 7],
                                   'remaining_points': 35, 'remaining_holes': 5, 'remaining_pure_heptads': 5},
                'eligible_even_heptads': 224, 'all_eligible_heptads_anchored_by_hole_capacity': True},
            'all_component_catalogs_compared_by_array_and_bitmask': True,
            'new_raw_profile_exclusions': 0, 'target_raw_profile_excluded': False,
            'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 2, 'remaining_C6_through_C8_count': 59, 'remaining_C5_count': 2,
            'inherited_theorem_report_sha256': inherited,
            'complete_joint_roots_constructed': False, 'new_cover_search': False, 'new_cover_certificate': False,
            'historical_cover_audits_rerun': False, 'previous_local_control_audit_rerun': False,
            'new_Lean': False, 'new_independent_Pro_review': False, 'exact_n7': 'open_lower_bound19',
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-five-six-symmetry.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check()
    arguments.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('forms', 'remaining_raw_profile_lists')}, indent=2))
