"""Audit the forced two-charge recoloring of (4,5,5;7,0,8)."""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum


def independent(points):
    return len(set(points)) == len(points) and all(dot(left, right) for left, right in combinations(points, 2))


def inherited_bindings(root):
    identities = {}
    for stem in ('three-five-cover', 'four-even-pairs', 'five-four-D-cover',
                 'five-four-H-cover', 'five-four-G-cover', 'five-four-Z-cover'):
        report_name = 'results/dimension-7-' + stem + '-check.json'
        report = json.loads((root / report_name).read_text())
        source_stem = stem.replace('-', '_')
        paths = {'certificate_sha256': 'results/dimension-7-' + stem + '-proof.json',
                 'builder_sha256': 'develop/build_dimension_seven_' + source_stem + '.py',
                 'checker_sha256': 'develop/check_dimension_seven_' + source_stem + '.py',
                 'proof_note_sha256': 'notes/dimension-seven-' + stem + '.md'}
        for key, name in paths.items():
            assert report[key] == digest(root / name), name
        for name, checksum in report.get('dependency_sha256', {}).items():
            assert digest(root / name) == checksum, name
        identities[report_name] = digest(root / report_name)
    report_name = 'results/dimension-7-four-four-hole-cover.json'
    report = json.loads((root / report_name).read_text())
    paths = {'certificate_sha256': 'results/dimension-7-four-four-hole-cover-certificate.json',
             'auditor_sha256': 'develop/check_four_four_hole_cover.py',
             'builder_sha256': 'develop/build_four_four_hole_cover.py',
             'proof_note_sha256': 'notes/dimension-seven-four-four-hole-cover.md',
             'prior_two_six_report_sha256': 'results/dimension-7-two-six-profiles.json'}
    for key, name in paths.items():
        assert report[key] == digest(root / name), name
    identities[report_name] = digest(root / report_name)
    return identities


