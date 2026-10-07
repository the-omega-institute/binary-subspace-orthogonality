"""Check the dominating color class and exact sixteen-color all14 branch reduction."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span
from encode_lines_planes_seventeen import build_encoding


def dot(left, right):
    return (left & right).bit_count() % 2


def verify_dominating_class(selected, spaces, edges):
    if not __debug__:
        raise RuntimeError('Run this validator without -O or PYTHONOPTIMIZE.')
    assert len(selected) == 8
    assert all(not (vertex in selected and neighbor in selected) for vertex, neighbor in edges)
    neighbors = {vertex: set() for vertex in spaces.keys() - selected}
    for vertex, neighbor in edges:
        if vertex in selected and neighbor not in selected:
            neighbors[neighbor].add(vertex)
        if neighbor in selected and vertex not in selected:
            neighbors[vertex].add(neighbor)
    assert all(neighbors.values())
    return neighbors


def check(output_cnf=None):
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    rows = bases(7, 2)
    spaces = {vertex: frozenset(span(row)) for vertex, row in enumerate(rows)
              if len(row) == 1 or all(dot(left, right) == 0 for left in span(row) for right in span(row))}
    lookup = {space: vertex for vertex, space in spaces.items()}
    isotropic = frozenset(span((3, 12, 48)))
    selected = {lookup[frozenset((0, 127 ^ vector))] for vector in isotropic}
    edges = [(vertex, neighbor) for vertex, neighbor in combinations(spaces, 2)
             if all(dot(left, right) == 0 for left in spaces[vertex] for right in spaces[neighbor])]
    neighbors = verify_dominating_class(selected, spaces, edges)
    characteristic = lookup[frozenset((0, 127))]
    assert len(spaces) == 442 and len(edges) == 16569
    degree_selected = {vertex: sum(vertex in edge for edge in edges) for vertex in selected}
    assert degree_selected[characteristic] == 378
    assert all(degree_selected[vertex] == 138 for vertex in selected - {characteristic})
    fixed = {vertex: color for color, vertex in enumerate(vertex for vertex in spaces if spaces[vertex] <= isotropic)}
    assert len(fixed) == 14
    remaining = spaces.keys() - selected
    core = sorted(remaining - fixed.keys())
    colors = tuple(range(14)) + (15, 16)
    palettes = {}
    for vertex in core:
        kernel = {vector for vector in isotropic if all(dot(vector, member) == 0 for member in spaces[vertex])}
        palettes[vertex] = [color for neighbor, color in fixed.items() if not spaces[neighbor] <= kernel] + [15, 16]
    core_edges = [(vertex, neighbor) for vertex, neighbor in edges if vertex in palettes and neighbor in palettes]
    remaining_edges = [(vertex, neighbor) for vertex, neighbor in edges if vertex in remaining and neighbor in remaining]
    assert (len(remaining), len(core), len(remaining_edges), len(core_edges)) == (434, 420, 15225, 14126)
    assert Counter(map(len, palettes.values())) == {12: 196, 15: 224}
    variables = {(vertex, color): identifier + 1 for identifier, (vertex, color) in enumerate(
        (vertex, color) for vertex in core for color in palettes[vertex])}
    clauses = []
    for vertex in core:
        choices = [variables[vertex, color] for color in palettes[vertex]]
        clauses.append(choices)
        clauses.extend([-left, -right] for left, right in combinations(choices, 2))
    vertex_clauses = len(clauses)
    for vertex, neighbor in core_edges:
        clauses.extend([-variables[vertex, color], -variables[neighbor, color]]
                       for color in sorted(set(palettes[vertex]) & set(palettes[neighbor])))
    assert (len(variables), vertex_clauses, len(clauses)) == (5712, 36876, 193900)
    geometric_clauses = {tuple(sorted(clause)) for clause in clauses}
    assert len(geometric_clauses) == len(clauses)
    original_rows, original_spaces, adjacency, original_fixed, original_palettes, original_variables, original_clauses, construction = build_encoding()
    assert original_rows == rows and original_spaces == spaces
    assert original_fixed[characteristic] == 14 and {vertex: color for vertex, color in original_fixed.items() if color != 14} == fixed
    assigned = {identifier: vertex in selected and color == 14 for (vertex, color), identifier in original_variables.items()
                if vertex in selected or color == 14}
    assert len(assigned) == 77 and sum(assigned.values()) == 7
    renumber = {original_variables[key]: identifier for key, identifier in variables.items()}
    assert original_variables.values() - assigned.keys() == renumber.keys()
    simplified = []
    for clause in original_clauses:
        if any(abs(literal) in assigned and assigned[abs(literal)] == (literal > 0) for literal in clause):
            continue
        reduced = [renumber[abs(literal)] * (1 if literal > 0 else -1) for literal in clause if abs(literal) not in assigned]
        assert reduced
        simplified.append(tuple(sorted(reduced)))
    assert len(simplified) == len(set(simplified)) == len(geometric_clauses)
    assert set(simplified) == geometric_clauses
    odd_core = [vertex for vertex in core if len(rows[vertex]) == 1 and dot(rows[vertex][0], 127)]
    assert len(odd_core) == 56
    assert all(len(neighbors[vertex]) == 4 for vertex in odd_core)
    assert all(color in colors and color != 14 for palette in palettes.values() for color in palette)
    even = {vertex for vertex in remaining if all(dot(vector, 127) == 0 for vector in spaces[vertex])}
    odd = remaining - even
    lagrangians = [frozenset(span(row)) for row in bases(7, 3)
                  if len(row) == 3 and all(dot(left, right) == 0 for left in row for right in row)]
    assert len(lagrangians) == 135 and len(even) == 378 and len(odd) == 56
    lagrangian_cliques = {lagrangian: {vertex for vertex in even if spaces[vertex] <= lagrangian}
                         for lagrangian in lagrangians}
    assert all(len(clique) == 14 for clique in lagrangian_cliques.values())
    memberships = 0
    for vertex in odd:
        point = rows[vertex][0] ^ 127
        containing = [lagrangian for lagrangian in lagrangians if point in lagrangian]
        assert len(containing) == 15
        covered = set().union(*(lagrangian_cliques[lagrangian] for lagrangian in containing))
        direct = {neighbor for neighbor in even if all(dot(left, right) == 0 for left in spaces[vertex] for right in spaces[neighbor])}
        assert covered == direct and len(direct) == 106
        memberships += len(direct)
    odd_edges = [(vertex, neighbor) for vertex, neighbor in remaining_edges if vertex in odd and neighbor in odd]
    assert len(odd_edges) == 784 and all(sum(vertex in edge for edge in odd_edges) == 28 for vertex in odd)
    rejected = {}
    for label, incomplete in [('missing_special_line', selected - {min(selected - {characteristic})}),
                              ('missing_characteristic_line', selected - {characteristic})]:
        try:
            verify_dominating_class(incomplete, spaces, edges)
        except AssertionError:
            rejected[label] = 'rejected'
        else:
            raise AssertionError(label)
    wrong_palette = set(palettes[odd_core[0]]) | {14}
    assert 14 in wrong_palette and neighbors[odd_core[0]]
    rejected['color14_retained_at_odd_core_line'] = 'conflicts_with_four_selected_neighbors'
    body = ('c all14-special-line branch target-colors 16 fixed-clique-size 14\n'
            + f'p cnf {len(variables)} {len(clauses)}\n'
            + ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses)).encode('ascii')
    if output_cnf:
        output_cnf.write_bytes(body)
        assert output_cnf.read_bytes() == body
    return {'status': 'dominating_independent_class_and_exact_branch_formula_checked',
            'dimension': 7, 'isotropic_basis': [3, 12, 48], 'characteristic_vector': 127,
            'selected_line_generators': sorted(rows[vertex][0] for vertex in selected),
            'selected_vertices': 8, 'selected_internal_edges': 0, 'dominated_vertices': len(neighbors),
            'selected_degree_histogram': dict(sorted(Counter(degree_selected.values()).items())),
            'remaining_vertices': len(remaining), 'remaining_edges': len(remaining_edges),
            'core_vertices': len(core), 'core_edges': len(core_edges), 'fixed_clique_size': 14,
            'branch_colors': colors, 'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items())),
            'variables': len(variables), 'clauses': len(clauses), 'vertex_clauses': vertex_clauses,
            'edge_clauses': len(clauses) - vertex_clauses, 'old_variables_assigned': len(assigned),
            'old_variables_assigned_true': sum(assigned.values()), 'unit_substitution_matches_all_geometric_clauses': True,
            'outside_odd_lines': 56, 'selected_neighbors_per_outside_odd_line': 4,
            'even_vertices': len(even), 'odd_vertices': len(odd), 'lagrangian_fourteen_cliques': len(lagrangian_cliques),
            'lagrangians_per_outside_point': 15, 'even_neighbors_per_odd_vertex': 106,
            'even_odd_neighbor_memberships_checked': memberships, 'odd_graph_edges': len(odd_edges), 'odd_graph_degree': 28,
            'written_extension_criterion': 'For a proper16coloring of the378evenvertices, eachLagrangian14clique omits a pairM(L). The exact allowedlist at oddpoint e outsideT is I(e)=intersection ofM(L) over15L containinge, with no fallbackcolor. Extension iff the56vertex oddgraph admits a proper listcoloring fromI. Nonemptylists and cliqueHall |unionI|>=|C| are necessary, not alone sufficient.',
            'negative_controls': rejected, 'cnf_sha256': hashlib.sha256(body).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'shared_RREF_span_helper_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'cross_checked_base_builder_sha256': hashlib.sha256(Path(__file__).with_name('encode_lines_planes_seventeen.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False, 'branch_solved': False,
            'other_31_orbits_retained': True, 'full_n7_chromatic_number': 'open_lower_bound18',
            'scope': 'Written all14 branch equivalence to16coloring the434vertex inducedgraph. Fullspan geometry and exactbaseCNF substitution checked, sharingRREF/span helpers only before builder crosscheck. No coloring, UNSAT, branch exclusion or newbound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--output-cnf', type=Path)
    args = parser.parse_args()
    result = check(args.output_cnf)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
