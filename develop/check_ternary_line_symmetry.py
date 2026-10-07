"""Verify the 32 ternary special-line orbits and a sufficient-route CNF restriction."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

from check_lines_planes_encoding import audit_bytes, check_contents, geometric_encoding
from dimension_seven_feasibility import bases, span


ISOTROPIC_BASIS = (3, 12, 48)
DUAL_BASIS = (65, 71, 95)
CHARACTERISTIC = 127
COLORS = (14, 15, 16)


def dot(left, right):
    return (left & right).bit_count() % 2


def combine(coordinates, basis):
    vector = 0
    for index, row in enumerate(basis):
        if coordinates >> index & 1:
            vector ^= row
    return vector


def act(pattern, permutation, swap=False):
    result = [14] * 7
    for coordinate, color in enumerate(pattern, 1):
        result[permutation[coordinate] - 1] = 31 - color if swap and color != 14 else color
    return tuple(result)


def cycle_lengths(permutation):
    remaining = set(range(1, 8))
    lengths = []
    while remaining:
        point = min(remaining)
        length = 0
        while point in remaining:
            remaining.remove(point)
            length += 1
            point = permutation[point]
        lengths.append(length)
    return lengths


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    basis = ISOTROPIC_BASIS + DUAL_BASIS + (CHARACTERISTIC,)
    assert len(set(span(basis))) == 128
    assert all(dot(left, right) == int(abs(first - second) == 3 and max(first, second) < 6 or first == second == 6)
               for first, left in enumerate(basis) for second, right in enumerate(basis))
    rows = bases(7, 2)
    spaces = {vertex: frozenset(span(row)) for vertex, row in enumerate(rows)
              if len(row) == 1 or all(dot(left, right) == 0 for left in span(row) for right in span(row))}
    lookup = {space: vertex for vertex, space in spaces.items()}
    isotropic = frozenset(span(ISOTROPIC_BASIS))
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    fixed[lookup[frozenset((0, CHARACTERISTIC))]] = 14
    edges = [(vertex, neighbor) for vertex, neighbor in combinations(spaces, 2)
             if all(dot(left, right) == 0 for left in spaces[vertex] for right in spaces[neighbor])]
    adjacency = {vertex: set() for vertex in spaces}
    for vertex, neighbor in edges:
        adjacency[vertex].add(neighbor)
        adjacency[neighbor].add(vertex)
    palettes = {vertex: set(range(17)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in spaces if vertex not in fixed}
    assert len(spaces) == 442 and len(fixed) == 15 and len(edges) == 16569
    special = [lookup[frozenset((0, CHARACTERISTIC ^ combine(coordinate, ISOTROPIC_BASIS)))]
               for coordinate in range(1, 8)]
    assert all(palettes[vertex] == set(COLORS) for vertex in special)
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
        color_image.update({15: 15, 16: 16})
        assert color_image[14] == 14 and set(color_image.values()) == set(range(17))
        assert all(vertex_image[neighbor] in adjacency[vertex_image[vertex]] for vertex, neighbor in edges)
        for swap in (False, True):
            renormalization = {color: 31 - target if swap and target >= 15 else target
                               for color, target in color_image.items()}
            assert all({renormalization[color] for color in palettes[vertex]} == palettes[vertex_image[vertex]]
                       for vertex in palettes)
            assert all(renormalization[color] == fixed[vertex_image[vertex]] for vertex, color in fixed.items())
        permutation = tuple(combine(coordinates, columns) for coordinates in range(8))
        assert all(vertex_image[special[index - 1]] == special[permutation[index] - 1] for index in range(1, 8))
        permutations.append(permutation)
    assert len(permutations) == len(set(permutations)) == 168
    identity = tuple(range(8))
    generators = [tuple(combine(coordinate, columns) for coordinate in range(8))
                  for columns in ((2, 4, 1), (1, 3, 4))]
    generated = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            following = tuple(generator[current[coordinate]] for coordinate in range(8))
            if following not in generated:
                generated.add(following)
                frontier.append(following)
    assert generated == set(permutations)
    patterns = set(product(COLORS, repeat=7))
    remaining = set(patterns)
    orbits = []
    linear_orbits = set()
    while remaining:
        representative = min(remaining)
        linear_orbit = {act(representative, permutation) for permutation in permutations}
        orbit = linear_orbit | {act(representative, permutation, True) for permutation in permutations}
        assert orbit <= remaining
        remaining -= orbit
        for pattern in orbit:
            linear_orbits.add(min(act(pattern, permutation) for permutation in permutations))
        reached = {representative}
        frontier = [representative]
        while frontier:
            current = frontier.pop()
            neighbors = [act(current, generator) for generator in generators] + [act(current, identity, True)]
            for following in neighbors:
                if following not in reached:
                    reached.add(following)
                    frontier.append(following)
        assert reached == orbit
        orbits.append({'representative': representative, 'orbit_size': len(orbit), 'stabilizer_order': 336 // len(orbit)})
    no_swap_sum = sum(3 ** len(cycle_lengths(permutation)) for permutation in permutations)
    swap_sum = sum(3 ** sum(length % 2 == 0 for length in cycle_lengths(permutation)) for permutation in permutations)
    assert (no_swap_sum, swap_sum) == (10080, 672)
    assert len(linear_orbits) == no_swap_sum // 168 == 60
    assert len(orbits) == (no_swap_sum + swap_sum) // 336 == 32
    assert sum(orbit['orbit_size'] for orbit in orbits) == len(patterns) == 2187
    transposition = (0, 2, 1, 3, 4, 5, 6, 7)
    assert any(transposition[first ^ second] != transposition[first] ^ transposition[second]
               for first in range(8) for second in range(8))
    assert any({15 if color == 14 else 14 if color == 15 else color for color in palette} != palette
               for palette in palettes.values())
    return {'status': 'orthogonal_lifts_renormalization_32_ternary_orbits_checked',
            'dimension': 7, 'isotropic_basis': ISOTROPIC_BASIS, 'dual_basis': DUAL_BASIS,
            'characteristic_vector': CHARACTERISTIC, 'fixed_clique_size': 15,
            'special_line_generators_in_coordinate_order': [CHARACTERISTIC ^ combine(index, ISOTROPIC_BASIS) for index in range(1, 8)],
            'special_line_colors': COLORS, 'linear_group_order': 168, 'group_with_extra_swap_order': 336,
            'isometry_vector_pairs_checked': 168 * 128 * 128, 'vertex_images_checked': 168 * len(spaces),
            'edge_images_checked': 168 * len(edges), 'palette_images_checked': 336 * len(palettes),
            'assignments': 2187, 'linear_orbits': 60, 'orbits_with_extra_swap': 32,
            'burnside_fixed_point_sums': {'without_swap': no_swap_sum, 'with_swap': swap_sum},
            'orbit_size_histogram': dict(sorted(Counter(orbit['orbit_size'] for orbit in orbits).items())),
            'orbits': orbits, 'independent_generator_closure_and_orbit_BFS': True,
            'invalid_arbitrary_point_transposition': 'rejected_as_nonlinear',
            'invalid_color14_extra_swap': 'rejected_by_palette_counterexample',
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'shared_RREF_span_helper_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False, 'full_n7_chromatic_number': 'open_lower_bound18',
            'scope': 'Only the auxiliary442vertex seventeen-color sufficient route. T itself absent; label14 fixed, only extras15/16 interchangeable. Every ternary orbit retained. No old full17color forcing, coloring or new bound.'}


def audit_restriction(contents, representatives, identifiers):
    if not __debug__:
        raise RuntimeError('Run this auditor without -O or PYTHONOPTIMIZE.')
    variables, expected, counts = geometric_encoding()
    records = contents.splitlines(keepends=True)
    forbidden = set(product(COLORS, repeat=7)) - set(representatives)
    assert records[1].split() == [b'p', b'cnf', b'5789', str(len(expected) + len(forbidden)).encode()]
    base_records = records[:2 + len(expected)]
    base_records[1] = f'p cnf 5789 {len(expected)}\n'.encode()
    audit_bytes(b''.join(base_records), len(variables), expected)
    clauses = []
    excluded = set()
    for record in records[2 + len(expected):]:
        literals = [int(token) for token in record.split()]
        assert literals.pop() == 0 and len(literals) == 7
        pattern = tuple(next(color for color in COLORS if identifiers[index][color] == -literal)
                        for index, literal in enumerate(literals))
        assert pattern not in excluded
        excluded.add(pattern)
        clauses.append(literals)
    assert excluded == forbidden
    for pattern in product(COLORS, repeat=7):
        chosen = {identifiers[index][color] for index, color in enumerate(pattern)}
        failures = sum(all(-literal in chosen for literal in clause) for clause in clauses)
        assert failures == int(pattern in forbidden)
    return counts


def emit_and_audit(source, target, report):
    if not __debug__:
        raise RuntimeError('Run this emitter without -O or PYTHONOPTIMIZE.')
    contents = source.read_bytes()
    base_audit = check_contents(contents)
    variables, expected, counts = geometric_encoding()
    rows = bases(7, 2)
    identifiers = [{color: variables[next(vertex for vertex, row in enumerate(rows) if row == (generator,)), color]
                    for color in COLORS} for generator in report['special_line_generators_in_coordinate_order']]
    representatives = {tuple(orbit['representative']) for orbit in report['orbits']}
    clauses = [tuple(-identifiers[index][color] for index, color in enumerate(pattern))
               for pattern in product(COLORS, repeat=7) if pattern not in representatives]
    assert len(clauses) == 2155
    records = contents.splitlines(keepends=True)
    original_header = records[1]
    records[1] = b'p cnf 5789 199499\n'
    base_bytes = b''.join(records)
    separator = b'' if base_bytes.endswith((b'\n', b'\r')) else b'\n'
    suffix = ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses).encode()
    target.write_bytes(base_bytes + separator + suffix)
    emitted = target.read_bytes()
    audit_restriction(emitted, representatives, identifiers)
    assert emitted == base_bytes + separator + suffix
    recovered = emitted[:len(base_bytes)].splitlines(keepends=True)
    recovered[1] = original_header
    assert b''.join(recovered) == contents
    variants = {'missing_symmetry_clause': emitted[:-len(suffix.splitlines(keepends=True)[-1])],
                'duplicate_symmetry_clause': emitted + suffix.splitlines(keepends=True)[0],
                'representative_excluded': emitted + (' '.join(str(-identifiers[index][color]) for index, color in enumerate(min(representatives))) + ' 0\n').encode()}
    for name, variant in variants.items():
        try:
            audit_restriction(variant, representatives, identifiers)
        except (AssertionError, StopIteration):
            pass
        else:
            raise AssertionError(('negative control accepted', name))
    return {'base_audit': base_audit, 'base_cnf_sha256': hashlib.sha256(contents).hexdigest(),
            'symmetry_cnf_sha256': hashlib.sha256(emitted).hexdigest(),
            'variables': 5789, 'base_clauses': len(expected), 'added_clauses': 2155, 'total_clauses': 199499,
            'special_line_variables_in_coordinate_order': identifiers, 'all_2187_assignments_checked': True,
            'base_bytes_recovered_exactly': True, 'negative_controls': {name: 'rejected' for name in variants},
            'clause_auditor_sha256': hashlib.sha256(Path(__file__).with_name('check_lines_planes_encoding.py').read_bytes()).hexdigest()}


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
