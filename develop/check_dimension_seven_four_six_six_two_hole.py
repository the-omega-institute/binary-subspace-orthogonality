"""Audit three marked forms of the transferred (4,6,6;5,2,8) two-hole branch."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, vector_sum
from check_dimension_seven_three_six_charge import linear_values
from check_dimension_seven_four_five_five_charge import accounting, inherited_bindings


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    holes = set(decoded[:8]) - {0}
    catalogs = {size: bit_cliques(even, size) for size in (4, 6, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    anchored = [block for block in catalogs[7] if len(set(block) & holes) == 1]
    assert len(catalogs[7]) == 288 and len(anchored) == 224
    by_sum = {total: [block for block in catalogs[6] if vector_sum(block) == total] for total in even}
    assert all(len(blocks) == 32 for blocks in by_sum.values())
    pure = [[block for block in by_sum[total] if len(set(block) & holes) == 1 and other not in block]
            for total, other in ((95, 96), (96, 95))]
    assert all(len(blocks) == 18 for blocks in pure)
    assert all(Counter(next(iter(set(block) & holes)) for block in blocks) == {48: 4, 51: 4, 60: 4, 63: 6}
               for blocks in pure)
    mixed = [[block for block in by_sum[odd] if completion in block] for odd, completion in ((51, 95), (60, 96))]
    assert all(len(blocks) == 6 for blocks in mixed)
    pure_pairs = [(first, second) for first in pure[0] for second in pure[1] if not set(first) & set(second)]
    assert pure_pairs == [(first, second) for first in pure[0] for second in pure[1] if all(point not in second for point in first)]
    assert len(pure_pairs) == 216
    hole_counts = Counter((next(iter(set(first) & holes)), next(iter(set(second) & holes))) for first, second in pure_pairs)
    assert len(hole_counts) == 12 and all(count == (24 if 63 in pair else 12) for pair, count in hole_counts.items())
    assert all(tuple(sorted(block + (total,))) in anchored
               for total, blocks in zip((95, 96), pure) for block in blocks)
    forms = []
    groups = {}
    for charge, order in ((3, 8), (15, 16), (63, 16)):
        four = [block for block in catalogs[4] if vector_sum(block) == 48
                and all(dot(point, 48) and dot(point, charge) for point in block)]
        assert len(four) == 16
        characteristic = tuple(sorted(holes - {48, charge, 51, 60}))
        assert len(characteristic) == 3
        assert vector_sum(characteristic) == charge ^ 63
        for blocks, odd_members in ((four, (48, charge)), (pure[0], ()), (pure[1], ()),
                                   (mixed[0], (51,)), (mixed[1], (60,))):
            for block in blocks:
                original = block + tuple(127 ^ odd for odd in odd_members)
                assert len(set(original)) == len(original)
                assert all(dot(first, second) for first, second in combinations(original, 2))
        assert all(not set(block) & holes for block in four + mixed[0] + mixed[1])
        forms.append({'b': charge, 'a': 48, 'mixed_odd_projections': [51, 60],
                      'pure_six_sums_and_paired_mixed_even_completions': [95, 96],
                      'characteristic_projections': characteristic, 'characteristic_charge': charge ^ 63,
                      'four_even_blocks': four, 'full_marked_stabilizer_order': order})
        groups[charge] = []
    matrices = [linear_values(columns) for columns in permutations(range(1, 8), 3)
                if len(set(linear_values(columns))) == 8]
    symmetric = []
    for bits in range(64):
        first, second, third, first_second, first_third, second_third = [(bits >> index) & 1 for index in range(6)]
        symmetric.append(linear_values((first | first_second << 1 | first_third << 2,
                                       first_second | second << 1 | second_third << 2,
                                       first_third | second_third << 1 | third << 2)))
    assert len(matrices) == 168 and len(set(symmetric)) == 64
    expected = set()
    for first_sum, charge, first_odd, second_odd in permutations(sorted(holes), 4):
        for first_total in even:
            if all(dot(first_total, point) for point in (first_sum, first_odd, second_odd)):
                assert first_total not in holes
                second_total = first_total ^ first_sum ^ first_odd ^ second_odd
                assert second_total not in holes and dot(first_total, second_total)
                expected.add((first_sum, charge, first_odd, second_odd, first_total))
    assert len(expected) == 5376
    controls = Counter()
    controls_by_form = {charge: Counter() for charge in groups}
    source_gram_entries = 0
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
            source_gram_entries += 49
            for charge in groups:
                key = (mapping[48], mapping[charge], mapping[51], mapping[60], mapping[95])
                assert key in expected
                controls[key] += 1
                controls_by_form[charge][key] += 1
                if charge == 3:
                    exchanged = (mapping[48], mapping[charge], mapping[60], mapping[51], mapping[96])
                    assert exchanged in expected
                    controls[exchanged] += 1
                    controls_by_form[charge][exchanged] += 1
                fixed = mapping[51] == 51 and mapping[60] == 60 and mapping[95] == 95 and mapping[96] == 96
                exchanged = mapping[51] == 60 and mapping[60] == 51 and mapping[95] == 96 and mapping[96] == 95
                if mapping[48] == 48 and mapping[charge] == charge and (fixed or exchanged):
                    groups[charge].append(mapping)
    assert set(controls) == expected and set(controls.values()) == {8}
    assert [len(controls_by_form[charge]) for charge in (3, 15, 63)] == [2688, 1344, 1344]
    assert all(set(counter.values()) == {8} for counter in controls_by_form.values())
    assert sum(controls.values()) == 43008 and source_gram_entries == 526848
    assert len(set().union(*(set(counter) for counter in controls_by_form.values()))) == 5376
    dot_controls = 0
    composition_controls = 0
    pair_actions = 0
    rows = []
    for form in forms:
        charge = form['b']
        group = groups[charge]
        group_set = set(group)
        assert len(group_set) == form['full_marked_stabilizer_order'] and tuple(range(128)) in group_set
        restrictions = {tuple(mapping[point] for point in sorted(holes)) for mapping in group}
        assert len(restrictions) == (1 if charge == 3 else 2)
        assert sum(mapping[95] == 95 for mapping in group) == 8

        def pair_image(pair, mapping):
            first, second = pair
            mapped_first = tuple(sorted(mapping[point] for point in first))
            mapped_second = tuple(sorted(mapping[point] for point in second))
            return (mapped_first, mapped_second) if mapping[95] == 95 else (mapped_second, mapped_first)

        def hole_image(pair, mapping):
            first, second = pair
            return (mapping[first], mapping[second]) if mapping[95] == 95 else (mapping[second], mapping[first])

        for mapping in group:
            assert all(dot(first, second) == dot(mapping[first], mapping[second])
                       for first in range(128) for second in range(128))
            dot_controls += 128**2
            for blocks in (form['four_even_blocks'], anchored):
                assert {tuple(sorted(mapping[point] for point in block)) for block in blocks} == set(blocks)
            for source_role in range(2):
                destination_role = source_role if mapping[95] == 95 else 1 - source_role
                for catalogs_by_role in (pure, mixed):
                    assert {tuple(sorted(mapping[point] for point in block)) for block in catalogs_by_role[source_role]} == set(catalogs_by_role[destination_role])
            assert {pair_image(pair, mapping) for pair in pure_pairs} == set(pure_pairs)
            for pair in pure_pairs:
                actual_holes = tuple(next(iter(set(block) & holes)) for block in pair)
                mapped_holes = tuple(next(iter(set(block) & holes)) for block in pair_image(pair, mapping))
                assert mapped_holes == hole_image(actual_holes, mapping)
                pair_actions += 1
        for first_map in group:
            for second_map in group:
                assert tuple(first_map[second_map[point]] for point in range(128)) in group_set
                composition_controls += 128
        representatives = {min(pair_image(pair, mapping) for mapping in group) for pair in pure_pairs}
        orbit_sizes = Counter()
        for representative in representatives:
            orbit = {pair_image(representative, mapping) for mapping in group}
            stabilizer = sum(pair_image(representative, mapping) == representative for mapping in group)
            assert len(orbit) * stabilizer == len(group)
            orbit_sizes[len(orbit)] += 1
        assert sum(size * count for size, count in orbit_sizes.items()) == 216
        hole_orbits = {tuple(sorted({hole_image(pair, mapping) for mapping in group})) for pair in hole_counts}
        assert len(hole_orbits) == (12 if charge == 3 else 7)
        for pair in hole_counts:
            stabilizer = sum(hole_image(pair, mapping) == pair for mapping in group)
            assert stabilizer == (16 if charge != 3 and pair in ((51, 60), (60, 51)) else 8)
        row = {key: value for key, value in form.items() if key != 'four_even_blocks'}
        row.update(four_even_blocks=16, pure_six_blocks_per_role=[18, 18], mixed_even_sextets_per_role=[6, 6],
                   disjoint_ordered_pure_defect_pairs=216, marked_M_restrictions=len(restrictions),
                   pointwise_M_lifts=8, paired_role_exchange_lifts=len(group) - 8,
                   actual_hole_pair_orbits=sorted(hole_orbits),
                   pure_pair_orbits=len(representatives), pure_pair_orbit_size_counts=dict(sorted(orbit_sizes.items())),
                   complete_five_block_roots_constructed=False)
        rows.append(row)
    previous_path = root / 'results/dimension-7-four-five-five-charge.json'
    previous = json.loads(previous_path.read_text())
    assert previous['checker_sha256'] == digest(root / 'develop/check_dimension_seven_four_five_five_charge.py')
    assert previous['proof_note_sha256'] == digest(root / 'notes/dimension-seven-four-five-five-charge.md')
    inherited = inherited_bindings(root)
    assert previous['inherited_theorem_report_sha256'] == inherited
    for name, checksum in previous['dependency_sha256'].items():
        assert digest(root / name) == checksum, name
    current_counts = accounting(root)
    assert current_counts['remaining_raw_profile_lists'] == previous['remaining_raw_profile_lists']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py', 'develop/check_dimension_seven_three_six_charge.py',
                    'develop/check_dimension_seven_four_five_five_charge.py', 'notes/dimension-seven-four-five-five-charge.md',
                    'results/dimension-7-four-five-five-charge.json', 'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'transferred_two_hole_branch_has_three_exhaustive_marked_forms', 'dimension': 7,
            'profile': [4, 6, 6, 5, 2, 8], 'source_profile': [4, 5, 5, 7, 0, 8],
            'scope_of_normalization': 'Only the two-hole subbranch reached by the previous paired-completion transfer; pure sums in their paired mixed classes.',
            'target_raw_profile_excluded': False, 'source_raw_profile_excluded': False,
            'written_exhaustive_normalization': True, 'full_marked_groups_proved': True,
            'M_nonzero': sorted(holes), 'forms': rows,
            'fixed_M_ordered_markings': len(expected), 'normalizing_image_controls': sum(controls.values()),
            'markings_by_form_b': {charge: len(counter) for charge, counter in controls_by_form.items()},
            'normalizing_images_per_ordered_marking': 8, 'source_Gram_entries_checked': source_gram_entries,
            'stabilizer_dot_product_pairs_checked': dot_controls,
            'stabilizer_composition_points_checked': composition_controls,
            'pure_pair_group_actions_and_actual_hole_transports_checked': pair_actions,
            'array_and_bitmask_catalogs_equal': True, 'all_component_catalog_actions_checked': True,
            'pure_six_blocks_by_actual_hole_each_role': {48: 4, 51: 4, 60: 4, 63: 6},
            'disjoint_pure_pairs_by_ordered_holes': [{'holes': pair, 'pairs': count} for pair, count in sorted(hole_counts.items())],
            'all_even_heptads': 288, 'anchored_even_heptads_for_later_cover': 224,
            'complete_five_block_roots_constructed': False, 'new_cover_search': False, 'new_finite_cover_certificate': False,
            'inherited_recoloring_report_sha256': digest(previous_path), 'inherited_theorem_report_sha256': inherited,
            'inherited_source_certificate_and_dependency_bindings_verified': True,
            'historical_cover_audits_rerun': False, 'previous_local_control_audit_rerun': False,
            **current_counts, 'exact_n7': 'open_lower_bound19', 'nineteen_color_witness': False,
            'new_Lean': False, 'new_independent_Pro_review': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-six-six-two-hole.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
