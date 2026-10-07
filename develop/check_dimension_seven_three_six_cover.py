"""Independently audit a failed-state proof for every necessary three-six orbit."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import hashlib
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit_heptads(points):
    neighbors = {point: mask(other for other in points if other > point and dot(point, other))
                 for point in points}
    blocks = []

    def visit(chosen, available):
        if len(chosen) == 7:
            blocks.append(chosen)
            return
        while available:
            first_bit = available & -available
            point = first_bit.bit_length() - 1
            available ^= first_bit
            visit(chosen + (point,), available & neighbors[point])

    visit((), mask(points))
    return blocks


def audit_states(certificate, representatives, rows, points, holes):
    assert certificate['status'] == 'all_three_six_orbit_representatives_failed_pending_independent_audit'
    assert certificate['representatives'] == representatives
    failed = {int(state): pivot for state, pivot in certificate['failed_states'].items()}
    assert len(failed) == len(certificate['failed_states'])
    assert all(str(state) in certificate['failed_states'] for state in failed)
    universe = mask(points)
    children = {}
    branches = 0
    leaves = 0
    sizes = Counter()
    for remaining, pivot in failed.items():
        assert remaining > 0 and remaining & universe == remaining
        assert remaining.bit_count() % 7 == 0 and remaining.bit_count() <= 42
        assert (remaining & mask(holes)).bit_count() == remaining.bit_count() // 7
        assert type(pivot) is int and pivot in points and remaining & (1 << pivot)
        successors = [remaining ^ row for row in rows if row & (1 << pivot) and row & remaining == row]
        assert all(successor in failed and successor.bit_count() == remaining.bit_count() - 7
                   for successor in successors)
        children[remaining] = successors
        branches += len(successors)
        leaves += not successors
        sizes[remaining.bit_count()] += 1
    frontier = [int(record['remaining']) for record in representatives]
    reached = set()
    while frontier:
        remaining = frontier.pop()
        assert remaining in failed
        if remaining not in reached:
            reached.add(remaining)
            frontier.extend(children[remaining])
    assert reached == set(failed)
    return {'reachable_failed_states': len(failed), 'checked_branches': branches,
            'leaves_without_any_admissible_heptad': leaves, 'state_size_histogram': dict(sorted(sizes.items()))}



def profile_accounting(root):
    raw = json.loads((root / 'results/dimension-7-size-four.json').read_text())
    previous = json.loads((root / 'results/dimension-7-five-four-Z-cover-check.json').read_text())
    assert previous['remaining_raw_profiles'] == {'five_six': 26, 'three_six': 39}
    target = [3, 6, 6, 2, 8]
    remaining = {}
    distributions = {}
    for name, sizes, prefix in (('5+6', (5, 6), 'five_six'), ('6+6+6', (6, 6, 6), 'three_six')):
        domains = [range(size + 1) if size != 6 else (0, 2, 4, 5, 6) for size in sizes]
        direct = set()
        for even in product(*domains):
            if name == '6+6+6' and tuple(sorted(even)) != even:
                continue
            for first in range(19):
                for mixed in range(19):
                    odd = 18 - len(sizes) - first - mixed
                    if odd >= 0 and 7 * first + 6 * mixed + sum(even) == 63 and mixed + 7 * odd + sum(sizes) - sum(even) + 4 == 64:
                        direct.add(even + (first, mixed, odd))
        archived = {tuple(row['defect_even_counts'] + row['saturated_counts']) for row in raw['count_profiles'][name]}
        assert direct == archived and len(direct) == (46 if prefix == 'five_six' else 48)
        prior = previous['remaining_raw_profile_lists'][prefix]
        assert len(prior) == (26 if prefix == 'five_six' else 39)
        assert len({tuple(row) for row in prior}) == len(prior)
        assert all(tuple(row) in direct for row in prior)
        assert previous['total_excluded_profiles'][prefix] == (20 if prefix == 'five_six' else 9)
        if prefix == 'five_six':
            assert prior.count(target) == 1
            current = [row for row in prior if row != target]
        else:
            current = prior
        remaining[prefix] = current
        distributions[prefix] = dict(sorted(Counter(row[-1] for row in current).items()))
    assert distributions == {'five_six': {6: 6, 7: 19}, 'three_six': {5: 2, 6: 14, 7: 18, 8: 5}}
    return {'newly_excluded_raw_profile': target, 'new_raw_profile_exclusions': 1,
            'remaining_raw_profiles': {prefix: len(rows) for prefix, rows in remaining.items()},
            'remaining_raw_profile_lists': remaining, 'remaining_counts_by_pure_odd_heptads': distributions,
            'total_excluded_profiles': {'five_six': 21, 'three_six': 9},
            'remaining_C6_through_C8_count': 62, 'remaining_C5_count': 2,
            'prior_cover_certificates_used_as_new_finite_proof_inputs': False,
            'prior_cover_audits_rerun': False, 'all_nineteen_color_branches_excluded': False,
            'characteristic_sizes_still_open': [4, 5, 6, 7, 8]}

def check(certificate_path=None):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    root_report_path = root / 'results/dimension-7-three-six-roots.json'
    root_report = json.loads(root_report_path.read_text())
    from check_dimension_seven_three_six_roots import check as reconstruct_roots
    fresh = reconstruct_roots()
    assert json.loads(json.dumps(fresh)) == root_report
    representatives = [dict(case=form['case'], **record) for form in root_report['normal_forms'] for record in form['orbit_representatives']]
    assert len(representatives) == 1279
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    heptads = bit_heptads(points)
    assert len(heptads) == 288
    assert all(all(dot(left, right) for left, right in combinations(block, 2)) for block in heptads)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    certificate_path = certificate_path or root / 'results/dimension-7-three-six-cover-proof.json'
    certificate = json.loads(certificate_path.read_text())
    assert set(certificate) == {'status', 'root_report_sha256', 'representatives', 'failed_states', 'search_limits'}
    assert certificate['root_report_sha256'] == digest(root_report_path)
    metadata = audit_states(certificate, representatives, rows, points, holes)
    invalid_controls = []
    missing_root = copy.deepcopy(certificate)
    del missing_root['failed_states'][representatives[0]['remaining']]
    invalid_controls.append(('missing_required_representative', missing_root))
    absent_pivot = copy.deepcopy(certificate)
    absent_pivot['failed_states'][representatives[0]['remaining']] = 127
    invalid_controls.append(('pivot_not_in_even_remaining_set', absent_pivot))
    empty_state = copy.deepcopy(certificate)
    empty_state['failed_states']['0'] = 3
    invalid_controls.append(('empty_set_falsely_marked_failed', empty_state))
    rejected = []
    for name, invalid in invalid_controls:
        try:
            audit_states(invalid, representatives, rows, points, holes)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Invalid failed-state control accepted: ' + name)
    dependencies = ('notes/dimension-seven-three-six-charge.md',
                    'notes/dimension-seven-three-six-roots.md',
                    'develop/check_dimension_seven_three_six_roots.py',
                    'develop/check_dimension_seven_three_six_charge.py',
                    'develop/check_dimension_seven_five_four_charge.py',
                    'results/dimension-7-three-six-roots.json',
                    'results/dimension-7-three-six-charge.json',
                    'results/dimension-7-size-four.json',
                    'results/dimension-7-five-four-Z-cover-check.json')
    return {
        'status': 'three_six_raw_profile_excluded_by_written_marked_reduction_and_audited_finite_cover_proof',
        'dimension': 7, 'profile': [3, 6, 6, 2, 8], 'characteristic_class_size': 4,
        'newly_excluded_normal_forms': ['I', 'II', 'III'],
        'remaining_normal_forms_for_this_profile': [], 'target_raw_profile_excluded': True,
        'ordered_necessary_roots_by_form': [7424, 12688, 8160],
        'distinct_necessary_root_sets_by_form': [7408, 12688, 8112],
        'full_marked_stabilizer_orders': [32, 32, 16],
        'orbit_representatives_checked_by_form': [248, 474, 557],
        'all_actual_pure_six_holes_and_both_hole_orbits_retained': True,
        'both_mixed_classes_retained': True, 'eligible_anchored_heptads': 224,
        **metadata, 'rejected_invalid_controls': rejected,
        'root_catalogs_and_complete_orbit_partitions_reconstructed_and_matched': True,
        **profile_accounting(root),
        'exact_n7': 'open_lower_bound19', 'nineteen_color_witness': False,
        'new_Lean': False, 'new_independent_Pro_review': False,
        'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
        'search_limits': certificate['search_limits'],
        'certificate_sha256': digest(certificate_path),
        'builder_sha256': digest(root / 'develop/build_dimension_seven_three_six_cover.py'),
        'checker_sha256': digest(Path(__file__)),
        'proof_note_sha256': digest(root / 'notes/dimension-seven-three-six-cover.md'),
        'dependency_sha256': {name: digest(root / name) for name in dependencies},
        'scope': 'All three marked forms excluded using complete necessary roots, proved marked orbit reductions and a new independently audited failed-state proof. Exactly the specified raw row is removed; 25/39 count candidates, characteristic sizes 4..8 and exact n7 remain open.'
    }



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.certificate)
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')
