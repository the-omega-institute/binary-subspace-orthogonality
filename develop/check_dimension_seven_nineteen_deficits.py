"""Check necessary nineteen-color class deficits and characteristic-size-two profiles."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    assert len(points) == 63
    deleted_profiles = [(even_count, mixed_count, odd_count)
                        for even_count in range(19) for mixed_count in range(19) for odd_count in range(19)
                        if even_count + mixed_count + odd_count == 18
                        and 7 * even_count + 6 * mixed_count == 63 and mixed_count + 7 * odd_count == 63]
    assert deleted_profiles == [(3, 7, 8), (9, 0, 9)]
    bounds = (7, 4, 4, 2, 2, 1, 1, 0)
    six_types = [even_count for even_count in range(7) if 6 - even_count <= bounds[even_count]]
    assert six_types == [0, 2, 4, 5, 6]
    profiles = []
    retained = []
    for defective_even in six_types:
        for even_count in range(18):
            for mixed_count in range(18):
                odd_count = 17 - even_count - mixed_count
                if odd_count < 0 or 7 * even_count + 6 * mixed_count + defective_even != 63:
                    continue
                if mixed_count + 7 * odd_count + 6 - defective_even + 2 != 64:
                    continue
                profile = {'defective_even': defective_even, 'defective_odd': 6 - defective_even,
                           'pure_even_heptads': even_count, 'mixed_saturated': mixed_count,
                           'pure_odd_heptads': odd_count}
                parameter = (mixed_count - defective_even) // 7
                assert mixed_count == defective_even + 7 * parameter
                assert even_count == 9 - defective_even - 6 * parameter and odd_count == 8 - parameter
                if even_count == 9:
                    profile['status'] = 'excluded_by_quadratic_parity'
                elif odd_count == 8 and even_count + int(defective_even == 6) < 7:
                    profile['status'] = 'excluded_by_completed_hole_clique'
                    profile['available_pure_even_labels'] = even_count + int(defective_even == 6)
                else:
                    profile['status'] = 'necessary_profile_only_realizability_open'
                    retained.append((defective_even, even_count, mixed_count, odd_count))
                profiles.append(profile)
    assert len(profiles) == 7
    assert retained == [(0, 3, 7, 7), (2, 1, 9, 7), (2, 7, 2, 8)]
    assert Counter(profile['status'] for profile in profiles) == {
        'excluded_by_quadratic_parity': 1, 'excluded_by_completed_hole_clique': 3,
        'necessary_profile_only_realizability_open': 3}
    deficit_rows = []
    for size in range(1, 9):
        outside_total = 127 - size
        deficit = 18 * 7 - outside_total
        assert deficit == size - 1 and 8 - size + deficit == 7
        defective_counts = [count for count in range(19) if count <= deficit <= 6 * count]
        assert defective_counts == ([0] if size == 1 else list(range((deficit + 5) // 6, deficit + 1)))
        deficit_rows.append({'characteristic_class_size': size, 'outside_deficit': deficit,
                             'capacity_only_defective_class_counts': defective_counts,
                             'singleton_excluded_by_deleted_graph_proof': size == 1})
    lagrangians = set()
    for left, middle, right in combinations(points, 3):
        if not any((dot(left, middle), dot(left, right), dot(middle, right))) and left ^ middle ^ right:
            space = frozenset((left, middle, right, left ^ middle, left ^ right,
                               middle ^ right, left ^ middle ^ right))
            assert len(space) == 7
            lagrangians.add(space)
    assert len(lagrangians) == 135
    heptads = []

    def extend(chosen, candidates):
        if len(chosen) == 7:
            heptads.append(frozenset(chosen))
            return
        for index, point in enumerate(candidates):
            extend(chosen + (point,), [other for other in candidates[index + 1:] if dot(point, other)])

    extend((), points)
    assert len(heptads) == 288
    intersections = Counter()
    adjacency_checks = 0
    for space in lagrangians:
        assert all(dot(left, right) == 0 for left, right in combinations(space, 2))
        for even_point in space:
            assert dot(even_point, 127) == 0
            for odd_point in space:
                assert dot(even_point, 127 ^ odd_point) == 0
                adjacency_checks += 1
        for heptad in heptads:
            intersection = len(space & heptad)
            assert intersection <= 1
            intersections[intersection] += 1
    assert adjacency_checks == 6615 and sum(intersections.values()) == 38880
    assert intersections == {0: 8640, 1: 30240}
    root = Path(__file__).parents[1]
    return {'status': 'written_deleted_line_lower_bound19_and_necessary_nineteen_color_deficit_constraints',
            'dimension': 7, 'characteristic_vector': 127,
            'deleted_line_graph_lower_bound': 19, 'line_graph_lower_bound': 19,
            'full_subspace_graph_lower_bound': 19, 'full_n7_exact_chromatic_number': 'open',
            'nineteen_color_witness': False, 'deleted_eighteen_saturation_profiles': deleted_profiles,
            'nineteen_characteristic_class_minimum': 2, 'nineteen_characteristic_class_maximum': 8,
            'deficit_identity': 'sum of 7-minus-size over eighteen non-characteristic classes equals characteristic-class-size minus one',
            'deficit_rows': deficit_rows, 'six_vertex_even_counts': six_types,
            'size_two_profiles': profiles, 'size_two_necessary_survivors': retained,
            'survivor_realizability': 'open_all_three',
            'lagrangians': 135, 'even_heptads': 288,
            'even_hole_odd_hole_adjacencies_checked': adjacency_checks,
            'heptad_lagrangian_intersections_checked': sum(intersections.values()),
            'intersection_size_histogram': dict(sorted(intersections.items())),
            'checked_UNSAT_proof': False, 'Lean_run': False, 'independent_Pro_review': False,
            'submitted_manuscript_changed': False,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-nineteen-deficits.md').read_bytes()).hexdigest(),
            'prior_obstruction_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-nineteen-obstruction.md').read_bytes()).hexdigest(),
            'prior_capacity_report_sha256': hashlib.sha256((root / 'results/dimension-7-line-capacity.json').read_bytes()).hexdigest(),
            'scope': 'Exact count-profile enumeration and coordinate incidence controls support written parity/completion proofs; no coloring enumeration, certified solver exclusion or upper bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
