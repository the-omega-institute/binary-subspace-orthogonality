"""Check quadratic class parity for a three-point characteristic class."""
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
    result = 0
    for vector in vectors:
        result ^= vector
    return result


def projection(vector):
    return vector ^ (127 if dot(vector, 127) else 0)


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
    assert all(dot(projection(left), projection(right)) == dot(left, right) ^ (dot(left, 127) & dot(right, 127))
               for left in range(128) for right in range(128))
    assert sum(quadratic[projection(vector)] for vector in range(1, 128)) % 2 == 0
    points = list(range(1, 127))
    neighbors = {point: sum(1 << other for other in points if other > point and dot(point, other))
                 for point in points}
    classes = {5: [], 6: []}

    def extend(chosen, candidates):
        if len(chosen) in classes:
            classes[len(chosen)].append(chosen)
        if len(chosen) == 6:
            return
        while candidates:
            first = candidates & -candidates
            point = first.bit_length() - 1
            candidates ^= first
            extend(chosen + (point,), candidates & neighbors[point])

    extend((), sum(1 << point for point in points))
    histograms = {}
    digests = {}
    local_counts = Counter()
    local_witnesses = {}
    hole_counts = Counter()
    hole_witnesses = {}
    for size, blocks in classes.items():
        histogram = Counter()
        for block in blocks:
            assert all(dot(left, right) == 1 for left, right in combinations(block, 2))
            odd_count = sum(dot(point, 127) for point in block)
            histogram[odd_count] += 1
            projected = [projection(point) for point in block]
            charge = vector_sum(projected)
            quadratic_sum = sum(quadratic[point] for point in projected) % 2
            assert quadratic_sum == (quadratic[charge] + comb(size, 2) + comb(odd_count, 2)) % 2
            if size == 5 and 124 not in block and 115 not in block and charge == 15:
                local_counts[odd_count] += 1
                local_witnesses.setdefault(odd_count, block)
                projected_odd = [projection(point) for point in block if dot(point, 127)]
                holes = [3, 12] + projected_odd
                if all(dot(left, right) == 0 for left, right in combinations(holes, 2)):
                    hole_counts[odd_count] += 1
                    hole_witnesses.setdefault(odd_count, block)
        histograms[size] = dict(sorted(histogram.items()))
        digests[size] = hashlib.sha256(json.dumps(sorted(blocks), separators=(',', ':')).encode()).hexdigest()
    assert histograms[5] == {0: 8064, 1: 40320, 2: 60480, 3: 60480, 4: 7560, 5: 2835}
    assert histograms[6] == {0: 2016, 1: 12096, 2: 30240, 4: 15120, 6: 945}
    prior = json.loads((root / 'results/dimension-7-characteristic-three.json').read_text())
    assert digests[6] == prior['independent_class_set_sha256']['6']
    assert local_counts == {0: 96, 1: 448, 2: 960, 3: 624, 4: 120, 5: 39}
    assert hole_counts == {0: 96, 1: 192, 3: 48, 5: 3}
    profiles = []
    survivors = []
    for defective_even in range(6):
        defective_odd = 5 - defective_even
        for even_count in range(18):
            for mixed_count in range(18):
                odd_count = 17 - even_count - mixed_count
                if odd_count < 0 or 7 * even_count + 6 * mixed_count + defective_even != 63:
                    continue
                if mixed_count + 7 * odd_count + defective_odd + 3 != 64:
                    continue
                row = {'defective_even': defective_even, 'defective_odd': defective_odd,
                       'pure_even_heptads': even_count, 'mixed_saturated': mixed_count,
                       'pure_odd_heptads': odd_count,
                       'saturated_quadratic_parity': (even_count + mixed_count) % 2,
                       'defective_quadratic_parity': comb(defective_odd, 2) % 2}
                if row['saturated_quadratic_parity'] != row['defective_quadratic_parity']:
                    row['status'] = 'excluded_by_quadratic_class_parity'
                elif odd_count == 8 and defective_even % 2 == 1 and defective_odd > 0:
                    assert (defective_even, even_count, mixed_count, odd_count) == (3, 6, 3, 8)
                    row['status'] = 'excluded_by_completed_lagrangian_and_odd_even_count'
                else:
                    row['status'] = 'necessary_profile_only_realizability_open'
                    survivors.append((defective_even, even_count, mixed_count, odd_count))
                profiles.append(row)
    assert len(profiles) == 10 and survivors == [(0, 3, 7, 7), (1, 2, 8, 7), (2, 7, 2, 8)]
    assert Counter(row['status'] for row in profiles) == {
        'excluded_by_quadratic_class_parity': 6,
        'excluded_by_completed_lagrangian_and_odd_even_count': 1,
        'necessary_profile_only_realizability_open': 3}
    tau = {even_count: (1 + comb(6 - even_count, 2)) % 2 for even_count in (0, 2, 4, 5, 6)}
    assert tau == {0: 0, 2: 1, 4: 0, 5: 1, 6: 1}
    assert all(quadratic[left ^ right] ^ quadratic[left] ^ quadratic[right] == dot(left, right)
               for left in coordinates for right in coordinates)
    return {'status': 'written_quadratic_constraints_for_three_point_characteristic_classes',
            'dimension': 7, 'characteristic_class_size_range': [3, 8],
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open', 'nineteen_color_witness': False,
            'new_numerical_lower_bound': False, 'projection_pairing_pairs_checked': 16384,
            'quadratic_polarization_pairs_checked': 4096,
            'class_counts_by_size_and_odd_count': histograms,
            'independent_class_set_sha256': digests,
            'independent_five_classes_checked': len(classes[5]), 'independent_six_classes_checked': len(classes[6]),
            'one_five_defect_count_profiles': profiles, 'one_five_defect_necessary_survivors': survivors,
            'survivor_realizability': 'open_all_three',
            'two_six_defect_pairing_condition': 'w1 dot w2 = A+B+tau1+tau2 modulo2, w1+w2 equals characteristic charge',
            'six_class_tau_by_even_count': tau, 'coupled_six_class_pairs_enumerated': False,
            'local_characteristic_pair': [3, 12], 'local_required_charge': 15,
            'local_charge_five_class_counts_by_odd_count': dict(sorted(local_counts.items())),
            'local_charge_five_class_witnesses': dict(sorted(local_witnesses.items())),
            'local_hole_compatible_counts_by_odd_count': dict(sorted(hole_counts.items())),
            'local_hole_compatible_witnesses': dict(sorted(hole_witnesses.items())),
            'local_classes_are_colorings': False, 'native_SAT': False, 'checked_UNSAT_proof': False,
            'Lean_run': False, 'independent_Pro_review': False, 'submitted_manuscript_changed': False,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256((root / 'notes/dimension-seven-three-point-defects.md').read_bytes()).hexdigest(),
            'prior_characteristic_report_sha256': hashlib.sha256((root / 'results/dimension-7-characteristic-three.json').read_bytes()).hexdigest(),
            'scope': 'Universal quadratic identities and exact independent5/6class/count-profile checks; neither completecoloring enumeration nor coupled sixclass feasibility or nineteen-color upperbound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
