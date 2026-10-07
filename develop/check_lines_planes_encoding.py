"""Audit every lines/planes clause using geometric lists and full-span adjacency."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(first, second):
    return (first & second).bit_count() % 2


def geometric_encoding():
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    rows = bases(7, 2)
    spaces = {vertex: frozenset(span(basis)) for vertex, basis in enumerate(rows)
              if len(basis) == 1 or all(dot(first, second) == 0 for first in span(basis) for second in span(basis))}
    fixed_space = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex, space in spaces.items() if space <= fixed_space]
    characteristic = next(vertex for vertex, space in spaces.items() if space == frozenset((0, 127)))
    core = sorted(spaces.keys() - set(clique) - {characteristic})
    assert len(clique) == 14 and len(core) == 427
    palettes = {}
    for vertex in core:
        kernel = {vector for vector in fixed_space if all(dot(vector, member) == 0 for member in spaces[vertex])}
        palettes[vertex] = [color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= kernel]
        if len(spaces[vertex]) == 2 and dot(next(iter(spaces[vertex] - {0})), 127) == 1:
            palettes[vertex].append(14)
        palettes[vertex].extend((15, 16))
    variables = {(vertex, color): identifier + 1 for identifier, (vertex, color) in enumerate(
        (vertex, color) for vertex in core for color in palettes[vertex])}
    expected = set()
    vertex_clauses = 0
    for vertex in core:
        choices = tuple(variables[vertex, color] for color in palettes[vertex])
        expected.add(choices)
        vertex_clauses += 1
        for first, second in combinations(choices, 2):
            expected.add(tuple(sorted((-first, -second))))
            vertex_clauses += 1
    edges = 0
    for vertex, neighbor in combinations(core, 2):
        if all(dot(first, second) == 0 for first in spaces[vertex] for second in spaces[neighbor]):
            edges += 1
            for color in set(palettes[vertex]) & set(palettes[neighbor]):
                expected.add(tuple(sorted((-variables[vertex, color], -variables[neighbor, color]))))
    assert len(variables) == 5789 and vertex_clauses == 37576
    return variables, expected, {'core_vertices': len(core), 'core_edges': edges, 'variables': len(variables),
                                 'clauses': len(expected), 'vertex_clauses': vertex_clauses,
                                 'edge_clauses': len(expected) - vertex_clauses,
                                 'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items()))}


def audit_bytes(contents, variable_count, expected):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    remaining = set(expected)
    lines = contents.decode('ascii').splitlines()
    assert len(lines) >= 2 and lines[0] == 'c lines-isotropic-planes target-colors 17 fixed-clique-size 15'
    assert lines[1].split() == ['p', 'cnf', str(variable_count), str(len(expected))]
    for line in lines[2:]:
        literals = [int(value) for value in line.split()]
        assert literals
        terminator = literals.pop()
        assert terminator == 0 and literals and all(0 < abs(literal) <= variable_count for literal in literals)
        clause = tuple(sorted(literals))
        assert clause in remaining, ('unexpected or duplicate clause', clause)
        remaining.remove(clause)
    assert not remaining, ('missing clauses', len(remaining))


def check(path, controls=False):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    variables, expected, counts = geometric_encoding()
    contents = path.read_bytes()
    audit_bytes(contents, len(variables), expected)
    control_results = {}
    if controls:
        lines = contents.splitlines(keepends=True)
        variants = {'missing_clause': b''.join(lines[:-1]),
                    'duplicate_replaces_last_clause': b''.join(lines[:-1] + [lines[2]]),
                    'wrong_construction_marker': contents.replace(b'target-colors 17', b'target-colors 18', 1),
                    'illegal_variable': b''.join(lines[:-1]) + b'-5790 -1 0\n',
                    'incomplete_positive_choice': b''.join(lines[:2]) + b'1 0\n' + b''.join(lines[3:]),
                    'interior_zero': b''.join(lines[:-1]) + b'-1 0 -2 0\n'}
        for label, variant in variants.items():
            try:
                audit_bytes(variant, len(variables), expected)
            except AssertionError:
                control_results[label] = 'rejected'
            else:
                raise AssertionError(('negative control accepted', label))
    return {'status': 'every_lines_planes_clause_matches_independent_geometric_encoding',
            'dimension': 7, 'target_colors': 17, 'retained_vertices': 442, 'fixed_clique_vertices': 15, **counts,
            'cnf_sha256': hashlib.sha256(contents).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'negative_controls': control_results, 'solver_run': False, 'lean_run': False,
            'scope': 'Every clause checked exactly once from geometric lists and full-span dot products. Shares only canonical RREF/span helpers. This is a sufficient eighteen-color construction, not an equivalent restriction. No coloring or chromatic bound from this audit.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.cnf, args.controls)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
