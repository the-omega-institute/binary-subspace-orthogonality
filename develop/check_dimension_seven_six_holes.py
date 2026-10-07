"""Check six-Lagrangian completion and exclude characteristic size three in nineteen colorings."""
from collections import Counter
from itertools import combinations, product
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


def span(basis):
    output = {0}
    for vector in basis:
        output |= {point ^ vector for point in output}
    return output


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def digest(rows):
    return hashlib.sha256(json.dumps(sorted(rows), separators=(',', ':')).encode()).hexdigest()


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    planes = sorted({tuple(sorted(span((left, middle, right)) - {0}))
                     for left, middle, right in combinations(points, 3)
                     if left ^ middle ^ right and not any((dot(left, middle), dot(left, right), dot(middle, right)))})
    assert len(planes) == 135 and all(len(plane) == 7 for plane in planes)
    symplectic_basis = (3, 12, 48, 65, 71, 95)
    coordinate_planes = []
    subspaces = 0
    for pivots in combinations(range(6), 3):
        free = [(row, column) for row, pivot in enumerate(pivots) for column in range(pivot + 1, 6) if column not in pivots]
        for bits in product((0, 1), repeat=len(free)):
            rows = [1 << pivot for pivot in pivots]
            for (row, column), bit in zip(free, bits):
                rows[row] |= bit << column
            lifted = [vector_sum(symplectic_basis[index] for index in range(6) if row & (1 << index)) for row in rows]
            subspaces += 1
            if all(dot(left, right) == 0 for left, right in combinations(lifted, 2)):
                coordinate_planes.append(tuple(sorted(span(lifted) - {0})))
    assert subspaces == 1395 and sorted(coordinate_planes) == planes
    fixed = planes.index((3, 12, 15, 48, 51, 60, 63))
    masks = [mask(plane) for plane in planes]
    universe = mask(points)
    neighbors = {index: sum(1 << other for other in range(index + 1, len(planes)) if not masks[index] & masks[other]) for index in range(len(planes))}
    candidates = sum(1 << index for index in range(len(planes)) if not masks[index] & masks[fixed])
    bit_partials = []

    def bit_visit(chosen, available):
        if len(chosen) == 6:
            bit_partials.append(tuple(sorted(chosen)))
            return
        if available.bit_count() < 6 - len(chosen):
            return
        while available:
            first = available & -available
            index = first.bit_length() - 1
            available ^= first
            bit_visit(chosen + (index,), available & neighbors[index])

    bit_visit((fixed,), candidates)
    array_partials = []
    point_sets = [set(plane) for plane in planes]

    def array_visit(chosen, available):
        if len(chosen) == 6:
            array_partials.append(tuple(sorted(chosen)))
            return
        if len(available) < 6 - len(chosen):
            return
        for position, index in enumerate(available):
            array_visit(chosen + (index,), [other for other in available[position + 1:] if not point_sets[index] & point_sets[other]])

    array_visit((fixed,), [index for index in range(len(planes)) if not point_sets[index] & point_sets[fixed]])
    assert len(bit_partials) == len(set(bit_partials)) == 3584
    assert sorted(array_partials) == sorted(bit_partials)
    completion_histogram = Counter()
    hyperplane_histogram = Counter()
    completion_rows = []
    near_complete_hole_planes = 0
    for partial in sorted(bit_partials):
        covered = 0
        for index in partial:
            assert not covered & masks[index]
            covered |= masks[index]
        holes = universe ^ covered
        assert holes.bit_count() == 21
        completion = tuple(index for index, plane in enumerate(masks) if plane & holes == plane)
        assert len(completion) == 3
        assert all(not masks[left] & masks[right] for left, right in combinations(completion, 2))
        assert masks[completion[0]] | masks[completion[1]] | masks[completion[2]] == holes
        completion_histogram[len(completion)] += 1
        completion_rows.append((partial, completion))
        near_complete_hole_planes += sum((plane & holes).bit_count() == 6 for plane in masks)
        assert not any((plane & holes).bit_count() == 6 for plane in masks)
        for point in points:
            count = sum(dot(point, other) == 0 for other in points if holes & (1 << other))
            assert count == (13 if holes & (1 << point) else 9)
            hyperplane_histogram[count] += 1
    first_partial, first_completion = completion_rows[0]
    local_holes = sorted(point for index in first_completion for point in planes[index])
    six_controls = []
    for index in first_completion:
        for missing in planes[index]:
            chosen = tuple(point for point in planes[index] if point != missing)
            source = tuple(127 ^ point for point in chosen)
            companion = 127 ^ missing
            assert vector_sum(chosen) == missing
            assert companion not in source and all(dot(point, companion) == 1 for point in source)
            assert all(dot(left, right) == 1 for left, right in combinations(source + (companion,), 2))
            assert missing in local_holes
            six_controls.append({'projections': list(chosen), 'completion': missing})
    assert len(six_controls) == 21
    characteristic_transfers = 0
    mixed_transfers = 0
    other_defect_transfers = 0
    for control in six_controls:
        missing = control['completion']
        odd_projections = set(control['projections'])
        source = tuple(127 ^ point for point in sorted(odd_projections))
        companion = 127 ^ missing
        completed = source + (companion,)
        for other in local_holes:
            if other == missing or other in odd_projections or dot(missing, other):
                continue
            characteristic = (127, companion, 127 ^ other)
            assert all(dot(left, right) == 1 for left, right in combinations(characteristic, 2))
            reduced = (127, 127 ^ other)
            assert not set(completed) & set(reduced) and dot(*reduced) == 1
            characteristic_transfers += 1
        even_candidates = [point for point in points if dot(point, missing)]
        mixed_sixes = []

        def even_visit(chosen, available):
            if len(chosen) == 6:
                mixed_sixes.append(chosen)
                return
            for position, point in enumerate(available):
                even_visit(chosen + (point,), [other for other in available[position + 1:] if dot(point, other)])

        even_visit((), even_candidates)
        assert len(mixed_sixes) == 32
        for block in mixed_sixes:
            assert vector_sum(block) == missing
            assert all(dot(left, right) == 1 for left, right in combinations(block + (companion,), 2))
            assert not set(block) & set(completed)
            mixed_transfers += 1
        available_odd = sorted(set(local_holes) - odd_projections - {missing})
        for other_three in combinations(available_odd, 3):
            projections = (missing,) + other_three
            if any(dot(left, right) for left, right in combinations(projections, 2)):
                continue
            compatible = [point for point in points if all(dot(point, projection) for projection in projections)]
            for even_pair in combinations(compatible, 2):
                if not dot(*even_pair):
                    continue
                block = even_pair + tuple(127 ^ point for point in projections)
                reduced = tuple(point for point in block if point != companion)
                assert len(reduced) == 5 and not set(reduced) & set(completed)
                assert all(dot(left, right) == 1 for left, right in combinations(block, 2))
                assert all(dot(left, right) == 1 for left, right in combinations(reduced, 2))
                other_defect_transfers += 1
    assert characteristic_transfers == 126 and mixed_transfers == 672
    assert other_defect_transfers == 288
    transfer_targets = [
        {'source_profile': [0, 0, 3, 7, 6], 'source_class': 'characteristic', 'target_characteristic_size': 2, 'excluded_by': 'characteristic_size_at_least_three'},
        {'source_profile': [0, 0, 3, 7, 6], 'source_class': 'mixed', 'target_two_six_profile': [0, 6, 3, 6, 7], 'excluded_by': 'previous_C7_two_six_exclusion'},
        {'source_profile': [0, 2, 1, 9, 6], 'source_class': 'characteristic', 'target_characteristic_size': 2, 'excluded_by': 'characteristic_size_at_least_three'},
        {'source_profile': [0, 2, 1, 9, 6], 'source_class': 'mixed', 'target_two_six_profile': [2, 6, 1, 8, 7], 'excluded_by': 'previous_C7_two_six_exclusion'},
        {'source_profile': [0, 2, 1, 9, 6], 'source_class': 'other_defect', 'target_one_five_profile': [2, 3, 1, 9, 7], 'excluded_by': 'previous_entire_one_five_exclusion'}
    ]
    prior_names = ('dimension-7-characteristic-three.json', 'dimension-7-one-five-exclusion.json',
                   'dimension-7-two-six-profiles.json', 'dimension-7-four-four-hole-cover.json')
    prior_bindings = {name: hashlib.sha256((root / 'results' / name).read_bytes()).hexdigest() for name in prior_names}
    prior = {name: json.loads((root / 'results' / name).read_text()) for name in prior_names}
    assert prior[prior_names[0]]['characteristic_class_size_range'] == [3, 8]
    assert prior[prior_names[1]]['one_five_branch_excluded']
    assert prior[prior_names[3]]['remaining_two_six_profiles'] == [[0, 0, 3, 7, 6], [0, 2, 1, 9, 6]]
    for name in prior_names:
        value = prior[name]
        source_key = 'auditor_sha256' if name == prior_names[3] else 'checker_sha256'
        source = {'dimension-7-characteristic-three.json': 'check_dimension_seven_characteristic_three.py',
                  'dimension-7-one-five-exclusion.json': 'check_dimension_seven_one_five_exclusion.py',
                  'dimension-7-two-six-profiles.json': 'check_dimension_seven_two_six_profiles.py',
                  'dimension-7-four-four-hole-cover.json': 'check_four_four_hole_cover.py'}[name]
        note = {'dimension-7-characteristic-three.json': 'dimension-seven-characteristic-three.md',
                'dimension-7-one-five-exclusion.json': 'dimension-seven-one-five-exclusion.md',
                'dimension-7-two-six-profiles.json': 'dimension-seven-two-six-profiles.md',
                'dimension-7-four-four-hole-cover.json': 'dimension-seven-four-four-hole-cover.md'}[name]
        assert value[source_key] == hashlib.sha256((root / 'develop' / source).read_bytes()).hexdigest()
        assert value['proof_note_sha256'] == hashlib.sha256((root / 'notes' / note).read_bytes()).hexdigest()
    c7 = prior[prior_names[2]]['count_profiles']
    for target in transfer_targets:
        if 'target_two_six_profile' in target:
            profile = target['target_two_six_profile']
            assert any(item['defect_even_counts'] + item['saturated_counts'] == profile and item['status'].startswith('excluded_') for item in c7)
    return {'status': 'six_lagrangians_complete_uniquely_and_characteristic_size_three_excluded',
            'dimension': 7, 'characteristic_class_size_range': [4, 8],
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'size_three_entire_branch_excluded': True, 'one_five_branch_excluded': True, 'two_six_branch': 'excluded',
            'remaining_two_six_profiles': [], 'excluded_final_two_six_profiles': [[0, 0, 3, 7, 6], [0, 2, 1, 9, 6]],
            'lagrangians': len(planes), 'rref_three_subspaces': subspaces, 'independent_lagrangian_sets_equal': True,
            'anchored_six_partial_spreads': len(bit_partials), 'independent_six_partial_spread_sets_equal': True,
            'fixed_lagrangian': list(planes[fixed]), 'hole_points_per_partial_spread': 21,
            'hole_lagrangians_per_partial_spread': 3, 'completion_unique': True,
            'completion_histogram': dict(sorted(completion_histogram.items())),
            'lagrangian_set_sha256': digest(planes), 'rref_lagrangian_set_sha256': digest(coordinate_planes),
            'bitmask_partial_spread_set_sha256': digest(bit_partials), 'array_partial_spread_set_sha256': digest(array_partials),
            'completion_set_sha256': digest(completion_rows),
            'near_complete_six_point_hole_lagrangians': near_complete_hole_planes,
            'hyperplane_hole_counts_checked': sum(hyperplane_histogram.values()),
            'hyperplane_hole_count_histogram': dict(sorted(hyperplane_histogram.items())),
            'pure_odd_six_local_controls': six_controls, 'pure_odd_six_completion_controls_checked': len(six_controls),
            'characteristic_size_two_local_transfer_controls': characteristic_transfers,
            'mixed_to_pure_even_six_local_transfer_controls': mixed_transfers,
            'other_six_to_five_local_transfer_controls': other_defect_transfers,
            'transfer_targets': transfer_targets,
            'seven_or_nine_partial_spread_enumeration_rerun': False, 'all_six_point_classes_reenumerated': False,
            'new_exact_cover_search': False, 'native_SAT': False, 'DRAT_checked': False,
            'Lean_run': False, 'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'prior_report_sha256': prior_bindings, 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-six-holes.md').read_bytes()).hexdigest(),
            'scope': 'Finite universal six-Lagrangian unique completion after a written fixed-member symplectic reduction, checked by independent original-vector/RREF catalogs and bitmask/array six-spread enumerations. Written span/intersection and conditional recoloring arguments exclude both remaining C6profiles and the entire characteristic-size-three branch. Earlier finite C8cover and other prior dependencies retained. Sizes4through8 and exactn7 remain open; lowerbound19 unchanged.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
