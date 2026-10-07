"""Check a written clique/omitted-color obstruction to seventeen colors."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import span


def dot(left, right):
    return (left & right).bit_count() % 2


def orthogonal(left, right):
    return all(dot(first, second) == 0 for first in left for second in right)


def family(generators):
    vectors = frozenset(span(generators))
    assert len(generators) == 3 and len(vectors) == 8
    assert all(0 <= vector < 128 for vector in vectors) and orthogonal(vectors, vectors)
    nonzero = sorted(vectors - {0})
    result = {frozenset((0, vector)) for vector in nonzero}
    result.update(frozenset((0, first, second, first ^ second)) for first, second in combinations(nonzero, 2))
    result.add(vectors)
    assert len(result) == 15 and all(orthogonal(left, right) for left, right in combinations(result, 2))
    return result


def line(vector):
    assert 0 < vector < 128
    return frozenset((0, vector))


def verify_forcing(fixed_clique, characteristic, special, first, second, triangle):
    assert len(triangle) == len(set(triangle)) == 3
    assert all(orthogonal(left, right) for left, right in combinations(triangle, 2))
    assert all(orthogonal(characteristic, space) and orthogonal(special, space) for space in first | second)
    assert all(orthogonal(triangle[0], space) for space in first)
    assert all(orthogonal(triangle[1], space) for space in second)
    assert all(orthogonal(triangle[2], space) for space in fixed_clique)
    assert not ({characteristic, special} | set(triangle)) & (fixed_clique | first | second)


def verify_missing_color(first, second, endpoints, anchors):
    odd_first, odd_middle, odd_second = endpoints
    assert len(set(endpoints)) == 3
    assert all(orthogonal(odd_first, space) and orthogonal(odd_middle, space) for space in first)
    assert all(orthogonal(odd_second, space) and orthogonal(odd_middle, space) for space in second)
    assert orthogonal(odd_first, odd_second)
    assert all(any(orthogonal(endpoint, anchor) for anchor in anchors) for endpoint in endpoints)
    assert not set(endpoints) & (first | second)


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    fixed_clique = family((3, 12, 48))
    characteristic = line(127)
    assert all(orthogonal(characteristic, space) for space in fixed_clique)
    first_anchor, second_anchor = line(124), line(115)
    assert all(orthogonal(anchor, space) for anchor in (first_anchor, second_anchor) for space in fixed_clique)
    forcing_records = [((3, 48, 71), (3, 48, 75), [56, 52, 115], first_anchor),
                       ((12, 48, 65), (12, 48, 66), [62, 61, 124], second_anchor)]
    vertices = fixed_clique | {characteristic, first_anchor, second_anchor}
    forcing_certificates = []
    for first_basis, second_basis, generators, anchor in forcing_records:
        first, second = family(first_basis), family(second_basis)
        triangle = list(map(line, generators))
        verify_forcing(fixed_clique, characteristic, anchor, first, second, triangle)
        component = fixed_clique | first | second | {characteristic, anchor} | set(triangle)
        assert len(component) == 42
        vertices |= component
        forcing_certificates.append({'forced_color15_line': next(iter(anchor - {0})),
                                     'first_lagrangian_basis': list(first_basis),
                                     'second_lagrangian_basis': list(second_basis),
                                     'triangle_generators': generators,
                                     'vertices': len(component), 'pairs_checked': 861,
                                     'edges': sum(orthogonal(left, right) for left, right in combinations(component, 2))})
    first_basis, second_basis = (48, 65, 71), (48, 66, 71)
    first, second = family(first_basis), family(second_basis)
    endpoints = [line(62), line(56), line(61)]
    anchors = (first_anchor, second_anchor)
    assert all(orthogonal(characteristic, space) for space in first | second)
    verify_missing_color(first, second, endpoints, anchors)
    assert first & second == {space for space in family((48, 65, 71)) if space <= frozenset(span((48, 71)))}
    vertices |= first | second | set(endpoints)
    controls = {}
    for label, broken in [('wrong_middle_line', [line(62), line(1), line(61)]),
                          ('repeated_endpoint', [line(62), line(56), line(56)])]:
        try:
            verify_missing_color(first, second, broken, anchors)
        except AssertionError:
            controls[label] = 'rejected'
        else:
            raise AssertionError(('negative control accepted', label))
    ordered = sorted(vertices, key=lambda space: (len(space), tuple(sorted(space))))
    assert len(set(ordered)) == len(ordered)
    index = {space: identifier for identifier, space in enumerate(ordered)}
    edges = [[index[left], index[right]] for left, right in combinations(ordered, 2) if orthogonal(left, right)]
    residual_obstruction = (first | second | set(endpoints)) - fixed_clique
    assert len(residual_obstruction) == 28
    residual_pairs = list(combinations(residual_obstruction, 2))
    return {'status': 'written_seventeen_color_contradiction_geometry_checked',
            'dimension': 7, 'full_graph_chromatic_lower_bound': 18,
            'exact_full_graph_chromatic_number': 'open',
            'graph_definition': 'Nonzero subspaces, distinct vertices adjacent iff every vector pair has dot product zero.',
            'vertices': [sorted(space) for space in ordered], 'edges': edges,
            'vertex_count': len(ordered), 'pairs_checked': len(ordered) * (len(ordered) - 1) // 2,
            'edge_count': len(edges), 'fixed_sixteen_clique_indices': sorted(index[space] for space in fixed_clique | {characteristic}),
            'forcing_certificates': forcing_certificates,
            'omitted_color_step': {'first_lagrangian_basis': list(first_basis), 'second_lagrangian_basis': list(second_basis),
                                   'odd_line_generators': [62, 56, 61], 'color15_forbidden_by_line_generators': [124, 115],
                                   'residual_vertices': len(residual_obstruction), 'residual_pairs_checked': len(residual_pairs),
                                   'residual_edges': sum(orthogonal(left, right) for left, right in residual_pairs),
                                   'reason': 'Each fifteen-clique avoids color 15 and uses fifteen of the other sixteen colors. Its two odd common neighbors, also avoiding 15, must equal its unique omitted color. The shared odd neighbor makes the two adjacent endpoints equal.'},
            'negative_controls': controls,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'span_helper_sha256': hashlib.sha256(Path(__file__).with_name('dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False,
            'scope': 'Written graph proof using two conditional 42-vertex anchor certificates and an omitted-color contradiction. Complete finite graph/adjacency geometry checked. No SAT/DRAT/Lean or full-graph upper bound. Exact n=7 chromatic number remains open; prior lower bound 17 strengthened to 18.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in ('vertices', 'edges')}, indent=2))
