"""Independently replay the requested projection diagnostic and exact partition."""

from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def enumerate_span(basis):
    vectors = set()
    for coefficients in product((0, 1), repeat=len(basis)):
        vector = 0
        for coefficient, generator in zip(coefficients, basis):
            if coefficient:
                vector ^= generator
        vectors.add(vector)
    return frozenset(vectors)


def project_vector(vector):
    return (vector ^ (vector >> 1)) & 21


def dimension(space):
    assert len(space) and len(space) & (len(space) - 1) == 0
    return len(space).bit_length() - 1


def analyze():
    certificate_path = ROOT / 'results/full-15-coloring.json'
    diagnostic_path = ROOT / 'results/complement-projection.json'
    certificate = json.loads(certificate_path.read_text())
    diagnostic = json.loads(diagnostic_path.read_text())
    isotropic_space = enumerate_span([3, 12, 48])
    complement = enumerate_span([1, 4, 16])
    assert isotropic_space & complement == {0}
    assert {first ^ second for first in isotropic_space
            for second in complement} == set(range(64))
    for vector in range(64):
        image = project_vector(vector)
        assert image in complement and vector ^ image in isotropic_space
    groups = defaultdict(list)
    exact_to_projection = defaultdict(set)
    projection_to_exact = defaultdict(set)
    line_records = {}
    for record in certificate['subspace_colors']:
        space = enumerate_span(record['basis'])
        if space <= isotropic_space:
            continue
        intersection = space & isotropic_space
        image = frozenset(project_vector(vector) for vector in space)
        annihilator = frozenset(vector for vector in isotropic_space
                                if all((vector & generator).bit_count() % 2 == 0
                                       for generator in record['basis']))
        recovered_image = frozenset(vector for vector in complement
                                   if all((vector & test).bit_count() % 2 == 0
                                          for test in annihilator))
        assert image == recovered_image
        assert dimension(space) == dimension(intersection) + dimension(image)
        profile = (dimension(space), tuple(sorted(intersection)),
                   tuple(sorted(image)))
        exact = (dimension(space), tuple(sorted(annihilator)),
                 tuple(sorted(intersection)))
        groups[profile].append(record)
        exact_to_projection[exact].add(profile)
        projection_to_exact[profile].add(exact)
        if space in (frozenset({0, 1}), frozenset({0, 2})):
            line_records[min(space - {0})] = {
                'profile': profile, 'color': record['color']}
    assert len(groups) == len(exact_to_projection) == 240
    assert all(len(images) == 1 for images in exact_to_projection.values())
    assert all(len(images) == 1 for images in projection_to_exact.values())
    assert sum(map(len, groups.values())) == 2809
    multi = {profile: {record['color'] for record in records}
             for profile, records in groups.items()
             if len({record['color'] for record in records}) > 1}
    reproduced = {
        'total_profiles': len(groups),
        'single_color_profiles': len(groups) - len(multi),
        'multi_color_profiles': len(multi),
        'first_multi_color_examples': [
            {'dim_U': profile[0], 'U_intersect_T': list(profile[1]),
             'projection_to_S': list(profile[2]), 'colors': sorted(colors)}
            for profile, colors in list(multi.items())[:10]],
    }
    assert reproduced == diagnostic
    for profile, records in groups.items():
        kernel_dimension = dimension(profile[1])
        image_dimension = dimension(profile[2])
        assert len(records) == 2 ** (image_dimension * (3 - kernel_dimension))
    assert line_records[1]['profile'] == line_records[2]['profile']
    assert (1 & 2).bit_count() % 2 == 0
    return {
        'status': 'passed',
        'method': 'Coefficient-tuple span enumeration and coordinate parity projection; independently recovered each image as the annihilator of H inside S.',
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'diagnostic_sha256': hashlib.sha256(diagnostic_path.read_bytes()).hexdigest(),
        'checked_vertices_outside_clique': 2809,
        'reproduced_entire_diagnostic_json': True,
        'total_profiles': len(groups),
        'single_color_profiles': len(groups) - len(multi),
        'multi_color_profiles': len(multi),
        'partition_identity': 'Every exact (dim U,H,K) group maps to exactly one projection group and conversely; the partitions are identical, not just their counts.',
        'all_240_fiber_cardinalities_checked': 'For K dimension k and nonzero P dimension p, the number of lifts is 2^(p*(3-k)).',
        'adjacent_lines': line_records,
        'validation_limits': 'No full edge/coloring check, solver search or Lean run. Projection equivalence and impossibility of a projection-pair coloring are written proofs; a structural 15-coloring and n7 remain open.'
    }


if __name__ == '__main__':
    result = analyze()
    output = ROOT / 'results/complement-projection-check.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
