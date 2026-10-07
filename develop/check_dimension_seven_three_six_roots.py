"""Audit complete necessary roots and marked orbits for the (3,6;6,2,8) profile."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum
from check_dimension_seven_three_six_charge import linear_values


def local_catalogs(even, holes, odd_pair, mixed_pair, triple_sum, pure_sum, bitwise):
    construct = bit_cliques if bitwise else array_cliques
    triples = [block for block in construct([point for point in even
                                             if all(dot(point, odd) for odd in odd_pair)], 3)
               if vector_sum(block) == triple_sum]
    pure = [block for block in construct(even, 6)
            if vector_sum(block) == pure_sum and len(set(block) & holes) == 1]
    mixed = [construct([point for point in even if dot(point, odd)], 6) for odd in mixed_pair]
    heptads = construct(even, 7)
    return triples, pure, mixed[0], mixed[1], heptads


def marked_group(odd_pair, mixed_pair, triple_sum, expected_order):
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    assert len(encoded) == 128
    restrictions = []
    for columns in permutations(range(1, 8), 3):
        matrix = linear_values(columns)
        if len(set(matrix)) != 8:
            continue
        if {decoded[matrix[encoded[point]]] for point in odd_pair} != set(odd_pair):
            continue
        if {decoded[matrix[encoded[point]]] for point in mixed_pair} != set(mixed_pair):
            continue
        restrictions.append(matrix)
    shears = []
    positions = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    functional = encoded[triple_sum] >> 3
    assert encoded[triple_sum] & 7 == 0
    for parameters in range(64):
        rows = [0, 0, 0]
        for index, (row, column) in enumerate(positions):
            if parameters & (1 << index):
                rows[row] ^= 1 << column
                if row != column:
                    rows[column] ^= 1 << row
        action = tuple(sum(dot(row, source) << index for index, row in enumerate(rows)) for source in range(8))
        if action[functional] == 0:
            shears.append(action)
    assert len(restrictions) == expected_order // 8 and len(shears) == 8
    group = []
    for matrix in restrictions:
        dual = tuple(next(image for image in range(8)
                          if all(dot(matrix[source], image) == dot(source, value) for source in range(8)))
                     for value in range(8))
        assert dual[functional] == functional
        for shear in shears:
            mapping = []
            for point in range(128):
                bits = encoded[point]
                image_dual = dual[(bits >> 3) & 7]
                image = matrix[bits & 7] ^ shear[image_dual]
                mapping.append(decoded[image | image_dual << 3 | bits & 64])
            group.append(tuple(mapping))
    group_set = set(group)
    assert len(group_set) == expected_order and tuple(range(128)) in group_set
    for mapping in group:
        assert len(set(mapping)) == 128 and mapping[127] == 127 and mapping[triple_sum] == triple_sum
        assert all(dot(left, right) == dot(mapping[left], mapping[right])
                   for left in range(128) for right in range(128))
        for second in group:
            assert tuple(mapping[second[point]] for point in range(128)) in group_set
    return group


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    universe = mask(even)
    hole_mask = mask(holes)
    prior = json.loads((root / 'results/dimension-7-three-six-charge.json').read_text())
    assert prior['profile'] == [3, 6, 6, 2, 8]
    results = []
    for previous in prior['normal_forms']:
        name = previous['case']
        odd_pair = tuple(previous['five_odd_projections'])
        mixed_pair = tuple(previous['mixed_odd_projections'])
        triple_sum = previous['three_even_sum']
        pure_sum = previous['pure_six_sum']
        catalogs = local_catalogs(even, holes, odd_pair, mixed_pair, triple_sum, pure_sum, True)
        arrays = local_catalogs(even, holes, odd_pair, mixed_pair, triple_sum, pure_sum, False)
        assert catalogs == arrays
        triples, pure, mixed_left, mixed_right, heptads = catalogs
        assert tuple(map(len, catalogs)) == (4, 24, 32, 32, 288)
        for blocks, projections in ((triples, odd_pair), (pure, ()),
                                    (mixed_left, (mixed_pair[0],)), (mixed_right, (mixed_pair[1],))):
            for block in blocks:
                original = block + tuple(127 ^ projection for projection in projections)
                assert len(set(original)) == len(original)
                assert all(dot(left, right) for left, right in combinations(original, 2))
        assert all(not set(block) & holes for block in triples + mixed_left + mixed_right)
        assert all(vector_sum(block) == projection for blocks, projection
                   in ((mixed_left, mixed_pair[0]), (mixed_right, mixed_pair[1])) for block in blocks)
        bit_roots = Counter()
        defect_histogram = Counter()
        root_histogram = Counter()
        distinct_histogram = Counter()
        mixed_pair_count = sum(not mask(left) & mask(right) for left in mixed_left for right in mixed_right)
        for first in triples:
            for second in pure:
                occupied_defects = mask(first) | mask(second)
                if occupied_defects.bit_count() != 9:
                    continue
                hole = next(iter(set(second) & holes))
                defect_histogram[hole] += 1
                for left in mixed_left:
                    left_mask = mask(left)
                    if left_mask & occupied_defects:
                        continue
                    occupied = occupied_defects | left_mask
                    for right in mixed_right:
                        right_mask = mask(right)
                        if right_mask & occupied:
                            continue
                        remaining = universe ^ (occupied | right_mask)
                        assert remaining.bit_count() == 42
                        assert remaining & hole_mask == mask(holes - {hole})
                        assert vector_sum(point for point in even if remaining & (1 << point)) == 0
                        bit_roots[remaining] += 1
                        root_histogram[hole] += 1
        assert sum(defect_histogram.values()) == previous['disjoint_defect_pairs']
        array_roots = Counter()
        for first in arrays[0]:
            for second in arrays[1]:
                if set(first) & set(second):
                    continue
                for left in arrays[2]:
                    if any(point in first or point in second for point in left):
                        continue
                    for right in arrays[3]:
                        if any(point in first or point in second or point in left for point in right):
                            continue
                        remaining_points = [point for point in even if point not in first + second + left + right]
                        array_roots[mask(remaining_points)] += 1
        assert bit_roots == array_roots and bit_roots
        group = marked_group(odd_pair, mixed_pair, triple_sum, previous['full_marked_stabilizer_order'])
        for mapping in group:
            assert mapping[pure_sum] == pure_sum
            assert {mapping[point] for point in holes} == holes
            assert {mapping[point] for point in previous['characteristic_projections']} == set(previous['characteristic_projections'])
            for blocks in (triples, pure, heptads):
                assert {tuple(sorted(mapping[point] for point in block)) for block in blocks} == set(blocks)
            for index, blocks in enumerate((mixed_left, mixed_right)):
                destination = mixed_pair.index(mapping[mixed_pair[index]])
                assert {tuple(sorted(mapping[point] for point in block)) for block in blocks} == set((mixed_left, mixed_right)[destination])
        expected_hole_orbits = {tuple(orbit) for orbit in previous['actual_hole_orbits']}
        actual_hole_orbits = {tuple(sorted({mapping[point] for mapping in group}))
                             for point in previous['possible_pure_six_holes']}
        assert actual_hole_orbits == expected_hole_orbits
        representatives = []
        orbit_histogram = Counter()
        orbit_hole_histogram = Counter()
        for state in bit_roots:
            hole = next(iter(holes - {point for point in holes if state & (1 << point)}))
            distinct_histogram[hole] += 1
        remaining_roots = set(bit_roots)
        while remaining_roots:
            representative = min(remaining_roots)
            present = [point for point in even if representative & (1 << point)]
            hole = next(iter(holes - set(present)))
            hole_orbit = tuple(sorted({mapping[hole] for mapping in group}))
            orbit = {mask(mapping[point] for point in present) for mapping in group}
            assert orbit <= remaining_roots
            assert len({bit_roots[state] for state in orbit}) == 1
            assert {next(iter(holes - {point for point in holes if state & (1 << point)})) for state in orbit} == set(hole_orbit)
            remaining_roots -= orbit
            representatives.append({'remaining': str(representative), 'hole': hole, 'hole_orbit': list(hole_orbit),
                                    'orbit_size': len(orbit), 'ordered_root_multiplicity': bit_roots[representative]})
            orbit_histogram[len(orbit)] += 1
            orbit_hole_histogram[','.join(map(str, hole_orbit))] += 1
        assert set(root_histogram) == set(previous['possible_pure_six_holes'])
        assert {tuple(row['hole_orbit']) for row in representatives} == expected_hole_orbits
        assert sum(size * count for size, count in orbit_histogram.items()) == len(bit_roots)
        assert sum(row['orbit_size'] * row['ordered_root_multiplicity'] for row in representatives) == sum(bit_roots.values())
        anchored = [block for block in heptads if len(set(block) & holes) == 1]
        assert len(anchored) == 224
        assert all(sum(hole not in block for block in anchored) == 192 for hole in holes)
        results.append({'case': name, 'five_odd_projections': list(odd_pair), 'mixed_odd_projections': list(mixed_pair),
                        'three_even_sum': triple_sum, 'pure_six_sum': pure_sum,
                        'catalog_counts': list(map(len, catalogs)), 'disjoint_defect_pairs': sum(defect_histogram.values()),
                        'disjoint_ordered_mixed_pairs': mixed_pair_count,
                        'defect_pairs_by_actual_pure_six_hole': dict(sorted(defect_histogram.items())),
                        'ordered_roots': sum(bit_roots.values()), 'distinct_root_sets': len(bit_roots),
                        'ordered_roots_by_actual_pure_six_hole': dict(sorted(root_histogram.items())),
                        'distinct_sets_by_actual_pure_six_hole': dict(sorted(distinct_histogram.items())),
                        'full_marked_stabilizer_order': len(group), 'actual_hole_orbits': sorted(actual_hole_orbits),
                        'remaining_root_orbits': len(representatives), 'orbit_size_histogram': dict(sorted(orbit_histogram.items())),
                        'orbits_by_actual_hole_orbit': dict(sorted(orbit_hole_histogram.items())),
                        'orbit_representatives': representatives,
                        'root_multiset_sha256': hashlib.sha256(json.dumps(sorted(bit_roots.items()), separators=(',', ':')).encode()).hexdigest(),
                        'symplectic_dot_checks': len(group) * 128 * 128,
                        'composition_point_checks': len(group) * len(group) * 128,
                        'eligible_anchored_heptads': len(anchored), 'rows_avoiding_each_actual_hole': 192,
                        'all_catalog_and_mixed_role_actions_checked': True, 'root_multiplicity_invariant': True,
                        'array_and_bitmask_catalogs_and_complete_root_multisets_equal': True,
                        'cover_feasibility': 'untested', 'normal_form_excluded': False})
    return {'status': 'complete_necessary_three_six_roots_and_proved_marked_orbit_reduction',
            'dimension': 7, 'profile': prior['profile'], 'characteristic_class_size': 4, 'normal_forms': results,
            'complete_necessary_roots_constructed': True, 'all_actual_pure_six_holes_and_both_mixed_roles_retained': True,
            'new_cover_search': False, 'new_finite_cover_certificate': False, 'target_profile_excluded': False,
            'nineteen_color_witness': False, 'remaining_raw_profiles': prior['remaining_raw_profiles'],
            'remaining_profile_lists_unchanged': True, 'exact_n7': 'open_lower_bound19',
            'Lean_run': False, 'independent_Pro_review': False,
            'prior_cover_certificates_used_as_new_proof_inputs': False, 'prior_spread_enumeration_rerun': False,
            'manuscript_PDFs_changed': False, 'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-three-six-roots.md'),
            'dependency_sha256': {name: digest(root / name) for name in (
                'develop/check_dimension_seven_five_four_charge.py', 'develop/check_dimension_seven_three_six_charge.py',
                'notes/dimension-seven-three-six-charge.md', 'results/dimension-7-three-six-charge.json')},
            'scope': 'Complete necessary roots and full marked-group orbit partitions for all three forms; no covering search, exclusion or full coloring. Actual hole transported, both mixed roles and both hole orbits retained; 26/39 totals unchanged, exact n7 open >=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
