"""Independently audit the transferred two-hole cover proof and exact source-row removal."""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import copy
import json

from check_dimension_seven_five_four_charge import array_cliques, digest, dot, mask
from check_dimension_seven_four_five_five_charge import inherited_bindings


def audit_states(certificate, representatives, rows, even, holes):
    assert certificate['status'] == 'all_transferred_two_hole_representatives_failed_pending_independent_audit'
    assert certificate['representatives'] == representatives
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
    assert all(str(state) in certificate['failed_states'] for state in failed)
    universe = mask(even)
    children = {}
    sizes = Counter()
    branches = 0
    leaves = 0
    for remaining, pivot in failed.items():
        assert remaining > 0 and remaining & universe == remaining
        assert remaining.bit_count() in (7, 14, 21, 28, 35)
        assert (remaining & mask(holes)).bit_count() == remaining.bit_count() // 7
        assert type(pivot) is int and pivot in even and remaining & (1 << pivot)
        successors = [remaining ^ row for row in rows if row & (1 << pivot) and row & remaining == row]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7
                   for successor in successors)
        children[remaining] = successors
        branches += len(successors)
        leaves += not successors
        sizes[remaining.bit_count()] += 1
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
    assert previous['remaining_raw_profiles'] == {'five_six': 25, 'three_six': 37}
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    target = [4, 5, 5, 7, 0, 8]
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
        assert len(prior) == (25 if prefix == 'five_six' else 37)
        assert len({tuple(row) for row in prior}) == len(prior) and all(tuple(row) in direct for row in prior)
        if prefix == 'three_six':
            assert prior.count(target) == 1
            current = [row for row in prior if row != target]
        else:
            current = prior
        remaining[prefix] = current
        distributions[prefix] = dict(sorted(Counter(row[-1] for row in current).items()))
    assert len(remaining['three_six']) == 36
    assert [4, 6, 6, 5, 2, 8] in remaining['three_six'] and [4, 5, 6, 6, 1, 8] in remaining['three_six']
    assert sum(count for distribution in distributions.values() for count in distribution.values()) == 61
    assert sum(distribution.get(5, 0) for distribution in distributions.values()) == 2
    return {'newly_excluded_raw_profile': target, 'new_raw_profile_exclusions': 1,
            'remaining_raw_profiles': {name: len(rows) for name, rows in remaining.items()},
            'remaining_raw_profile_lists': remaining, 'remaining_counts_by_pure_odd_heptads': distributions,
            'total_excluded_raw_profiles': {'five_six': 21, 'three_six': 12},
            'remaining_three_six_C8_count': 2, 'remaining_C6_through_C8_count': 59,
            'remaining_C5_count': 2, 'characteristic_sizes_still_open': [4, 5, 6, 7, 8]}


