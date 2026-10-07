"""Build a bounded failed-state certificate for the size-four four-even-pairs profile."""
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


def array_cliques(points, size):
    blocks = []

    def visit(chosen, available):
        if len(chosen) == size:
            blocks.append(chosen)
            return
        for index, point in enumerate(available):
            visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    visit((), points)
    return blocks


def build(max_states, max_visits, seconds):
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    if min(max_states, max_visits, seconds) <= 0:
        raise ValueError('All search limits must be positive.')
    started = time.monotonic()
    points = [point for point in range(1, 128) if not dot(point, 127)]
    holes = {3, 12, 15, 48, 51, 60, 63}
    four = array_cliques(points, 4)
    first = [block for block in four if vector_sum(block) == 3
             and not any(all(dot(point, odd) for point in block) for odd in (51, 60, 63))]
    second = [block for block in four if vector_sum(block) == 12
              and all(dot(point, 12) and dot(point, 48) for point in block)]
    six = array_cliques(points, 6)
    mixed = [block for block in six if vector_sum(block) == 15]
    heptads = sorted({tuple(sorted(block + (vector_sum(block),))) for block in six})
    assert len(four) == 10080 and len(six) == 2016 and len(heptads) == 288
    assert (len(first), len(second), len(mixed)) == (112, 16, 32)
    rows = sorted(mask(block) for block in heptads if len(set(block) & holes) == 1)
    assert len(rows) == 224
    universe = mask(points)
    roots = []
    for first_block in first:
        for second_block in second:
            if set(first_block) & set(second_block):
                continue
            for mixed_block in mixed:
                if set(first_block + second_block) & set(mixed_block):
                    continue
                remaining = universe ^ mask(first_block + second_block + mixed_block)
                assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                roots.append({'first': list(first_block), 'second': list(second_block),
                              'mixed': list(mixed_block), 'remaining': str(remaining)})
    assert len(roots) == 18752 and len({item['remaining'] for item in roots}) == 18656
    by_point = {point: [row for row in rows if row & (1 << point)] for point in points}
    failed = {}
    visits = 0

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
