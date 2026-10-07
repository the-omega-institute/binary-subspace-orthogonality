"""Encode the sufficient lines-and-isotropic-planes seventeen-color construction."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


MARKER = 'c lines-isotropic-planes target-colors 17 fixed-clique-size 15'


def build_encoding():
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    rows = bases(7, 2)
    retained = [vertex for vertex, basis in enumerate(rows) if len(basis) == 1
                or all((first & second).bit_count() % 2 == 0 for first in basis for second in basis)]
    spaces = {vertex: frozenset(span(rows[vertex])) for vertex in retained}
    fixed_space = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex in retained if spaces[vertex] <= fixed_space]
    characteristic = next(vertex for vertex in retained if spaces[vertex] == frozenset((0, 127)))
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    fixed[characteristic] = 14
    assert len(retained) == 442 and len(clique) == 14 and len(fixed) == 15
    adjacency = {vertex: set() for vertex in retained}
    for vertex, neighbor in combinations(retained, 2):
        if all((first & second).bit_count() % 2 == 0 for first in rows[vertex] for second in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    assert sum(map(len, adjacency.values())) == 2 * 16569
    assert all(neighbor in adjacency[vertex] for vertex, neighbor in combinations(fixed, 2))
    palettes = {vertex: sorted(set(range(17)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()})
                for vertex in retained if vertex not in fixed}
    special = [vertex for vertex in palettes if len(rows[vertex]) == 1 and rows[vertex][0] ^ 127 in fixed_space]
    assert len(special) == 7 and all(palettes[vertex] == [14, 15, 16] for vertex in special)
    assert all(15 in palette and 16 in palette for palette in palettes.values())
    variables = {(vertex, color): identifier + 1 for identifier, (vertex, color) in enumerate(
        (vertex, color) for vertex in sorted(palettes) for color in palettes[vertex])}
    clauses = []
    for vertex, palette in sorted(palettes.items()):
        choices = [variables[vertex, color] for color in palette]
        clauses.append(choices)
        clauses.extend([-first, -second] for first, second in combinations(choices, 2))
    vertex_clauses = len(clauses)
    edges = 0
    for vertex in sorted(palettes):
        for neighbor in sorted(adjacency[vertex] & palettes.keys()):
            if neighbor < vertex:
                edges += 1
                clauses.extend([-variables[vertex, color], -variables[neighbor, color]]
                               for color in sorted(set(palettes[vertex]) & set(palettes[neighbor])))
    assert len(palettes) == 427 and len(variables) == 5789 and vertex_clauses == 37576
    report = {'dimension': 7, 'target_colors': 17, 'construction': 'separate_eighteenth_color_for_all_isotropic_three_spaces',
              'retained_vertices': 442, 'retained_edges': 16569, 'fixed_clique_vertices': 15,
              'fixed_clique': [{'basis': rows[vertex], 'color': color} for vertex, color in fixed.items()],
              'core_vertices': len(palettes), 'core_edges': edges, 'variables': len(variables),
              'clauses': len(clauses), 'vertex_clauses': vertex_clauses, 'edge_clauses': len(clauses) - vertex_clauses,
              'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items())),
              'special_line_lists': [{'generator': rows[vertex][0], 'colors': palettes[vertex]} for vertex in special],
              'both_extra_colors_available_everywhere': True, 'old_full_graph_seventeen_color_forcing_used': False,
              'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
              'solver_run': False, 'lean_run': False,
              'scope': 'Exact seventeen-color encoding of the 442-vertex lines/planes graph. SAT would give a sufficient eighteen-color construction after adding the independent three-spaces and validating the original lift. UNSAT only rejects this route, not full eighteen-colorability.'}
    return rows, spaces, adjacency, fixed, palettes, variables, clauses, report


def encode_bytes(variables, clauses):
    header = f'{MARKER}\np cnf {len(variables)} {len(clauses)}\n'
    return (header + ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses)).encode('ascii')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    rows, spaces, adjacency, fixed, palettes, variables, clauses, report = build_encoding()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / 'dimension-7-lines-planes-17.cnf'
    path.write_bytes(encode_bytes(variables, clauses))
    report.update(status='lines_planes_seventeen_color_CNF_emitted', cnf_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (args.output_dir / 'dimension-7-lines-planes-17-encoding.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
