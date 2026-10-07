"""Audit complete necessary 49-point roots and marked orbits for (2,6,6;7,0,8)."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum
from check_dimension_seven_three_six_charge import linear_values


def marked_group():
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    group = []
    for first_column in (1, 3):
        restriction = linear_values((first_column, 2, 4))
        dual = tuple(next(image for image in range(8)
                          if all(dot(restriction[source], image) == dot(source, value) for source in range(8)))
                     for value in range(8))
        for second_diagonal in (0, 1):
            for third_diagonal in (0, 1):
                shear = linear_values((0, second_diagonal << 1, third_diagonal << 2))
                mapping = []
                for point in range(128):
                    bits = encoded[point]
                    image_dual = dual[(bits >> 3) & 7]
                    image = restriction[bits & 7] ^ shear[image_dual]
                    mapping.append(decoded[image | image_dual << 3 | bits & 64])
                group.append(tuple(mapping))
    group_set = set(group)
    assert len(group_set) == 8 and tuple(range(128)) in group_set
    for mapping in group:
        assert len(set(mapping)) == 128 and mapping[127] == 127
        assert mapping[65] == 65 and mapping[113] == 113
        assert {mapping[95], mapping[111]} == {95, 111}
        assert all(dot(left, right) == dot(mapping[left], mapping[right])
                   for left in range(128) for right in range(128))
        for second in group:
            assert tuple(mapping[second[point]] for point in range(128)) in group_set
    return group


def catalogs(even, bitwise):
    construct = bit_cliques if bitwise else array_cliques
    sextets = construct(even, 6)
    first = [block for block in sextets if vector_sum(block) == 65 and 95 not in block and 111 not in block]
    second = [block for block in sextets if vector_sum(block) == 113 and 95 not in block and 111 not in block]
    return first, second, construct(even, 7)


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    universe = mask(even)
    prior = json.loads((root / 'results/dimension-7-two-six-six-charge.json').read_text())
    assert prior['profile'] == [2, 6, 6, 7, 0, 8]
    assert prior['normal_form']['full_marked_stabilizer_order'] == 8
    assert prior['inside_M_exclusion_uses_prior_finite_cover']
    assert prior['checker_sha256'] == digest(root / 'develop/check_dimension_seven_two_six_six_charge.py')
    assert prior['proof_note_sha256'] == digest(root / 'notes/dimension-seven-two-six-six-charge.md')
    for name, checksum in prior['dependency_sha256'].items():
        assert digest(root / name) == checksum
    bit_catalogs = catalogs(even, True)
    array_catalogs = catalogs(even, False)
    assert bit_catalogs == array_catalogs
    first, second, heptads = bit_catalogs
    assert tuple(map(len, bit_catalogs)) == (32, 22, 288)
    first_class = (95, 111, 127 ^ 48, 127 ^ 51, 127 ^ 60, 127 ^ 63)
    for block in [first_class] + first + second:
        assert all(dot(left, right) for left, right in combinations(block, 2))
    bit_roots = Counter()
    witnesses = {}
    hole_allocations = Counter()
    for left in first:
        for right in second:
            occupied = mask(left) | mask(right) | mask((95, 111))
            if occupied.bit_count() != 14:
                continue
            state = universe ^ occupied
            present = [point for point in even if state & (1 << point)]
            first_holes = set(left) & holes
            second_holes = set(right) & holes
            assert len(first_holes) <= 1 and len(second_holes) <= 1
            first_hole = next(iter(first_holes), 0)
            second_hole = next(iter(second_holes), 0)
            assert state.bit_count() == 49 and vector_sum(present) == 0
            assert set(present) & holes == holes - first_holes - second_holes
            bit_roots[state] += 1
            assert state not in witnesses
            witnesses[state] = (left, right, first_hole, second_hole)
            hole_allocations[(len(first_holes), len(second_holes))] += 1
    array_roots = Counter()
    array_witnesses = {}
    for left in array_catalogs[0]:
        for right in array_catalogs[1]:
            if any(point in right for point in left):
                continue
            present = [point for point in even if point not in left + right + (95, 111)]
            state = mask(present)
            array_roots[state] += 1
            array_witnesses[state] = (left, right, next((point for point in left if point in holes), 0),
                                      next((point for point in right if point in holes), 0))
    assert bit_roots == array_roots and witnesses == array_witnesses
    assert sum(bit_roots.values()) == len(bit_roots) == 384 and set(bit_roots.values()) == {1}
    expected_allocations = {tuple(row['hole_counts']): row['pairs']
                            for row in prior['normal_form']['pairs_by_ordered_hole_counts']}
    assert hole_allocations == expected_allocations
    group = marked_group()
    group_actions = 0
    for mapping in group:
        assert {mapping[point] for point in holes} == holes
        assert {mapping[point] for point in (3, 12, 15)} == {3, 12, 15}
        for blocks in bit_catalogs:
            assert {tuple(sorted(mapping[point] for point in block)) for block in blocks} == set(blocks)
        for state, (left, right, first_hole, second_hole) in witnesses.items():
            image = mask(mapping[point] for point in even if state & (1 << point))
            assert image in witnesses and bit_roots[image] == bit_roots[state]
            assert witnesses[image] == (tuple(sorted(mapping[point] for point in left)),
                                        tuple(sorted(mapping[point] for point in right)),
                                        mapping[first_hole], mapping[second_hole])
            group_actions += 1
    remaining = set(bit_roots)
    representatives = []
    orbit_sizes = Counter()
    allocation_orbits = Counter()
    eligible_counts = Counter()
    heptad_masks = [(block, mask(block)) for block in heptads]
    while remaining:
        representative = min(remaining)
        points = [point for point in even if representative & (1 << point)]
        orbit = {mask(mapping[point] for point in points) for mapping in group}
        assert orbit <= remaining
        remaining -= orbit
        left, right, first_hole, second_hole = witnesses[representative]
        allocation = (int(bool(first_hole)), int(bool(second_hole)))
        assert all((int(bool(witnesses[state][2])), int(bool(witnesses[state][3]))) == allocation for state in orbit)
        marked_hole_orbit = sorted({(mapping[first_hole], mapping[second_hole]) for mapping in group})
        assert {(witnesses[state][2], witnesses[state][3]) for state in orbit} == set(marked_hole_orbit)
        eligible = [block for block, block_mask in heptad_masks if block_mask & representative == block_mask]
        anchored = sum(bool(set(block) & holes) for block in eligible)
        stabilizer_size = sum(mask(mapping[point] for point in points) == representative for mapping in group)
        assert len(orbit) * stabilizer_size == 8
        representatives.append({'remaining': str(representative), 'pure_six_q1': list(left), 'pure_six_q2': list(right),
                                'actual_defect_holes': [first_hole, second_hole], 'ordered_hole_counts': list(allocation),
                                'marked_hole_orbit': marked_hole_orbit,
                                'remaining_holes': sorted(holes - {first_hole, second_hole}),
                                'orbit_size': len(orbit), 'remaining_set_stabilizer_order': stabilizer_size,
                                'ordered_root_multiplicity': bit_roots[representative],
                                'eligible_heptads': len(eligible), 'eligible_anchored_heptads': anchored,
                                'eligible_heptads_avoiding_M': len(eligible) - anchored})
        orbit_sizes[len(orbit)] += 1
        allocation_orbits[allocation] += 1
        eligible_counts[len(eligible)] += 1
    assert sum(size * count for size, count in orbit_sizes.items()) == 384
    assert set(allocation_orbits) == set(hole_allocations)
    assert Counter(len(set(block) & holes) for block in heptads) == {0: 64, 1: 224}
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'develop/check_dimension_seven_three_six_charge.py',
                    'develop/check_dimension_seven_two_six_six_charge.py',
                    'notes/dimension-seven-two-six-six-charge.md', 'results/dimension-7-two-six-six-charge.json')
    return {'status': 'complete_necessary_two_six_six_roots_and_marked_orbit_reduction',
            'dimension': 7, 'profile': prior['profile'], 'characteristic_class_size': 4,
            'catalog_counts': [32, 22, 288], 'disjoint_ordered_defect_pairs': 384,
            'ordered_roots': sum(bit_roots.values()), 'distinct_49_point_sets': len(bit_roots),
            'every_remaining_set_has_unique_ordered_defect_pair': True,
            'roots_by_ordered_hole_counts': [{'hole_counts': counts, 'roots': count} for counts, count in sorted(hole_allocations.items())],
            'full_marked_stabilizer_order': len(group), 'remaining_set_orbits': len(representatives),
            'orbit_size_histogram': dict(sorted(orbit_sizes.items())),
            'orbits_by_ordered_hole_counts': [{'hole_counts': counts, 'orbits': count} for counts, count in sorted(allocation_orbits.items())],
            'eligible_heptad_count_histogram_over_representatives': dict(sorted(eligible_counts.items())),
            'all_even_heptads': 288, 'anchored_heptads': 224, 'heptads_avoiding_M': 64,
            'orbit_representatives': representatives,
            'root_multiset_sha256': hashlib.sha256(json.dumps(sorted(bit_roots.items()), separators=(',', ':')).encode()).hexdigest(),
            'root_group_actions_checked': group_actions, 'symplectic_dot_checks': len(group) * 128**2,
            'composition_point_checks': len(group)**2 * 128,
            'array_and_bitmask_catalogs_complete_roots_and_witnesses_equal': True,
            'all_catalog_actions_and_intrinsic_defect_roles_checked': True,
            'all_actual_defect_holes_transported_and_retained': True,
            'orbit_stabilizer_identities_checked': True, 'complete_necessary_roots_constructed': True,
            'new_cover_search': False, 'new_finite_cover_certificate': False, 'target_profile_excluded': False,
            'nineteen_color_witness': False, 'remaining_raw_profiles': prior['remaining_raw_profiles'],
            'remaining_profile_lists_unchanged': True, 'exact_n7': 'open_lower_bound19',
            'inside_M_exclusion_inherits_prior_finite_cover': True, 'historical_cover_audit_rerun': False,
            'new_cover_certificate_used_for_outside_case': False, 'prior_spread_enumeration_rerun': False,
            'Lean_run': False, 'independent_Pro_review': False, 'manuscript_PDFs_changed': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-two-six-six-roots.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Complete necessary 49-point sets and order-eight marked orbits; actual defect holes retained and all 288 heptads allowed. No covering search, exclusion or full coloring; 25/39 totals unchanged, exact n7 open >=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
