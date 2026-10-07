"""Check seven-Lagrangian completion and the remaining one-five defect forms."""
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
    values = {0}
    for vector in basis:
        values |= {point ^ vector for point in values}
    return values


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
        free = [(row, column) for row, pivot in enumerate(pivots)
                for column in range(pivot + 1, 6) if column not in pivots]
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
    neighbors = {index: sum(1 << other for other in range(index + 1, len(planes)) if not masks[index] & masks[other])
                 for index in range(len(planes))}
    candidates = sum(1 << index for index in range(len(planes)) if not masks[index] & masks[fixed])
    partials = []

    def enumerate_seven(chosen, available):
        if len(chosen) == 7:
            partials.append(tuple(sorted(chosen)))
            return
        if available.bit_count() < 7 - len(chosen):
            return
        while available:
            first = available & -available
            index = first.bit_length() - 1
            available ^= first
            enumerate_seven(chosen + (index,), available & neighbors[index])

    enumerate_seven((fixed,), candidates)
    assert len(partials) == len(set(partials)) == 1792
    indexed = {point: [index for index, plane in enumerate(planes) if point in plane] for point in points}
    complete = []

    def enumerate_nine(chosen, remaining):
        if not remaining:
            assert len(chosen) == 9
            complete.append(tuple(sorted(chosen)))
            return
        point = (remaining & -remaining).bit_length() - 1
        for index in indexed[point]:
            if masks[index] & remaining == masks[index]:
                enumerate_nine(chosen + (index,), remaining ^ masks[index])

    enumerate_nine((fixed,), universe ^ masks[fixed])
    assert len(complete) == len(set(complete)) == 64
    deletion_counts = Counter()
    for spread in complete:
        for omitted in combinations([index for index in spread if index != fixed], 2):
            deletion_counts[tuple(index for index in spread if index not in omitted)] += 1
    assert set(partials) == set(deletion_counts)
    assert set(deletion_counts.values()) == {1}
    intersections = Counter()
    hyperplanes_checked = 0
    for partial in partials:
        covered = 0
        for index in partial:
            assert not covered & masks[index]
            covered |= masks[index]
        holes = universe ^ covered
        assert holes.bit_count() == 14
        completions = [index for index, plane in enumerate(masks) if plane & holes == plane]
        assert len(completions) == 2
        first, second = completions
        assert not masks[first] & masks[second] and masks[first] | masks[second] == holes
        for point in points:
            count = sum(dot(point, other) == 0 for other in points if holes & (1 << other))
            assert count == (10 if holes & (1 << point) else 6)
            intersections[count] += 1
            hyperplanes_checked += 1
    mixed_isotropic_counts = Counter()
    five_point_controls = 0
    four_point_controls = 0
    transverse_pairs = 0
    for first, second in combinations(planes, 2):
        if set(first) & set(second):
            continue
        transverse_pairs += 1
        hole_points = sorted(first + second)
        for size in (4, 5):
            for chosen in combinations(hole_points, size):
                if any(dot(left, right) for left, right in combinations(chosen, 2)):
                    continue
                first_count = len(set(chosen) & set(first))
                if first_count and first_count < size:
                    assert size == 4 and first_count in (1, 3)
                    triple = [point for point in chosen if point in (first if first_count == 3 else second)]
                    assert vector_sum(triple) == 0
                    mixed_isotropic_counts[size] += 1
                    continue
                if size == 5:
                    assert vector_sum(chosen) != 0
                    five_point_controls += 1
                else:
                    four_point_controls += 1
    assert transverse_pairs == 4320
    first = (3, 12, 15, 48, 51, 60, 63)
    second = (6, 24, 30, 65, 71, 89, 95)
    local_cases = []
    for even_first, even_second in ((65, 71), (3, 71)):
        even_defect = even_first ^ even_second
        odd_defect = [point for point in first if dot(even_defect, point)]
        characteristic = (127, 127 ^ even_first, 127 ^ even_second)
        defect = (even_defect, *(127 ^ point for point in odd_defect))
        assert len(odd_defect) == 4 and vector_sum(odd_defect) == 0
        assert not set(characteristic) & set(defect)
        assert all(dot(left, right) == 1 for left, right in combinations(characteristic, 2))
        assert all(dot(left, right) == 1 for left, right in combinations(defect, 2))
        assert vector_sum(point ^ (127 if dot(point, 127) else 0) for point in defect) == even_defect
        remaining_odd = sorted(set(first + second) - {even_first, even_second} - set(odd_defect))
        assert len(remaining_odd) == 8
        local_cases.append({'characteristic_projections': [even_first, even_second], 'even_defect': even_defect,
                            'odd_defect_projections': odd_defect, 'remaining_mixed_odd_projections': remaining_odd,
                            'characteristic_class': list(characteristic), 'defect_class': list(defect),
                            'complete_coloring': False})
    expected_local = set()
    for even_first, even_second in combinations(sorted(first + second), 2):
        if dot(even_first, even_second):
            continue
        even_defect = even_first ^ even_second
        odd_defect = tuple(point for point in first if dot(even_defect, point))
        if len(odd_defect) == 4 and not {even_first, even_second} & set(odd_defect):
            expected_local.add(((even_first, even_second), even_defect, odd_defect))
    local_orbits = [set(), set()]
    basis_checks = 0
    linear_changes = 0
    original_basis = symplectic_basis + (127,)
    for basis in product(first, repeat=3):
        if len(span(basis)) != 8:
            continue
        dual = tuple(next(point for point in second if all(dot(basis[row], point) == int(row == column)
                                                          for row in range(3))) for column in range(3))
        image_basis = basis + dual + (127,)
        assert len(span(image_basis)) == 128
        assert all(dot(original_basis[left], original_basis[right]) == dot(image_basis[left], image_basis[right])
                   for left in range(7) for right in range(7))
        mapping = {vector_sum(original_basis[index] for index in range(7) if bits & (1 << index)):
                   vector_sum(image_basis[index] for index in range(7) if bits & (1 << index)) for bits in range(128)}
        assert len(mapping) == len(set(mapping.values())) == 128
        for index, case in enumerate(local_cases):
            local_orbits[index].add((tuple(sorted(mapping[point] for point in case['characteristic_projections'])),
                                     mapping[case['even_defect']],
                                     tuple(sorted(mapping[point] for point in case['odd_defect_projections']))))
        linear_changes += 1
        basis_checks += 49
    assert linear_changes == 168 and [len(orbit) for orbit in local_orbits] == [21, 21]
    assert not local_orbits[0] & local_orbits[1]
    assert local_orbits[0] | local_orbits[1] == expected_local
    return {
        'status': 'seven_lagrangians_complete_uniquely_and_pure_odd_five_defect_profile_excluded',
        'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
        'exact_n7_chromatic_number': 'open', 'nineteen_color_witness': False, 'new_numerical_lower_bound': False,
        'excluded_profile': [0, 5, 3, 7, 7], 'remaining_one_five_profiles': [[1, 4, 2, 8, 7]],
        'two_six_branch': 'open_not_enumerated', 'characteristic_class_size_range': [3, 8],
        'lagrangians': len(planes), 'rref_three_subspaces': subspaces,
        'independent_lagrangian_sets_equal': True, 'fixed_lagrangian': list(planes[fixed]),
        'anchored_seven_partial_spreads': len(partials), 'anchored_nine_complete_spreads': len(complete),
        'all_anchored_seven_partial_spreads_enumerated': True, 'deletion_set_equals_partial_spread_set': True,
        'completion_multiplicity': 1, 'hole_lagrangians_per_partial_spread': 2,
        'lagrangian_set_sha256': digest(planes), 'rref_lagrangian_set_sha256': digest(coordinate_planes),
        'partial_spread_set_sha256': digest(partials), 'deletion_set_sha256': digest(deletion_counts),
        'complete_spread_set_sha256': digest(complete),
        'hyperplane_hole_counts_checked': hyperplanes_checked, 'hyperplane_hole_count_histogram': dict(sorted(intersections.items())),
        'transverse_lagrangian_pairs': transverse_pairs, 'five_point_single_side_isotropic_controls': five_point_controls,
        'four_point_single_side_isotropic_controls': four_point_controls,
        'four_point_mixed_side_isotropic_controls': mixed_isotropic_counts[4],
        'five_point_mixed_side_isotropic_controls': mixed_isotropic_counts[5],
        'remaining_profile_local_forms': local_cases,
        'fixed_hole_pair_local_configurations': len(expected_local), 'local_form_orbit_sizes': [len(orbit) for orbit in local_orbits],
        'hole_pair_basis_changes_checked': linear_changes, 'original_dot_basis_pairings_checked': basis_checks,
        'remaining_profile_realizability': 'open_both_local_forms_no_common_coloring_constructed',
        'completion_proof_scope': 'All seven-member partial spreads containing a fixed Lagrangian enumerated; independently generated full-spread deletion set agrees exactly. Written symplectic transitivity covers every seven-member partial spread.',
        'coloring_exclusion_scope': 'Written five-odd-defect exclusion uses the finitely proved completion lemma. Local remaining-profile controls are individual classes, not complete colorings.',
        'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
        'submitted_manuscript_changed': False,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-seven-holes.md').read_bytes()).hexdigest(),
        'prior_hole_cover_report_sha256': hashlib.sha256((root / 'results/dimension-7-hole-cover-check.json').read_bytes()).hexdigest(),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
