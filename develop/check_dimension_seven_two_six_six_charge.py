"""Audit the (2,6,6;7,0,8) charge reduction and local marked geometry."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import (
    array_cliques, bit_cliques, digest, dot, vector_sum,
)
from check_dimension_seven_three_six_charge import linear_values


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    holes = set(linear_values(basis[:3])) - {0}
    even_pair = (95, 111)
    affine = (48, 51, 60, 63)
    first_class = tuple(sorted(even_pair + tuple(127 ^ point for point in affine)))
    sums = (65, 113)
    sextets = bit_cliques(even, 6)
    heptads = bit_cliques(even, 7)
    assert sextets == array_cliques(even, 6)
    assert heptads == array_cliques(even, 7)
    unanchored = [block for block in sextets if not set(block) & holes]
    by_sum = {total: [block for block in sextets if vector_sum(block) == total] for total in even}
    unanchored_by_sum = {total: [block for block in unanchored if vector_sum(block) == total] for total in even}
    assert len(unanchored) == 672
    assert all(len(by_sum[total]) == 32 for total in even)
    assert all(len(unanchored_by_sum[total]) == (32 if total in holes else 8) for total in even)
    assert all(vector_sum(block) not in block and all(dot(vector_sum(block), point) for point in block)
               for block in sextets)
    assert all(dot(left, right) for left, right in combinations(first_class, 2))
    catalogs = [[block for block in by_sum[total] if not set(block) & set(even_pair)] for total in sums]
    pairs = [(left, right) for left in catalogs[0] for right in catalogs[1] if not set(left) & set(right)]
    assert pairs == [(left, right) for left in catalogs[0] for right in catalogs[1]
                     if all(point not in right for point in left)]
    hole_allocations = Counter((len(set(left) & holes), len(set(right) & holes)) for left, right in pairs)
    assert [len(blocks) for blocks in catalogs] == [32, 22] and len(pairs) == 384
    assert hole_allocations == {(0, 0): 16, (0, 1): 88, (1, 0): 64, (1, 1): 216}
    inside_controls = 0
    inside_pairs = []
    for lower in sorted(holes):
        upper = lower ^ 48
        if upper not in holes or dot(lower, 95) or not dot(upper, 95):
            continue
        count = 0
        for left in by_sum[lower]:
            for right in by_sum[upper]:
                if set(even_pair) & (set(left) | set(right)) or set(left) & set(right):
                    continue
                moved = 127 ^ upper
                reduced = tuple(point for point in first_class if point != moved)
                enlarged = right + (moved,)
                assert len(reduced) == 5 and sum(not dot(point, 127) for point in reduced) == 2
                assert len(enlarged) == 7 and sum(not dot(point, 127) for point in enlarged) == 6
                assert all(dot(first, second) for block in (reduced, enlarged, left)
                           for first, second in combinations(block, 2))
                assert not set(reduced) & set(enlarged) and not set(left) & (set(reduced) | set(enlarged))
                assert set(reduced) | set(enlarged) | set(left) == set(first_class) | set(left) | set(right)
                count += 1
                inside_controls += 1
        inside_pairs.append({'sums': [lower, upper], 'compatible_disjoint_pairs': count})
    assert len(inside_pairs) == 3

    matrices = [linear_values(columns) for columns in permutations(range(1, 8), 3)
                if len(set(linear_values(columns))) == 8]
    symmetric = []
    for bits in range(64):
        entries = [(bits >> index) & 1 for index in range(6)]
        first, second, third, first_second, first_third, second_third = entries
        symmetric.append(linear_values((first | first_second << 1 | first_third << 2,
                                       first_second | second << 1 | second_third << 2,
                                       first_third | second_third << 1 | third << 2)))
    assert len(matrices) == 168 and len(set(symmetric)) == 64
    controls = Counter()
    group = []
    restrictions = set()
    inverse_classes = 0
    gram_checks = 0
    for matrix in matrices:
        dual = tuple(next(destination for destination in range(8)
                          if all(dot(matrix[1 << index], destination) == ((source >> index) & 1)
                                 for index in range(3))) for source in range(8))
        for shear in symmetric:
            mapping = tuple(decoded[matrix[bits & 7] ^ shear[dual[(bits >> 3) & 7]]
                                    | dual[(bits >> 3) & 7] << 3 | bits & 64]
                            for bits in range(128))
            by_point = tuple(mapping[encoded[point]] for point in range(128))
            assert len(set(by_point)) == 128 and by_point[127] == 127
            assert all(dot(left, right) == dot(by_point[left], by_point[right]) for left in basis for right in basis)
            gram_checks += 49
            source_pair = tuple(sorted(by_point[point] for point in even_pair))
            source_sum = by_point[sums[0]]
            key = (source_pair, source_sum)
            if not controls[key]:
                projected = {by_point[point] for point in affine}
                charge = vector_sum(source_pair)
                characteristic = holes - projected
                assert charge in projected and vector_sum(characteristic) == 0
                assert projected == {point for point in holes if dot(source_pair[0], point)}
                assert all(dot(source_pair[0], point) == dot(source_pair[1], point) for point in holes)
                assert source_sum not in holes and not dot(charge, source_sum)
                assert not dot(source_pair[0], source_sum) and not dot(source_pair[1], source_sum)
                assert by_point[sums[1]] == source_sum ^ charge
                for block in [first_class] + catalogs[0] + catalogs[1]:
                    original = tuple(by_point[point] for point in block)
                    assert all(dot(left, right) for left, right in combinations(original, 2))
                    inverse_classes += 1
            controls[key] += 1
            if source_pair == even_pair and source_sum == sums[0]:
                assert by_point[sums[1]] == sums[1]
                assert {by_point[point] for point in affine} == set(affine)
                assert all(dot(left, right) == dot(by_point[left], by_point[right])
                           for left in range(128) for right in range(128))
                for blocks in catalogs + [heptads]:
                    assert {tuple(sorted(by_point[point] for point in block)) for block in blocks} == set(blocks)
                assert {(tuple(sorted(by_point[point] for point in left)),
                         tuple(sorted(by_point[point] for point in right))) for left, right in pairs} == set(pairs)
                restrictions.add(tuple(by_point[point] for point in sorted(holes)))
                group.append(by_point)
    all_first = []
    expected = set()
    for pair in combinations(even, 2):
        if not dot(*pair):
            continue
        function = tuple(dot(pair[0], point) for point in sorted(holes))
        if not any(function) or function != tuple(dot(pair[1], point) for point in sorted(holes)):
            continue
        projected = {point for point in holes if dot(pair[0], point)}
        assert len(projected) == 4 and vector_sum(projected) == 0
        original = pair + tuple(127 ^ point for point in projected)
        assert all(dot(left, right) for left, right in combinations(original, 2))
        charge = vector_sum(pair)
        assert charge in projected
        all_first.append(pair)
        for total in even:
            if total not in holes and not dot(total, charge) and not dot(total, pair[0]):
                assert not dot(total, pair[1])
                expected.add((pair, total))
    assert len(all_first) == 112 and len(expected) == 1344
    assert set(controls) == expected and set(controls.values()) == {8}
    group_set = set(group)
    assert len(group_set) == 8 and len(restrictions) == 2 and tuple(range(128)) in group_set
    assert all(tuple(first[second[point]] for point in range(128)) in group_set
               for first in group for second in group)
    prior = json.loads((root / 'results/dimension-7-three-six-cover-check.json').read_text())
    inherited = json.loads((root / 'results/dimension-7-five-six-cover.json').read_text())
    assert inherited['cover_excluded_profile'] == [2, 6, 7, 1, 8]
    assert inherited['existing_finite_cover_certificate_used']
    bindings = {'certificate_sha256': 'results/dimension-7-hole-cover-proof.json',
                'checker_sha256': 'develop/check_dimension_seven_five_six_cover.py',
                'proof_note_sha256': 'notes/dimension-seven-five-six-cover.md'}
    for key, name in bindings.items():
        assert inherited[key] == digest(root / name)
    for name, checksum in inherited['dependency_sha256'].items():
        assert digest(root / name) == checksum
    profile = [2, 6, 6, 7, 0, 8]
    assert prior['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 39}
    assert profile in prior['remaining_raw_profile_lists']['three_six']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'develop/check_dimension_seven_three_six_charge.py',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-two-six-profiles.md',
                    'notes/dimension-seven-five-six-affine.md', 'notes/dimension-seven-five-six-cover.md',
                    'results/dimension-7-five-six-cover.json', 'results/dimension-7-three-six-cover-check.json')
    return {'status': 'two_six_six_profile_reduced_to_one_necessary_outside_charge_form',
            'dimension': 7, 'profile': profile, 'profile_columns': ['m6_1', 'm6_2', 'm6_3', 'A', 'B', 'C'],
            'characteristic_class_size': 4, 'target_profile_excluded': False, 'target_profile_realized': False,
            'normal_form': {'M_nonzero': sorted(holes), 'even_pair': even_pair, 'odd_projections': affine,
                            'characteristic_projections': [3, 12, 15], 'charge_r': 48, 'pure_six_sums': sums,
                            'unfiltered_sextets_per_sum': [len(by_sum[total]) for total in sums],
                            'sextets_avoiding_even_pair_per_sum': [len(blocks) for blocks in catalogs],
                            'disjoint_ordered_pure_defect_pairs': len(pairs),
                            'pairs_by_ordered_hole_counts': [{'hole_counts': counts, 'pairs': count}
                                                            for counts, count in sorted(hole_allocations.items())],
                            'full_marked_stabilizer_order': len(group), 'marked_M_restrictions': len(restrictions),
                            'pure_six_roles_fixed_individually': True},
            'unanchored_even_sextets': len(unanchored), 'even_heptads': len(heptads),
            'array_and_bitmask_catalogs_equal': True, 'inside_M_recoloring_cases': inside_pairs,
            'inside_M_original_recoloring_controls': inside_controls,
            'inside_M_exclusion_uses_prior_finite_cover': True,
            'inherited_cover_hash_bindings_verified': True, 'historical_cover_audit_rerun': False,
            'fixed_M_first_classes': len(all_first), 'outside_charge_normalization_controls': len(controls),
            'normalizing_isometries': sum(controls.values()), 'source_Gram_entries_checked': gram_checks,
            'original_class_image_controls': inverse_classes, 'stabilizer_dot_product_pairs_checked': len(group) * 128**2,
            'stabilizer_composition_points_checked': len(group)**2 * 128,
            'all_catalog_and_disjoint_pair_actions_checked': True,
            'remaining_raw_profiles': prior['remaining_raw_profiles'],
            'remaining_raw_profile_lists': prior['remaining_raw_profile_lists'],
            'exact_n7_chromatic_number': 'open', 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'complete_necessary_roots_constructed': False, 'new_cover_search': False,
            'new_finite_cover_certificate': False, 'new_numerical_lower_bound': False,
            'prior_spread_enumeration_rerun': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_PDFs_changed': False, 'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-two-six-six-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
