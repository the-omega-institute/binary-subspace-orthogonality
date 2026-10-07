"""Check the seven-clique label budget excluding the final one-five profile."""
from collections import Counter
from itertools import combinations
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


def maximum_matching(lists):
    reachable = {frozenset()}
    for available in lists:
        updated = set(reachable)
        for used in reachable:
            for label in available - used:
                updated.add(used | {label})
        reachable = updated
    return max(map(len, reachable))


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    prior_path = root / 'results/dimension-7-seven-holes.json'
    prior_bytes = prior_path.read_bytes()
    assert hashlib.sha256(prior_bytes).hexdigest() == '6fae4b1d6d60a27f4049a40210981661af36163d98b1980d33345abe63fea0a0'
    prior = json.loads(prior_bytes)
    assert prior['anchored_seven_partial_spreads'] == 1792 and prior['anchored_nine_complete_spreads'] == 64
    assert prior['deletion_set_equals_partial_spread_set'] and prior['completion_multiplicity'] == 1
    assert prior['checker_sha256'] == hashlib.sha256((root / 'develop/check_dimension_seven_seven_holes.py').read_bytes()).hexdigest()
    assert prior['proof_note_sha256'] == hashlib.sha256((root / 'notes/dimension-seven-seven-holes.md').read_bytes()).hexdigest()
    first = (3, 12, 15, 48, 51, 60, 63)
    second = (6, 24, 30, 65, 71, 89, 95)
    assert not set(first) & set(second)
    assert all(dot(left, right) == 0 for left, right in combinations(first, 2))
    assert all(dot(left, right) == 0 for left, right in combinations(second, 2))
    function_weights = Counter(sum(dot(functional, point) for point in range(1, 8)) for functional in range(8))
    assert function_weights == {0: 1, 4: 7}
    all_cases = []
    for even_first, even_second in combinations(sorted(first + second), 2):
        if dot(even_first, even_second):
            continue
        even_defect = even_first ^ even_second
        odd_defect = tuple(point for point in first if dot(even_defect, point))
        if len(odd_defect) != 4 or {even_first, even_second} & set(odd_defect):
            continue
        characteristic = (127, 127 ^ even_first, 127 ^ even_second)
        defect = (even_defect, *(127 ^ point for point in odd_defect))
        assert vector_sum(odd_defect) == 0 and not set(characteristic) & set(defect)
        assert all(dot(left, right) == 1 for left, right in combinations(characteristic, 2))
        assert all(dot(left, right) == 1 for left, right in combinations(defect, 2))
        mixed = sorted(set(first + second) - {even_first, even_second} - set(odd_defect))
        assert len(mixed) == 8
        mixed_first = sorted(set(mixed) & set(first))
        assert len(mixed_first) <= 3
        lists = []
        defect_allowed = []
        for point in second:
            assert any(dot(point, member) == 0 for member in characteristic if member != point)
            available = {'pure_even_0', 'pure_even_1'}
            for projection in mixed:
                if dot(point, 127 ^ projection):
                    available.add(f'mixed_{projection}')
                elif projection in second:
                    assert dot(point, projection) == 0
            if all(dot(point, member) == 1 for member in defect if member != point):
                available.add('defect')
                defect_allowed.append(point)
            assert not any(f'mixed_{projection}' in available for projection in set(mixed) & set(second))
            lists.append(available)
        union = set().union(*lists)
        assert union <= {'pure_even_0', 'pure_even_1', 'defect'} | {f'mixed_{projection}' for projection in mixed_first}
        assert len(union) <= 2 + 3 + 1 < 7
        matched = maximum_matching(lists)
        assert matched == len(union) and matched in (4, 6)
        all_cases.append({'characteristic_projections': [even_first, even_second], 'even_defect': even_defect,
                          'odd_defect_projections': list(odd_defect), 'mixed_odd_projections_in_first_hole': mixed_first,
                          'defect_label_available_at': defect_allowed, 'clique': list(second),
                          'necessary_lists': {point: sorted(available) for point, available in zip(second, lists)},
                          'label_union': sorted(union), 'available_label_union_size': len(union),
                          'maximum_shadow_matching': matched, 'seven_distinct_labels_possible': False})
    assert len(all_cases) == 42
    histogram = Counter(case['available_label_union_size'] for case in all_cases)
    assert histogram == {4: 21, 6: 21}
    canonical = []
    for pair in ((65, 71), (3, 71)):
        canonical.append(next(case for case in all_cases if case['characteristic_projections'] == list(pair)))
    for old, new in zip(prior['remaining_profile_local_forms'], canonical):
        assert old['characteristic_projections'] == new['characteristic_projections']
        assert old['even_defect'] == new['even_defect'] and old['odd_defect_projections'] == new['odd_defect_projections']
    assert canonical[0]['defect_label_available_at'] == [6] and canonical[1]['defect_label_available_at'] == []
    return {'status': 'entire_one_five_defect_branch_excluded_for_three_point_characteristic_class',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'excluded_last_profile': [1, 4, 2, 8, 7], 'remaining_one_five_profiles': [],
            'one_five_branch_excluded': True, 'size_three_entire_branch_excluded': False,
            'required_outside_defects_when_characteristic_size_three': [6, 6],
            'saturated_outside_classes_when_characteristic_size_three': 16,
            'two_six_branch': 'open_coupled_realizability_not_enumerated', 'characteristic_class_size_range': [3, 8],
            'uniform_clique_size': 7, 'uniform_label_upper_bound': 6,
            'linear_functional_weight_histogram': dict(sorted(function_weights.items())),
            'fixed_hole_pair_local_configurations_checked': len(all_cases),
            'local_label_union_histogram': dict(sorted(histogram.items())), 'canonical_shadow_controls': canonical,
            'prior_completion_enumeration_reused': True, 'prior_completion_enumeration_rerun': False,
            'complete_colorings_enumerated': False, 'native_SAT': False, 'exact_cover_search': False,
            'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-one-five-exclusion.md').read_bytes()).hexdigest(),
            'prior_seven_holes_report_sha256': hashlib.sha256(prior_bytes).hexdigest(),
            'prior_completed_hole_report_sha256': hashlib.sha256((root / 'results/dimension-7-hole-cover-check.json').read_bytes()).hexdigest(),
            'prior_quadratic_defects_report_sha256': hashlib.sha256((root / 'results/dimension-7-three-point-defects.json').read_bytes()).hexdigest(),
            'scope': 'Written seven-clique color budget excludes the final one-five profile using the previously finitely proved completion lemma; 42 local shadow-list controls do not enumerate complete colorings or exclude two-six defects.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
