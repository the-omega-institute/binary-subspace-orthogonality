"""Bounded six-heptad cover search on the proved three-six orbit representatives."""
from pathlib import Path
import argparse
import hashlib
import json
import time


def dot(left, right):
    return (left & right).bit_count() % 2


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def array_cliques(candidates, size):
    blocks = []

    def visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        for index, point in enumerate(available):
            visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    visit((), candidates)
    return blocks


def build(max_states, max_visits, seconds):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    if min(max_states, max_visits, seconds) <= 0:
        raise ValueError('Search limits must be positive.')
    started = time.monotonic()
    root = Path(__file__).parents[1]
    source = root / 'results/dimension-7-three-six-roots.json'
    report = json.loads(source.read_text())
    representatives = [dict(case=form['case'], **record) for form in report['normal_forms'] for record in form['orbit_representatives']]
    assert len(representatives) == 1279
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    rows = sorted(mask(block) for block in array_cliques(points, 7) if len(set(block) & holes) == 1)
    assert len(rows) == 224
    by_point = {point: [row for row in rows if row & (1 << point)] for point in points}
    failed = {}
    visits = 0

    def solve(remaining):
        nonlocal visits
        visits += 1
        if len(failed) >= max_states or visits > max_visits or time.monotonic() - started > seconds:
            raise RuntimeError('Bounded three-six target exhausted; no exclusion certificate written.')
        if not remaining:
            return []
        if remaining in failed:
            return None
        pivot, options = min(((point, [row for row in by_point[point] if row & remaining == row])
                              for point in points if remaining & (1 << point)),
                             key=lambda item: (len(item[1]), item[0]))
        for row in options:
            answer = solve(remaining ^ row)
            if answer is not None:
                return [row] + answer
        failed[remaining] = pivot
        return None

    for record in representatives:
        answer = solve(int(record['remaining']))
        if answer is not None:
            return {'status': 'necessary_even_cover_found_pending_original_graph_extension',
                    'representative': record, 'cover': [str(row) for row in answer]}
    return {'status': 'all_three_six_orbit_representatives_failed_pending_independent_audit',
            'root_report_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'representatives': representatives,
            'failed_states': {str(state): pivot for state, pivot in sorted(failed.items())},
            'search_limits': {'max_states': max_states, 'max_visits': max_visits, 'seconds': seconds}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--max-states', type=int, default=20000)
    parser.add_argument('--max-visits', type=int, default=80000)
    parser.add_argument('--seconds', type=float, default=20)
    args = parser.parse_args()
    certificate = build(args.max_states, args.max_visits, args.seconds)
    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    print(json.dumps({'status': certificate['status'],
                      'failed_states': len(certificate.get('failed_states', {}))}, indent=2))
