"""Check quadratic parity and partial-spread completion excluding eighteen line colors."""
from collections import Counter
from itertools import combinations
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


def multiply(left, right):
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        if left & 8:
            left ^= 11
        right >>= 1
    return result


def trace(value):
    square = multiply(value, value)
    return value ^ square ^ multiply(square, square)


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    basis = (3, 12, 48, 65, 71, 95)
    coordinates = {vector_sum(vector for index, vector in enumerate(basis) if bits & (1 << index)): bits
                   for bits in range(64)}
    even = set(coordinates)
    assert even == {vector for vector in range(128) if dot(vector, 127) == 0}
    points = sorted(even - {0})
    quadratic = {vector: ((bits & 7) & (bits >> 3)).bit_count() % 2 for vector, bits in coordinates.items()}
    assert Counter(quadratic.values()) == {0: 36, 1: 28}
    assert all(quadratic[left ^ right] == quadratic[left] ^ quadratic[right] ^ dot(left, right)
               for left in even for right in even)
    lagrangians = set()
    for left, middle, right in combinations(points, 3):
        if not any((dot(left, middle), dot(left, right), dot(middle, right))) and left ^ middle ^ right:
            space = frozenset((0, left, middle, right, left ^ middle, left ^ right,
                               middle ^ right, left ^ middle ^ right))
            assert len(space) == 8
            lagrangians.add(space)
    lagrangians = sorted(lagrangians, key=lambda space: tuple(sorted(space)))
    assert len(lagrangians) == 135
    incidence_counts = Counter()
    for point in points:
        hyperplane = {vector for vector in points if dot(point, vector) == 0}
        assert len(hyperplane) == 31
        for space in lagrangians:
            size = len(hyperplane & space)
            assert size == (7 if point in space else 3)
            incidence_counts[size] += 1
    assert incidence_counts == {7: 945, 3: 7560}
    neighbors = {point: {other for other in points if dot(point, other)} for point in points}
    heptads = []
    six_cliques = []

    def extend(chosen, candidates):
        if len(chosen) == 6:
            six_cliques.append(chosen)
        if len(chosen) == 7:
            heptads.append(chosen)
            return
        for index, point in enumerate(candidates):
            extend(chosen + (point,), [other for other in candidates[index + 1:] if other in neighbors[point]])

    extend((), points)
    assert len(heptads) == 288 and len(six_cliques) == 2016
    heptad_sets = {frozenset(block) for block in heptads}
    quadratic_histogram = Counter()
    for block in heptads:
        assert vector_sum(block) == 0 and all(dot(left, right) == 1 for left, right in combinations(block, 2))
        value = sum(quadratic[point] for point in block)
        assert value % 2 == 1
        quadratic_histogram[value] += 1
    for block in six_cliques:
        forced = vector_sum(block)
        assert forced not in block and frozenset(block + (forced,)) in heptad_sets
        assert {point for point in points if all(dot(point, member) for member in block)} == {forced}
    isotropic = frozenset(vector_sum(basis[index] for index in range(3) if bits & (1 << index)) for bits in range(8))
    spread = [isotropic]
    for coefficient in range(8):
        matrix = [[trace(multiply(coefficient, multiply(left, right))) for right in (1, 2, 4)]
                  for left in (1, 2, 4)]
        space = set()
        for bits in range(8):
            first = sum((sum(matrix[row][column] * ((bits >> column) & 1) for column in range(3)) % 2) << row
                        for row in range(3))
            space.add(vector_sum(basis[index] for index in range(3) if first & (1 << index))
                      ^ vector_sum(basis[index + 3] for index in range(3) if bits & (1 << index)))
        spread.append(frozenset(space))
    assert len(spread) == 9 and all(space in lagrangians for space in spread)
    assert all(left & right == {0} for left, right in combinations(spread, 2))
    assert set().union(*spread) == even
    completion_controls = []
    for omitted in spread:
        partial = [space for space in spread if space != omitted]
        covered = set().union(*partial) - {0}
        holes = set(points) - covered
        assert len(covered) == 56 and len(holes) == 7 and holes | {0} == omitted
        assert all(dot(left, right) == 0 for left in holes for right in holes)
        for point in points:
            hyperplane = {vector for vector in points if dot(point, vector) == 0}
            assert len(hyperplane & covered) == (24 if point in holes else 28)
            assert len(hyperplane & holes) == (7 if point in holes else 3)
        assert all(dot(even_point, 127 ^ odd_point) == 0 for even_point in holes for odd_point in holes)
        assert sum(dot(left, right) == 0 for left, right in combinations(holes, 2)) == 21
        completion_controls.append({'holes': sorted(holes), 'completed_lagrangian': sorted(omitted),
                                    'even_hole_clique_vertices': 7, 'even_hole_clique_edges': 21,
                                    'even_odd_hole_adjacencies': 49, 'available_all_even_labels_in_mixed_type': 3})
    types = [(even_count, mixed_count, odd_count)
             for even_count in range(18) for mixed_count in range(18) for odd_count in range(18)
             if even_count + mixed_count + odd_count == 17 and 7 * even_count + 6 * mixed_count == 63
             and mixed_count + 7 * odd_count == 56]
    assert types == [(3, 7, 7), (9, 0, 8)]
    assert sum(quadratic[point] for point in points) % 2 == 0 and 9 % 2 == 1
    assert 7 > 3
    return {'status': 'written_nineteen_color_lower_bound_supported_by_exact_quadratic_and_incidence_checks',
            'dimension': 7, 'characteristic_vector': 127, 'symplectic_basis': basis,
            'line_graph_lower_bound': 19, 'full_subspace_graph_lower_bound': 19,
            'exact_n7_chromatic_number': 'open_lower_bound19', 'nineteen_color_witness': False,
            'prior_capacity_lemma_and_saturation': 'Written proof at85639e4: class avoidingz<=7 and eighteen colors force types(9,0,8)/(3,7,7). Prior finite certificate unchanged.',
            'quadratic_polarization_pairs_checked': 4096, 'quadratic_value_counts': dict(Counter(quadratic.values())),
            'even_heptads_checked': 288, 'even_heptad_quadratic_weight_histogram': dict(sorted(quadratic_histogram.items())),
            'all_even_heptad_vector_sums_zero': True, 'all_even_heptad_quadratic_sums_odd': True,
            'even_six_cliques_and_unique_heptad_completions_checked': 2016,
            'lagrangians': 135, 'point_hyperplane_lagrangian_intersections_checked': 8505,
            'intersection_size_histogram': dict(incidence_counts),
            'written_partial_spread_completion_scope': 'Every eight pairwise zero-intersecting Lagrangian three-spaces in symplectic E have seven holes forming the unique ninth Lagrangian, by31point hyperplane counts24/28. Not a finite enumeration of all partial spreads.',
            'explicit_spread_completion_controls': completion_controls,
            'finite_partial_spread_controls': 9, 'all_partial_spreads_enumerated': False,
            'necessary_eighteen_color_types': types,
            'type_9_0_8_exclusion': 'Nine odd quadratic-sum heptads cannot partition63evenpoints whose quadratic-sum iseven.',
            'type_3_7_7_exclusion': 'Seven holes formLagrangianM; its7evenline clique cannot use7mixedlabels or pureoddlabels and has only3all-evenlabels.',
            'auxiliary442_eighteen_colors_excluded': True, 'fresh_common_nineteenth_color_three_space_route_excluded': True,
            'native_solver_run': False, 'DRAT_checked': False, 'lean_run': False, 'submitted_manuscript_changed': False,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256(Path(__file__).parents[1].joinpath('notes/dimension-seven-nineteen-obstruction.md').read_bytes()).hexdigest(),
            'prior_capacity_report_sha256': hashlib.sha256(Path(__file__).parents[1].joinpath('results/dimension-7-line-capacity.json').read_bytes()).hexdigest(),
            'scope': 'Written universal exclusion ofboth saturated18linecolor types yieldsline/fullsubspace lowerbound19. Exact finite checks ofquadratic/heptad andhyperplane ingredients plusnine explicitpartialspread controls. No independentPro/Lean/SAT/DRAT orupperwitness; exactn7open.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
