"""Check seven conditional clique-triangle contradictions and mask0 lists."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, span


def dot(left, right):
    return (left & right).bit_count() % 2


def orthogonal(left, right):
    return all(dot(first, second) == 0 for first in left for second in right)


def subspace_family(generators):
    vectors = frozenset(span(generators))
    assert len(generators) == 3 and all(0 <= vector < 128 for vector in vectors)
    assert len(vectors) == 8 and orthogonal(vectors, vectors)
    nonzero = sorted(vectors - {0})
    lines = {frozenset((0, vector)) for vector in nonzero}
    planes = {frozenset((0, first, second, first ^ second)) for first, second in combinations(nonzero, 2)}
    family = lines | planes | {vectors}
    assert len(lines) == len(planes) == 7 and len(family) == 15
    assert all(orthogonal(first, second) for first, second in combinations(family, 2))
    return family


def witness(vector):
    isotropic = span((3, 12, 48))
    companion = next(value for value in isotropic if value not in (0, vector))
    even = next(value for value in span((65, 71, 95)) if dot(value, vector) == 0 and dot(value, companion) == 1)
    common = next(value for value in isotropic if value not in (0, vector) and dot(value, even) == 0)
    return {'assumed_color16_special_generator': 127 ^ vector,
            't': vector, 'd': companion, 'e': even, 'f': even ^ companion,
            'first_lagrangian_basis': [vector, common, even],
            'second_lagrangian_basis': [vector, common, even ^ companion],
            'triangle_generators': [127 ^ even, 127 ^ even ^ companion, 127 ^ companion]}


def verify_witness(record):
    isotropic = frozenset(span((3, 12, 48)))
    vector, companion, even, partner = (record[key] for key in ('t', 'd', 'e', 'f'))
    assert all(0 < value < 128 for value in (vector, companion, even, partner))
    assert vector in isotropic - {0} and companion in isotropic - {0, vector}
    assert even.bit_count() % 2 == partner.bit_count() % 2 == 0
    assert dot(even, vector) == dot(partner, vector) == 0
    assert dot(even, companion) == 1 and partner == even ^ companion
    assert record['assumed_color16_special_generator'] == 127 ^ vector
    first = subspace_family(record['first_lagrangian_basis'])
    second = subspace_family(record['second_lagrangian_basis'])
    assert {0, vector, even} <= set(span(record['first_lagrangian_basis']))
    assert {0, vector, partner} <= set(span(record['second_lagrangian_basis']))
    fixed_clique = subspace_family((3, 12, 48))
    characteristic = frozenset((0, 127))
    assumed = frozenset((0, 127 ^ vector))
    triangle = [frozenset((0, value)) for value in record['triangle_generators']]
    assert record['triangle_generators'] == [127 ^ even, 127 ^ partner, 127 ^ companion]
    assert len(set(triangle)) == 3 and all(orthogonal(left, right) for left, right in combinations(triangle, 2))
    assert all(orthogonal(characteristic, space) for space in fixed_clique | first | second)
    assert all(orthogonal(assumed, space) for space in first | second)
    assert all(orthogonal(triangle[0], space) for space in first)
    assert all(orthogonal(triangle[1], space) for space in second)
    assert all(orthogonal(triangle[2], space) for space in fixed_clique)
    vertices = sorted(fixed_clique | first | second | {characteristic, assumed} | set(triangle), key=lambda space: tuple(sorted(space)))
    assert len(vertices) == 42
    edges = sum(orthogonal(left, right) for left, right in combinations(vertices, 2))
    return {'vertices': len(vertices), 'pairs_checked': len(vertices) * (len(vertices) - 1) // 2,
            'edges': edges, 'three_cliques_size15_checked': True,
            'triangle_size3_checked': True, 'triangle_lists_forced_inside15and16': True,
            'contradiction': 'The two Lagrangian cliques use all0..14 after excluding15and16. Each triangle vertex excludes0..14 via its clique. A triangle cannot use only15and16.'}


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    isotropic = frozenset(span((3, 12, 48)))
    witnesses = []
    for vector in span((3, 12, 48)):
        if vector:
            record = witness(vector)
            witnesses.append({**record, 'verification': verify_witness(record)})
    bad_triangle = witness(3)
    bad_triangle['triangle_generators'][1] = bad_triangle['triangle_generators'][0]
    bad_lagrangian = witness(3)
    bad_lagrangian['first_lagrangian_basis'][-1] = 127
    controls = {}
    for label, record in [('repeated_triangle_vertex', bad_triangle), ('nonisotropic_lagrangian', bad_lagrangian)]:
        try:
            verify_witness(record)
        except AssertionError:
            controls[label] = 'rejected'
        else:
            raise AssertionError(('negative control accepted', label))
    rows = bases(7, 3)
    spaces = {vertex: frozenset(span(basis)) for vertex, basis in enumerate(rows)
              if len(basis) == 1 or orthogonal(span(basis), span(basis))}
    clique = [vertex for vertex, space in spaces.items() if space <= isotropic]
    odd_class = {vertex for vertex, space in spaces.items() if len(space) == 2
                 and next(iter(space - {0})) ^ 127 in isotropic}
    fixed = {vertex: color for color, vertex in enumerate(clique)}
    fixed.update(dict.fromkeys(odd_class, 15))
    assert len(clique) == 15 and len(odd_class) == 8 and len(fixed) == 23
    assert all(not orthogonal(spaces[first], spaces[second]) for first, second in combinations(odd_class, 2))
    adjacency = {vertex: set() for vertex in spaces}
    for vertex, neighbor in combinations(spaces, 2):
        if orthogonal(spaces[vertex], spaces[neighbor]):
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
    core = sorted(spaces.keys() - fixed.keys())
    palettes = {vertex: set(range(17)) - {fixed[neighbor] for neighbor in adjacency[vertex] & fixed.keys()}
                for vertex in core}
    for vertex in core:
        kernel = {vector for vector in isotropic if all(dot(vector, other) == 0 for other in spaces[vertex])}
        geometric = {color for color, neighbor in enumerate(clique) if not spaces[neighbor] <= kernel} | {16}
        assert palettes[vertex] == geometric and 15 not in palettes[vertex]
    edges = sum(len(adjacency[vertex] & palettes.keys()) for vertex in core) // 2
    vertex_clauses = sum(1 + len(palette) * (len(palette) - 1) // 2 for palette in palettes.values())
    edge_clauses = sum(len(palettes[vertex] & palettes[neighbor]) for vertex in core
                       for neighbor in adjacency[vertex] & palettes.keys() if neighbor < vertex)
    assert (len(core), edges, sum(map(len, palettes.values())), vertex_clauses + edge_clauses) == (554, 16730, 7744, 241782)
    assert Counter(map(len, palettes.values())) == {12: 210, 15: 280, 16: 64}
    return {'status': 'seven_color15_forcing_clique_triangle_certificates_and_mask0_lists_checked',
            'dimension': 7, 'target_colors': 17, 'fixed_last_line_basis': [127],
            'forced_special_line_color': 15, 'only_remaining_pattern': 0,
            'excluded_symmetry_representatives': [1, 3, 7, 11, 15, 30, 31, 63, 127],
            'written_proof_scope': 'Every normalized17coloring of the retained graph has all seven special lines15. This follows from conditional clique-triangle contradictions, not a solver UNSAT report.',
            'witnesses': witnesses, 'negative_controls': controls,
            'retained_vertices': len(spaces), 'retained_pairs_checked': len(spaces) * (len(spaces) - 1) // 2,
            'fixed_T_clique_vertices': len(clique), 'fixed_color15_class': len(odd_class),
            'uncolored_vertices': len(core), 'uncolored_edges': edges,
            'uncolored_dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in core).items())),
            'palette_sizes': dict(sorted(Counter(map(len, palettes.values())).items())),
            'variables': sum(map(len, palettes.values())), 'vertex_clauses': vertex_clauses,
            'edge_clauses': edge_clauses, 'clauses': vertex_clauses + edge_clauses,
            'all554_geometric_lists_checked': len(core) == 554,
            'every_residual_vertex_allows16_and_forbids15': True,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'basis_enumerator_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'new_CNF_emitted': False, 'solver_run': False, 'lean_run': False,
            'full_n7_chromatic_number': 'open_lower_bound17',
            'scope': 'Written color-forcing proof with seven42vertex finite certificates and exact residual-list counts. Mask127 ruled out by graph proof, not solver/DRAT. Mask0 colorability and exact fulln7chi remain open. Color16 remains allowed throughout the residual17color problem; old16color uncolorability does not settle it.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
