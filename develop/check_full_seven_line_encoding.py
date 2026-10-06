"""Audit every saturated mask127 clause from geometric lists and full spans."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(left, right):
    return (left & right).bit_count() % 2


def geometric_encoding():
    rows = bases(7, 3)
    spaces = {vertex: frozenset(span(basis)) for vertex, basis in enumerate(rows)
              if len(basis) == 1 or all(dot(left, right) == 0 for left in span(basis) for right in span(basis))}
    isotropic = frozenset(span((3, 12, 48)))
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    characteristic = next(vertex for vertex, space in spaces.items() if space == {0, 127})
    special = {vertex for vertex, space in spaces.items() if len(space) == 2
               and next(iter(space - {0})) ^ 127 in isotropic - {0}}
    transverse = {vertex for vertex, space in spaces.items() if len(space) == 8 and space & isotropic == {0}}
    fixed = set(clique) | {characteristic} | special | transverse
    assert (len(clique), len(special), len(transverse), len(fixed)) == (15, 7, 64, 87)
    core = sorted(spaces.keys() - fixed)
    palettes = {}
    for vertex in core:
        kernel = {vector for vector in isotropic if all(dot(vector, other) == 0 for other in spaces[vertex])}
        palette = [color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= kernel]
        if any(vector.bit_count() % 2 for vector in spaces[vertex]):
            palette.append(15)
        palettes[vertex] = palette
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
        if all(dot(left, right) == 0 for left in spaces[vertex] for right in spaces[neighbor]):
            edges += 1
            for color in set(palettes[vertex]) & set(palettes[neighbor]):
                expected.add(tuple(sorted((-variables[vertex, color], -variables[neighbor, color]))))
    assert (len(core), edges, len(variables), len(expected), vertex_clauses) == (490, 15386, 6286, 196350, 38136)
    return variables, expected, {'core_vertices': len(core), 'core_edges': edges, 'variables': len(variables),
                                 'clauses': len(expected), 'vertex_clauses': vertex_clauses,
                                 'edge_clauses': len(expected) - vertex_clauses,
                                 'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items()))}


def audit_bytes(contents, variable_count, expected):
    remaining = set(expected)
    lines = contents.decode('ascii').splitlines()
    assert lines[0] == 'c full-seven-line-pattern-mask 127 saturated-color16-class 71'
    assert lines[1].split() == ['p', 'cnf', str(variable_count), str(len(expected))]
    actual = 0
    for line in lines[2:]:
        literals = [int(value) for value in line.split()]
        assert literals and literals.pop() == 0
        assert literals and all(0 < abs(literal) <= variable_count for literal in literals)
        clause = tuple(sorted(literals))
        assert clause in remaining, ('unexpected or duplicate clause', clause)
        remaining.remove(clause)
        actual += 1
    assert not remaining and actual == len(expected), ('missing clauses', len(remaining))


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
                    'wrong_branch_marker': contents.replace(b'pattern-mask 127', b'pattern-mask 126', 1),
                    'illegal_color_variable': b''.join(lines[:-1]) + b'-6287 -1 0\n'}
        for label, variant in variants.items():
            try:
                audit_bytes(variant, len(variables), expected)
            except AssertionError:
                control_results[label] = 'rejected'
            else:
                raise AssertionError(('negative control accepted', label))
    return {'status': 'every_mask127_clause_exactly_matches_independent_geometric_encoding',
            'dimension': 7, 'pattern_mask': 127, 'fixed_clique_vertices': 16,
            'independent_color16_class_size': 71, **counts,
            'cnf_sha256': hashlib.sha256(contents).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'negative_controls': control_results, 'solver_run': False, 'lean_run': False,
            'scope': 'Mask127 only. Every clause checked exactly once against geometric lists and full-span orthogonality. Shares only canonical RREF/span helpers, not the builder or adjacency. Other nine patterns remain; no SAT/UNSAT or upper bound.'}


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
