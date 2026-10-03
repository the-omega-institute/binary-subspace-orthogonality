"""Replay value patterns and check the full domain/quotient representation."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from check_complement_projection import dimension, enumerate_span
from check_lift_map_features import independent_features
from lift_map_value import basis_of, lift_map_pattern

ROOT = Path(__file__).resolve().parents[1]


def independent_basis(space):
    basis = []
    for vector in sorted(space, reverse=True):
        remainder = min(vector ^ previous for previous in enumerate_span(basis))
        if remainder:
            basis.append(remainder)
            basis.sort(reverse=True)
    assert enumerate_span(basis) == space
    assert len(basis) == dimension(space)
    return tuple(basis)


def summary(groups):
    counts = [Counter(record['color'] for record in members)
              for members in groups.values()]
    return {
        'profiles': len(counts),
        'single_color_profiles': sum(len(count) == 1 for count in counts),
        'multi_color_profiles': sum(len(count) > 1 for count in counts),
        'vertices_in_multi_color_profiles': sum(sum(count.values()) for count in counts
                                                if len(count) > 1),
        'minimum_disagreements_with_fixed_witness': sum(
            sum(count.values()) - max(count.values()) for count in counts),
    }


def analyze():
    certificate_path = ROOT / 'results/full-15-coloring.json'
    output_path = ROOT / 'results/lift-map-values.json'
    records = json.loads(certificate_path.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    requested = defaultdict(list)
    requested_to_exact = defaultdict(set)
    full_values = defaultdict(list)
    previous_features = defaultdict(list)
    feature_to_values = defaultdict(set)
    projection_to_values = defaultdict(set)
    line_records = {}
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        exact, features, mapping = independent_features(space, isotropic_space)
        intersection, projection = exact
        basis = independent_basis(projection)
        assert basis == basis_of(projection)
        values = tuple(min(mapping[vector]) for vector in basis)
        pattern = (dimension(intersection), dimension(projection), values)
        assert pattern == lift_map_pattern(space, isotropic_space, complement)
        lifted_basis = [vector ^ value for vector, value in zip(basis, values)]
        assert enumerate_span(list(intersection) + lifted_basis) == space
        requested[pattern].append(record)
        requested_to_exact[pattern].add(exact)
        full_key = (exact, values)
        full_values[full_key].append(record)
        previous_key = (exact, features)
        previous_features[previous_key].append(record)
        feature_to_values[previous_key].add(full_key)
        projection_to_values[exact].add(full_key)
        if space in (frozenset({0, 1}), frozenset({0, 4})):
            line_records[min(space - {0})] = {
                'basis': list(basis), 'pattern': pattern, 'color': record['color']}
    assert sum(map(len, requested.values())) == 2809
    assert len(full_values) == 2809
    assert all(len(members) == 1 for members in full_values.values())
    multi = {pattern: {record['color'] for record in members}
             for pattern, members in requested.items()
             if len({record['color'] for record in members}) > 1}
    reproduced = {
        'total_profiles': len(requested),
        'single_color_profiles': len(requested) - len(multi),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_K': pattern[0], 'dim_P': pattern[1],
             'f_values': list(pattern[2]), 'colors': sorted(colors)}
            for pattern, colors in list(multi.items())[:10]]}
    assert reproduced == json.loads(output_path.read_text())
    assert line_records[1]['pattern'] == line_records[4]['pattern'] == (0, 1, (0,))
    assert (1 & 4).bit_count() % 2 == 0
    previous_mixed = {key for key, members in previous_features.items()
                      if len({record['color'] for record in members}) > 1}
    assert len(previous_mixed) == 160
    assert all(all(len(full_values[value_key]) == 1
                   for value_key in feature_to_values[feature_key])
               for feature_key in previous_mixed)
    return {
        'status': 'passed',
        'method': 'Independent coefficient-tuple spans, coordinate projection and quotient cosets; canonical basis replayed by exhaustive minimum over the preceding span rather than the author elimination algorithm.',
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'requested_output_sha256': hashlib.sha256(output_path.read_bytes()).hexdigest(),
        'checked_vertices_outside_clique': 2809,
        'each_author_value_pattern_verified': True,
        'entire_requested_JSON_reproduced': True,
        'requested_pattern_partition': summary(requested),
        'requested_patterns_mixing_exact_K_P': sum(
            len(exacts) > 1 for exacts in requested_to_exact.values()),
        'previous_exact_K_P_plus_rank_image_kernel': summary(previous_features),
        'exact_K_P_plus_basis_values': summary(full_values),
        'all_vertices_reconstructed_from_K_and_basis_lifts': True,
        'all_160_previous_mixed_feature_groups_resolve_to_singletons': True,
        'original_exact_K_P_profiles': len(projection_to_values),
        'omitted_domain_counterexample': {
            'first_line': line_records[1], 'second_line': line_records[4],
            'cross_dot_product': 0,
            'conclusion': 'The value lists agree but their domain bases differ; the literal pattern alone cannot support a proper coloring.'
        },
        'scope': 'Full K,P and basis values encode U itself; singleton profiles do not constitute a structural 15-color construction. No finer description is needed to reconstruct U, but a proved 15-label assignment is still needed.',
        'validation_limits': 'Targeted geometry replay only; no full/line edge-checker rerun, solver search or Lean run. Original final n6 Lean theorem retains four native-evaluation axioms. Structural15-coloring, exact line chromatic number and n7 remain open.'
    }


if __name__ == '__main__':
    result = analyze()
    (ROOT / 'results/lift-map-values-check.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