def accounting(root):
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    previous = json.loads((root / 'results/dimension-7-four-four-six-charge.json').read_text())
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 37}
    for name, sizes, prefix in (('5+6', (5, 6), 'five_six'), ('6+6+6', (6, 6, 6), 'three_six')):
        domains = [range(size + 1) if size != 6 else (0, 2, 4, 5, 6) for size in sizes]
        direct = set()
        for counts in product(*domains):
            if name == '6+6+6' and tuple(sorted(counts)) != counts:
                continue
            for pure_even in range(19):
                for mixed in range(19):
                    pure_odd = 18 - len(sizes) - pure_even - mixed
                    if pure_odd >= 0 and 7 * pure_even + 6 * mixed + sum(counts) == 63 and mixed + 7 * pure_odd + sum(sizes) - sum(counts) + 4 == 64:
                        direct.add(counts + (pure_even, mixed, pure_odd))
        archived = {tuple(row['defect_even_counts'] + row['saturated_counts']) for row in raw['count_profiles'][name]}
        assert direct == archived and len(direct) == (46 if prefix == 'five_six' else 48)
        assert len(previous['remaining_raw_profile_lists'][prefix]) == previous['remaining_raw_profiles'][prefix]
        assert all(tuple(row) in direct for row in previous['remaining_raw_profile_lists'][prefix])
    rows = previous['remaining_raw_profile_lists']['three_six']
    assert [4, 5, 5, 7, 0, 8] in rows and [4, 6, 6, 5, 2, 8] in rows
    assert len([row for row in rows if row[-1] == 8]) == 3
    return {'new_raw_profile_exclusions': 0, 'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 3, 'remaining_C6_through_C8_count': 60,
            'remaining_C5_count': 2, 'characteristic_sizes_still_open': [4, 5, 6, 7, 8]}


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    catalogs = {size: bit_cliques(even, size) for size in (4, 5, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    five = defaultdict(list)
    completion_controls = 0
    for odd_projection in sorted(holes):
        for block in catalogs[5]:
            if not all(dot(point, odd_projection) for point in block):
                continue
            radical = vector_sum(block)
            completion = radical ^ odd_projection
            original = block + (127 ^ odd_projection,)
            assert independent(original) and radical not in holes and radical != 0
            assert dot(radical, odd_projection) and all(not dot(point, radical) for point in block)
            assert completion not in holes and completion not in original and independent(original + (completion,))
            assert vector_sum(block + (completion,)) == odd_projection
            assert [point for point in even if independent(original + (point,))] == [completion]
            assert not set(block) & holes
            five[(odd_projection, radical)].append((block, mask(block)))
            completion_controls += 1
    assert completion_controls == 1344 and all(len(blocks) == 6 for blocks in five.values())
    four = {}
    for even_sum, charge in permutations(sorted(holes), 2):
        blocks = [block for block in catalogs[4] if vector_sum(block) == even_sum
                  and all(dot(point, even_sum) and dot(point, charge) for point in block)]
        assert len(blocks) == 16
        assert all(independent(block + (127 ^ even_sum, 127 ^ charge)) for block in blocks)
        four[(even_sum, charge)] = [(block, mask(block)) for block in blocks]
    marking_count = 0
    characteristic_zero_count = 0
    compatible_triples = 0
    source_counts = Counter()
    charge_pairs = set()
    for first_sum, first_charge, first_odd, second_odd in permutations(sorted(holes), 4):
        for first_radical in even:
            if not all(dot(first_radical, point) for point in (first_sum, first_odd, second_odd)):
                continue
            second_radical = first_radical ^ first_sum
            first_completion = first_radical ^ first_odd
            second_completion = second_radical ^ second_odd
            characteristic = holes - {first_sum, first_charge, first_odd, second_odd}
            characteristic_charge = vector_sum(characteristic)
            assert first_charge ^ first_completion ^ second_completion == characteristic_charge
            assert first_completion not in holes and second_completion not in holes
            assert first_completion != second_completion and dot(first_completion, second_completion)
            pair_sum = first_completion ^ second_completion
            assert pair_sum == first_sum ^ first_odd ^ second_odd and pair_sum in holes
            assert dot(first_completion, pair_sum) and dot(second_completion, pair_sum)
            assert (pair_sum == first_charge) == (characteristic_charge == 0)
            assert pair_sum == first_charge or pair_sum in characteristic
            assert all(dot(first_radical, hole) == dot(second_radical, hole) for hole in holes)
            assert first_charge in holes and first_completion ^ second_completion ^ first_charge == characteristic_charge
            assert dot(first_charge, first_completion) ^ dot(first_charge, second_completion) ^ dot(first_completion, second_completion) == 1
            marking_count += 1
            characteristic_zero_count += characteristic_charge == 0
            charge_pairs.add((first_completion, second_completion))
            for mixed_block, mixed_mask in four[(first_sum, first_charge)]:
                for first_block, first_mask in five[(first_odd, first_radical)]:
                    if mixed_mask & first_mask:
                        continue
                    for second_block, second_mask in five[(second_odd, second_radical)]:
                        if (mixed_mask | first_mask) & second_mask:
                            continue
                        compatible_triples += 1
                        classes = (mixed_block + (127 ^ first_sum, 127 ^ first_charge),
                                   first_block + (127 ^ first_odd,), second_block + (127 ^ second_odd,))
                        before = set().union(*map(set, classes))
                        assert len(before) == 18
                        for role, completion in ((1, first_completion), (2, second_completion)):
                            other_role = 3 - role
                            if completion in mixed_block:
                                source = 0
                                source_counts['four_even_defect_to_three_five_exclusion'] += 1
                            elif completion in classes[other_role]:
                                source = other_role
                                source_counts['other_five_even_defect_to_four_even_pair_exclusion'] += 1
                            else:
                                source_counts['outside_all_defects_requires_pure_even_source'] += 1
                                continue
                            reduced = tuple(point for point in classes[source] if point != completion)
                            completed = classes[role] + (completion,)
                            untouched = classes[3 - source - role]
                            assert len(reduced) == 5 and len(completed) == 7
                            assert independent(reduced) and independent(completed)
                            reduced_even_count = sum(not dot(point, 127) for point in reduced)
                            untouched_even_count = sum(not dot(point, 127) for point in untouched)
                            assert (reduced_even_count, untouched_even_count, 7, 1, 8) == ((3, 5, 7, 1, 8) if source == 0 else (4, 4, 7, 1, 8))
                            assert sum(not dot(point, 127) for point in completed) == 6
                            assert set(reduced) | set(completed) | set(untouched) == before
                            assert not set(reduced) & set(completed)
    assert marking_count == 5376 and len(charge_pairs) == 224
    assert sum(source_counts.values()) == 2 * compatible_triples
    anchored = [(block, mask(block)) for block in catalogs[7] if set(block) & holes]
    assert len(anchored) == 224 and len(catalogs[7]) == 288
    assert all(vector_sum(block) == 0 and len(set(block) & holes) == 1 for block, block_mask in anchored)
    same_source_controls = 0
    distinct_source_controls = 0
    for first_completion, second_completion in sorted(charge_pairs):
        first_rows = [(block, block_mask) for block, block_mask in anchored if first_completion in block]
        second_rows = [(block, block_mask) for block, block_mask in anchored if second_completion in block]
        for block, block_mask in first_rows:
            if second_completion in block:
                reduced = tuple(point for point in block if point not in (first_completion, second_completion))
                assert len(reduced) == 5 and independent(reduced)
                assert vector_sum(reduced) == first_completion ^ second_completion
                assert set(reduced) | {first_completion, second_completion} == set(block)
                same_source_controls += 1
        for first_block, first_mask in first_rows:
            for second_block, second_mask in second_rows:
                if first_mask & second_mask:
                    continue
                first_reduced = tuple(point for point in first_block if point != first_completion)
                second_reduced = tuple(point for point in second_block if point != second_completion)
                first_hole, = set(first_reduced) & holes
                second_hole, = set(second_reduced) & holes
                assert first_hole != second_hole
                assert vector_sum(first_reduced) == first_completion and vector_sum(second_reduced) == second_completion
                assert dot(first_hole, first_completion) and dot(second_hole, second_completion)
                assert set(first_reduced) | set(second_reduced) | {first_completion, second_completion} == set(first_block) | set(second_block)
                distinct_source_controls += 1
    dependencies = ('develop/check_dimension_seven_five_four_charge.py', 'notes/dimension-seven-two-six-profiles.md',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-nineteen-obstruction.md',
                    'results/dimension-7-size-four.json', 'results/dimension-7-four-four-six-charge.json')
    return {'status': 'four_five_five_recolors_to_open_four_six_six_two_hole_branch',
            'dimension': 7, 'profile': [4, 5, 5, 7, 0, 8], 'characteristic_class_size': 4,
            'resulting_profile': [4, 6, 6, 5, 2, 8], 'target_raw_profile_excluded': False,
            'resulting_profile_excluded': False, 'written_recoloring_reduction': True,
            'completion_vectors_forced_into_distinct_pure_even_heptads': True,
            'resulting_pure_six_sums_outside_M': True, 'resulting_actual_defect_holes': [1, 1],
            'resulting_actual_holes_distinct': True,
            'unique_mixed_heptad_completion_controls': completion_controls,
            'fixed_M_role_and_radical_markings': marking_count,
            'markings_with_zero_characteristic_charge': characteristic_zero_count,
            'compatible_disjoint_local_defect_triples': compatible_triples,
            'single_transfer_source_controls': dict(sorted(source_counts.items())),
            'distinct_ordered_completion_pairs': len(charge_pairs),
            'same_source_anchored_heptad_controls': same_source_controls,
            'disjoint_distinct_source_heptad_pair_controls': distinct_source_controls,
            'array_and_bitmask_catalogs_equal': True,
            'inherited_theorem_report_sha256': inherited_bindings(root),
            'inherited_finite_certificate_and_source_hash_bindings_verified': True,
            'prior_finite_cover_inputs_retained': True, 'historical_cover_audits_rerun': False,
            'new_cover_search': False, 'new_finite_cover_certificate': False,
            'complete_covering_roots_constructed': False,
            **accounting(root), 'exact_n7': 'open_lower_bound19', 'nineteen_color_witness': False,
            'new_Lean': False, 'new_independent_Pro_review': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-five-five-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written unique even completions force distinct pure-even source heptads via three exact prior exclusions; simultaneous transfer gives the open (4,6,6;5,2,8) branch with two distinct actual holes. Modular local controls and inherited hash bindings checked, no covering search or historical audit rerun. No raw row removed;25/37 remain and exactn7 open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
