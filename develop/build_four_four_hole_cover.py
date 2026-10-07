"""Build a bounded failed-state certificate for the eight-odd-heptad two-six profile."""
from itertools import permutations
from pathlib import Path
from time import monotonic
import argparse
import json


def dot(left, right):
    return (left & right).bit_count() % 2


def vector_sum(vectors):
    total = 0
    for vector in vectors:
        total ^= vector
    return total


def mask(vectors):
    return sum(1 << vector for vector in vectors)


def cliques(points, size):
    output = []

    def visit(chosen, available):
        if len(chosen) == size:
            output.append(chosen)
            return
        if len(available) < size - len(chosen):
            return
        for index, point in enumerate(available):
            visit(chosen + (point,), [other for other in available[index + 1:] if dot(point, other)])

    visit((), sorted(points))
    return output


def build(node_limit, time_limit):
    if not __debug__:
        raise RuntimeError('Run this builder without -O or PYTHONOPTIMIZE.')
    if node_limit < 1 or time_limit <= 0:
        raise ValueError('Positive node and time limits are required.')
    points = [point for point in range(1, 128) if dot(point, 127) == 0]
    holes = {3, 12, 15, 48, 51, 60, 63}
    universe = mask(points)
    heptads = cliques(points, 7)
    rows = [mask(block) for block in heptads if len(set(block) & holes) == 1]
    assert len(heptads) == 288 and len(rows) == 224
    indexed = {point: [row for row in rows if row & (1 << point)] for point in points}
    roots = []
    configurations = []
    for first_other, second_other, mixed_odd in permutations((15, 51, 60)):
        first = [block for block in cliques([point for point in points if dot(point, 3) and dot(point, first_other)], 4)
                 if vector_sum(block) == first_other]
        second = [block for block in cliques([point for point in points if dot(point, 12) and dot(point, second_other)], 4)
                  if vector_sum(block) == second_other]
        mixed = cliques([point for point in points if dot(point, mixed_odd)], 6)
        assert len(first) == len(second) == 16 and len(mixed) == 32
        assert all(vector_sum(block) == mixed_odd for block in mixed)
        before = len(roots)
        for left in first:
            for right in second:
                if set(left) & set(right):
                    continue
                blocked = mask(left + right)
                for block in mixed:
                    if mask(block) & blocked:
                        continue
                    remaining = universe ^ (blocked | mask(block))
                    assert remaining.bit_count() == 49 and remaining & mask(holes) == mask(holes)
                    roots.append({'configuration': [first_other, second_other, mixed_odd],
                                  'first': list(left), 'second': list(right), 'mixed': list(block),
                                  'remaining': str(remaining)})
        configurations.append({'configuration': [first_other, second_other, mixed_odd],
                               'class_catalog_sizes': [len(first), len(second), len(mixed)],
                               'disjoint_partial_triples': len(roots) - before})
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

    report = {'status': 'unknown', 'configurations': configurations, 'even_heptads': len(heptads),
              'eligible_heptad_rows': len(rows), 'eligible_ordered_roots': len(roots),
              'node_limit': node_limit, 'time_limit_seconds': time_limit, 'completed_roots': 0}
    try:
        for root in roots:
            solution = search(int(root['remaining']))
            report['completed_roots'] += 1
            if solution is not None:
                report['status'] = 'cover_found'
                report['witness'] = {'root': root, 'heptads': [[point for point in points if row & (1 << point)] for row in solution]}
                return None, report
    except TimeoutError:
        return None, report
    report.update(status='all_roots_exhausted', nodes_visited=visits, failed_states=len(dead))
    return {'roots': roots, 'failed_states': {str(state): pivot for state, pivot in sorted(dead.items())}}, report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', required=True, type=Path)
    parser.add_argument('--node-limit', type=int, default=100000)
    parser.add_argument('--time-limit', type=float, default=30)
    args = parser.parse_args()
    if args.certificate.exists() or args.certificate.is_symlink():
        raise FileExistsError(args.certificate)
    certificate, report = build(args.node_limit, args.time_limit)
    if certificate is not None:
        args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    print(json.dumps(report, indent=2))
    if certificate is None:
        raise SystemExit(2)
