"""Check the eight-color odd graph and the conditional two-list extension encoding."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def multiply(left, right):
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        if left & 8:
            left ^= 11
        right >>= 1
    return result


def trace(value):
    square = multiply(value, value)
    return value ^ square ^ multiply(square, square)


def coordinates(bits, basis):
    result = 0
    for index, vector in enumerate(basis):
        if bits & (1 << index):
            result ^= vector
    return result


def two_list_formula(lists, edges):
    vertices = sorted(lists)
    variables = {vertex: index + 1 for index, vertex in enumerate(vertices)}
    clauses = []
    choices = {}
    for vertex in vertices:
        palette = sorted(set(lists[vertex]))
        if len(palette) > 2:
            raise ValueError('The exact Boolean reduction requires lists of size at most two.')
        if not palette:
            clauses.append([])
            choices[vertex] = {}
        elif len(palette) == 1:
            clauses.append([variables[vertex]])
            choices[vertex] = {palette[0]: variables[vertex]}
        else:
            choices[vertex] = {palette[0]: -variables[vertex], palette[1]: variables[vertex]}
    for left, right in edges:
        for color in sorted(choices[left].keys() & choices[right].keys()):
            clauses.append([-choices[left][color], -choices[right][color]])
    return variables, clauses, choices


def implication_conflicts(variables, clauses):
    if any(not clause for clause in clauses):
        return {'empty_clause': True, 'conflicting_vertices': []}
    nodes = [sign * identifier for identifier in variables.values() for sign in (-1, 1)]
    forward = {node: set() for node in nodes}
    reverse = {node: set() for node in nodes}
    for clause in clauses:
        left, right = (clause[0], clause[0]) if len(clause) == 1 else clause
        for source, target in ((-left, right), (-right, left)):
            forward[source].add(target)
            reverse[target].add(source)
    visited = set()
    order = []
    for root in nodes:
        stack = [(root, False)]
        while stack:
            node, finished = stack.pop()
            if finished:
                order.append(node)
            elif node not in visited:
                visited.add(node)
                stack.append((node, True))
                stack.extend((neighbor, False) for neighbor in sorted(forward[node]) if neighbor not in visited)
    components = {}
    for root in reversed(order):
        if root in components:
            continue
        component = len(components)
        stack = [root]
        while stack:
            node = stack.pop()
            if node in components:
                continue
            components[node] = component
            stack.extend(reverse[node] - components.keys())
    return {'empty_clause': False,
            'conflicting_vertices': [vertex for vertex, identifier in variables.items()
                                     if components[identifier] == components[-identifier]]}


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    isotropic_basis = (3, 12, 48)
    dual_basis = (65, 71, 95)
    basis = isotropic_basis + dual_basis
    assert all(dot(left, right) == (abs(left_index - right_index) == 3)
               for left_index, left in enumerate(basis) for right_index, right in enumerate(basis))
    isotropic = {coordinates(bits, isotropic_basis) for bits in range(8)}
    even = {vector for vector in range(128) if dot(vector, 127) == 0}
    assert {coordinates(bits, basis) for bits in range(64)} == even
    points = sorted(even - isotropic)
    assert len(points) == 56
    edges = [(left, right) for left, right in combinations(points, 2) if dot(left, right)]
    assert len(edges) == 784 and all(sum(point in edge for edge in edges) == 28 for point in points)
    assert all((dot(127 ^ left, 127 ^ right) == 0) == (dot(left, right) == 1)
               for left, right in combinations(points, 2))
    assert all(trace(value) in (0, 1) for value in range(8))
    assert all(any(multiply(value, inverse) == 1 for inverse in range(1, 8)) for value in range(1, 8))
    matrices = [[[trace(multiply(coefficient, multiply(left, right))) for right in (1, 2, 4)]
                 for left in (1, 2, 4)] for coefficient in range(8)]

    def image(matrix, bits):
        return sum((sum(matrix[row][column] * ((bits >> column) & 1) for column in range(3)) % 2) << row
                   for row in range(3))

    assert all(matrix[row][column] == matrix[column][row] for matrix in matrices
               for row in range(3) for column in range(3))
    assert all({image(matrix, bits) for bits in range(8)} == set(range(8)) for matrix in matrices[1:])
    assert all(all(matrices[left][row][column] ^ matrices[right][row][column] == matrices[left ^ right][row][column]
                   for row in range(3) for column in range(3)) for left in range(8) for right in range(8))
    classes = [[coordinates(image(matrix, bits), isotropic_basis) ^ coordinates(bits, dual_basis)
                for bits in range(1, 8)] for matrix in matrices]
    assert all(len(set(members)) == 7 and set(members).isdisjoint(isotropic) for members in classes)
    assert all(dot(left, right) == 0 for members in classes for left in members for right in members)
    assert len(set().union(*map(set, classes))) == sum(map(len, classes)) == 56
    assert set().union(*map(set, classes)) == set(points)
    coloring = {point: color for color, members in enumerate(classes) for point in members}
    assert all(coloring[left] != coloring[right] for left, right in edges)
    local_palettes = [(color,) for color in range(3)] + list(combinations(range(3), 2))
    instance_count = assignment_count = 0
    possible_edges = list(combinations(range(3), 2))
    for palettes in product(local_palettes, repeat=3):
        lists = dict(enumerate(palettes))
        for edge_bits in range(8):
            local_edges = [edge for index, edge in enumerate(possible_edges) if edge_bits & (1 << index)]
            variables, clauses, choices = two_list_formula(lists, local_edges)
            feasible = False
            for bits in product((False, True), repeat=3):
                assignment = dict(zip(variables.values(), bits))

                def true(literal):
                    return assignment[abs(literal)] == (literal > 0)

                cnf_value = all(any(true(literal) for literal in clause) for clause in clauses)
                selected = {vertex: [color for color, literal in options.items() if true(literal)]
                            for vertex, options in choices.items()}
                proper = all(len(colors) == 1 for colors in selected.values()) and all(
                    selected[left] != selected[right] for left, right in local_edges)
                assert cnf_value == proper
                feasible |= proper
                assignment_count += 1
            conflicts = implication_conflicts(variables, clauses)
            assert feasible == (not conflicts['empty_clause'] and not conflicts['conflicting_vertices'])
            instance_count += 1
    variables, clauses, choices = two_list_formula({0: [], 1: [0]}, [(0, 1)])
    assert implication_conflicts(variables, clauses)['empty_clause']
    try:
        two_list_formula({0: [0, 1, 2]}, [])
    except ValueError:
        oversized_rejected = True
    else:
        raise AssertionError('Oversized list accepted')
    return {'status': 'odd_graph_exact_eight_colors_and_conditional_two_list_encoding_checked',
            'dimension': 7, 'isotropic_basis': isotropic_basis, 'dual_isotropic_basis': dual_basis,
            'odd_graph_vertices': 56, 'odd_graph_edges': 784, 'odd_graph_degree': 28,
            'all_1540_pair_adjacencies_checked': True,
            'written_independence_upper_bound': 'A graph-independent set spans a totally isotropic subspace of the nondegenerate alternating six-space E, of dimension at most three, hence contains at most seven nonzero vectors.',
            'independence_number': 7, 'odd_graph_chromatic_number': 8,
            'field_polynomial': 'a^3+a+1', 'field_trace_values': [trace(value) for value in range(8)],
            'trace_matrices': matrices, 'eight_color_classes_even_points': classes,
            'odd_line_color_certificate': [{'odd_generator': 127 ^ point, 'even_point': point, 'color': coloring[point]}
                                          for point in points],
            'conditional_capacity_bound': 'For any subset R of the 56 odd points, |union I(e) over R| >= ceil(|R|/7) is necessary; in particular the global union has at least eight labels.',
            'two_list_hypothesis': 'I(e) must be the exact intersection of fifteen omitted pairs from one common proper sixteen-coloring of all 378 even vertices. This checker does not supply that even coloring or assert realizability of synthetic lists.',
            'two_list_variables_maximum': 56, 'two_list_clauses_maximum': 1624,
            'local_encoding_instances': instance_count, 'local_boolean_assignments': assignment_count,
            'SCC_feasibility_matches_local_exhaustion': True, 'empty_list_control': 'immediate_empty_clause',
            'oversized_list_rejected': oversized_rejected,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'proof_note_sha256': hashlib.sha256(Path(__file__).parents[1].joinpath('notes/all14-odd-extension.md').read_bytes()).hexdigest(),
            'native_solver_run': False, 'lean_run': False, 'even_coloring_supplied': False, 'branch_solved': False,
            'full_n7_chromatic_number': 'open_lower_bound18',
            'scope': 'Written odd-subgraph chi=8 and conditional exact2SAT criterion; finite GF8 spread witness/all odd adjacencies and exhaustive small synthetic encoding/SCC tests. No434vertex16coloring, branch exclusion, full18coloring or new full-graph bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
