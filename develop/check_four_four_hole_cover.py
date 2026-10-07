"""Independently reconstruct and audit the four-four completed-hole cover certificate."""
from collections import Counter
from itertools import combinations, permutations, product
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


def bit_cliques(points, size):
    neighbors = {point: mask(other for other in points if other > point and dot(point, other)) for point in points}
    output = []

    def visit(chosen, available):
        if len(chosen) == size:
            output.append(chosen)
            return
        while available:
            first = available & -available
            point = first.bit_length() - 1
            available ^= first
            visit(chosen + (point,), available & neighbors[point])

    visit((), mask(points))
    return output


def check(certificate_path):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if point.bit_count() % 2 == 0]
    universe = mask(points)
    holes = {3, 12, 15, 48, 51, 60, 63}
    heptads = bit_cliques(points, 7)
    assert len(heptads) == 288
    assert all(vector_sum(block) == 0 for block in heptads)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    expected_roots = []
    configurations = []
    catalogs = []
    for first_other, second_other, mixed_odd in permutations((15, 51, 60)):
        first = [block for block in bit_cliques([point for point in points if dot(point, 3) and dot(point, first_other)], 4)
                 if vector_sum(block) == first_other]
        second = [block for block in bit_cliques([point for point in points if dot(point, 12) and dot(point, second_other)], 4)
                  if vector_sum(block) == second_other]
        mixed = bit_cliques([point for point in points if dot(point, mixed_odd)], 6)
        assert len(first) == len(second) == 16 and len(mixed) == 32
        assert all(vector_sum(block) == mixed_odd for block in mixed)
        for blocks, odd_projections, charge in ((first, (3, first_other), 3), (second, (12, second_other), 12)):
            for block in blocks:
                full = block + tuple(127 ^ point for point in odd_projections)
                assert all(dot(left, right) == 1 for left, right in combinations(full, 2))
                assert vector_sum(full) == charge
        assert all(all(dot(left, right) == 1 for left, right in combinations(block + (127 ^ mixed_odd,), 2)) for block in mixed)
        before = len(expected_roots)
        for left in first:
            for right in second:
                if set(left) & set(right):
                    continue
                for block in mixed:
                    if set(block) & (set(left) | set(right)):
                        continue
                    remaining = universe ^ mask(left + right + block)
                    assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                    expected_roots.append({'configuration': [first_other, second_other, mixed_odd],
                                           'first': list(left), 'second': list(right), 'mixed': list(block),
                                           'remaining': str(remaining)})
        configurations.append({'configuration': [first_other, second_other, mixed_odd],
                               'class_catalog_sizes': [len(first), len(second), len(mixed)],
                               'disjoint_partial_triples': len(expected_roots) - before})
        catalogs.append([first, second, mixed])
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'roots', 'failed_states'}
    assert certificate['roots'] == expected_roots
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
    children = {}
    sizes = Counter()
    leaves = 0
    branches = 0
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
    frontier = [int(item['remaining']) for item in expected_roots]
    reached = set()
    while frontier:
        remaining = frontier.pop()
        assert remaining in failed
        if remaining not in reached:
            reached.add(remaining)
            frontier.extend(children[remaining])
    assert reached == set(failed)
    target_basis = (3, 12, 48, 65, 71, 95)
    basis_pair_checks = 0
    frames = 0
    projected_configurations = 0
    for first_charge, second_charge, first_characteristic in permutations(sorted(holes), 3):
        if first_characteristic in {first_charge ^ second_charge}:
            continue
        source_half = (first_charge, second_charge, first_characteristic)
        assert len({vector_sum(source_half[index] for index in range(3) if bits & (1 << index)) for bits in range(8)}) == 8
        duals = []
        for position in range(3):
            dual = next(point for point in points if all(dot(point, source_half[index]) == int(index == position) for index in range(3))
                        and all(dot(point, previous) == 0 for previous in duals))
            duals.append(dual)
        source_basis = source_half + tuple(duals)
        assert all(dot(source_basis[left], source_basis[right]) == dot(target_basis[left], target_basis[right]) for left, right in product(range(6), repeat=2))
        basis_pair_checks += 36
        mapping = {vector_sum(source_basis[index] for index in range(6) if bits & (1 << index)):
                   vector_sum(target_basis[index] for index in range(6) if bits & (1 << index)) for bits in range(64)}
        assert len(mapping) == 64 and len(set(mapping.values())) == 64
        assert {mapping[point] for point in holes} == holes
        second_characteristic = first_characteristic ^ first_charge ^ second_charge
        assert mapping[second_characteristic] == 63
        remainder = sorted(holes - {first_charge, second_charge, first_characteristic, second_characteristic})
        for assignment in permutations(remainder):
            assert tuple(mapping[point] for point in assignment) in set(permutations((15, 51, 60)))
            assert vector_sum(assignment) == 0
            projected_configurations += 1
        frames += 1
    assert frames == 168 and projected_configurations == 1008
    prior_path = root / 'results/dimension-7-two-six-profiles.json'
    prior = json.loads(prior_path.read_text())
    assert prior['remaining_profiles'] == [[0, 0, 3, 7, 6], [0, 2, 1, 9, 6], [4, 4, 7, 1, 8]]
    assert prior['checker_sha256'] == hashlib.sha256((root / 'develop/check_dimension_seven_two_six_profiles.py').read_bytes()).hexdigest()
    assert prior['proof_note_sha256'] == hashlib.sha256((root / 'notes/dimension-seven-two-six-profiles.md').read_bytes()).hexdigest()
    return {'status': 'C8_four_four_two_six_profile_excluded_by_checked_exact_cover_certificate',
            'dimension': 7, 'excluded_profile': [4, 4, 7, 1, 8],
            'remaining_two_six_profiles': [[0, 0, 3, 7, 6], [0, 2, 1, 9, 6]],
            'initial_two_six_count_profiles': 21, 'excluded_two_six_count_profiles': 19,
            'all_C7_and_C8_two_six_profiles_excluded': True,
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False,
            'nineteen_color_witness': False, 'size_three_entire_branch_excluded': False,
            'six_Lagrangian_completion_claimed': False, 'configurations': configurations,
            'even_heptads': len(heptads), 'eligible_heptad_rows': len(rows),
            'eligible_ordered_roots': len(expected_roots),
            'distinct_root_states': len({item['remaining'] for item in expected_roots}),
            'failed_states_checked': len(failed), 'branches_checked': branches, 'leaf_states': leaves,
            'state_sizes': dict(sorted(sizes.items())), 'all_states_reachable': True,
            'normalization_frames': frames, 'normalization_basis_dot_pairs_checked': basis_pair_checks,
            'ordered_projection_configurations_checked': projected_configurations,
            'row_catalog_sha256': hashlib.sha256(json.dumps([heptads, catalogs], separators=(',', ':')).encode()).hexdigest(),
            'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'auditor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'builder_sha256': hashlib.sha256((root / 'develop/build_four_four_hole_cover.py').read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-four-four-hole-cover.md').read_bytes()).hexdigest(),
            'prior_two_six_report_sha256': hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            'checked_exact_cover_certificate': True, 'native_SAT': False, 'DRAT_checked': False,
            'Lean_run': False, 'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'scope': 'Written eight-spread completion and charge-member normalization reduce this C8 profile to six fixed-hole configurations. Every disjoint partial triple and every finite failed-state branch is independently reconstructed and checked. Only two C6 count candidates remain; their common-coloring realizability and the entire s3 branch stay open.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.certificate)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
