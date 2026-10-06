"""Check a nonradical-line retraction on every vertex and edge in dimensions six and seven."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


ROOT = Path(__file__).resolve().parents[1]


def dot(left, right):
    return (left & right).bit_count() % 2


def totally_isotropic(basis):
    return all(dot(left, right) == 0 for left in basis for right in basis)


def nonradical_target(basis):
    if len(basis) == 1 or totally_isotropic(basis):
        return basis
    return (min(vector for vector in basis if any(dot(vector, partner) for partner in basis)),)


def gaussian(dimension, rank):
    numerator = denominator = 1
    for index in range(rank):
        numerator *= 2 ** dimension - 2 ** index
        denominator *= 2 ** rank - 2 ** index
    return numerator // denominator


def number_of_subspaces(dimension):
    return sum(gaussian(dimension, rank) for rank in range(1, dimension + 1))


def perpendicular_basis(basis, dimension):
    perpendicular = [vector for vector in range(1 << dimension)
                     if all(dot(vector, row) == 0 for row in basis)]
    assert len(perpendicular) == 2 ** (dimension - len(basis))
    chosen = []
    generated = {0}
    for vector in perpendicular:
        if vector not in generated:
            chosen.append(vector)
            generated |= {value ^ vector for value in generated}
    assert generated == set(perpendicular)
    assert len(chosen) == dimension - len(basis)
    return chosen


def list_instance(rows, spaces, adjacency, clique, colors, dimension):
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    core = set(adjacency) - set(fixed)
    palettes = {vertex: set(range(colors)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in core}
    forced = {vertex: next(iter(palette)) for vertex, palette in palettes.items() if len(palette) == 1}
    if dimension == 7 and colors == 16:
        assert len(forced) == 7 and set(forced.values()) == {15}
    else:
        assert not forced
    for vertex, color in forced.items():
        assert all(fixed[neighbor] != color for neighbor in adjacency[vertex] & fixed.keys())
        assert all(forced[neighbor] != color for neighbor in adjacency[vertex] & forced.keys())
        for neighbor in adjacency[vertex] & core - forced.keys():
            palettes[neighbor].discard(color)
    core.difference_update(forced)
    fixed_space = frozenset(span((3, 12, 48)))
    for vertex in core:
        intersection = {vector for vector in fixed_space if all(dot(vector, row) == 0 for row in rows[vertex])}
        geometric = {color for color, fixed_vertex in enumerate(clique[:15])
                     if not spaces[fixed_vertex] <= intersection}
        if dimension == 7:
            if colors == 16:
                if 64 in {left ^ right for left in spaces[vertex] for right in fixed_space}:
                    geometric.add(15)
            else:
                if any(dot(64, row) for row in rows[vertex]):
                    geometric.add(15)
                geometric.add(16)
        assert palettes[vertex] == geometric and palettes[vertex]
    edges = sum(len(adjacency[vertex] & core) for vertex in core) // 2
    variables = sum(len(palettes[vertex]) for vertex in core)
    clauses = sum(1 + len(palettes[vertex]) * (len(palettes[vertex]) - 1) // 2 for vertex in core)
    clauses += sum(len(palettes[vertex] & palettes[neighbor]) for vertex in core
                   for neighbor in adjacency[vertex] & core if neighbor < vertex)
    if dimension == 7 and colors == 17:
        assert len(core) == 561
        assert all(16 in palettes[vertex] for vertex in core)
        assert sum(palettes[vertex] == {15, 16} for vertex in core) == 7
    return {'target_colors': colors, 'fixed_clique_vertices': len(clique),
            'extra_singleton_vertices': len(forced), 'uncolored_vertices': len(core),
            'uncolored_edges': edges, 'variables': variables, 'pairwise_clauses': clauses,
            'dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in core).items())),
            'palette_sizes': dict(sorted(Counter(len(palettes[vertex]) for vertex in core).items())),
            'geometric_lists_checked': len(core),
            'status': 'written_obstruction_rules_out_target' if dimension == 7 and colors == 16 else 'encoding_counts_only_no_coloring_or_solver',
            'fixed_color_rule': 'For seventeen colors the seven former forced lines retain both15and16; they are not preassigned. No color15 propagation or elimination is reused.' if dimension == 7 and colors == 17 else 'Original fixed clique and justified singleton assignments only.'}


def check(dimension):
    rows = bases(dimension, dimension)
    spaces = [frozenset(span(basis)) for basis in rows]
    lookup = {space: vertex for vertex, space in enumerate(spaces)}
    counts = dict(sorted(Counter(len(basis) for basis in rows).items()))
    assert len(lookup) == len(rows) == number_of_subspaces(dimension)
    assert counts == {rank: gaussian(dimension, rank) for rank in range(1, dimension + 1)}
    targets = [lookup[frozenset(span(nonradical_target(basis)))] for basis in rows]
    retained = [vertex for vertex, basis in enumerate(rows) if len(basis) == 1 or totally_isotropic(basis)]
    assert all(target in retained for target in targets)
    for vertex, target in enumerate(targets):
        assert spaces[target] <= spaces[vertex]
        if vertex in retained:
            assert vertex == target
        else:
            assert len(rows[target]) == 1
            assert any(dot(rows[target][0], partner) for partner in rows[vertex])
    adjacency = {vertex: set() for vertex in retained}
    for vertex, neighbor in combinations(retained, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    edges = low_edges = directed_degree_sum = 0
    for vertex, basis in enumerate(rows):
        perpendicular = perpendicular_basis(basis, dimension)
        mapped = [0]
        for vector in perpendicular:
            mapped += [value ^ vector for value in mapped]
        neighbors = set()
        for local in bases(len(perpendicular), len(perpendicular)):
            neighbor = lookup[frozenset(span([mapped[row] for row in local]))]
            assert neighbor not in neighbors
            neighbors.add(neighbor)
            if neighbor < vertex:
                first, second = targets[vertex], targets[neighbor]
                assert first != second and second in adjacency[first]
                edges += 1
                if len(basis) <= 3 and len(rows[neighbor]) <= 3:
                    low_edges += 1
        assert len(neighbors) == number_of_subspaces(dimension - len(basis))
        assert (vertex in neighbors) == totally_isotropic(basis)
        directed_degree_sum += len(neighbors) - (vertex in neighbors)
    assert directed_degree_sum == 2 * edges
    expected_sum = sum(counts[rank] * number_of_subspaces(dimension - rank) for rank in counts)
    expected_sum -= sum(totally_isotropic(basis) for basis in rows)
    assert expected_sum == 2 * edges
    assert edges == (44968 if dimension == 6 else 1160206)
    expected_retained = {1: 63, 2: 75, 3: 15} if dimension == 6 else {1: 127, 2: 315, 3: 135}
    assert dict(Counter(len(rows[vertex]) for vertex in retained)) == expected_retained
    fixed_space = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex in retained if spaces[vertex] <= fixed_space]
    if dimension == 7:
        clique.append(lookup[frozenset((0, 64))])
    assert all(neighbor in adjacency[vertex] for vertex, neighbor in combinations(clique, 2))
    control = None
    if dimension == 6:
        path = ROOT / 'results/full-15-coloring.json'
        previous = {frozenset(span(record['basis'])): record['color']
                    for record in json.loads(path.read_text())['subspace_colors']}
        assert all(previous[spaces[vertex]] != previous[spaces[neighbor]]
                   for vertex in retained for neighbor in adjacency[vertex])
        control = {'status': 'historical_witness_restricted_to_retained_graph_passed',
                   'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'old_full_graph_coloring_rerun': False}
    assert all(dot(3, row) == 0 for row in (3, 4))
    assert nonradical_target((3, 4)) == (4,)
    return {'status': 'every_vertex_and_full_graph_edge_retraction_checked', 'dimension': dimension,
            'all_vertices': len(rows), 'all_dimension_counts': counts,
            'retained_vertices': len(retained), 'retained_dimension_counts': expected_retained,
            'retained_pairs_directly_tested': len(retained) * (len(retained) - 1) // 2,
            'retained_edges': sum(map(len, adjacency.values())) // 2,
            'all_original_edges_checked': edges, 'low_dimension_edges_checked': low_edges,
            'edges_incident_to_high_dimensions_checked': edges - low_edges,
            'directed_degree_sum': directed_degree_sum,
            'edge_count_independent_gaussian_degree_formula_matches': True,
            'self_loops_excluded': True, 'edge_images_distinct': True,
            'radical_line_collapse_negative_control': 'The edge between span(3) and span(3,4) would collapse under a radical-line choice; the implemented rule selects span(4).',
            'coloring_instances': [list_instance(rows, spaces, adjacency, clique, colors, dimension)
                                  for colors in ([15] if dimension == 6 else [16, 17])],
            'n6_existing_witness_control': control,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256((ROOT / 'develop/dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False,
            'n7_exact_chromatic_number': 'open',
            'scope': 'Every vertex image and every original graph edge enumerated through exact orthogonal complements; retained adjacency tested directly on all pairs. Shared canonical RREF basis enumerator and span helper, new adjacency construction and product-formula counts. Written retraction establishes chromatic equivalence in every dimension. No new full coloring, emitted CNF, SAT, UNSAT solver or Lean result.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.dimension)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
