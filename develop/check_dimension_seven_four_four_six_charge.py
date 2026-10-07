"""Audit the transferable pure-six sum and recoloring exclusion of (4,4,6;7,0,8)."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum


def accounting(root):
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    previous = json.loads((root / 'results/dimension-7-two-six-six-cover-check.json').read_text())
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 38}
    target = [4, 4, 6, 7, 0, 8]
    remaining = {}
    distributions = {}
    for name, sizes, prefix in (('5+6', (5, 6), 'five_six'), ('6+6+6', (6, 6, 6), 'three_six')):
        domains = [range(size + 1) if size != 6 else (0, 2, 4, 5, 6) for size in sizes]
        direct = set()
        for counts in product(*domains):
            if name == '6+6+6' and tuple(sorted(counts)) != counts:
                continue
            for pure_even in range(19):
                for mixed in range(19):
                    pure_odd = 18 - len(sizes) - pure_even - mixed
                    if pure_odd >= 0 and 7 * pure_even + 6 * mixed + sum(counts) == 63 and mixed + 7 * pure_odd + sum(sizes) - sum(counts) + 4 == 64:
                        direct.add(counts + (pure_even, mixed, pure_odd))
        archived = {tuple(row['defect_even_counts'] + row['saturated_counts']) for row in raw['count_profiles'][name]}
        assert direct == archived and len(direct) == (46 if prefix == 'five_six' else 48)
        prior = previous['remaining_raw_profile_lists'][prefix]
        assert len(prior) == (25 if prefix == 'five_six' else 38)
        assert len({tuple(row) for row in prior}) == len(prior)
        assert all(tuple(row) in direct for row in prior)
        if prefix == 'three_six':
            assert prior.count(target) == 1
            current = [row for row in prior if row != target]
        else:
            current = prior
        remaining[prefix] = current
        distributions[prefix] = dict(sorted(Counter(row[-1] for row in current).items()))
    assert distributions == {'five_six': {6: 6, 7: 19}, 'three_six': {5: 2, 6: 14, 7: 18, 8: 3}}
    return {'newly_excluded_raw_profile': target, 'new_raw_profile_exclusions': 1,
            'remaining_raw_profiles': {prefix: len(rows) for prefix, rows in remaining.items()},
            'remaining_raw_profile_lists': remaining, 'remaining_counts_by_pure_odd_heptads': distributions,
            'total_excluded_profiles': {'five_six': 21, 'three_six': 11},
            'remaining_C6_through_C8_count': 60, 'remaining_C5_count': 2,
            'all_nineteen_color_branches_excluded': False, 'characteristic_sizes_still_open': [4, 5, 6, 7, 8]}


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    four = bit_cliques(even, 4)
    six = bit_cliques(even, 6)
    assert four == array_cliques(even, 4) and six == array_cliques(even, 6)
    catalogs = {}
    original_class_controls = 0
    for even_sum, charge in permutations(sorted(holes), 2):
        blocks = [block for block in four if vector_sum(block) == even_sum
                  and all(dot(point, even_sum) and dot(point, charge) for point in block)]
        assert len(blocks) == 16
        for block in blocks:
            original = block + (127 ^ even_sum, 127 ^ charge)
            assert all(dot(left, right) for left, right in combinations(original, 2))
            assert vector_sum(original) == charge
            assert not set(block) & holes
            original_class_controls += 1
        catalogs[(even_sum, charge)] = [(block, mask(block)) for block in blocks]
    pure = {}
    completion_controls = 0
    for total in sorted(holes):
        blocks = [block for block in six if vector_sum(block) == total]
        assert len(blocks) == 32
        for block in blocks:
            assert total not in block and not set(block) & holes
            assert all(dot(point, total) for point in block)
            enlarged = block + (127 ^ total,)
            assert all(dot(left, right) for left, right in combinations(enlarged, 2))
            completion_controls += 1
        pure[total] = [(block, mask(block)) for block in blocks]
    role_counts = Counter()
    source_reduction_controls = Counter()
    compatible_triples = Counter()
    charge_controls = 0
    for first_sum, first_charge, second_sum, second_charge in permutations(sorted(holes), 4):
        total = first_sum ^ second_sum
        characteristic = holes - {first_sum, first_charge, second_sum, second_charge}
        characteristic_class = (127,) + tuple(127 ^ point for point in sorted(characteristic))
        assert len(characteristic_class) == 4
        assert all(dot(left, right) for left, right in combinations(characteristic_class, 2))
        characteristic_charge = vector_sum(characteristic)
        assert total in holes and total not in (first_sum, second_sum)
        assert first_charge ^ second_charge ^ total == characteristic_charge
        assert not dot(first_charge, second_charge) and not dot(first_charge, total) and not dot(second_charge, total)
        charge_controls += 1
        if total in characteristic:
            branch = 'characteristic_class_to_size_three_two_six'
            reduced = tuple(point for point in characteristic_class if point != (127 ^ total))
            assert len(reduced) == 3 and all(dot(left, right) for left, right in combinations(reduced, 2))
            source_reduction_controls[branch] += 1
        else:
            branch = 'mixed_six_to_size_four_five_plus_six'
            source = (first_sum, first_charge) if total == first_charge else (second_sum, second_charge)
            assert total == source[1]
            for block, block_mask in catalogs[source]:
                reduced = block + (127 ^ source[0],)
                assert len(reduced) == 5 and all(dot(left, right) for left, right in combinations(reduced, 2))
                source_reduction_controls[branch] += 1
        role_counts[branch] += 1
        for left, left_mask in catalogs[(first_sum, first_charge)]:
            for right, right_mask in catalogs[(second_sum, second_charge)]:
                if left_mask & right_mask:
                    continue
                occupied = left_mask | right_mask
                for sextet, sextet_mask in pure[total]:
                    if occupied & sextet_mask:
                        continue
                    moved = 127 ^ total
                    before = set(characteristic_class) | set(left) | {127 ^ first_sum, 127 ^ first_charge} | set(right) | {127 ^ second_sum, 127 ^ second_charge} | set(sextet)
                    assert len(before) == 22 and moved in before
                    if total in characteristic:
                        reduced_source = set(characteristic_class) - {moved}
                        other = set(left) | {127 ^ first_sum, 127 ^ first_charge} | set(right) | {127 ^ second_sum, 127 ^ second_charge}
                    else:
                        source_first = total == first_charge
                        reduced_source = (set(left) | {127 ^ first_sum, 127 ^ first_charge} if source_first else set(right) | {127 ^ second_sum, 127 ^ second_charge}) - {moved}
                        other = set(characteristic_class) | (set(right) | {127 ^ second_sum, 127 ^ second_charge} if source_first else set(left) | {127 ^ first_sum, 127 ^ first_charge})
                    completed = set(sextet) | {moved}
                    assert len(completed) == 7 and not reduced_source & completed and not other & (reduced_source | completed)
                    assert reduced_source | completed | other == before
                    compatible_triples[branch] += 1
    assert role_counts == {'characteristic_class_to_size_three_two_six': 504,
                           'mixed_six_to_size_four_five_plus_six': 336}
    assert charge_controls == 840 and original_class_controls == 672 and completion_controls == 224
    inherited = {}
    bindings = (
        ('results/dimension-7-four-four-hole-cover.json', {
            'certificate_sha256': 'results/dimension-7-four-four-hole-cover-certificate.json',
            'auditor_sha256': 'develop/check_four_four_hole_cover.py',
            'builder_sha256': 'develop/build_four_four_hole_cover.py',
            'proof_note_sha256': 'notes/dimension-seven-four-four-hole-cover.md',
            'prior_two_six_report_sha256': 'results/dimension-7-two-six-profiles.json'}),
        ('results/dimension-7-four-even-pairs-check.json', {
            'certificate_sha256': 'results/dimension-7-four-even-pairs-proof.json',
            'checker_sha256': 'develop/check_dimension_seven_four_even_pairs.py',
            'builder_sha256': 'develop/build_dimension_seven_four_even_pairs.py',
            'proof_note_sha256': 'notes/dimension-seven-four-even-pairs.md'}))
    for report_name, identities in bindings:
        report = json.loads((root / report_name).read_text())
        for key, name in identities.items():
            assert report[key] == digest(root / name), name
        for name, checksum in report.get('dependency_sha256', {}).items():
            assert digest(root / name) == checksum, name
        inherited[report_name] = digest(root / report_name)
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'notes/dimension-seven-two-six-profiles.md', 'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-nineteen-obstruction.md', 'notes/dimension-seven-four-four-hole-cover.md',
                    'notes/dimension-seven-four-even-pairs.md', 'results/dimension-7-size-four.json',
                    'results/dimension-7-two-six-six-cover-check.json')
    return {'status': 'four_four_six_raw_profile_excluded_by_transferable_pure_six_sum_and_inherited_theorems',
            'dimension': 7, 'profile': [4, 4, 6, 7, 0, 8], 'characteristic_class_size': 4,
            'target_raw_profile_excluded': True, 'pure_six_sum_forced_in_M': True,
            'pure_six_sum_is_sum_of_mixed_defect_even_sums': True,
            'all_defects_avoid_even_holes': True,
            'written_exclusion_branches': dict(sorted(role_counts.items())),
            'fixed_M_ordered_odd_role_assignments': charge_controls,
            'original_mixed_six_class_controls': original_class_controls,
            'source_class_reduction_controls': dict(sorted(source_reduction_controls.items())),
            'pure_six_to_mixed_heptad_completion_controls': completion_controls,
            'compatible_disjoint_local_triple_recolorings': dict(sorted(compatible_triples.items())),
            'array_and_bitmask_catalogs_equal': True, 'inherited_theorem_report_sha256': inherited,
            'inherited_finite_certificate_and_source_hash_bindings_verified': True,
            'prior_finite_cover_inputs_retained': True, 'historical_cover_audits_rerun': False,
            'new_cover_search': False, 'new_finite_cover_certificate': False,
            **accounting(root), 'exact_n7': 'open_lower_bound19', 'nineteen_color_witness': False,
            'new_Lean': False, 'new_independent_Pro_review': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-four-six-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies},
            'scope': 'Written charge forces the pure-six sum into M; moving its odd vector reduces every hypothetical coloring to one of two previously excluded profiles. Finite local controls and inherited hash bindings checked, no new cover search or historical audit rerun. Exactly one three-six row removed;25/37 remain and exact n7 stays open >=19.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check()
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
