"""Audit ordered pure-source normal forms, full stabilizers and local hole geometry."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum
from check_dimension_seven_three_six_charge import linear_values
from check_dimension_seven_four_five_five_charge import inherited_bindings
from check_dimension_seven_four_five_six_charge import cover_binding
from check_dimension_seven_four_five_six_symmetry import image_block, orbit_data


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    holes = set(decoded[:8]) - {0}
    even = [point for point in range(1, 128) if not dot(point, 127)]
    patterns = (1, 2, 4, 7)
    forms = [(pattern, charge) for pattern in patterns for charge in (15, 51, 60, 63)]
    completions = {pattern: decoded[pattern << 3] for pattern in patterns}
    expected = set()
    for even_sum, charge, first_odd, second_odd in permutations(sorted(holes), 4):
        for completion in even:
            other = completion ^ even_sum ^ first_odd ^ second_odd
            if dot(completion, other):
                assert completion not in holes and other not in holes
                expected.add((even_sum, charge, first_odd, second_odd, completion))
    assert len(expected) == 21504
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
    groups = {pattern: [] for pattern in patterns}
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
            for pattern, charge in forms:
                completion = completions[pattern]
                other = completion ^ 63
                key = (mapping[3], mapping[charge], mapping[12], mapping[48], mapping[completion])
                assert key in expected
                assert mapping[other] == mapping[completion] ^ mapping[3] ^ mapping[12] ^ mapping[48]
                assert tuple(dot(mapping[completion], mapping[point]) for point in (3, 12, 48)) == tuple((pattern >> index) & 1 for index in range(3))
                controls[(pattern, charge)][key] += 1
            if all(mapping[point] == point for point in (3, 12, 48)):
                for pattern, completion in completions.items():
                    if mapping[completion] == completion:
                        assert mapping[completion ^ 63] == completion ^ 63
                        groups[pattern].append(mapping)
    assert gram_controls == 526848
    assert all(len(group) == 8 and len(set(group)) == 8 for group in groups.values())
    assert all(len(counter) == 1344 and set(counter.values()) == {8} for counter in controls.values())
    assert sum(len(counter) for counter in controls.values()) == len(expected)
    assert set().union(*(set(counter) for counter in controls.values())) == expected
    assert all(not set(controls[first]) & set(controls[second]) for first, second in combinations(forms, 2))
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
    catalogs = {size: bit_cliques(even, size) for size in (4, 6, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    anchored = [block for block in catalogs[7] if len(set(block) & holes) == 1]
    assert len(catalogs[7]) == 288 and len(anchored) == 224
    masks = {block: mask(block) for blocks in catalogs.values() for block in blocks}
    rows = []
    catalog_actions = 0
    actual_hole_transports = 0
    for pattern, charge in forms:
        completion = completions[pattern]
        other = completion ^ 63
        group = groups[pattern]
        positive = {hole for hole in holes if dot(hole, completion)}
        kernel = holes - positive
        components = {
            'D0': [block for block in catalogs[4] if vector_sum(block) == 3
                   and all(dot(point, 3) and dot(point, charge) for point in block)
                   and completion not in block and other not in block],
            'J1': [block for block in catalogs[6] if vector_sum(block) == 12
                   and completion not in block and other not in block],
            'J2': [block for block in catalogs[6] if vector_sum(block) == 48
                   and completion not in block and other not in block],
            'P1': [block for block in catalogs[6] if vector_sum(block) == completion
                   and set(block) & holes and other not in block],
            'P2': [block for block in catalogs[6] if vector_sum(block) == other
                   and set(block) & holes and completion not in block],
            'H1': [block for block in anchored if completion in block and other not in block],
            'H2': [block for block in anchored if other in block and completion not in block],
            'residual_heptad': [block for block in anchored if set(block) & kernel]}
        expected_four = (10, 10, 16, 8) if pattern == 1 else ((16, 16, 16, 8) if pattern == 7 else (16, 16, 16, 16))
        assert len(components['D0']) == expected_four[(15, 51, 60, 63).index(charge)]
        assert len(components['J1']) == (22 if pattern & 2 else 32)
        assert len(components['J2']) == (22 if pattern & 4 else 32)
        assert all(len(components[name]) == 18 for name in ('P1', 'P2', 'H1', 'H2'))
        assert len(components['residual_heptad']) == 96
        for name, blocks in components.items():
            odd = (3, charge) if name == 'D0' else ((12,) if name == 'J1' else ((48,) if name == 'J2' else ()))
            for block in blocks:
                original = block + tuple(127 ^ point for point in odd)
                assert all(dot(first, second) for first, second in combinations(original, 2))
                if name in ('D0', 'J1', 'J2'):
                    assert not set(block) & holes
                else:
                    actual, = set(block) & holes
                    assert actual in (kernel if name == 'residual_heptad' else positive)
            for mapping in group:
                assert {image_block(block, mapping) for block in blocks} == set(blocks)
                catalog_actions += len(blocks)
                if name not in ('D0', 'J1', 'J2'):
                    for block in blocks:
                        actual, = set(block) & holes
                        mapped, = set(image_block(block, mapping)) & holes
                        assert mapped == mapping[actual] == actual
                        actual_hole_transports += 1
        quartets = []
        array_quartets = []
        for first in components['P1']:
            for second in components['P2']:
                for source_first in components['H1']:
                    for source_second in components['H2']:
                        quartet = (first, second, source_first, source_second)
                        if all(not masks[left] & masks[right] for left, right in combinations(quartet, 2)):
                            quartets.append(quartet)
                        if len(set().union(*(set(block) for block in quartet))) == 26:
                            array_quartets.append(quartet)
        assert quartets == array_quartets
        assert len(quartets) == 1152
        hole_counts = Counter(tuple(next(iter(set(block) & holes)) for block in quartet) for quartet in quartets)
        assert all(set(allocation) == positive for allocation in hole_counts)
        assert set(hole_counts) == set(permutations(sorted(positive))) and set(hole_counts.values()) == {48}
        quartet_action = lambda quartet, mapping: tuple(image_block(block, mapping) for block in quartet)
        quartet_orbits = orbit_data(quartets, group, quartet_action)
        assert quartet_orbits['orbits'] == 144 and quartet_orbits['orbit_size_counts'] == {8: 144}
        assert quartet_orbits['stabilizer_order_counts'] == {1: 144}
        for mapping in group:
            assert {quartet_action(quartet, mapping) for quartet in quartets} == set(quartets)
        component_orbits = {name: orbit_data(blocks, group, image_block) for name, blocks in components.items()}
        rows.append({'functional_values': [(pattern >> index) & 1 for index in range(3)],
                     'a': 3, 'b': charge, 'c': 12, 'd': 48, 'u': completion, 'v': other,
                     'characteristic_projections': sorted(holes - {3, charge, 12, 48}),
                     'characteristic_charge': charge ^ 63, 'positive_holes': sorted(positive),
                     'residual_kernel_holes': sorted(kernel),
                     'ordered_markings_in_orbit': 1344, 'full_ordered_marked_stabilizer_order': 8,
                     'all_M_points_fixed': True, 'ordered_role_exchange_symmetries': 0,
                     'ordered_distinct_positive_hole_allocations': 24,
                     'each_ordered_hole_allocation_marked_stabilizer_order': 8,
                     'component_catalogs_and_orbits': component_orbits,
                     'disjoint_local_P1_P2_H1_H2_quartet_orbits': quartet_orbits,
                     'actual_quartet_hole_allocations': [{'holes': allocation, 'quartets': count} for allocation, count in sorted(hole_counts.items())],
                     'complete_joint_roots_constructed': False})
    previous_name = 'results/dimension-7-four-six-six-pure-sources.json'
    previous = json.loads((root / previous_name).read_text())
    assert previous['checker_sha256'] == digest(root / 'develop/check_dimension_seven_four_six_six_pure_sources.py')
    assert previous['proof_note_sha256'] == digest(root / 'notes/dimension-seven-four-six-six-pure-sources.md')
    for name, checksum in previous['dependency_sha256'].items():
        assert digest(root / name) == checksum, name
    inherited = inherited_bindings(root)
    inherited.update(cover_binding(root, stem) for stem in ('three-six-cover', 'four-six-six-cover', 'four-five-six-cover'))
    assert len(inherited) == 10 and inherited == previous['inherited_theorem_report_sha256']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py', 'develop/check_dimension_seven_three_six_charge.py',
                    'develop/check_dimension_seven_four_five_six_symmetry.py',
                    'develop/check_dimension_seven_four_five_six_charge.py',
                    'notes/dimension-seven-four-six-six-pure-sources.md', previous_name)
    return {'status': 'sixteen_exhaustive_ordered_pure_source_forms_and_full_groups', 'dimension': 7,
            'profile': [4, 6, 6, 5, 2, 8], 'written_exhaustive_normalization': True,
            'full_ordered_marked_groups_proved': True, 'forms': rows,
            'four_functional_patterns_retained': True, 'all_four_actual_positive_holes_retained': True,
            'reversible_recoloring_not_used_as_geometric_role_exchange': True,
            'fixed_M_ordered_markings': len(expected),
            'normalizing_image_controls': sum(sum(counter.values()) for counter in controls.values()),
            'normalizing_images_per_ordered_marking': 8, 'source_Gram_entries_checked': gram_controls,
            'stabilizer_dot_product_pairs_checked': dot_controls,
            'stabilizer_composition_points_checked': closure_controls,
            'component_catalog_actions_checked': catalog_actions,
            'actual_hole_transports_checked': actual_hole_transports,
            'necessary_cover_specification': {'fixed_even_component_sizes': [4, 6, 6, 6, 6, 7, 7],
                                             'remaining_points': 21, 'remaining_holes': 3,
                                             'remaining_pure_heptads': 3, 'eligible_kernel_anchored_heptads': 96},
            'all_component_catalogs_compared_by_array_and_bitmask': True,
            'local_quartets_compared_by_array_and_bitmask': True,
            'new_raw_profile_exclusions': 0, 'target_raw_profile_excluded': False,
            'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 1, 'remaining_C6_through_C8_count': 58, 'remaining_C5_count': 2,
            'inherited_theorem_report_sha256': inherited,
            'complete_joint_roots_constructed': False, 'new_cover_search': False, 'new_cover_certificate': False,
            'historical_cover_audits_rerun': False, 'previous_local_control_audit_rerun': False,
            'new_Lean': False, 'new_independent_Pro_review': False, 'exact_n7': 'open_lower_bound19',
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-pure-source-normalization.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check()
    arguments.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('forms', 'remaining_raw_profile_lists')}, indent=2))
