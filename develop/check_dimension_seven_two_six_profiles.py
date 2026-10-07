"""Check two-six count profiles and local controls for eighteen written exclusions."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
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


def independent(block):
    return len(set(block)) == len(block) and all(dot(left, right) == 1 for left, right in combinations(block, 2))


def cliques(points, size):
    output = []

    def visit(chosen, available):
        if len(chosen) == size:
            output.append(chosen)
            return
        if len(available) < size - len(chosen):
            return
        for index, point in enumerate(available):
            visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    visit((), sorted(points))
    return output


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    bindings = {}
    for name in ('dimension-7-nineteen-obstruction.json', 'dimension-7-seven-holes.json',
                 'dimension-7-one-five-exclusion.json', 'dimension-7-three-point-defects.json',
                 'dimension-7-characteristic-three.json'):
        bindings[name] = hashlib.sha256((root / 'results' / name).read_bytes()).hexdigest()
    assert bindings['dimension-7-one-five-exclusion.json'] == '88d24335c41f525a34ca4df2447fe76618d315dc199d5202b2d754b78c009c68'
    assert bindings['dimension-7-seven-holes.json'] == '6fae4b1d6d60a27f4049a40210981661af36163d98b1980d33345abe63fea0a0'
    prior = json.loads((root / 'results/dimension-7-one-five-exclusion.json').read_text())
    assert prior['one_five_branch_excluded'] and not prior['size_three_entire_branch_excluded']
    assert prior['checker_sha256'] == hashlib.sha256((root / 'develop/check_dimension_seven_one_five_exclusion.py').read_bytes()).hexdigest()
    assert prior['proof_note_sha256'] == hashlib.sha256((root / 'notes/dimension-seven-one-five-exclusion.md').read_bytes()).hexdigest()
    direct = []
    formula = []
    even_counts = (0, 2, 4, 5, 6)
    for first, second in combinations_with_replacement(even_counts, 2):
        total_even = first + second
        for pure_even in range(17):
            for mixed in range(17 - pure_even):
                pure_odd = 16 - pure_even - mixed
                if 7 * pure_even + 6 * mixed + total_even == 63 and mixed + 7 * pure_odd + 12 - total_even + 3 == 64:
                    direct.append((first, second, pure_even, mixed, pure_odd))
        for shift in range(-3, 4):
            mixed = total_even + 7 * shift
            pure_even = 9 - total_even - 6 * shift
            pure_odd = 7 - shift
            if min(pure_even, mixed, pure_odd) >= 0:
                formula.append((first, second, pure_even, mixed, pure_odd))
    assert sorted(direct) == sorted(formula) and len(direct) == 21
    profiles = []
    for first, second, pure_even, mixed, pure_odd in sorted(direct):
        status = 'necessary_profile_realizability_open'
        bound = None
        two_hole_bound = None
        single_hole_bound = None
        if pure_odd == 8:
            bound = pure_even + int(first == 6) + int(second == 6)
            if bound < 7:
                status = 'excluded_by_completed_hole_clique_label_budget'
            elif (first, second) == (2, 5):
                status = 'excluded_by_charge_in_hole_lagrangian_and_odd_pairing'
            elif (first, second) == (2, 6):
                status = 'excluded_by_conditional_transfer_to_one_five_branch'
        elif pure_odd == 7:
            capacities = {0: 0, 2: 1, 4: 1, 5: 1, 6: 2}
            two_hole_bound = 2 * pure_even + mixed + capacities[first] + capacities[second]
            if two_hole_bound < 14:
                status = 'excluded_by_two_hole_even_point_capacity'
            elif (first, second) == (0, 0):
                assert pure_even == 9 and mixed == 0
                status = 'excluded_by_existing_nine_even_heptad_quadratic_partition'
            elif (first, second) == (0, 2):
                status = 'excluded_by_pure_odd_charge_and_characteristic_collision'
            elif first == 0 and second in (4, 5, 6):
                single_hole_bound = pure_even + (2 if second == 6 else 1)
                assert single_hole_bound < 7
                status = 'excluded_by_six_odd_points_and_other_hole_label_budget'
            elif first == 2 and second in (2, 4):
                status = 'excluded_by_affine_odd_plane_and_member_charge_overlap'
        profiles.append({'defect_even_counts': [first, second], 'defect_odd_counts': [6 - first, 6 - second],
                         'saturated_counts': [pure_even, mixed, pure_odd], 'hole_label_bound_when_C8': bound,
                         'two_hole_even_point_capacity_when_C7': two_hole_bound,
                         'other_hole_label_bound_with_six_odd_defect': single_hole_bound, 'status': status})
    survivors = [item for item in profiles if item['status'] == 'necessary_profile_realizability_open']
    assert len(survivors) == 3 and not any(item['saturated_counts'][2] == 7 for item in survivors)
    assert [item['defect_even_counts'] + item['saturated_counts'] for item in survivors if item['saturated_counts'][2] == 8] == [[4, 4, 7, 1, 8]]
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    first_hole = (3, 12, 15, 48, 51, 60, 63)
    second_hole = (6, 24, 30, 65, 71, 89, 95)
    affine = (48, 51, 60, 63)
    even_candidates = [point for point in points if all(dot(point, projection) for projection in affine)]
    local_two_even = []
    charge_histogram = Counter()
    for even_pair in combinations(even_candidates, 2):
        block = even_pair + tuple(127 ^ projection for projection in affine)
        if independent(block):
            charge = vector_sum(block)
            assert charge in affine and (127 ^ charge) in block
            assert all(dot(point, 127 ^ charge) for point in block)
            local_two_even.append((even_pair, block, charge))
            charge_histogram[charge] += 1
    assert len(local_two_even) == 16 and set(charge_histogram.values()) == {4}
    four_even_candidates = [point for point in points if dot(point, 3) and dot(point, 12)]
    four_even_histogram = Counter()
    for even_part in cliques(four_even_candidates, 4):
        block = even_part + (124, 115)
        assert independent(block)
        charge = vector_sum(block)
        assert charge in (3, 12) and (127 ^ charge) in block
        assert all(dot(point, 127 ^ charge) for point in block)
        four_even_histogram[charge] += 1
    assert four_even_histogram == {3: 16, 12: 16}
    forced = {}
    for target in affine:
        rows = cliques([point for point in points if dot(point, target)], 6)
        assert len(rows) == 32 and all(vector_sum(row) == target for row in rows)
        assert all(independent(row + (127 ^ target,)) for row in rows)
        forced[target] = rows
    transfers = 0
    for even_pair, defect, charge in local_two_even:
        target = charge ^ 15
        assert target in affine and (127 ^ target) in defect
        for pure_even_defect in forced[target]:
            if set(even_pair) & set(pure_even_defect):
                continue
            reduced = tuple(point for point in defect if point != (127 ^ target))
            completed = pure_even_defect + (127 ^ target,)
            assert len(reduced) == 5 and len(completed) == 7
            assert independent(reduced) and independent(completed) and not set(reduced) & set(completed)
            assert not {127, 124, 115} & (set(reduced) | set(completed))
            transfers += 1
    assert transfers > 0
    quadruples = 0
    for characteristic in combinations(sorted(first_hole + second_hole), 2):
        if dot(*characteristic):
            continue
        for charges in combinations(sorted(set(first_hole + second_hole) - set(characteristic)), 2):
            if vector_sum(characteristic) != vector_sum(charges):
                continue
            assert set(charges).issubset(first_hole) or set(charges).issubset(second_hole)
            assert dot(*charges) == 0
            quadruples += 1
    assert quadruples == 84
    pure_odd_collision_controls = 0
    for missing in first_hole:
        for member_charge in second_hole:
            available = sorted(({missing} | set(second_hole)) - {member_charge})
            assert not any(dot(*pair) == 0 and vector_sum(pair) == (missing ^ member_charge)
                           for pair in combinations(available, 2))
            pure_odd_collision_controls += 1
    affine_overlap_controls = 0
    for first_charge in affine:
        for second_charge in sorted(set(first_hole + second_hole) - set(affine)):
            available = sorted(set(first_hole + second_hole) - set(affine) - {second_charge})
            assert not any(dot(*pair) == 0 and vector_sum(pair) == (first_charge ^ second_charge)
                           for pair in combinations(available, 2))
            affine_overlap_controls += 1
    assert pure_odd_collision_controls == 49 and affine_overlap_controls == 40
    hole_points = sorted(first_hole + second_hole)
    six_odd_subsets = [chosen for chosen in combinations(hole_points, 6)
                       if all(dot(left, right) == 0 for left, right in combinations(chosen, 2))]
    assert len(six_odd_subsets) == 14
    assert all(set(chosen).issubset(first_hole) or set(chosen).issubset(second_hole) for chosen in six_odd_subsets)
    mixed_four_odd_subsets = [chosen for chosen in combinations(hole_points, 4)
                             if set(chosen) & set(first_hole) and set(chosen) & set(second_hole)
                             and all(dot(left, right) == 0 for left, right in combinations(chosen, 2))]
    assert len(mixed_four_odd_subsets) == 14
    assert not any(all(dot(point, projection) for projection in chosen)
                   for chosen in mixed_four_odd_subsets for point in points)
    return {'status': 'two_six_defect_count_profiles_reduce_from21_to3_necessary_candidates',
            'dimension': 7, 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'characteristic_class_size_range': [3, 8], 'one_five_branch_excluded': True,
            'size_three_entire_branch_excluded': False, 'two_six_branch': 'open_three_necessary_profiles',
            'count_profiles': profiles, 'initial_count_profile_count': 21, 'written_exclusion_count': 18,
            'exclusions_by_reason': dict(Counter(item['status'] for item in profiles if item not in survivors)),
            'remaining_profiles': [item['defect_even_counts'] + item['saturated_counts'] for item in survivors],
            'remaining_profile_histogram_by_C': dict(sorted(Counter(item['saturated_counts'][2] for item in survivors).items())),
            'eight_odd_heptad_survivor': [4, 4, 7, 1, 8], 'direct_and_formula_profile_sets_equal': True,
            'local_two_even_four_odd_classes_checked': len(local_two_even), 'local_two_even_charge_histogram': dict(sorted(charge_histogram.items())),
            'local_four_even_two_odd_classes_checked': sum(four_even_histogram.values()),
            'local_four_even_charge_histogram': dict(sorted(four_even_histogram.items())),
            'forced_even_six_choices_by_sum': {target: len(rows) for target, rows in forced.items()},
            'disjoint_local_two_six_transfer_pairs_checked': transfers,
            'distinct_hole_charge_characteristic_quadruples_checked': quadruples,
            'pure_odd_member_charge_collision_controls': pure_odd_collision_controls,
            'affine_plane_member_charge_overlap_controls': affine_overlap_controls,
            'six_odd_hole_subsets_checked': len(six_odd_subsets),
            'mixed_four_odd_hole_subsets_checked': len(mixed_four_odd_subsets),
            'even_vectors_compatible_with_mixed_four_odd_holes': 0,
            'local_control_scope': 'Fixed affine odd plane or fixed odd pair, four forced even-six sums, conditional recoloring of disjoint partial class pairs, and fixed-hole quadruples; not complete colorings or all coupled six-class pairs.',
            'prior_spread_enumeration_rerun': False, 'all_six_classes_reenumerated': False,
            'native_SAT': False, 'exact_cover_search': False, 'DRAT_checked': False, 'Lean_run': False,
            'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'prior_report_sha256': bindings,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-two-six-profiles.md').read_bytes()).hexdigest(),
            'scope': 'Written exclusion of eighteen count profiles, with retained eight-spread, finite seven-spread and one-five dependencies. Three necessary profiles remain unrealized; no six-spread completion claim, numerical bound change or entire s=3 exclusion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
