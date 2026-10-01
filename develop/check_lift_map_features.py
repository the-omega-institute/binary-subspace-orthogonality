"""Check lift features and compare them within the exact projection partition."""

from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path

from check_complement_projection import dimension, enumerate_span, project_vector
from lift_map_matrix import lift_map_features

ROOT = Path(__file__).resolve().parents[1]


def independent_features(space, isotropic_space):
    intersection = space & isotropic_space
    projection = frozenset(project_vector(vector) for vector in space)
    mapping = {}
    for vector in space:
        image_vector = project_vector(vector)
        quotient_value = frozenset(vector ^ image_vector ^ kernel_vector
                                   for kernel_vector in intersection)
        if image_vector in mapping:
            assert mapping[image_vector] == quotient_value
        mapping[image_vector] = quotient_value
    assert mapping[0] == intersection
    for first, second in combinations(projection, 2):
        assert {first_value ^ second_value for first_value in mapping[first]
                for second_value in mapping[second]} == mapping[first ^ second]
    image = frozenset(mapping.values())
    kernel = frozenset(vector for vector, value in mapping.items()
                       if value == intersection)
    assert dimension(projection) == dimension(image) + dimension(kernel)
    assert kernel == space & enumerate_span([1, 4, 16])
    assert len(space) == len(intersection) * len(projection)
    features = (dimension(intersection), dimension(projection), dimension(image),
                image, kernel)
    return (intersection, projection), features, mapping


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
    diagnostic_path = ROOT / 'results/lift-map-matrix.json'
    records = json.loads(certificate_path.read_text())['subspace_colors']
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    baseline = defaultdict(list)
    requested = defaultdict(list)
    refined = defaultdict(list)
    full_maps = defaultdict(list)
    base_to_refined = defaultdict(set)
    requested_to_baseline = defaultdict(set)
    spaces_by_basis = {}
    for record in records:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        exact, features, mapping = independent_features(space, isotropic_space)
        assert features == lift_map_features(space, isotropic_space, complement)
        baseline[exact].append(record)
        requested[features].append(record)
        refined[(exact, features)].append(record)
        base_to_refined[exact].add((exact, features))
        requested_to_baseline[features].add(exact)
        full_key = (exact, tuple((vector, tuple(sorted(value)))
                                for vector, value in sorted(mapping.items())))
        full_maps[full_key].append(record)
        spaces_by_basis[tuple(record['basis'])] = (space, exact, features, mapping)
    assert sum(map(len, baseline.values())) == 2809
    assert len(baseline) == 240 and len(full_maps) == 2809
    assert all(len(members) == 1 for members in full_maps.values())
    requested_stats = summary(requested)
    multi = {features: {record['color'] for record in members}
             for features, members in requested.items()
             if len({record['color'] for record in members}) > 1}
    reproduced = {
        'total_profiles': len(requested),
        'single_color_profiles': len(requested) - len(multi),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_K': features[0], 'dim_P': features[1], 'rank_f': features[2],
             'image': sorted(sorted(value) for value in features[3]),
             'kernel': sorted(features[4]), 'colors': sorted(colors)}
            for features, colors in list(multi.items())[:10]]}
    assert reproduced == json.loads(diagnostic_path.read_text())
    original_multi = {exact for exact, members in baseline.items()
                      if len({record['color'] for record in members}) > 1}
    resolved = sum(all(len({record['color'] for record in refined[key]}) == 1
                       for key in base_to_refined[exact]) for exact in original_multi)
    first_space, first_exact, first_features, first_map = spaces_by_basis[(13, 6)]
    second_space, second_exact, second_features, second_map = spaces_by_basis[(9, 14)]
    assert first_space != second_space
    assert first_exact == second_exact and first_features == second_features
    cross_gram = [[(first & second).bit_count() % 2 for second in (9, 14)]
                  for first in (13, 6)]
    assert cross_gram == [[0, 0], [0, 0]]
    assert first_map != second_map
    return {
        'status': 'passed',
        'method': 'Independent coordinate projection and coefficient-tuple spans; quotient values include zero, with consistency, linearity and rank-nullity checked for every non-clique vertex. Compared every feature tuple to the corrected author function.',
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'diagnostic_sha256': hashlib.sha256(diagnostic_path.read_bytes()).hexdigest(),
        'checked_vertices_outside_clique': 2809,
        'entire_requested_output_reproduced': True,
        'original_projection_partition': summary(baseline),
        'requested_feature_partition': requested_stats,
        'requested_groups_spanning_multiple_original_groups': sum(
            len(exacts) > 1 for exacts in requested_to_baseline.values()),
        'exact_profile_plus_features': summary(refined),
        'original_multi_color_profiles_completely_resolved': resolved,
        'original_multi_color_profiles_still_unresolved': len(original_multi) - resolved,
        'full_lift_map_profiles': len(full_maps),
        'full_lift_map_scope': 'All 2809 maps with K and P distinguish vertices; this is the proved full representation, not a compression or 15-color construction.',
        'adjacent_equal_feature_planes': {
            'first_basis': [13, 6], 'second_basis': [9, 14],
            'first_vectors': sorted(first_space), 'second_vectors': sorted(second_space),
            'K_vectors': sorted(first_exact[0]), 'P_vectors': sorted(first_exact[1]),
            'rank': first_features[2],
            'image_cosets': sorted(sorted(value) for value in first_features[3]),
            'kernel_vectors': sorted(first_features[4]),
            'first_map': {str(vector): sorted(value) for vector, value in sorted(first_map.items())},
            'second_map': {str(vector): sorted(value) for vector, value in sorted(second_map.items())},
            'cross_gram': cross_gram,
            'conclusion': 'No proper coloring solely from K,P,rank,image,kernel; written obstruction independent of witness color choices.'
        },
        'validation_limits': 'Targeted finite geometry checks and written obstruction only; no full/line coloring-checker rerun, solver or Lean execution. Structural 15-coloring, exact line chromatic number and n7 remain open.'
    }


if __name__ == '__main__':
    result = analyze()
    (ROOT / 'results/lift-map-matrix-check.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
