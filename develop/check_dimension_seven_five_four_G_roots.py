"""Check the G-form mixed-class roots and pointwise-hole stabilizer orbits."""
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
            if vector_sum(block) == 12 and len(set(block) & holes) == 1]
    four = [block for block in cliques([point for point in points if dot(point, 3) and dot(point, 48)], 4, bitwise)
            if vector_sum(block) == 3]
    mixed_left = cliques([point for point in points if dot(point, 51)], 6, bitwise)
    mixed_right = cliques([point for point in points if dot(point, 60)], 6, bitwise)
    heptads = cliques(points, 7, bitwise)
    return five, four, mixed_left, mixed_right, heptads


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
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
    assert tuple(map(len, bit_catalogs)) == (96, 16, 32, 32, 288)
    assert all(vector_sum(block) == projection for blocks, projection
               in ((mixed_left, 51), (mixed_right, 60)) for block in blocks)
    assert all(not set(block) & holes for block in four + mixed_left + mixed_right)
    for blocks, odd_members in ((five, ()), (four, (124, 79)),
                               (mixed_left, (76,)), (mixed_right, (67,))):
        assert all(all(dot(left, right) for left, right in combinations(block + odd_members, 2))
                   for block in blocks)
    universe = mask(points)
    hole_mask = mask(holes)
    defect_histogram = Counter()
    ordered_histogram = Counter()
    bit_roots = Counter()
    for first in five:
        hole = next(iter(set(first) & holes))
        assert hole != 12
        first_mask = mask(first)
        for second in four:
            defect_mask = first_mask | mask(second)
            if defect_mask.bit_count() != 9:
                continue
            defect_histogram[hole] += 1
            for left in mixed_left:
                left_mask = mask(left)
                if left_mask & defect_mask:
                    continue
                occupied = defect_mask | left_mask
                for right in mixed_right:
                    right_mask = mask(right)
                    if right_mask & occupied:
                        continue
                    remaining = universe ^ (occupied | right_mask)
                    assert remaining.bit_count() == 42
                    assert remaining & hole_mask == mask(holes - {hole})
                    bit_roots[remaining] += 1
                    ordered_histogram[hole] += 1
    assert sum(defect_histogram.values()) == 1088
    array_roots = Counter()
    for first in array_catalogs[0]:
        for second in array_catalogs[1]:
            if set(first) & set(second):
                continue
            for left in array_catalogs[2]:
                if set(left) & set(first + second):
                    continue
                for right in array_catalogs[3]:
                    if set(right) & set(first + second + left):
                        continue
                    remaining_points = set(points) - set(first + second + left + right)
                    array_roots[mask(remaining_points)] += 1
    assert array_roots == bit_roots
    coordinates = {vector_sum(vector for index, vector in enumerate(basis) if bits & (1 << index)): bits
                   for bits in range(64)}
    assert set(coordinates) == set(points) | {0}
    transformations = []
    positions = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    for parameters in range(64):
        symmetric_rows = [0, 0, 0]
        for index, (row, column) in enumerate(positions):
            if parameters & (1 << index):
                symmetric_rows[row] ^= 1 << column
                if row != column:
                    symmetric_rows[column] ^= 1 << row
        permutation = {}
        for point, bits in coordinates.items():
            dual_bits = bits >> 3
            translated = bits ^ sum(((symmetric_rows[index] & dual_bits).bit_count() % 2) << index
                                    for index in range(3))
            image = vector_sum(vector for index, vector in enumerate(basis) if translated & (1 << index))
            permutation[point] = image
        assert set(permutation.values()) == set(coordinates)
        assert all(permutation[point] == point for point in holes | {0})
        assert all(permutation[permutation[point]] == point for point in coordinates)
        assert all(dot(left, right) == dot(permutation[left], permutation[right])
                   for left in coordinates for right in coordinates)
        transformations.append(permutation)
    assert len({tuple(sorted(permutation.items())) for permutation in transformations}) == 64
    assert all(all(transformations[left ^ right][point] == transformations[left][transformations[right][point]]
                   for point in coordinates) for left in range(64) for right in range(64))
    for permutation in transformations:
        for blocks in bit_catalogs:
            assert {tuple(sorted(permutation[point] for point in block)) for block in blocks} == set(blocks)
    representatives = []
    orbit_histogram = Counter()
    orbit_hole_histogram = Counter()
    remaining_roots = set(bit_roots)
    while remaining_roots:
        representative = min(remaining_roots)
        present = [point for point in points if representative & (1 << point)]
        orbit = {mask(permutation[point] for point in present) for permutation in transformations}
        assert orbit <= remaining_roots
        assert len({bit_roots[state] for state in orbit}) == 1
        hole = next(iter(holes - set(present)))
        assert all(state & hole_mask == mask(holes - {hole}) for state in orbit)
        remaining_roots -= orbit
        representatives.append({'remaining': str(representative), 'hole': hole, 'orbit_size': len(orbit),
                                'ordered_root_multiplicity': bit_roots[representative]})
        orbit_histogram[len(orbit)] += 1
        orbit_hole_histogram[hole] += 1
    rows = [block for block in heptads if len(set(block) & holes) == 1]
    assert len(rows) == 224
    assert all(sum(hole not in block for block in rows) == 192 for hole in holes)
    assert sum(size * count for size, count in orbit_histogram.items()) == len(bit_roots)
    return {
        'status': 'G_complete_necessary_roots_and_proved_pointwise_hole_stabilizer_reduction',
        'dimension': 7, 'profile': [5, 4, 6, 2, 8], 'normal_form': 'G',
        'five_even_sum': 12, 'four_even_sum': 3, 'D6_odd_projections': [3, 48],
        'mixed_odd_projections': [51, 60], 'characteristic_projections': [12, 15, 63],
        'characteristic_charge': 60, 'symplectic_basis': list(basis),
        'catalog_counts': [len(blocks) for blocks in bit_catalogs],
        'two_independent_catalog_and_root_constructions_agree': True,
        'disjoint_defect_pairs': sum(defect_histogram.values()),
        'defect_pairs_by_actual_pure_five_hole': dict(sorted(defect_histogram.items())),
        'ordered_roots': sum(bit_roots.values()), 'distinct_root_sets': len(bit_roots),
        'ordered_roots_by_actual_pure_five_hole': dict(sorted(ordered_histogram.items())),
        'pointwise_hole_stabilizer_order': 64, 'symplectic_dot_checks': 64 * 64 * 64,
        'composition_point_checks': 64 * 64 * 64, 'remaining_root_orbits': len(representatives),
        'orbit_size_histogram': dict(sorted(orbit_histogram.items())),
        'orbits_by_actual_pure_five_hole': dict(sorted(orbit_hole_histogram.items())),
        'orbit_representatives': representatives,
        'root_multiset_sha256': hashlib.sha256(json.dumps(sorted(bit_roots.items()), separators=(',', ':')).encode()).hexdigest(),
        'eligible_anchored_heptads': 224, 'eligible_rows_avoiding_each_hole': 192,
        'new_cover_search': False, 'new_cover_certificate': False, 'G_excluded': False,
        'remaining_normal_forms': ['Z', 'G'], 'raw_profile_excluded': False,
        'remaining_raw_profiles': {'five_six': 27, 'three_six': 39},
        'exact_n7': 'open_lower_bound19', 'new_Lean': False, 'new_independent_review': False,
        'checker_sha256': digest(Path(__file__)),
        'note_sha256': digest(root / 'notes/dimension-seven-five-four-G-roots.md'),
        'dependency_sha256': {name: digest(root / name) for name in (
            'notes/dimension-seven-five-four-charge.md', 'results/dimension-7-five-four-charge.json',
            'notes/dimension-seven-nineteen-obstruction.md')},
        'scope': 'Complete necessary G root family and exact orbit partition under a written symplectic group. No root solved or excluded; actual t fixed, both mixed classes retained.'
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
