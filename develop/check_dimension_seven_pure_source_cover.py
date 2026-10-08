"""Independently audit complete pure-source covering failure and exact raw-row removal."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import json

from check_dimension_seven_five_four_charge import array_cliques, digest, dot, mask
from check_dimension_seven_pure_source_roots import check as reconstruct_roots


def audit_states(certificate, representatives, heptads, even, holes):
    assert certificate['status'] == 'all_sixteen_pure_source_representatives_failed_pending_independent_audit'
    assert certificate['representatives'] == representatives
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
    assert all(str(state) in certificate['failed_states'] for state in failed)
    children = {}
    sizes = Counter()
    branches = 0
    leaves = 0
    universe = set(even)
    for remaining, pivot in failed.items():
        points = {point for point in even if remaining & (1 << point)}
        assert remaining > 0 and mask(points) == remaining
        assert points <= universe and len(points) in (7, 14, 21)
        assert len(points & holes) == len(points) // 7
        assert type(pivot) is int and pivot in points
        successors = [mask(points - block) for block in heptads if pivot in block and block <= points]
        assert all(successor in failed and successor.bit_count() == len(points) - 7 for successor in successors)
        children[remaining] = successors
        branches += len(successors)
        leaves += not successors
        sizes[len(points)] += 1
    reached = set()
    frontier = [int(record['remaining']) for record in representatives]
    while frontier:
        remaining = frontier.pop()
        assert remaining in failed
        if remaining not in reached:
            reached.add(remaining)
            frontier.extend(children[remaining])
    assert reached == set(failed)
    return {'reachable_failed_states': len(failed), 'checked_branches': branches,
            'leaves_without_admissible_anchored_heptad': leaves,
            'state_size_histogram': dict(sorted(sizes.items()))}, children


def accounting(root, previous):
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 35}
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    target = [4, 6, 6, 5, 2, 8]
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
        assert len(prior) == (25 if prefix == 'five_six' else 35)
        assert len({tuple(row) for row in prior}) == len(prior) and all(tuple(row) in direct for row in prior)
        if prefix == 'three_six':
            assert prior.count(target) == 1
            current = [row for row in prior if row != target]
        else:
            current = prior
        remaining[prefix] = current
        distributions[prefix] = dict(sorted(Counter(row[-1] for row in current).items()))
    assert len(remaining['three_six']) == 34
    assert sum(count for distribution in distributions.values() for count in distribution.values()) == 59
    assert sum(distribution.get(5, 0) for distribution in distributions.values()) == 2
    assert all(row[-1] < 8 for rows in remaining.values() for row in rows)
    return {'newly_excluded_raw_profile': target, 'new_raw_profile_exclusions': 1,
            'remaining_raw_profiles': {name: len(rows) for name, rows in remaining.items()},
            'remaining_raw_profile_lists': remaining, 'remaining_counts_by_pure_odd_heptads': distributions,
            'total_excluded_raw_profiles': {'five_six': 21, 'three_six': 14},
            'remaining_three_six_C8_count': 0, 'remaining_size_four_C8_count': 0,
            'all_size_four_C8_count_candidates_excluded': True,
            'remaining_C6_through_C8_count': 57, 'remaining_C5_count': 2,
            'characteristic_sizes_still_open': [4, 5, 6, 7, 8]}


def check(certificate_path):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    roots_path = root / 'results/dimension-7-pure-source-roots.json'
    root_report_path = root / 'results/dimension-7-pure-source-roots-check.json'
    artifact = json.loads(roots_path.read_text())
    root_report = json.loads(root_report_path.read_text())
    fresh = reconstruct_roots(roots_path)
    assert json.loads(json.dumps(fresh)) == root_report
    assert fresh['all_sixteen_ordered_forms_complete'] and fresh['all_component_decompositions_retained']
    assert fresh['all_roles_and_actual_holes_transported']
    representatives = [{'functional_values': form['functional_values'], 'b': form['b'],
                        'root_index': orbit['representative'],
                        'remaining': form['roots'][orbit['representative']]['remaining']}
                       for form in artifact['forms'] for orbit in form['orbits']]
    assert len(representatives) == 1276
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    all_heptads = array_cliques(even, 7)
    assert len(all_heptads) == 288
    heptads = [frozenset(block) for block in all_heptads if len(set(block) & holes) == 1]
    assert len(heptads) == 224
    kernel_catalogs = {}
    for record in representatives:
        points = {point for point in even if int(record['remaining']) & (1 << point)}
        kernel = frozenset(points & holes)
        assert len(kernel) == 3 and all(first ^ second in kernel for first, second in combinations(kernel, 2))
        eligible = [block for block in heptads if block & kernel]
        assert len(eligible) == 96
        assert [block for block in heptads if block <= points] == [block for block in eligible if block <= points]
        kernel_catalogs[tuple(sorted(kernel))] = len(eligible)
    assert len(kernel_catalogs) == 4
    certificate = json.loads(certificate_path.read_text())
    assert certificate['root_artifact_sha256'] == digest(roots_path)
    assert 0 < certificate['visited_cover_states'] <= certificate['search_limits']['max_visits']
    assert len(certificate['failed_states']) <= certificate['search_limits']['max_states']
    audit, children = audit_states(certificate, representatives, heptads, even, holes)
    assert audit == {'reachable_failed_states':1276, 'checked_branches':0,
                     'leaves_without_admissible_anchored_heptad':1276, 'state_size_histogram':{21:1276}}
    negative_controls = []
    for kind in ('missing_representative', 'absent_pivot', 'false_empty_failure', 'false_leaf_on_coverable_state'):
        invalid = copy.deepcopy(certificate)
        expected_representatives = representatives
        if kind == 'missing_representative':
            invalid['representatives'].pop()
        elif kind == 'absent_pivot':
            first_state = next(iter(invalid['failed_states']))
            invalid['failed_states'][first_state] = next(point for point in even if not int(first_state) & (1 << point))
        elif kind == 'false_empty_failure':
            invalid['failed_states']['0'] = even[0]
        else:
            first, second = next((first, second) for first, second in combinations(heptads, 2) if not first & second)
            points = first | second
            control = {'remaining': str(mask(points))}
            expected_representatives = [control]
            invalid['representatives'] = expected_representatives
            invalid['failed_states'] = {control['remaining']: min(first)}
            assert len(points) == 14 and len(points & holes) == 2
        try:
            audit_states(invalid, expected_representatives, heptads, even, holes)
        except AssertionError:
            negative_controls.append(kind)
        else:
            raise AssertionError('Invalid certificate accepted: ' + kind)
    dependencies = ('develop/check_dimension_seven_pure_source_roots.py',
                    'develop/build_dimension_seven_pure_source_roots.py',
                    'notes/dimension-seven-pure-source-roots.md',
                    'results/dimension-7-pure-source-roots.json',
                    'results/dimension-7-pure-source-roots-check.json',
                    'develop/check_dimension_seven_five_four_charge.py',
                    'develop/check_dimension_seven_pure_source_normalization.py',
                    'notes/dimension-seven-pure-source-normalization.md',
                    'results/dimension-7-pure-source-normalization.json',
                    'develop/check_dimension_seven_four_six_six_pure_sources.py',
                    'notes/dimension-seven-four-six-six-pure-sources.md',
                    'results/dimension-7-four-six-six-pure-sources.json')
    return {'status': 'entire_four_six_six_raw_profile_excluded_by_complete_pure_source_cover_proof',
            'dimension':7, 'profile':[4,6,6,5,2,8], 'target_raw_profile_excluded':True,
            'entire_four_six_six_raw_profile_excluded':True, 'all_sixteen_ordered_pure_source_forms_excluded':True,
            'complete_joint_families':fresh['complete_joint_families'],
            'distinct_form_labelled_remaining_sets':fresh['distinct_form_labelled_remaining_sets'],
            'complete_remaining_set_orbits':fresh['complete_remaining_set_orbits'],
            'checked_orbit_representatives':len(representatives),
            'representatives_by_form':[{'functional_values':form['functional_values'], 'b':form['b'], 'orbits':len(form['orbits'])} for form in artifact['forms']],
            'all_even_heptads':288, 'anchored_heptads_checked':224, 'eligible_kernel_heptads_per_form':96,
            'normalized_kernel_catalogs':[{'nonzero_holes':kernel, 'eligible_heptads':count} for kernel,count in sorted(kernel_catalogs.items())],
            'proof_audit':audit, 'rejected_invalid_controls':negative_controls,
            'root_family_and_orbits_independently_reconstructed':True,
            'all_component_decompositions_and_actual_holes_retained':True,
            'remaining_set_decomposition_unique':False, 'free_group_action_assumed':False,
            'prior_finite_cover_inputs_retained_for_source_restrictions':True,
            'prior_cover_certificates_used_as_new_branch_failed_state_premises':False,
            'historical_cover_audits_rerun':False, 'prior_normalization_and_source_audits_rerun':False,
            'inherited_theorem_report_sha256':fresh['inherited_theorem_report_sha256'],
            'new_cover_search':True, 'new_independently_checked_cover_certificate':True,
            'search_limits':certificate['search_limits'], 'visited_cover_states':certificate['visited_cover_states'],
            **accounting(root,fresh), 'exact_n7':'open_lower_bound19', 'new_Lean':False, 'new_independent_Pro_review':False,
            'old_n6_formal_scope':'three standard plus four native-evaluation axioms',
            'certificate_sha256':digest(certificate_path),
            'builder_sha256':digest(root/'develop/build_dimension_seven_pure_source_cover.py'),
            'checker_sha256':digest(Path(__file__)), 'proof_note_sha256':digest(root/'notes/dimension-seven-pure-source-cover.md'),
            'dependency_sha256':{name:digest(root/name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    arguments = parser.parse_args()
    report = check(arguments.certificate)
    arguments.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='remaining_raw_profile_lists'},indent=2))
