"""Check size-four characteristic deficits, charge identities and the single-four-defect reduction."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import comb
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


def projection(vector):
    return vector ^ (127 if dot(vector, 127) else 0)


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    basis = (3, 12, 48, 65, 71, 95)
    coordinates = {vector_sum(vector for index, vector in enumerate(basis) if bits & (1 << index)): bits for bits in range(64)}
    quadratic = {point: ((bits & 7) & (bits >> 3)).bit_count() % 2 for point, bits in coordinates.items()}
    assert len(coordinates) == 64
    assert all(dot(projection(left), projection(right)) == dot(left, right) ^ (dot(left, 127) & dot(right, 127))
               for left in range(128) for right in range(128))
    assert all(quadratic[left ^ right] == quadratic[left] ^ quadratic[right] ^ dot(left, right)
               for left in coordinates for right in coordinates)
    triple_charge_controls = 0
    for first, second, third in product(coordinates, repeat=3):
        assert quadratic[first ^ second ^ third] == (quadratic[first] ^ quadratic[second] ^ quadratic[third]
                                                     ^ dot(first, second) ^ dot(first, third) ^ dot(second, third))
        triple_charge_controls += 1
    patterns = ((4,), (5, 6), (6, 6, 6))
    profiles_by_pattern = {}
    one_four_survivors = []
    for sizes in patterns:
        if sizes == (4,):
            even_parts = list(product(range(5)))
        elif sizes == (5, 6):
            even_parts = list(product(range(6), (0, 2, 4, 5, 6)))
        else:
            even_parts = list(combinations_with_replacement((0, 2, 4, 5, 6), 3))
        direct = []
        formula = []
        saturated = 18 - len(sizes)
        for even_counts in even_parts:
            total_even = sum(even_counts)
            total_odd = sum(sizes) - total_even
            for pure_even in range(saturated + 1):
                for mixed in range(saturated - pure_even + 1):
                    pure_odd = saturated - pure_even - mixed
                    if 7 * pure_even + 6 * mixed + total_even == 63 and mixed + 7 * pure_odd + total_odd + 4 == 64:
                        direct.append((even_counts, pure_even, mixed, pure_odd))
            for shift in range(-4, 5):
                mixed = total_even + 7 * shift
                pure_even = 9 - total_even - 6 * shift
                pure_odd = 9 - len(sizes) - shift
                if min(pure_even, mixed, pure_odd) >= 0:
                    formula.append((even_counts, pure_even, mixed, pure_odd))
        assert sorted(direct) == sorted(formula)
        expected_count = {(4,): 9, (5, 6): 46, (6, 6, 6): 48}[sizes]
        assert len(direct) == expected_count
        records = []
        for even_counts, pure_even, mixed, pure_odd in sorted(direct):
            odd_counts = [size - even for size, even in zip(sizes, even_counts)]
            taus = [(comb(size, 2) + comb(odd, 2)) % 2 for size, odd in zip(sizes, odd_counts)]
            pairing_parity = (pure_even + mixed + sum(taus)) % 2
            status = 'raw_count_profile_charge_and_common_coloring_feasibility_open'
            capacity = None
            if sizes == (4,):
                even = even_counts[0]
                if pairing_parity:
                    status = 'excluded_by_single_defect_quadratic_parity'
                elif pure_odd == 7:
                    defect_capacity = 0 if even == 0 else 2 if even == 4 else 1
                    capacity = 2 * pure_even + mixed + defect_capacity
                    assert capacity < 14
                    status = 'excluded_by_two_hole_even_point_capacity'
                elif even == 1 and pure_odd == 8:
                    status = 'excluded_by_single_even_member_forced_into_hole_lagrangian'
                else:
                    assert (even, pure_even, mixed, pure_odd) == (2, 7, 2, 8)
                    status = 'necessary_single_four_defect_profile_realizability_open'
                    one_four_survivors.append([even, 4 - even, pure_even, mixed, pure_odd])
            records.append({'defect_sizes': list(sizes), 'defect_even_counts': list(even_counts), 'defect_odd_counts': odd_counts,
                            'saturated_counts': [pure_even, mixed, pure_odd], 'defect_quadratic_taus': taus,
                            'required_sum_of_pairwise_charge_products': pairing_parity,
                            'two_hole_even_point_capacity': capacity, 'status': status})
        profiles_by_pattern['+'.join(map(str, sizes))] = records
    assert one_four_survivors == [[2, 2, 7, 2, 8]]
    points = sorted(set(coordinates) - {0})
    holes = (3, 12, 15, 48, 51, 60, 63)
    local_configurations = []
    charge_locations = Counter()
    for odd_pair in combinations(holes, 2):
        candidates = [point for point in points if all(dot(point, odd) for odd in odd_pair)]
        array_pairs = [pair for pair in combinations(candidates, 2) if dot(*pair)]
        available = sum(1 << point for point in candidates)
        bit_pairs = []
        while available:
            first = available & -available
            point = first.bit_length() - 1
            available ^= first
            compatible = available & sum(1 << other for other in candidates if dot(point, other))
            while compatible:
                second = compatible & -compatible
                other = second.bit_length() - 1
                compatible ^= second
                bit_pairs.append((point, other))
        assert array_pairs == bit_pairs
        for even_pair in array_pairs:
            defect = even_pair + tuple(127 ^ point for point in odd_pair)
            charge = vector_sum(projection(point) for point in defect)
            assert sum(quadratic[projection(point)] for point in defect) % 2 == (quadratic[charge] + comb(4, 2) + comb(2, 2)) % 2
            for characteristic in combinations(sorted(set(holes) - set(odd_pair)), 3):
                if vector_sum(characteristic) != charge:
                    continue
                characteristic_class = (127,) + tuple(127 ^ point for point in characteristic)
                assert all(dot(left, right) == 1 for left, right in combinations(characteristic_class, 2))
                assert not set(characteristic_class) & set(defect)
                assert all(dot(left, right) == 1 for left, right in combinations(defect, 2))
                mixed_projections = tuple(sorted(set(holes) - set(characteristic) - set(odd_pair)))
                radical = vector_sum(even_pair)
                assert radical == vector_sum(mixed_projections) and radical in holes
                assert dot(even_pair[0], radical) == 1
                assert all(dot(even_pair[0], point) == dot(even_pair[1], point) for point in holes)
                assert sum(dot(even_pair[0], point) for point in characteristic) == 1
                assert sum(dot(even_pair[0], point) for point in mixed_projections) == 1
                assert charge and charge not in characteristic
                location = 'charge_in_defect' if charge in odd_pair else 'charge_in_mixed'
                assert charge in set(odd_pair) | set(mixed_projections)
                charge_locations[location] += 1
                local_configurations.append((odd_pair, even_pair, characteristic, mixed_projections, charge))
    assert len(local_configurations) == 1008 and charge_locations == {'charge_in_defect': 672, 'charge_in_mixed': 336}
    prior_names = ('dimension-7-six-holes.json', 'dimension-7-seven-holes.json', 'dimension-7-three-point-defects.json')
    prior_bindings = {name: hashlib.sha256((root / 'results' / name).read_bytes()).hexdigest() for name in prior_names}
    prior = json.loads((root / 'results' / prior_names[0]).read_text())
    assert prior['characteristic_class_size_range'] == [4, 8] and prior['size_three_entire_branch_excluded']
    assert prior['checker_sha256'] == hashlib.sha256((root / 'develop/check_dimension_seven_six_holes.py').read_bytes()).hexdigest()
    assert prior['proof_note_sha256'] == hashlib.sha256((root / 'notes/dimension-seven-six-holes.md').read_bytes()).hexdigest()
    seven = json.loads((root / 'results' / prior_names[1]).read_text())
    assert seven['completion_multiplicity'] == 1 and seven['hole_lagrangians_per_partial_spread'] == 2
    return {'status': 'size_four_deficits_and_charges_derived_single_four_defect_profiles_reduce9to1',
            'dimension': 7, 'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19, 'exact_n7_chromatic_number': 'open',
            'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'outside_deficit': 3, 'defect_size_patterns': [list(sizes) for sizes in patterns],
            'raw_count_profiles_by_pattern': {key: len(records) for key, records in profiles_by_pattern.items()},
            'count_profiles': profiles_by_pattern, 'direct_and_formula_profile_sets_equal': True,
            'single_four_initial_profiles': 9, 'single_four_excluded_profiles': 8,
            'single_four_remaining_profiles': one_four_survivors,
            'single_four_exclusions_by_reason': dict(Counter(item['status'] for item in profiles_by_pattern['4'] if item['status'].startswith('excluded_'))),
            'five_six_branch': 'open_46_raw_count_profiles_not_feasibility_checked',
            'three_six_branch': 'open_48_raw_count_profiles_not_feasibility_checked',
            'projection_pair_controls': 16384, 'quadratic_pair_controls': 4096,
            'three_charge_polarization_controls': triple_charge_controls,
            'fixed_hole_single_four_local_configurations': len(local_configurations),
            'local_charge_location_histogram': dict(sorted(charge_locations.items())),
            'local_configuration_sha256': hashlib.sha256(json.dumps(sorted(local_configurations), separators=(',', ':')).encode()).hexdigest(),
            'local_array_and_bitmask_even_pair_catalogs_equal': True,
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'exact_cover_search': False, 'DRAT_checked': False, 'Lean_run': False,
            'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'prior_report_sha256': prior_bindings, 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-size-four.md').read_bytes()).hexdigest(),
            'scope': 'Written size4deficit/count/generalcharge derivation, five quadratic single4exclusions, two finite-seven-spread-dependent capacity exclusions, and one written eight-spread isotropy exclusion. Only single4profile(2,2;7,2,8)remains necessary, unrealized; other46/48raw count profiles are not feasibility results. Fixed-hole1008local controls preserve characteristic/defect disjointness and charge constraints but do not construct common colorings. Size4through8/exactn7remainopen>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
