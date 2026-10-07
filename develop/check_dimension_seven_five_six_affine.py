"""Check the four-odd affine-plane exclusion of two size-four five-plus-six profiles."""
from collections import Counter
from itertools import combinations
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


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    basis = (3, 12, 48, 65, 71, 95)
    coordinates = {vector_sum(vector for index, vector in enumerate(basis) if bits & (1 << index)): bits
                   for bits in range(64)}
    quadratic = {point: ((bits & 7) & (bits >> 3)).bit_count() % 2 for point, bits in coordinates.items()}
    assert len(coordinates) == 64
    assert all(quadratic[left ^ right] == quadratic[left] ^ quadratic[right] ^ dot(left, right)
               for left in coordinates for right in coordinates)
    holes = sorted(vector_sum(basis[index] for index in range(3) if bits & (1 << index)) for bits in range(1, 8))
    assert all(dot(left, right) == 0 for left in holes for right in holes)
    points = sorted(set(coordinates) - {0})
    functional_planes = {}
    for functional in range(1, 8):
        plane = tuple(sorted(vector_sum(basis[index] for index in range(3) if bits & (1 << index))
                             for bits in range(1, 8) if (bits & functional).bit_count() % 2))
        assert len(plane) == 4
        functional_planes[plane] = functional
    assert len(functional_planes) == 7
    subset_planes = {}
    controls = Counter()
    charge_histograms = {5: Counter(), 6: Counter()}
    local_records = []
    for odd_projections in combinations(holes, 4):
        even_choices = [point for point in points if all(dot(point, odd) for odd in odd_projections)]
        if not even_choices:
            continue
        subset_planes[odd_projections] = len(even_choices)
        assert odd_projections in functional_planes and len(even_choices) == 8
        characteristic = tuple(sorted(set(holes) - set(odd_projections)))
        assert len(characteristic) == 3 and vector_sum(characteristic) == 0
        assert vector_sum(odd_projections) == 0
        characteristic_class = (127,) + tuple(127 ^ point for point in characteristic)
        assert all(dot(left, right) for left, right in combinations(characteristic_class, 2))
        array_pairs = [pair for pair in combinations(even_choices, 2) if dot(*pair)]
        available = sum(1 << point for point in even_choices)
        bit_pairs = []
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            compatible = available & sum(1 << other for other in even_choices if dot(point, other))
            while compatible:
                second_bit = compatible & -compatible
                other = second_bit.bit_length() - 1
                compatible ^= second_bit
                bit_pairs.append((point, other))
        assert array_pairs == bit_pairs and len(array_pairs) == 16
        for evens in [(point,) for point in even_choices] + array_pairs:
            defect = evens + tuple(127 ^ point for point in odd_projections)
            size = len(defect)
            assert size in (5, 6)
            assert not set(defect) & set(characteristic_class)
            assert all(dot(left, right) for left, right in combinations(defect, 2))
            projected = evens + odd_projections
            charge = vector_sum(projected)
            tau = (comb(size, 2) + comb(4, 2)) % 2
            assert sum(quadratic[point] for point in projected) % 2 == quadratic[charge] ^ tau
            assert dot(charge, charge) == 0
            if size == 6:
                assert charge in holes and all(dot(evens[0], point) == dot(evens[1], point) for point in holes)
                assert dot(evens[0], charge) == 1
            controls[size] += 1
            charge_histograms[size][charge] += 1
            local_records.append((size, odd_projections, evens, characteristic, charge))
    assert set(subset_planes) == set(functional_planes) and set(subset_planes.values()) == {8}
    assert controls == {5: 56, 6: 112}
    prior_path = root / 'results/dimension-7-size-four.json'
    prior = json.loads(prior_path.read_text())
    profiles = prior['count_profiles']['5+6']
    assert len(profiles) == 46
    targeted = []
    remaining = []
    for profile in profiles:
        even_counts = profile['defect_even_counts']
        counts = profile['saturated_counts']
        if even_counts not in ([5, 2], [1, 6]) or counts != [8, 0, 8]:
            remaining.append(profile)
            continue
        odds = [size - even for size, even in zip((5, 6), even_counts)]
        assert sorted(odds) == [0, 4]
        assert 7 * counts[0] + 6 * counts[1] + sum(even_counts) == 63
        assert counts[1] + 7 * counts[2] + sum(odds) + 4 == 64
        taus = [(comb(size, 2) + comb(odd, 2)) % 2 for size, odd in zip((5, 6), odds)]
        parity = (counts[0] + counts[1] + sum(taus)) % 2
        assert taus == [0, 1] and parity == profile['required_sum_of_pairwise_charge_products'] == 1
        targeted.append({'defect_even_counts': even_counts, 'defect_odd_counts': odds,
                         'saturated_counts': counts, 'defect_quadratic_taus': taus,
                         'forced_characteristic_charge': 0, 'required_charge_product': parity,
                         'actual_equal_charge_product': 0, 'status': 'excluded_by_four_odd_affine_plane_and_quadratic_charge'})
    assert len(targeted) == 2 and len(remaining) == 44
    for key, name in (('checker_sha256', 'develop/check_dimension_seven_size_four.py'),
                      ('proof_note_sha256', 'notes/dimension-seven-size-four.md')):
        assert prior[key] == hashlib.sha256((root / name).read_bytes()).hexdigest()
    dependencies = ('results/dimension-7-size-four.json', 'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'two_size_four_five_plus_six_profiles_excluded_by_affine_plane_and_quadratic_charge',
            'dimension': 7, 'characteristic_class_size_range': [4, 8], 'characteristic_size_four_excluded': False,
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'five_six_initial_raw_profiles': 46, 'five_six_newly_excluded_profiles': targeted,
            'five_six_remaining_unexcluded_count': len(remaining),
            'remaining_profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'five_six_remaining_raw_profiles': [profile['defect_even_counts'] + profile['saturated_counts'] for profile in remaining],
            'remaining_profiles_feasibility': 'untested_no_coloring_or_exclusion_claim',
            'three_six_raw_count_profiles': 48, 'three_six_feasibility': 'untested',
            'functional_and_subset_plane_catalogs_equal': True, 'affine_planes': len(functional_planes),
            'even_lifts_per_functional': 8, 'five_point_local_defects': controls[5], 'six_point_local_defects': controls[6],
            'local_array_and_bitmask_even_pair_catalogs_equal': True,
            'all_local_complementary_characteristic_charges_zero': True,
            'local_charge_histograms': {size: dict(sorted(histogram.items())) for size, histogram in charge_histograms.items()},
            'local_configuration_sha256': hashlib.sha256(json.dumps(sorted(local_records), separators=(',', ':')).encode()).hexdigest(),
            'quadratic_pair_controls': 4096, 'written_eight_spread_completion_used': True,
            'new_proof_uses_finite_cover_or_spread_completion_enumeration': False,
            'prior_spread_enumeration_rerun': False, 'all_small_classes_reenumerated': False,
            'native_SAT': False, 'exact_cover_search': False, 'DRAT_checked': False, 'Lean_run': False,
            'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'dependency_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in dependencies},
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-five-six-affine.md').read_bytes()).hexdigest(),
            'scope': 'Universal written four-odd affine-plane geometry forces h=0; two-defect quadratic charge parity1 contradicts equal alternating charges. Excludes only(5,2;8,0,8)and(1,6;8,0,8).168fixed-hole partial defect controls,not full colorings.44other5+6and48three-sixraw profiles untested;size4..8andexactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
