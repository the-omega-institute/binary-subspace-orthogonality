"""Check an exact graph retraction onto isotropic subspaces, lines and even planes."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import bases, build_instance, span


ROOT = Path(__file__).resolve().parents[1]


def dot(left, right):
    return (left & right).bit_count() % 2


def target_basis(rows):
    if len(rows) == 1 or all(dot(left, right) == 0 for left in rows for right in rows):
        return rows
    odd_rows = [row for row in rows if dot(row, row)]
    if odd_rows:
        return (min(odd_rows),)
    if len(rows) == 2:
        return rows
    return next(pair for pair in combinations(rows, 2) if dot(*pair))


def check(dimension):
    rows, adjacency, clique, original_palettes = build_instance(dimension)
    spaces = [frozenset(span(basis)) for basis in rows]
    lookup = {space: index for index, space in enumerate(spaces)}
    targets = [lookup[frozenset(span(target_basis(basis)))] for basis in rows]
    retained = {index for index, target in enumerate(targets) if index == target}
    assert all(target in retained for target in targets)
    assert set(clique) <= retained
    for index, target in enumerate(targets):
        assert spaces[target] <= spaces[index]
        if index != target:
            assert any(dot(left, right) for left in rows[target] for right in rows[target])
    edges_checked = 0
    for index, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            if neighbor < index:
                first, second = targets[index], targets[neighbor]
                assert first != second
                assert all(dot(left, right) == 0 for left in rows[first] for right in rows[second])
                assert second in adjacency[first]
                edges_checked += 1
    full_counts = Counter()
    high_dimension_checked = 0
    for basis in bases(dimension, dimension):
        target_space = frozenset(span(target_basis(basis)))
        assert target_space in lookup and lookup[target_space] in retained
        assert target_space <= frozenset(span(basis))
        if len(basis) >= 4:
            assert any(dot(left, right) for left in target_basis(basis) for right in target_basis(basis))
            high_dimension_checked += 1
        full_counts[len(basis)] += 1
    uncolored = retained - set(clique)
    palettes = {vertex: set(original_palettes[vertex]) for vertex in uncolored}
    forced = {}
    if dimension == 7:
        forced = {vertex: next(iter(palettes[vertex]))
                  for vertex in uncolored if len(palettes[vertex]) == 1}
        assert len(forced) == 7 and set(forced.values()) == {15}
        for vertex, color in forced.items():
            assert all(other != vertex and other not in adjacency[vertex] for other in forced if other != vertex)
            for neighbor in adjacency[vertex] & uncolored:
                if neighbor not in forced:
                    palettes[neighbor].discard(color)
                    assert palettes[neighbor]
        uncolored.difference_update(forced)
        assert all(15 not in palettes[vertex] for vertex in uncolored)
    edges = sum(len(adjacency[vertex] & uncolored) for vertex in uncolored) // 2
    variables = sum(len(palettes[vertex]) for vertex in uncolored)
    clauses = sum(1 + len(palettes[vertex]) * (len(palettes[vertex]) - 1) // 2 for vertex in uncolored)
    clauses += sum(len(palettes[vertex] & palettes[neighbor]) for vertex in uncolored
                   for neighbor in adjacency[vertex] & uncolored if neighbor < vertex)
    expected_counts = {1: 127, 2: 651, 3: 135} if dimension == 7 else {1: 63, 2: 155, 3: 15}
    assert dict(Counter(len(rows[vertex]) for vertex in retained)) == expected_counts
    assert len(uncolored) == (890 if dimension == 7 else 218)
    return {'status': 'retraction_checked_no_new_coloring_or_unsat', 'dimension': dimension,
            'all_vertices': sum(full_counts.values()), 'all_dimension_counts': dict(sorted(full_counts.items())),
            'retained_vertices': len(retained), 'retained_dimension_counts': expected_counts,
            'retained_edges': sum(len(adjacency[vertex] & retained) for vertex in retained) // 2,
            'low_dimension_edges_independently_checked': edges_checked,
            'high_dimension_images_checked': high_dimension_checked,
            'fixed_clique_vertices': len(clique), 'extra_forced_vertices': len(forced),
            'uncolored_core': {'vertices': len(uncolored), 'edges': edges, 'variables': variables, 'clauses': clauses},
            'core_dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in uncolored).items())),
            'core_palette_sizes': dict(sorted(Counter(len(palettes[vertex]) for vertex in uncolored).items())),
            'color15_absent_from_n7_core': dimension == 7,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'construction_sha256': hashlib.sha256((ROOT / 'develop/dimension_seven_feasibility.py').read_bytes()).hexdigest(),
            'solver_run': False, 'lean_run': False,
            'scope': 'The written retraction proves equality of chromatic numbers in every dimension. Exact n6/n7 checks cover every vertex image and every edge among dimensions1to3. High-dimensional edges follow from containment and nonisotropic images in the written proof. No new coloring or nonexistence conclusion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    args = parser.parse_args()
    print(json.dumps(check(args.dimension), indent=2))
