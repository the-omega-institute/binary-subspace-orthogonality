"""Replay the author's color statistics and test the label-matrix conditions."""

from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import runpy
import time

from check_complement_projection import dimension, enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis

ROOT = Path(__file__).resolve().parents[1]


def coordinate_dot(first, second):
    return sum(((first >> coordinate) % 2) * ((second >> coordinate) % 2)
               for coordinate in range(6)) % 2


def separated_by_blocks(first, second, products):
    first_kernel, first_projection, first_values = first
    second_kernel, second_projection, second_values = second
    if any(products[kernel][vector] for kernel in first_kernel for vector in second_projection):
        return True
    if any(products[vector][kernel] for vector in first_projection for kernel in second_kernel):
        return True
    return any(products[first_vector][second_vector]
               ^ products[first_value][second_vector]
               ^ products[first_vector][second_value]
               for first_vector, first_value in zip(first_projection, first_values)
               for second_vector, second_value in zip(second_projection, second_values))


def main():
    start = time.monotonic()
    script_path = ROOT / 'develop/analyze_color_function'
    author = runpy.run_path(str(script_path))
    certificate_path = ROOT / 'results/full-15-coloring.json'
    output_path = ROOT / 'results/color-function-analysis.json'
    records = json.loads(certificate_path.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    labels = {}
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            labels[record['color']] = space
    assert set(labels) == set(range(15)) and len(set(labels.values())) == 15
    by_projection = defaultdict(set)
    by_full = defaultdict(set)
    by_color = defaultdict(set)
    fibers = defaultdict(list)
    palette_sizes = defaultdict(int)
    products = [[coordinate_dot(first, second) for second in range(64)] for first in range(64)]
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        exact, features, mapping = independent_features(space, isotropic_space)
        kernel, projection = exact
        basis = independent_basis(projection)
        values = tuple(min(mapping[vector]) for vector in basis)
        assert author['lift_data'](space, isotropic_space, complement) == (kernel, projection, values)
        assert author['dim'](kernel) == dimension(kernel)
        assert author['dim'](projection) == dimension(projection)
        assert enumerate_span(list(kernel) + [vector ^ value for vector, value in zip(basis, values)]) == space
        color = record['color']
        by_projection[exact].add(color)
        by_full[(exact, values)].add(color)
        by_color[color].add(exact)
        kernel_basis = independent_basis(kernel)
        fibers[color].append((kernel_basis, basis, values))
        allowed = {label for label, label_space in labels.items()
                   if any(products[vector][argument]
                          for vector in independent_basis(label_space) for argument in basis)}
        assert color in allowed
        annihilator = frozenset(vector for vector in isotropic_space
                               if all(products[vector][argument] == 0 for argument in basis))
        assert allowed == {label for label, label_space in labels.items() if not label_space <= annihilator}
        assert len(allowed) in (11, 14, 15)
        palette_sizes[len(allowed)] += 1
    reproduced = {
        'distinct_K_P_pairs': len(by_projection),
        'multi_color_K_P_pairs': sum(len(colors) > 1 for colors in by_projection.values()),
        'distinct_full_tuples': len(by_full),
        'multi_color_full_tuples': sum(len(colors) > 1 for colors in by_full.values()),
        'color_K_P_diversity': {str(color): len(pairs) for color, pairs in sorted(by_color.items())},
        'scope': 'Statistics of the fixed certificate; full lift tuples identify vertices, not a new structural color formula.'
    }
    assert reproduced == json.loads(output_path.read_text())
    assert len(by_full) == 2809
    same_label_pairs = 0
    for entries in fibers.values():
        for first, second in combinations(entries, 2):
            assert separated_by_blocks(first, second, products)
            same_label_pairs += 1
    assert not separated_by_blocks(((), (1,), (0,)), ((), (4,), (0,)), products)
    assert separated_by_blocks(((), (1,), (0,)), ((), (1, 4), (0, 0)), products)
    assert separated_by_blocks(((3,), (), ()), ((), (1,), (0,)), products)
    report = {
        'status': 'passed', 'vertices_outside_clique': 2809,
        'author_output_reproduced': reproduced,
        'label_subspaces': [{'color': color, 'basis': list(independent_basis(space))}
                           for color, space in sorted(labels.items())],
        'palette_sizes': dict(sorted(palette_sizes.items())),
        'every_fixed_color_passes_label_projection_matrix_condition': True,
        'same_label_non_clique_pairs_checked': same_label_pairs,
        'every_same_label_pair_has_a_nonzero_cross_kernel_or_lift_block': True,
        'coordinate_examples_checked': ['adjacent_zero_lift_lines', 'essential_S_S_term', 'essential_cross_kernel_condition'],
        'elapsed_seconds': time.monotonic() - start,
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'author_script_sha256': hashlib.sha256(script_path.read_bytes()).hexdigest(),
        'author_output_sha256': hashlib.sha256(output_path.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Independent exact-statistics and label/fiber checks on the existing certificate. The matrix criterion is a written equivalence, not a new label formula. No solver or Lean run; n7 and structural15-coloring remain open; historical n6 full theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/color-function-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
