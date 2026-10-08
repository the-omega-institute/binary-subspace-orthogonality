"""Audit completion sources for (4,5,6;6,1,8), without a cover search."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, vector_sum
from check_dimension_seven_four_five_five_charge import inherited_bindings


def independent(points):
    return len(set(points)) == len(points) and all(dot(left, right) for left, right in combinations(points, 2))


def transfer_profile(source, recipient, second_source=None, second_recipient=None):
    classes = [(6, 4), (6, 5), (6, 6), (7, 6)] + [(7, 7)] * 6 + [(7, 0)] * 8
    for origin, target in ((source, recipient), (second_source, second_recipient)):
        if origin is None:
            continue
        size, evens = classes[origin]
        classes[origin] = (size - 1, evens - 1)
        size, evens = classes[target]
        classes[target] = (size + 1, evens + 1)
    assert sum(size for size, evens in classes) == 123
    assert sum(evens for size, evens in classes) == 63
    defects = sorted((size, evens) for size, evens in classes if size < 7)
    counts = Counter(evens for size, evens in classes if size == 7)
    assert set(counts) <= {0, 6, 7}
    return tuple(evens for size, evens in defects) + (counts[7], counts[6], counts[0])


def cover_binding(root, stem):
    name = 'results/dimension-7-' + stem + '-check.json'
    report = json.loads((root / name).read_text())
    source_stem = stem.replace('-', '_')
    paths = {'certificate_sha256': 'results/dimension-7-' + stem + '-proof.json',
             'builder_sha256': 'develop/build_dimension_seven_' + source_stem + '.py',
             'checker_sha256': 'develop/check_dimension_seven_' + source_stem + '.py',
             'proof_note_sha256': 'notes/dimension-seven-' + stem + '.md'}
    for key, path in paths.items():
        assert report[key] == digest(root / path), path
    for path, checksum in report.get('dependency_sha256', {}).items():
        assert digest(root / path) == checksum, path
    for path, checksum in report.get('inherited_theorem_report_sha256', {}).items():
        assert digest(root / path) == checksum, path
    return name, digest(root / name)


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    catalogs = {size: bit_cliques(even, size) for size in (4, 5, 6, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    assert len(catalogs[7]) == 288
    pure = defaultdict(list)
    mixed = defaultdict(list)
    five = defaultdict(list)
    four = {}
    controls = Counter()
    for block in catalogs[6]:
        completion = vector_sum(block)
        assert completion not in block and independent(block + (completion,))
        assert [point for point in even if independent(block + (point,))] == [completion]
        pure[completion].append(block)
        controls['unique_pure_six_completion'] += 1
        if completion in holes:
            assert not set(block) & holes
            assert independent(block + (127 ^ completion,))
            mixed[completion].append(block)
    for odd_projection in sorted(holes):
        for block in catalogs[5]:
            if not all(dot(point, odd_projection) for point in block):
                continue
            completion = vector_sum(block) ^ odd_projection
            original = block + (127 ^ odd_projection,)
            assert completion not in holes and not set(block) & holes
            assert independent(original) and independent(original + (completion,))
            assert [point for point in even if independent(original + (point,))] == [completion]
            five[(odd_projection, completion)].append(block)
            controls['unique_five_even_mixed_completion'] += 1
    assert controls['unique_pure_six_completion'] == 2016
    assert controls['unique_five_even_mixed_completion'] == 1344
    assert all(len(blocks) == 32 for blocks in pure.values())
    assert all(len(blocks) == 6 for blocks in five.values())
    assert all(len(blocks) == 32 for blocks in mixed.values())
    for even_sum, charge in permutations(sorted(holes), 2):
        blocks = [block for block in catalogs[4] if vector_sum(block) == even_sum
                  and all(dot(point, even_sum) and dot(point, charge) for point in block)]
        assert len(blocks) == 16
        assert all(independent(block + (127 ^ even_sum, 127 ^ charge)) for block in blocks)
        four[(even_sum, charge)] = blocks
    anchored = [block for block in catalogs[7] if set(block) & holes]
    assert len(anchored) == 224
    assert all(vector_sum(block) == 0 and len(set(block) & holes) == 1 for block in anchored)
    markings = Counter()
    pairs = set()
    sources = set()
    for even_sum, charge, odd_projection, mixed_odd in permutations(sorted(holes), 4):
        for completion in even:
            if not dot(completion, odd_projection) or dot(completion, even_sum) != dot(completion, mixed_odd):
                continue
            pure_completion = completion ^ even_sum ^ odd_projection ^ mixed_odd
            if not dot(completion, pure_completion):
                continue
            functional_value = dot(completion, even_sum)
            assert completion not in holes and pure_completion not in holes
            assert completion != pure_completion
            assert len({even_sum, odd_projection, mixed_odd, even_sum ^ odd_projection,
                        even_sum ^ mixed_odd, odd_projection ^ mixed_odd,
                        even_sum ^ odd_projection ^ mixed_odd}) == 7
            characteristic_charge = vector_sum(holes - {even_sum, charge, odd_projection, mixed_odd})
            assert charge ^ completion ^ pure_completion == characteristic_charge
            assert all(dot(completion, hole) == dot(pure_completion, hole) for hole in holes)
            assert dot(charge, completion) ^ dot(charge, pure_completion) ^ dot(completion, pure_completion) == 1
            markings[functional_value] += 1
            pairs.add((completion, pure_completion))
            sources.update(('q_D0', block, pure_completion) for block in four[(even_sum, charge)] if pure_completion in block)
            sources.update(('q_D1', block + (127 ^ odd_projection,), pure_completion)
                           for block in five[(odd_projection, completion)] if pure_completion in block)
            sources.update(('q_J', block + (127 ^ mixed_odd,), pure_completion)
                           for block in mixed[mixed_odd] if pure_completion in block)
            sources.update(('t_D0', block, completion) for block in four[(even_sum, charge)] if completion in block)
            sources.update(('t_P', block, completion) for block in pure[pure_completion]
                           if set(block) & holes and completion in block)
            sources.update(('t_J', block + (127 ^ mixed_odd,), completion)
                           for block in mixed[mixed_odd] if completion in block)
            if not functional_value:
                assert all(completion not in block and pure_completion not in block for block in mixed[mixed_odd])
    assert markings == {0: 5376, 1: 5376}
    source_profiles = {'q_D0': (3, 5, 7, 1, 8), 'q_D1': (4, 4, 7, 1, 8),
                       'q_J': (4, 5, 5, 7, 0, 8), 't_D0': (3, 6, 6, 2, 8),
                       't_P': (5, 4, 6, 2, 8), 't_J': (4, 5, 6, 6, 1, 8)}
    source_roles = {'q_D0': (0, 2), 'q_D1': (1, 2), 'q_J': (3, 2),
                    't_D0': (0, 1), 't_P': (2, 1), 't_J': (3, 1)}
    for name, block, completion in sorted(sources):
        reduced = tuple(point for point in block if point != completion)
        assert independent(block) and independent(reduced)
        assert set(reduced) | {completion} == set(block)
        assert transfer_profile(*source_roles[name]) == source_profiles[name]
        if name == 't_J':
            mixed_odd = vector_sum(point for point in block if not dot(point, 127))
            odd_member, = (point for point in block if dot(point, 127))
            assert odd_member == 127 ^ mixed_odd and dot(completion, mixed_odd)
            assert vector_sum(point for point in reduced if not dot(point, 127)) ^ mixed_odd == completion
            assert independent(reduced + (completion,))
        controls[name] += 1
    local_sizes = Counter()
    for completion, pure_completion in sorted(pairs):
        pure_rows = [block for block in pure[pure_completion] if set(block) & holes]
        source_rows = [block for block in anchored if pure_completion in block]
        assert len(pure_rows) == len(source_rows) == 24
        pure_rows_avoiding = [block for block in pure_rows if completion not in block]
        source_rows_avoiding = [block for block in source_rows if completion not in block]
        assert len(pure_rows_avoiding) == len(source_rows_avoiding) == 18
        for block in source_rows:
            reduced = tuple(point for point in block if point != pure_completion)
            assert vector_sum(reduced) == pure_completion and reduced in pure_rows
            hole, = set(reduced) & holes
            assert dot(hole, pure_completion)
            if completion in block:
                twice_reduced = tuple(point for point in reduced if point != completion)
                assert len(twice_reduced) == 5 and independent(twice_reduced)
                assert transfer_profile(4, 1, 4, 2) == (5, 4, 6, 2, 8)
                controls['common_pure_source_two_removals'] += 1
            else:
                controls['q_pure_source_retains_actual_hole'] += 1
        local_sizes[(len(pure_rows), len(pure_rows_avoiding), len(source_rows), len(source_rows_avoiding))] += 1
    assert len(pairs) == 224 and local_sizes == {(24, 18, 24, 18): 224}
    assert transfer_profile(4, 1) == (4, 6, 6, 5, 2, 8)
    assert transfer_profile(4, 2) == (4, 5, 6, 6, 1, 8)
    identities = inherited_bindings(root)
    identities.update(cover_binding(root, stem) for stem in ('three-six-cover', 'four-six-six-cover'))
    previous = json.loads((root / 'results/dimension-7-four-six-six-cover-check.json').read_text())
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 36}
    assert [4, 5, 6, 6, 1, 8] in previous['remaining_raw_profile_lists']['three_six']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'develop/check_dimension_seven_four_five_five_charge.py',
                    'notes/dimension-seven-two-six-profiles.md', 'notes/dimension-seven-size-four.md',
                    'notes/dimension-seven-nineteen-obstruction.md')
    return {'status': 'written_completion_source_constraints_with_modular_local_controls',
            'dimension': 7, 'profile': [4, 5, 6, 6, 1, 8], 'target_raw_profile_excluded': False,
            'q_forced_into_pure_even_heptad_avoiding_t': True,
            't_source_alternatives': ['existing_mixed_heptad_if_eta1', 'distinct_pure_even_heptad'],
            'eta0_forces_t_pure_source': True, 't_pure_transfer_profile': [4, 6, 6, 5, 2, 8],
            't_pure_transfer_has_completion_locations': ['paired_mixed', 'distinct_pure_even_heptad'],
            'previous_paired_mixed_mixed_subbranch_certificate_applies': False,
            'fixed_M_ordered_markings': sum(markings.values()),
            'markings_by_eta': dict(sorted(markings.items())),
            'distinct_ordered_completion_pairs': len(pairs), 'local_controls': dict(sorted(controls.items())),
            'per_pair_pure_six_and_q_source_catalog_sizes': [24, 18, 24, 18],
            'source_controls_are_modular_not_joint_roots': True,
            'source_transfer_profiles': source_profiles,
            'new_raw_profile_exclusions': 0,
            'remaining_raw_profiles': previous['remaining_raw_profiles'],
            'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 2, 'remaining_C6_through_C8_count': 59, 'remaining_C5_count': 2,
            'inherited_theorem_report_sha256': identities,
            'historical_cover_audits_rerun': False, 'new_cover_search': False,
            'new_cover_certificate': False, 'new_Lean': False, 'new_independent_Pro_review': False,
            'exact_n7': 'open_lower_bound19',
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-five-six-charge.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check()
    arguments.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'remaining_raw_profile_lists'}, indent=2))
