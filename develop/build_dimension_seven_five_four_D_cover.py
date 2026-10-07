"""Build a bounded certificate for normal form D of the pure-five/four-even profile."""
from pathlib import Path
import argparse
import json
import time


def dot(left, right):
    return (left & right).bit_count() % 2


def vector_sum(vectors):
    total = 0
    for vector in vectors:
        total ^= vector
    return total


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
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    if min(max_states, max_visits, seconds) <= 0:
        raise ValueError('All search limits must be positive.')
    started = time.monotonic()
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    five = [block for block in array_cliques(points, 5) if vector_sum(block) == 63 and len(set(block) & holes) == 1]
    four = [block for block in array_cliques([point for point in points if dot(point, 48) and dot(point, 15)], 4)
            if vector_sum(block) == 48]
    mixed_left = array_cliques([point for point in points if dot(point, 3)], 6)
    mixed_right = array_cliques([point for point in points if dot(point, 12)], 6)
    heptads = array_cliques(points, 7)
    assert (len(five), len(four), len(mixed_left), len(mixed_right), len(heptads)) == (96, 16, 32, 32, 288)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    universe = mask(points)
    roots = []
    for first in five:
        hole = next(iter(set(first) & holes))
        for second in four:
            if set(first) & set(second):
                continue
            for left in mixed_left:
                if set(left) & set(first + second):
                    continue
                for right in mixed_right:
                    if set(right) & set(first + second + left):
                        continue
                    remaining = universe ^ mask(first + second + left + right)
                    assert remaining.bit_count() == 42 and remaining & mask(holes) == mask(holes - {hole})
                    roots.append({'five': list(first), 'four': list(second), 'mixed_left': list(left),
                                  'mixed_right': list(right), 'hole': hole, 'remaining': str(remaining)})
    assert len(roots) == 62976 and len({row['remaining'] for row in roots}) == 54448
    by_point = {point: [row for row in rows if row & (1 << point)] for point in points}
    failed = {}
    visits = 0

    def solve(remaining):
        nonlocal visits
        visits += 1
        if len(failed) >= max_states or visits > max_visits or time.monotonic() - started > seconds:
            raise RuntimeError('Bounded target search exhausted; no exclusion certificate written.')
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

    for record in roots:
        if solve(int(record['remaining'])) is not None:
            raise RuntimeError('A normalized even cover exists; no exclusion certificate written.')
    return {'roots': roots, 'failed_states': {str(state): pivot for state, pivot in sorted(failed.items())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--max-states', type=int, default=150000)
    parser.add_argument('--max-visits', type=int, default=1000000)
    parser.add_argument('--seconds', type=float, default=30)
    args = parser.parse_args()
    certificate = build(args.max_states, args.max_visits, args.seconds)
    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    print(json.dumps({'status': 'failed_state_certificate_written_pending_independent_audit',
                      'roots': len(certificate['roots']), 'failed_states': len(certificate['failed_states'])}, indent=2))
