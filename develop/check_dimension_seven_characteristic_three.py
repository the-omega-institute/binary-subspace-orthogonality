"""Check projected class sums and transfer pairings excluding characteristic size two."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def vector_sum(vectors):
    result = 0
    for vector in vectors:
        result ^= vector
    return result


def projection(vector):
    return vector ^ (127 if dot(vector, 127) else 0)


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    assert len(points) == 63 and vector_sum(projection(vector) for vector in range(1, 128)) == 0
    assert all(projection(vector) in points + [0] for vector in range(128))
    assert all(projection(left ^ right) == projection(left) ^ projection(right)
               for left in range(128) for right in range(128))
    lagrangians = set()
    for left, middle, right in combinations(points, 3):
        if not any((dot(left, middle), dot(left, right), dot(middle, right))) and left ^ middle ^ right:
            space = frozenset((left, middle, right, left ^ middle, left ^ right,
                               middle ^ right, left ^ middle ^ right))
            assert len(space) == 7
            lagrangians.add(space)
    assert len(lagrangians) == 135
    classes = {6: set(), 7: set()}
    even_counts = Counter()

    def extend(chosen, candidates):
        even_size = len(chosen)
        even_counts[even_size] += 1
        if even_size <= 7:
            allowed = {point for point in points if all(dot(point, member) == 1 for member in chosen)}
            for size in (6, 7):
                odd_size = size - even_size
                if odd_size < 0 or odd_size > 7:
                    continue
                if odd_size == 0:
                    classes[size].add(tuple(sorted(chosen)))
                    continue
                if odd_size == 1:
                    odd_sets = {(point,) for point in allowed}
                elif odd_size == 2:
                    odd_sets = {pair for pair in combinations(sorted(allowed), 2) if dot(*pair) == 0}
                else:
                    odd_sets = {subset for space in lagrangians for subset in combinations(sorted(space & allowed), odd_size)}
                for subset in odd_sets:
                    assert all(dot(left, right) == 0 for left, right in combinations(subset, 2))
                    classes[size].add(tuple(sorted(chosen + tuple(127 ^ point for point in subset))))
        if even_size == 7:
            return
        for index, point in enumerate(candidates):
            extend(chosen + (point,), [other for other in candidates[index + 1:] if dot(point, other)])

    extend((), points)
    assert [even_counts[size] for size in range(8)] == [1, 63, 1008, 5376, 10080, 8064, 2016, 288]
    histograms = {}
    transfer_counts = Counter()
    parity_controls = 0
    projection_checks = 0
    for size, blocks in classes.items():
        histogram = Counter()
        for block in blocks:
            assert len(block) == size and 127 not in block
            assert all(dot(left, right) == 1 for left, right in combinations(block, 2))
            odd_count = sum(dot(vector, 127) for vector in block)
            histogram[odd_count] += 1
            projected_sum = vector_sum(projection(vector) for vector in block)
            if size == 7:
                assert projected_sum == 0
                projection_checks += 1
            elif odd_count % 2 == 0:
                assert projected_sum == vector_sum(block)
                companion = 127 ^ projected_sum
                assert dot(companion, 127) == 1
                assert all(dot(vector, companion) == 1 for vector in block)
                if companion in block:
                    transfer_counts['proposed_companion_already_in_class'] += 1
                else:
                    assert companion != 127 and vector_sum(projection(vector) for vector in block + (companion,)) == 0
                    assert tuple(sorted(block + (companion,))) in classes[7]
                    transfer_counts['proper_seven_point_completion'] += 1
                transfer_counts['pairings_checked'] += 6
            else:
                assert odd_count == 1
                companion = 127 ^ projected_sum
                assert all(dot(vector, companion) == (0 if dot(vector, 127) else 1) for vector in block)
                parity_controls += 1
        histograms[size] = dict(sorted(histogram.items()))
    assert histograms[7] == {0: 288, 1: 2016, 7: 135}
    assert histograms[6] == {0: 2016, 1: 12096, 2: 30240, 4: 15120, 6: 945}
    root = Path(__file__).parents[1]
    prior = json.loads((root / 'results/dimension-7-nineteen-deficits.json').read_text())
    profiles = []
    for profile in prior['size_two_profiles']:
        row = dict(profile)
        if row['defective_odd'] % 2 == 0:
            row['current_exclusion'] = 'projected_sum_and_companion_transfer_or_disjointness_contradiction'
        else:
            assert (row['defective_even'], row['defective_odd'], row['pure_even_heptads'],
                    row['mixed_saturated'], row['pure_odd_heptads']) == (5, 1, 4, 5, 8)
            assert row['status'] == 'excluded_by_completed_hole_clique'
            row['current_exclusion'] = 'prior_completed_hole_clique_four_labels_for_seven_points'
        profiles.append(row)
    assert len(profiles) == 7 and all(row['defective_odd'] % 2 == 0 for row in profiles
                                   if row['status'] == 'necessary_profile_only_realizability_open')
    return {'status': 'written_characteristic_class_size_at_least_three_in_any_nineteen_line_coloring',
            'dimension': 7, 'characteristic_vector': 127, 'characteristic_class_size_range': [3, 8],
            'line_graph_lower_bound': 19, 'deleted_line_graph_lower_bound': 19,
            'full_subspace_graph_lower_bound': 19, 'exact_n7_chromatic_number': 'open',
            'nineteen_color_witness': False, 'new_numerical_lower_bound': False,
            'projection_linearity_pairs_checked': 16384,
            'even_independent_classes_by_size': dict(sorted(even_counts.items())),
            'lagrangians': 135, 'independent_six_classes': len(classes[6]),
            'independent_seven_classes': len(classes[7]),
            'class_counts_by_size_and_odd_count': histograms,
            'independent_class_set_sha256': {
                size: hashlib.sha256(json.dumps(sorted(blocks), separators=(',', ':')).encode()).hexdigest()
                for size, blocks in classes.items()},
            'zero_projected_seven_class_sums_checked': projection_checks,
            'transfer_controls': dict(transfer_counts), 'odd_parity_nontransfer_controls': parity_controls,
            'historical_size_two_profiles_now_all_excluded': profiles,
            'remaining_size_two_profiles': [],
            'next_size_three_defect_types': ['one five-point class', 'two six-point classes'],
            'native_SAT': False, 'checked_UNSAT_proof': False, 'Lean_run': False,
            'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-characteristic-three.md').read_bytes()).hexdigest(),
            'prior_deficit_report_sha256': hashlib.sha256((root / 'results/dimension-7-nineteen-deficits.json').read_bytes()).hexdigest(),
            'scope': 'Written projection/recoloring proof and exhaustive six/seven independent-class coordinate checks, not complete coloring enumeration or a numerical bound beyond19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
