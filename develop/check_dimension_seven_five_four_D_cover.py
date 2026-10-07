"""Independently audit all six-heptad covering roots for the five-four D normal form."""
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
    all_five = bit_cliques(points, 5)
    five = [block for block in all_five if vector_sum(block) == 63 and len(set(block) & holes) == 1]
    four = [block for block in bit_cliques([point for point in points if dot(point, 48) and dot(point, 15)], 4)
            if vector_sum(block) == 48]
    mixed_left = bit_cliques([point for point in points if dot(point, 3)], 6)
    mixed_right = bit_cliques([point for point in points if dot(point, 12)], 6)
    heptads = bit_cliques(points, 7)
    assert (len(five), len(four), len(mixed_left), len(mixed_right), len(heptads)) == (96, 16, 32, 32, 288)
    assert all(vector_sum(block) == 3 for block in mixed_left)
    assert all(vector_sum(block) == 12 for block in mixed_right)
    assert all(vector_sum(block) == 0 for block in heptads)
    assert all(not set(block) & holes for block in four + mixed_left + mixed_right)
    for blocks, odd_members in ((five, ()), (four, (79, 112)), (mixed_left, (124,)), (mixed_right, (115,))):
        assert all(all(dot(left, right) for left, right in combinations(block + odd_members, 2)) for block in blocks)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224 and all(sum(bool(row & (1 << hole)) for row in rows) == 32 for hole in holes)
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    frames = 0
    gram_controls = 0
    source_class_controls = 0
    for mixed_pair in combinations(sorted(holes), 2):
        first_mixed, second_mixed = mixed_pair
        second_odd = first_mixed ^ second_mixed
        for first_odd in sorted(holes - set(mixed_pair) - {second_odd}):
            first_sum = first_odd ^ first_mixed ^ second_mixed
            half = (first_mixed, second_mixed, first_odd)
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
            assert {mapping[point] for point in holes} == holes
            assert (mapping[first_sum], mapping[first_odd], mapping[second_odd]) == (63, 48, 15)
            characteristic = holes - set(mixed_pair) - {first_odd, second_odd}
            assert {mapping[point] for point in characteristic} == {51, 60, 63}
            assert vector_sum(characteristic) == first_odd
            source_five = [block for block in all_five if vector_sum(block) == first_sum and len(set(block) & holes) == 1]
            assert {tuple(sorted(mapping[point] for point in block)) for block in source_five} == set(five)
            source_four_candidates = {point for point in points if dot(point, first_odd) and dot(point, second_odd)}
            assert {mapping[point] for point in source_four_candidates} == {point for point in points if dot(point, 48) and dot(point, 15)}
            inverse = {destination: source for source, destination in mapping.items()}
            for blocks, odd_projections, required_sum in ((five, (), first_sum),
                                                          (four, (first_odd, second_odd), first_odd),
                                                          (mixed_left, (first_mixed,), first_mixed),
                                                          (mixed_right, (second_mixed,), second_mixed)):
                for block in blocks:
                    source_even = tuple(inverse[point] for point in block)
                    source_class = source_even + tuple(127 ^ odd for odd in odd_projections)
                    assert vector_sum(source_even) == required_sum
                    assert all(dot(left, right) for left, right in combinations(source_class, 2))
                    source_class_controls += 1
            frames += 1
            gram_controls += 49
    assert frames == 84 and gram_controls == 4116 and source_class_controls == 14784
    universe = mask(points)
    expected_roots = []
    defect_histogram = Counter()
    root_histogram = Counter()
    for first in five:
        hole = next(iter(set(first) & holes))
        assert hole != 63
        for second in four:
            if set(first) & set(second):
                continue
            defect_histogram[hole] += 1
            for left in mixed_left:
                if set(left) & set(first + second):
                    continue
                for right in mixed_right:
                    if set(right) & set(first + second + left):
                        continue
                    remaining = universe ^ mask(first + second + left + right)
                    assert remaining.bit_count() == 42 and remaining & mask(holes) == mask(holes - {hole})
                    expected_roots.append({'five': list(first), 'four': list(second), 'mixed_left': list(left),
                                           'mixed_right': list(right), 'hole': hole, 'remaining': str(remaining)})
                    root_histogram[hole] += 1
    assert defect_histogram == {3: 128, 12: 128, 15: 144, 48: 128, 51: 128, 60: 128}
    assert root_histogram == {3: 8960, 12: 8960, 15: 14080, 48: 13056, 51: 8960, 60: 8960}
    assert len(expected_roots) == 62976 and len({row['remaining'] for row in expected_roots}) == 54448
    certificate_path = certificate_path or root / 'results/dimension-7-five-four-D-cover-proof.json'
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
        assert remaining.bit_count() % 7 == 0 and remaining.bit_count() <= 42
        assert (remaining & mask(holes)).bit_count() == remaining.bit_count() // 7
        assert pivot in points and remaining & (1 << pivot)
        successors = [remaining ^ row for row in rows if row & (1 << pivot) and row & remaining == row]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7 for successor in successors)
        children[remaining] = successors
        branches += len(successors)
        leaves += not successors
        sizes[remaining.bit_count()] += 1
    frontier = [int(row['remaining']) for row in expected_roots]
    reached = set()
    while frontier:
        remaining = frontier.pop()
        assert remaining in failed
        if remaining not in reached:
            reached.add(remaining)
            frontier.extend(children[remaining])
    assert reached == set(failed)
    from check_dimension_seven_five_four_charge import check as check_prior_normal_forms
    prior = check_prior_normal_forms()
    assert json.loads(json.dumps(prior)) == json.loads((root / 'results/dimension-7-five-four-charge.json').read_text())
    target = next(row for row in prior['normal_forms'] if row['case'] == 'D')
    assert target['disjoint_defect_pairs'] == 784 and not prior['target_profile_excluded']
    dependencies = ('notes/dimension-seven-five-four-charge.md', 'develop/check_dimension_seven_five_four_charge.py',
                    'results/dimension-7-five-four-charge.json', 'notes/dimension-seven-two-six-profiles.md',
                    'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'five_four_D_normal_form_excluded_by_new_audited_six_heptad_cover',
            'dimension': 7, 'profile': [5, 4, 6, 2, 8], 'newly_excluded_normal_form': 'D',
            'remaining_normal_forms_for_this_profile': ['Z', 'H', 'G'], 'target_raw_profile_excluded': False,
            'target_raw_profile_realized': False, 'five_six_total_excluded_profiles': 19,
            'five_six_remaining_unexcluded_count': 27, 'three_six_total_excluded_profiles': 9,
            'three_six_remaining_unexcluded_count': 39, 'characteristic_class_size_range': [4, 8],
            'exact_n7_chromatic_number': 'open', 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'five_even_sum': 63, 'six_even_sum': 48, 'six_odd_projections': [48, 15],
            'mixed_odd_projections': [3, 12], 'characteristic_projections': [51, 60, 63], 'characteristic_charge': 48,
            'five_blocks': len(five), 'six_four_even_blocks': len(four), 'mixed_sextets_each': [len(mixed_left), len(mixed_right)],
            'disjoint_defect_pairs': sum(defect_histogram.values()), 'defect_pairs_by_pure_five_hole': dict(sorted(defect_histogram.items())),
            'ordered_roots_by_pure_five_hole': dict(sorted(root_histogram.items())),
            'remaining_even_cover_points': 42, 'remaining_heptads': 6, 'remaining_holes': 6,
            'even_heptads': len(heptads), 'eligible_heptad_catalog': len(rows), 'eligible_rows_avoiding_each_pure_five_hole': 192,
            'eligible_ordered_roots': len(expected_roots), 'distinct_root_states': len({row['remaining'] for row in expected_roots}),
            'failed_states_checked': len(failed), 'branches_checked': branches, 'leaf_states': leaves,
            'state_sizes': dict(sorted(sizes.items())), 'all_states_reachable': True, 'hole_anchor_count_checked_at_every_state': True,
            'normalization_frames': frames, 'normalization_Gram_entries_checked': gram_controls,
            'inverse_source_class_controls': source_class_controls, 'prior_four_form_local_report_fully_reaudited': True,
            'written_eight_spread_completion_used': True, 'existing_charge_member_lemma_applied': True,
            'new_checked_finite_cover_certificate': True, 'new_exact_cover_search': True,
            'search_scope': 'Only62976ordered roots for the universally normalized D form;150000states,1000000visits,30seconds.',
            'prior_seven_heptad_cover_certificate_used': False, 'prior_spread_enumeration_rerun': False,
            'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_and_Zenodo_PDF_changed': False,
            'certificate_sha256': digest(certificate_path), 'builder_sha256': digest(root / 'develop/build_dimension_seven_five_four_D_cover.py'),
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-five-four-D-cover.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written marked D reduction plus independently audited new six-heptad certificate excludes D only. All t values and both mixed classes retained. Z/H/G and the raw profile remain unexcluded;27five-six/39three-sixrows and exactn7open>=19.'}


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
