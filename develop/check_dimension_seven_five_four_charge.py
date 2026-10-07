"""Check the four necessary pure-five/four-even normal forms without a covering search."""
from collections import Counter, defaultdict
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


def bit_cliques(candidates, size):
    neighbors = {point: mask(other for other in candidates if other > point and dot(point, other)) for point in candidates}
    blocks = []

    def visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            visit(chosen + (point,), available & neighbors[point])

    visit((), mask(candidates))
    return blocks


def array_cliques(candidates, size):
    blocks = []

    def visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        for index, point in enumerate(available):
            visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    visit((), candidates)
    return blocks


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    four = bit_cliques(points, 4)
    five = bit_cliques(points, 5)
    assert four == array_cliques(points, 4) and five == array_cliques(points, 5)
    assert len(four) == 10080 and len(five) == 8064
    five_ranks = Counter()
    anchored_by_sum = defaultdict(list)
    for block in five:
        total = vector_sum(block)
        span = {vector_sum(block[index] for index in range(5) if bits & (1 << index)) for bits in range(32)}
        assert all(not dot(total, point) for point in block)
        assert len(span) == (32 if total else 16)
        five_ranks['rank_five_nonzero_sum' if total else 'rank_four_zero_sum'] += 1
        if len(set(block) & holes) == 1:
            anchored_by_sum[total].append(block)
            if total:
                assert total not in set(block) & holes
    anchored_histogram = Counter()
    for total, blocks in anchored_by_sum.items():
        anchored_histogram['zero' if not total else ('hole' if total in holes else 'outside')] += len(blocks)
    assert anchored_histogram == {'zero': 1120, 'hole': 672, 'outside': 2688}
    four_catalogs = defaultdict(list)
    charge_member_controls = 0
    for block in four:
        compatible = tuple(hole for hole in sorted(holes) if all(dot(point, hole) for point in block))
        assert len(compatible) <= 2
        total = vector_sum(block)
        assert total and all(dot(total, point) for point in block)
        for odd_pair in combinations(compatible, 2):
            assert total in odd_pair
            charge = total ^ vector_sum(odd_pair)
            assert charge in odd_pair and charge != total
            four_catalogs[(total, odd_pair)].append(block)
            charge_member_controls += 1
    assert charge_member_controls == 672
    forms = (
        ('Z', 0, 15, (15, 48), (3, 12), (1120, 16, 13584)),
        ('H', 12, 3, (3, 12), (48, 63), (96, 16, 1536)),
        ('D', 63, 48, (48, 15), (3, 12), (96, 16, 784)),
        ('G', 12, 3, (3, 48), (51, 60), (96, 16, 1088)),
    )
    catalogs = {}
    normal_forms = []
    for name, first_sum, second_sum, odd_pair, mixed_pair, expected in forms:
        first = anchored_by_sum[first_sum]
        second = four_catalogs[(second_sum, tuple(sorted(odd_pair)))]
        mixed = [bit_cliques([point for point in points if dot(point, odd)], 6) for odd in mixed_pair]
        assert all(len(blocks) == 32 for blocks in mixed)
        assert all(vector_sum(block) == odd for odd, blocks in zip(mixed_pair, mixed) for block in blocks)
        assert all(not set(block) & holes for block in second + mixed[0] + mixed[1])
        disjoint_pairs = [(left, right) for left in first for right in second if not set(left) & set(right)]
        assert (len(first), len(second), len(disjoint_pairs)) == expected
        characteristic = holes - set(odd_pair) - set(mixed_pair)
        charge = vector_sum(characteristic)
        assert first_sum ^ second_sum == vector_sum(mixed_pair)
        assert charge == first_sum ^ odd_pair[1]
        assert not dot(first_sum, vector_sum(mixed_pair))
        for blocks, odd_members in ((first, ()), (second, tuple(127 ^ point for point in odd_pair)),
                                    (mixed[0], (127 ^ mixed_pair[0],)), (mixed[1], (127 ^ mixed_pair[1],))):
            assert all(all(dot(left, right) for left, right in combinations(block + odd_members, 2)) for block in blocks)
        catalogs[name] = (first, second, mixed)
        normal_forms.append({'case': name, 'five_even_sum': first_sum, 'six_even_sum': second_sum,
                             'six_odd_projections': list(odd_pair), 'mixed_odd_projections': list(mixed_pair),
                             'characteristic_projections': sorted(characteristic), 'characteristic_charge': charge,
                             'anchored_five_blocks': len(first), 'six_four_even_blocks': len(second),
                             'disjoint_defect_pairs': len(disjoint_pairs), 'mixed_sextets_each': [32, 32],
                             'full_coloring_feasibility': 'untested'})
    target_basis = (3, 12, 48, 65, 71, 95, 127)
    role_controls = Counter()
    gram_controls = 0
    source_class_controls = 0
    for odd_pair in combinations(sorted(holes), 2):
        for mixed_pair in combinations(sorted(holes - set(odd_pair)), 2):
            first_mixed, second_mixed = mixed_pair
            for second_sum in odd_pair:
                first_odd = second_sum
                second_odd = next(point for point in odd_pair if point != second_sum)
                first_sum = first_odd ^ first_mixed ^ second_mixed
                characteristic = holes - set(odd_pair) - set(mixed_pair)
                charge = vector_sum(characteristic)
                assert first_sum ^ second_sum == vector_sum(mixed_pair) and charge == first_sum ^ second_odd
                if not first_sum:
                    name = 'Z'
                    half = (first_mixed, second_mixed, second_odd)
                elif not charge:
                    name = 'H'
                    assert first_sum == second_odd
                    half = (first_odd, second_odd, first_mixed)
                elif charge in odd_pair:
                    name = 'D'
                    assert charge == first_odd and second_odd == first_mixed ^ second_mixed
                    half = (first_mixed, second_mixed, first_odd)
                else:
                    name = 'G'
                    assert first_sum in characteristic
                    half = (first_odd, first_sum, second_odd)
                assert len({vector_sum(half[index] for index in range(3) if bits & (1 << index)) for bits in range(8)}) == 8
                duals = []
                for position in range(3):
                    dual = next(point for point in points if all(dot(point, half[index]) == int(index == position) for index in range(3))
                                and all(not dot(point, previous) for previous in duals))
                    duals.append(dual)
                source_basis = half + tuple(duals) + (127,)
                assert all(dot(source_basis[left], source_basis[right]) == dot(target_basis[left], target_basis[right])
                           for left in range(7) for right in range(7))
                mapping = {vector_sum(source_basis[index] for index in range(7) if bits & (1 << index)):
                           vector_sum(target_basis[index] for index in range(7) if bits & (1 << index)) for bits in range(128)}
                assert len(mapping) == len(set(mapping.values())) == 128 and mapping[127] == 127
                assert {mapping[point] for point in holes} == holes
                target = next(row for row in normal_forms if row['case'] == name)
                assert mapping[first_sum] == target['five_even_sum'] and mapping[second_sum] == target['six_even_sum']
                assert {mapping[point] for point in odd_pair} == set(target['six_odd_projections'])
                assert {mapping[point] for point in mixed_pair} == set(target['mixed_odd_projections'])
                assert {mapping[point] for point in characteristic} == set(target['characteristic_projections'])
                assert mapping[charge] == target['characteristic_charge']
                target_first, target_second, target_mixed = catalogs[name]
                assert {tuple(sorted(mapping[point] for point in block)) for block in anchored_by_sum[first_sum]} == set(target_first)
                assert {tuple(sorted(mapping[point] for point in block)) for block in four_catalogs[(second_sum, odd_pair)]} == set(target_second)
                inverse = {destination: source for source, destination in mapping.items()}
                for blocks, odd_projections, required_sum in ((target_first, (), first_sum),
                                                              (target_second, odd_pair, second_sum),
                                                              (target_mixed[0], (inverse[target['mixed_odd_projections'][0]],), inverse[target['mixed_odd_projections'][0]]),
                                                              (target_mixed[1], (inverse[target['mixed_odd_projections'][1]],), inverse[target['mixed_odd_projections'][1]])):
                    for block in blocks:
                        source_even = tuple(inverse[point] for point in block)
                        source_class = source_even + tuple(127 ^ odd for odd in odd_projections)
                        assert vector_sum(source_even) == required_sum
                        assert all(dot(left, right) for left, right in combinations(source_class, 2))
                        source_class_controls += 1
                gram_controls += 49
                role_controls[name] += 1
    assert role_controls == {'Z': 84, 'H': 84, 'D': 84, 'G': 168}
    assert gram_controls == 20580 and source_class_controls == 159936
    prior = json.loads((root / 'results/dimension-7-four-even-pairs-check.json').read_text())
    target_profile = [5, 4, 6, 2, 8]
    assert prior['five_six_remaining_raw_profiles'].count(target_profile) == 1
    assert prior['five_six_total_excluded_profiles'] == 19 and prior['five_six_remaining_unexcluded_count'] == 27
    assert prior['three_six_total_excluded_profiles'] == 9 and prior['three_six_remaining_unexcluded_count'] == 39
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    target_row = next(row for row in raw['count_profiles']['5+6'] if row['defect_even_counts'] + row['saturated_counts'] == target_profile)
    assert target_row['required_sum_of_pairwise_charge_products'] == 0
    dependencies = ('notes/dimension-seven-two-six-profiles.md', 'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-nineteen-obstruction.md', 'results/dimension-7-size-four.json',
                    'results/dimension-7-four-even-pairs-check.json')
    return {'status': 'specified_five_four_profile_reduced_to_four_necessary_marked_normal_forms',
            'dimension': 7, 'profile': target_profile, 'profile_columns': ['k5', 'k6', 'A', 'B', 'C'],
            'target_profile_excluded': False, 'target_profile_realized': False, 'normal_forms': normal_forms,
            'five_six_total_excluded_profiles': 19, 'five_six_remaining_unexcluded_count': 27,
            'five_six_remaining_raw_profiles': prior['five_six_remaining_raw_profiles'],
            'three_six_total_excluded_profiles': 9, 'three_six_remaining_unexcluded_count': 39,
            'three_six_remaining_raw_profiles': prior['three_six_remaining_raw_profiles'],
            'remaining_profiles_feasibility': 'untested', 'characteristic_class_size_range': [4, 8],
            'exact_n7_chromatic_number': 'open', 'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'new_numerical_lower_bound': False, 'nineteen_color_witness': False,
            'existing_charge_member_lemma_applied': True, 'outside_hole_even_sums_excluded_for_this_profile': True,
            'zero_five_even_sum_retained': True, 'five_defect_exactly_one_hole_point': True,
            'remaining_even_cover_points': 42, 'remaining_heptads': 6, 'remaining_holes': 6,
            'four_even_cliques': len(four), 'five_even_cliques': len(five), 'five_span_rank_histogram': dict(sorted(five_ranks.items())),
            'anchored_five_sum_histogram': dict(sorted(anchored_histogram.items())),
            'independent_array_and_bitmask_catalogs_equal': True, 'charge_member_local_controls': charge_member_controls,
            'marked_role_normalization_controls': dict(sorted(role_controls.items())), 'total_marked_role_controls': sum(role_controls.values()),
            'normalization_Gram_entries_checked': gram_controls, 'inverse_source_class_controls': source_class_controls,
            'disjoint_defect_pair_counts_are_full_cover_roots': False, 'mixed_and_heptad_joint_feasibility_tested': False,
            'new_exact_cover_search': False, 'new_finite_cover_certificate': False,
            'prior_cover_certificate_used_for_new_reduction': False, 'prior_spread_enumeration_rerun': False,
            'native_SAT': False, 'DRAT_checked': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_and_Zenodo_PDF_changed': False,
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-five-four-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written application of the existing charge-member lemma removes the apparent rank-two exception,forces both sums into M,and reduces the specified profile to four marked forms. Local classes and isometries checked;no full cover search or new raw-profile exclusion.27five-six/39three-sixprofiles remain unexcluded;exactn7open>=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')
