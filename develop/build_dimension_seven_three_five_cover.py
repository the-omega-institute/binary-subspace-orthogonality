"""Build a bounded failed-state certificate for the normalized three-plus-five even cover."""
from itertools import combinations
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


def build(max_states, max_visits, seconds):
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    if min(max_states, max_visits, seconds) <= 0:
        raise ValueError('All search limits must be positive.')
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    five_candidates = [point for point in points if dot(point, 48) and dot(point, 51) and not dot(point, 95)]
    six_candidates = [point for point in points if dot(point, 60) and not dot(point, 96)]
    five = [block for block in combinations(five_candidates, 3) if vector_sum(block) == 95
            and all(dot(left, right) for left, right in combinations(block, 2))]
    six = [block for block in combinations(six_candidates, 5) if vector_sum(block) == 96
           and all(dot(left, right) for left, right in combinations(block, 2))]
    all_six = []

    def enumerate_six(chosen, available):
        if len(chosen) == 6:
            all_six.append(chosen)
            return
        for index, point in enumerate(available):
            enumerate_six(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    enumerate_six((), points)
    mixed = [block for block in all_six if vector_sum(block) == 63]
    heptads = sorted({tuple(sorted(block + (vector_sum(block),))) for block in all_six})
    assert len(all_six) == 2016 and len(heptads) == 288
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224 and (len(five), len(six), len(mixed)) == (4, 6, 32)
    roots = []
    universe = mask(points)
    for first in five:
        for second in six:
            for third in mixed:
                if set(first) & set(second) or set(first) & set(third) or set(second) & set(third):
                    continue
                remaining = universe ^ mask(first + second + third)
                assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                roots.append({'five_even': list(first), 'six_even': list(second),
                              'mixed_even': list(third), 'remaining': str(remaining)})
    assert len(roots) == 400
    by_point = {point: [row for row in rows if row & (1 << point)] for point in points}
    failed = {}
    visits = 0
    started = time.monotonic()

    def solve(remaining):
        nonlocal visits
        visits += 1
        if visits > max_visits or len(failed) >= max_states or time.monotonic() - started > seconds:
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

    for root in roots:
        if solve(int(root['remaining'])) is not None:
            raise RuntimeError('A normalized even cover exists; no exclusion certificate written.')
    return {'roots': roots, 'failed_states': {str(state): pivot for state, pivot in sorted(failed.items())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--max-states', type=int, default=50000)
    parser.add_argument('--max-visits', type=int, default=500000)
    parser.add_argument('--seconds', type=float, default=60)
    args = parser.parse_args()
    certificate = build(args.max_states, args.max_visits, args.seconds)
    args.certificate.write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps({'status': 'failed_state_certificate_written_pending_independent_audit',
                      'roots': len(certificate['roots']), 'failed_states': len(certificate['failed_states'])}, indent=2))
