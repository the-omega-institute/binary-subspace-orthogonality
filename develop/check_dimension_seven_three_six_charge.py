"""Audit the three necessary (3,6;6,2,8) marked forms, without a cover search."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import (
    array_cliques, bit_cliques, digest, dot, vector_sum,
)


def linear_values(basis):
    return tuple(vector_sum(point for index, point in enumerate(basis)
                            if bits & (1 << index)) for bits in range(1 << len(basis)))


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    basis = (3, 12, 48, 65, 71, 95, 127)
    decoded = linear_values(basis)
    encoded = {point: bits for bits, point in enumerate(decoded)}
    holes = set(linear_values(basis[:3])) - {0}
    assert len(encoded) == 128 and holes == {3, 12, 15, 48, 51, 60, 63}
    matrices = [linear_values(columns) for columns in permutations(range(1, 8), 3)
                if len(set(linear_values(columns))) == 8]
    assert len(matrices) == 168
    symmetric = []
    for bits in range(64):
        entries = [(bits >> index) & 1 for index in range(6)]
        diagonal_first, diagonal_second, diagonal_third, first_second, first_third, second_third = entries
        columns = (diagonal_first | first_second << 1 | first_third << 2,
                   first_second | diagonal_second << 1 | second_third << 2,
                   first_third | second_third << 1 | diagonal_third << 2)
        symmetric.append(linear_values(columns))
    assert len(set(symmetric)) == 64
    for functional in range(1, 8):
        assert Counter(matrix[functional] for matrix in symmetric) == {value: 8 for value in range(8)}

    def shear(point, matrix):
        bits = encoded[point]
        return decoded[bits ^ matrix[(bits >> 3) & 7]]

    triples = bit_cliques(even, 3)
    sextets = bit_cliques(even, 6)
    heptads = bit_cliques(even, 7)
    assert triples == array_cliques(even, 3)
    assert sextets == array_cliques(even, 6)
    assert heptads == array_cliques(even, 7)
    anchored = [block for block in heptads if len(set(block) & holes) == 1]
    assert len(heptads) == 288 and len(anchored) == 224
    forms = (
        ('I', 0, (48, 63), (3, 12), 95, 80, 0, 32, ((48, 63), (51, 60))),
        ('II', 1, (3, 51), (12, 60), 6, 54, 0, 32, ((3, 51), (12, 60))),
        ('III', 0, (48, 51), (3, 12), 95, 80, 12, 16, ((48, 51), (60, 63))),
    )
    catalogs = {}
    rows = []
    symplectic_pairs = 0
    composition_points = 0
    original_class_controls = 0
    for name, eta, odd_pair, mixed_pair, triple_sum, pure_sum, charge, order, expected_orbits in forms:
        first = [block for block in triples if vector_sum(block) == triple_sum
                 and all(dot(point, odd) for point in block for odd in odd_pair)]
        second = [block for block in sextets if vector_sum(block) == pure_sum
                  and len(set(block) & holes) == 1]
        mixed = [bit_cliques([point for point in even if dot(point, odd)], 6) for odd in mixed_pair]
        assert mixed == [array_cliques([point for point in even if dot(point, odd)], 6) for odd in mixed_pair]
        assert len(first) == 4 and len(second) == 24 and all(len(blocks) == 32 for blocks in mixed)
        characteristic = tuple(sorted(holes - set(odd_pair) - set(mixed_pair)))
        possible_holes = tuple(sorted(point for point in holes if dot(point, triple_sum)))
        assert vector_sum(characteristic) == charge and triple_sum ^ pure_sum == vector_sum(mixed_pair)
        assert not dot(triple_sum ^ vector_sum(odd_pair), pure_sum)
        assert all(dot(point, triple_sum) == eta for point in mixed_pair)
        for blocks, odd_members in ((first, odd_pair), (second, ()),
                                    (mixed[0], (mixed_pair[0],)), (mixed[1], (mixed_pair[1],))):
            for block in blocks:
                original = block + tuple(127 ^ odd for odd in odd_members)
                assert len(set(original)) == len(original)
                assert all(dot(left, right) for left, right in combinations(original, 2))
                original_class_controls += 1
        assert all(not set(block) & holes for block in first + mixed[0] + mixed[1])
        assert all(vector_sum(block) == odd for odd, blocks in zip(mixed_pair, mixed) for block in blocks)
        assert all(pure_sum not in block and all(dot(pure_sum, point) for point in block) for block in second)
        assert all(tuple(sorted(block + (pure_sum,))) in heptads for block in second)
        hole_histogram = Counter(next(iter(set(block) & holes)) for block in second)
        assert hole_histogram == {point: 6 for point in possible_holes}
        disjoint = [(left, right) for left in first for right in second if not set(left) & set(right)]
        independent_disjoint = [(left, right) for left in first for right in second
                                if all(point not in right for point in left)]
        assert disjoint == independent_disjoint
        assert len(disjoint) == (72 if name == 'III' else 96)
        catalogs[name] = (first, second, mixed)
        allowed = [matrix for matrix in matrices
                   if {decoded[matrix[encoded[point]]] for point in odd_pair} == set(odd_pair)
                   and {decoded[matrix[encoded[point]]] for point in mixed_pair} == set(mixed_pair)]
        assert len(allowed) == order // 8
        functional = (encoded[triple_sum] >> 3) & 7
        assert encoded[triple_sum] & 7 == 0
        fixing_shears = [matrix for matrix in symmetric if matrix[functional] == 0]
        assert len(fixing_shears) == 8
        group = []
        for matrix in allowed:
            dual = tuple(next(destination for destination in range(8)
                              if all(dot(matrix[1 << index], destination) == ((source >> index) & 1)
                                     for index in range(3))) for source in range(8))
            assert dual[functional] == functional
            for shear_matrix in fixing_shears:
                mapping = tuple(shear(decoded[matrix[bits & 7] | dual[(bits >> 3) & 7] << 3 | bits & 64],
                                      shear_matrix) for bits in range(128))
                by_point = tuple(mapping[encoded[point]] for point in range(128))
                assert len(set(by_point)) == 128 and by_point[127] == 127
                assert by_point[triple_sum] == triple_sum and by_point[pure_sum] == pure_sum
                assert {by_point[point] for point in characteristic} == set(characteristic)
                assert by_point[charge] == charge
                assert all(dot(left, right) == dot(by_point[left], by_point[right])
                           for left in range(128) for right in range(128))
                symplectic_pairs += 128 * 128
                for blocks in (first, second, anchored):
                    assert {tuple(sorted(by_point[point] for point in block)) for block in blocks} == set(blocks)
                for odd, blocks in zip(mixed_pair, mixed):
                    destination = mixed_pair.index(by_point[odd])
                    assert {tuple(sorted(by_point[point] for point in block)) for block in blocks} == set(mixed[destination])
                mapped_pairs = {(tuple(sorted(by_point[point] for point in left)),
                                 tuple(sorted(by_point[point] for point in right))) for left, right in disjoint}
                assert mapped_pairs == set(disjoint)
                group.append(by_point)
        group_set = set(group)
        assert len(group_set) == order and tuple(range(128)) in group_set
        for first_map in group:
            for second_map in group:
                assert tuple(first_map[second_map[point]] for point in range(128)) in group_set
                composition_points += 128
        actual_orbits = {tuple(sorted({mapping[point] for mapping in group})) for point in possible_holes}
        assert actual_orbits == set(expected_orbits)
        rows.append({'case': name, 'eta': eta, 'five_odd_projections': list(odd_pair),
                     'mixed_odd_projections': list(mixed_pair), 'three_even_sum': triple_sum,
                     'pure_six_sum': pure_sum, 'characteristic_projections': list(characteristic),
                     'characteristic_charge': charge, 'possible_pure_six_holes': list(possible_holes),
                     'five_even_triples': len(first), 'anchored_pure_six_blocks': len(second),
                     'pure_six_blocks_by_hole': dict(sorted(hole_histogram.items())),
                     'mixed_sextets_each': [len(blocks) for blocks in mixed],
                     'disjoint_defect_pairs': len(disjoint), 'marked_M_restrictions': len(allowed),
                     'pointwise_M_shears_fixing_r': len(fixing_shears), 'full_marked_stabilizer_order': order,
                     'actual_hole_orbits': sorted(actual_orbits), 'full_coloring_feasibility': 'untested'})

    role_controls = Counter()
    fiber_controls = Counter()
    inverse_class_controls = 0
    gram_entries = 0
    for odd_pair in combinations(sorted(holes), 2):
        for mixed_pair in combinations(sorted(holes - set(odd_pair)), 2):
            for functional in range(1, 8):
                if any(dot(encoded[odd], functional) != 1 for odd in odd_pair):
                    continue
                if dot(encoded[mixed_pair[0]], functional) != dot(encoded[mixed_pair[1]], functional):
                    continue
                first_odd, second_odd = odd_pair
                first_mixed, second_mixed = mixed_pair
                if dot(encoded[first_mixed], functional):
                    name = 'II'
                    half = (first_odd, first_mixed, first_odd ^ second_odd)
                elif vector_sum(odd_pair) == vector_sum(mixed_pair):
                    name = 'I'
                    half = (first_mixed, second_mixed, first_odd)
                else:
                    name = 'III'
                    assert vector_sum(odd_pair) in mixed_pair
                    if vector_sum(odd_pair) != first_mixed:
                        first_mixed, second_mixed = second_mixed, first_mixed
                    half = (first_mixed, second_mixed, first_odd)
                assert len(set(linear_values(half))) == 8
                duals = []
                for position in range(3):
                    duals.append(next(point for point in even
                                      if all(dot(point, half[index]) == int(index == position) for index in range(3))
                                      and all(not dot(point, previous) for previous in duals)))
                source_basis = half + tuple(duals) + (127,)
                assert all(dot(source_basis[left], source_basis[right]) == dot(basis[left], basis[right])
                           for left in range(7) for right in range(7))
                gram_entries += 49
                initial = dict(zip(linear_values(source_basis), decoded))
                assert len(initial) == 128
                target = next(row for row in rows if row['case'] == name)
                role_controls[name] += 1
                fiber = [point for point in even
                         if all(dot(point, hole) == dot(encoded[hole], functional) for hole in holes)]
                assert len(fiber) == 8
                for triple_sum in fiber:
                    image = initial[triple_sum]
                    shear_matrix = next(matrix for matrix in symmetric
                                        if shear(image, matrix) == target['three_even_sum'])
                    mapping = {point: shear(destination, shear_matrix) for point, destination in initial.items()}
                    assert len(set(mapping.values())) == 128 and mapping[127] == 127
                    assert mapping[triple_sum] == target['three_even_sum']
                    assert mapping[triple_sum ^ vector_sum(mixed_pair)] == target['pure_six_sum']
                    assert {mapping[point] for point in holes} == holes
                    assert {mapping[point] for point in odd_pair} == set(target['five_odd_projections'])
                    assert {mapping[point] for point in mixed_pair} == set(target['mixed_odd_projections'])
                    assert mapping[vector_sum(odd_pair + mixed_pair)] == target['characteristic_charge']
                    inverse = {destination: source for source, destination in mapping.items()}
                    first, second, mixed = catalogs[name]
                    for blocks, target_odd in ((first, target['five_odd_projections']), (second, ()),
                                               (mixed[0], (target['mixed_odd_projections'][0],)),
                                               (mixed[1], (target['mixed_odd_projections'][1],))):
                        for block in blocks:
                            original = tuple(inverse[point] for point in block) + tuple(127 ^ inverse[point] for point in target_odd)
                            assert all(dot(left, right) for left, right in combinations(original, 2))
                            inverse_class_controls += 1
                    fiber_controls[name] += 1
    assert role_controls == {'I': 42, 'II': 42, 'III': 84}
    assert fiber_controls == {'I': 336, 'II': 336, 'III': 672}
    prior = json.loads((root / 'results/dimension-7-five-four-Z-cover-check.json').read_text())
    assert prior['remaining_raw_profiles'] == {'five_six': 26, 'three_six': 39}
    profile = [3, 6, 6, 2, 8]
    assert [row for row in prior['remaining_raw_profile_lists']['five_six'] if row[-1] == 8] == [profile]
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'notes/dimension-seven-nineteen-obstruction.md', 'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-two-six-profiles.md', 'results/dimension-7-five-four-Z-cover-check.json')
    return {'status': 'three_six_profile_reduced_to_three_necessary_marked_forms', 'dimension': 7,
            'profile': profile, 'profile_columns': ['m5', 'm6', 'A', 'B', 'C'], 'characteristic_class_size': 4,
            'target_profile_excluded': False, 'target_profile_realized': False, 'normal_forms': rows,
            'even_triples': len(triples), 'even_sextets': len(sextets), 'even_heptads': len(heptads),
            'anchored_even_heptads': len(anchored), 'array_and_bitmask_catalogs_equal': True,
            'original_coordinate_class_controls': original_class_controls,
            'marked_role_functional_controls': dict(sorted(role_controls.items())),
            'all_r_fiber_normalization_controls': dict(sorted(fiber_controls.items())),
            'normalization_Gram_entries_checked': gram_entries,
            'inverse_original_class_controls': inverse_class_controls,
            'stabilizer_dot_product_pairs_checked': symplectic_pairs,
            'stabilizer_composition_points_checked': composition_points,
            'all_catalog_actions_and_disjoint_defect_pair_actions_checked': True,
            'remaining_raw_profiles': prior['remaining_raw_profiles'],
            'remaining_raw_profile_lists': prior['remaining_raw_profile_lists'],
            'exact_n7_chromatic_number': 'open', 'line_graph_lower_bound': 19,
            'full_subspace_graph_lower_bound': 19, 'new_numerical_lower_bound': False,
            'complete_necessary_roots_constructed': False, 'new_cover_search': False,
            'new_finite_cover_certificate': False, 'prior_cover_certificates_used_as_geometric_proof_inputs': False,
            'prior_spread_enumeration_rerun': False, 'Lean_run': False, 'independent_Pro_review': False,
            'manuscript_PDFs_changed': False, 'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-three-six-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written charge/hole reduction and full marked stabilizers, audited local catalogs and explicit isometries. No complete root family, cover search, profile exclusion, new Lean or Pro review; 26/39 candidates remain, exact n7 open >=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
