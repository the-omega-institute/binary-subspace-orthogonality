"""Audit exhaustive pure completion sources and functional patterns for the remaining row."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

from check_dimension_seven_five_four_charge import array_cliques, bit_cliques, digest, dot, mask, vector_sum
from check_dimension_seven_four_five_five_charge import inherited_bindings
from check_dimension_seven_four_five_six_charge import cover_binding


def independent(points):
    return len(set(points)) == len(points) and all(dot(left, right) for left, right in combinations(points, 2))


def transfer_profile(source, recipient, second_source=None, second_recipient=None):
    classes = [(6, 4), (6, 6), (6, 6), (7, 6), (7, 6)] + [(7, 7)] * 5 + [(7, 0)] * 8
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
    saturated = Counter(evens for size, evens in classes if size == 7)
    assert set(saturated) <= {0, 6, 7}
    return tuple(evens for size, evens in defects) + (saturated[7], saturated[6], saturated[0])


def check():
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    catalogs = {size: bit_cliques(even, size) for size in (4, 6, 7)}
    assert all(catalogs[size] == array_cliques(even, size) for size in catalogs)
    pure = defaultdict(list)
    mixed = defaultdict(list)
    controls = Counter()
    for block in catalogs[6]:
        completion = vector_sum(block)
        assert completion not in block and independent(block + (completion,))
        assert [point for point in even if independent(block + (point,))] == [completion]
        pure[completion].append(block)
        controls['unique_pure_six_completions'] += 1
        if completion in holes:
            original = block + (127 ^ completion,)
            assert independent(original) and not set(block) & holes
            mixed[completion].append(original)
    four = {}
    for even_sum, charge in permutations(sorted(holes), 2):
        blocks = [block + (127 ^ even_sum, 127 ^ charge) for block in catalogs[4]
                  if vector_sum(block) == even_sum and all(dot(point, even_sum) and dot(point, charge) for point in block)]
        assert len(blocks) == 16 and all(independent(block) for block in blocks)
        four[(even_sum, charge)] = blocks
    markings = Counter()
    pairs = set()
    sources = set()
    for even_sum, charge, first_odd, second_odd in permutations(sorted(holes), 4):
        difference = even_sum ^ first_odd ^ second_odd
        for completion in even:
            other = completion ^ difference
            if not dot(completion, other):
                continue
            assert completion not in holes and other not in holes and completion != other
            basis = (even_sum, first_odd, second_odd)
            assert len({vector_sum(basis[index] for index in range(3) if bits & (1 << index)) for bits in range(8)}) == 8
            pattern = tuple(dot(completion, point) for point in basis)
            assert sum(pattern) % 2 == 1
            assert all(dot(completion, hole) == dot(other, hole) for hole in holes)
            characteristic = holes - {even_sum, charge, first_odd, second_odd}
            assert charge ^ completion ^ other == vector_sum(characteristic)
            assert dot(charge, completion) ^ dot(charge, other) ^ dot(completion, other) == 1
            markings[pattern] += 1
            pairs.add((completion, other))
            sources.update(('four_even_source', block, completion) for block in four[(even_sum, charge)] if completion in block)
            sources.update(('first_mixed_source', block, completion) for block in mixed[first_odd] if completion in block)
            sources.update(('second_mixed_source', block, completion) for block in mixed[second_odd] if completion in block)
            sources.update(('other_pure_six_source', block, completion) for block in pure[other]
                           if set(block) & holes and completion in block)
    assert markings == {(1, 0, 0): 5376, (0, 1, 0): 5376, (0, 0, 1): 5376, (1, 1, 1): 5376}
    assert len(pairs) == 224 and controls['unique_pure_six_completions'] == 2016
    profiles = {'four_even_source': (3, 6, 6, 2, 8), 'other_pure_six_source': (5, 4, 6, 2, 8),
                'first_mixed_source': (4, 5, 6, 6, 1, 8), 'second_mixed_source': (4, 5, 6, 6, 1, 8)}
    source_roles = {'four_even_source': 0, 'other_pure_six_source': 2,
                    'first_mixed_source': 3, 'second_mixed_source': 4}
    for name, block, completion in sorted(sources):
        reduced = tuple(point for point in block if point != completion)
        assert independent(block) and independent(reduced)
        assert set(reduced) | {completion} == set(block)
        assert transfer_profile(source_roles[name], 1) == profiles[name]
        controls[name] += 1
    assert transfer_profile(5, 1, 5, 2) == (5, 4, 6, 2, 8)
    assert transfer_profile(5, 1) == transfer_profile(5, 1, 6, 2) == (4, 6, 6, 5, 2, 8)
    anchored = [block for block in catalogs[7] if len(set(block) & holes) == 1]
    assert len(catalogs[7]) == 288 and len(anchored) == 224
    assert all(vector_sum(block) == 0 for block in anchored)
    local_counts = Counter()
    kernel_catalog_counts = Counter()
    for completion, other in sorted(pairs):
        targets = [block for block in pure[completion] if set(block) & holes]
        source_rows = [block for block in anchored if completion in block]
        assert len(targets) == len(source_rows) == 24
        targets_avoiding = [block for block in targets if other not in block]
        sources_avoiding = [block for block in source_rows if other not in block]
        assert len(targets_avoiding) == len(sources_avoiding) == 18
        local_counts[(len(targets), len(targets_avoiding), len(source_rows), len(sources_avoiding))] += 1
        for block in source_rows:
            if other in block:
                reduced = tuple(point for point in block if point not in (completion, other))
                assert independent(reduced) and len(reduced) == 5
                controls['common_source_two_removals'] += 1
        for block in sources_avoiding:
            reduced = tuple(point for point in block if point != completion)
            assert vector_sum(reduced) == completion and independent(reduced + (completion,))
            assert set(reduced) & holes == set(block) & holes
            assert all(dot(hole, completion) for hole in set(reduced) & holes)
            controls['pure_source_removals_retain_actual_holes'] += 1
        for block in targets_avoiding:
            assert vector_sum(block + (completion,)) == 0
            assert set(block + (completion,)) & holes == set(block) & holes
            controls['pure_target_completions_retain_actual_holes'] += 1
        other_sources = [block for block in anchored if other in block and completion not in block]
        other_targets = [block for block in pure[other] if set(block) & holes and completion not in block]
        for name, first_rows, second_rows in (('disjoint_pure_source_pairs', sources_avoiding, other_sources),
                                             ('disjoint_pure_target_pairs', targets_avoiding, other_targets)):
            count = 0
            for first in first_rows:
                for second in second_rows:
                    if not mask(first) & mask(second):
                        first_hole, = set(first) & holes
                        second_hole, = set(second) & holes
                        assert first_hole != second_hole
                        assert dot(first_hole, completion) == dot(second_hole, completion) == 1
                        count += 1
            assert count == 216
            controls[name] += count
        positive = {hole for hole in holes if dot(hole, completion)}
        kernel = holes - positive
        assert len(positive) == 4 and len(kernel) == 3
        assert vector_sum(kernel) == 0
        assert all(first ^ second in kernel for first, second in combinations(kernel, 2))
        kernel_rows = [block for block in anchored if set(block) & kernel]
        assert len(kernel_rows) == 96
        kernel_catalog_counts[tuple(sorted(kernel))] += 1
        for actual in permutations(sorted(positive), 4):
            assert holes - set(actual) == kernel
            controls['four_distinct_positive_holes_leave_kernel'] += 1
    assert local_counts == {(24, 18, 24, 18): 224}
    assert len(kernel_catalog_counts) == 7 and set(kernel_catalog_counts.values()) == {32}
    previous_name = 'results/dimension-7-four-five-six-cover-check.json'
    previous = json.loads((root / previous_name).read_text())
    assert previous['target_raw_profile_excluded'] and previous['all_twelve_completion_source_branches_excluded']
    inherited = inherited_bindings(root)
    inherited.update(cover_binding(root, stem) for stem in ('three-six-cover', 'four-six-six-cover', 'four-five-six-cover'))
    assert len(inherited) == 10
    assert {name: checksum for name, checksum in inherited.items() if name != previous_name} == previous['inherited_theorem_report_sha256']
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 35}
    assert [4, 6, 6, 5, 2, 8] in previous['remaining_raw_profile_lists']['three_six']
    dependencies = ('develop/check_dimension_seven_five_four_charge.py',
                    'develop/check_dimension_seven_four_five_six_charge.py',
                    'notes/dimension-seven-size-four.md', 'notes/dimension-seven-two-six-profiles.md')
    return {'status': 'both_pure_six_completions_forced_into_distinct_pure_heptads_with_kernel_holes',
            'dimension': 7, 'profile': [4, 6, 6, 5, 2, 8],
            'written_exhaustive_source_reduction': True, 'both_completion_sources_pure': True,
            'completion_source_heptads_distinct': True, 'source_heptads_avoid_other_completion': True,
            'four_actual_holes_are_all_functional_one_points': True, 'remaining_holes_are_nonzero_kernel_plane': True,
            'ordered_functional_patterns': [{'values': pattern, 'markings': count} for pattern, count in sorted(markings.items())],
            'fixed_M_ordered_markings': sum(markings.values()), 'distinct_ordered_completion_pairs': len(pairs),
            'local_controls': dict(sorted(controls.items())),
            'per_pair_target_and_source_catalog_sizes': [24, 18, 24, 18],
            'kernel_plane_pair_counts': [{'nonzero_points': kernel, 'completion_pairs': count} for kernel, count in sorted(kernel_catalog_counts.items())],
            'necessary_remaining_points': 21, 'necessary_remaining_holes': 3, 'residual_pure_heptads_required': 3,
            'eligible_kernel_anchored_heptads': 96,
            'single_and_double_pure_source_recolorings_preserve_profile': True,
            'pure_source_recolorings_are_not_assumed_isometries': True,
            'local_controls_are_modular_not_complete_joint_roots': True,
            'target_raw_profile_excluded': False, 'new_raw_profile_exclusions': 0,
            'remaining_raw_profiles': previous['remaining_raw_profiles'], 'remaining_raw_profile_lists': previous['remaining_raw_profile_lists'],
            'remaining_three_six_C8_count': 1, 'remaining_C6_through_C8_count': 58, 'remaining_C5_count': 2,
            'inherited_theorem_report_sha256': inherited, 'historical_cover_audits_rerun': False,
            'previous_source_or_root_audits_rerun': False, 'complete_joint_roots_constructed': False,
            'new_cover_search': False, 'new_cover_certificate': False, 'new_Lean': False, 'new_independent_Pro_review': False,
            'exact_n7': 'open_lower_bound19', 'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'checker_sha256': digest(Path(__file__)),
            'proof_note_sha256': digest(root / 'notes/dimension-seven-four-six-six-pure-sources.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check()
    arguments.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'remaining_raw_profile_lists'}, indent=2))
