"""Check common-even-sum exclusions and the existing hole-cover certificate."""
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


def check(certificate_path=None):
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    prior_split = json.loads((root / 'results/dimension-7-five-six-split31.json').read_text())
    local_five = []
    local_placements = []
    zero_completion = 0
    charges = Counter()
    roles = Counter()
    gram_controls = 0
    for odd_triple in combinations(sorted(holes), 3):
        candidates = [point for point in points if all(dot(point, odd) for odd in odd_triple)]
        pairs = [pair for pair in combinations(candidates, 2) if dot(*pair)]
        for even_pair in pairs:
            first, second = even_pair
            radical = first ^ second
            charge_five = radical ^ vector_sum(odd_triple)
            assert radical in holes and dot(first, radical) == 1
            assert all(dot(first, point) == dot(second, point) for point in holes)
            local_five.append((odd_triple, even_pair, charge_five))
            for mixed_odd in sorted(holes - set(odd_triple)):
                characteristic = tuple(sorted(holes - set(odd_triple) - {mixed_odd}))
                characteristic_charge = vector_sum(characteristic)
                pure_even_charge = radical ^ mixed_odd
                assert characteristic_charge == vector_sum(odd_triple) ^ mixed_odd
                assert charge_five ^ pure_even_charge == characteristic_charge
                characteristic_class = (127,) + tuple(127 ^ point for point in characteristic)
                defect_five = even_pair + tuple(127 ^ point for point in odd_triple)
                assert not set(characteristic_class) & set(defect_five)
                assert 127 ^ mixed_odd not in set(characteristic_class) | set(defect_five)
                assert all(dot(left, right) for block in (characteristic_class, defect_five)
                           for left, right in combinations(block, 2))
                if not pure_even_charge:
                    assert mixed_odd == radical
                    zero_completion += 1
                    continue
                assert pure_even_charge in holes and pure_even_charge != mixed_odd
                pair = (mixed_odd, pure_even_charge)
                assert dot(first, pair[0]) ^ dot(first, pair[1]) == 1
                zero = next(point for point in pair if not dot(first, point))
                one = next(point for point in pair if dot(first, point))
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
                assert {mapping[mixed_odd], mapping[pure_even_charge]} == {15, 63}
                for block in (characteristic_class, defect_five):
                    assert all(dot(mapping[left], mapping[right]) for left, right in combinations(block, 2))
                charges['zero' if not characteristic_charge else 'nonzero'] += 1
                roles[str(mapping[mixed_odd])] += 1
                local_placements.append((odd_triple, even_pair, mixed_odd, characteristic, pure_even_charge))
    assert len(local_five) == 448 and zero_completion == 112 and len(local_placements) == 1680
    assert charges == {'zero': 336, 'nonzero': 1344} and roles == {'15': 1344, '63': 336}
    assert hashlib.sha256(json.dumps(local_five, separators=(',', ':')).encode()).hexdigest() == prior_split['five_configuration_sha256']
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
    completed_heptads = set()
    completions = Counter()
    for block in six:
        completion = vector_sum(block)
        assert completion in points and completion not in block
        assert all(dot(left, right) for left, right in combinations(block, 2))
        assert all(dot(completion, point) for point in block)
        heptad = tuple(sorted(block + (completion,)))
        assert vector_sum(heptad) == 0
        completed_heptads.add(heptad)
        completions[completion] += 1
        if completion in holes:
            assert not set(block) & holes
    assert len(completed_heptads) == 288 and set(completions.values()) == {32}
    array_heptads = []

    def enumerate_heptads(chosen, available):
        if len(chosen) == 7:
            array_heptads.append(chosen)
            return
        for index, point in enumerate(available):
            compatible = [other for other in available[index + 1:] if dot(point, other)]
            enumerate_heptads(chosen + (point,), compatible)

    enumerate_heptads((), points)
    assert set(array_heptads) == completed_heptads and len(array_heptads) == 288
    array_six = {block for heptad in array_heptads for block in combinations(heptad, 6)}
    assert array_six == set(six)
    rows = sorted(mask(block) for block in array_heptads if len(set(block) & holes) == 1)
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
            assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
            expected_roots.append({'first': list(first), 'second': list(second), 'remaining': str(remaining)})
    assert len(expected_roots) == 384
    certificate_path = certificate_path or root / 'results/dimension-7-hole-cover-proof.json'
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
    old_audit = json.loads((root / 'results/dimension-7-hole-cover-check.json').read_text())
    assert old_audit['certificate_sha256'] == digest(certificate_path)
    for key, name in (('auditor_sha256', 'develop/check_three_point_hole_cover.py'),
                      ('builder_sha256', 'develop/build_three_point_hole_cover.py'),
                      ('proof_note_sha256', 'notes/dimension-seven-hole-cover.md')):
        assert old_audit[key] == digest(root / name)
    prior_capacity = json.loads((root / 'results/dimension-7-hole-capacity.json').read_text())
    for prior, checker, note in ((prior_capacity, 'develop/check_dimension_seven_hole_capacity.py', 'notes/dimension-seven-hole-capacity.md'),
                                  (prior_split, 'develop/check_dimension_seven_five_six_split31.py', 'notes/dimension-seven-five-six-split31.md')):
        assert prior['checker_sha256'] == digest(root / checker)
        assert prior['proof_note_sha256'] == digest(root / note)
        for name, expected in prior['dependency_sha256'].items():
            assert digest(root / name) == expected
    product_controls = 0
    for even_sum in [0] + points:
        for first_odd_sum in sorted(holes | {0}):
            for second_odd_sum in sorted(holes | {0}):
                assert dot(even_sum ^ first_odd_sum, even_sum ^ second_odd_sum) == dot(even_sum, first_odd_sum ^ second_odd_sum)
                product_controls += 1
    assert product_controls == 4096
    prior_count = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    parity_rows = []
    for row in prior_count['count_profiles']['5+6']:
        if row['saturated_counts'][1:] != [0, 8]:
            continue
        even = row['defect_even_counts']
        odd = row['defect_odd_counts']
        computed = sum(even_count * odd_count for even_count, odd_count in zip(even, odd)) % 2
        taus = [(size * (size - 1) // 2 + count * (count - 1) // 2) % 2
                for size, count in zip((5, 6), odd)]
        required = (sum(row['saturated_counts'][:2]) + sum(taus)) % 2
        assert required == row['required_sum_of_pairwise_charge_products']
        assert computed != required
        parity_rows.append({'profile': even + row['saturated_counts'], 'computed_product': computed, 'required_product': required})
    assert len(parity_rows) == 4
    target = [2, 6, 7, 1, 8]
    parity_target = [3, 4, 8, 0, 8]
    assert prior_capacity['five_six_remaining_unexcluded_count'] == 31
    assert prior_capacity['five_six_remaining_raw_profiles'].count(target) == 1
    assert prior_capacity['five_six_remaining_raw_profiles'].count(parity_target) == 1
    assert [row['profile'] for row in parity_rows if row['profile'] in prior_capacity['five_six_remaining_raw_profiles']] == [parity_target]
    remaining = [row for row in prior_capacity['five_six_remaining_raw_profiles'] if row not in (target, parity_target)]
    assert len(remaining) == 29 and prior_capacity['three_six_remaining_unexcluded_count'] == 39
    dependencies = ('results/dimension-7-hole-capacity.json', 'results/dimension-7-five-six-split31.json',
                    'results/dimension-7-hole-cover-check.json', 'results/dimension-7-hole-cover-proof.json',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'two_size_four_five_plus_six_profiles_excluded_by_common_even_sum_and_existing_cover',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'cover_excluded_profile': target, 'written_parity_excluded_profile': parity_target,
            'newly_excluded_profiles': [target, parity_target], 'profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'five_six_initial_raw_profiles': 46, 'five_six_total_excluded_profiles': 17,
            'five_six_remaining_unexcluded_count': 29, 'five_six_remaining_raw_profiles': remaining,
            'three_six_initial_raw_profiles': 48, 'three_six_total_excluded_profiles': 9,
            'three_six_remaining_unexcluded_count': 39,
            'three_six_remaining_raw_profiles': prior_capacity['three_six_remaining_raw_profiles'],
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'five_point_local_defects': len(local_five), 'conditional_odd_placements': len(local_placements) + zero_completion,
            'zero_pure_even_completion_exclusions': zero_completion, 'normalized_nonzero_completion_controls': len(local_placements),
            'characteristic_charge_histogram': dict(sorted(charges.items())), 'normalized_mixed_sum_histogram': dict(sorted(roles.items())),
            'normalization_Gram_entries_checked': gram_controls,
            'common_even_sum_product_controls': product_controls, 'uniform_C8_B0_parity_exclusions': parity_rows,
            'all_four_C8_B0_raw_profiles_excluded': True,
            'local_placement_sha256': hashlib.sha256(json.dumps(local_placements, separators=(',', ':')).encode()).hexdigest(),
            'even_six_cliques': len(six), 'even_heptads': len(array_heptads), 'array_and_bitmask_catalogs_equal': True,
            'eligible_heptad_rows': len(rows), 'forced_six_choices': {target: len(blocks) for target, blocks in forced.items()},
            'eligible_ordered_roots': len(expected_roots), 'failed_states_checked': len(failed),
            'branches_checked': branches, 'leaf_states': leaves, 'all_states_reachable': True,
            'written_eight_spread_completion_used': True, 'existing_finite_cover_certificate_used': True,
            'certificate_sha256': digest(certificate_path), 'new_exact_cover_search': False,
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_and_Zenodo_PDF_changed': False,
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-five-six-cover.md'),
            'scope': 'Written charge/normalization reduces(2,6;7,1,8)to the existing384-root cover certificate, fully reaudited without a new search.1680conditional controls retain both six-class roles and both h charges. Written common-even-sum parity excludes(3,4;8,0,8)and recovers all three prior C8B0 exclusions.29five-six/39three-six raw profiles unexcluded;size4..8andexactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.certificate)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
