"""Check the Lagrangian coverage used in the eighteen-color extension criterion."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def dot(first, second):
    return (first & second).bit_count() % 2


def span(generators):
    vectors = {0}
    for generator in generators:
        vectors |= {vector ^ generator for vector in vectors}
    return frozenset(vectors)


def family(lagrangian, even_vertices):
    result = {space for space in even_vertices if space <= lagrangian}
    assert len(result) == 15
    return result


def verify_cover(vector, lagrangians, even_vertices):
    incident = {space for space in lagrangians if vector in space}
    covered = set().union(*(family(space, even_vertices) for space in incident))
    neighbors = {space for space in even_vertices if all(dot(vector, member) == 0 for member in space)}
    assert covered == neighbors, ('Lagrangian coverage mismatch', vector)
    return incident, neighbors


def clique_statistics(nonzero):
    adjacency = {vector: {neighbor for neighbor in nonzero if dot(vector, neighbor) == 1} for vector in nonzero}
    sizes, maximal_sizes, examples = Counter(), Counter(), {}
    def visit(clique, candidates):
        for index, vector in enumerate(candidates):
            extended = clique + (vector,)
            sizes[len(extended)] += 1
            common = set(nonzero).intersection(*(adjacency[member] for member in extended))
            if not common:
                total = 0
                for member in extended:
                    total ^= member
                assert len(extended) in (3, 5, 7) and total == 0
                maximal_sizes[len(extended)] += 1
                examples.setdefault(len(extended), list(extended))
            visit(extended, [neighbor for neighbor in candidates[index + 1:] if neighbor in adjacency[vector]])
    visit((), nonzero)
    assert dict(sizes) == {1: 63, 2: 1008, 3: 5376, 4: 10080, 5: 8064, 6: 2016, 7: 288}
    assert dict(maximal_sizes) == {3: 336, 5: 2016, 7: 288}
    return dict(sorted(sizes.items())), dict(sorted(maximal_sizes.items())), dict(sorted(examples.items()))


def check():
    if not __debug__:
        raise RuntimeError('Run this checker without -O or PYTHONOPTIMIZE.')
    characteristic = 127
    even_vectors = span((3, 12, 48, 65, 71, 95))
    assert len(even_vectors) == 64 and even_vectors == frozenset(vector for vector in range(128) if dot(characteristic, vector) == 0)
    nonzero = sorted(even_vectors - {0})
    lines = {span((vector,)) for vector in nonzero}
    planes = {span((first, second)) for first, second in combinations(nonzero, 2) if dot(first, second) == 0}
    lagrangians = {span(generators) for generators in combinations(nonzero, 3)
                   if all(dot(first, second) == 0 for first, second in combinations(generators, 2))
                   and len(span(generators)) == 8}
    even_vertices = lines | planes | lagrangians
    assert (len(lines), len(planes), len(lagrangians), len(even_vertices)) == (63, 315, 135, 513)
    assert all(all(dot(first, second) == 0 for first in space for second in space) for space in even_vertices)
    families = {space: family(space, even_vertices) for space in lagrangians}
    assert all(all(all(dot(left, right) == 0 for left in first for right in second)
                   for first, second in combinations(clique, 2)) for clique in families.values())
    rows = []
    for vector in sorted(even_vectors):
        incident, neighbors = verify_cover(vector, lagrangians, even_vertices)
        assert len(incident) == (135 if vector == 0 else 15)
        odd_neighbors = {space for space in even_vertices
                         if all(dot(characteristic ^ vector, member) == 0 for member in space)}
        assert neighbors == odd_neighbors and len(neighbors) == (513 if vector == 0 else 121)
        rows.append({'even_vector': vector, 'odd_line_generator': characteristic ^ vector,
                     'incident_lagrangians': len(incident), 'even_neighbors': len(neighbors)})
    assert all(dot(characteristic ^ first, characteristic ^ second) == 1 ^ dot(first, second)
               for first in even_vectors for second in even_vectors)
    odd_edges = [(first, second) for first, second in combinations(nonzero, 2) if dot(first, second) == 1]
    assert len(odd_edges) == 1008
    assert all(sum(dot(vector, neighbor) == 1 for neighbor in nonzero if neighbor != vector) == 32 for vector in nonzero)
    clique_sizes, maximal_clique_sizes, maximal_examples = clique_statistics(nonzero)
    fixed = span((3, 12, 48))
    assert fixed in lagrangians and all(dot(first, second) == 0 for first, second in combinations(fixed - {0}, 2))
    triple_pairs = list(combinations(lagrangians, 2))
    assert len(triple_pairs) == 9045 and not any(all(dot(left, right) == 0 for left in first for right in second)
                                               for first, second in triple_pairs)
    reduced = (even_vertices - lagrangians) | {span((characteristic ^ vector,)) for vector in even_vectors}
    reduced_edges = sum(all(dot(left, right) == 0 for left in first for right in second)
                        for first, second in combinations(reduced, 2))
    assert len(reduced) == 442 and reduced_edges == 16569
    controls = {}
    try:
        verify_cover(3, lagrangians - {fixed}, even_vertices)
    except AssertionError:
        controls['missing_incident_lagrangian'] = 'rejected'
    else:
        raise AssertionError('Missing Lagrangian control accepted.')
    try:
        assert all(dot(characteristic ^ first, characteristic ^ second) == 0
                   for first, second in combinations(nonzero, 2) if dot(first, second) == 0)
    except AssertionError:
        controls['wrong_odd_adjacency_parity'] = 'rejected'
    else:
        raise AssertionError('Wrong parity control accepted.')
    return {'status': 'all_even_odd_neighbor_sets_equal_incident_Lagrangian_clique_unions',
            'dimension': 7, 'target_palette_size': 18, 'even_vertices': 513,
            'even_vertex_dimensions': {1: 63, 2: 315, 3: 135}, 'lagrangians': 135,
            'nonzero_points': 63, 'lagrangians_per_nonzero_point': 15,
            'nonzero_point_lagrangian_incidences': 945, 'all_vector_lagrangian_memberships_checked': 8640,
            'even_odd_neighbor_memberships_checked': 32832,
            'even_odd_edges': sum(row['even_neighbors'] for row in rows),
            'even_neighbor_histogram_nonzero_vectors': dict(sorted(Counter(row['even_neighbors'] for row in rows if row['even_vector']).items())),
            'odd_noncharacteristic_vertices': 63, 'odd_pairs_checked': 1953, 'odd_edges': 1008,
            'odd_degree': 32, 'characteristic_line_odd_degree': 0,
            'odd_cliques_by_size': clique_sizes, 'odd_maximal_cliques_by_size': maximal_clique_sizes,
            'odd_maximal_clique_examples': maximal_examples,
            'triple_independence_pairs_checked': 9045, 'triple_independence_edges': 0,
            'lines_and_planes_sufficient_construction': {'vertices': 442, 'pairs_checked': 97461, 'edges': reduced_edges,
                                                        'target_colors': 17, 'coloring_supplied': False,
                                                        'scope': 'A seventeen-coloring here plus one separate color for all 135 Lagrangian three-spaces would give eighteen colors on the retained graph. Sufficient construction only, not an equivalent restriction.'},
            'point_records': rows, 'negative_controls': controls,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'written_criterion': 'Given a proper coloring of the513even vertices with17non15colors, odd line[z+e] has list{15} union the intersection of the two omitted colors over all Lagrangians containing e. Extending on the63nonzeroe nonorthogonality graph is necessary and sufficient.',
            'written_necessary_condition': 'If the given even coloring admits an eighteen-color extension, then the nonzero vectors whose omitted-pair intersection is empty are pairwise symplectically orthogonal. Their span is totally isotropic, so at most seven such vectors occur and at least fifty-six nonzero points have a nonempty intersection.',
            'written_clique_condition': 'If the given even coloring admits an eighteen-color extension, then for every nonempty odd clique C the union of its omitted-pair intersections has at least |C|-1 colors. All 26,895 cliques of the 63-vertex graph enumerated. Its 2,640 maximal cliques have sizes 3,5,7 and vector sum zero. These are necessary constraints, not a sufficient global list-coloring test.',
            'even_coloring_supplied': False, 'odd_list_coloring_supplied': False,
            'new_chromatic_bound': False, 'solver_run': False, 'lean_run': False,
            'scope': 'Written conditional extension theorem with exhaustive incidence/neighbor geometry checks. No actual17color even coloring,18color full witness or new lower bound. Exact full n7chromatic number remains open>=18. No seventeen-color anchor assignments imposed on eighteen colors.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'point_records'}, indent=2))
