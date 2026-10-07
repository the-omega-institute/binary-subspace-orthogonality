"""Build a finite failed-state certificate for the completed-hole defect profile."""
from pathlib import Path
from time import monotonic
import argparse
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def vector_sum(vectors):
    result = 0
    for vector in vectors:
        result ^= vector
    return result


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def build(node_limit, time_limit):
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    if node_limit < 1 or time_limit <= 0:
        raise ValueError('Positive node and time limits are required.')
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    holes = {3, 12, 15, 48, 51, 60, 63}
    six = []
    heptads = []

    def enumerate_even(chosen, candidates):
        if len(chosen) == 6:
            six.append(chosen)
        if len(chosen) == 7:
            heptads.append(chosen)
            return
        for index, point in enumerate(candidates):
            enumerate_even(chosen + (point,), [other for other in candidates[index + 1:] if dot(point, other)])

    enumerate_even((), points)
    assert len(six) == 2016 and len(heptads) == 288
    rows = [mask(block) for block in heptads if len(set(block) & holes) == 1]
    assert len(rows) == 224
    indexed = {point: [row for row in rows if row & (1 << point)] for point in points}
    first = [block for block in six if vector_sum(block) == 15]
    second = [block for block in six if vector_sum(block) == 63]
    assert len(first) == len(second) == 32
    blocked = mask((95, 111))
    roots = []
    for left in first:
        for right in second:
            if (mask(left) | mask(right)) & blocked or set(left) & set(right):
                continue
            remaining = mask(points) ^ (mask(left) | mask(right) | blocked)
            assert remaining.bit_count() == 49 and mask(holes) & remaining == mask(holes)
            roots.append({'first': left, 'second': right, 'remaining': remaining})
    dead = {}
    started = monotonic()
    visits = 0

    def search(remaining):
        nonlocal visits
        if not remaining:
            return []
        if remaining in dead:
            return None
        visits += 1
        if visits > node_limit or monotonic() - started > time_limit:
            raise TimeoutError('Bounded node/time budget reached.')
        options = None
        pivot = None
        for point in points:
            if remaining & (1 << point):
                candidates = [row for row in indexed[point] if row & remaining == row]
                if options is None or len(candidates) < len(options):
                    pivot, options = point, candidates
                if not candidates:
                    break
        for row in options:
            suffix = search(remaining ^ row)
            if suffix is not None:
                return [row] + suffix
        dead[remaining] = pivot
        return None

    report = {'six_classes_by_forced_sum': [len(first), len(second)],
              'eligible_ordered_pairs': len(roots), 'heptad_rows': len(rows),
              'node_limit': node_limit, 'time_limit_seconds': time_limit,
              'status': 'unknown', 'completed_roots': 0}
    try:
        for root in roots:
            result = search(root['remaining'])
            report['completed_roots'] += 1
            if result is not None:
                report['status'] = 'cover_found'
                report['witness'] = {'first': root['first'], 'second': root['second'],
                                     'heptads': [[point for point in points if row & (1 << point)] for row in result]}
                return None, report
    except TimeoutError:
        return None, report
    report.update(status='all_roots_exhausted', nodes_visited=visits, failed_states=len(dead))
    certificate = {'roots': [{'first': root['first'], 'second': root['second'], 'remaining': str(root['remaining'])}
                             for root in roots],
                   'failed_states': {str(state): pivot for state, pivot in sorted(dead.items())}}
    return certificate, report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', required=True, type=Path)
    parser.add_argument('--node-limit', type=int, default=100000)
    parser.add_argument('--time-limit', type=float, default=15)
    args = parser.parse_args()
    if args.certificate.exists() or args.certificate.is_symlink():
        raise FileExistsError(args.certificate)
    certificate, report = build(args.node_limit, args.time_limit)
    if certificate is not None:
        args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    print(json.dumps(report, indent=2))
    if certificate is None:
        raise SystemExit(2)
