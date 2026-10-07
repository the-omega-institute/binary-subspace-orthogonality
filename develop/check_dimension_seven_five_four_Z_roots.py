"""Audit complete necessary Z roots and the written 128-element marked stabilizer."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time


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


def cliques(candidates, size, bitwise):
    blocks = []
    neighbors = {point: mask(other for other in candidates if other > point and dot(point, other))
                 for point in candidates}

    def bit_visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            bit_visit(chosen + (point,), available & neighbors[point])

    def array_visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        for index, point in enumerate(available):
            array_visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    if bitwise:
        bit_visit((), mask(candidates))
    else:
        array_visit((), candidates)
    return blocks


def catalogs(points, holes, bitwise):
    five = [block for block in cliques(points, 5, bitwise)
            if vector_sum(block) == 0 and len(set(block) & holes) == 1]
    four = [block for block in cliques([point for point in points if dot(point, 15) and dot(point, 48)], 4, bitwise)
            if vector_sum(block) == 15]
    mixed_left = cliques([point for point in points if dot(point, 3)], 6, bitwise)
    mixed_right = cliques([point for point in points if dot(point, 12)], 6, bitwise)
    return five, four, mixed_left, mixed_right, cliques(points, 7, bitwise)


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    started = time.monotonic()

    def budget():
        if time.monotonic() - started > 90:
            raise RuntimeError('Bounded Z root audit exhausted; no complete report written.')

    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    basis = (3, 12, 48, 65, 71, 95)
    assert all(dot(left, right) == (abs(left_index - right_index) == 3)
               for left_index, left in enumerate(basis) for right_index, right in enumerate(basis))
    bit_catalogs = catalogs(points, holes, True)
    array_catalogs = catalogs(points, holes, False)
    assert bit_catalogs == array_catalogs
    five, four, mixed_left, mixed_right, heptads = bit_catalogs
    assert tuple(map(len, bit_catalogs)) == (1120, 16, 32, 32, 288)
    assert all(vector_sum(block) == projection for blocks, projection
               in ((mixed_left, 3), (mixed_right, 12)) for block in blocks)
    assert all(not set(block) & holes for block in four + mixed_left + mixed_right)
    for blocks, odd_members in ((five, ()), (four, (112, 79)),
                               (mixed_left, (124,)), (mixed_right, (115,))):
        assert all(all(dot(left, right) for left, right in combinations(block + odd_members, 2))
                   for block in blocks)
    universe = mask(points)
    hole_mask = mask(holes)
    defect_histogram = Counter()
    ordered_histogram = Counter()
    bit_roots = Counter()
    four_masks = [mask(block) for block in four]
    left_masks = [mask(block) for block in mixed_left]
    right_masks = [mask(block) for block in mixed_right]
    for first in five:
        budget()
        hole = next(iter(set(first) & holes))
        first_mask = mask(first)
        for second_mask in four_masks:
            if first_mask & second_mask:
                continue
            defect_mask = first_mask | second_mask
            defect_histogram[hole] += 1
            for left_mask in left_masks:
                if left_mask & defect_mask:
                    continue
                occupied = defect_mask | left_mask
                for right_mask in right_masks:
                    if right_mask & occupied:
                        continue
                    remaining = universe ^ (occupied | right_mask)
                    assert remaining.bit_count() == 42
                    assert remaining & hole_mask == mask(holes - {hole})
                    bit_roots[remaining] += 1
                    ordered_histogram[hole] += 1
        if len(bit_roots) > 2000000:
            raise RuntimeError('Z distinct-root memory budget exhausted; no complete report written.')
    assert sum(defect_histogram.values()) == 13584
    mixed_pairs = [set(left + right) for left in array_catalogs[2] for right in array_catalogs[3]
                   if not set(left) & set(right)]
    array_roots = Counter()
    for first in array_catalogs[0]:
        budget()
        for second in array_catalogs[1]:
            if set(first) & set(second):
                continue
            defect = set(first + second)
            for mixed in mixed_pairs:
                if not defect & mixed:
                    array_roots[mask(set(points) - defect - mixed)] += 1
    assert array_roots == bit_roots
    del array_roots
    coordinates = {vector_sum(vector for index, vector in enumerate(basis) if bits & (1 << index)): bits
                   for bits in range(64)}
    assert set(coordinates) == set(points) | {0}
    transformations = []
    positions = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    for exchange in range(2):
        for parameters in range(64):
            symmetric_rows = [0, 0, 0]
            for index, (row, column) in enumerate(positions):
                if parameters & (1 << index):
                    symmetric_rows[row] ^= 1 << column
                    if row != column:
                        symmetric_rows[column] ^= 1 << row
            permutation = {}
            for point, bits in coordinates.items():
                if exchange:
                    bits ^= (((bits >> 0) ^ (bits >> 1)) & 1) * 3
                    bits ^= (((bits >> 3) ^ (bits >> 4)) & 1) * 24
                dual_bits = bits >> 3
                translated = bits ^ sum(((symmetric_rows[index] & dual_bits).bit_count() % 2) << index
                                        for index in range(3))
                permutation[point] = vector_sum(vector for index, vector in enumerate(basis) if translated & (1 << index))
            assert set(permutation.values()) == set(coordinates)
            assert permutation[15] == 15 and permutation[48] == 48
            assert {permutation[3], permutation[12]} == {3, 12}
            assert {permutation[point] for point in (51, 60, 63)} == {51, 60, 63}
            assert all(dot(left, right) == dot(permutation[left], permutation[right])
                       for left in coordinates for right in coordinates)
            transformations.append(permutation)
    signatures = {tuple(permutation[point] for point in sorted(coordinates)) for permutation in transformations}
    assert len(signatures) == 128
    for left in transformations:
        budget()
        for right in transformations:
            assert tuple(left[right[point]] for point in sorted(coordinates)) in signatures
    for permutation in transformations:
        for index, blocks in enumerate(bit_catalogs):
            target = 5 - index if index in (2, 3) and permutation[3] == 12 else index
            assert {tuple(sorted(permutation[point] for point in block)) for block in blocks} == set(bit_catalogs[target])
    representatives = []
    orbit_histogram = Counter()
    orbit_hole_histogram = Counter()
    unseen = set(bit_roots)
    for representative in sorted(bit_roots):
        if representative not in unseen:
            continue
        budget()
        occupied_points = [point for point in points if not representative & (1 << point)]
        orbit = {universe ^ mask(permutation[point] for point in occupied_points) for permutation in transformations}
        assert orbit <= unseen
        assert len({bit_roots[state] for state in orbit}) == 1
        hole = next(iter(holes & set(occupied_points)))
        hole_orbit = sorted({permutation[hole] for permutation in transformations})
        assert all((hole_mask ^ (state & hole_mask)).bit_count() == 1 for state in orbit)
        assert {point for point in holes if any(not state & (1 << point) for state in orbit)} == set(hole_orbit)
        unseen -= orbit
        representatives.append({'remaining': str(representative), 'hole': hole, 'hole_orbit': hole_orbit,
                                'orbit_size': len(orbit), 'ordered_root_multiplicity': bit_roots[representative]})
        orbit_histogram[len(orbit)] += 1
        orbit_hole_histogram[tuple(hole_orbit)] += 1
    assert not unseen
    assert sum(size * count for size, count in orbit_histogram.items()) == len(bit_roots)
    rows = [block for block in heptads if len(set(block) & holes) == 1]
    assert len(rows) == 224
    assert all(sum(hole not in block for block in rows) == 192 for hole in holes)
    return {
        'status': 'Z_complete_necessary_roots_and_proved_128_element_marked_stabilizer_reduction',
        'dimension': 7, 'profile': [5, 4, 6, 2, 8], 'normal_form': 'Z',
        'five_even_sum': 0, 'four_even_sum': 15, 'D6_odd_projections': [15, 48],
        'mixed_odd_projections': [3, 12], 'characteristic_projections': [51, 60, 63],
        'characteristic_charge': 48, 'symplectic_basis': list(basis),
        'catalog_counts': [len(blocks) for blocks in bit_catalogs],
        'two_independent_catalog_and_root_constructions_agree': True,
        'disjoint_defect_pairs': sum(defect_histogram.values()),
        'defect_pairs_by_actual_pure_five_hole': dict(sorted(defect_histogram.items())),
        'disjoint_ordered_mixed_pairs': len(mixed_pairs),
        'ordered_roots': sum(bit_roots.values()), 'distinct_root_sets': len(bit_roots),
        'ordered_roots_by_actual_pure_five_hole': dict(sorted(ordered_histogram.items())),
        'marked_stabilizer_order': 128, 'pointwise_hole_subgroup_order': 64,
        'symplectic_dot_checks': 128 * 64 * 64, 'closure_point_checks': 128 * 128 * 64,
        'remaining_root_orbits': len(representatives),
        'orbit_size_histogram': dict(sorted(orbit_histogram.items())),
        'orbits_by_hole_orbit': {','.join(map(str, holes)): count for holes, count in sorted(orbit_hole_histogram.items())},
        'orbit_representatives': representatives,
        'root_multiset_sha256': hashlib.sha256(json.dumps(sorted(bit_roots.items()), separators=(',', ':')).encode()).hexdigest(),
        'eligible_anchored_heptads': 224, 'eligible_rows_avoiding_each_hole': 192,
        'new_cover_search': False, 'new_cover_certificate': False, 'Z_excluded': False,
        'remaining_normal_forms': ['Z'], 'raw_profile_excluded': False,
        'remaining_raw_profiles': {'five_six': 27, 'three_six': 39},
        'exact_n7': 'open_lower_bound19', 'new_Lean': False, 'new_independent_Pro_review': False,
        'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
        'execution_budget': {'seconds': 90, 'max_distinct_roots': 2000000},
        'checker_sha256': digest(Path(__file__)),
        'note_sha256': digest(root / 'notes/dimension-seven-five-four-Z-roots.md'),
        'dependency_sha256': {name: digest(root / name) for name in (
            'notes/dimension-seven-five-four-charge.md', 'results/dimension-7-five-four-charge.json',
            'notes/dimension-seven-nineteen-obstruction.md')},
        'scope': 'Complete necessary Z roots and exact orbit partition under the written marked stabilizer, including mixed-class exchange and transported actual hole. No covering problem solved; no profile exclusion.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')
