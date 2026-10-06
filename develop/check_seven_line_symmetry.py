"""Check orthogonal lifts and ten symmetry classes of the seven two-color lines."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

from check_nonradical_encoding import check as check_encoding
from dimension_seven_feasibility import bases, span


ROOT = Path(__file__).resolve().parents[1]
ISOTROPIC_BASIS = (3, 12, 48)
DUAL_BASIS = (65, 71, 95)
CHARACTERISTIC = 127


def dot(left, right):
    return (left & right).bit_count() % 2


def combine(coordinates, basis):
    vector = 0
    for index, row in enumerate(basis):
        if coordinates >> index & 1:
            vector ^= row
    return vector


def transform_mask(mask, permutation):
    return sum(1 << (permutation[index] - 1) for index in range(1, 8) if mask >> (index - 1) & 1)


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    basis = ISOTROPIC_BASIS + DUAL_BASIS + (CHARACTERISTIC,)
    assert len(set(span(basis))) == 128
    assert all(dot(left, right) == int(abs(first - second) == 3 and max(first, second) < 6 or first == second == 6)
               for first, left in enumerate(basis) for second, right in enumerate(basis))
    rows = bases(7, 3)
    spaces = {vertex: frozenset(span(row)) for vertex, row in enumerate(rows)
              if len(row) == 1 or all(dot(left, right) == 0 for left in row for right in row)}
    lookup = {space: vertex for vertex, space in spaces.items()}
    isotropic = frozenset(span(ISOTROPIC_BASIS))
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    clique.append(lookup[frozenset((0, CHARACTERISTIC))])
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    adjacency = {vertex: set() for vertex in spaces}
    for vertex, neighbor in combinations(spaces, 2):
        if all(dot(left, right) == 0 for left in rows[vertex] for right in rows[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    palettes = {vertex: set(range(17)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in spaces if vertex not in fixed}
    special = [lookup[frozenset((0, CHARACTERISTIC ^ combine(coordinates, ISOTROPIC_BASIS)))]
               for coordinates in range(1, 8)]
    assert all(palettes[vertex] == {15, 16} for vertex in special)
    assert sum(palette == {15, 16} for palette in palettes.values()) == 7
    permutations = []
    for columns in product(range(1, 8), repeat=3):
        if len(set(span(columns))) != 8:
            continue
        dual_columns = tuple(next(vector for vector in range(8)
                                  if all(dot(column, vector) == int(index == target)
                                         for index, column in enumerate(columns)))
                             for target in range(3))
        image_basis = tuple(combine(column, ISOTROPIC_BASIS) for column in columns)
        image_basis += tuple(combine(column, DUAL_BASIS) for column in dual_columns) + (CHARACTERISTIC,)
        image = {combine(coordinates, basis): combine(coordinates, image_basis) for coordinates in range(128)}
        assert len(set(image.values())) == 128 and image[CHARACTERISTIC] == CHARACTERISTIC
        assert all(dot(left, right) == dot(image[left], image[right])
                   for left in range(128) for right in range(128))
        vertex_image = {vertex: lookup[frozenset(image[vector] for vector in space)] for vertex, space in spaces.items()}
        assert set(vertex_image.values()) == set(spaces)
        assert {vertex_image[vertex] for vertex in fixed} == set(fixed)
        color_image = {color: fixed[vertex_image[vertex]] for vertex, color in fixed.items()}
        color_image[16] = 16
        assert color_image[15] == 15 and set(color_image.values()) == set(range(17))
        assert all({color_image[color] for color in palettes[vertex]} == palettes[vertex_image[vertex]]
                   for vertex in palettes)
        assert all(vertex_image[neighbor] in adjacency[vertex_image[vertex]]
                   for vertex in adjacency for neighbor in adjacency[vertex] if neighbor < vertex)
        permutation = tuple(combine(coordinates, columns) for coordinates in range(8))
        assert all(vertex_image[special[index - 1]] == special[permutation[index] - 1] for index in range(1, 8))
        permutations.append(permutation)
    assert len(permutations) == len(set(permutations)) == 168
    remaining = set(range(128))
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {transform_mask(representative, permutation) for permutation in permutations}
        assert orbit <= remaining
        remaining -= orbit
        subset = [index for index in range(1, 8) if representative >> (index - 1) & 1]
        orbits.append({'representative_mask': representative, 'color16_coordinates': subset,
                      'subset_size': len(subset), 'orbit_size': len(orbit), 'members': sorted(orbit)})
    assert len(orbits) == 10 and sum(orbit['orbit_size'] for orbit in orbits) == 128
    assert Counter(orbit['subset_size'] for orbit in orbits) == Counter({0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 1, 7: 1})
    return {'status': 'orthogonal_lifts_normalized_palette_action_and_all_pattern_orbits_checked',
            'dimension': 7, 'isotropic_basis': ISOTROPIC_BASIS, 'dual_basis': DUAL_BASIS,
            'characteristic_vector': CHARACTERISTIC, 'linear_group_order': len(permutations),
            'isometry_vector_pairs_checked': len(permutations) * 128 * 128,
            'retained_vertex_images_checked': len(permutations) * len(spaces),
            'retained_edge_images_checked': len(permutations) * sum(map(len, adjacency.values())) // 2,
            'palette_images_checked': len(permutations) * len(palettes),
            'special_line_generators_in_coordinate_order': [CHARACTERISTIC ^ combine(index, ISOTROPIC_BASIS) for index in range(1, 8)],
            'pattern_assignments': 128, 'pattern_orbits': orbits, 'allowed_representative_patterns': 10,
            'forbidden_patterns': 118, 'added_seven_literal_clauses': 118,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'shared_basis_helper_sha256': hashlib.sha256((ROOT / 'develop/dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False, 'full_n7_chromatic_number': 'open_lower_bound17',
            'scope': 'Written extension of everyGL(3,2) action by inverse transpose on a symplectic dual basis, fixingz. All168maps verified on everyvectorpair, retainedvertex/edge and normalizedpalette. All128seven-linepatterns partitioned; tenrepresentatives lose no normalized17colorability. NoSAT/UNSAT/fullcoloring/Lean.'}


def emit_and_audit(source, target, report):
    base_audit = check_encoding(source, 7, 127)
    rows = bases(7, 3)
    isotropic = frozenset(span(ISOTROPIC_BASIS))
    spaces = {vertex: frozenset(span(row)) for vertex, row in enumerate(rows)
              if len(row) == 1 or all(dot(left, right) == 0 for left in span(row) for right in span(row))}
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    core = sorted(set(spaces) - set(clique) - {vertex for vertex, space in spaces.items() if space == {0, CHARACTERISTIC}})
    identifiers = {}
    next_identifier = 1
    for vertex in core:
        intersection = {vector for vector in isotropic if all(dot(vector, row) == 0 for row in rows[vertex])}
        colors = [color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= intersection]
        if any(vector.bit_count() % 2 for vector in spaces[vertex]):
            colors.append(15)
        colors.append(16)
        for color in colors:
            identifiers[vertex, color] = next_identifier
            next_identifier += 1
    variables = [identifiers[next(vertex for vertex, space in spaces.items()
                                  if space == {0, CHARACTERISTIC ^ combine(index, ISOTROPIC_BASIS)}), 16]
                 for index in range(1, 8)]
    representatives = {orbit['representative_mask'] for orbit in report['pattern_orbits']}
    clauses = [tuple(-variable if mask >> index & 1 else variable for index, variable in enumerate(variables))
               for mask in range(128) if mask not in representatives]
    assert len(clauses) == len(set(clauses)) == 118
    for mask in range(128):
        truth = {variable: bool(mask >> index & 1) for index, variable in enumerate(variables)}
        failed_clauses = sum(not any(truth[abs(literal)] == (literal > 0) for literal in clause) for clause in clauses)
        assert failed_clauses == int(mask not in representatives)
    lines = source.read_text().splitlines()
    header = next(index for index, line in enumerate(lines) if line.startswith('p'))
    lines[header] = f'p cnf {base_audit["variables"]} {base_audit["clauses"] + len(clauses)}'
    lines += [' '.join(map(str, clause)) + ' 0' for clause in clauses]
    target.write_text('\n'.join(lines) + '\n')
    replay = target.read_text().splitlines()
    assert replay[-118:] == lines[-118:]
    replay = replay[:-118]
    replay[header] = source.read_text().splitlines()[header]
    assert '\n'.join(replay) + '\n' == source.read_text()
    return {'base_clause_audit': base_audit, 'base_CNF_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'symmetry_CNF_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'variables': base_audit['variables'], 'clauses': base_audit['clauses'] + 118,
            'added_clause_truth_table_assignments_checked': 128, 'added_clauses': len(clauses),
            'base_clause_body_byte_identical': True, 'color16_variables_in_coordinate_order': variables,
            'symmetry_clause_audit': 'Eachnonrepresentativeassignmentexcludedbyexactlyoneclause; allrepresentativesaccepted. Emittedsuffixcheckedonreadback; basebodyrecoveredbyteidentically and everybaseclause independentlyaudited.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--cnf', type=Path)
    parser.add_argument('--output-cnf', type=Path)
    args = parser.parse_args()
    if bool(args.cnf) != bool(args.output_cnf):
        parser.error('--cnf and --output-cnf must be supplied together')
    result = check()
    if args.cnf:
        result['encoding'] = emit_and_audit(args.cnf, args.output_cnf, result)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
