"""Audit a DIMACS instance from geometric lists and direct dot products."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(left, right):
    return (left & right).bit_count() % 2


def check(path, dimension):
    rows = bases(dimension, 3)
    isotropic = set(span((3, 12, 48)))
    spaces = {vertex: set(span(basis)) for vertex, basis in enumerate(rows)
              if len(basis) == 1 or (len(basis) == 2 and all(vector.bit_count() % 2 == 0 for vector in span(basis)))
              or all(dot(left, right) == 0 for left in span(basis) for right in span(basis))}
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    forced_spaces = [{0, 64 ^ vector} for vector in isotropic] if dimension == 7 else []
    core = [vertex for vertex, space in spaces.items() if vertex not in clique and space not in forced_spaces]
    palettes = {}
    for vertex in core:
        intersection = {vector for vector in isotropic if all(dot(vector, row) == 0 for row in rows[vertex])}
        palettes[vertex] = [color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= intersection]
        if dimension == 7:
            assert not any(64 ^ vector in spaces[vertex] for vector in isotropic)
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
    original_count = len(expected)
    header = None
    actual_count = 0
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        if line.startswith('p'):
            assert header is None
            header = line.split()
            assert header[:2] == ['p', 'cnf']
            assert list(map(int, header[2:])) == [len(variables), original_count]
            continue
        assert header is not None
        literals = [int(value) for value in line.split()]
        assert literals.pop() == 0 and all(literals)
        clause = tuple(sorted(literals, reverse=all(literal < 0 for literal in literals)))
        assert clause in expected, ('unexpected or duplicate clause', clause)
        expected.remove(clause)
        actual_count += 1
    assert header is not None and not expected and actual_count == original_count
    return {'status': 'every_dimacs_clause_exactly_matches_geometric_encoding', 'dimension': dimension,
            'core_vertices': len(core), 'core_edges': edges, 'variables': len(variables),
            'clauses': actual_count, 'vertex_clauses': vertex_clauses, 'edge_clauses': actual_count - vertex_clauses,
            'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'scope': 'Independent clause construction from geometric lists and direct basis adjacency, sharing only the canonical basis enumerator. No SAT, UNSAT or Lean conclusion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.cnf, args.dimension)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
