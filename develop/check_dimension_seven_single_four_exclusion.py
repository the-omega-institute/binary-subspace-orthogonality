"""Check the single-four-defect normalization and reuse the existing cover certificate."""
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


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    configurations = []
    locations = Counter()
    gram_controls = 0
    for odd_pair in combinations(sorted(holes), 2):
        candidates = [point for point in points if all(dot(point, odd) for odd in odd_pair)]
        for even_pair in combinations(candidates, 2):
            if not dot(*even_pair):
                continue
            charge = vector_sum(even_pair + odd_pair)
            for characteristic in combinations(sorted(holes - set(odd_pair)), 3):
                if vector_sum(characteristic) != charge:
                    continue
                mixed = holes - set(odd_pair) - set(characteristic)
                first, second = even_pair
                radical = first ^ second
                assert radical == vector_sum(mixed) and radical in holes
                assert all(dot(first, point) == dot(second, point) for point in holes)
                assert dot(first, radical) == 1
                zero = next(point for point in mixed if not dot(first, point))
                one = next(point for point in mixed if dot(first, point))
                kernel = sorted(point for point in holes if not dot(first, point))
                assert len(kernel) == 3 and one == zero ^ radical
                first_base = next(point for point in kernel if point != zero)
                second_base = first_base ^ zero
                dual_first = next(point for point in points if dot(point, first_base) == 1
                                  and not dot(point, second_base) and not dot(point, radical)
                                  and not dot(point, first))
                dual_second = next(point for point in points if not dot(point, first_base)
                                   and dot(point, second_base) == 1 and not dot(point, radical)
                                   and not dot(point, first) and not dot(point, dual_first))
                source_basis = (first_base, second_base, radical, dual_first, dual_second, first, 127)
                assert all(dot(source_basis[left], source_basis[right]) == dot(target_basis[left], target_basis[right])
                           for left in range(7) for right in range(7))
                gram_controls += 49
                mapping = {vector_sum(source_basis[index] for index in range(7) if bits & (1 << index)):
                           vector_sum(target_basis[index] for index in range(7) if bits & (1 << index))
                           for bits in range(128)}
                assert len(mapping) == len(set(mapping.values())) == 128 and mapping[127] == 127
                assert {mapping[point] for point in holes} == holes
                assert (mapping[first], mapping[second], mapping[zero], mapping[one]) == (95, 111, 15, 63)
                characteristic_class = (127,) + tuple(127 ^ point for point in characteristic)
                defect = even_pair + tuple(127 ^ point for point in odd_pair)
                assert not set(characteristic_class) & set(defect)
                for block in (characteristic_class, defect):
                    assert all(dot(mapping[left], mapping[right]) for left, right in combinations(block, 2))
                location = 'charge_in_defect' if charge in odd_pair else 'charge_in_mixed'
                assert charge in set(odd_pair) | mixed
                locations[location] += 1
                configurations.append((odd_pair, even_pair, characteristic, tuple(sorted(mixed)), charge))
    assert len(configurations) == 1008 and locations == {'charge_in_defect': 672, 'charge_in_mixed': 336}
    universe = mask(points)
    neighbors = {point: mask(other for other in points if other > point and dot(point, other)) for point in points}
    six = []

    def enumerate_six(chosen, available):
        if len(chosen) == 6:
            six.append(chosen)
            return
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            enumerate_six(chosen + (point,), available & neighbors[point])

    enumerate_six((), universe)
    assert len(six) == 2016
    heptads = set()
    for block in six:
        completion = vector_sum(block)
        assert completion in points and completion not in block
        heptad = tuple(sorted(block + (completion,)))
        assert all(dot(left, right) for left, right in combinations(heptad, 2))
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
            used = mask(first) | mask(second)
            if set(first) & set(second) or used & blocked:
                continue
            remaining = universe ^ (used | blocked)
            assert remaining.bit_count() == 49
            expected_roots.append({'first': list(first), 'second': list(second), 'remaining': str(remaining)})
    assert len(expected_roots) == 384
    certificate_path = root / 'results/dimension-7-hole-cover-proof.json'
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'roots', 'failed_states'} and certificate['roots'] == expected_roots
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states']) == 1784
    children = {}
    leaves = 0
    branches = 0
    for remaining, pivot in failed.items():
        assert remaining > 0 and remaining & universe == remaining
        assert remaining.bit_count() % 7 == 0 and remaining.bit_count() <= 49
        assert pivot in points and remaining & (1 << pivot)
        successors = [remaining ^ row for row in rows if row & (1 << pivot) and row & remaining == row]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7 for successor in successors)
        children[remaining] = successors
        branches += len(successors)
        leaves += not successors
    frontier = [int(item['remaining']) for item in expected_roots]
    reached = set()
    while frontier:
        state = frontier.pop()
        assert state in failed
        if state not in reached:
            reached.add(state)
            frontier.extend(children[state])
    assert reached == set(failed) and branches == 1400 and leaves == 968
    prior_size_four = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    assert prior_size_four['single_four_remaining_profiles'] == [[2, 2, 7, 2, 8]]
    assert prior_size_four['single_four_excluded_profiles'] == 8
    local_digest = hashlib.sha256(json.dumps(sorted(configurations), separators=(',', ':')).encode()).hexdigest()
    assert local_digest == prior_size_four['local_configuration_sha256']
    old_audit = json.loads((root / 'results/dimension-7-hole-cover-check.json').read_text())
    for key, name in (('certificate_sha256', 'results/dimension-7-hole-cover-proof.json'),
                      ('auditor_sha256', 'develop/check_three_point_hole_cover.py'),
                      ('builder_sha256', 'develop/build_three_point_hole_cover.py'),
                      ('proof_note_sha256', 'notes/dimension-seven-hole-cover.md')):
        assert old_audit[key] == hashlib.sha256((root / name).read_bytes()).hexdigest()
    for key, name in (('checker_sha256', 'develop/check_dimension_seven_size_four.py'),
                      ('proof_note_sha256', 'notes/dimension-seven-size-four.md')):
        assert prior_size_four[key] == hashlib.sha256((root / name).read_bytes()).hexdigest()
    dependencies = ('results/dimension-7-size-four.json', 'results/dimension-7-hole-cover-check.json',
                    'results/dimension-7-hole-cover-proof.json')
    return {'status': 'entire_size_four_single_four_point_defect_branch_excluded',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'characteristic_class_size_range': [4, 8],
            'characteristic_size_four_excluded': False, 'single_four_entire_branch_excluded': True,
            'newly_excluded_profile': [2, 2, 7, 2, 8], 'single_four_remaining_profiles': [],
            'five_six_branch': 'open_46_raw_count_profiles_not_feasibility_checked',
            'three_six_branch': 'open_48_raw_count_profiles_not_feasibility_checked',
            'fixed_hole_local_configurations': len(configurations), 'local_charge_location_histogram': dict(sorted(locations.items())),
            'local_configuration_sha256': local_digest, 'basis_gram_pair_controls': gram_controls,
            'even_six_cliques': len(six), 'even_heptads': len(heptads), 'eligible_heptad_rows': len(rows),
            'forced_six_choices': {target: len(blocks) for target, blocks in forced.items()},
            'eligible_ordered_roots': len(expected_roots), 'roots_equal_existing_certificate': True,
            'failed_states_checked': len(failed), 'branches_checked': branches, 'leaf_states': leaves,
            'all_states_reachable': True, 'existing_finite_cover_certificate_reaudited': True,
            'exact_cover_search': False, 'prior_spread_enumeration_rerun': False,
            'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
            'new_numerical_lower_bound': False, 'nineteen_color_witness': False, 'submitted_manuscript_changed': False,
            'dependency_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in dependencies},
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-single-four-exclusion.md').read_bytes()).hexdigest(),
            'scope': 'Universal written covering-data normalization,1008fixed-hole local controls,and full reaudit of the existing384root failed-state certificate. Entire single4defect branch excluded;5+6/6+6+6raw46/48profiles and sizes4..8/exactn7open>=19. No full marked orbit classification,new cover search,Lean or independent Pro review.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
