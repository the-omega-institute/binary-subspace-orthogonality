"""Independently audit the size-four four-even-pairs cover and its written controls."""
from collections import Counter
from itertools import combinations, permutations
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
    gram = [[int(left != right) for right in range(4)] for left in range(4)]
    assert all(sum(gram[left][middle] * gram[middle][right] for middle in range(4)) % 2 == int(left == right)
               for left in range(4) for right in range(4))
    four = bit_cliques(points, 4)
    first_raw = [block for block in four if vector_sum(block) == 3]
    first = [block for block in first_raw if not any(all(dot(point, odd) for point in block) for odd in (51, 60, 63))]
    second = [block for block in bit_cliques([point for point in points if dot(point, 12) and dot(point, 48)], 4)
              if vector_sum(block) == 12]
    mixed = bit_cliques([point for point in points if dot(point, 15)], 6)
    heptads = bit_cliques(points, 7)
    assert len(four) == 10080 and len(heptads) == 288
    assert (len(first_raw), len(first), len(second), len(mixed)) == (160, 112, 16, 32)
    assert all(vector_sum(block) == 15 for block in mixed)
    assert all(vector_sum(block) == 0 for block in heptads)
    assert all(not set(block) & holes for block in first + second + mixed)
    for blocks, odd_members in ((first, (124,)), (second, (115, 79)), (mixed, (112,))):
        assert all(all(dot(left, right) for left, right in combinations(block + odd_members, 2)) for block in blocks)
    member_controls = []
    for block in four:
        total = vector_sum(block)
        assert total and all(dot(total, point) for point in block)
        if total not in holes:
            continue
        compatible = tuple(hole for hole in sorted(holes) if all(dot(point, hole) for point in block))
        perpendicular = {point for point in points if all(not dot(point, member) for member in block)}
        assert len(perpendicular) == 3 and len(perpendicular & holes) <= 1
        assert total in compatible and len(compatible) in (1, 2)
        assert all(total in odd_pair for odd_pair in combinations(compatible, 2))
        member_controls.append((block, total, compatible))
    assert len(member_controls) == 1120
    assert Counter(len(item[2]) for item in member_controls) == {1: 448, 2: 672}
    role_controls = Counter()
    for odd_first, odd_left, odd_right, odd_mixed in permutations(sorted(holes), 4):
        for first_sum in sorted(holes):
            second_sum = first_sum ^ odd_mixed
            if second_sum not in (odd_left, odd_right):
                continue
            other_second = odd_right if second_sum == odd_left else odd_left
            characteristic = holes - {odd_first, odd_left, odd_right, odd_mixed}
            assert vector_sum(characteristic) == odd_first ^ odd_left ^ odd_right ^ odd_mixed
            if first_sum in characteristic:
                role_controls['move_characteristic_to_five'] += 1
            elif first_sum == odd_first:
                assert other_second not in {first_sum, second_sum, first_sum ^ second_sum}
                assert characteristic == {other_second ^ first_sum, other_second ^ second_sum, other_second ^ first_sum ^ second_sum}
                assert vector_sum(characteristic) == other_second
                role_controls['normal_form'] += 1
            else:
                assert first_sum == other_second
                assert odd_first not in {first_sum, second_sum, first_sum ^ second_sum}
                role_controls['move_between_defects_and_exchange_sizes'] += 1
    assert sum(role_controls.values()) == 1680
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    frames = 0
    gram_controls = 0
    source_class_controls = 0
    for first_sum, second_sum, other_second in permutations(sorted(holes), 3):
        if other_second == first_sum ^ second_sum:
            continue
        half = (first_sum, second_sum, other_second)
        duals = []
        for position in range(3):
            dual = next(point for point in points if all(dot(point, half[index]) == int(index == position) for index in range(3))
                        and all(not dot(point, previous) for previous in duals))
            duals.append(dual)
        source_basis = half + tuple(duals) + (127,)
        assert all(dot(source_basis[left], source_basis[right]) == dot(target_basis[left], target_basis[right])
                   for left in range(7) for right in range(7))
        mapping = {vector_sum(source_basis[index] for index in range(7) if bits & (1 << index)):
                   vector_sum(target_basis[index] for index in range(7) if bits & (1 << index)) for bits in range(128)}
        assert len(mapping) == len(set(mapping.values())) == 128 and mapping[127] == 127
        assert {mapping[hole] for hole in holes} == holes
        characteristic = (other_second ^ first_sum, other_second ^ second_sum, other_second ^ first_sum ^ second_sum)
        assert {mapping[point] for point in characteristic} == {51, 60, 63}
        inverse = {destination: source for source, destination in mapping.items()}
        source_candidates = [point for point in points if dot(point, second_sum) and dot(point, other_second)]
        assert {mapping[point] for point in source_candidates} == {point for point in points if dot(point, 12) and dot(point, 48)}
        for blocks, odd_projections, required_sum in ((first, (first_sum,), first_sum),
                                                      (second, (second_sum, other_second), second_sum),
                                                      (mixed, (first_sum ^ second_sum,), first_sum ^ second_sum)):
            for block in blocks:
                source_even = tuple(inverse[point] for point in block)
                source_class = source_even + tuple(127 ^ odd for odd in odd_projections)
                assert vector_sum(source_even) == required_sum
                assert all(dot(left, right) for left, right in combinations(source_class, 2))
                if blocks is first:
                    assert not any(all(dot(point, odd) for point in source_even) for odd in characteristic)
                source_class_controls += 1
        frames += 1
        gram_controls += 49
    assert frames == 168 and gram_controls == 8232 and source_class_controls == 26880
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    universe = mask(points)
    expected_roots = []
    for first_block in first:
        for second_block in second:
            if set(first_block) & set(second_block):
                continue
            for mixed_block in mixed:
                if set(first_block + second_block) & set(mixed_block):
                    continue
                remaining = universe ^ mask(first_block + second_block + mixed_block)
                assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                expected_roots.append({'first': list(first_block), 'second': list(second_block),
                                       'mixed': list(mixed_block), 'remaining': str(remaining)})
    assert len(expected_roots) == 18752 and len({item['remaining'] for item in expected_roots}) == 18656
    certificate_path = certificate_path or root / 'results/dimension-7-four-even-pairs-proof.json'
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'roots', 'failed_states'} and certificate['roots'] == expected_roots
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
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
        branches += len(successors)
        leaves += not successors
        sizes[remaining.bit_count()] += 1
    frontier = [int(item['remaining']) for item in expected_roots]
    reached = set()
    while frontier:
        remaining = frontier.pop()
        assert remaining in failed
        if remaining not in reached:
            reached.add(remaining)
            frontier.extend(children[remaining])
    assert reached == set(failed)
    from check_four_four_hole_cover import check as check_prior_cover
    prior_cover = check_prior_cover(root / 'results/dimension-7-four-four-hole-cover-certificate.json')
    assert json.loads(json.dumps(prior_cover)) == json.loads((root / 'results/dimension-7-four-four-hole-cover.json').read_text())
    prior = json.loads((root / 'results/dimension-7-three-five-cover-check.json').read_text())
    assert prior['checker_sha256'] == digest(root / 'develop/check_dimension_seven_three_five_cover.py')
    assert prior['proof_note_sha256'] == digest(root / 'notes/dimension-seven-three-five-cover.md')
    for name, expected in prior['dependency_sha256'].items():
        assert digest(root / name) == expected
    target = [4, 4, 7, 1, 8]
    assert prior['five_six_remaining_unexcluded_count'] == 28 and prior['five_six_remaining_raw_profiles'].count(target) == 1
    remaining_profiles = [row for row in prior['five_six_remaining_raw_profiles'] if row != target]
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    target_row = next(row for row in raw['count_profiles']['5+6'] if row['defect_even_counts'] + row['saturated_counts'] == target)
    assert target_row['required_sum_of_pairwise_charge_products'] == 0
    dependencies = ('results/dimension-7-three-five-cover-check.json', 'results/dimension-7-size-four.json',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-nineteen-obstruction.md',
                    'notes/dimension-seven-four-four-hole-cover.md', 'develop/check_four_four_hole_cover.py',
                    'develop/build_four_four_hole_cover.py', 'results/dimension-7-four-four-hole-cover.json',
                    'results/dimension-7-four-four-hole-cover-certificate.json')
    return {'status': 'size_four_four_even_pairs_profile_excluded_by_recoloring_and_new_audited_cover',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'newly_excluded_profile': target, 'profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'five_six_initial_raw_profiles': 46, 'five_six_total_excluded_profiles': 19,
            'five_six_remaining_unexcluded_count': 27, 'five_six_remaining_raw_profiles': remaining_profiles,
            'three_six_initial_raw_profiles': 48, 'three_six_total_excluded_profiles': 9,
            'three_six_remaining_unexcluded_count': 39, 'three_six_remaining_raw_profiles': prior['three_six_remaining_raw_profiles'],
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'even_sums_forced_into_hole': True, 'six_defect_even_sum_is_an_odd_projection': True,
            'remaining_normal_form_characteristic_charge_nonzero': True,
            'four_even_cliques': len(four), 'hole_sum_member_controls': len(member_controls),
            'hole_compatible_projection_count_histogram': {'one': 448, 'two': 672},
            'odd_role_recoloring_controls': dict(sorted(role_controls.items())),
            'normalization_frames': frames, 'normalization_Gram_entries_checked': gram_controls,
            'inverse_source_class_controls': source_class_controls,
            'raw_five_defect_even_quads': len(first_raw), 'recoloring_excluded_five_quads': len(first_raw) - len(first),
            'five_defect_even_quads': len(first), 'six_defect_even_quads': len(second), 'mixed_even_sextets': len(mixed),
            'even_heptads': len(heptads), 'eligible_heptad_rows': len(rows),
            'eligible_ordered_roots': len(expected_roots), 'distinct_root_states': len(set(item['remaining'] for item in expected_roots)),
            'failed_states_checked': len(failed), 'branches_checked': branches, 'leaf_states': leaves,
            'state_sizes': dict(sorted(sizes.items())), 'all_states_reachable': True,
            'written_eight_spread_completion_used': True,
            'earlier_size_three_cover_used_by_recoloring': True, 'earlier_size_three_cover_fully_reaudited': True,
            'earlier_size_three_cover_states': prior_cover['failed_states_checked'],
            'new_checked_finite_cover_certificate': True, 'new_exact_cover_search': True,
            'search_scope': 'Only18752ordered roots of the proved remaining normal form;150000states,1000000visits,30seconds.',
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_and_Zenodo_PDF_changed': False,
            'certificate_sha256': digest(certificate_path), 'builder_sha256': digest(root / 'develop/build_dimension_seven_four_even_pairs.py'),
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-four-even-pairs.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written charge/nondegenerate-span and valid odd-point transfers reduce the specified size-four5+6profile to the earlier audited size-three two-six theorem or a new normalized cover. Both finite proof dependencies audited.27five-six/39three-sixraw rows unexcluded;size4..8andexactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.certificate)
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')
