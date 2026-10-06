"""Check a 29-vertex 17-chromatic induced subgraph using only the standard library."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def dot(left, right):
    return sum(((left >> position) & 1) * ((right >> position) & 1) for position in range(7)) % 2


def span(basis):
    values = {0}
    for vector in basis:
        values |= {value ^ vector for value in values}
    return frozenset(values)


def subspaces(space):
    result = {}
    for dimension in range(1, 4):
        for basis in combinations(sorted(space - {0}), dimension):
            generated = span(basis)
            if len(generated) == 2 ** dimension:
                result.setdefault(generated, basis)
    assert len(result) == 15
    return result


def orthogonal(first, second):
    return all(dot(left, right) == 0 for left in first for right in second)


def check():
    first_space = span((66, 12, 48))
    second_space = span((65, 12, 48))
    assert len(first_space) == len(second_space) == 8
    assert orthogonal(first_space, first_space) and orthogonal(second_space, second_space)
    first_clique = subspaces(first_space)
    second_clique = subspaces(second_space)
    assert len(first_clique.keys() & second_clique.keys()) == 4
    records = dict(first_clique)
    records.update(second_clique)
    for vector in (127, 1, 2):
        assert span((vector,)) not in records
        records[span((vector,))] = (vector,)
    ordered = sorted(records, key=lambda space: (len(records[space]), sorted(space)))
    colors = {space: color for color, space in enumerate(sorted(first_clique, key=lambda space: (len(records[space]), sorted(space))))}
    for space in second_clique:
        swapped = frozenset(vector ^ 3 if (vector & 1) != ((vector >> 1) & 1) else vector for vector in space)
        assert swapped in first_clique
        colors[space] = colors[swapped]
    colors.update({span((127,)): 15, span((1,)): 16, span((2,)): 15})
    assert len(records) == len(colors) == 29
    for clique, forced_vector in ((first_clique, 1), (second_clique, 2)):
        assert all(orthogonal(records[first], records[second]) for first, second in combinations(clique, 2))
        assert all(orthogonal((127,), basis) and orthogonal((forced_vector,), basis) for basis in clique.values())
    assert orthogonal((1,), (2,))
    edges = []
    for first_index, second_index in combinations(range(len(ordered)), 2):
        first, second = ordered[first_index], ordered[second_index]
        if orthogonal(records[first], records[second]):
            assert colors[first] != colors[second]
            edges.append([first_index, second_index])
    fixed_space = span((3, 12, 48))
    fixed_clique = list(subspaces(fixed_space))
    pigeonhole = [space for space in first_clique if not space <= fixed_space] + [span((1,))]
    assert len(pigeonhole) == 12
    assert all(orthogonal(records[first], records[second]) for first, second in combinations(pigeonhole, 2))
    lists = {space: {color for color, fixed in enumerate(fixed_clique) if not orthogonal(space, fixed)}
             for space in pigeonhole}
    assert all(64 not in {left ^ right for left in space for right in fixed_space} for space in pigeonhole)
    assert len(set().union(*lists.values())) == 11
    return {'status': 'written_17_lower_bound_obstruction_and_17_coloring_checked',
            'ambient_dimension': 7, 'vertices': len(records), 'all_pairs_checked': 406,
            'edges_checked': len(edges), 'dimension_counts': dict(sorted(Counter(len(basis) for basis in records.values()).items())),
            'clique_sizes': [15, 15], 'clique_overlap': 4,
            'common_odd_line': 127, 'first_forced_line': 1, 'second_forced_line': 2,
            'forced_lines_adjacent': True, 'induced_subgraph_chromatic_number': 17,
            'full_graph_chromatic_lower_bound': 17, 'full_graph_chromatic_number': 'open',
            'reduced_pigeonhole_clique_vertices': 12, 'reduced_palette_union_colors': 11,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'subspace_colors': [{'basis': records[space], 'color': colors[space]} for space in ordered],
            'clique_indices': [[ordered.index(space) for space in clique] for clique in (first_clique, second_clique)],
            'edges': edges, 'solver_run': False, 'lean_run': False,
            'scope': 'Exact 406-pair check of the explicit 29-vertex induced subgraph and its 17-color witness. The written two-clique forcing argument proves its lower bound and hence chi(O7*) >= 17. No full-graph upper bound or exact seven-dimensional chromatic number claimed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('subspace_colors', 'clique_indices', 'edges')}, indent=2))
