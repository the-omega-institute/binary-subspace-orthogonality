"""Bounded anchored-heptad cover test on all twelve completion-source branches."""
from pathlib import Path
import argparse
import json
import time

from check_dimension_seven_five_four_charge import bit_cliques, digest, dot, mask


def build(max_states=30000, max_visits=120000, seconds=20.0):
    if not __debug__:
        raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
    if min(max_states, max_visits, seconds) <= 0:
        raise ValueError('Search limits must be positive.')
    started = time.monotonic()
    root = Path(__file__).parents[1]
    source = root / 'results/dimension-7-four-five-six-roots.json'
    artifact = json.loads(source.read_text())
    representatives = [{'eta': form['eta'], 'b': form['b'], 't_source': form['t_source'],
                        'root_index': orbit['representative'],
                        'remaining': form['roots'][orbit['representative']]['remaining']}
                       for form in artifact['forms'] for orbit in form['orbits']]
    assert len(representatives) == 3258
    even = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    rows = sorted(mask(block) for block in bit_cliques(even, 7) if len(set(block) & holes) == 1)
    assert len(rows) == 224
    by_point = {point: [row for row in rows if row & (1 << point)] for point in even}
    failed = {}
    visits = 0

    def solve(remaining):
        nonlocal visits
        visits += 1
        if len(failed) >= max_states or visits > max_visits or time.monotonic() - started > seconds:
            raise RuntimeError('Bounded twelve-branch cover test incomplete; no exclusion certificate written.')
        if not remaining:
            return []
        if remaining in failed:
            return None
        pivot, options = min(((point, [row for row in by_point[point] if row & remaining == row])
                              for point in even if remaining & (1 << point)),
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
                    'root_artifact_sha256': digest(source), 'representative': record,
                    'cover': [str(row) for row in answer],
                    'visited_cover_states': visits,
                    'search_limits': {'max_states': max_states, 'max_visits': max_visits, 'seconds': seconds}}
    return {'status': 'all_twelve_source_branch_representatives_failed_pending_independent_audit',
            'root_artifact_sha256': digest(source), 'representatives': representatives,
            'failed_states': {str(state): pivot for state, pivot in sorted(failed.items())},
            'visited_cover_states': visits,
            'search_limits': {'max_states': max_states, 'max_visits': max_visits, 'seconds': seconds}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--max-states', type=int, default=30000)
    parser.add_argument('--max-visits', type=int, default=120000)
    parser.add_argument('--seconds', type=float, default=20.0)
    arguments = parser.parse_args()
    certificate = build(arguments.max_states, arguments.max_visits, arguments.seconds)
    arguments.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    print(json.dumps({'status': certificate['status'],
                      'visited_cover_states': certificate['visited_cover_states'],
                      'failed_states': len(certificate.get('failed_states', {})),
                      'cover_found': 'cover' in certificate}, indent=2))
