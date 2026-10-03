"""Check the normalized line encoding and complete 12-color witness independently."""

import hashlib
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def coordinate_dot(first, second):
    return sum(((first >> coordinate) % 2) * ((second >> coordinate) % 2)
               for coordinate in range(6)) % 2


def validate_coloring(data):
    assert data['dimension'] == 6 and data['colors'] == 12
    classes = data['classes']
    assert len(classes) == 12 and all(classes)
    assert all(type(vertex) is int for group in classes for vertex in group)
    assert sorted(vertex for group in classes for vertex in group) == list(range(1, 64))
    assigned = {vertex: color for color, group in enumerate(classes) for vertex in group}
    edges = 0
    for first, second in combinations(range(1, 64), 2):
        if coordinate_dot(first, second) == 0:
            edges += 1
            assert assigned[first] != assigned[second]
    return edges


def main():
    certificate_path = ROOT / 'results/line-coloring-12.json'
    search_path = ROOT / 'results/line-chromatic-exact.json'
    data = json.loads(certificate_path.read_text())
    search = json.loads(search_path.read_text())
    edges = validate_coloring(data)
    fixed_class = [1, 3, 5, 9, 17, 33]
    assert data['classes'][-1] == fixed_class
    assert all(coordinate_dot(first, second) == 1
               for first, second in combinations(fixed_class, 2))
    vertices = sorted(set(range(1, 64)) - set(fixed_class))
    variable = {(vertex, color): index * 11 + color + 1
                for index, vertex in enumerate(vertices) for color in range(11)}
    expected = []
    for vertex in vertices:
        expected.append(tuple(variable[vertex, color] for color in range(11)))
    for vertex in vertices:
        expected.extend((-variable[vertex, first], -variable[vertex, second])
                        for first, second in combinations(range(11), 2))
    remaining_edges = [(first, second) for first, second in combinations(vertices, 2)
                       if coordinate_dot(first, second) == 0]
    expected.extend((-variable[first, color], -variable[second, color])
                    for first, second in remaining_edges for color in range(11))
    clauses = expected
    assert len(clauses) == 11772
    encoded = 'p cnf 627 11772\n' + ''.join(
        ' '.join(map(str, clause)) + ' 0\n' for clause in clauses)
    cnf_digest = hashlib.sha256(encoded.encode()).hexdigest()
    assert len(set(variable.values())) == 627
    assignment = {variable[vertex, color]
                  for color, group in enumerate(data['classes'][:-1]) for vertex in group}
    assert all(any((literal in assignment) if literal > 0 else (-literal not in assignment)
                   for literal in clause) for clause in clauses)
    assert search['status'] == 'sat_candidate'
    assert search['cnf_sha256'] == cnf_digest
    assert search['certificate_sha256'] == hashlib.sha256(certificate_path.read_bytes()).hexdigest()
    controls = []
    for name in ('duplicate_vertex', 'zero_vector', 'monochromatic_edge'):
        invalid = json.loads(certificate_path.read_text())
        if name == 'duplicate_vertex':
            invalid['classes'][0][0] = invalid['classes'][1][0]
        elif name == 'zero_vector':
            invalid['classes'][0][0] = 0
        else:
            first, second = next(pair for pair in combinations(range(1, 64), 2)
                                 if coordinate_dot(*pair) == 0)
            group_index = next(index for index, group in enumerate(invalid['classes'])
                               if first in group)
            for group in invalid['classes']:
                if second in group:
                    group.remove(second)
            invalid['classes'][group_index].append(second)
        try:
            validate_coloring(invalid)
        except AssertionError:
            controls.append(name)
        else:
            raise AssertionError('Invalid control accepted: ' + name)
    report = {
        'status': 'passed', 'dimension': 6, 'colors': 12, 'vertices': 63,
        'all_distinct_vertex_pairs_checked': 1953, 'orthogonality_edges_checked': edges,
        'class_sizes': list(map(len, data['classes'])),
        'normalized_remaining_vertices': 57, 'normalized_edges': len(remaining_edges),
        'cnf_variables': 627, 'cnf_clauses': len(clauses),
        'every_clause_reproduced_by_coordinate_method': True,
        'certificate_satisfies_every_CNF_clause': True,
        'invalid_controls_rejected': controls,
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'cnf_sha256': cnf_digest,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'conclusion': 'Checked upper bound 12 combines with the existing written weighted lower bound 12 to prove chi(Gamma_6)=12.',
        'scope': 'Standard-library finite coloring and encoding check, not a Lean theorem or new result for n7.'
    }
    (ROOT / 'results/line-coloring-12-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
