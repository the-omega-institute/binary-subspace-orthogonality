"""Compare numerical partitions with refinements retaining the exact H and K."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from check_full_coloring import dot, span
from refine_geometry import analyze as numerical_analysis
from refine_geometry__arf import analyze as parity_analysis

ROOT = Path(__file__).resolve().parents[1]


def binary_rank(rows):
    pivots = {}
    for row in rows:
        reduced = row
        while reduced:
            position = reduced.bit_length() - 1
            if position in pivots:
                reduced ^= pivots[position]
            else:
                pivots[position] = reduced
                break
    return len(pivots)


def summarize(groups):
    counts = [Counter(record['color'] for record in records)
              for records in groups.values()]
    return {
        'profiles': len(counts),
        'single_color_profiles': sum(len(colors) == 1 for colors in counts),
        'multi_color_profiles': sum(len(colors) > 1 for colors in counts),
        'vertices_in_multi_color_profiles': sum(
            sum(colors.values()) for colors in counts if len(colors) > 1),
        'maximum_colors_in_one_profile': max(map(len, counts)),
        'minimum_disagreements_with_fixed_witness': sum(
            sum(colors.values()) - max(colors.values()) for colors in counts),
    }


def analyze(certificate):
    data = json.loads(certificate.read_text())
    assert data['dimension'] == 6 and data['colors'] == 15
    isotropic_space = span([3, 12, 48])
    partitions = {name: defaultdict(list) for name in (
        'dimension_only', 'original_numerical', 'numerical_with_parity',
        'exact_baseline', 'exact_with_quotient_dimension',
        'exact_with_bilinear_invariants')}
    refinement_maps = defaultdict(lambda: defaultdict(set))
    parity_values = defaultdict(set)
    for record in data['subspace_colors']:
        space = span(record['basis'])
        if space <= isotropic_space:
            continue
        dimension = len(record['basis'])
        orthogonal = frozenset(vector for vector in isotropic_space
                              if all(dot(vector, basis) == 0
                                     for basis in record['basis']))
        intersection = space & isotropic_space
        radical = frozenset(vector for vector in space
                            if all(dot(vector, basis) == 0
                                   for basis in record['basis']))
        radical_dimension = len(radical).bit_length() - 1
        quotient_dimension = dimension - radical_dimension
        gram_rows = [sum(dot(first, second) << index
                         for index, second in enumerate(record['basis']))
                     for first in record['basis']]
        assert binary_rank(gram_rows) == quotient_dimension
        alternating = all(dot(basis, basis) == 0 for basis in record['basis'])
        assert all(dot(vector, vector) == 0 for vector in space) == alternating
        assert space & orthogonal == intersection & orthogonal
        parity = sum(dot(vector, vector) == 0
                     for vector in space - radical) % 2
        expected_count = ((1 << dimension) if alternating else
                          (1 << (dimension - 1))) - (1 << radical_dimension)
        assert sum(dot(vector, vector) == 0
                   for vector in space - radical) == expected_count
        dimension_key = (dimension, len(orthogonal).bit_length() - 1,
                         len(intersection).bit_length() - 1)
        exact_key = (dimension, tuple(sorted(orthogonal)),
                     tuple(sorted(intersection)))
        common_dimension = len(space & orthogonal).bit_length() - 1
        numerical_key = dimension_key + (common_dimension, common_dimension,
                                          (quotient_dimension,))
        parity_key = dimension_key + (common_dimension, common_dimension,
                                       (quotient_dimension, parity))
        rank_key = exact_key + (quotient_dimension,)
        bilinear_key = rank_key + (alternating,)
        keys = (dimension_key, numerical_key, parity_key, exact_key,
                rank_key, bilinear_key)
        for name, key in zip(partitions, keys):
            partitions[name][key].append(record)
        refinement_maps['quotient_dimension'][exact_key].add(rank_key)
        refinement_maps['bilinear_invariants'][exact_key].add(bilinear_key)
        parity_values[numerical_key].add(parity)
    stats = {name: summarize(groups) for name, groups in partitions.items()}
    for name, original in (
            ('original_numerical', numerical_analysis(certificate)),
            ('numerical_with_parity', parity_analysis(certificate))):
        assert stats[name]['profiles'] == original['total_refined_profiles']
        assert stats[name]['multi_color_profiles'] == original['multi_color_profiles']
        assert stats[name]['single_color_profiles'] == original['single_color_profiles']
    assert all(len(values) == 1 for values in parity_values.values())
    refinements = {}
    for name, mapping in refinement_maps.items():
        target = partitions['exact_with_' + name]
        refinements[name] = {
            'baseline_profiles_split': sum(len(children) > 1
                                           for children in mapping.values()),
            'baseline_multicolor_profiles_fully_resolved': sum(
                len({record['color'] for record in partitions['exact_baseline'][key]}) > 1
                and all(len({record['color'] for record in target[child]}) == 1
                        for child in children)
                for key, children in mapping.items()),
        }
    first_line = span([1])
    second_line = span([2])
    witness_key = (1, tuple(sorted(span([12, 48]))), (0,), 1, False)
    witness_records = partitions['exact_with_bilinear_invariants'][witness_key]
    first_record = next(record for record in witness_records
                        if span(record['basis']) == first_line)
    second_record = next(record for record in witness_records
                         if span(record['basis']) == second_line)
    assert first_line != second_line
    assert all(dot(first, second) == 0 for first in first_line for second in second_line)
    assert first_record['color'] != second_record['color']
    multicolor_profiles = [
        {'dimension': key[0], 'H_vectors': list(key[1]), 'K_vectors': list(key[2]),
         'quotient_dimension': key[3], 'alternating': key[4],
         'vertices': len(records),
         'color_counts': dict(sorted(Counter(record['color'] for record in records).items())),
         'members': records}
        for key, records in sorted(partitions['exact_with_bilinear_invariants'].items())
        if len({record['color'] for record in records}) > 1]
    return {
        'status': 'passed',
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'partitions': stats,
        'exact_refinement_comparison': refinements,
        'identities_checked_on_all_outside_vertices': {
            'vertices': 2809, 'U_intersect_H_equals_K_intersect_H': True,
            'gram_rank_equals_quotient_dimension': True,
            'self_orthogonal_count_formula': True,
            'parity_splits_original_numerical_profiles': False},
        'adjacent_same_profile_witness': {
            'first': first_record, 'second': second_record,
            'H_vectors': list(witness_key[1]), 'K_vectors': list(witness_key[2]),
            'quotient_dimension': 1, 'alternating': False,
            'conclusion': 'No proper coloring can depend only on this exact profile and these quotient invariants.'},
        'remaining_exact_multicolor_profiles': multicolor_profiles,
        'scope': 'Finite partition statistics for the fixed witness, plus a coordinate obstruction. '
                 'Minimum disagreements ignore edges and are not feasible recoloring counts. '
                 'The parity is not an Arf invariant; n=7 remains open.'}


if __name__ == '__main__':
    report = analyze(ROOT / 'results/full-15-coloring.json')
    output = ROOT / 'results/geometry-profile-audit.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key != 'remaining_exact_multicolor_profiles'}, indent=2))
