"""Exhaust the dimension-seven line-class capacities and auxiliary-route obstruction."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def rank(vectors):
    pivots = {}
    for vector in vectors:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length()
            if pivot not in pivots:
                pivots[pivot] = reduced
                break
            reduced ^= pivots[pivot]
    return len(pivots)


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def members(bitset):
    return [vector for vector in range(128) if bitset & (1 << vector)]


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    even = [vector for vector in range(128) if dot(vector, 127) == 0]
    assert len(even) == 64 and even[0] == 0
    isotropic = {0, 3, 12, 15, 48, 51, 60, 63}
    even_nonzero = even[1:]
    deleted_characteristic_domain = mask(even_nonzero)
    all14_domain = mask(vector for vector in even if vector not in isotropic)
    all_even = mask(even)
    lagrangians = set()
    independent_triples = 0
    for left, middle, right in combinations(even_nonzero, 3):
        if not any((dot(left, middle), dot(left, right), dot(middle, right))) and left ^ middle ^ right:
            vectors = {0, left, middle, right, left ^ middle, left ^ right, middle ^ right, left ^ middle ^ right}
            assert len(vectors) == 8 and all(dot(first, second) == 0 for first in vectors for second in vectors)
            lagrangians.add(mask(vectors))
            independent_triples += 1
    lagrangians = sorted(lagrangians)
    assert len(lagrangians) == 135 and independent_triples == 135 * 28
    assert mask(isotropic) in lagrangians
    neighbors = {vector: {other for other in even_nonzero if dot(vector, other)} for vector in even_nonzero}
    availability = {vector: mask(other for other in even if dot(vector, other)) for vector in even_nonzero}
    class_counts = Counter()
    affine_histograms = {size: Counter() for size in range(8)}
    deleted_histograms = {size: Counter() for size in range(8)}
    all14_histograms = {size: Counter() for size in range(8)}
    maxima = {size: 0 for size in range(8)}
    all14_maxima = {size: 0 for size in range(8)}
    witnesses = {}
    maximum_total = maximum_all14_total = 0
    bounds = (7, 4, 4, 2, 2, 1, 1, 0)

    def extend(chosen, candidates, allowed):
        nonlocal maximum_total, maximum_all14_total
        size = len(chosen)
        assert size <= 7
        class_counts[size] += 1
        assert all(dot(left, right) == 1 for left, right in combinations(chosen, 2))
        assert allowed == mask(vector for vector in even if all(dot(vector, selected) == 1 for selected in chosen))
        dimension = rank(chosen)
        if dimension == size:
            assert allowed.bit_count() == 2 ** (6 - dimension)
        else:
            assert size % 2 == 1 and dimension == size - 1 and not allowed
        vector_sum = 0
        for vector in chosen:
            vector_sum ^= vector
        if size == 6:
            assert allowed == mask([vector_sum])
        if dimension < size:
            assert vector_sum == 0
        affine_histograms[size][allowed.bit_count()] += 1
        intersections = [allowed & space & deleted_characteristic_domain for space in lagrangians]
        all14_intersections = [allowed & space & all14_domain for space in lagrangians]
        capacity = max(intersection.bit_count() for intersection in intersections)
        all14_capacity = max(intersection.bit_count() for intersection in all14_intersections)
        assert capacity <= bounds[size] and all14_capacity <= bounds[size]
        deleted_histograms[size][capacity] += 1
        all14_histograms[size][all14_capacity] += 1
        maxima[size] = max(maxima[size], capacity)
        all14_maxima[size] = max(all14_maxima[size], all14_capacity)
        maximum_total = max(maximum_total, size + capacity)
        maximum_all14_total = max(maximum_all14_total, size + all14_capacity)
        if size not in witnesses or witnesses[size]['odd_count'] < capacity:
            odd_points = members(next(intersection for intersection in intersections if intersection.bit_count() == capacity))
            line_class = list(chosen) + [127 ^ point for point in odd_points]
            assert 127 not in line_class and all(dot(left, right) == 1 for left, right in combinations(line_class, 2))
            witnesses[size] = {'even_generators': list(chosen), 'odd_even_points': odd_points,
                               'odd_generators': [127 ^ point for point in odd_points], 'odd_count': capacity,
                               'total_count': len(line_class)}
        for position, vector in enumerate(candidates):
            remaining = [other for other in candidates[position + 1:] if other in neighbors[vector]]
            extend(chosen + (vector,), remaining, allowed & availability[vector])

    extend((), even_nonzero, all_even)
    assert dict(class_counts) == {0: 1, 1: 63, 2: 1008, 3: 5376, 4: 10080, 5: 8064, 6: 2016, 7: 288}
    assert tuple(maxima.values()) == tuple(all14_maxima.values()) == bounds
    assert maximum_total == maximum_all14_total == 7
    assert max((space & all_even).bit_count() for space in lagrangians) == 8
    assert all(space & 1 for space in lagrangians)
    lines = set(range(1, 128))
    removed = {127 ^ vector for vector in isotropic}
    without_characteristic = lines - {127}
    all14_lines = lines - removed
    edges = {edge for edge in combinations(sorted(lines), 2) if dot(*edge) == 0}
    deleted_edges = {edge for edge in edges if set(edge) <= without_characteristic}
    all14_edges = {edge for edge in edges if set(edge) <= all14_lines}
    assert len(edges) == 3969 and len(deleted_edges) == 3906 and len(all14_edges) == 3465
    assert len(without_characteristic) == 126 and len(all14_lines) == 119 and 127 in removed
    capacity_diagnostics = {}
    for label, vertex_count, proposed_colors in (
        ('all14_sixteen_colors', 119, 16), ('deleted_characteristic_seventeen_colors', 126, 17),
    ):
        assert vertex_count > proposed_colors * maximum_total
        capacity_diagnostics[label] = {'vertices': vertex_count, 'colors': proposed_colors,
                                       'available_capacity': proposed_colors * maximum_total, 'deficit': vertex_count - proposed_colors * maximum_total}
    saturated_types = [{'seven_even_classes': even_classes, 'six_even_one_odd_classes': mixed_classes,
                        'seven_odd_classes': odd_classes}
                       for even_classes in range(18) for mixed_classes in range(18) for odd_classes in range(18)
                       if 7 * even_classes + 6 * mixed_classes == 63 and mixed_classes + 7 * odd_classes == 56
                       and even_classes + mixed_classes + odd_classes == 17]
    assert saturated_types == [{'seven_even_classes': 3, 'six_even_one_odd_classes': 7, 'seven_odd_classes': 7},
                               {'seven_even_classes': 9, 'six_even_one_odd_classes': 0, 'seven_odd_classes': 8}]
    return {
        'status': 'written_line_lower_bound18_and_entire_auxiliary17_route_exclusion_finitely_checked',
        'dimension': 7, 'characteristic_vector': 127, 'line_graph_vertices': 127, 'line_graph_edges': 3969,
        'deleted_characteristic_vertices': 126, 'deleted_characteristic_edges': 3906,
        'deleted_characteristic_maximum_independent_class': 7, 'line_graph_lower_bound': 18,
        'all14_line_vertices': 119, 'all14_line_edges': 3465, 'all14_line_lower_bound': 17,
        'isotropic_basis': [3, 12, 48], 'removed_line_generators': sorted(removed),
        'lagrangians': 135, 'isotropic_independent_triples': independent_triples,
        'even_color_classes_checked': sum(class_counts.values()), 'even_color_class_counts_by_size': dict(class_counts),
        'exact_affine_availability_histograms': affine_histograms,
        'exact_odd_capacity_histograms_deleted_characteristic': deleted_histograms,
        'exact_odd_capacity_histograms_all14': all14_histograms,
        'maximum_odd_capacity_by_even_count': maxima, 'maximum_all14_odd_capacity_by_even_count': all14_maxima,
        'maximum_total_class_size': 7, 'capacity_witnesses': witnesses,
        'all135_intersections_per_domain_per_even_class_checked': True,
        'capacity_budget_diagnostics': capacity_diagnostics,
        'necessary_saturated_line18_partition_types': saturated_types,
        'saturated_partitions_realized': False,
        'auxiliary442_graph_seventeen_coloring_possible': False,
        'all32_ternary_orbits_excluded_by_written_line_obstruction': True,
        'all14_branch_excluded_by_written_line_obstruction': True,
        'CNF_UNSAT_solver_run': False, 'DRAT_proof_checked': False, 'native_solver_run': False, 'lean_run': False,
        'full_n7_chromatic_number': 'open_lower_bound18', 'new_fullgraph_lower_bound': False,
        'full18color_witness': False, 'line18color_witness': False,
        'submitted_manuscript_changed': False,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_note_sha256': hashlib.sha256(Path(__file__).parents[1].joinpath('notes/dimension-seven-line-capacity.md').read_bytes()).hexdigest(),
        'scope': 'Written capacity proof excludes17colors already onall127lines and excludes16colors on119all14lines; exhaustive coordinate-only capacity validation over26896evenclasses and135Lagrangians. No CNF solver/proof, new fullgraph bound, eighteen-color witness or Lean. Historical unknown reports retained.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
