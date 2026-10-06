"""Check saturation of color sixteen in the full seven-line pattern only."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(left, right):
    return (left & right).bit_count() % 2


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    rows = bases(7, 3)
    spaces = {vertex: frozenset(span(row)) for vertex, row in enumerate(rows)
              if len(row) == 1 or all(dot(left, right) == 0 for left in row for right in row)}
    lookup = {space: vertex for vertex, space in spaces.items()}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    clique.append(lookup[frozenset((0, 127))])
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    special = {lookup[frozenset((0, 127 ^ vector))] for vector in isotropic if vector}
    adjacency = {vertex: set() for vertex in spaces}
    for vertex, neighbor in combinations(spaces, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    branch_fixed = {**fixed, **dict.fromkeys(special, 16)}
    branch_lists = {vertex: set(range(17)) - {branch_fixed[neighbor] for neighbor in adjacency[vertex] & branch_fixed.keys()}
                    for vertex in spaces if vertex not in branch_fixed}
    transverse = {vertex for vertex, palette in branch_lists.items() if 16 in palette}
    geometric_transverse = {vertex for vertex, space in spaces.items() if len(rows[vertex]) == 3
                            and space & isotropic == {0}}
    assert transverse == geometric_transverse and len(transverse) == 64
    color_class = special | transverse
    assert len(color_class) == 71 and not any(adjacency[vertex] & color_class for vertex in color_class)
    assert all(len(rows[vertex]) == 3 for vertex in transverse)
    assert all(palette == set(range(15)) | {16} for vertex, palette in branch_lists.items() if vertex in transverse)
    saturated_fixed = {**fixed, **dict.fromkeys(color_class, 16)}
    core = set(spaces) - set(saturated_fixed)
    palettes = {vertex: set(range(17)) - {saturated_fixed[neighbor] for neighbor in adjacency[vertex] & saturated_fixed.keys()}
                for vertex in core}
    for vertex in core:
        intersection = {vector for vector in isotropic if all(dot(vector, row) == 0 for row in rows[vertex])}
        geometric = {color for color, neighbor in enumerate(clique[:15]) if not spaces[neighbor] <= intersection}
        if any(row.bit_count() % 2 for row in rows[vertex]):
            geometric.add(15)
        assert palettes[vertex] == geometric and 16 not in palettes[vertex]
    edges = sum(len(adjacency[vertex] & core) for vertex in core) // 2
    vertex_clauses = sum(1 + len(palette) * (len(palette) - 1) // 2 for palette in palettes.values())
    edge_clauses = sum(len(palettes[vertex] & palettes[neighbor]) for vertex in core
                       for neighbor in adjacency[vertex] & core if neighbor < vertex)
    assert (len(core), edges, sum(map(len, palettes.values())), vertex_clauses + edge_clauses) == (490, 15386, 6286, 196350)
    return {'status': 'full_pattern_color16_saturation_and_residual_lists_counts_checked',
            'dimension': 7, 'pattern_mask': 127, 'scope_only_this_orbit': True,
            'seven_odd_lines_preassigned16': len(special), 'transverse_isotropic_triples_recolored16': len(transverse),
            'independent_color16_class_size': len(color_class), 'fixed_clique_vertices': len(fixed),
            'all_other_uncolored_vertices_forbid16_after_seven_line_assignment': True,
            'transverse_triple_lists_before_saturation': list(range(15)) + [16],
            'uncolored_vertices': len(core), 'uncolored_edges': edges,
            'uncolored_dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in core).items())),
            'variables': sum(map(len, palettes.values())), 'clauses': vertex_clauses + edge_clauses,
            'vertex_clauses': vertex_clauses, 'edge_clauses': edge_clauses,
            'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items())),
            'all490lists_checked_against_geometric_formula': True,
            'retained_pairs_directly_tested': len(spaces) * (len(spaces) - 1) // 2,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'shared_basis_helper_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'CNF_emitted': False, 'solver_run': False, 'lean_run': False,
            'full_n7_chromatic_number': 'open_lower_bound17',
            'scope': 'Onlyfullpatternmask127. Allremainingverticesallowing16are exactly64transverseLagrangiantriples; togetherwithsevenoddlines theyareindependent, so saturating16losesnocoloringwithinthisbranch. Counts/geometriclistschecked only; othernineorbitsremain, nobranchCNF/solve/upperbound/Lean.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