def check(certificate_path=None):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    roots_path = root / 'results/dimension-7-four-six-six-roots.json'
    root_report_path = root / 'results/dimension-7-four-six-six-roots-check.json'
    artifact = json.loads(roots_path.read_text())
    root_report = json.loads(root_report_path.read_text())
    from check_dimension_seven_four_six_six_roots import check as reconstruct_roots
    fresh = reconstruct_roots()
    assert json.loads(json.dumps(fresh)) == root_report
    representatives = [{'b': form['b'], 'root_index': orbit['representative'],
                        'remaining': form['roots'][orbit['representative']]['remaining'],
                        'actual_holes': form['roots'][orbit['representative']]['actual_holes']}
                       for form in artifact['forms'] for orbit in form['orbits']]
    assert Counter(record['b'] for record in representatives) == {3: 224, 15: 112, 63: 21}
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    heptads = array_cliques(even, 7)
    assert len(heptads) == 288
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    source = certificate_path or root / 'results/dimension-7-four-six-six-cover-proof.json'
    certificate = json.loads(source.read_text())
    assert certificate['root_artifact_sha256'] == digest(roots_path)
    audit, children = audit_states(certificate, representatives, rows, even, holes)
    negative_controls = []
    for kind in ('missing_representative', 'absent_pivot', 'false_empty_failure', 'omitted_required_successor'):
        invalid = copy.deepcopy(certificate)
        if kind == 'missing_representative':
            invalid['representatives'].pop()
        elif kind == 'absent_pivot':
            first_state = next(iter(invalid['failed_states']))
            invalid['failed_states'][first_state] = next(point for point in even if not int(first_state) & (1 << point))
        elif kind == 'false_empty_failure':
            invalid['failed_states']['0'] = even[0]
        else:
            successor = next(successor for successors in children.values() for successor in successors)
            del invalid['failed_states'][str(successor)]
        try:
            audit_states(invalid, representatives, rows, even, holes)
        except AssertionError:
            negative_controls.append(kind)
        else:
            raise AssertionError('Invalid certificate accepted: ' + kind)
    inherited = inherited_bindings(root)
    assert inherited == root_report['inherited_theorem_report_sha256']
    recoloring_path = root / 'results/dimension-7-four-five-five-charge.json'
    recoloring = json.loads(recoloring_path.read_text())
    assert recoloring['written_recoloring_reduction'] and recoloring['resulting_profile'] == [4, 6, 6, 5, 2, 8]
    assert recoloring['resulting_actual_holes_distinct'] and recoloring['resulting_actual_defect_holes'] == [1, 1]
    assert recoloring['prior_finite_cover_inputs_retained'] and recoloring['inherited_theorem_report_sha256'] == inherited
    dependencies = ('develop/check_dimension_seven_four_six_six_roots.py',
                    'develop/build_dimension_seven_four_six_six_roots.py',
                    'notes/dimension-seven-four-six-six-roots.md', 'results/dimension-7-four-six-six-roots.json',
                    'results/dimension-7-four-six-six-roots-check.json',
                    'develop/check_dimension_seven_four_five_five_charge.py',
                    'notes/dimension-seven-four-five-five-charge.md', 'results/dimension-7-four-five-five-charge.json')
    return {'status': 'transferred_two_hole_branch_excluded_and_source_four_five_five_row_excluded',
            'dimension': 7, 'transferred_profile': [4, 6, 6, 5, 2, 8],
            'source_profile': [4, 5, 5, 7, 0, 8],
            'transferred_two_hole_subbranch_excluded': True, 'source_raw_profile_excluded': True,
            'entire_four_six_six_raw_profile_excluded': False,
            'complete_joint_families': [1708, 1648, 304], 'complete_remaining_set_orbits': [224, 112, 21],
            'checked_orbit_representatives': len(representatives), 'all_even_heptads': 288,
            'anchored_heptads_used': 224, 'proof_audit': audit,
            'rejected_invalid_controls': negative_controls,
            'root_family_and_orbits_independently_reconstructed': True,
            'root_decomposition_roles_and_actual_holes_retained': True,
            'prior_finite_cover_inputs_used_for_source_profile_transfer': True,
            'prior_cover_certificates_used_as_new_subbranch_finite_proof_inputs': False,
            'historical_cover_audits_rerun': False, 'prior_normalization_and_recoloring_audits_rerun': False,
            'inherited_theorem_report_sha256': inherited,
            'new_cover_search': True, 'new_independently_checked_cover_certificate': True,
            **accounting(root, root_report), 'exact_n7': 'open_lower_bound19',
            'new_Lean': False, 'new_independent_Pro_review': False,
            'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
            'certificate_sha256': digest(source), 'builder_sha256': digest(root / 'develop/build_dimension_seven_four_six_six_cover.py'),
            'checker_sha256': digest(Path(__file__)), 'proof_note_sha256': digest(root / 'notes/dimension-seven-four-six-six-cover.md'),
            'dependency_sha256': {name: digest(root / name) for name in dependencies}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.certificate)
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')
