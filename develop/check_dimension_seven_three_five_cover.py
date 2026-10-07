"""Independently audit the three-plus-five even cover and its written normalization controls."""
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


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit_cliques(candidates, size):
    neighbors = {point: mask(other for other in candidates if other > point and dot(point, other)) for point in candidates}
    blocks = []

    def visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            visit(chosen + (point,), available & neighbors[point])

    visit((), mask(candidates))
    return blocks


def check(certificate_path=None):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    five_candidates = [point for point in points if dot(point, 48) and dot(point, 51) and not dot(point, 95)]
    six_candidates = [point for point in points if dot(point, 60) and not dot(point, 96)]
    five = [block for block in combinations(five_candidates, 3) if vector_sum(block) == 95
            and all(dot(left, right) for left, right in combinations(block, 2))]
    six = [block for block in combinations(six_candidates, 5) if vector_sum(block) == 96
           and all(dot(left, right) for left, right in combinations(block, 2))]
    assert five == [block for block in bit_cliques(five_candidates, 3) if vector_sum(block) == 95]
    assert six == [block for block in bit_cliques(six_candidates, 5) if vector_sum(block) == 96]
    assert (len(five_candidates), len(six_candidates), len(five), len(six)) == (8, 16, 4, 6)
    array_heptads = []

    def enumerate_heptads(chosen, available):
        if len(chosen) == 7:
            array_heptads.append(chosen)
            return
        for index, point in enumerate(available):
            enumerate_heptads(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    enumerate_heptads((), points)
    all_six = bit_cliques(points, 6)
    assert len(all_six) == 2016 and len(array_heptads) == 288
    assert {block for heptad in array_heptads for block in combinations(heptad, 6)} == set(all_six)
    assert all(vector_sum(heptad) == 0 and all(dot(left, right) for left, right in combinations(heptad, 2))
               for heptad in array_heptads)
    mixed = [block for block in all_six if vector_sum(block) == 63]
    assert len(mixed) == 32
    for block in five:
        actual_class = block + (79, 76)
        assert vector_sum(block) == 95 and all(dot(left, right) for left, right in combinations(actual_class, 2))
    for block in six:
        actual_class = block + (67,)
        assert vector_sum(block) == 96 and all(dot(left, right) for left, right in combinations(actual_class, 2))
    for block in mixed:
        assert all(dot(left, right) for left, right in combinations(block + (64,), 2))
    assert all(not set(block) & holes for block in five + six + mixed)
    rows = sorted(mask(block) for block in array_heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    functionals = {tuple(dot(point, hole) for hole in sorted(holes)) for point in points}
    planes = {tuple(hole for hole, value in zip(sorted(holes), functional) if value)
              for functional in functionals if any(functional)}
    array_planes = {quad for quad in combinations(sorted(holes), 4)
                    if any(all(dot(point, odd) for odd in quad) for point in points)}
    assert len(functionals) == 8 and len(planes) == 7 and planes == array_planes
    local_controls = []
    gram_controls = 0
    source_class_controls = 0
    for plane in sorted(planes):
        characteristic = tuple(sorted(holes - set(plane)))
        assert vector_sum(characteristic) == 0
        radicals = [point for point in points if {hole for hole in holes if dot(point, hole)} == set(plane)]
        assert len(radicals) == 8
        for odd_pair in combinations(plane, 2):
            first_odd, second_odd = odd_pair
            for six_odd in sorted(set(plane) - set(odd_pair)):
                mixed_odd = next(point for point in plane if point not in set(odd_pair) | {six_odd})
                first_base = first_odd ^ second_odd
                second_base = first_odd ^ six_odd
                assert mixed_odd == first_odd ^ first_base ^ second_base
                for radical in radicals:
                    second_radical = radical ^ mixed_odd
                    assert dot(radical, mixed_odd) == 1
                    dual_first = next(point for point in points if dot(point, first_base) == 1
                                      and not dot(point, second_base) and not dot(point, first_odd)
                                      and not dot(point, radical))
                    dual_second = next(point for point in points if not dot(point, first_base)
                                       and dot(point, second_base) == 1 and not dot(point, first_odd)
                                       and not dot(point, radical) and not dot(point, dual_first))
                    source_basis = (first_base, second_base, first_odd, dual_first, dual_second, radical, 127)
                    assert all(dot(source_basis[left], source_basis[right]) == dot(target_basis[left], target_basis[right])
                               for left in range(7) for right in range(7))
                    gram_controls += 49
                    mapping = {vector_sum(source_basis[index] for index in range(7) if bits & (1 << index)):
                               vector_sum(target_basis[index] for index in range(7) if bits & (1 << index))
                               for bits in range(128)}
                    assert len(mapping) == len(set(mapping.values())) == 128 and mapping[127] == 127
                    assert {mapping[point] for point in holes} == holes
                    assert {mapping[point] for point in characteristic} == {3, 12, 15}
                    assert (mapping[first_odd], mapping[second_odd], mapping[six_odd], mapping[mixed_odd]) == (48, 51, 60, 63)
                    assert (mapping[radical], mapping[second_radical]) == (95, 96)
                    source_five = {point for point in points if dot(point, first_odd) and dot(point, second_odd) and not dot(point, radical)}
                    source_six = {point for point in points if dot(point, six_odd) and not dot(point, second_radical)}
                    assert {mapping[point] for point in source_five} == set(five_candidates)
                    assert {mapping[point] for point in source_six} == set(six_candidates)
                    inverse = {destination: source for source, destination in mapping.items()}
                    for blocks, odd_members, required_sum in ((five, (127 ^ first_odd, 127 ^ second_odd), radical),
                                                              (six, (127 ^ six_odd,), second_radical)):
                        for block in blocks:
                            source_even = tuple(inverse[point] for point in block)
                            source_class = source_even + odd_members
                            assert vector_sum(source_even) == required_sum
                            assert all(dot(left, right) for left, right in combinations(source_class, 2))
                            source_class_controls += 1
                    local_controls.append((odd_pair, six_odd, mixed_odd, characteristic, radical, second_radical))
    assert len(local_controls) == 672 and gram_controls == 32928 and source_class_controls == 6720
    universe = mask(points)
    expected_roots = []
    for first in five:
        for second in six:
            for third in mixed:
                if set(first) & set(second) or set(first) & set(third) or set(second) & set(third):
                    continue
                remaining = universe ^ mask(first + second + third)
                assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                expected_roots.append({'five_even': list(first), 'six_even': list(second),
                                       'mixed_even': list(third), 'remaining': str(remaining)})
    assert len(expected_roots) == len({row['remaining'] for row in expected_roots}) == 400
    certificate_path = certificate_path or root / 'results/dimension-7-three-five-cover-proof.json'
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'roots', 'failed_states'} and certificate['roots'] == expected_roots
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states']) == 2004
    children = {}
    branches = 0
    leaves = 0
    sizes = Counter()
    for remaining, pivot in failed.items():
        assert remaining > 0 and remaining & universe == remaining
        assert remaining.bit_count() % 7 == 0 and remaining.bit_count() <= 49
        assert pivot in points and remaining & (1 << pivot)
        successors = [remaining ^ row for row in rows if row & (1 << pivot) and row & remaining == row]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7 for successor in successors)
        children[remaining] = successors
        sizes[remaining.bit_count()] += 1
        branches += len(successors)
        leaves += not successors
    frontier = [int(row['remaining']) for row in expected_roots]
    reached = set()
    while frontier:
        state = frontier.pop()
        assert state in failed
        if state not in reached:
            reached.add(state)
            frontier.extend(children[state])
    assert reached == set(failed)
    prior = json.loads((root / 'results/dimension-7-five-six-cover.json').read_text())
    assert prior['checker_sha256'] == digest(root / 'develop/check_dimension_seven_five_six_cover.py')
    assert prior['proof_note_sha256'] == digest(root / 'notes/dimension-seven-five-six-cover.md')
    for name, expected in prior['dependency_sha256'].items():
        assert digest(root / name) == expected
    target = [3, 5, 7, 1, 8]
    assert prior['five_six_remaining_unexcluded_count'] == 29
    assert prior['five_six_remaining_raw_profiles'].count(target) == 1
    remaining = [row for row in prior['five_six_remaining_raw_profiles'] if row != target]
    assert len(remaining) == 28 and prior['three_six_remaining_unexcluded_count'] == 39
    prior_count = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    target_row = next(row for row in prior_count['count_profiles']['5+6']
                      if row['defect_even_counts'] + row['saturated_counts'] == target)
    assert target_row['required_sum_of_pairwise_charge_products'] == 0
    dependencies = ('results/dimension-7-five-six-cover.json', 'results/dimension-7-size-four.json',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'size_four_three_even_five_even_defect_profile_excluded_by_normalized_cover_certificate',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'newly_excluded_profile': target, 'profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'five_six_initial_raw_profiles': 46, 'five_six_total_excluded_profiles': 18,
            'five_six_remaining_unexcluded_count': 28, 'five_six_remaining_raw_profiles': remaining,
            'three_six_initial_raw_profiles': 48, 'three_six_total_excluded_profiles': 9,
            'three_six_remaining_unexcluded_count': 39,
            'three_six_remaining_raw_profiles': prior['three_six_remaining_raw_profiles'],
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'characteristic_charge_forced_zero': True, 'fixed_hole_affine_planes': len(planes),
            'normalization_local_controls': len(local_controls), 'normalization_Gram_entries_checked': gram_controls,
            'inverse_source_defect_class_controls': source_class_controls,
            'local_control_sha256': hashlib.sha256(json.dumps(local_controls, separators=(',', ':')).encode()).hexdigest(),
            'five_even_candidate_points': len(five_candidates), 'six_even_candidate_points': len(six_candidates),
            'five_defect_even_triples': len(five), 'six_defect_even_quintuples': len(six), 'mixed_even_sextets': len(mixed),
            'independent_array_and_bitmask_defect_catalogs_equal': True,
            'even_six_cliques': len(all_six), 'even_heptads': len(array_heptads), 'eligible_heptad_rows': len(rows),
            'eligible_ordered_roots': len(expected_roots), 'distinct_root_states': len(expected_roots),
            'failed_states_checked': len(failed), 'branches_checked': branches, 'leaf_states': leaves,
            'state_sizes': dict(sorted(sizes.items())), 'all_states_reachable': True,
            'written_eight_spread_completion_used': True, 'new_checked_finite_cover_certificate': True,
            'new_exact_cover_search': True, 'search_scope': 'Only400roots in the universally normalized specified profile; builder defaults50000states,500000visits,60seconds.',
            'prior_cover_certificate_reused_for_this_exclusion': False, 'prior_spread_enumeration_rerun': False,
            'all_small_classes_reenumerated': False, 'native_SAT': False, 'DRAT_checked': False,
            'Lean_run': False, 'independent_Pro_review': False, 'manuscript_and_Zenodo_PDF_changed': False,
            'certificate_sha256': digest(certificate_path),
            'builder_sha256': digest(root / 'develop/build_dimension_seven_three_five_cover.py'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-three-five-cover.md'),
            'scope': 'Written charge parity forces h=0 and an affine odd plane; universal symplectic normalization reduces the specified profile to400roots. Independent auditor verifies every root and every failed-state branch of the new finite certificate.28five-six/39three-six raw rows unexcluded;size4..8andexactn7open>=19. No Lean or new numerical bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.certificate)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
