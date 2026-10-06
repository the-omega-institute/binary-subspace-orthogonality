"""Compare two legitimate fixed sixteen-cliques for the seventeen-color target."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from search_nonradical_coloring import build_encoding
from dimension_seven_feasibility import span


def check():
    rows, spaces, adjacency, fixed, palettes, variables, cnf, previous = build_encoding(7)
    old_line = next(vertex for vertex, color in fixed.items() if color == 15)
    characteristic = next(vertex for vertex in adjacency if rows[vertex] == (127,))
    clique = [vertex for vertex, color in sorted(fixed.items(), key=lambda item: item[1]) if color < 15]
    clique.append(characteristic)
    assert all(neighbor in adjacency[vertex] for vertex, neighbor in combinations(clique, 2))
    new_fixed = {vertex: color for color, vertex in enumerate(clique)}
    core = set(adjacency) - set(new_fixed)
    lists = {vertex: set(range(17)) - {new_fixed[neighbor] for neighbor in adjacency[vertex] & new_fixed.keys()}
             for vertex in core}
    isotropic = frozenset(span((3, 12, 48)))
    for vertex in core:
        intersection = {vector for vector in isotropic if all((vector & row).bit_count() % 2 == 0 for row in rows[vertex])}
        geometric = {color for color, neighbor in enumerate(clique[:15]) if not spaces[neighbor] <= intersection}
        if any(row.bit_count() % 2 for row in rows[vertex]):
            geometric.add(15)
        geometric.add(16)
        assert lists[vertex] == geometric
    assert len(core) == 561 and sum(palette == {15, 16} for palette in lists.values()) == 7
    assert all(16 in palette for palette in lists.values())
    counts = {'vertices': len(core), 'edges': sum(len(adjacency[vertex] & core) for vertex in core) // 2,
              'variables': sum(len(palette) for palette in lists.values())}
    clauses = sum(1 + len(palette) * (len(palette) - 1) // 2 for palette in lists.values())
    clauses += sum(len(lists[vertex] & lists[neighbor]) for vertex in core
                   for neighbor in adjacency[vertex] & core if neighbor < vertex)
    counts['clauses'] = clauses
    assert counts == {'vertices': 561, 'edges': 17696, 'variables': 7814, 'clauses': 244442}
    assert len(adjacency[old_line]) == 153 and len(adjacency[characteristic]) == 513
    return {'status': 'alternative_clique_lists_and_counts_checked', 'dimension': 7, 'target_colors': 17,
            'fixed_clique_vertices': 16, 'extra_preassigned_vertices': 0, 'fixed_last_line_basis': [127],
            'old_last_line_basis': [64], 'old_last_line_retained_degree': 153, 'characteristic_line_retained_degree': 513,
            'original_instance': {key: previous[key] for key in ('core_vertices', 'core_edges', 'variables', 'clauses')},
            'alternative_instance': counts, 'palette_sizes': dict(sorted(Counter(len(palette) for palette in lists.values()).items())),
            'geometric_lists_checked': len(core), 'former_forced_lines_keep_both15and16': True,
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'construction_sha256': hashlib.sha256(Path(__file__).with_name('search_nonradical_coloring.py').read_bytes()).hexdigest(),
            'CNF_emitted_for_alternative': False, 'solver_run': False, 'lean_run': False,
            'scope': 'Exact comparison using the shared retained graph; geometric palettes separately checked. Any17coloring can be relabeled on either16clique. No assignments beyond its clique, no alternative CNF or second solver run, no chromatic conclusion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
