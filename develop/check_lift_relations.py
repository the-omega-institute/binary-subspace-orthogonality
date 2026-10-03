"""Compare the author's lift-coordinate test with all original graph pairs."""

from collections import defaultdict
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

from check_complement_projection import dimension, enumerate_span
from check_lift_map_features import independent_features
from check_lift_map_values import independent_basis
import lift_relations as author

ROOT = Path(__file__).resolve().parents[1]


def coordinate_dot(first, second):
    return sum(((first >> coordinate) % 2) * ((second >> coordinate) % 2)
               for coordinate in range(6)) % 2


def main():
    start = time.monotonic()
    certificate_path = ROOT / 'results/full-15-coloring.json'
    output_path = ROOT / 'results/lift-relations.json'
    records = json.loads(certificate_path.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    assert all(coordinate_dot(first, second) == 0
               for first in isotropic_space for second in isotropic_space)
    entries = []
    requested_groups = defaultdict(set)
    full_groups = defaultdict(list)
    author.basis_of = lru_cache(maxsize=None)(author.basis_of)
    author.extend_lift = lru_cache(maxsize=None)(author.extend_lift)
    for record in records:
        space = enumerate_span(record['basis'])
        exact, features, mapping = independent_features(space, isotropic_space)
        intersection, projection = exact
        basis = independent_basis(projection)
        values = tuple(min(mapping[vector]) for vector in basis)
        data = (intersection, projection, values)
        assert author.lift_data(space, isotropic_space, complement) == data
        assert author.basis_of(projection) == basis
        assert enumerate_span(list(intersection) + [vector ^ value
                              for vector, value in zip(basis, values)]) == space
        for vector in projection:
            extended = author.extend_lift(basis, values, vector, intersection)
            assert extended == min(mapping[vector])
        mask = sum(1 << vector for vector in space)
        orthogonal_mask = sum(1 << vector for vector in range(64)
                              if all(coordinate_dot(vector, generator) == 0
                                     for generator in record['basis']))
        entries.append((space, data, record['color'], mask, orthogonal_mask))
        if not space <= isotropic_space:
            requested_groups[(dimension(intersection), dimension(projection), values)].add(record['color'])
            full_groups[data].append(space)
    assert len(entries) == 2824 and len({entry[0] for entry in entries}) == 2824
    assert len(full_groups) == 2809 and all(len(group) == 1 for group in full_groups.values())
    sample = [entry for entry in entries if not entry[0] <= isotropic_space][:20]
    sample_edges = sum(author.are_orthogonal(first[1], second[1])
                       for first, second in combinations(sample, 2))
    reproduced = {
        'total_groups': len(requested_groups),
        'multi_color_groups': sum(len(colors) > 1 for colors in requested_groups.values()),
        'full_data_groups': len(full_groups), 'full_data_multi_color_groups': 0,
        'sample_vertices': [list(independent_basis(entry[0])) for entry in sample],
        'sample_pairs': 190, 'orthogonal_pairs_in_sample': sample_edges,
        'monochromatic_orthogonal_pairs_in_sample': sum(
            first[2] == second[2] and author.are_orthogonal(first[1], second[1])
            for first, second in combinations(sample, 2)),
        'scope': 'First twenty non-clique vertices only; existing certificate colors, not a structural label construction.'
    }
    assert reproduced == json.loads(output_path.read_text())
    pair_count = 0
    edge_count = 0
    outside_pair_count = 0
    outside_edge_count = 0
    for index, first in enumerate(entries):
        for second in entries[index + 1:]:
            direct = first[3] & second[4] == first[3]
            relation = author.are_orthogonal(first[1], second[1])
            assert relation == direct, (first[0], second[0])
            pair_count += 1
            outside = not first[0] <= isotropic_space and not second[0] <= isotropic_space
            outside_pair_count += outside
            if direct:
                edge_count += 1
                outside_edge_count += outside
                assert first[2] != second[2]
        if (index + 1) % 700 == 0:
            print(f'Checked {pair_count} pairs', flush=True)
    assert pair_count == 3986076 and outside_pair_count == 3943836
    assert edge_count == 44968
    report = {
        'status': 'passed', 'vertices': len(entries), 'vertices_outside_clique': 2809,
        'all_lift_data_and_extensions_checked': True,
        'all_vertices_reconstructed': True,
        'author_output_reproduced': reproduced,
        'all_distinct_pairs_checked': pair_count,
        'orthogonality_edges_checked': edge_count,
        'non_clique_pairs_checked': outside_pair_count,
        'non_clique_edges_checked': outside_edge_count,
        'criterion_disagreements': 0, 'monochromatic_orthogonal_pairs': 0,
        'method': 'Author lift_data, basis and extensions compared to independently enumerated spans, coordinate projection and quotient cosets. Every author are_orthogonal result compared to coordinate-defined orthogonal-complement masks for distinct pairs of all2824 vertices, including the clique.',
        'optimization': 'Memoize only deterministic author basis_of and extend_lift functions; the author pair test itself is unchanged.',
        'elapsed_seconds': time.monotonic() - start,
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'author_script_sha256': hashlib.sha256((ROOT / 'develop/lift_relations.py').read_bytes()).hexdigest(),
        'author_output_sha256': hashlib.sha256(output_path.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Exhaustive replay of lift-coordinate adjacency and existing certificate colors, not a new certificate or structural15-label construction. Exact line chi12 remains proved; n7 and structural15-coloring remain open. No solver or Lean run; historical full-subspace n6 theorem retains four native-evaluation axioms.'
    }
    (ROOT / 'results/lift-relations-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
