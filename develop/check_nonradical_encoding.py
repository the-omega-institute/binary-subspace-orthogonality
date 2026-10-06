"""Independently reconstruct every nonradical-instance DIMACS clause geometrically."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(left, right):
    return (left & right).bit_count() % 2


def check(path, dimension, last_line=64):
    assert last_line in (64, 127) and (dimension == 7 or last_line == 64)
    rows = bases(dimension, 3)
    spaces = {vertex: frozenset(span(basis)) for vertex, basis in enumerate(rows)
              if len(basis) == 1 or all(dot(left, right) == 0 for left in span(basis) for right in span(basis))}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    fixed = set(clique)
    if dimension == 7:
        fixed.add(next(vertex for vertex, space in spaces.items() if space == {0, last_line}))
    core = sorted(spaces.keys() - fixed)
    palettes = {}
    for vertex in core:
        intersection = {vector for vector in isotropic if all(dot(vector, row) == 0 for row in rows[vertex])}
        palette = [color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= intersection]
        if dimension == 7:
            allows_fifteen = (any(vector.bit_count() % 2 for vector in spaces[vertex]) if last_line == 127
                              else any(dot(64, vector) for vector in spaces[vertex]))
            if allows_fifteen:
                palette.append(15)
            palette.append(16)
        palettes[vertex] = palette
    assert len(core) == (138 if dimension == 6 else 561)
    if dimension == 7:
        assert sum(palette == [15, 16] for palette in palettes.values()) == 7
        assert all(16 in palette for palette in palettes.values())
    variables = {(vertex, color): identifier + 1 for identifier, (vertex, color) in enumerate(
        (vertex, color) for vertex in core for color in palettes[vertex])}
    expected = set()
    vertex_clauses = 0
    for vertex in core:
        choices = [variables[vertex, color] for color in palettes[vertex]]
        expected.add(tuple(choices))
        vertex_clauses += 1
        for first, second in combinations(choices, 2):
            expected.add((-first, -second))
            vertex_clauses += 1
    edges = 0
    for vertex, neighbor in combinations(core, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            edges += 1
            for color in set(palettes[vertex]) & set(palettes[neighbor]):
                expected.add(tuple(sorted((-variables[vertex, color], -variables[neighbor, color]), reverse=True)))
    total = len(expected)
    header = None
    actual = 0
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        if line.startswith('p'):
            assert header is None
            header = line.split()
            assert header[:2] == ['p', 'cnf'] and list(map(int, header[2:])) == [len(variables), total]
            continue
        assert header is not None
        literals = [int(value) for value in line.split()]
        assert literals.pop() == 0 and all(literals)
        clause = tuple(sorted(literals, reverse=all(literal < 0 for literal in literals)))
        assert clause in expected, ('unexpected or duplicate clause', clause)
        expected.remove(clause)
        actual += 1
    assert header is not None and not expected and actual == total
    return {'status': 'every_dimacs_clause_exactly_matches_geometric_encoding', 'dimension': dimension,
            'fixed_last_line_basis': [last_line] if dimension == 7 else None,
            'target_colors': 15 if dimension == 6 else 17, 'core_vertices': len(core), 'core_edges': edges,
            'variables': len(variables), 'clauses': total, 'vertex_clauses': vertex_clauses, 'edge_clauses': total - vertex_clauses,
            'extra_preassigned_vertices': 0, 'former_forced_lines_keep_both15and16': dimension == 7,
            'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'scope': 'Every clause reconstructed from geometric lists and direct dot products without the search builder or its adjacency. Shared canonical basis enumerator/span helper only. No coloring, SAT, UNSAT or Lean conclusion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--last-line', type=int, choices=(64, 127), default=64)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.dimension == 6 and args.last_line != 64:
        parser.error('--last-line 127 applies only to dimension seven')
    report = check(args.cnf, args.dimension, args.last_line)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
