"""Check the three-plus-one odd split and the incompatible defect charge catalogs."""
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
    holes = (3, 12, 15, 48, 51, 60, 63)
    points = [point for point in range(1, 128) if not dot(point, 127)]
    functionals = {tuple(dot(point, hole) for hole in holes) for point in points}
    nonzero = sorted(functional for functional in functionals if any(functional))
    assert len(functionals) == 8 and len(nonzero) == 7
    for first, second in combinations(nonzero, 2):
        assert sum(left & right for left, right in zip(first, second)) == 2
    assert all(dot(left, right) == 0 for left in holes for right in holes)
    five_records = []
    joins = []
    characteristic_charges = Counter()
    required_charges = {point: set() for point in holes}
    for odd_triple in combinations(holes, 3):
        candidates = [point for point in points if all(dot(point, odd) for odd in odd_triple)]
        if not candidates:
            continue
        assert len(candidates) == 8
        array_pairs = [pair for pair in combinations(candidates, 2) if dot(*pair)]
        available = mask(candidates)
        bit_pairs = []
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            compatible = available & mask(other for other in candidates if dot(point, other))
            while compatible:
                second_bit = compatible & -compatible
                other = second_bit.bit_length() - 1
                compatible ^= second_bit
                bit_pairs.append((point, other))
        assert bit_pairs == array_pairs and len(array_pairs) == 16
        for even_pair in array_pairs:
            first, second = even_pair
            defect = even_pair + tuple(127 ^ point for point in odd_triple)
            assert all(dot(left, right) for left, right in combinations(defect, 2))
            assert all(dot(first, point) == dot(second, point) for point in holes)
            radical = first ^ second
            assert radical in holes and dot(first, radical) == 1
            charge_five = radical ^ vector_sum(odd_triple)
            assert charge_five in set(holes) | {0}
            five_records.append((odd_triple, even_pair, charge_five))
            for odd_six in sorted(set(holes) - set(odd_triple)):
                characteristic = tuple(sorted(set(holes) - set(odd_triple) - {odd_six}))
                characteristic_class = (127,) + tuple(127 ^ point for point in characteristic)
                assert not set(characteristic_class) & set(defect)
                assert all(dot(left, right) for left, right in combinations(characteristic_class, 2))
                charge_characteristic = vector_sum(characteristic)
                assert charge_characteristic == vector_sum(odd_triple) ^ odd_six
                required_six = charge_characteristic ^ charge_five
                assert required_six == radical ^ odd_six and required_six in set(holes) | {0}
                assert dot(required_six, odd_six) == 0
                required_charges[odd_six].add(required_six)
                characteristic_charges['zero' if charge_characteristic == 0 else 'nonzero'] += 1
                joins.append((odd_triple, even_pair, odd_six, characteristic, required_six))
    assert len(five_records) == 448 and len(joins) == 1792
    assert characteristic_charges == {'zero': 448, 'nonzero': 1344}
    six_records = []
    available_charge_counts = {}
    for odd in holes:
        candidates = [point for point in points if dot(point, odd)]
        assert len(candidates) == 32
        array_blocks = [block for block in combinations(candidates, 5)
                        if all(dot(left, right) for left, right in combinations(block, 2))]
        neighbors = {point: mask(other for other in candidates if other > point and dot(point, other)) for point in candidates}
        bit_blocks = []

        def enumerate_five(chosen, available):
            if len(chosen) == 5:
                bit_blocks.append(chosen)
                return
            while available:
                first_bit = available & -available
                point = first_bit.bit_length() - 1
                available ^= first_bit
                enumerate_five(chosen + (point,), available & neighbors[point])

        enumerate_five((), mask(candidates))
        assert array_blocks == bit_blocks and len(array_blocks) == 192
        histogram = Counter()
        for block in array_blocks:
            defect = block + (127 ^ odd,)
            assert all(dot(left, right) for left, right in combinations(defect, 2))
            even_sum = vector_sum(block)
            charge = even_sum ^ odd
            assert dot(even_sum, odd) == dot(charge, odd) == 1
            assert even_sum not in set(holes) | {0} and charge not in set(holes) | {0}
            assert all(dot(even_sum, point) == 0 for point in block)
            assert charge not in block and all(dot(charge, point) == 1 for point in block)
            histogram[charge] += 1
            six_records.append((odd, block, charge))
        assert len(histogram) == 32 and set(histogram.values()) == {6}
        assert not set(histogram) & required_charges[odd]
        available_charge_counts[odd] = len(histogram)
    assert len(six_records) == 1344
    prior_path = root / 'results/dimension-7-five-six-affine.json'
    prior = json.loads(prior_path.read_text())
    assert prior['five_six_remaining_unexcluded_count'] == 44
    target = [2, 5, 8, 0, 8]
    assert prior['five_six_remaining_raw_profiles'].count(target) == 1
    remaining = [row for row in prior['five_six_remaining_raw_profiles'] if row != target]
    assert len(remaining) == 43
    for key, name in (('checker_sha256', 'develop/check_dimension_seven_five_six_affine.py'),
                      ('proof_note_sha256', 'notes/dimension-seven-five-six-affine.md')):
        assert prior[key] == hashlib.sha256((root / name).read_bytes()).hexdigest()
    dependencies = ('results/dimension-7-five-six-affine.json', 'results/dimension-7-size-four.json',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'size_four_five_plus_six_odd_split3plus1_profile_excluded_by_partition_charge',
            'dimension': 7, 'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19, 'exact_n7_chromatic_number': 'open',
            'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'newly_excluded_profile': target, 'profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'five_six_initial_raw_profiles': 46, 'five_six_total_excluded_profiles': 3,
            'five_six_remaining_unexcluded_count': len(remaining), 'five_six_remaining_raw_profiles': remaining,
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'three_six_raw_count_profiles': 48, 'three_six_feasibility': 'untested',
            'nonzero_functional_pair_controls': 21, 'common_value_one_points_per_distinct_pair': 2,
            'five_point_local_defects': len(five_records), 'conditional_partition_charge_controls': len(joins),
            'characteristic_charge_histogram': dict(sorted(characteristic_charges.items())),
            'six_point_local_defects': len(six_records), 'six_point_local_defects_per_odd_projection': 192,
            'six_point_distinct_charges_per_odd_projection': available_charge_counts,
            'all_conditional_charge_joins_empty': True, 'array_and_bitmask_defect_catalogs_equal': True,
            'five_configuration_sha256': hashlib.sha256(json.dumps(five_records, separators=(',', ':')).encode()).hexdigest(),
            'conditional_join_sha256': hashlib.sha256(json.dumps(joins, separators=(',', ':')).encode()).hexdigest(),
            'six_configuration_sha256': hashlib.sha256(json.dumps(six_records, separators=(',', ':')).encode()).hexdigest(),
            'written_eight_spread_completion_used': True, 'new_proof_uses_finite_cover_or_spread_completion_enumeration': False,
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'exact_cover_search': False, 'DRAT_checked': False, 'Lean_run': False,
            'independent_Pro_review': False, 'manuscript_and_Zenodo_PDF_changed': False,
            'dependency_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in dependencies},
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-five-six-split31.md').read_bytes()).hexdigest(),
            'scope': 'Universal written equal-functional and partition-charge proof excludes only(2,5;8,0,8),without assuming h=0.448fixed-hole D5classes,1792conditional charge joins,and1344D6classes checked locally;not full colorings.43other5+6and48three-sixrawprofiles untested;size4..8andexactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
