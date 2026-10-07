"""Independently audit the normalized exact-cover failed-state certificate."""
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


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def check(certificate_path):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    universe = mask(points)
    holes = {3, 12, 15, 48, 51, 60, 63}
    neighbors = {point: mask(other for other in points if other > point and dot(point, other)) for point in points}
    six = []

    def enumerate_six(chosen, candidates):
        if len(chosen) == 6:
            six.append(chosen)
            return
        while candidates:
            first = candidates & -candidates
            point = first.bit_length() - 1
            candidates ^= first
            enumerate_six(chosen + (point,), candidates & neighbors[point])

    enumerate_six((), universe)
    assert len(six) == 2016
    heptads = set()
    for block in six:
        completion = vector_sum(block)
        assert completion not in block and completion in points
        heptad = tuple(sorted(block + (completion,)))
        assert all(dot(left, right) == 1 for left, right in combinations(heptad, 2))
        heptads.add(heptad)
    assert len(heptads) == 288
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    forced = {target: sorted(block for block in six if vector_sum(block) == target) for target in (15, 63)}
    assert all(len(blocks) == 32 for blocks in forced.values())
    blocked = mask((95, 111))
    expected_roots = []
    for first in forced[15]:
        for second in forced[63]:
            if set(first) & set(second) or (mask(first) | mask(second)) & blocked:
                continue
            remaining = universe ^ (mask(first) | mask(second) | blocked)
            assert remaining.bit_count() == 49
            expected_roots.append({'first': list(first), 'second': list(second), 'remaining': str(remaining)})
    assert len(expected_roots) == 384
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'roots', 'failed_states'}
    assert certificate['roots'] == expected_roots
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
    children = {}
    leaves = 0
    branch_count = 0
    sizes = Counter()
    for remaining, pivot in failed.items():
        assert remaining > 0 and remaining & universe == remaining
        assert remaining.bit_count() % 7 == 0 and remaining.bit_count() <= 49
        assert pivot in points and remaining & (1 << pivot)
        sizes[remaining.bit_count()] += 1
        options = [row for row in rows if row & (1 << pivot) and row & remaining == row]
        successors = [remaining ^ row for row in options]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7 for successor in successors)
        children[remaining] = successors
        branch_count += len(successors)
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
    lagrangians = set()
    for left, middle, right in combinations(points, 3):
        if not any((dot(left, middle), dot(left, right), dot(middle, right))) and left ^ middle ^ right:
            lagrangians.add(frozenset((0, left, middle, right, left ^ middle, left ^ right,
                                      middle ^ right, left ^ middle ^ right)))
    local_controls = set()
    target_basis = (3, 12, 48, 65, 71, 95)
    target_defect = frozenset((95, 111, 79, 76, 67))
    normalization_checks = 0
    for space in sorted(lagrangians, key=lambda value: tuple(sorted(value))):
        if not {3, 12}.issubset(space):
            continue
        for radical in sorted(space):
            if radical in {0, 3, 12, 15}:
                continue
            for even_first in points:
                if dot(even_first, 3) or dot(even_first, 12) or dot(even_first, radical) != 1:
                    continue
                even_second = even_first ^ radical
                affine = {point for point in space if dot(even_first, point) == 1}
                missing = radical ^ 15
                assert len(affine) == 4 and missing in affine
                defect = frozenset((even_first, even_second, *(127 ^ point for point in affine - {missing})))
                if defect in local_controls:
                    continue
                local_controls.add(defect)
                dual_first = next(point for point in points if dot(point, 3) == 1 and dot(point, 12) == 0
                                  and dot(point, radical) == 0 and dot(point, even_first) == 0)
                dual_second = next(point for point in points if dot(point, 3) == 0 and dot(point, 12) == 1
                                   and dot(point, radical) == 0 and dot(point, even_first) == 0
                                   and dot(point, dual_first) == 0)
                source_basis = (3, 12, radical, dual_first, dual_second, even_first)
                mapping = {vector_sum(source_basis[index] for index in range(6) if bits & (1 << index)):
                           vector_sum(target_basis[index] for index in range(6) if bits & (1 << index))
                           for bits in range(64)}
                assert len(mapping) == 64
                lifted = {point: mapping[point ^ (127 if dot(point, 127) else 0)]
                          ^ (127 if dot(point, 127) else 0) for point in range(128)}
                assert len(set(lifted.values())) == 128
                assert {lifted[point] for point in defect} == target_defect
                assert {lifted[point] for point in space} == holes | {0}
                assert {lifted[point] for point in (127, 124, 115)} == {127, 124, 115}
                assert all(dot(lifted[left], lifted[right]) == dot(left, right)
                           for left in range(128) for right in range(128))
                normalization_checks += 16384
    assert len(local_controls) == 48 and normalization_checks == 786432
    assert all(all(dot(left, right) == 1 for left, right in combinations(block, 2)) for block in local_controls)
    return {'status': 'completed_hole_three_point_one_five_defect_profile_excluded_by_checked_exact_cover_certificate',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'nineteen_color_witness': False,
            'new_numerical_lower_bound': False, 'excluded_profile': [2, 3, 7, 2, 8],
            'remaining_one_five_profiles': [[0, 5, 3, 7, 7], [1, 4, 2, 8, 7]],
            'two_six_branch': 'open_not_enumerated', 'characteristic_class_size_range': [3, 8],
            'even_six_cliques': 2016, 'even_heptads': 288, 'eligible_heptad_rows': 224,
            'forced_six_choices': {target: len(blocks) for target, blocks in forced.items()},
            'eligible_ordered_roots': len(expected_roots), 'distinct_root_states': len(set(row['remaining'] for row in expected_roots)),
            'failed_states_checked': len(failed), 'branches_checked': branch_count, 'leaf_states': leaves,
            'state_sizes': dict(sorted(sizes.items())), 'all_states_reachable': True,
            'normalization_local_defect_controls': len(local_controls), 'normalization_dot_pairs_checked': normalization_checks,
            'normalization_scope': 'Written symplectic basis/shear proof is universal; 48 local defect controls with a fixed characteristic pair are independently verified, not complete colorings.',
            'checked_exact_cover_certificate': True, 'native_SAT': False, 'DRAT_checked': False,
            'Lean_run': False, 'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'auditor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'builder_sha256': hashlib.sha256((root / 'develop/build_three_point_hole_cover.py').read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-hole-cover.md').read_bytes()).hexdigest(),
            'prior_defect_report_sha256': hashlib.sha256((root / 'results/dimension-7-three-point-defects.json').read_bytes()).hexdigest(),
            'scope': 'Every normalized candidate root and every failed-state branch independently reconstructed and checked; excludes this one profile only, not all nineteen-colorings or the full s=3 branch.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.certificate)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
