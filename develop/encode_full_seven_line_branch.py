"""Emit the saturated mask127 branch as a deterministic list-coloring CNF."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


ROOT = Path(__file__).resolve().parents[1]
MARKER = 'c full-seven-line-pattern-mask 127 saturated-color16-class 71'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_encoding():
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    rows = bases(7, 3)
    retained = [vertex for vertex, basis in enumerate(rows) if len(basis) == 1
                or all((left & right).bit_count() % 2 == 0 for left in basis for right in basis)]
    spaces = {vertex: frozenset(span(rows[vertex])) for vertex in retained}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex in retained if spaces[vertex] <= isotropic]
    clique.append(next(vertex for vertex in retained if rows[vertex] == (127,)))
    special = {vertex for vertex in retained if len(rows[vertex]) == 1
               and rows[vertex][0] ^ 127 in isotropic - {0}}
    transverse = {vertex for vertex in retained if len(rows[vertex]) == 3
                  and spaces[vertex] & isotropic == {0}}
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    fixed.update(dict.fromkeys(special | transverse, 16))
    assert (len(retained), len(clique), len(special), len(transverse), len(fixed)) == (577, 16, 7, 64, 87)
    adjacency = {vertex: set() for vertex in retained}
    for vertex, neighbor in combinations(retained, 2):
        if all((left & right).bit_count() % 2 == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    assert all(fixed[vertex] != fixed[neighbor] for vertex in fixed for neighbor in adjacency[vertex] & fixed.keys())
    palettes = {vertex: sorted(set(range(17)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()})
                for vertex in retained if vertex not in fixed}
    assert all(palette and 16 not in palette for palette in palettes.values())
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
    assert (len(palettes), edges, len(variables), len(clauses), vertex_clauses) == (490, 15386, 6286, 196350, 38136)
    report = {'dimension': 7, 'target_colors': 17, 'pattern_mask': 127,
              'retained_vertices': len(retained), 'fixed_clique_vertices': len(clique),
              'independent_color16_class_size': len(special | transverse),
              'fixed_vertices': len(fixed), 'core_vertices': len(palettes), 'core_edges': edges,
              'variables': len(variables), 'clauses': len(clauses), 'vertex_clauses': vertex_clauses,
              'edge_clauses': len(clauses) - vertex_clauses,
              'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items())),
              'builder_sha256': digest(Path(__file__)),
              'basis_enumerator_sha256': digest(ROOT / 'develop/dimension_seven_feasibility.py'),
              'branch_note_sha256': digest(ROOT / 'notes/full-seven-line-branch.md'),
              'solver_run': False, 'lean_run': False}
    return rows, spaces, adjacency, fixed, palettes, variables, clauses, report


def encode_bytes(variables, clauses):
    header = f'{MARKER}\np cnf {len(variables)} {len(clauses)}\n'
    body = ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses)
    return (header + body).encode('ascii')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    rows, spaces, adjacency, fixed, palettes, variables, clauses, report = build_encoding()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / 'dimension-7-full-seven-line-branch.cnf'
    path.write_bytes(encode_bytes(variables, clauses))
    report.update(status='mask127_saturated_branch_CNF_emitted_no_solver_run', cnf_sha256=digest(path))
    (args.output_dir / 'dimension-7-full-seven-line-branch-encoding.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
