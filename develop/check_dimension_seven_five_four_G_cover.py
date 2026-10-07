"""Independently audit a failed-state proof for every necessary G orbit."""
from collections import Counter
from itertools import combinations
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
    assert certificate['status'] == 'all_G_orbit_representatives_failed_pending_independent_audit'
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


def check(certificate_path=None):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    root = Path(__file__).parents[1]
    root_report_path = root / 'results/dimension-7-five-four-G-roots.json'
    root_report = json.loads(root_report_path.read_text())
    from check_dimension_seven_five_four_G_roots import check as reconstruct_roots
    fresh = reconstruct_roots()
    assert json.loads(json.dumps(fresh)) == root_report
    representatives = root_report['orbit_representatives']
    assert len(representatives) == 2306
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    heptads = bit_heptads(points)
    assert len(heptads) == 288
    assert all(all(dot(left, right) for left, right in combinations(block, 2)) for block in heptads)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    certificate_path = certificate_path or root / 'results/dimension-7-five-four-G-cover-proof.json'
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
    dependencies = ('notes/dimension-seven-five-four-charge.md',
                    'notes/dimension-seven-five-four-G-roots.md',
                    'develop/check_dimension_seven_five_four_G_roots.py',
                    'results/dimension-7-five-four-G-roots.json',
                    'notes/dimension-seven-nineteen-obstruction.md')
    return {
        'status': 'G_normal_form_excluded_by_written_stabilizer_reduction_and_audited_finite_cover_proof',
        'dimension': 7, 'profile': [5, 4, 6, 2, 8], 'newly_excluded_normal_form': 'G',
        'remaining_normal_forms_for_this_profile': ['Z'], 'target_raw_profile_excluded': False,
        'ordered_necessary_roots': 129280, 'distinct_necessary_root_sets': 127984,
        'pointwise_M_stabilizer_order': 64, 'orbit_representatives_checked': 2306,
        'all_actual_pure_five_holes_retained': [3, 15, 48, 51, 60, 63],
        'both_mixed_classes_retained': True, 'eligible_anchored_heptads': 224,
        **metadata, 'rejected_invalid_controls': rejected,
        'root_catalog_and_full_orbit_partition_reconstructed_and_matched': True,
        'prior_D_H_cover_certificates_used_as_G_proof_inputs': False,
        'prior_seven_heptad_certificates_used': False,
        'remaining_raw_profiles': {'five_six': 27, 'three_six': 39},
        'exact_n7': 'open_lower_bound19', 'nineteen_color_witness': False,
        'new_Lean': False, 'new_independent_Pro_review': False,
        'old_n6_formal_scope': 'three standard plus four native-evaluation axioms',
        'search_limits': certificate['search_limits'],
        'certificate_sha256': digest(certificate_path),
        'builder_sha256': digest(root / 'develop/build_dimension_seven_five_four_G_cover.py'),
        'checker_sha256': digest(Path(__file__)),
        'proof_note_sha256': digest(root / 'notes/dimension-seven-five-four-G-cover.md'),
        'dependency_sha256': {name: digest(root / name) for name in dependencies},
        'scope': 'Universal G exclusion from written marked normalization and proved orbit reduction, complete necessary roots, and new independently audited finite failed-state proof. Z and raw profile remain open; submitted manuscript preserved and extended working draft updated.'
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
