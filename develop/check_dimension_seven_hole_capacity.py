"""Check uniform hole capacities and all newly excluded size-four count profiles."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def vector_sum(vectors):
    total = 0
    for vector in vectors:
        total ^= vector
    return total


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    prior_count = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    prior_charge = json.loads((root / 'results/dimension-7-five-six-split31.json').read_text())
    prior_seven = json.loads((root / 'results/dimension-7-seven-holes.json').read_text())
    prior_eight = json.loads((root / 'results/dimension-7-nineteen-obstruction.json').read_text())
    sources = ((prior_count, 'develop/check_dimension_seven_size_four.py', 'notes/dimension-seven-size-four.md'),
               (prior_charge, 'develop/check_dimension_seven_five_six_split31.py', 'notes/dimension-seven-five-six-split31.md'),
               (prior_seven, 'develop/check_dimension_seven_seven_holes.py', 'notes/dimension-seven-seven-holes.md'),
               (prior_eight, 'develop/check_dimension_seven_nineteen_obstruction.py', 'notes/dimension-seven-nineteen-obstruction.md'))
    for report, checker, note in sources:
        assert report['checker_sha256'] == digest(root / checker)
        assert report['proof_note_sha256'] == digest(root / note)
    for name, expected in prior_charge['dependency_sha256'].items():
        assert digest(root / name) == expected
    assert prior_seven['anchored_seven_partial_spreads'] == 1792
    assert prior_seven['deletion_set_equals_partial_spread_set']
    assert prior_seven['completion_multiplicity'] == 1
    assert prior_seven['hole_lagrangians_per_partial_spread'] == 2
    assert not prior_eight['all_partial_spreads_enumerated']
    first = tuple(sorted(vector_sum(base[index] for index in range(3) if bits & (1 << index))
                         for base in ((3, 12, 48),) for bits in range(1, 8)))
    second = tuple(sorted(vector_sum(base[index] for index in range(3) if bits & (1 << index))
                          for base in ((65, 71, 95),) for bits in range(1, 8)))
    assert len(set(first)) == len(set(second)) == 7 and not set(first) & set(second)
    for space in (first, second):
        assert all(not dot(point, 127) for point in space)
        assert all(not dot(left, right) for left in space for right in space)
        assert all(left ^ right in set(space) | {0} for left in space for right in space)
    local_controls = {}
    for component_count, spaces in ((1, (first,)), (2, (first, second))):
        holes = tuple(sorted(point for space in spaces for point in space))
        pairs = [pair for pair in combinations(holes, 2) if dot(*pair)]
        triples = [triple for triple in combinations(holes, 3)
                   if all(dot(left, right) for left, right in combinations(triple, 2))]
        assert not triples and len(pairs) == (0 if component_count == 1 else 28)
        odd_controls = []
        for odd in holes:
            containing = next(space for space in spaces if odd in space)
            compatible = tuple(point for point in holes if dot(point, odd))
            assert not set(compatible) & set(containing)
            assert len(compatible) == (0 if component_count == 1 else 4)
            assert not any(dot(left, right) for left, right in combinations(compatible, 2))
            odd_controls.append((odd, compatible))
        local_controls[component_count] = {
            'hole_points': len(holes), 'pair_tests': len(list(combinations(holes, 2))),
            'compatible_even_pairs': len(pairs), 'triple_tests': len(list(combinations(holes, 3))),
            'compatible_even_triples': len(triples), 'odd_projection_tests': len(odd_controls),
            'odd_even_pair_tests': len(holes) ** 2,
            'mixed_compatible_hole_points_per_odd': 0 if component_count == 1 else 4,
            'pure_even_hole_capacity': component_count, 'mixed_hole_capacity': component_count - 1,
            'odd_control_sha256': hashlib.sha256(json.dumps(odd_controls).encode()).hexdigest()}
    patterns = {'4': (4,), '5+6': (5, 6), '6+6+6': (6, 6, 6)}
    capacities = {}
    excluded = {}
    all_rows = {}
    for pattern, sizes in patterns.items():
        choices = ([range(5)] if pattern == '4' else
                   [range(6), (0, 2, 4, 5, 6)] if pattern == '5+6' else None)
        even_profiles = list(product(*choices)) if choices else list(combinations_with_replacement((0, 2, 4, 5, 6), 3))
        direct = []
        formula = []
        for even in even_profiles:
            odd = tuple(size - count for size, count in zip(sizes, even))
            for pure_even, mixed, pure_odd in product(range(19), repeat=3):
                if (pure_even + mixed + pure_odd == 18 - len(sizes)
                        and 7 * pure_even + 6 * mixed + sum(even) == 63
                        and mixed + 7 * pure_odd + sum(odd) + 4 == 64):
                    direct.append(even + (pure_even, mixed, pure_odd))
            for parameter in range(-10, 11):
                mixed = sum(even) + 7 * parameter
                pure_even = 9 - sum(even) - 6 * parameter
                pure_odd = 9 - len(sizes) - parameter
                if min(pure_even, mixed, pure_odd) >= 0:
                    formula.append(even + (pure_even, mixed, pure_odd))
        direct.sort()
        formula.sort()
        prior_rows = sorted(tuple(row['defect_even_counts'] + row['saturated_counts'])
                            for row in prior_count['count_profiles'][pattern])
        assert direct == formula == prior_rows
        assert len(direct) == {'4': 9, '5+6': 46, '6+6+6': 48}[pattern]
        capacities[pattern] = []
        excluded[pattern] = []
        all_rows[pattern] = direct
        for row in direct:
            even = row[:-3]
            odd = tuple(size - count for size, count in zip(sizes, even))
            pure_even, mixed, pure_odd = row[-3:]
            if pure_odd not in (7, 8):
                continue
            component_count = 9 - pure_odd
            pure_defects = sum(count == 0 for count in odd)
            mixed_defects = sum(even_count > 0 and odd_count > 0
                                for even_count, odd_count in zip(even, odd))
            capacity = component_count * (pure_even + pure_defects) + (component_count - 1) * (mixed + mixed_defects)
            class_capacities = ([component_count] * pure_even + [component_count - 1] * mixed
                                + [min(even_count, component_count if odd_count == 0 else component_count - 1)
                                   for even_count, odd_count in zip(even, odd)])
            assert capacity == sum(class_capacities)
            item = {'profile': list(row), 'pure_even_defects': pure_defects, 'mixed_defects': mixed_defects,
                    'hole_points': 7 * component_count, 'capacity': capacity,
                    'excluded': capacity < 7 * component_count}
            capacities[pattern].append(item)
            if item['excluded']:
                excluded[pattern].append(list(row))
    assert {pattern: len(rows) for pattern, rows in excluded.items()} == {'4': 6, '5+6': 12, '6+6+6': 9}
    prior_remaining = prior_charge['five_six_remaining_raw_profiles']
    assert len(prior_remaining) == prior_charge['five_six_remaining_unexcluded_count'] == 43
    previous_exclusions = [[1, 6, 8, 0, 8], [2, 5, 8, 0, 8], [5, 2, 8, 0, 8]]
    assert sorted(tuple(row) for row in prior_remaining + previous_exclusions) == all_rows['5+6']
    assert all(prior_remaining.count(row) == 1 for row in excluded['5+6'])
    remaining_five = [row for row in prior_remaining if row not in excluded['5+6']]
    remaining_three = [list(row) for row in all_rows['6+6+6'] if list(row) not in excluded['6+6+6']]
    assert len(remaining_five) == 31 and len(remaining_three) == 39
    assert [2, 6, 7, 1, 8] in remaining_five
    dependency_counts = Counter(row[-1] for pattern in ('5+6', '6+6+6') for row in excluded[pattern])
    assert dependency_counts == {7: 13, 8: 8}
    dependencies = ('results/dimension-7-size-four.json', 'results/dimension-7-five-six-split31.json',
                    'results/dimension-7-seven-holes.json', 'results/dimension-7-nineteen-obstruction.json')
    return {'status': 'uniform_hole_capacity_excludes_twenty_one_further_size_four_profiles',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False,
            'nineteen_color_witness': False, 'characteristic_class_size_range': [4, 8],
            'characteristic_size_four_excluded': False, 'single_four_entire_branch_previously_excluded': True,
            'raw_profile_counts': {'4': 9, '5+6': 46, '6+6+6': 48},
            'direct_and_formula_profile_sets_equal': True, 'capacity_controls': capacities,
            'newly_excluded_five_six_profiles': excluded['5+6'],
            'newly_excluded_three_six_profiles': excluded['6+6+6'],
            'redundant_single_four_capacity_exclusions': excluded['4'],
            'prior_five_six_charge_exclusions': previous_exclusions,
            'five_six_total_excluded_profiles': 15, 'five_six_remaining_unexcluded_count': 31,
            'five_six_remaining_raw_profiles': remaining_five,
            'three_six_total_excluded_profiles': 9, 'three_six_remaining_unexcluded_count': 39,
            'three_six_remaining_raw_profiles': remaining_three,
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'local_capacity_controls': local_controls,
            'new_exclusions_by_completion_input': {'written_eight_spread': 8, 'prior_finite_seven_spread': 13},
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'exact_cover_search': False, 'DRAT_checked': False,
            'Lean_run': False, 'independent_Pro_review': False, 'manuscript_and_Zenodo_PDF_changed': False,
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-hole-capacity.md'),
            'scope': 'Written isotropic-hole capacity theorem with fixed-coordinate controls and all raw count rows checked. C7 uses the existing finite completion lemma; C8 uses written completion. No full coloring enumeration. 31five-six and39three-six rows unexcluded; sizes4..8andexactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
