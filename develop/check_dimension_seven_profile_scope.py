"""Audit count coverage and uniform necessary capacities, without a cover search."""
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capacity(sizes, even, saturated):
    first, mixed, odd = saturated
    if 6 <= odd <= 8:
        holes = 9-odd
        return holes * first + (holes-1) * mixed + sum(0 if not count else (holes if count == size else holes-1)
                                                       for count, size in zip(even, sizes)), 7 * holes
    return None


def check():
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    latest = json.loads((root / 'results/dimension-7-four-even-pairs-check.json').read_text())
    marked = json.loads((root / 'results/dimension-7-five-four-H-cover-check.json').read_text())
    assert marked['remaining_normal_forms_for_this_profile'] == ['Z', 'G']
    assert not marked['target_raw_profile_excluded'] and marked['newly_excluded_normal_form'] == 'H'
    families = (('4', (4,), None), ('5+6', (5, 6), 'five_six'),
                ('6+6+6', (6, 6, 6), 'three_six'))
    counts = {}
    distributions = {}
    capacities = []
    raw_capacity_failures = {}
    for name, sizes, prefix in families:
        defect_count = len(sizes)
        assert sum(7-size for size in sizes) == 3
        domains = [range(size+1) if size != 6 else (0, 2, 4, 5, 6) for size in sizes]
        direct = set()
        formulas = set()
        for even in product(*domains):
            if name == '6+6+6' and tuple(sorted(even)) != even:
                continue
            total_even = sum(even)
            total_odd = sum(sizes) - total_even
            for first in range(19):
                for mixed in range(19):
                    odd = 18 - defect_count - first - mixed
                    if odd >= 0 and 7*first+6*mixed+total_even == 63 and mixed+7*odd+total_odd+4 == 64:
                        direct.add(even + (first, mixed, odd))
            for parameter in range(-18, 19):
                saturated = (9-total_even-6*parameter, total_even+7*parameter, 9-defect_count-parameter)
                if min(saturated) >= 0:
                    formulas.add(even + saturated)
        assert direct == formulas
        stored = raw['count_profiles'][name]
        identities = [tuple(row['defect_even_counts'] + row['saturated_counts']) for row in stored]
        assert len(set(identities)) == len(identities) and set(identities) == direct
        assert len(direct) == {'4': 9, '5+6': 46, '6+6+6': 48}[name]
        for row in stored:
            even = row['defect_even_counts']
            saturated = row['saturated_counts']
            assert row['defect_sizes'] == list(sizes)
            odd_counts = [size-count for size, count in zip(sizes, even)]
            assert row['defect_odd_counts'] == odd_counts
            taus = [(comb(size, 2)+comb(odd, 2)) % 2 for size, odd in zip(sizes, odd_counts)]
            assert row['defect_quadratic_taus'] == taus
            assert row['required_sum_of_pairwise_charge_products'] == (sum(saturated[:2])+sum(taus)) % 2
        raw_capacity_failures[name] = sum(bound is not None and bound[0] < bound[1]
                                         for row in stored for bound in [capacity(sizes, row['defect_even_counts'], row['saturated_counts'])])
        counts[name] = len(direct)
        if prefix is None:
            continue
        remaining = latest[prefix+'_remaining_raw_profiles']
        assert len({tuple(row) for row in remaining}) == len(remaining)
        assert all(tuple(row) in direct for row in remaining)
        expected_count, excluded = (27, 19) if prefix == 'five_six' else (39, 9)
        assert len(remaining) == latest[prefix+'_remaining_unexcluded_count'] == marked[prefix+'_remaining_unexcluded_count'] == expected_count
        assert len(direct)-len(remaining) == latest[prefix+'_total_excluded_profiles'] == marked[prefix+'_total_excluded_profiles'] == excluded
        distributions[name] = dict(sorted(Counter(row[-1] for row in remaining).items()))
        for row in remaining:
            bound = capacity(sizes, row[:defect_count], row[defect_count:])
            if bound is not None:
                assert bound[0] >= bound[1]
                capacities.append({'family': name, 'profile': row, 'upper_capacity': bound[0], 'required_holes': bound[1]})
    assert distributions == {'5+6': {6: 6, 7: 19, 8: 2}, '6+6+6': {5: 2, 6: 14, 7: 18, 8: 5}}
    assert len(capacities) == 64
    dependencies = ('notes/dimension-seven-size-four.md', 'results/dimension-7-size-four.json',
                    'notes/dimension-seven-two-six-profiles.md', 'notes/dimension-seven-nineteen-obstruction.md',
                    'notes/dimension-seven-seven-holes.md', 'results/dimension-7-seven-holes.json',
                    'notes/dimension-seven-six-holes.md', 'results/dimension-7-six-holes.json',
                    'results/dimension-7-four-even-pairs-check.json',
                    'results/dimension-7-five-four-H-cover-check.json')
    return {'status': 'uniform_count_and_capacity_scope_audited_no_new_exclusion',
            'characteristic_size_of_66_count_candidates': 4,
            'written_deficit_formula': 'sum(7-k_i)=s-1',
            'written_count_formulas': ['B=m+7t', 'A=9-m-6t', 'C=9-r-t'],
            'original_raw_profile_counts': counts, 'raw_profiles_failing_applicable_hole_capacity': raw_capacity_failures,
            'remaining_raw_profiles': {'five_six': 27, 'three_six': 39},
            'remaining_counts_by_pure_odd_heptads': distributions,
            'applicable_remaining_capacity_controls': capacities,
            'remaining_C6_through_C8_count': 64, 'remaining_C5_count': 2,
            'new_raw_profile_exclusions': 0, 'remaining_normal_forms_of_five_four_profile': ['Z', 'G'],
            'characteristic_sizes_still_open': [4, 5, 6, 7, 8], 'all_nineteen_color_branches_excluded': False,
            'line_lower_bound': 19, 'full_subspace_lower_bound': 19, 'exact_n7': 'open',
            'uniform_exclusion_of_remaining_family_established': False, 'completion_time_estimate': None,
            'written_generalization_of_existing_bookkeeping': True,
            'finite_scope': 'Count rows and existing-report metadata only; no graph or coloring enumeration.',
            'new_cover_search': False, 'new_cover_certificate': False, 'new_Lean': False,
            'new_Pro_review': False, 'stopping_point_decided': False,
            'checker_sha256': digest(Path(__file__)), 'note_sha256': digest(root / 'notes/dimension-seven-profile-scope.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')
