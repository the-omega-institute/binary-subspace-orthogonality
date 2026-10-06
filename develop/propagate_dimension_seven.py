"""Propagate fixed-clique color lists and apply reversible degree deletion."""
from collections import Counter, deque
from pathlib import Path
import argparse
import hashlib
import json

from dimension_seven_feasibility import build_instance, span


ROOT = Path(__file__).resolve().parents[1]


def encoding_counts(active, adjacency, palettes):
    variables = sum(len(palettes[vertex]) for vertex in active)
    vertex_clauses = sum(1 + len(palettes[vertex]) * (len(palettes[vertex]) - 1) // 2
                         for vertex in active)
    edge_clauses = sum(len(palettes[vertex] & palettes[neighbor])
                       for vertex in active for neighbor in adjacency[vertex] & active
                       if neighbor < vertex)
    edges = sum(len(adjacency[vertex] & active) for vertex in active) // 2
    return {'vertices': len(active), 'edges': edges, 'variables': variables,
            'clauses': vertex_clauses + edge_clauses}


def propagate(dimension):
    rows, adjacency, clique, palettes = build_instance(dimension)
    initial = encoding_counts(set(palettes), adjacency, palettes)
    expected = ({'vertices': 2080, 'edges': 39400, 'variables': 28600, 'clauses': 627510}
                if dimension == 6 else
                {'vertices': 14589, 'edges': 953057, 'variables': 214355, 'clauses': 12984679})
    if dimension == 7:
        assert initial == expected
    active = set(palettes)
    queue = deque(sorted(vertex for vertex in active if len(palettes[vertex]) == 1))
    initial_singletons = len(queue)
    forced = {}
    removed_color_count = 0
    while queue:
        vertex = queue.popleft()
        if vertex not in active:
            continue
        assert len(palettes[vertex]) == 1
        color = next(iter(palettes[vertex]))
        assert all(forced[neighbor] != color for neighbor in adjacency[vertex] & forced.keys())
        assert all(clique[color] != neighbor for neighbor in adjacency[vertex] & set(clique))
        forced[vertex] = color
        active.remove(vertex)
        for neighbor in sorted(adjacency[vertex] & active):
            if color in palettes[neighbor]:
                palettes[neighbor].remove(color)
                removed_color_count += 1
                assert palettes[neighbor], ('empty color list', rows[neighbor], rows[vertex], color)
                if len(palettes[neighbor]) == 1:
                    queue.append(neighbor)
    after_forcing = encoding_counts(active, adjacency, palettes)
    degree = {vertex: len(adjacency[vertex] & active) for vertex in active}
    queue = deque(sorted(vertex for vertex in active if degree[vertex] < len(palettes[vertex])))
    peeled = []
    while queue:
        vertex = queue.popleft()
        if vertex not in active:
            continue
        assert len(adjacency[vertex] & active) < len(palettes[vertex])
        active.remove(vertex)
        peeled.append(vertex)
        for neighbor in sorted(adjacency[vertex] & active):
            degree[neighbor] -= 1
            if degree[neighbor] < len(palettes[neighbor]):
                queue.append(neighbor)
    for vertex in active:
        assert len(palettes[vertex]) > 1
        assert len(adjacency[vertex] & active) >= len(palettes[vertex])
        assert not any(forced[neighbor] in palettes[vertex]
                       for neighbor in adjacency[vertex] & forced.keys())
    final = encoding_counts(active, adjacency, palettes)
    if dimension == 6:
        assert final == expected
    else:
        isotropic_space = set(span((3, 12, 48)))
        perpendicular_space = isotropic_space | {value ^ 64 for value in isotropic_space}
        geometric_forced = {vertex for vertex in palettes
                            if set(span(rows[vertex])) <= perpendicular_space
                            and not set(span(rows[vertex])) <= isotropic_space}
        assert set(forced) == geometric_forced
        assert set(forced.values()) == {15}
        for vertex in active:
            geometric_palette = set(range(15)) - {
                color for color, fixed in enumerate(clique[:15])
                if all((left & right).bit_count() % 2 == 0
                       for left in rows[vertex] for right in rows[fixed])}
            if 64 in span(rows[vertex] + (3, 12, 48)):
                geometric_palette.add(15)
            assert palettes[vertex] == geometric_palette
    components = []
    unseen = set(active)
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        component = {seed}
        queue = deque([seed])
        while queue:
            vertex = queue.popleft()
            neighbors = adjacency[vertex] & unseen
            unseen.difference_update(neighbors)
            component.update(neighbors)
            queue.extend(sorted(neighbors))
        components.append(len(component))
    return {
        'status': 'equivalent_reduction_no_coloring_or_nonexistence_result',
        'dimension': dimension, 'target_colors': len(clique),
        'initial_low_dimension_instance': initial,
        'initial_singleton_lists': initial_singletons,
        'forced_assignments_count': len(forced),
        'forced_dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in forced).items())),
        'forced_assignments': [{'vertex_index': vertex, 'basis': list(rows[vertex]), 'color': color}
                               for vertex, color in forced.items()],
        'neighbor_color_removals': removed_color_count,
        'after_forcing': after_forcing,
        'reversible_degree_deletions': len(peeled),
        'deletion_order': peeled,
        'final_core': final,
        'final_core_dimension_counts': dict(sorted(Counter(len(rows[vertex]) for vertex in active).items())),
        'final_palette_types': [{'dimension': rank, 'list_size': size, 'vertices': count}
                                for (rank, size), count in sorted(Counter(
                                    (len(rows[vertex]), len(palettes[vertex])) for vertex in active).items())],
        'connected_component_sizes': sorted(components, reverse=True),
        'geometric_forced_set_and_palette_identity_checked': dimension == 7,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'construction_sha256': hashlib.sha256((ROOT / 'develop/dimension_seven_feasibility.py').read_bytes()).hexdigest(),
        'solver_run': False, 'lean_run': False,
        'scope': 'Exact list propagation and reversible degree deletion on the fixed-clique low-dimensional graph. No coloring, UNSAT, time-to-solution or new chromatic equality is claimed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension', type=int, choices=(6, 7), default=7)
    args = parser.parse_args()
    print(json.dumps(propagate(args.dimension), indent=2))
